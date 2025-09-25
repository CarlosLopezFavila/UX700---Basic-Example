from ux700 import do_sale
import requests

amount = 10.00  # MXN or USD

try:
    payment = do_sale(amount=amount)
    
    if payment.status_code == 200:
        data = payment.json()
        acquirer_code = data.get("payment", {}).get("acquirerResponseCode")
        acquirer_message = data.get("payment", {}).get("acquirerResponseMessage")
        auth_result = data.get("payment", {}).get("authResult", "")
        print(f"Status: {auth_result}\nCode: {acquirer_code}\nMessage: {acquirer_message}")
    else:
        print(f"Error.\nConnection with terminal failed.\n"\
                "Payment rejected.\nHTTP Status: {payment.status_code}")

except requests.exceptions.Timeout:
    print("Error: Timeout exceded.")