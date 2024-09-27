class Backpack:
    def __init__(self):
        #Создаём список объектов и устанавливаем максимальный вес рюкзака
        self.items = []
        self.maxCapacity = 0
        
        self.__init_data()
    
    def __len__(self):
        return len(self.items)
    
    def __init_data(self):
        
        self.items = [
            ("карта", 9, 150),
            ("компас", 13, 35),
            ("вода", 153, 200),
            ("бутерброд", 50, 160),
            ("глюкоза", 15, 60),
            ("банка", 68, 45),
            ("банан", 27, 60),
            ("яблоко", 39, 40),
            ("сыр", 23, 30),
            ("кресало", 5, 80),
            ("крем от загара", 11, 70),
            ("камера", 32, 30),
            ("футболка", 24, 15),
            ("брюки", 48, 10),
            ("зонтик", 73, 40),
            ("водонепроницаемые брюки", 42, 70),
            ("водонепроницаемая верхняя одежда", 43, 75),
            ("портмоне", 22, 80),
            ("солнечные очки", 7, 20),
            ("полотенце", 18, 12),
            ("носки", 4, 50),
            ("книга", 30, 10)
        ]
    
        self.maxCapacity = 400

    def getValue(self, zeroOneList):
        totalWeight = totalValue = 0

        for i in range(min(len(zeroOneList), len(self.items))):
            item, weight, value = self.items[i]
            if totalWeight + weight <= self.maxCapacity:
                totalWeight += zeroOneList[i] * weight
                totalValue += zeroOneList[i] * value
        return totalValue,
    
    def printItems(self, zeroOneList):
        
        totalWeight = totalValue = 0
        listOfItems = ''
        
        for i in range(len(zeroOneList)):
            item, weight, value = self.items[i]
            if totalWeight + weight <= self.maxCapacity:
                totalWeight += weight
                totalValue += value
                listOfItems += item + ', '
                print("Добавлено {}: вес {}, ценность {}. Суммарный вес {}, суммарная ценность {}".format(item, weight, value, totalWeight, totalValue))
        print ("Сборка завершена. Общий вес {}, общая ценность груза {}".format(totalWeight, totalValue))
        print ("Общий список рекомендуемых предметов: {}".format(listOfItems)) 