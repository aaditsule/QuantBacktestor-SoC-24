import yfinance as yf
import pandas as pd

def download_historical_data(symbol: str, start_date: str, end_date: str, timeframe: str = "1d") -> pd.DataFrame:
    data = yf.download(symbol, start=start_date, end=end_date, interval=timeframe)
    return data

# start_date = "2024-06-01"
# end_date = "2024-06-11"
# timeframe = "1d"
# print(download_historical_data("MSFT",start_date,end_date,timeframe))