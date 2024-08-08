import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def strategy_build(df):
    # Calculate 9-day and 20-day Simple Moving Averages (SMA)
    df['SMA9'] = df['Close'].rolling(window=9).mean()
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    
    # Initialize signal column
    df['signal'] = 0  # 0 means hold
    
    # Generate signals
    df.loc[df['SMA9'] > df['SMA20'], 'signal'] = 1  # Buy signal
    df.loc[df['SMA9'] < df['SMA20'], 'signal'] = -1  # Sell signal
    
    return df


class TradingExecution:
    def __init__(self, data):
        self.df = data
    
    def run(self):
        returns = pd.Series(index=self.df[self.df.columns[0]])
        position = 0  # 0 means no position
        entry_price = 0.0
        
        for i in range(len(self.df)):
            if self.df['signal'].iloc[i] == 1 and position == 0:
                # Buy signal and no position held
                entry_price = self.df['Close'].iloc[i]
                position = 1  # Long position
                returns.iloc[i] = 0
                
            elif self.df['signal'].iloc[i] == -1 and position == 1:
                # Sell signal and long position held
                exit_price = self.df['Close'].iloc[i]
                
                # Calculate returns
                returns.iloc[i] = (exit_price - entry_price) / entry_price
                position = 0  # No position after selling
            
            else:
                returns.iloc[i] = 0  # No trade made
            
        # Handle unclosed position at the end of the period
        if position == 1:
            # Calculate returns assuming exit at the last close price
            last_close_price = self.df['Close'].iloc[-1]
            returns.iloc[-1] = (last_close_price - entry_price) / entry_price

        (1 + returns).cumprod().to_csv('returns.csv')
        self.df.to_csv('strategy.csv')
        plt.plot((1 + returns).cumprod() - 1)
        plt.xlabel('Date')
        plt.ylabel('Returns')
        plt.title('Returns from Trading Strategy')
        plt.gca().xaxis.set_major_locator(MaxNLocator())
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

from data import StockAnalyzer

if __name__ == '__main__':
    ticker = 'AAPL'
    start_date = '2010-06-30'
    end_date = '2024-06-30'
    interval = '1d'
    stock = StockAnalyzer(ticker, start_date, end_date, interval)
    
    if stock.is_data_available():
        stock.download_data()
        stock.data = strategy_build(stock.data)
        trading = TradingExecution(stock.data)
        trading.run()
