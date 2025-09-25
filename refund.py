from ux700 import refund
import requests, json

amount2refund = 300.0
originalAmount =  28.33 # MXN or USD

try:
    payment = refund(original_amount=originalAmount, refund_amount=amount2refund)
    data = payment.json()
    print(json.dumps(data, indent=4))
except requests.exceptions.Timeout:
    print("Error: Timeout exceded.")