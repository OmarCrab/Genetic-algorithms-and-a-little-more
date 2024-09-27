import numpy as np


class NurseSchedulingProblem:
    """Этот класс инкапсулирует проблему расписания медсестер
    """

    def __init__(self, hardConstraintPenalty):
        """
        :param hardConstraintPenalty: коэффициент штрафа за нарушение жесткого ограничения
        """
        self.hardConstraintPenalty = hardConstraintPenalty

        # список медсестер:
        self.nurses = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # предпочтения смен медсестер - утро, вечер, ночь:
        self.shiftPreference = [[1, 0, 0], [1, 1, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 1, 1], [1, 1, 1]]

        # минимальное и максимальное количество медсестер, разрешенных для каждой смены - утро, вечер, ночь:
        self.shiftMin = [2, 2, 1]
        self.shiftMax = [3, 4, 2]

        # максимальное количество смен в неделю, разрешенное для каждой медсестры
        self.maxShiftsPerWeek = 5

        # количество недель, для которых создается расписание:
        self.weeks = 1

        # полезные значения:
        self.shiftPerDay = len(self.shiftMin)
        self.shiftsPerWeek = 7 * self.shiftPerDay

    def __len__(self):
        """
        :return: количество смен в расписании
        """
        return len(self.nurses) * self.shiftsPerWeek * self.weeks

    def getCost(self, schedule):
        """
        Вычисляет общую стоимость различных нарушений в данном расписании
        ...
        :param schedule: список бинарных значений, описывающих данное расписание
        :return: вычисленная стоимость
        """

        if len(schedule) != self.__len__():
            raise ValueError("размер списка расписания должен быть равен ", self.__len__())

        # преобразовать все расписание в словарь с отдельным расписанием для каждой медсестры:
        nurseShiftsDict = self.getNurseShifts(schedule)

        # подсчитать различные нарушения:
        consecutiveShiftViolations = self.countConsecutiveShiftViolations(nurseShiftsDict)
        shiftsPerWeekViolations = self.countShiftsPerWeekViolations(nurseShiftsDict)[1]
        nursesPerShiftViolations = self.countNursesPerShiftViolations(nurseShiftsDict)[1]
        shiftPreferenceViolations = self.countShiftPreferenceViolations(nurseShiftsDict)

        # вычислить стоимость нарушений:
        hardContstraintViolations = consecutiveShiftViolations + nursesPerShiftViolations + shiftsPerWeekViolations
        softContstraintViolations = shiftPreferenceViolations

        return self.hardConstraintPenalty * hardContstraintViolations + softContstraintViolations

    def getNurseShifts(self, schedule):
        """
        Преобразует все расписание в словарь с отдельным расписанием для каждой медсестры
        :param schedule: список бинарных значений, описывающих данное расписание
        :return: словарь, где каждая медсестра является ключом, а соответствующие смены - значением
        """
        shiftsPerNurse = self.__len__() // len(self.nurses)
        nurseShiftsDict = {}
        shiftIndex = 0

        for nurse in self.nurses:
            nurseShiftsDict[nurse] = schedule[shiftIndex:shiftIndex + shiftsPerNurse]
            shiftIndex += shiftsPerNurse

        return nurseShiftsDict

    def countConsecutiveShiftViolations(self, nurseShiftsDict):
        """
        Подсчитывает нарушения последовательных смен в расписании
        :param nurseShiftsDict: словарь с отдельным расписанием для каждой медсестры
        :return: количество найденных нарушений
        """
        violations = 0
        # итерация по сменам каждой медсестры:
        for nurseShifts in nurseShiftsDict.values():
            # поиск двух последовательных '1':
            for shift1, shift2 in zip(nurseShifts, nurseShifts[1:]):
                if shift1 == 1 и shift2 == 1:
                    violations += 1
        return violations

    def countShiftsPerWeekViolations(self, nurseShiftsDict):
        """
        Подсчитывает нарушения максимального количества смен в неделю в расписании
        :param nurseShiftsDict: словарь с отдельным расписанием для каждой медсестры
        :return: количество найденных нарушений
        """
        violations = 0
        weeklyShiftsList = []
        # итерация по сменам каждой медсестры:
        for nurseShifts in nurseShiftsDict.values():  # все смены одной медсестры
            # итерация по сменам каждой недели:
            for i in range(0, self.weeks * self.shiftsPerWeek, self.shiftsPerWeek):
                # подсчет всех '1' за неделю:
                weeklyShifts = sum(nurseShifts[i:i + self.shiftsPerWeek])
                weeklyShiftsList.append(weeklyShifts)
                if weeklyShifts > self.maxShiftsPerWeek:
                    violations += weeklyShifts - self.maxShiftsPerWeek

        return weeklyShiftsList, violations

    def countNursesPerShiftViolations(self, nurseShiftsDict):
        """
        Подсчитывает нарушения количества медсестер на смену в расписании
        :param nurseShiftsDict: словарь с отдельным расписанием для каждой медсестры
        :return: количество найденных нарушений
        """
        # суммирование смен по всем медсестрам:
        totalPerShiftList = [sum(shift) for shift in zip(*nurseShiftsDict.values())]

        violations = 0
        # итерация по всем сменам и подсчет нарушений:
        for shiftIndex, numOfNurses in enumerate(totalPerShiftList):
            dailyShiftIndex = shiftIndex % self.shiftPerDay  # -> 0, 1 или 2 для 3 смен в день
            if (numOfNurses > self.shiftMax[dailyShiftIndex]):
                violations += numOfNurses - self.shiftMax[dailyShiftIndex]
            elif (numOfNurses < self.shiftMin[dailyShiftIndex]):
                violations += self.shiftMin[dailyShiftIndex] - numOfNurses

        return totalPerShiftList, violations

    def countShiftPreferenceViolations(self, nurseShiftsDict):
        """
        Подсчитывает нарушения предпочтений медсестер в расписании
        :param nurseShiftsDict: словарь с отдельным расписанием для каждой медсестры
        :return: количество найденных нарушений
        """
        violations = 0
        for nurseIndex, shiftPreference in enumerate(self.shiftPreference):
            # дублирование предпочтений смен на дни периода
            preference = shiftPreference * (self.shiftsPerWeek // self.shiftPerDay)
            # итерация по сменам и сравнение с предпочтениями:
            shifts = nurseShiftsDict[self.nurses[nurseIndex]]
            for pref, shift in zip(preference, shifts):
                if pref == 0 и shift == 1:
                    violations += 1

        return violations

    def printScheduleInfo(self, schedule):
        """
        Печатает информацию о расписании и нарушениях
        :param schedule: список бинарных значений, описывающих данное расписание
        """
        nurseShiftsDict = self.getNurseShifts(schedule)

        print("Расписание для каждой медсестры:")
        for nurse in nurseShiftsDict:  # все смены одной медсестры
            print(nurse, ":", nurseShiftsDict[nurse])

        print("нарушения последовательных смен = ", self.countConsecutiveShiftViolations(nurseShiftsDict))
        print()

        weeklyShiftsList, violations = self.countShiftsPerWeekViolations(nurseShiftsDict)
        print("недельные смены = ", weeklyShiftsList)
        print("нарушения смен в неделю = ", violations)
        print()

        totalPerShiftList, violations = self.countNursesPerShiftViolations(nurseShiftsDict)
        print("медсестры на смену = ", totalPerShiftList)
        print("нарушения количества медсестер на смену = ", violations)
        print()

        shiftPreferenceViolations = self.countShiftPreferenceViolations(nurseShiftsDict)
        print("нарушения предпочтений смен = ", shiftPreferenceViolations)
        print()


# тестирование класса:
def main():
    # создание экземпляра проблемы:
    nurses = NurseSchedulingProblem(10)

    randomSolution = np.random.randint(2, size=len(nurses))
    print("Случайное решение = ")
    print(randomSolution)
    print()

    nurses.printScheduleInfo(randomSolution)

    print("Общая стоимость = ", nurses.getCost(randomSolution))


if __name__ == "__main__":
    main()