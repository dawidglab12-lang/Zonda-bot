import os
import json
import time
import requests
from datetime import datetime
from decimal import Decimal

# Wczytaj config
with open("config.json") as f:
    config = json.load(f)

BUY_THRESHOLD = config["buy_threshold"]
SELL_THRESHOLD = config["sell_threshold"]
TRADE_PERCENT = config["trade_amount_percent"]
MAX_POSITIONS = config["max_open_positions"]
TRADING_PAIRS = config["trading_pairs"]
CHECK_INTERVAL = config["check_interval_seconds"]

API_PUBLIC = os.getenv("ZONDA_API_PUBLIC")
API_PRIVATE = os.getenv("ZONDA_API_PRIVATE")

open_positions = {}

def get_ticker(pair):
    url = f"https://api.zondacrypto.exchange/rest/trading/ticker/{pair}"
    r = requests.get(url)
    return r.json()

def get_balance():
    # Tu można pobrać saldo konta z API
    return Decimal("10000")  # przykładowa wartość testowa

def place_order(pair, side, amount):
    print(f"[{datetime.now()}] {side.upper()} {amount} {pair}")

while True:
    if len(open_positions) < MAX_POSITIONS:
        for pair in TRADING_PAIRS:
            ticker = get_ticker(pair)
            try:
                rate = Decimal(ticker["ticker"]["rate"])
                highest = Decimal(ticker["ticker"]["highestBid"])
                change_percent = ((rate - highest) / highest) * 100

                if change_percent <= BUY_THRESHOLD and pair not in open_positions:
                    balance = get_balance()
                    trade_amount = (balance * Decimal(TRADE_PERCENT) / 100) / rate
                    place_order(pair, "buy", trade_amount)
                    open_positions[pair] = rate

            except Exception as e:
                print(f"Błąd przy {pair}: {e}")

    to_sell = []
    for pair, buy_rate in open_positions.items():
        ticker = get_ticker(pair)
        try:
            rate = Decimal(ticker["ticker"]["rate"])
            profit_percent = ((rate - buy_rate) / buy_rate) * 100

            if profit_percent >= SELL_THRESHOLD:
                balance = get_balance()
                place_order(pair, "sell", balance)
                to_sell.append(pair)

        except Exception as e:
            print(f"Błąd sprzedaży {pair}: {e}")

    for pair in to_sell:
        del open_positions[pair]

    time.sleep(CHECK_INTERVAL)
