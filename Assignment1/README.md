# **Assignment 1: Creating data_fetch.py**

## **Task**
Implement the `download_historical_data` function to fetch historical price data for cryptocurrencies from Yahoo API. Within this module, implement the function `download_historical_data` using Yahoo Finance as the data source. This function should be capable of fetching historical data for a specified stock symbol between given start and end dates. Additionally, it should support an optional parameter for the data timeframe with a default value of '1d' (daily).

## **Function Specifications**

**Parameters:**
- `symbol`: The ticker symbol of the stock (e.g., 'RELIANCE.NS').
- `start_date`: Start date for the data in 'YYYY-MM-DD' format.
- `end_date`: End date for the data in 'YYYY-MM-DD' format.
- `timeframe`: The frequency of the data ('1d', '1wk', '1mo'), default is '1d'.

**Return:**
- A pandas DataFrame containing the fetched data.

## **For Visualization**

In a separate script, `main.py`:
1. Import your `download_historical_data` function.
2. Fetch data for 'RELIANCE.NS' from June 1, 2024, to today.
3. Plot the closing prices of the stock using matplotlib with a well-labeled image.
4. Make this plotting a function specifying the parameters you pass and its objective is to show the plot.
5. Move this function to `performance.py` file, then import this in `main.py` and call it to plot.

## **Deliverables**

A screen recording (maximum 20 minutes) showing:
- The coding process of your implementation (time lapse).
- DataFrame being displayed and the plot generated in your `main.py`.

This assignment is designed to ensure you grasp basic data fetching and manipulation techniques, which are crucial for the upcoming complex tasks in this course. Take this assignment seriously to prepare for the challenging parts of our project.

## **Example: main.py**

```python
from data_fetch import download_historical_data 
from strategy_builder import buy_func, sell_func 
from backtest import ohlc_long_only_backtester 
from performance import calculate_performance_metrics 

symbol = "BTC-USDT"
timeframe = "4hour" 
df = download_historical_data(symbol, start_date, end_date, timeframe)
