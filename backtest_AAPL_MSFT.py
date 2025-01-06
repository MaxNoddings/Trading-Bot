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

def main():
    # Step 1: Fetch historical data
    tickers = ['AAPL', 'MSFT']
    data = yf.download(tickers, start='2010-01-01', end='2023-12-31')['Adj Close'] # A DataFrame containing dates as the index and adjusted closing prices for AAPL and MSFT as columns

    # Step 2: Calculate spread and z-score
    data['Spread'] = data['AAPL'] - data['MSFT']
    data['Spread_Mean'] = data['Spread'].rolling(window=30).mean()
    data['Spread_Std'] = data['Spread'].rolling(window=30).std()
    data['Z_Score'] = (data['Spread'] - data['Spread_Mean']) / data['Spread_Std']

    # print(data.to_string())
    # print(data)
    print("-----------------------------------------------------------------------------------")

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

    # # Vectorized logic to set position states
    # # When "Enter" is True, start a position
    # data.loc[data['Enter'], 'Position'] = True

    # # When "Exit" is True, end a position
    # data['Position'] = data['Position'].shift().fillna(True)  # Carry forward positions until exit
    # data.loc[data['Exit'], 'Position'] = False
    # data['Position'] = data['Position'].ffill().fillna(False) # Ensure positions are carried forward

    # data['Long'] = data['Z_Score'] < -z_entry_threshold  # Long AAPL, Short MSFT
    # data['Short'] = data['Z_Score'] > z_entry_threshold  # Short AAPL, Long MSFT
    # data['Exit'] = abs(data['Z_Score']) < z_exit_threshold

    data = data.dropna()
    print(data.to_string())
    # print(data)
    print("-----------------------------------------------------------------------------------")

    # # Step 4: Simulate trades
    # positions = pd.DataFrame(index=data.index)
    # positions['AAPL'] = 0
    # positions['MSFT'] = 0

    # print("POSITIONS DATAFRAME INITIALIZATION -----------------------------------------------------------------------------------")
    # print(positions.to_string())
    # print("-----------------------------------------------------------------------------------")

    # # Find where in the history, a change is made in the data
    # long_signal = data['Long'] & ~data['Long'].shift(1, fill_value=False)  # Entry signal
    # short_signal = data['Short'] & ~data['Short'].shift(1, fill_value=False)  # Entry signal
    # exit_signal = data['Exit'] & ~data['Exit'].shift(1, fill_value=False)  # Exit signal

    # print("POSITIONS DATAFRAME FIRST FILL -----------------------------------------------------------------------------------")
    # print(positions.to_string())
    # print("-----------------------------------------------------------------------------------")

    # positions.loc[long_signal, 'AAPL'] = 1
    # positions.loc[long_signal, 'MSFT'] = -1
    # positions.loc[short_signal, 'AAPL'] = -1
    # positions.loc[short_signal, 'MSFT'] = 1
    # positions.loc[exit_signal, ['AAPL', 'MSFT']] = 0

    # print("POSITIONS DATAFRAME 1, -1, 0 FILL -----------------------------------------------------------------------------------")
    # print(positions.to_string())
    # print(positions)
    # print("-----------------------------------------------------------------------------------")


    # positions['AAPL'] = positions['AAPL'].cumsum()  # Running position count
    # positions['MSFT'] = positions['MSFT'].cumsum()

    # print("-----------------------------------------------------------------------------------")
    # print(positions.to_string())
    # print(positions)

    # # Step 5: Calculate portfolio returns
    # returns = data.pct_change()
    # portfolio_returns = positions.shift().mul(returns).sum(axis=1)  # Daily portfolio return
    # cumulative_returns = (1 + portfolio_returns).cumprod()

    # # Step 6: Plot results
    # plt.figure(figsize=(12, 6))
    # plt.plot(cumulative_returns, label="Cumulative Returns")
    # plt.title("Pairs Trading Backtest: AAPL and MSFT")
    # plt.legend()
    # plt.show()

if __name__ == "__main__":
    main()