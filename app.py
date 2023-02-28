# Definering av funksjoner og importering av bibiliotek
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

# Finner medgåtte måneder
def getElapsedMonths(startMonth, startYear, month, year):
    elapsedMonths = 0
    elapsedMonths += (year - startYear) * 12
    elapsedMonths += month - startMonth
    return elapsedMonths

# Finner kapasietsleddet basert på forbruk
def getCapacityLink(maxCapacity):
    value= 0
    if maxCapacity < 2: value= 1
    elif maxCapacity >= 2 and maxCapacity < 5: value= 2
    elif maxCapacity >= 5 and maxCapacity < 10: value= 3
    elif maxCapacity >= 10 and maxCapacity < 15: value= 4
    elif maxCapacity >= 15 and maxCapacity < 20: value= 5
    elif maxCapacity >= 20 and maxCapacity < 25: value= 6
    elif maxCapacity >= 25 and maxCapacity < 50: value= 7
    elif maxCapacity >= 50 and maxCapacity < 75: value= 8
    elif maxCapacity >= 75 and maxCapacity < 100: value= 9
    elif maxCapacity >= 100: value= 10

    # Trekker fra 1 for at det skal passe med index i kapasitetsleddlisten
    index = value - 1 
    return index

# Finner kapasietsleddkostnad basert på kapasitetsleddnivå
def findCapacityPrice(consumptionList, capacityList):
    capacity = 0
    for j in consumptionList:
        if j > capacity:
            capacity = j
    newLink = getCapacityLink(capacity)
    newPrice = capacityList[newLink]
    return newPrice


# Definerer konstanter
evenMonth = [4, 6, 9, 11]
oddMonth = [1, 3, 5, 7, 8, 10, 12]
flag = 0

# Liste som beskriver forbruk over dagen per time
normalConsumptionPercent = [        0.068775791, 0.055020633, 0.056396149, 0.057771664,
                                    0.05914718, 0.027510316, 0.023383769, 0.024759285,
                                    0.03301238, 0.068775791, 0.057771664, 0.037138927,
                                    0.024759285, 0.031636864, 0.031636864, 0.034387895,
                                    0.020632737, 0.038514443, 0.068775791, 0.03301238,
                                    0.034387895,0.037138927,0.034387895,0.041265475 ]

# Liste som beskriver forbruk over dagen per time med Energy buff sin batteripakke
normalConsumptionWBPercent = [0.06232687, 0.06232687, 0.06232687, 0.06232687,
                                    0.06232687, 0.06232687, 0.0, 0.0,
                                    0.0, 0.0, 0.009695291, 0.06232687,
                                    0.06232687, 0.06232687, 0.06232687, 0.06232687,
                                    0.041551247, 0.041551247, 0.027700831, 0.013850416,
                                    0.013850416,0.055401662,0.055401662,0.06232687 ]

# Liste med priser ppå alle kapasitetsleddnivå
capacityLinkList = [                168.75, 281.25,
                                    462.50, 822.50,
                                    1092.50, 1355.00,
                                    2100.00, 3287.50,
                                    4475.00, 7252.50]

normalYearlyConsumption = []
normalYearlyConsumptionWB = []

fileName = "strom2022.csv"
df = pd.read_csv(fileName)


# Bruker input
priceArea = "NO1"
yearlyConsumption = 72*365
capacityLink = 3

# Beregninger
dailyConsumption = yearlyConsumption / 365
normalConsumption = [i * dailyConsumption for i in normalConsumptionPercent]
normalConsumptionWB = [i * dailyConsumption for i in normalConsumptionWBPercent]


# Verdier for simulering
startDate = 1
startMonth = 1
startYear = 2022
days = 365

date = startDate
month = startMonth
year = startYear
elapsedMonths = 0

for i in range(0,days):
    normalYearlyConsumption.extend(normalConsumption)
    normalYearlyConsumptionWB.extend(normalConsumptionWB)

    # Bytter dag og endrer år om nødvendig
    date, month = checkMonth(date, month)
    if month == 13:
        month = 1
        year = year + 1
flag = 0


# Legger på kolonner
df['consumption'] = normalYearlyConsumption
df['consumption_cost'] = df['consumption']*df['NOK_per_kWh']
df['consumption_with_battery'] = normalYearlyConsumptionWB
df['consumption_cost_with_battery'] = df['consumption_with_battery']*df['NOK_per_kWh']


elapsedMonths = getElapsedMonths(startMonth, startYear, month, year)
newCapacityLinkPrice = findCapacityPrice(normalConsumptionWB, capacityLinkList)
capacityLinkDiff = elapsedMonths * (capacityLinkList[capacityLink - 1] - newCapacityLinkPrice)


cost_with_battery = df['consumption_cost_with_battery'].sum()
cost_without_battery = df['consumption_cost'].sum()

saved = cost_without_battery - cost_with_battery 
total_saved = saved + capacityLinkDiff

# Utskrift av nøkkelverdier
print("Regnskap")
print("Penger spart uten kapasitetsledd: " + str(round(saved, 2)))
print("Penger spart i kapasitetsledd:    " + str(round(capacityLinkDiff, 2)))
print("Totalt spart gjennom perioden:    " + str(round(total_saved, 2)))
print("Gammel nettleie pris per måned:   " + str(capacityLinkList[capacityLink - 1]))
print("Ny nettleie pris per måned:       " + str(newCapacityLinkPrice))