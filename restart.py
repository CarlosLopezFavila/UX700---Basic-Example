import json, requests
from ux700 import restart

try:
    restart_ux = restart()
    print(json.dumps(restart_ux.json(),indent=4))
except requests.exceptions.Timeout:
    print("Error: Timeout exceded.")