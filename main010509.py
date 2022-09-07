import pandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# data.row = r.read ()

# generationValue = pd.read_csv ("dataSet/askoe.small_pv.system.generation.15m.txt", sep=" ")
# print(generationValue)
# print (convert_1 (dataraw))

#DATASET
# askoe.small_pv.system.generation.15m.txt     +      genaration                  15 m
# dewpoint_celsius                             +      dewpoint                    3 h    точка роси
# downward_short_wave                          +      downward_short_wave         3 h
# sun.azi                                      +      azimuth                     15 m
# sun.ele                                      +      elevator                    15 m
# sunriseSunset                                -      sunrise sunset duration     1 d
# temperature                                  +      temperature                 3 h
# total_boundary_cloud.comb                    +      total_boundary_cloud        1 h гранична
# total_cloud                                  +      total_cloud                 3 h
# total_convective_cloud.comb                  +      total_convective_cloud      3 h конвективна
# total_high_cloud.comb                        +      total_high_cloud            3 h
# total_low_cloud.comb                         +      total_low_cloud             3 h
# total_middle_cloud.comb                      +      total_middle_cloud          3 h
# total_precipitation.comb                     +      precipitation               at time опади
# unknowhData                                  +      unknown                     at time
# upward_short_wave.comb                       +      upward_short_wave           3 h

# winter                      summer

# 2019                      26.10-27.10
# 2020                      25.10-26.10                 29.03-30.03
# 2021                      31.10-01.11                 28.03-29.03
# 2022                      27.03-28.03

# cntrl/`+
g = [] # пустий список
listName = os.listdir(("dataSet"))  # записуємо в змінну список файлів шляхи файлів закидаємо в список
listName.remove("sunriseSunset.txt") # видалення зі списку

sunrise = open("dataSet/sunriseSunset.txt")
print(listName)

for name in listName:
    g.append(open("dataSet/" + name)) # зчитуємо всі файли додаємо в список g


def convert_1(text):
    """
    функція обробляє файли перетворює в формат списків

    68 ідем з кінця data_2 рядки -1 бо з 0 номерація
    :param text: текст з файла
    :return: список списків з даних  номер час  значення
    """
    data_1 = text.split("\n")
    # data_1.replace ('"', "")
    data_2 = [d.split("\t") for d in data_1]




    for i in range(len(data_2) - 1, -1, -1): # рендж створює з останнього по кроку мінус 1 до -1

        if data_2[i][2] == '':
            del data_2[i]


    for i in range(len(data_2)): # приведення з строкової з числа або дати
        data_2[i][0] = int(data_2[i][0])
        data_2[i][1] = data_2[i][1].replace("A", "0")
        data_2[i][1] = data_2[i][1].replace("B", "0")
        data_2[i][1] = datetime.strptime(data_2[i][1], "%d.%m.%Y %H:%M:%S")

        data_2[i][2] = data_2[i][2].replace(" ", "")
        data_2[i][2] = data_2[i][2].replace(",", ".")
        data_2[i][2] = float(data_2[i][2])
    return data_2

def convert_2(text):

    data_1 = text.split("\n")

    # data_1 = data_1[:100] 100:200 :2 крок 2      в обернену сторону -1
    data_2 = [d.split("\t") for d in data_1]

    for i in range(len(data_2)): # приведення з строкової з числа dо дати
        data_2[i][0] = datetime.strptime(data_2[i][0], "%d.%m.%Y") # cntrl D copypaste raw # alt click other data backspace
        data_2[i][1] = datetime.strptime(data_2[i][1], "%H:%M")
        data_2[i][2] = datetime.strptime(data_2[i][2], "%H:%M")
        data_2[i][3] = datetime.strptime(data_2[i][3], "%H:%M")

    return data_2


dataraw = []
for gg in g:

    dataraw.append (gg.read()) # зчитуємо з відкритих даних та записуємо в датарав
    gg.close() # відступи 4 пробіли важливі інакше не сприймає як в циклі

dataSort = []# створюємо список голих даних вони вже конвенртовані в дататайм флоат запсиані в список списків
for d in dataraw:
    dataSort.append(convert_1(d)) # беремо дані кожного текстового файлу і за домомогою функції коверт перетворюємо їх в числа час дататайм
dataSort.append(convert_2(sunrise.read())) # add sunrise
sunrise.close()
# for d in dataSort:
#     print(d)


# консолідуємо данні
data = pandas.DataFrame(dataSort[0], columns=["number", "data_time", "value"])
print(data.describe()) # max min avarage

list_values = [
"genaration",
"dewpoint",
"downward_short_wave",
"azimuth",
"elevator",
# "sunrise",
"temperature",
"total_boundary_cloud",
"total_cloud",
"total_convective_cloud",
"total_high_cloud",
"total_low_cloud",
"total_middle_cloud",
"precipitation",
"unknown",
"upward_short_wave",
]


data = []
for d,k in zip(dataSort[:-1], list_values): # exeption surise еріть той список беріть другий  порівнюйте і робіть один
    data.append(pandas.DataFrame(d, columns=["number", "data_time", k]))
    print(data[-1])

data.append(pandas.DataFrame(dataSort[-1], columns=["data_time", "sunrise", "sunset", "sunDuration"]))
print(data [-1])

# консолідація в один дата сет
dataConsolidated = pandas.DataFrame ([[datetime.now()]], columns=["data_time"])
for d in data[:-1]:
    dataConsolidated =pd.merge(dataConsolidated, d.drop(columns=["number"]), how="outer", on = "data_time")
dataConsolidated =pd.merge(dataConsolidated, data[-1], how="outer", on = "data_time")
print(dataConsolidated)

# dataConsolidated["time"] = dataConsolidated["data_time"].time()

# data_concat = pd.merge(data_1, data_2, how='outer', on = 'date')
# dataConsolidated =pd.merge(dataConsolidated, data[0].drop(columns=["number"]), how="outer", on = "data_time")
# dataConsolidated =pd.merge(dataConsolidated, data[1].drop(columns=["number"]), how="outer", on = "data_time")
# dataConsolidated =pd.merge(dataConsolidated, data[2].drop(columns=["number"]), how="outer", on = "data_time")
# dataConsolidated =pd.merge(dataConsolidated, data[3].drop(columns=["number"]), how="outer", on = "data_time")
# dataConsolidated =pd.merge(dataConsolidated, data[4].drop(columns=["number"]), how="outer", on = "data_time")
# dataConsolidated =pd.merge(dataConsolidated, data[1], how="outer", on = "data_time")
# dataConsolidated =pd.merge(dataConsolidated, data[2], how="outer", on = "data_time")
# dataConsolidated =pd.merge(dataConsolidated, data[3], how="outer", on = "data_time")
#dataConsolidated =pd.merge(dataConsolidated, data[4], how="outer", on = "data_time")
#dataConsolidated =pd.merge(dataConsolidated, data[5], how="outer", on = "data_time")
#print(dataConsolidated[0:100].values)
print(dataConsolidated.info())
print(pandas.isnull(dataConsolidated).any())# аналіз пропуски

plt.scatter(dataConsolidated["data_time"], dataConsolidated["genaration"])
plt.show()# перший графік генерація енергії по датах

plt.scatter(dataConsolidated["data_time"], dataConsolidated["genaration"])
plt.show()

dataConsolidated.to_csv("data.csv")