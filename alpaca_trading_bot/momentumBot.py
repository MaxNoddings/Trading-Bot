from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
import time
import datetime

API_KEY = 'API_KEY'
SECRET_KEY = 'SECRET_KEY'
BASE_URL = 'https://paper-api.alpaca.markets'

api = REST(API_KEY, SECRET_KEY, BASE_URL)

def get_signal(symbol):
    bars = api.get_bars(symbol, TimeFrame.Day, limit=15).df
    sma_short = bars['close'].rolling(5).mean().iloc[-1]
    sma_long = bars['close'].rolling(10).mean().iloc[-1]
    if sma_short > sma_long:
        return "buy"
    else:
        return "sell"

def run_bot():
    symbols = ["AAPL", "MSFT", "TSLA"]  # example universe
    for symbol in symbols:
        signal = get_signal(symbol)
        position = None
        try:
            position = api.get_position(symbol)
        except:
            pass
        if signal == "buy" and not position:
            api.submit_order(symbol=symbol, qty=1, side='buy', type='market', time_in_force='day')
            print(f"{datetime.datetime.now()}: BUY {symbol}")
        elif signal == "sell" and position:
            api.submit_order(symbol=symbol, qty=1, side='sell', type='market', time_in_force='day')
            print(f"{datetime.datetime.now()}: SELL {symbol}")

# Run every X minutes during market hours
while True:
    now = datetime.datetime.now()
    print(f"Running the Stockbot at {now.strftime('%Y-%m-%d %H:%M:%S')}")
    if now.weekday() < 5 and now.hour >= 9 and now.hour <= 16:
        run_bot()
    else:
        print("Market is closed. Waiting for next trading day.")

    # time.sleep(60 * 15)  # run every 15 min
    time.sleep(15)