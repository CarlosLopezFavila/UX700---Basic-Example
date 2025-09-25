import json, os, requests
from ux700 import status

while True: 
    try:
        estado = status()
        os.system('cls')
        print(json.dumps(estado.json(),indent=4))
    except requests.exceptions.Timeout:
        print("Error: Timeout exceded.")