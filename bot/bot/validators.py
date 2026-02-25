bot/validators.py
def validate_inputs(symbol, side, order_type, qty, price):

    if side not in ("BUY", "SELL"):
        raise ValueError("Side must be BUY or SELL")

    if order_type not in ("MARKET", "LIMIT"):
        raise ValueError("Type must be MARKET or LIMIT")

    if qty <= 0:
        raise ValueError("Quantity must be > 0")

    if order_type == "LIMIT" and not price:
        raise ValueError("LIMIT order requires price")
