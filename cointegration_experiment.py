import yfinance as yf
import itertools
from statsmodels.tsa.stattools import coint

# Download historical data
symbols = ['AAPL', 'MSFT', 'GOOG', 'AMZN']  # Add your list of stocks
data = yf.download(symbols, start='2015-01-01', end='2023-01-01')['Adj Close']

# Generate all pairs of stocks
pairs = list(itertools.combinations(data.columns, 2))

# Find cointegrated pairs
cointegrated_pairs = []
for pair in pairs:
    stock1, stock2 = pair
    series1 = data[stock1]
    series2 = data[stock2]
    
    # Run the cointegration test
    score, p_value, _ = coint(series1, series2)
    
    # Check p-value
    if p_value < 0.05:  # 5% significance level
        cointegrated_pairs.append((stock1, stock2, p_value))

# Display results
print("Cointegrated Pairs:")
for pair in cointegrated_pairs:
    print(f"{pair[0]} and {pair[1]} with p-value: {pair[2]:.4f}")
