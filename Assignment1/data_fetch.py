import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
msft = yf.Ticker("msft")
info = msft.info
# for key,value in info.items():
#     print(key,":",value)

# today = dt.now().date().srtftime("%Y-%m-%d")

df = msft.history(period="max")
# print(df)
plt.figure()
plt.plot(df["Close"], color ="red")
plt.plot(df["Open"],color="green")
plt.show()
