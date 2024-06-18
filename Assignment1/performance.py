import matplotlib.pyplot as plt 
import pandas as pd
list = [0,1,2,3,4,5]
df = pd.DataFrame(list)
print(df)
df["square"] = df[0]**2
print(df)
plt.plot(df["square"])
plt.show()
