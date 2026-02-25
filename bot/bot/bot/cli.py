cli.py
import argparse
import logging
from dotenv import load_dotenv
import os
from colorama import Fore, init

from bot.client import create_client
from bot.orders import place_order
from bot.validators import validate_inputs
from bot.logging_config import setup_logger

init(autoreset=True)
setup_logger()

load_dotenv()

API_KEY = os.getenv("BINANCE_KEY")
API_SECRET = os.getenv("BINANCE_SECRET")

def main():

    parser = argparse.ArgumentParser(description="Binance Futures Testnet Bot")

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--qty", type=float, required=True)
    parser.add_argument("--price", type=float)

    args = parser.parse_args()

    try:

        validate_inputs(
            args.symbol,
            args.side,
            args.type,
            args.qty,
            args.price
        )

        client = create_client(API_KEY, API_SECRET)

        print(Fore.CYAN + "\nORDER REQUEST")
        print(vars(args))

        # ⭐ Auto fetch market price if LIMIT price not given
        if args.type == "LIMIT" and args.price is None:
            ticker = client.futures_symbol_ticker(symbol=args.symbol)
            args.price = ticker["price"]
            print(Fore.YELLOW + f"Auto price used: {args.price}")

        result = place_order(
            client,
            args.symbol,
            args.side,
            args.type,
            args.qty,
            args.price
        )

        print(Fore.GREEN + "\nSUCCESS")
        print("OrderID:", result["orderId"])
        print("Status:", result["status"])
        print("ExecutedQty:", result["executedQty"])

        if "avgPrice" in result:
            print("AvgPrice:", result["avgPrice"])

    except Exception as e:

        logging.exception("ORDER FAILED")

        print(Fore.RED + "\nFAILED")
        print(str(e))


if __name__ == "__main__":
    main()
