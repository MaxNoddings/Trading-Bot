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

The **formula for calculating a z-score** is:

$$
z = \frac{(X - \mu)}{\sigma}
$$

where:
- $X$ is the data point (e.g., a current price or spread between two assets),
- $\mu$ is the mean (average) of the dataset,
- $\sigma$ is the standard deviation of the dataset.

**Interpreting the Z-Score**
- A **z-score of 0** means the data point is exactly at the mean.
- A **positive z-score** indicates that the data point is above the mean.
- A **negative z-score** shows that the data point is below the mean.
- **High z-scores** (e.g., above 2 or 3) imply that the data point is significantly above the mean, while **low z-scores** (e.g., below -2 or -3) indicate that it’s significantly below the mean.

---

### **Z-scores in Trading** ###

- A **high z-score** (e.g., +2 or +3) indicates that the price spread between the two assets is unusually wide compared to its historical average. This can suggest that the higher-priced asset might be overvalued relative to the other, or the lower-priced asset might be undervalued. In pairs trading, this would typically signal a potential opportunity to **short the higher-priced asset** and **buy the lower-priced asset**, anticipating that the spread will narrow as they revert to their usual relationship.

- A **low z-score** (e.g., -2 or -3) means that the spread is unusually narrow, with the prices of the two assets closer together than usual. This might suggest that the higher-priced asset is undervalued relative to the other, or the lower-priced asset is overvalued. Here, it may signal an opportunity to **buy the higher-priced asset** and **short the lower-priced asset**, expecting the spread to widen back to its historical mean.

---

### **What is the difference between Cointegration and Correlation?** ###

**Correlation**
- **Correlation** measures the **degree and direction of linear relationship** between two variables. If two assets have a high positive correlation, their prices tend to move up and down together in the short term. 
- Correlation values range from -1 to +1:
  - **+1**: Perfect positive linear relationship (both assets move in the same direction).
  - **-1**: Perfect negative linear relationship (one asset goes up as the other goes down).
  - **0**: No linear relationship (assets move independently of each other).
- Correlation is **symmetric** and does not account for time dependency, nor does it indicate any "long-term equilibrium" relationship between the assets.
- A high correlation is useful for identifying pairs that may move similarly, but it does not mean they will revert to a stable relationship over time.

**Cointegration**
- **Cointegration** is a concept from time series analysis that describes a **long-term equilibrium relationship** between two (or more) non-stationary time series. 
- Two assets are said to be cointegrated if their **price difference (spread) tends to revert to a constant mean over time**, even though each asset price itself may wander unpredictably. Cointegration implies that the assets are bound together in the long term, despite short-term deviations.
- Unlike correlation, cointegration can **detect a stable, mean-reverting relationship** even when the assets are not strongly correlated in the short term.
- Note: **cointegration** functions may return p-values which range from 0 to 1.
  - **0:** Suggests strong evidence against the null hypothesis. In terms of **cointegration** this indicates strong evidence that the two time series are cointegrated.
  - **1:** Suggests weak or no evidence against the null hypothesis. In terms of **cointegration** a high p-value indicates that there is likely no significant long-term relationship between the two time series.
  

**Key Differences**
1. **Persistence**: Correlation does not imply that two assets will maintain a stable, mean-reverting relationship over time. Cointegration, however, indicates that the assets will revert to a mean value over time.
2. **Short-term vs. Long-term**: Correlation is often useful for short-term movement relationships, whereas cointegration is useful for identifying pairs that have a stable relationship over the long term.
3. **Implication for Strategies**: In pairs trading (like statistical arbitrage), cointegration is more valuable than correlation because it indicates a stable relationship. Cointegrated assets tend to revert to their mean spread, making them ideal for mean-reversion strategies.

**Example**
- **Correlated, but not cointegrated**: Suppose two technology stocks are correlated because they’re both influenced by similar market forces. However, they don’t have a stable price spread, meaning their prices could drift apart permanently over time.
- **Cointegrated**: Imagine a company and its subsidiary, where the parent company stock price is cointegrated with the subsidiary’s stock price. Their prices may fluctuate, but they tend to revert to a certain spread due to the underlying business relationship.

---

### **How can I identify a pair of cointegrated assets through historical data?** ###