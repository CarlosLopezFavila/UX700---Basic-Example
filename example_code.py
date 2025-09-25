import ux700, time, json, requests
from iso_codes import ISO_CODES

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

def process_option(option):
    if option == 1:
        print("\nPayment Selected.")
        try:
            status_resp = ux700.status()
            if status_resp.status_code != 200:
                print("Terminal is inactive.")
                return True
            amount = float(input("\nEnter the payment amount: "))
            if amount <= 0:
                print("The amount must be greater than zero.")
                return True
            print("Processing payment. Please confirm on the terminal...")
            payment = ux700.do_sale(amount=amount)
            handle_response(payment, "Payment successful")
            acquirer_code = payment.json().get("payment", {}).get("acquirerResponseCode")
            acquirer_message = payment.json().get("payment", {}).get("acquirerResponseMessage")
            auth_result = payment.json().get("payment", {}).get("authResult", "")
            print(f"Acquirer Code: {acquirer_code}\nAcquirer Message: {acquirer_message}\nAuth Result: {auth_result}")
        except ValueError:
            print("\nInvalid amount. Please try again.\n")
        except requests.exceptions.Timeout:
            print("Error: Timeout exceeded. Please try again.")
        time.sleep(1)

    elif option == 2:
        print("\nPrint Last Transaction selected.")
        print("Retrieving the last transaction, please wait...")
        last_txn = ux700.last_txn()
        handle_response(last_txn, "Last Transaction retrieved successfully")
        acquirer_code = last_txn.json().get("payment", {}).get("acquirerResponseCode")
        acquirer_message = last_txn.json().get("payment", {}).get("acquirerResponseMessage")
        auth_result = last_txn.json().get("payment", {}).get("authResult", "")
        print(f"Acquirer Code: {acquirer_code}\nAcquirer Message: {acquirer_message}\nAuth Result: {auth_result}")

    elif option == 3:
        print("\nPrint a Sale selected.")
        print("Requesting receipt print, please wait...")
        printed = ux700.print_receipt()
        handle_response(printed, "Receipt printed successfully")

    elif option == 4:
        print("\nCancel a Sale selected.")
        print("Requesting cancellation of the last sale...")
        cancelled = ux700.cancel_sale()
        handle_response(cancelled, "Sale cancelled successfully")

    elif option == 5:
        print("\nSend HeartBeat selected.")
        print("Sending heartbeat to terminal...")
        heartbeat = ux700.send_hb()
        handle_response(heartbeat, "Heartbeat sent successfully. Connection established.")

    elif option == 6:
        print("\nStart a Refund selected.")
        print("Processing refund request, please confirm on the terminal...")
        refund = ux700.refund()
        handle_response(refund, "Refund processed successfully")

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
