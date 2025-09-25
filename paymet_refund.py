import requests as r, json

# URL BASE: IP Address of terminal UX700
URL_BASE = "http://10.0.1.4:8421"
DO_SALE_ENDPOINT = "/avotechPayApi/v2/doSale"
REFUND_ENDPOINT = "/avotechPayApi/v2/Refund"
CANCEL_ENDPOINT = "/avotechPayApi/v2/Void"


def do_sale():
    """Process a sale transaction."""
    payload = {
        "storeId": "01-987654321-001",
        "amount": 275.12,
        "tip": 0,
        "currency": "MXN",
        "promoType": "MSI",
        "promoMonths": 0,
        "promoDeferral": 0,
        "customer": None,
        "reference": "I-93253093-J76",
        "seller": "Kiosko7",
        "receiptType": "email",
        "mobileNumber": "+525500000000",
        "email": "nobody@avotech.mx"
    }

    #TPV Internal timeout = 30, so  the request timeout should be more or equal to 30
    return r.post(URL_BASE + DO_SALE_ENDPOINT, json=payload,timeout=60)

def refund():
    """Process a refund."""
    payload = {
	"originalAmount": 275.12,
	"originalReference": "I-93253093-J76",
	"originalsystemTraceAuditNumber": 569874236528,
	"refundAmount": 25,
	"receiptType": "email",
	"mobileNumber": "+525500000000",
	"email": "nobody@avotech.mx"
}

    return r.post(URL_BASE + REFUND_ENDPOINT, json=payload, timeout=40)

def cancel_sale():
    """Cancel a sale."""
    payload = {
        "originalAmount": 275.12,
        "originalReference": "I-93253093-J76",
        "originalsystemTraceAuditNumber": 569874236528,
        "lastTxn": False,
        "receiptType": "email",
        "mobileNumber": "+525500000000",
        "email": "nobody@avotech.mx"
    }

    return r.post(URL_BASE + CANCEL_ENDPOINT, json=payload, timeout=40)


print("TEST")

sale = do_sale()
print(json.dumps(sale.json(), indent=4))

ref = refund()
print(json.dumps(ref.json(), indent=4))

cancel = cancel_sale()
print(json.dumps(ref.json(), indent=4))