import yfinance as yf

# Fetch historical data for two stocks
stock1 = yf.download("AAPL", start="2015-01-01", end="2024-11-15")
stock2 = yf.download("MSFT", start="2015-01-01", end="2024-11-15")
stock3 = yf.download("NVDA", start="2015-01-01", end="2024-11-22")

# Extract adjusted close prices
prices1 = stock1['Adj Close']
prices2 = stock2['Adj Close']
prices3 = stock3['Adj Close']

# Save to CSV for offline use
prices1.to_csv("AAPL.csv")
prices2.to_csv("MSFT.csv")
prices3.to_csv("NVDA.csv")