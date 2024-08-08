from data import StockAnalyzer
from trading import TradingExecution, strategy_build

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class TradingStrategyAnalysis:
    def __init__(self, return_series):
        self.returns = return_series
        
    def calc_cumulative_returns(self):
        # Compute cumulative returns from the strategy's return series.
        cum_returns = (1 + self.returns).cumprod() - 1
        return cum_returns
    
    def calc_max_drawdown(self):
        # Compute the maximum drawdown from the strategy's cumulative returns.
        cumulative_returns = (1 + self.returns).cumprod()
        drawdowns = 1 - cumulative_returns / cumulative_returns.cummax()
        max_dd = drawdowns.max()
        return max_dd
    
    def calc_sharpe_ratio(self, risk_free_rate=0.0, trading_days=252):
        # Compute the Sharpe ratio for the strategy.
        adjusted_returns = self.returns - risk_free_rate / trading_days
        annual_return = np.mean(adjusted_returns) * trading_days
        annual_volatility = np.std(adjusted_returns) * np.sqrt(trading_days)
        sharpe_ratio = annual_return / annual_volatility
        return sharpe_ratio
    
    def calc_sortino_ratio(self, risk_free_rate=0.0, trading_days=252):
        # Compute the Sortino ratio, focusing on downside risk.
        downside_returns = self.returns[self.returns < 0]
        annual_return = np.mean(self.returns) * trading_days
        downside_volatility = np.std(downside_returns) * np.sqrt(trading_days)
        sortino_ratio = annual_return / downside_volatility
        return sortino_ratio
    
    def calc_hit_ratio(self):
        # Compute the hit ratio, representing the percentage of profitable trades.
        positive_trades = np.sum(self.returns > 0)
        total_trades = len(self.returns[self.returns != 0])
        hit_ratio = positive_trades / total_trades if total_trades > 0 else 0
        return hit_ratio
    
    def generate_monthly_returns_heatmap(self):
        # Create a heatmap to visualize monthly returns over different years.
        monthly_returns = self.returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
        monthly_returns.index = pd.MultiIndex.from_tuples([(date.year, date.month) for date in monthly_returns.index],
                                                  names=['Year', 'Month'])
        monthly_returns = monthly_returns.unstack().fillna(0)
        plt.figure(figsize=(10, 8))
        sns.heatmap(monthly_returns, annot=True, cmap='RdYlGn', fmt=".2%")
        plt.title('Monthly Returns Heatmap')
        plt.xlabel('Month')
        plt.ylabel('Year')
        plt.show()
    
    def plot_cumulative_returns(self):
        # Visualize cumulative returns over time.
        cumulative = self.calc_cumulative_returns()
        plt.figure(figsize=(10, 6))
        plt.plot(cumulative.index, cumulative.values, label='Cumulative Returns', color='green', linestyle='-')
        plt.title('Cumulative Returns Over Time')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        plt.grid(True)
        plt.show()

# Sample execution:
if __name__ == "__main__":
    # Define the stock ticker, start and end dates, and interval.
    ticker = 'AAPL'
    start_date = '2014-06-30'
    end_date = '2024-06-30'
    interval = '1d'
    
    stock_data = StockAnalyzer(ticker, start_date, end_date, interval)
    if stock_data.is_data_available():
        stock_data.download_data()
        stock_data.data = strategy_build(stock_data.data)
        trading_exec = TradingExecution(stock_data.data)
        strategy_returns = trading_exec.run()
    
        # Analyze the strategy
        analysis = TradingStrategyAnalysis(strategy_returns)
    
        # Example of using analysis methods
        print("\nMaximum Drawdown:")
        print(analysis.calc_max_drawdown())
        print("\nSharpe Ratio:")
        print(analysis.calc_sharpe_ratio())
        print("\nSortino Ratio:")
        print(analysis.calc_sortino_ratio())
        print("\nHit Ratio:")
        print(analysis.calc_hit_ratio())
        
        # Generate and display heatmap of monthly returns
        analysis.generate_monthly_returns_heatmap()
        
        # Plot and display cumulative returns over time
        analysis.plot_cumulative_returns()
