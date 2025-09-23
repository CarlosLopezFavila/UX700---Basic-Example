import ux700
import json
import time

def menu():
    while True:
        try:
            option = int(input("--------MENU-------\n"\
                            "1. Initiate Payment \n" \
                            "2. Print Last Transaction\n" \
                            "3. Print a Sale\n" \
                            "4. Cancel a Sale\n" \
                            "5. Send HeartBeat\n" \
                            "6. Start a Refund\n"\
                            "7. Restart Terminal\n" \
                            "8. Close\n" \
                            "Type an option: "))
            
            if 1 <= option <= 8:
                return option
            else:
                print("\nError: The typed option must be between 1 and 7. Try Again.\n")
        except ValueError:
            print("\nError: The typed option should be a valid number. Try Again.\n")

def check_response(response, operation_name):
    """Auxiliar function to check response status"""
    if response.status_code == 200:
        print(f"\n {operation_name} successful")
        time.sleep(2)
        return True
    else:
        print(f"\n {operation_name} failed - Status Code: {response.status_code} - Reason: {response.reason}")
        time.sleep(2)
        return False

def process_option(option):
    if option == 1:
        print("\nPayment Selected.")
        try:
            amount = float(input("\nPlease enter the amount to pay: "))
            payment = ux700.do_sale(amount=amount)
            
            if check_response(payment, "Payment"):
                print(json.dumps(payment.json(), indent=4))
            print()
            time.sleep(1)
        except ValueError:
            print("\nError: The amount should be a valid number. Try Again.\n")
            time.sleep(1)

    elif option == 2:
        print("\nPrint Last Transaction selected")
        last_txn = ux700.last_txn()
        
        if check_response(last_txn, "Last Transaction"):
            print(json.dumps(last_txn.json(), indent=4))
        print()
        time.sleep(1)

    elif option == 3:
        print("\nPrint a Sale selected")
        printed = ux700.print_receipt()
        
        if check_response(printed, "Print Receipt"):
            print(json.dumps(printed.json(), indent=4))
        print()

    elif option == 4:
        print("\nCancel a Sale selected")
        cancelled = ux700.cancel_sale()
        
        if check_response(cancelled, "Cancel Sale"):
            print(json.dumps(cancelled.json(), indent=4))
        print()

    elif option == 5:
        print("\nSend HeartBeat selected")
        heartbeat = ux700.send_hb()
        
        if check_response(heartbeat, "HeartBeat"):
            print(json.dumps(heartbeat.json(), indent=4))
        print()
        time.sleep(1)
    elif option == 6:
        print("\nStart a Refund")
        refund = ux700.refund()
        
        if check_response(refund, "Refund"):
            print(json.dumps(refund.json(), indent=4))
        print()
        time.sleep(1)

    elif option == 7:
        print("\nRestart Terminal selected")
        restart = ux700.restart()
        
        if check_response(restart, "Restart"):
            print(json.dumps(restart.json(), indent=4))
            print("\nBye!")
            time.sleep(2)
            return False
        else:
            print("Restart failed, returning to menu...")
            time.sleep(2)

    elif option == 8:
        print("\nBye!")
        time.sleep(2)
        return False  # To close the program
    
    return True  # to continue on the menu

print("===== Testing UX700 =====")
status = ux700.status()
if status.status_code == 200:
    print("Status: ACTIVE \n")
    
    while True:
        selected_option = menu()
        should_continue = process_option(selected_option)
        
        if not should_continue:  # if option 7 was typed
            break
        
else:
    print("Status: INACTIVE \n")