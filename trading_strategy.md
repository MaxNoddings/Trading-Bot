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

### **How can I identify a pair of cointegrated assets through historical data?** ###