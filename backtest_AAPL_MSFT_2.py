import numpy as np
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Step 1: Download Historical Data
def download_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Close']
    return data

# Step 2: Calculate Spread and Z-Score
def calculate_spread_zscore(series1, series2):
    # Perform OLS regression to find hedge ratio
    model = sm.OLS(series1, sm.add_constant(series2))
    result = model.fit()
    hedge_ratio = result.params[1]
    spread = series1 - hedge_ratio * series2

    # Z-score of the spread
    zscore = (spread - spread.mean()) / spread.std()
    return spread, zscore

# Step 3: Define Trading Logic
def pairs_trading_logic(zscore, entry_threshold=2, exit_threshold=0.5):
    signal = pd.Series(index=zscore.index)
    signal[zscore > entry_threshold] = -1  # Short spread
    signal[zscore < -entry_threshold] = 1  # Long spread
    signal[abs(zscore) < exit_threshold] = 0  # Close positions
    return signal.ffill().fillna(0)

# Step 4: Backtest the Strategy
def backtest(data, signals):
    returns = data.pct_change().dropna()
    signals_aligned = signals.shift(1).reindex(returns.index)
    strategy_returns = signals_aligned * returns
    cumulative_returns = (1 + strategy_returns).cumprod()
    return cumulative_returns

# Main Script
if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT']
    start_date = "2020-01-01"
    end_date = "2023-12-31"
    
    # Download data
    data = download_data(tickers, start_date, end_date)
    
    # Ensure no missing values
    data = data.dropna()

    # Calculate spread and z-score
    spread, zscore = calculate_spread_zscore(data['AAPL'], data['MSFT'])
    
    # Define trading logic
    signals = pairs_trading_logic(zscore)

    # Backtest
    cumulative_returns = backtest(data, signals)

    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_returns, label="Strategy Cumulative Returns")
    plt.title("Pairs Trading Strategy Backtest")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Returns")
    plt.legend()
    plt.grid()
    plt.show()
