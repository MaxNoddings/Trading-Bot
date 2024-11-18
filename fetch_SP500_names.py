import pandas as pd

# Fetch S&P 500 symbols from Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp500_table = pd.read_html(url, header=0)[0]
sp500_symbols = sp500_table['Symbol'].tolist()

# print(f"Found {len(sp500_symbols)} symbols: {sp500_symbols[:10]}...")  # Print first 10 symbols

print(f"Found {len(sp500_symbols)} symbols: {sp500_symbols}")

