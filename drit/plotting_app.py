import pandas as pd
import matplotlib.pyplot as plt

# Beskriver hvor .CSV filen skal lagres
# Denne må byttes om du ikke heter Peder og bruker linux
fileName = "strom.csv"
fileLocation = "/home/peder/GitHub/INGT2300/" + fileName

hist = pd.read_csv(fileLocation)
cost_with_battery = hist['consumption_cost_with_battery'].sum()
cost_whitout_battery = hist['consumption_cost'].sum()
spart = cost_whitout_battery - cost_with_battery
print("Penger spart uten kapasitetsledd: " + str(spart))
hist.plot(x='time_start', y=['consumption_cost_with_battery','consumption_cost'], figsize=(40, 10))

# Lagring av plottet
plt.savefig('plot.png',dpi=500)


plt.show()