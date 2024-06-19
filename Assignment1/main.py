from data_fetch import download_historical_data
from performance import plot_closing_prices
from datetime import datetime

symbol = "RELIANCE.NS"
start_date = "2023-06-01"
end_date = datetime.today().strftime("%Y-%m-%d")
timeframe = "1d"

stock_data = download_historical_data(symbol, start_date, end_date, timeframe)

plot_closing_prices(stock_data)