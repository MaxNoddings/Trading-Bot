import argparse
import yfinance as yf
import pandas as pd
from statsmodels.tsa.stattools import coint

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
    company_name1 = tickerObject1.info.get("longName", "Name not available")
    tickerSymbol2 = args.ticker2
    tickerObject2 = yf.Ticker(tickerSymbol2)
    company_name2 = tickerObject2.info.get("longName", "Name not available")

    # cokeTicker = 'KO'  # Coca-Cola
    # pepsiTicker = 'PEP'  # PepsiCo
    # print("\nCoke and Pepsi -------------------------------------------")
    
    print(f"\n{company_name1} ({tickerSymbol1}) and {company_name2} ({tickerSymbol2}) -------------------------------------")

    cointegration, correlation = analyze_cointegration_and_correlation(tickerSymbol1, tickerSymbol2, '1978-01-13', '2024-12-08')
    print(f"Cointegration p-value: {cointegration}")
    print(f"Correlation coefficient: {correlation}")

    print("\nNext Trial")

if __name__ == "__main__":
    main()