import requests, json
from ux700 import last_txn

try:
    last_transaction = last_txn()
    print(json.dumps(last_transaction.json(),indent=4))
except requests.exceptions.Timeout:
    print("Error: Timeout exceded.")