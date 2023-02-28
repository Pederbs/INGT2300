import requests
import pandas as pd
import matplotlib.pyplot as plt

# Ittererer dagene og sjekker om det er nødvendig å bytte måned
def checkMonth(cDate, cMonth):
    if ((cDate == 31) and (cMonth in oddMonth)):
        cDate = 1
        cMonth = cMonth + 1
        return cDate, cMonth
    elif ((cDate == 30) and (cMonth in evenMonth)):
        cDate = 1
        cMonth = cMonth + 1
        return cDate, cMonth
    elif ((cDate == 28) and (cMonth == 2)):
        cDate = 1
        cMonth = cMonth + 1
        return cDate, cMonth
    else:
        cDate = cDate + 1
        return cDate, cMonth

# Gjør nummerene til ord så de kan bli brukt i API'en
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
prices = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# Beskriver hvor .CSV filen skal lagres
# Denne må byttes om du ikke heter Peder og booter fra linux
fileName = "strom.csv"
fileLocation = "/home/peder/GitHub/INGT2300/" + fileName

# Bruker input
date = 1
month = 12
year = 2021

priceArea = "NO1"
yearlyConsumption = 72*365
capacityLink = None
carChargerPower = None
# Legge inn en noe som estimerer hvor mye en sparer på fornybar delen ved å: trekke fra 80% av spotpris og få ned kjøpt kw?
# Litt usikker på implementeringen
renewableEnergy = None


#fetching data for a year
#not accounting for leap year so just fetching 365 days
for i in range(0,432):
    strDate = makeStr(date)
    strMonth = makeStr(month)
    # Bygger link for å hente data
    link = "https://www.hvakosterstrommen.no/api/v1/prices/" + str(year) + "/" + strMonth + "-" + strDate + "_" + priceArea + ".json"
    # Henter data
    response = requests.get(link).text
    df = pd.read_json(response)
    # Rydder data 
    df = df.drop(['EXR', 'EUR_per_kWh','time_end', 'time_start'], axis=1)

    # Når nasjonen bytter tidssone blir det kluss fordi vi ikke får de forventede 24 tastene 
    # Tar da et gjennomsnitt av 23 datapunkt og legger det inn for sommertid
    # For vinterstid tar vi vekk 3 tast i døgnet
    if len(df.index) < 24:
        missing = 24 - len(df.index)
        avg = df['NOK_per_kWh'].sum()/len(df.index)
        for i in range(missing):
            df.loc[len(df.index)] = [avg, 0]
    elif len(df.index) == 25:
       df.drop(3, axis=0, inplace=True)
    

    for j in range(0,24):
        prices[j] = prices[j] + df['NOK_per_kWh'].iloc[j]



    # Bytter dag og endrer år om nødvendig
    date, month = checkMonth(date, month)
    if month == 13:
        month = 1
        year = year + 1
plt.bar(range(24),prices)
plt.show()