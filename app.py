import requests
import pandas as pd
import matplotlib.pyplot as plt

def checkMonth(currentDate, currentMonth):
    if (currentDate == 30) and (currentMonth == (4 or 6 or 9 or 11)):
        return True
    if (currentDate == 28) and (currentMonth == 2):
        return True
    if (currentDate == 31) and (currentMonth == (1 or 3 or 5 or 7 or 8 or 10 or 12)):
        return True
    else:
        return False

def makeStr(number):
    str_number = str(number)
    if len(str_number) < 2:
        str_number = "0" + str_number
        return str_number
    else:
        return str(str_number)


priceArea = "NO1"

#starter simuleringen fra Dato

startDate = 1
startMonth = 1
startYear = 2022

#fetching data for a year
#not accounting for leap year so just fetching 365 days
date = startDate
month = startMonth
year = startYear
for date in range(1,366):
    strDate = makeStr(date)
    strMonth = makeStr(month)
    link = "https://www.hvakosterstrommen.no/api/v1/prices/" + str(year) + "/" + strMonth + "-" + strDate + "_" + priceArea + ".json"

    if checkMonth(date, month) == True:
        date = 1
        month = month + 1
    else:
        date += 1

    if month == 13:
        month = 1
        year += 1

    response = requests.get(link).text

    df = pd.read_json(response)
    dfClean = df.drop(['EXR', 'EUR_per_kWh'], axis=1)

dfClean.plot()
plt.show()