import pandas as pd
import matplotlib.pyplot as plt

# Beskriver hvor .CSV filen skal lagres
# Denne må byttes om du ikke heter Peder og bruker linux
fileName = "strom_30_03_22.csv"
fileLocation = "/home/peder/GitHub/INGT2300/" + fileName

prices = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


df = pd.read_csv(fileLocation)
for i in range(len(df)):
#for i in range(120):
    j = i%24
    prices[j] = prices[j] + df['NOK_per_kWh'].iloc[j]
Sum = sum(prices)
for i in range(len(prices)):
    a = prices[i]/Sum
    pp[i] = a*100
plt.bar(range(24),pp)
plt.show()