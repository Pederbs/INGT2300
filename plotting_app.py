import requests
import pandas as pd
import matplotlib.pyplot as plt

# Beskriver hvor .CSV filen skal lagres
# Denne må byttes om du ikke heter Peder og bruker linux
fileName = "strom.csv"
fileLocation = "/home/peder/GitHub/INGT2300/" + fileName

hist = pd.read_csv(fileLocation)
hist.plot(x='time_start', y='NOK_per_kWh', figsize=(40, 10))

# Lagring av plottet
plt.savefig('plot.png',dpi=500)


plt.show()