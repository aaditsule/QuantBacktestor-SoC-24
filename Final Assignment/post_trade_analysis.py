from data import StockAnalyzer
from trading import TradingExecution, strategy_build

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class StrategyAnalysis:
    def __init__(self, returns_series):
        self.returns = returns_series
        
    def cumulative_returns(self):
        """
        Calculate cumulative returns of the trading strategy.
        """
        cumulative = (1 + self.returns).cumprod() - 1
        return cumulative
    
    def maximum_drawdown(self):
        """
        Calculate maximum drawdown of the trading strategy.
        """
        cum_returns = (1 + self.returns).cumprod()
        drawdown = 1 - cum_returns.div(cum_returns.cummax())
        max_drawdown = drawdown.max()
        return max_drawdown
    
    def sharpe_ratio(self, risk_free_rate=0.0, periods_per_year=252):
        """
        Calculate Sharpe ratio of the trading strategy.
        """
        excess_returns = self.returns - risk_free_rate / periods_per_year
        annualized_return = np.mean(self.returns) * periods_per_year
        annualized_volatility = np.std(self.returns) * np.sqrt(periods_per_year)
        sharpe = annualized_return / annualized_volatility
        return sharpe
    
    def sortino_ratio(self, risk_free_rate=0.0, periods_per_year=252):
        """
        Calculate Sortino ratio of the trading strategy.
        """
        downside_returns = self.returns[self.returns < 0]
        annualized_return = np.mean(self.returns) * periods_per_year
        downside_deviation = np.std(downside_returns) * np.sqrt(periods_per_year)
        sortino = annualized_return / downside_deviation
        return sortino
    
    def hit_ratio(self):
        """
        Calculate the percentage of profitable trades (Hit Ratio).
        """
        num_profitable = np.sum(self.returns > 0)
        total_trades = np.sum(self.returns != 0)
        hit_ratio = num_profitable / total_trades
        return hit_ratio
    
    def monthly_returns_heatmap(self):
        """
        Generate a heatmap of monthly returns for each year.
        """
        monthly_returns = self.returns.resample('ME').apply(lambda x: (1 + x).prod() - 1)
        monthly_returns.index = pd.MultiIndex.from_tuples([(d.year, d.month) for d in monthly_returns.index],
                                                  names=['Year', 'Month'])
        monthly_returns = monthly_returns.unstack().fillna(0)
        plt.figure(figsize=(10, 8))
        sns.heatmap(monthly_returns, annot=True, cmap='coolwarm', fmt=".2%")
        plt.title('Monthly Returns Heatmap')
        plt.xlabel('Month')
        plt.ylabel('Year')
        plt.show()
    
    def plot_cumulative_returns(self):
        """
        Generate a plot of cumulative returns over time.
        """
        cumulative = self.cumulative_returns()
        plt.figure(figsize=(10, 6))
        plt.plot(cumulative.index, cumulative.values, label='Cumulative Returns', color='blue', linestyle='-')
        plt.title('Cumulative Returns')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        plt.grid(True)
        plt.show()

# Example usage:
if __name__ == "__main__":
    # Example Pandas Series for returns
    ticker = 'AAPL'
    start_date = '2014-06-30'
    end_date = '2024-06-30'
    interval = '1d'
    stock = StockAnalyzer(ticker, start_date, end_date, interval)
    if stock.is_data_available():
        stock.download_data()
        stock.data = strategy_build(stock.data)
        trading = TradingExecution(stock.data)
        returns = trading.run()
    
        # Instantiate the analysis class
        strategy_analysis = StrategyAnalysis(returns)
    
    # Example of using functions
    print("\nMaximum Drawdown:")
    print(strategy_analysis.maximum_drawdown())
    print("\nSharpe Ratio:")
    print(strategy_analysis.sharpe_ratio())
    print("\nSortino Ratio:")
    print(strategy_analysis.sortino_ratio())
    print("\nHit Ratio:")
    print(strategy_analysis.hit_ratio())
    
    # Generate monthly returns heatmap
    strategy_analysis.monthly_returns_heatmap()
    
    # Plot cumulative returns
    strategy_analysis.plot_cumulative_returns()
