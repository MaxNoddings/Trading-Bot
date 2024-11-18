# **Data Collection and Analysis** #
**Historical Data**: Start by collecting historical data to use for backtesting (can use free APIs like Yahoo Finance or Alpha Vantage for this).

**Feature Engineering**: the process of transforming raw data into meaningful inputs, called features, that can be used to improve the performance of a model or algorithm.
- For **Statistical Arbitrage**, create features based on correlation and cointegration of asset pairs.

**Visualize Data**: Plot price trends, correlation heatmaps, and moving averages to understand market behaviors.



### **How can I identify a pair of cointegrated assets through historical data?** ###

Now I am on the data collection and analysis stage. How can I get started with this stage? How do I collect historical data that can be used for backtesting? How can I transform raw data into meaningful inputs to create features for correlation and cointegration of asset pairs? How do I even identify a pair of cointegrated assets through historical data?


 Here’s a detailed roadmap for tackling the **data collection and analysis stage** for your statistical arbitrage project.

---

## Chat GPT: ##

### **1. Collecting Historical Data**
To backtest and identify asset relationships, you need **historical price data**. Here's how you can get started:

#### **Sources of Historical Data**
- **Free Sources**:
  - [Yahoo Finance](https://finance.yahoo.com): Use libraries like `yfinance` in Python.
  - [Alpha Vantage](https://www.alphavantage.co): Offers free APIs with limited daily requests.
  - [Quandl](https://www.quandl.com): Provides free datasets like WIKI Prices (some data might require a subscription).
  - [Polygon.io](https://polygon.io): Offers free and paid plans for market data.
  - [IEX Cloud](https://iexcloud.io): A good option for affordable historical market data.
  
- **Paid Sources**:
  - Bloomberg Terminal (best for professionals; very expensive).
  - Refinitiv Eikon or other financial data platforms.
  - Quandl Premium or Polygon.io paid plans.

#### **Using Python for Data Collection**
Here's an example of fetching data using `yfinance`:
```python
import yfinance as yf

# Fetch historical data for two stocks
stock1 = yf.download("AAPL", start="2015-01-01", end="2024-01-01")
stock2 = yf.download("MSFT", start="2015-01-01", end="2024-01-01")

# Extract adjusted close prices
prices1 = stock1['Adj Close']
prices2 = stock2['Adj Close']

# Save to CSV for offline use
prices1.to_csv("AAPL.csv")
prices2.to_csv("MSFT.csv")
```

---

### **2. Transforming Raw Data into Features**
To analyze asset relationships, you must preprocess and structure the data.

#### **Preprocessing Steps**
- **Cleaning the Data**:
  - Handle missing values (e.g., forward fill, backward fill, or interpolation).
  - Align timestamps if assets have inconsistent trading days (e.g., one trades globally, the other doesn't).
  
- **Calculating Returns**:
  - Convert prices to daily or log returns, as they're stationary:
    ```python
    import numpy as np
    returns1 = np.log(prices1 / prices1.shift(1))
    returns2 = np.log(prices2 / prices2.shift(1))
    ```

- **Normalization**:
  - Normalize prices or returns if the assets differ significantly in scale. This helps compare them more easily.

#### **Creating Features for Correlation and Cointegration**
- **Correlation**:
  - Use a rolling window to compute the correlation coefficient between two assets:
    ```python
    rolling_corr = returns1.rolling(window=252).corr(returns2)
    ```

- **Cointegration Features**:
  - Compute the price spread between two assets:
    \[
    \text{Spread} = P_1 - \beta P_2
    \]
    - Determine \(\beta\) using **linear regression**:
      ```python
      import statsmodels.api as sm
      X = prices2
      Y = prices1
      X = sm.add_constant(X)  # Add intercept
      model = sm.OLS(Y, X).fit()
      beta = model.params[1]
      spread = prices1 - beta * prices2
      ```
    - Check stationarity of the spread using the **Augmented Dickey-Fuller (ADF) Test**:
      ```python
      from statsmodels.tsa.stattools import adfuller
      result = adfuller(spread)
      print(f"ADF Statistic: {result[0]}, p-value: {result[1]}")
      ```
      A p-value < 0.05 suggests the spread is stationary.

---

### **3. Identifying Cointegrated Pairs**
To find cointegrated pairs among multiple assets:
1. **Form a Universe of Assets**:
   - Choose stocks from similar industries or sectors, as they're more likely to exhibit cointegration (e.g., pairs of tech stocks).

2. **Test Each Pair**:
   - Iterate through all possible pairs in your dataset.
   - Calculate the spread using the method above and test for cointegration using the ADF test.
   - Retain pairs with statistically significant p-values (< 0.05).

3. **Automating the Process**:
   - Example Python script to test multiple pairs:
     ```python
     from itertools import combinations

     def find_cointegrated_pairs(prices):
         pairs = []
         for stock1, stock2 in combinations(prices.columns, 2):
             X = prices[stock1]
             Y = prices[stock2]
             X = sm.add_constant(X)
             model = sm.OLS(Y, X).fit()
             beta = model.params[1]
             spread = Y - beta * prices[stock1]
             adf_result = adfuller(spread)
             if adf_result[1] < 0.05:
                 pairs.append((stock1, stock2, beta))
         return pairs

     prices_data = pd.DataFrame({'AAPL': prices1, 'MSFT': prices2, 'GOOG': prices3})
     cointegrated_pairs = find_cointegrated_pairs(prices_data)
     print(cointegrated_pairs)
     ```

---

### **4. Backtesting the Strategy**
Once you've identified cointegrated pairs:
- Simulate trades based on the z-score of the spread.
- Define entry/exit thresholds for z-scores (e.g., long if z-score > 2; short if z-score < -2).
- Use backtesting libraries like **Backtrader** or build your own framework.

---

### Summary Checklist
1. **Data Collection**:
   - Obtain historical price data for assets of interest.
   - Ensure data integrity through cleaning and alignment.

2. **Feature Engineering**:
   - Create rolling correlations, price spreads, and z-scores.
   - Use ADF tests to identify cointegrated pairs.

3. **Strategy Testing**:
   - Simulate trades based on the statistical arbitrage signals.
   - Evaluate results using backtesting metrics (e.g., Sharpe ratio, drawdown).

4. **Optimize**:
   - Adjust thresholds, timeframes, and parameters for better performance.

Let me know if you’d like detailed help on any specific step!

---

Plan:

1. Somehow identify two stocks that are cointegrated? Build a coding tool that searches through a bunch of stock data to find stocks that are the most cointegrated?
2. Get data on both of those stocks
3. Backtest trading strategies on the past stock prices

---

I am currently at the step where I want to find two (or more) cointegrated stocks. Would it be possible to search through a bunch of stock market data to find two stocks that are the "most" cointegrated, or two stocks that could work the best for my strategy trading strategy at hand - meaning that they must be cointegrated, but it is ok if they have some swings up and down?