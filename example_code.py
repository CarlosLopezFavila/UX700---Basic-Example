"""
Example script demonstrating how to interact with the Verifone UX700 payment terminal.
Includes initiating payments, printing last transactions, sending heartbeat signals, 
and restarting the terminal.
"""
import ux700, time, json, requests, phonenumbers
from email_validator import validate_email, EmailNotValidError
from phonenumbers import NumberParseException


def menu():
    """Show the main menu and let the user select an action."""
    while True:
        try:
            option = int(input(
                "-------- MENU --------\n"
                "1. Initiate Payment\n"
                "2. Print Last Transaction\n"
                "3. Send HeartBeat\n"
                "4. Restart Terminal\n"
                "5. Close\n"
                "Select an option: "
            ))
            if 1 <= option <= 5:
                return option
            print("\nInvalid option. Please select a number between 1 and 5.\n")
        except ValueError:
            print("\nInvalid input. Please type a valid number.\n")


def handle_response(response, success_msg, unknown_msg="Unknown response. Please contact support"):
    """Show the result after sending a request to the terminal."""
    if response.status_code == 200:
        print(f"\n{success_msg}")
        time.sleep(1)
        data = response.json()
        print("Data received: ")
        print(json.dumps(data, indent=4))
    else:
        print(f"\nOperation failed - Status Code: {response.status_code} - Reason: {response.reason}\n")
    time.sleep(2)


def option_y_n(ask_y_n="", ask_var=""):
    """Ask user yes/no. If yes, request extra input (like email/phone)."""
    while True:
        yes_or_no = input(ask_y_n)
        if yes_or_no in ['y', 'Y']:
            return input(ask_var)
        elif yes_or_no in ['n', 'N']:
            return None
        else:
            print("The input should be only 'y' or 'n'. Try again.")


def is_valid_phone_library(phone, country_code=None):
    """Check if the phone number entered is valid."""
    try:
        parsed_number = phonenumbers.parse(phone, country_code)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False


