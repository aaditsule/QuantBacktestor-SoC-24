import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

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
        is_date_valid = self.start_date < self.end_date
        return is_symbol_valid and is_interval_valid and is_date_valid
    
    def download_data(self):
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date, interval=self.interval).reset_index()
        columns = self.data.columns
        if 'Datetime' in columns:
            self.data['Datetime'] = self.data['Datetime'].dt.strftime('%Y-%m-%d %H:%M')

    def handle_missing_data(self):
        if self.data is not None:
            imputer = IterativeImputer()
            missing = self.data.loc[:, self.data.isnull().sum() > 0].iloc[:, 0]
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
            stats_filtered = stats.drop(['count'])
            return stats_filtered
        
    def add_cummulative_return(self):
        if self.data is not None:
            self.data['Cummulative Return'] = (1 + self.data['Close'].pct_change()).cumprod()

def plot_cummulative_return(symbol, start_date, end_date, interval):
    stock_cummulative_return = stock.data['Cummulative Return']
    nifty_cummulative_return = nifty.data['Cummulative Return']

    if 'Datetime' in stock.data.columns:
        stock_cummulative_return.index = stock.data['Datetime']
        nifty_cummulative_return.index = nifty.data['Datetime']
    else:
        stock_cummulative_return.index = stock.data['Date']
        nifty_cummulative_return.index = nifty.data['Date']

    stock_cummulative_return.plot()
    nifty_cummulative_return.plot()

    plt.xlabel('Date')
    plt.ylabel('Cummulative Return')
    plt.xticks(rotation=45)
    plt.legend([symbol, 'NIFTY'])
    plt.title(f'{symbol} Cummulative Return from {start_date} to {end_date} with interval {interval}')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    ticker = 'RELIANCE.NS'
    start_date = '2024-06-01'
    end_date = '2024-06-30'
    interval = '1h'
    stock = StockAnalyzer(ticker, start_date, end_date, interval)
    nifty = StockAnalyzer('^NSEI', start_date, end_date, interval)

    if stock.is_data_available():
        stock.download_data()
        nifty.download_data()
        print(stock.get_statistial_measure())
        stock.add_cummulative_return()
        nifty.add_cummulative_return()
        plot_cummulative_return(ticker, start_date, end_date, interval)
    else:
        print('No data found for the given symbol, date or interval.')