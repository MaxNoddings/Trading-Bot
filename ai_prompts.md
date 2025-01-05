Hello! Currently I am trying to make a stock trading bot that trades two assets based on a "Pairs Trading / Statistical Arbitrage" strategy. 

I have made a test script to test a variety of stock pairs to see which pairs are the most correlated and cointegrated with eachother. Through my tests I have found Apple (AAPL) and Microsoft (MSFT) to yeild the best numbers for cointegration and correlation, by far, among all the pairs that I compared. 

Now, it is my goal to develop a trading algorithm that will go long and short on these assets (AAPL and MSFT). 

... first of all, once this algorithm is developed, I want to be able to back test this algorithm with historical data. 



Technical Details about the Algorithm:
- Calculate the spread (difference or ratio) between the prices of the two assets.
- Use the z-score of the spread as a trading signal. If the z-score exceeds a certain threshold (e.g., +2 or -2), enter a trade expecting mean reversion.

Trade potentially using this strategy:
- A **high z-score** (e.g., +2 or +3) indicates that the price spread between the two assets is unusually wide compared to its historical average. This can suggest that the higher-priced asset might be overvalued relative to the other, or the lower-priced asset might be undervalued. In pairs trading, this would typically signal a potential opportunity to **short the higher-priced asset** and **buy the lower-priced asset**, anticipating that the spread will narrow as they revert to their usual relationship.
- A **low z-score** (e.g., -2 or -3) means that the spread is unusually narrow, with the prices of the two assets closer together than usual. This might suggest that the higher-priced asset is undervalued relative to the other, or the lower-priced asset is overvalued. Here, it may signal an opportunity to **buy the higher-priced asset** and **short the lower-priced asset**, expecting the spread to widen back to its historical mean.


Techologies / Libraries / Resources to Use:
- BackTrader (for backtesting)
- QuantConnect (for backtesting)


Hello! Currently I am trying to make a stock trading bot that trades two assets based on a "Pairs Trading / Statistical Arbitrage" strategy. 

I have made a test script to test a variety of stock pairs to see which pairs are the most correlated and cointegrated with eachother. Through my tests I have found Apple (AAPL) and Microsoft (MSFT) to yield the best numbers for cointegration and correlation, by far, among all the pairs that I compared. 

Now, it is my goal to develop a trading algorithm that will go long and short on these assets (AAPL and MSFT). I want my algorithm to trade based on the spread and the z-score of the spread.

Here is some more z-score information about how this algo could operate:
- A **high z-score** (e.g., +2 or +3) indicates that the price spread between the two assets is unusually wide compared to its historical average. This can suggest that the higher-priced asset might be overvalued relative to the other, or the lower-priced asset might be undervalued. In pairs trading, this would typically signal a potential opportunity to **short the higher-priced asset** and **buy the lower-priced asset**, anticipating that the spread will narrow as they revert to their usual relationship.
- A **low z-score** (e.g., -2 or -3) means that the spread is unusually narrow, with the prices of the two assets closer together than usual. This might suggest that the higher-priced asset is undervalued relative to the other, or the lower-priced asset is overvalued. Here, it may signal an opportunity to **buy the higher-priced asset** and **short the lower-priced asset**, expecting the spread to widen back to its historical mean.

Once my trading algorithm is created, I want to be able to backtest the algorithm on historical AAPL and MSFT stock price data.

Can you please develop this algorithm for me and then explain/show me how this algorithm can be used with historical data to back test?

If there are any specific tools/libraries/technologies required that I may need to use let me know.



I've noticed a couple of things. First, but printing out the full data DataFrame, I noticed that the Exit column is never "True" meaning that the positions are never closed. How can I make sure that the positions actually close?

Additionally, I noticed that in the first 30 rows, Spread_Mean, Spread_Std, and Z_Score are labeled as NaN. Is this an issue? Should I replace these with another value?
