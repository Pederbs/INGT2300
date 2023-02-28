import requests
import pandas as pd
import matplotlib.pyplot as plt

# Itererer dagene og sjekker om det er nødvendig å bytte måned
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

def getElapsedMonths(startMonth, startYear, month, year):
    elapsedMonths = 0
    elapsedMonths += (year - startYear) * 12
    elapsedMonths += month - startMonth
    return elapsedMonths

def getCapacityLink(maxCapacity):
    value= 0
    if maxCapacity < 2:
        value= 1
    elif maxCapacity >= 2 and maxCapacity < 5:
        value= 2
    elif maxCapacity >= 5 and maxCapacity < 10:
        value= 3
    elif maxCapacity >= 10 and maxCapacity < 15:
        value= 4
    elif maxCapacity >= 15 and maxCapacity < 20:
        value= 5
    elif maxCapacity >= 20 and maxCapacity < 25:
        value= 6
    elif maxCapacity >= 25 and maxCapacity < 50:
        value= 7
    elif maxCapacity >= 50 and maxCapacity < 75:
        value= 8
    elif maxCapacity >= 75 and maxCapacity < 100:
        value= 9
    elif maxCapacity >= 100:
        value= 10
    index = value- 1
    return index

def findCapacityPrice(consumptionList, capacityList):
    capacity = 0
    for j in consumptionList:
        if j > capacity:
            capacity = j
    newLink = getCapacityLink(capacity)
    newPrice = capacityList[newLink]
    return newPrice

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

normalConsumptionWBatteryPercent = [0.06232687,
                                    0.06232687,
                                    0.06232687,
                                    0.06232687,
                                    0.06232687,
                                    0.06232687,
                                    0.0,
                                    0.0,
                                    0.0,
                                    0.0,
                                    0.009695291,
                                    0.06232687,
                                    0.06232687,
                                    0.06232687,
                                    0.06232687,
                                    0.06232687,
                                    0.041551247,
                                    0.041551247,
                                    0.027700831,
                                    0.013850416,
                                    0.013850416,
                                    0.055401662,
                                    0.055401662,
                                    0.06232687
]

"""
normalConsumptionWCarPercent = [   0.101936799,
                                    0.101936799,
                                    0.101936799,
                                    0.101936799,
                                    0.101936799,
                                    0.017329256,
                                    0.018348624,
                                    0.024464832,
                                    0.0509684,
                                    0.042813456,
                                    0.027522936,
                                    0.018348624,
                                    0.023445464,
                                    0.023445464,
                                    0.0254842,
                                    0.01529052,
                                    0.028542304,
                                    0.0509684,
                                    0.024464832,
                                    0.0254842,
                                    0.027522936,
                                    0.0254842,
                                    0.03058104
]

normalConsumptionWBatteryWECarPercent = []
"""

