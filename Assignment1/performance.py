import matplotlib.pyplot as plt
import pandas as pd

def plot_closing_prices(data: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'], label='Closing Price')
    plt.title("Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.legend()
    plt.grid(True)
    plt.show()
