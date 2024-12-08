import argparse
import datetime
import yfinance as yf
import pandas as pd
from statsmodels.tsa.stattools import coint

def get_ipo_date(tickerObject):
    """Gets the estimated IPO date of a stock using yfinance."""
    try:
        hist = tickerObject.history(period="max")
        return hist.index.min().date()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def analyze_cointegration_and_correlation(stock1, stock2, start_date, end_date):
    """
    Analyzes the cointegration and correlation between two stocks.
    
    Parameters:
        stock1 (str): Ticker symbol for the first stock.
        stock2 (str): Ticker symbol for the second stock.
        start_date (str): Start date for historical data in 'YYYY-MM-DD' format.
        end_date (str): End date for historical data in 'YYYY-MM-DD' format.
    
    Returns:
        (float, float): Cointegration p-value and Correlation coefficient.
    """
    # Download adjusted close prices for the two stocks
    data = yf.download([stock1, stock2], start=start_date, end=end_date)['Adj Close']
    
    # Ensure we have no missing data
    data = data.dropna()
    
    # Extract the price series
    stock1_prices = data[stock1]
    stock2_prices = data[stock2]
    
    # Calculate correlation
    correlation = stock1_prices.corr(stock2_prices)
    
    # Perform cointegration test
    coint_result = coint(stock1_prices, stock2_prices)
    cointegration_p_value = coint_result[1]  # Extract p-value
    
    return cointegration_p_value, correlation

def main():
    # Set up argparse
    parser = argparse.ArgumentParser(description="Calculate correlation and cointegration between two stocks.")
    parser.add_argument("ticker1", type=str, help="The first stock ticker symbol (e.g., AAPL).")
    parser.add_argument("ticker2", type=str, help="The second stock ticker symbol (e.g., MSFT).")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get tickers and their company names from command-line arguments
    tickerSymbol1 = args.ticker1
    tickerObject1 = yf.Ticker(tickerSymbol1)
    ipo_date1 = get_ipo_date(tickerObject1)
    company_name1 = tickerObject1.info.get("longName", "Name not available")
    tickerSymbol2 = args.ticker2
    tickerObject2 = yf.Ticker(tickerSymbol2)
    ipo_date2 = get_ipo_date(tickerObject2)
    company_name2 = tickerObject2.info.get("longName", "Name not available")

    # Compare IPO dates and select the most recent
    if ipo_date1 > ipo_date2:
        start_date = ipo_date1
        print(f"{tickerSymbol1} has a more recent IPO of {ipo_date1}.")
        print(f"{tickerSymbol2}'s was on {ipo_date2}.")
    elif ipo_date2 > ipo_date1:
        start_date = ipo_date2
        print(f"{tickerSymbol2} has a more recent IPO of {ipo_date2}.")
        print(f"{tickerSymbol1}'s was on {ipo_date1}.")
    
    # Todays date
    today = datetime.date.today()
    formatted_date = today.strftime("%Y-%m-%d")

    print(f"The start date is: {start_date}")
    print(f"The end date is: {formatted_date}")
    
    print(f"\n{company_name1} ({tickerSymbol1}) and {company_name2} ({tickerSymbol2}) -------------------------------------")

    cointegration, correlation = analyze_cointegration_and_correlation(tickerSymbol1, tickerSymbol2, start_date, formatted_date)
    print(f"Cointegration p-value: {cointegration}")
    print(f"Correlation coefficient: {correlation}")

    print("\nNext Trial")

if __name__ == "__main__":
    main()