import pandas as pd
import numpy as np
import deap
import matplotlib.pyplot as plt
import seaborn as sns

class SpellsPrepareProblem:
    def __init__(self):
        self.spells = []
        self.maxSpellsCapacity = 0
        
        self.__init_data()
    
    def __len__(self):
        return len(self.spells)
    
    @staticmethod
    def check_element_bonus(element1, element2):
        if (element1 == "вода" and element2 == "Огонь"):
            return True
        elif (element1 == "огонь" and element2 == "Вода"):
            return True
        elif (element1 == "молния" and element2 == "Природа"):
            return True
        elif (element1 == "природа" and element2 == "Молния"):
            return True
        elif (element1 == "свет" and element2 == "Тьма"):
            return True
        elif (element1 == "тьма" and element2 == "Свет"):
            return True
    
    def __init_data(self):

    #Загрузка данных из Excel-файла, обработка и инициализация объекта.

   # Выполняет следующие действия:
       # 1. Загружает данные из файла "Spells.xls".
       # 2. Преобразует данные в DataFrame.
       # 3. Сохраняет информацию о заклинаниях в self.spells.
       # 4. Печатает доступные стихии.
       # 5. Запрашивает у пользователя среду боя и корректирует ценность заклинаний.
       # 6. Запрашивает у пользователя стиль игры и корректирует ценность заклинаний.
       # 7. Устанавливает максимальную вместимость заклинаний (self.maxSpellsCapacity).

        try:
            # 1. Загрузка данных из Excel-файла
            data = pd.read_excel("Spells.xls")

            # 2. Преобразование данных в DataFrame
            df = pd.DataFrame(data, columns=["Название", "Круг", "Стихия", "Тип", "Ценность заклинания"])

            # 3. Сохранение информации о заклинаниях
            for i in range(len(df)):
                self.spells.append(df.iloc[i])

            # 4. Печать доступных стихий
            print("Доступные стихии:")
            unique_df = df.loc[~df["Стихия"].duplicated()]
            print(unique_df["Стихия"].to_list())
            # 5. Запрос среды боя и корректировка ценности заклинаний
            cmd = input("Выберите стихию, в среде которой планируется боёвка: ").lower()
            for i in range(len(self.spells)):
                if self.check_element_bonus(cmd, self.spells[i]["Стихия"]):
                    self.spells[i]["Ценность заклинания"] += 1

            # 6. Запрос стиля игры и корректировка ценности заклинаний
            cmd = input("Выберите стиль игры: Атакующий, Поддерживающий, Сбалансированный ").lower()
            for i in range(len(self.spells)):
                if (cmd == "атакующий") and (self.spells[i]["Тип"] == "Атакующее"):
                    self.spells[i]["Ценность заклинания"] += 1
                elif (cmd == "поддерживающий") and (self.spells[i]["Тип"] == "Поддерживающее"):
                    self.spells[i]["Ценность заклинания"] += 1

            # 7. Установка максимальной вместимости заклинаний
            cmd = input("Введите доступное количество подготовленных заклинаний ").lower()
            self.maxSpellsCapacity = int(cmd)

        except FileNotFoundError:
            print("Файл Spells.xls не найден. Проверьте наличие файла.")


            
    def getValue(self, zeroOneList):
        totalWeight = totalValue = 0

        for i in range(min(len(zeroOneList), len(self.spells))):
            item, lvl, element, tipe, value_str = self.spells[i]
            value = int(value_str)

            weight = 1
            if totalWeight + weight <= self.maxSpellsCapacity:
                totalWeight += zeroOneList[i] * weight
                totalValue += zeroOneList[i] * value

        return totalValue

    
    def printItems(self, zeroOneList):
        
        totalWeight = totalValue = 0
        listOfItems = ''
        
        for i in range(len(zeroOneList)):
            item, lvl, element, tipe, value = self.spells[i]
            weight = 1
            
            if totalWeight + weight <= self.maxSpellsCapacity:
                if zeroOneList[i] > 0:
                    totalWeight += weight
                    totalValue += value
                    listOfItems += item + ', '
                    print("Добавлено {}: круг {}, стихия {}, тип {}, ценность {}. Суммарный вес {}, суммарная ценность {}".format(item, lvl, element, tipe, value, totalWeight, totalValue))
        print ("Сборка завершена. Количество подготовленных заклинаний {}, общая ценность {}".format(totalWeight, totalValue))
        print ("Общий список рекомендуемых заклинаний: {}".format(listOfItems)) 
  