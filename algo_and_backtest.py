import argparse
import datetime
import yfinance as yf 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_ipo_date(tickerObject):
    """Gets the estimated IPO date of a stock using yfinance."""
    try:
        hist = tickerObject.history(period="max")
        return hist.index.min().date()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def get_most_recent_ipo(ticker1, ticker2):
    tickerObject1 = yf.Ticker(ticker1)
    tickerObject2 = yf.Ticker(ticker2)
    ipo_date1 = get_ipo_date(tickerObject1)
    ipo_date2 = get_ipo_date(tickerObject2)

    # Compare IPO dates and select the most recent
    if ipo_date1 > ipo_date2:
        return ipo_date1
    elif ipo_date2 > ipo_date1:
        return ipo_date2
    else:
        return ipo_date2



def update_positions(row, prev_position):
    if row['Enter']:  # Open command
        return 1
    elif row['Exit']:  # Close command
        return 0
    else:  # No change, keep the previous state
        return prev_position

def calculate_returns(data):
    # Initialize variables
    cumulative_returns = 0  # Cumulative return in dollars
    initial_portfolio_value = 0 # Initial Portfolio Value upon the first trade
    entry_price_aapl = 0    # Entry price for AAPL
    entry_price_msft = 0    # Entry price for MSFT
    trade_count = 0         # Count the number of trades
    completed_trades = 0    # Number of completed trades
    days_elapsed = 0 # Count the number of days elapsed for each trade
    
    # Iterate through the DataFrame to track trades
    for i in range(1, len(data)):
        # Get current and previous rows
        current_row = data.iloc[i]
        prev_row = data.iloc[i - 1]

        # Add one to days elapsed
        days_elapsed += 1

        # Check for position changes
        if prev_row['Position'] == 0 and current_row['Position'] == 1:
            # Reset days elapsed to 0, since a new trade is starting
            days_elapsed = 0
            
            # Set the Initial Portfolio Value upon the first trade
            if trade_count == 0:
                initial_portfolio_value = current_row['AAPL'] + current_row['MSFT']
            
            # Enter trade based on Z-Score
            trade_count += 1
            entry_date = current_row.name 
            if current_row['Z_Score'] < 0:
                # Long AAPL, Short MSFT
                entry_price_aapl = current_row['AAPL']
                entry_price_msft = current_row['MSFT']
                trade_direction = "Long AAPL, Short MSFT"
            else:
                # Short AAPL, Long MSFT
                entry_price_aapl = current_row['AAPL']
                entry_price_msft = current_row['MSFT']
                trade_direction = "Short AAPL, Long MSFT"

            print(f"Trade {trade_count}: Enter {trade_direction}")
            print(f"Trade {trade_count}: Enter at AAPL=${entry_price_aapl:.2f}, MSFT=${entry_price_msft:.2f} ({entry_date.strftime('%Y-%m-%d')})")

        elif prev_row['Position'] == 1 and current_row['Position'] == 0:
            # Exit trade and calculate returns
            exit_price_aapl = current_row['AAPL']
            exit_price_msft = current_row['MSFT']
            exit_date = current_row.name # Get exit date

            if trade_direction == "Long AAPL, Short MSFT":
                trade_return = (exit_price_aapl - entry_price_aapl) - (exit_price_msft - entry_price_msft)
            else:
                trade_return = (entry_price_aapl - exit_price_aapl) - (entry_price_msft - exit_price_msft)

            # Update cumulative returns
            cumulative_returns += trade_return

            # Calculate percent return from the trade
            starting_amount = entry_price_aapl + entry_price_msft
            percent_return = (trade_return / starting_amount) * 100
            
            # Print trade performance
            print(f"Trade {trade_count}: Exit at AAPL=${exit_price_aapl:.2f}, MSFT=${exit_price_msft:.2f} ({exit_date.strftime('%Y-%m-%d')})")
            print(f"Trade {trade_count}: Return = ${trade_return:.2f} ({percent_return:.2f}%)")
            print(f"Trade {trade_count}: Duration = {days_elapsed} business days\n")

            # Update the number of completed trades
            completed_trades = trade_count

    # Print cumulative results
    print(f"\nTotal Completed Trades: {completed_trades}")
    print(f"Initial Portfolio Value: ${initial_portfolio_value:.2f}")
    print(f"Final Portfolio Value: ${initial_portfolio_value + cumulative_returns:.2f}")
    print(f"Cumulative Return = ${cumulative_returns:.2f} ({(cumulative_returns / initial_portfolio_value) * 100:.2f}%)")

def main():
    # Get todays date for default end date
    today = datetime.date.today()
    formatted_date_today = today.strftime("%Y-%m-%d")

    # Parse all arguments, including the computed default for -end
    parser = argparse.ArgumentParser(description="Backtest Statistical Arbitrage Trading Strategy on Stocks")
    parser.add_argument("-tick1", type=str, help="first stock ticker symbol (e.g., AAPL).", required=True)
    parser.add_argument("-tick2", type=str, help="second stock ticker symbol (e.g., MSFT).", required=True)
    parser.add_argument("-zenter", type=float, help="entry z-score threshold", required=False, default=1.7)
    parser.add_argument("-zexit", type=float, help="exit z-score threshold", required=False, default=0.35)
    parser.add_argument("-start", type=str, help="backtest start date", required=False)
    parser.add_argument("-end", type=str, help="backtest end date", required=False, default=formatted_date_today)
    args = parser.parse_args()
    
    # Assign stock data start date for data download
    if args.start is None:
        stock_data_start_date = get_most_recent_ipo(args.tick1, args.tick2)
    else:
        stock_data_start_date = args.start

    # Print out trading start date and end date
    print(f"BACKTEST START DATE: {stock_data_start_date}")
    print(f"BACKTEST END DATE: {args.end}\n")
    
    # Fetch historical data
    tickers = [args.tick1, args.tick2]
    print(f"DOWNLOADING STOCK DATA FOR: {tickers[0]} and {tickers[1]}")
    data = yf.download(tickers, start=stock_data_start_date, end=args.end)['Adj Close'] # A DataFrame containing dates as the index and adjusted closing prices for AAPL and MSFT as columns
    print("")

    # Calculate spread and z-score
    data['Spread'] = data[tickers[0]] - data[tickers[1]]
    data['Spread_Mean'] = data['Spread'].rolling(window=30).mean()
    data['Spread_Std'] = data['Spread'].rolling(window=30).std()
    data['Z_Score'] = (data['Spread'] - data['Spread_Mean']) / data['Spread_Std']

    # Define trading signals
    z_entry_threshold = args.zenter
    z_exit_threshold = args.zexit

    data['Enter'] = abs(data['Z_Score']) > z_entry_threshold
    data['Exit'] = abs(data['Z_Score']) < z_exit_threshold

    # Initialize a column to track the position state
    data['Position'] = 0

    position_state = 0  # Initial position state (door is closed)
    positions = []  # List to store the resulting positions

    for _, row in data.iterrows():
        position_state = update_positions(row, position_state)
        positions.append(position_state)

    # Update the DataFrame with the calculated positions
    data['Position'] = positions

    data = data.dropna()
    # print(data.to_string())

    calculate_returns(data)
    # print(f"{args.tick1} and {args.tick2}") # Print out stocks being traded
    # print(f"Trading Period: {stock_data_start_date} to {args.end}\n") # Print out trading time period

if __name__ == "__main__":
    print("")
    main()
    print("")