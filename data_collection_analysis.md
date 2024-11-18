# **Data Collection and Analysis** #
**Historical Data**: Start by collecting historical data to use for backtesting (can use free APIs like Yahoo Finance or Alpha Vantage for this).

**Feature Engineering**: the process of transforming raw data into meaningful inputs, called features, that can be used to improve the performance of a model or algorithm.
- For **Statistical Arbitrage**, create features based on correlation and cointegration of asset pairs.

**Visualize Data**: Plot price trends, correlation heatmaps, and moving averages to understand market behaviors.

---

### **Collect Data from these stock pairs below, through data analysis, find which pair is most correlated/cointegrated** ###

Pair candidates:
- Coca-Cola (KO) and PepsiCo (PEP) -> Consumer Staples
- ExxonMobile (XOM) and Chevron (CVX) -> Energy
- Proctor & Gamble (PG) and Colgate-Palmolive (CL) -> Consumer Staples
- Visa (V) and Mastercard (MA) -> Financial Services
- JPMorgan Chase (JPM) and Bank of America (BAC) -> Financials
- Ford Motor Company (F) and General Motors (GM) -> Consumer Discretionary
- American Airlines (AAL) and Delta Air Lines (DAL) -> Industrials

---

### **Next Steps:** ### 
- refine correlation/cointegration algorithm scoring system
- test algorithms on all pairs
- choose final pair with highest correlation/cointegration score to trade with and then go on to developing the trading