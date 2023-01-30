import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def checkMonth(cDate, cMonth):
    if ((cDate == 30) and (cMonth in evenMonth)):
        cDate = 1
        cMonth = cMonth + 1
        return cDate, cMonth
    elif ((cDate == 28) and (cMonth == 2)):
        cDate = 1
        cMonth = cMonth + 1
        return cDate, cMonth
    elif ((cDate == 31) and (cMonth in oddMonth)):
        cDate = 1
        cMonth = cMonth + 1
        return cDate, cMonth
    else:
        cDate = cDate + 1
        return cDate, cMonth

def makeStr(number):
    str_number = str(number)
    if len(str_number) < 2:
        str_number = "0" + str_number
        return str_number
    else:
        return str(str_number)

# Verdier og konstanter for programmet
evenMonth = [4, 6, 9, 11]
oddMonth = [1, 3, 5, 7, 8, 10, 12]
flag = 0

# Beskriver hvor .CSV filen skal lagres
# Denne må byttes om du ikke heter Peder og bruker linux
fileName = "strom.csv"
fileLocation = "/home/peder/GitHub/INGT2300/" + fileName

# Bruker input
priceArea = "NO1"
date = 5
month = 4
year = 2022

#fetching data for a year
#not accounting for leap year so just fetching 365 days
for i in range(0,300):
    strDate = makeStr(date)
    strMonth = makeStr(month)
    # Bygger link for å hente data
    link = "https://www.hvakosterstrommen.no/api/v1/prices/" + str(year) + "/" + strMonth + "-" + strDate + "_" + priceArea + ".json"
    # Henter data
    response = requests.get(link).text
    df = pd.read_json(response)
    dfClean = df.drop(['EXR', 'EUR_per_kWh','time_end'], axis=1)

    # Fjerner øverste beskrivende rad for hver dag men beholder den første
    if flag == 0:
        flag = 1
        dfClean.to_csv(fileLocation, index=False)
    else:
        dfClean.to_csv(fileLocation, header=False, index=False, mode="a")


    date, month = checkMonth(date, month)

    if month == 13:
        month = 1
        year = year + 1
hist = pd.read_csv(fileLocation)
hist.plot(x='time_start', y='NOK_per_kWh')
plt.show()