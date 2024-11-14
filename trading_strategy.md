# **Trading Strategy** #

### **Chosen Strategy**: Pairs Trading (to start out with) ###

<br>

### **Process**: ### 
- Identify a pair of cointegrated assets through historical data.
- Calculate the **spread** (difference or ratio) between the prices of the two assets.
- Use the **z-score** of the spread as a trading signal. If the z-score exceeds a certain threshold (e.g., +2 or -2), enter a trade expecting mean reversion.

### **Example**: ### 
Suppose Stock A and Stock B have a historically stable spread. If the spread widens significantly (z-score above +2), you could short the higher-priced stock and go long on the lower-priced one. 

---

### **What exactly is a z-score?** ###

A **z-score** is a statistical measure that indicates how many standard deviations an element is from the mean of a dataset. It’s commonly used to understand the position of a data point within a distribution and is especially useful in detecting anomalies or deviations from a historical pattern. In statistical arbitrage and trading, the z-score helps determine if a price or price spread has deviated significantly from its average, often signaling a potential trade opportunity.

### How Z-Scores Work

The **formula for calculating a z-score** is:

\[
z = \frac{(X - \mu)}{\sigma}
\]

where:
- \( X \) is the data point (e.g., a current price or spread between two assets),
- \( \mu \) is the mean (average) of the dataset,
- \( \sigma \) is the standard deviation of the dataset.

### Interpreting the Z-Score
- A **z-score of 0** means the data point is exactly at the mean.
- A **positive z-score** indicates that the data point is above the mean.
- A **negative z-score** shows that the data point is below the mean.
- **High z-scores** (e.g., above 2 or 3) imply that the data point is significantly above the mean, while **low z-scores** (e.g., below -2 or -3) indicate that it’s significantly below the mean.

For example:
- **z = 1** means the data point is 1 standard deviation above the mean.
- **z = -2** means the data point is 2 standard deviations below the mean.

### Why Z-Scores Matter in Trading

In trading strategies like **pairs trading**:
1. Calculate the z-score of the **spread** between two cointegrated assets (the difference in their prices).
2. A high positive or negative z-score in the spread can signal a trade opportunity:
   - If the z-score is **positive and high** (e.g., 2 or above), it may suggest the spread is unusually wide, meaning the higher-priced asset could be overbought relative to the other asset.
   - If the z-score is **negative and low** (e.g., -2 or below), it may indicate the spread is unusually narrow, meaning the higher-priced asset may be oversold.

By using z-scores, traders identify when the relationship between two assets has deviated significantly from the norm, potentially predicting that they will revert to the mean, which creates an opportunity for profitable trades.

How to identify a pair of cointegrated assets through historical data: