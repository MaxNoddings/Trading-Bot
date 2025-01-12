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


Currently I have a data table that is named `data` and is defined as so:

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

# print(data.to_string())
# print(data)
print("-----------------------------------------------------------------------------------")

# Step 3: Define trading signals
z_entry_threshold = 1.7
z_exit_threshold = 0.35

data['Long'] = data['Z_Score'] < -z_entry_threshold  # Long AAPL, Short MSFT
data['Short'] = data['Z_Score'] > z_entry_threshold  # Short AAPL, Long MSFT
data['Exit'] = abs(data['Z_Score']) < z_exit_threshold

data = data.dropna()

Now, based on this DataFrame, I want my algorithm to perform as follows:
- 



I currently have a dataframe that looks as follows:
.
.
.

Now I want to add a column for `Enter Position` and `Exit Position`. Essentially, I want to enter a position when the absolute value of the `Z_Score` is greater than the `z_entry_threshold`.
    From here the trading logic should operate as follows:
        if data['Z_Score'] < -z_entry_threshold
            go Long AAPL, Short MSFT
        else if data['Z_Score'] > z_entry_threshold
            go Short AAPL, Long MSFT
        else
            "Something went wrong"

Next key thing we have to program in: once a position enter is made, another entry cannot be made


Next key thing we have to program in: an unlimited entry positions can be made (theoretically they should time out after a certain amount of time), but all the entry positions should be exited when an exit condition is triggered. 


Lets start out with: only one entry position can be made at a time, even if another entry condition is triggered before an exit is made. This being so - once an exit condition is triggered, then the enter position ability opens up. 


Start this by first just making simple entry and exit columns in `data`, then program in the rules such that two entries cannot be made in a row, it basically has to alternate between entry and exit. 


.... Wherever there is an "Entry" == True, mark the price here -> if the Z-score is negative then -> long AAPL, short MSFT, else if the Z-score is positive then -> short AAPL, long MSFT
    - *** Might have to make functions for `Short` and `Long`....
    - How should these functions operate, what should their parameters be, and what should they return ....
    - I have a list of dates with stock closing prices for each day...
    - Going to have to have a short_entry() function and a long_entry() function in addition to a short_close() and long_close() function
        - Simply can just have variables that hold values for `short_entry` or `long_entry`.
        - Then you can have exit conditions -> if exit condition is met, then set `short_exit` or `long_exit` variables and then calculate the return and print it out!

.
.
.

I think that I am going to want to have an iterator function such that it iterates over the data dataframe.

.
.
.

Actually ... it looks like for efficiency sake it is better to avoid iteration and rather than that use vectorized operations instead ...
    How can we do this with the algorithm return function that we are trying to build above ... ?
        We could have a "short_entry" and "short_close" column



From where I am currently at, the `data` Dataframe shows when I should Enter a Position and then exit a position. Now I need to implement some type of code that will calculate the stock returns based on the data frame. Is there any way to do this in a way of vectorized operations, or will I need to create a function that iterates over the DataFrame?

Here is the code:

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

# print(data.to_string())
# print(data)
print("-----------------------------------------------------------------------------------")

# Step 3: Define trading signals
z_entry_threshold = 1.7
z_exit_threshold = 0.35

data['Enter'] = abs(data['Z_Score']) > z_entry_threshold
data['Exit'] = abs(data['Z_Score']) < z_exit_threshold





Like you mentioned at the end, the Enter and Exit signals are actually overlapping meaning that there are simultaneous enter and exits. With this said, some more complex logic will need to be implemented: I want the enter and exits to almost act as a door. If the door is open and gets a command to be closed, it will be closed. If it gets another command to be closed, it will simply stay closed, since it is already closed. Once a command comes in to open the door, the door will be opened back up. Similarily, if the door is already open, it will simply stay open since it is already open.

Can you implement this logic for me, in terms of the enter and exit signals and the position column. Here the position column will represent the door in the above analogy, and the enter signal will act as the open command while the exit signal will act as the close command.



This is the code that I am currently using:
..
Now, I want a function that loops back through the DataFrame. For this function, I want to record stock returns over the time whenever Position = 1. In the row when position first turns from 0 to 1, if the Z-Score for that column is a negative number, then start a buy/long order of AAPL, and a short order of MSFT. If the Z-Score for the column when position first turns from 0 to 1 is a positive number, then start a short order of AAPL, and a buy/long order of MSFT. Then, once Position changes back from 1 to 0, then exit the buy/short orders that were places and calculate the returns. 

For this iterative function, I want it to print out something after each trade completes, effectively printing out the performance of that specific trade. Then, I also want it to print out a cumulative returns result too. Print out a percentage result and a dollar amount result assuming for each entry/exit one share is bought/shorted. 



When tracking returns in stock trading, what is the best way to do it? Lets say I have enough money to buy one apple stock (priced at $100) and one microsoft stock (priced at $250), giving my portfolio a value of $350. I buy both of the stocks and apple goes up be 5% (to $105) and then microsoft goes up by 10% (to $275). My portfolio value is now $380. 

What would my total return percentage be? = 8.57%


Need to create two variables: one variable that will track the percentage returns for each specific trade and another variable that will track the percentage returns for the entire trading duration.


Next Up: Add command line options to modularize code
- custom options for z-score
- custom options for date range
    - default would be the auto-date finder from the coint/corr code
- custom stock ticker names

. . . 

Next: add the auto-date finder from the coint/corr code for the default dates
    - pass two ticker names into a function and have the function return the later IPO date in the correct format

.... also: modify code so that it supports interchanging different ticker names!!

.. in the calculate return function should I have it take in the name of the stocks?? And should it return a string with all the calculations that it has made?

I think that you should be able to extract the names of the stocks from the data table?

Also, I think that you should be able to extract the data of the trading period (dates) from the data DataFrame as well?

^ this way you could print all of the correct data that you want to display from just taking in the data DataFrame into the calculate_returns function.


It appears that the spread needs to be negative in order for the algorithm to trade correctlt
    try to introduce an absolute value into the equation and see how it operates -> this should cover for the case if the stocks cross paths with eachother?