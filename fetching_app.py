import requests
import pandas as pd
import matplotlib.pyplot as plt

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
# Liste som beskriver forbruk over dagen
normalConsumptionPercent = [    0.068775791, 
                                0.055020633, 
                                0.056396149, 
                                0.057771664,
                                0.05914718,
                                0.027510316,
                                0.023383769,
                                0.024759285,
                                0.03301238,
                                0.068775791,
                                0.057771664,
                                0.037138927,
                                0.024759285,
                                0.031636864,
                                0.031636864,
                                0.034387895,
                                0.020632737,
                                0.038514443,
                                0.068775791,
                                0.03301238,
                                0.034387895,
                                0.037138927,
                                0.034387895,
                                0.041265475
                                ]

normalConsumptionWBatteryPercent = [   0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                0.041666667,
                                ]

#https://norgesnett.no/kunde/ny-nettleie/priser-ny-nettleie/
kapasitetsLedd = [  168.75,
                    281.25,
                    462.50,
                    822.50,
                    1092.50,
                    1355.00,
                    2100.00,
                    3287.50,
                    4475.00,
                    7252.50]

# Beskriver hvor .CSV filen skal lagres
# Denne må byttes om du ikke heter Peder og bruker linux
fileName = "strom.csv"
fileLocation = "/home/peder/GitHub/INGT2300/" + fileName

# Bruker input
priceArea = "NO1"
date = 27
month = 3
year = 2022
weeklyConsumption = 72.7

# Beregner konstnad basert på forbruk
normalConsumption = [i * weeklyConsumption for i in normalConsumptionPercent]
normalConsumptionWBattery = [i * weeklyConsumption for i in normalConsumptionWBatteryPercent]

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
    # Rydder data 
    df = df.drop(['EXR', 'EUR_per_kWh','time_end'], axis=1)

    # Noen ganger gir API'en 23 datapunkter istedenfor de forventede 24,
    # da legger vi til et siste datapunkt som er snittet av de tidligere datapunktene.
    if len(df.index) < 24:
        missing = 24 - len(df.index)
        avg = df['NOK_per_kWh'].sum()/len(df.index)
        for i in range(missing):
            df.loc[len(df.index)] = [avg, 0]
    elif len(df.index) < 25:
        df.iloc[3]


    # Legger på kolonner
    df['consumption'] = normalConsumption
    df['consumption_cost'] = df['consumption']*df['NOK_per_kWh']
    df['consumption_with_battery'] = normalConsumptionWBattery
    df['consumption_cost_with_battery'] = df['consumption_with_battery']*df['NOK_per_kWh']
    #df['savings'] = df['consumption_cost'] - df['consumption_cost_with_battery']


    # Fjerner øverste beskrivende rad for hver dag men beholder den første
    if flag == 0:
        flag = 1
        df.to_csv(fileLocation, index=False)
    else:
        df.to_csv(fileLocation, header=False, index=False, mode="a")


    date, month = checkMonth(date, month)

    if month == 13:
        month = 1
        year = year + 1
hist = pd.read_csv(fileLocation)
hist.plot(x='time_start', y='NOK_per_kWh')
plt.show()