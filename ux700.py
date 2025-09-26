"""
Defines every function to make a request to the payment terminal API.
"""

import requests as r

# URL BASE: IP Address of terminal UX700
URL_BASE = "http://10.0.1.4:8421"

STATUS_ENDPOINT = "/avotechPayApi/v2/getStatus"
DO_SALE_ENDPOINT = "/avotechPayApi/v2/doSale"
LAST_TXN_ENDPOINT = "/avotechPayApi/v2/lastTxn"
RESTART_ENDPOINT = "/avotechPayApi/v2/RestartUx"
REFUND_ENDPOINT = "/avotechPayApi/v2/Refund"
PRINT_ENDPOINT = "/avotechPayApi/v2/Print"
CANCEL_ENDPOINT = "/avotechPayApi/v2/Void"
SEND_HB = "/avotechPayApi/v2/SendHB"

# Timeout for HTTP requests (seconds)/Refund
TIMEOUT = 30


def status():
    """Check terminal status."""
    return r.get(URL_BASE + STATUS_ENDPOINT, timeout=TIMEOUT)


def restart():
    """Restart the terminal."""
    return r.get(URL_BASE + RESTART_ENDPOINT, timeout=TIMEOUT)


def do_sale(
    amount=0,
    tip=0,
    currency="MXN",
    promo=None,
    promo_months=0,
    promo_deferral=0,
    receipt_type=None,
    mobile_number="+525500000000",
    email="nobody@avotech.mx"
):
    """Process a sale transaction."""
    payload = {
        "storeId": "01-987654321-001", #it must be changed depending on the store
        "amount": amount,
        "tip": tip,
        "currency": currency,
        "promoType": promo,
        "promoMonths": promo_months,
        "promoDeferral": promo_deferral,
        "customer": None,
        "reference": "I-93253093-J76", #static for examples,but must be changed by the store on each sale
        "seller": "Kiosko7",
        "receiptType": receipt_type,
        "mobileNumber": mobile_number,
        "email": email
    }
    #TPV Internal timeout = 30, so  the request timeout should be more or equal to 30
    return r.post(URL_BASE + DO_SALE_ENDPOINT, json=payload,timeout=40)


def last_txn():
    """Get last transaction details."""
    return r.get(URL_BASE + LAST_TXN_ENDPOINT, timeout=TIMEOUT)


def refund(
    original_amount=0,
    refund_amount=0,
    original_system_trace_audit_number=569874236528,
    receipt_type=None,
    mobile_number="+525500000000",
    email="nobody@avotech.mx"
):
    """Process a refund."""
    payload = {
        "originalAmount": original_amount,
        "originalReference": "I-93253093-J76", #static for examples,but must be changed by the store on each sale
        "originalsystemTraceAuditNumber": original_system_trace_audit_number,
        "refundAmount": refund_amount,
        "receiptType": receipt_type,
        "mobileNumber": mobile_number,
        "email": email
    }
    return r.post(URL_BASE + REFUND_ENDPOINT, json=payload, timeout=TIMEOUT)


def print_receipt(
    original_system_trace_audit_number=569874236528,
    last_transaction=False,
    receipt_type=None,
    mobile_number="+525500000000",
    email="nobody@avotech.mx"
):
    """Print a receipt."""
    payload = {
        "originalReference": "I-93253093-J76", #static for examples,but must be changed by the store on each sale
        "originalsystemTraceAuditNumber": original_system_trace_audit_number,
        "lastTxn": last_transaction,
        "receiptType": receipt_type,
        "mobileNumber": mobile_number,
        "email": email
    }
    return r.post(URL_BASE + PRINT_ENDPOINT, json=payload, timeout=TIMEOUT)


def cancel_sale(
    amount=0,
    last_transaction=False,
    receipt_type=None,
    email="nobody@avotech.mx",
    mobile_number="+525500000000"
):
    """Cancel a sale."""
    payload = {
        "originalAmount": amount,
        "originalReference": "I-93253093-J76", #static for examples,but must be changed by the store on each sale
        "originalsystemTraceAuditNumber": 569874236528,
        "lastTxn": last_transaction,
        "receiptType": receipt_type,
        "mobileNumber": mobile_number,
        "email": email
    }
    return r.post(URL_BASE + CANCEL_ENDPOINT, json=payload, timeout=TIMEOUT)

def send_hb():
    """Send Heart Beat"""
    return r.get(URL_BASE + SEND_HB, timeout=TIMEOUT)
