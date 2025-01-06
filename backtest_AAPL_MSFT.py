import yfinance as yf 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    entry_price_aapl = 0    # Entry price for AAPL
    entry_price_msft = 0    # Entry price for MSFT
    trade_count = 0         # Count the number of trades
    
    # Iterate through the DataFrame to track trades
    for i in range(1, len(data)):
        # Get current and previous rows
        current_row = data.iloc[i]
        prev_row = data.iloc[i - 1]

        # Check for position changes
        if prev_row['Position'] == 0 and current_row['Position'] == 1:
            # Enter trade based on Z-Score
            trade_count += 1
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

            print(f"Trade {trade_count}: Enter {trade_direction} at AAPL={entry_price_aapl:.2f}, MSFT={entry_price_msft:.2f}")

        elif prev_row['Position'] == 1 and current_row['Position'] == 0:
            # Exit trade and calculate returns
            exit_price_aapl = current_row['AAPL']
            exit_price_msft = current_row['MSFT']

            if trade_direction == "Long AAPL, Short MSFT":
                trade_return = (exit_price_aapl - entry_price_aapl) - (exit_price_msft - entry_price_msft)
            else:
                trade_return = (entry_price_aapl - exit_price_aapl) - (entry_price_msft - exit_price_msft)

            # Update cumulative returns
            cumulative_returns += trade_return

            # Print trade performance
            print(f"Trade {trade_count}: Exit at AAPL={exit_price_aapl:.2f}, MSFT={exit_price_msft:.2f}")
            print(f"Trade {trade_count}: Return = ${trade_return:.2f} ({(trade_return / 2) * 100:.2f}%)\n")

    # Print cumulative results
    print(f"Total Trades: {trade_count}")
    print(f"Cumulative Return = ${cumulative_returns:.2f} ({(cumulative_returns / 2) * 100:.2f}%)\n")

def main():
    # Step 1: Fetch historical data
    tickers = ['AAPL', 'MSFT']
    data = yf.download(tickers, start='2010-01-01', end='2023-12-31')['Adj Close'] # A DataFrame containing dates as the index and adjusted closing prices for AAPL and MSFT as columns

    # Step 2: Calculate spread and z-score
    data['Spread'] = data['AAPL'] - data['MSFT']
    data['Spread_Mean'] = data['Spread'].rolling(window=30).mean()
    data['Spread_Std'] = data['Spread'].rolling(window=30).std()
    data['Z_Score'] = (data['Spread'] - data['Spread_Mean']) / data['Spread_Std']

    # Step 3: Define trading signals
    z_entry_threshold = 1.7
    z_exit_threshold = 0.35

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

if __name__ == "__main__":
    main()