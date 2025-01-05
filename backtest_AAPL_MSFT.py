import yfinance as yf 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Fetch historical data
tickers = ['AAPL', 'MSFT']
data = yf.download(tickers, start='2010-01-01', end='2023-12-31')['Adj Close'] # A DataFrame containing dates as the index and adjusted closing prices for AAPL and MSFT as columns

# Step 2: Calculate spread and z-score
data['Spread'] = data['AAPL'] - data['MSFT']
data['Spread_Mean'] = data['Spread'].rolling(window=30).mean()
data['Spread_Std'] = data['Spread'].rolling(window=30).std()
data['Z_Score'] = (data['Spread'] - data['Spread_Mean']) / data['Spread_Std']

print(data.to_string())

print("-----------------------------------------------------------------------------------")

# Step 3: Define trading signals
z_entry_threshold = 2
z_exit_threshold = 0.5

data['Long'] = data['Z_Score'] < -z_entry_threshold  # Long AAPL, Short MSFT
data['Short'] = data['Z_Score'] > z_entry_threshold  # Short AAPL, Long MSFT
data['Exit'] = abs(data['Z_Score']) < z_exit_threshold

data = data.dropna()
print(data.to_string())

# Step 4: Simulate trades
positions = pd.DataFrame(index=data.index)
positions['AAPL'] = 0
positions['MSFT'] = 0

long_signal = data['Long'] & ~data['Long'].shift(1, fill_value=False)  # Entry signal
short_signal = data['Short'] & ~data['Short'].shift(1, fill_value=False)  # Entry signal
exit_signal = data['Exit'] & ~data['Exit'].shift(1, fill_value=False)  # Exit signal

positions.loc[long_signal, 'AAPL'] = 1
positions.loc[long_signal, 'MSFT'] = -1
positions.loc[short_signal, 'AAPL'] = -1
positions.loc[short_signal, 'MSFT'] = 1
positions.loc[exit_signal, ['AAPL', 'MSFT']] = 0

print(positions.to_string())

positions['AAPL'] = positions['AAPL'].cumsum()  # Running position count
positions['MSFT'] = positions['MSFT'].cumsum()

print("-----------------------------------------------------------------------------------")
print(positions.to_string())

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
