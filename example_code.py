import ux700, time, json, requests, phonenumbers
from iso_codes import ISO_CODES
from email_validator import validate_email, EmailNotValidError
from phonenumbers import NumberParseException



def menu():
    while True:
        try:
            option = int(input(
                "-------- MENU --------\n"
                "1. Initiate Payment\n"
                "2. Print Last Transaction\n"
                "3. Print a Sale\n"
                "4. Cancel a Sale\n"
                "5. Send HeartBeat\n"
                "6. Start a Refund\n"
                "7. Restart Terminal\n"
                "8. Close\n"
                "Select an option: "
            ))
            if 1 <= option <= 8:
                return option
            print("\nInvalid option. Please select a number between 1 and 8.\n")
        except ValueError:
            print("\nInvalid input. Please type a valid number.\n")

def handle_response(response, success_msg, unknown_msg="Unknown response. Please contact support"):
    if response.status_code == 200:
        print(f"\n{success_msg}")
        data = response.json()
        print(json.dumps(data, indent=4))
        acquirer_code = data.get("payment", {}).get("acquirerResponseCode")
        if acquirer_code:
            print(ISO_CODES.get(acquirer_code, unknown_msg))
    else:
        print(f"\nOperation failed - Status Code: {response.status_code} - Reason: {response.reason}")
    print()
    time.sleep(2)


def option_y_n(ask_y_n="", ask_var=""):
    while True:
        yes_or_no = input(ask_y_n)
        if yes_or_no == 'y' or yes_or_no == "Y":
            return input(ask_var)
        elif yes_or_no == "n"  or yes_or_no == "N":
            return None
        else:
            print("The input should be only 'y' or 'n'. Try again.")


def is_valid_phone_library(phone, country_code=None):
    """Function to validate a mobile number."""
    try:
        parsed_number = phonenumbers.parse(phone, country_code)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False

def process_option(option):
    if option == 1:
        print("\nPayment Selected.")
        try:
            status_resp = ux700.status()
            if status_resp.status_code != 200:
                print("\nTerminal is inactive.\n")
                return True
            amount = float(input("\nEnter the payment amount: "))
            if amount <= 0:
                print("The amount must be greater than zero.")
                return True
            # ========================= to print a receipt ==========================
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
                                while True:
                                    email = input("\nPlease enter your email: ").strip()
                                    try:
                                        valid_email = validate_email(email).email
                                        print(valid_email)
                                        receipt = "email"
                                        break
                                    except EmailNotValidError as e:
                                        print(f"Please enter a valid email address: {str(e)}")
                                break
                            elif receipt_type == 2:
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

            # ========================= to select a promo type ==========================
            promo = None
            promo_type = None
            promo_months = None
            promo_deferral = None

            while True:
                promo = input("\nWould you like interest-free installments or installments with interest? (y/n): ").strip().lower()
                
                if promo == "y":
                    while True: 
                        try:
                            print("\nWhich type of promo do you want:")
                            print("1. Interest-free installments")
                            print("2. Installments with interest")
                            
                            promo_opt = int(input("Type your option (1-2): "))
                            
                            if promo_opt == 1:
                                promo_type = "MSI"
                                break 
                            elif promo_opt == 2:
                                promo_type = "MCI"
                                break
                            else:
                                print("Please enter 1 or 2 only.")
                        except ValueError:
                            print("Please enter a valid number (1 or 2).")
                            time.sleep(1)  

                    #---------- promo months -----------    
                    while True:
                        try:
                            promo_months = int(input("How many months will last the promo? (3,6,9,12 only): "))
                            if promo_months in [3,6,9,12]:
                                break
                            else:
                                print("Please enter a valid number (3, 6, 9 or 12). ")
                                time.sleep(1)
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    #-------- promo deferral ---------
                    while True:
                        try:
                            promo_deferral = int(input("When would you like your payments to start (0,1,2 months)?: "))  # Variable diferente
                            if promo_deferral in [0,1,2]:
                                break
                            else:
                                print("Please enter a valid number (0, 1 or 2). ")
                                time.sleep(1)
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    break  
                    
                elif promo == 'n':
                    print("\nNo promo has been selected.")
                    break
                else: 
                    print("Please enter 'y' for yes or 'n' for no.")

            print("\nProcessing payment. Please confirm on the terminal...")
            payment = ux700.do_sale(amount=amount, receipt_type=receipt,email=valid_email,mobile_number=number,
                                    promo=promo_type,promo_months=promo_months, 
                                    promo_deferral=promo_deferral)
            handle_response(payment, "Payment successful")
            acquirer_code = payment.json().get("payment", {}).get("acquirerResponseCode")
            acquirer_message = payment.json().get("payment", {}).get("acquirerResponseMessage")
            auth_result = payment.json().get("payment", {}).get("authResult", "")
            print(f"Acquirer Code: {acquirer_code}\nAcquirer Message: {acquirer_message}\nAuth Result: {auth_result}\n")
        except ValueError:
            print("\nInvalid amount. Please try again.\n")
        except requests.exceptions.Timeout:
            print("\nError: Timeout exceeded. Please try again.")
        time.sleep(1)

    elif option == 2:
        print("\nPrint Last Transaction selected.")
        print("\nRetrieving the last transaction, please wait...")
        last_txn = ux700.last_txn()
        handle_response(last_txn, "Last Transaction retrieved successfully")
        acquirer_code = last_txn.json().get("payment", {}).get("acquirerResponseCode")
        acquirer_message = last_txn.json().get("payment", {}).get("acquirerResponseMessage")
        auth_result = last_txn.json().get("payment", {}).get("authResult", "")
        print(f"Acquirer Code: {acquirer_code}\nAcquirer Message: {acquirer_message}\nAuth Result: {auth_result}")
        time.sleep(1)

    elif option == 3:
        print("\nPrint a Sale selected.")
        print("Requesting receipt print, please wait...")
        printed = ux700.print_receipt()
        handle_response(printed, "Receipt printed successfully")
        time.sleep(1)

    elif option == 4:
        print("\nCancel a Sale selected.")
        print("Requesting cancellation of the last sale...")
        cancelled = ux700.cancel_sale()
        handle_response(cancelled, "Sale cancelled successfully")
        time.sleep(1)

    elif option == 5:
        print("\nSend HeartBeat selected.")
        print("Sending heartbeat to terminal...")
        heartbeat = ux700.send_hb()
        handle_response(heartbeat, "Heartbeat sent successfully. Connection established.")
        time.sleep(1)

    elif option == 6:
        print("\nStart a Refund selected.")
        print("Processing refund request, please confirm on the terminal...")
        refund = ux700.refund()
        handle_response(refund, "Refund processed successfully")
        time.sleep(1)

    elif option == 7:
        print("\nRestart Terminal selected.")
        print("Restarting the terminal, please wait...")
        restart = ux700.restart()
        handle_response(restart, "Terminal restarted successfully")
        print("Exiting program.")
        time.sleep(2)
        return False

    elif option == 8:
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
