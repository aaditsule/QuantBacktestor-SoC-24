import yfinance as yf

import matplotlib.pyplot as plt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from datetime import datetime

class StockAnalyzer:
    def __init__(self, symbol, start_date, end_date, interval):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.data = None

    def is_data_available(self):
        is_symbol_valid = yf.Ticker(self.symbol).history(period='1d').empty == False
        is_interval_valid = self.interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
        is_date_valid = self.start_date < self.end_date and self.start_date < datetime.now() 
        return is_symbol_valid and is_interval_valid and is_date_valid
    
    def download_data(self):
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date, interval=self.interval).reset_index()
        columns = self.data.columns
        if 'Datetime' in columns:
            self.data['Datetime'] = self.data['Datetime'].dt.strftime('%Y-%m-%d %H:%M')

    def has_missing_data(self):
        if self.data is not None:
            return self.data.isnull().values.any()
        return False

    def handle_missing_data(self):
        if self.data is not None:
            imputer = IterativeImputer()
            missing = self.data[self.data.isnull().any(axis=1)]
            self.data = imputer.fit_transform(self.data)
            return missing
        return None

    def plot_performance(self):
        if self.data is not None:
            self.data['Close'].plot()
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.title(f'{self.symbol} from {self.start_date} to {self.end_date} with interval {self.interval}')
            plt.show()

    def get_statistial_measure(self):
        if self.data is not None:
            stats = self.data.describe()
            stats_filtered = stats.drop(['count']).drop(stats.columns[0], axis = 1).round(2)
            stats_filtered.reset_index(names=['Statistical Measure'], inplace=True)
            return stats_filtered
        
    def add_cummulative_return(self):
        if self.data is not None:
            self.data['Cummulative Return'] = (1 + self.data['Close'].pct_change()).cumprod()