#https://norgesnett.no/kunde/ny-nettleie/priser-ny-nettleie/
capacityLinkList = [168.75,
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
# Denne må byttes om du ikke heter Peder og booter fra linux
fileName = "strom.csv"
fileLocation = "/home/peder/GitHub/INGT2300/" + fileName

'''
# Bruker input
startDate = 1
startMonth = 12
startYear = 2021

priceArea = "NO1"
yearlyConsumption = 72*365
capacityLink = 5
carCharger = False
renewableEnergy = False
carDistance = 15000
antallPanel= 20
days = 365
#prisProduct = 30000
'''

# Bruker input
startDate = 1
startMonth = 12
startYear = 2021

priceArea = str(input("Skriv inn hvilket område i Norge du bor: \nNO1 = Øst-Norge \nNO2 = Sør-Norge \nNO3 = Midt-Norge \nNO4 = Nord-Norge \nNO5 = Vest-Norge\n"))
yearlyConsumption = float(input("Skriv inn hvor mye kW bruker du iløpet av et år: "))
capacityLink = int(input("Skriv inn hvilket kapasitetsledd du befinner deg i: "))
carCharger = int(input("Har du elbil og lader hovedsaklig hjemme? (1 = Ja, 0 = Nei) "))

carCharger = bool(carCharger)
if carCharger:
    carDistance = float(input("Hvor langt kjører du iløpet av et år: "))
renewableEnergy = int(input("Har du fornybare energikilder instalert? (1 = Ja, 0 = Nei) "))
renewableEnergy = bool(renewableEnergy)
if renewableEnergy:
    antallPanel= int(input("hvor mange solcelle panel har du: "))
days = int(input("Hvor mange dager vil du simulere? "))
#prisProduct = 30000

# Beregner konstnad basert på forbruk

# lenke til effektivitetsestimat solceller
# https://www.nve.no/energi/energisystem/solkraft/#:~:text=Et%20solcelleanlegg%20p%C3%A5%20et%20tak,prosent%20av%20str%C3%B8mforbruket%20til%20boligen.

# Lenke til effektivitetsestimat bil
# https://www.fjordkraft.no/strom/stromforbruk/elbil/#:~:text=Kj%C3%B8rer%20du%2010.000%20km%20i,dette%20redusere%20str%C3%B8mkostnaden%20enda%20mer.

###########################################################################
###### IMPLEMENTASJONEN AV ELBIL OG SOLCELLE ER FEIL ######################
###########################################################################

# ikke riktig å legge på eller trekke fra strøm  da vi spør om totalt forbruk 
# 3 ganger så lønnsomt å bruke enn å selge
# Alt er regnet ex moms


if renewableEnergy:
    effectPrPanel = 850 / 20    #850kW på et år for 220 panel
    solarEnergy = antallPanel * effectPrPanel
if carCharger:
    effectPrDistance = 2000 / 10000
    carEnergy = carDistance * effectPrDistance

if not carCharger and renewableEnergy:
    dailyConsumptionWSolar = (yearlyConsumption - solarEnergy) / 365
    normalConsumptionWSolar = [i * dailyConsumptionWSolar for i in normalConsumptionPercent]
    normalConsumptionWBatteryAndSolar = [i * dailyConsumptionWSolar for i in normalConsumptionWBatteryPercent]

elif carCharger and not renewableEnergy:
    dailyConsumptionWCar = (yearlyConsumption + carEnergy) / 365
    normalConsumptionWCar = [i * dailyConsumptionWCar for i in normalConsumptionPercent]
    normalConsumptionWBatteryAndCar = [i * dailyConsumptionWCar for i in normalConsumptionWBatteryPercent]

elif carCharger and renewableEnergy:
    dailyConsumptionWCarAndSolar = (yearlyConsumption + carEnergy - solarEnergy) / 365
    normalConsumptionWCarAndSolar = [i * dailyConsumptionWCarAndSolar for i in normalConsumptionPercent]
    normalConsumptionWBatteryAndCarAndSolar = [i * dailyConsumptionWCarAndSolar for i in normalConsumptionWBatteryPercent]
else:
    dailyConsumption = yearlyConsumption / 365
    normalConsumption = [i * dailyConsumption for i in normalConsumptionPercent]
    normalConsumptionWBattery = [i * dailyConsumption for i in normalConsumptionWBatteryPercent]

date = startDate
month = startMonth
year = startYear
elapsedMonths = 0

#fetching data for a year
#not accounting for leap year so just fetching 365 days
for i in range(0,days):
    strDate = makeStr(date)
    strMonth = makeStr(month)
    # Bygger link for å hente data
    link = "https://www.hvakosterstrommen.no/api/v1/prices/" + str(year) + "/" + strMonth + "-" + strDate + "_" + priceArea + ".json"
    # Henter data
    response = requests.get(link).text
    df = pd.read_json(response)
    # Rydder data 
    df = df.drop(['EXR', 'EUR_per_kWh','time_end'], axis=1)

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

    # Legger på kolonner
    if not carCharger and renewableEnergy:
        df['consumption_with_solar'] = normalConsumptionWSolar
        df['consumption_cost_with_solar'] = df['consumption_with_solar']*df['NOK_per_kWh']
        df['consumption_with_battery_and_solar'] = normalConsumptionWBatteryAndSolar
        df['consumption_cost_with_battery_and_solar'] = df['consumption_with_battery_and_solar']*df['NOK_per_kWh']

    elif carCharger and not renewableEnergy:
        df['consumption_with_car'] = normalConsumptionWCar
        df['consumption_cost_with_car'] = df['consumption_with_car']*df['NOK_per_kWh']
        df['consumption_with_battery_and_car'] = normalConsumptionWBatteryAndCar
        df['consumption_cost_with_battery_and_car'] = df['consumption_with_battery_and_car']*df['NOK_per_kWh']

    elif carCharger and renewableEnergy:
        df['consumption_with_car_and_solar'] = normalConsumptionWCarAndSolar
        df['consumption_cost_with_car_and_solar'] = df['consumption_with_car_and_solar']*df['NOK_per_kWh']
        df['consumption_with_battery_and_car_and_solar'] = normalConsumptionWBatteryAndCarAndSolar
        df['consumption_cost_with_battery_and_car_and_solar'] = df['consumption_with_battery_and_car_and_solar']*df['NOK_per_kWh']
    else:
        df['consumption'] = normalConsumption
        df['consumption_cost'] = df['consumption']*df['NOK_per_kWh']
        df['consumption_with_battery'] = normalConsumptionWBattery
        df['consumption_cost_with_battery'] = df['consumption_with_battery']*df['NOK_per_kWh']


    # Fjerner øverste beskrivende rad for hver dag men beholder den første
    if flag == 0:
        flag = 1
        df.to_csv(fileLocation, index=False)
    else:
        df.to_csv(fileLocation, header=False, index=False, mode="a")
    # Bytter dag og endrer år om nødvendig
    date, month = checkMonth(date, month)
    if month == 13:
        month = 1
        year = year + 1


elapsedMonths = getElapsedMonths(startMonth, startYear, month, year)

if not carCharger and renewableEnergy:
    newCapacityLinkPriceWSolar = findCapacityPrice(normalConsumptionWBatteryAndSolar, capacityLinkList)
    capacityLinkDiffWSolar = elapsedMonths * newCapacityLinkPriceWSolar - capacityLinkList[capacityLink-1] * elapsedMonths

elif carCharger and not renewableEnergy:
    newCapacityLinkPriceWCar = findCapacityPrice(normalConsumptionWBatteryAndCar, capacityLinkList)
    capacityLinkDiffWCar = elapsedMonths * newCapacityLinkPriceWCar - capacityLinkList[capacityLink-1] * elapsedMonths

elif carCharger and renewableEnergy:
    newCapacityLinkPriceWCarAndSolar = findCapacityPrice(normalConsumptionWBatteryAndCarAndSolar, capacityLinkList)
    capacityLinkDiffWCarAndSolar = elapsedMonths * newCapacityLinkPriceWCarAndSolar - capacityLinkList[capacityLink-1] * elapsedMonths

else:
    newCapacityLinkPrice = findCapacityPrice(normalConsumptionWBattery, capacityLinkList)
    capacityLinkDiff = elapsedMonths * newCapacityLinkPrice - capacityLinkList[capacityLink-1] * elapsedMonths

# Henter hele simulasjonen for å gjøre beregninger
hist = pd.read_csv(fileLocation)


if not carCharger and renewableEnergy:
    cost_with_battery_and_solar = hist['consumption_cost_with_battery_and_solar'].sum()
    cost_without_battery_and_solar = hist['consumption_cost_with_solar'].sum()
    saved_solar = cost_without_battery_and_solar - cost_with_battery_and_solar
    total_saved_solar = saved_solar + capacityLinkDiffWSolar

    print("\nRegnskap med solenergi")
    print("Penger spart uten kapasitetsledd: " + str(round(saved_solar, 2)))
    print("Penger spart i kapasitetsledd:    " + str(round(capacityLinkDiffWSolar, 2)))
    print("Totalt spart gjennom perioden:    " + str(round(total_saved_solar, 2)))

elif carCharger and not renewableEnergy:
    cost_with_battery_and_car = hist['consumption_cost_with_battery_and_car'].sum()
    cost_without_battery_and_car = hist['consumption_cost_with_car'].sum()
    saved_car = cost_without_battery_and_car - cost_with_battery_and_car
    total_saved_car = saved_car + capacityLinkDiffWCar

    print("\nRegnskap med elbil")
    print("Penger spart uten kapasitetsledd: " + str(round(saved_car, 2)))
    print("Penger spart i kapasitetsledd:    " + str(round(capacityLinkDiffWCar, 2)))
    print("Totalt spart gjennom perioden:    " + str(round(total_saved_car, 2)))

elif carCharger and renewableEnergy:
    cost_with_battery_and_car_and_solar = hist['consumption_cost_with_battery_and_car_and_solar'].sum()
    cost_without_battery_and_car_and_solar = hist['consumption_cost_with_car_and_solar'].sum()
    saved_car_and_solar = cost_without_battery_and_car_and_solar - cost_with_battery_and_car_and_solar
    total_saved_car_and_solar = saved_car_and_solar + capacityLinkDiffWCar

    print("\nRegnskap med elbil og solceller")
    print("Penger spart uten kapasitetsledd: " + str(round(saved_car_and_solar, 2)))
    print("Penger spart i kapasitetsledd:    " + str(round(capacityLinkDiffWCarAndSolar, 2)))
    print("Totalt spart gjennom perioden:    " + str(round(total_saved_car_and_solar, 2)))

else:
    cost_with_battery = hist['consumption_cost_with_battery'].sum()
    cost_without_battery = hist['consumption_cost'].sum()
    saved = cost_without_battery - cost_with_battery 
    total_saved = saved + capacityLinkDiff

    print("\nRegnskap uten elbil eller fornybar energi")
    print("Penger spart uten kapasitetsledd: " + str(round(saved, 2)))
    print("Penger spart i kapasitetsledd:    " + str(round(capacityLinkDiff, 2)))
    print("Totalt spart gjennom perioden:    " + str(round(total_saved, 2)))


#hist.plot(x='time_start', y='NOK_per_kWh')
#plt.show()