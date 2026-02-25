bot/client.py
from binance.client import Client

TESTNET = "https://testnet.binancefuture.com"

def create_client(key, secret):
    client = Client(key, secret)
    client.FUTURES_URL = TESTNET
    return client
