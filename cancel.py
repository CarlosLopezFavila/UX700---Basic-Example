from ux700 import cancel_sale
import requests, json

amount2refund = 300.0
originalAmount =  28.33 # MXN or USD

try:
    payment = cancel_sale(amount=originalAmount)
    data = payment.json()
    print(json.dumps(data, indent=4))
except requests.exceptions.Timeout:
    print("Error: Timeout exceded.")