def process_option(option):
    """Run the selected menu option."""
    if option == 1:
        # -------- Payment --------
        print("\nPayment Selected.")
        try:
            status_resp = ux700.status()
            if status_resp.status_code != 200:
                print("\nTerminal is inactive.\n")
                time.sleep(1)
                return True

            # Ask for payment amount
            amount = float(input("\nEnter the payment amount: "))
            while True:
                if amount <= 0:
                    print("The amount must be greater than zero.")
                else:
                    break

            # -------- Receipt handling --------
            number = None
            receipt = None
            valid_email = None
            while True:
                receipt_y_n = input("\nDo you want a receipt? (y/n): ")
                if receipt_y_n == 'y':
                    while True:
                        try:
                            print("\nWhich type of receipt do you want?")
                            print("1. Email")
                            print("2. Mobile Number")
                            receipt_type = int(input("Type your option (1-2): "))

                            if receipt_type == 1:
                                # Ask for email
                                while True:
                                    email = input("\nPlease enter your email: ").strip()
                                    try:
                                        valid_email = validate_email(email).email
                                        receipt = "email"
                                        break
                                    except EmailNotValidError as e:
                                        print(f"Please enter a valid email address: {str(e)}")
                                break
                            elif receipt_type == 2:
                                # Ask for phone number
                                while True: 
                                    number = input("\nPlease enter your mobile number: ").strip()
                                    if number and is_valid_phone_library(number, "MX"):
                                        receipt = "mobile"
                                        break
                                    else:
                                        print("Please enter a valid mobile number.")
                                break
                            else:
                                print("Please enter 1 or 2 only.")
                            break
                        except ValueError:
                            print("Please enter a valid number (1 or 2).")
                    break
                elif receipt_y_n == 'n':
                    print('\nNo receipt will be generated.')
                    time.sleep(1)
                    break
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
                    time.sleep(1)

            # -------- Promo handling --------
            promo_type = None
            promo_months = None
            promo_deferral = None

            while True:
                promo = input("\nWould you like installments with/without interest? (y/n): ").strip().lower()
                if promo == "y":
                    try:
                        print("\nWhich type of promo do you want:")
                        print("1. Interest-free installments")
                        print("2. Installments with interest")
                        promo_opt = int(input("Type your option (1-2): "))
                        if promo_opt == 1:
                            promo_type = "MSI"
                        elif promo_opt == 2:
                            promo_type = "MCI"
                    except ValueError:
                        print("Please enter a valid number (1 or 2).")
                        time.sleep(1)  

                    # Months for promo
                    while True:
                        try:
                            promo_months = int(input("How many months? (3,6,9,12 only): "))
                            if promo_months in [3,6,9,12]:
                                break
                            else:
                                print("Please enter a valid number (3, 6, 9 or 12). ")
                        except ValueError:
                            print("Please enter a valid number.")

                    # Delay before first payment
                    while True:
                        try:
                            promo_deferral = int(input("Start payments after how many months? (0,1,2): "))
                            if promo_deferral in [0,1,2]:
                                break
                            else:
                                print("Please enter a valid number (0, 1 or 2). ")
                        except ValueError:
                            print("Please enter a valid number.")
                    break
                elif promo == 'n':
                    print("\nNo promo has been selected.")
                    break
                else: 
                    print("Please enter 'y' for yes or 'n' for no.")

            # -------- Execute payment --------
            print("\nProcessing payment. Please confirm on the terminal...")
            payment = ux700.do_sale(
                amount=amount,
                receipt_type=receipt,
                email=valid_email,
                mobile_number=number,
                promo=promo_type,
                promo_months=promo_months, 
                promo_deferral=promo_deferral
            )
            handle_response(payment, "Request successful")
            acquirer_code = payment.json().get("payment", {}).get("acquirerResponseCode")
            acquirer_message = payment.json().get("payment", {}).get("acquirerResponseMessage")
            auth_result = payment.json().get("payment", {}).get("authResult", "")
            print("\nResume:")
            print(f"ISO Acquirer Code: {acquirer_code}\nISO Acquirer Message: {acquirer_message}\nTransaction Result: {auth_result}\n")

        except ValueError:
            print("\nInvalid amount. Please try again.\n")
        except requests.exceptions.Timeout:
            print("\nError: Timeout exceeded. Please try again.")
        time.sleep(1)

    elif option == 2:
        # -------- Last transaction --------
        print("\nPrint Last Transaction selected.")
        last_txn = ux700.last_txn()
        handle_response(last_txn, "Last Transaction retrieved successfully")
        acquirer_code = last_txn.json().get("payment", {}).get("acquirerResponseCode")
        acquirer_message = last_txn.json().get("payment", {}).get("acquirerResponseMessage")
        auth_result = last_txn.json().get("payment", {}).get("authResult", "")
        print("\nResume:")
        print(f"ISO Acquirer Code: {acquirer_code}\nISO Acquirer Message: {acquirer_message}\nTransaction Result: {auth_result}\n")
        time.sleep(1)

    elif option == 3:
        # -------- Heartbeat --------
        print("\nSend HeartBeat selected.")
        heartbeat = ux700.send_hb()
        handle_response(heartbeat, "Heartbeat sent successfully. Connection established.")
        time.sleep(1)

    elif option == 4:
        # -------- Restart terminal --------
        print("\nRestart Terminal selected.")
        restart = ux700.restart()
        handle_response(restart, "Terminal restarted successfully")
        print("Exiting program.")
        time.sleep(2)
        return False

    elif option == 5:
        # -------- Close program --------
        print("\nClosing program. Goodbye.")
        time.sleep(2)
        return False

    return True


print("===== Testing UX700 =====")
try:
    status_resp = ux700.status()
    if status_resp.status_code == 200:
        print("Status: ACTIVE \n")
        while True:
            selected_option = menu()
            if not process_option(selected_option):
                break
    else:
        print("Status: INACTIVE \n")
except requests.exceptions.Timeout:
    print("STATUS: INACTIVE\nError: Timeout exceeded. Please try again.")
