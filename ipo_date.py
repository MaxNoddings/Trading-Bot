import yfinance as yf

def get_ipo_date(ticker):
    """Gets the estimated IPO date of a stock using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="max")
        return hist.index.min().date()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Get IPO dates for two stocks
stock1 = "NVDA"
stock2 = "GME"
ipo_date1 = get_ipo_date(stock1)
ipo_date2 = get_ipo_date(stock2)

# Compare IPO dates and select the most recent
if ipo_date1 > ipo_date2:
    print(f"{stock1} has a more recent IPO of {ipo_date1}.")
    print(f"{stock2}'s was on {ipo_date2}.")
elif ipo_date2 > ipo_date1:
    print(f"{stock2} has a more recent IPO of {ipo_date2}.")
    print(f"{stock1}'s was on {ipo_date1}.")
else:
    print("Both stocks have the same IPO date.")