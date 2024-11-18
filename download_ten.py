import yfinance as yf
import pandas as pd

# List of stocks
ten_stocks_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'PLTR', 'BA', 'TSLA', 'GME', 'ADBE', 'HD']  # Add more symbols

# Empty DataFrame to store downloaded data
data = pd.DataFrame()

try:
    for i, symbol in enumerate(ten_stocks_symbols, start=1):
        print(f"Downloading {symbol} ({i}/{len(ten_stocks_symbols)})")
        stock_data = yf.download(symbol, start='2015-01-01', end='2023-01-01')['Adj Close']
        data[symbol] = stock_data
except KeyboardInterrupt:
    print("Download interrupted by user!")

# Save the downloaded data to a file if needed
data.to_csv('ten_stocks_data.csv')
print("Download complete or partially saved.")