import pandas as pd
import numpy as np
from scipy import stats

# Load historical data (Replace with your preferred data source)
# This example uses pandas_datareader, but you can use other sources like yfinance
import pandas_datareader as web

start_date = '2010-01-01'
end_date = '2023-12-31'

data = web.DataReader(['AAPL', 'MSFT'], 'yahoo', start_date, end_date)['Adj Close']

# Calculate the spread
data['Spread'] = data['AAPL'] - data['MSFT']

# Calculate z-score
window = 60  # Adjust window size as needed
data['Spread_Mean'] = data['Spread'].rolling(window).mean()
data['Spread_Std'] = data['Spread'].rolling(window).std()
data['Z-Score'] = (data['Spread'] - data['Spread_Mean']) / data['Spread_Std']

# Define trading signals
data['Position'] = 0
data.loc[(data['Z-Score'] > 2), 'Position'] = -1  # Short AAPL, Long MSFT
data.loc[(data['Z-Score'] < -2), 'Position'] = 1   # Long AAPL, Short MSFT
data.loc[(data['Z-Score'].abs() < 1), 'Position'] = 0  # Exit trade

# Calculate daily returns
data['AAPL_Return'] = data['AAPL'].pct_change()
data['MSFT_Return'] = data['MSFT'].pct_change()
data['Portfolio_Return'] = data['Position'].shift(1) * (data['AAPL_Return'] - data['MSFT_Return'])

# Calculate cumulative returns
data['Cumulative_Return'] = (1 + data['Portfolio_Return']).cumprod()

# Calculate performance metrics
annualized_return = data['Portfolio_Return'].mean() * 252 
annualized_volatility = data['Portfolio_Return'].std() * np.sqrt(252)
sharpe_ratio = annualized_return / annualized_volatility 
max_drawdown = (data['Cumulative_Return'].cummax() - data['Cumulative_Return']) / data['Cumulative_Return'].cummax()
max_drawdown = max_drawdown.max()

print(f"Annualized Return: {annualized_return:.4f}")
print(f"Annualized Volatility: {annualized_volatility:.4f}")
print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
print(f"Maximum Drawdown: {max_drawdown:.4f}")

# (Optional: Plot results)
# import matplotlib.pyplot as plt
# plt.figure(figsize=(12, 6))
# plt.plot(data['Cumulative_Return'])
# plt.title('Cumulative Returns')
# plt.xlabel('Date')
# plt.ylabel('Cumulative Return')
# plt.show() 

# Note:
# 1. This code requires the `pandas_datareader` library. Install it using `pip install pandas-datareader`.
# 2. Adjust the `window` size for calculating the moving average and standard deviation based on your analysis.
# 3. This is a simplified example and may require further refinement for real-world trading.
# 4. Consider adding features like transaction costs, risk management rules (stop-loss), and more sophisticated performance metrics.