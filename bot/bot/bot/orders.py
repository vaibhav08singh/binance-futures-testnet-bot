bot/orders.py
import logging
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def place_order(client, symbol, side, order_type, qty, price=None):

    params = {
        "symbol": symbol.upper(),
        "side": side,
        "type": order_type,
        "quantity": qty,
        "recvWindow": 5000
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    logging.info(f"REQUEST -> {params}")

    res = client.futures_create_order(**params)

    logging.info(f"RESPONSE -> {res}")

    return res
