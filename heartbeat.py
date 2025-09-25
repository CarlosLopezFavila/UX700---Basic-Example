import json, requests
from ux700 import send_hb

try:
    heartbeat = send_hb()
    print(json.dumps(heartbeat.json(),indent=4))
except requests.exceptions.Timeout:
    print("Error: Timeout exceded.")