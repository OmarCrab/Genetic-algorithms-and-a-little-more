from deap import tools
from deap import algorithms

def eaSimpleWithElitism(population, toolbox, cxpb, mutpb, ngen, stats=None,
                       halloffame=None, verbose=__debug__):

  '''
  Эта функция реализует простой генетический алгоритм с элитизмом.

  Args:
      population: Начальная популяция кандидатов (решений).
      toolbox: Набор инструментов, содержащий функции для оценки,
                скрещивания, мутации и отбора.
      cxpb: Вероятность кроссовера (скрещивания) между двумя особями.
      mutpb: Вероятность мутации отдельного гена особи.
      ngen: Число поколений, которые должен выполнить алгоритм.
      stats: (Необязательно) Объект статистики для сбора данных о
             популяции во время эволюции.
      halloffame: Зал славы для хранения лучших особей на протяжении
                 поколений.
      verbose: (Необязательно) Флаг для включения печати информации
               о ходе алгоритма.

  Returns:
      tuple: Кортеж, содержащий финальную популяцию и журнал
             (logbook) с информацией о процессе эволюции.
    '''
    
  # Журнал для записи информации о ходе алгоритма
  logbook = tools.Logbook()
  logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

  # Оценка особей с невалидным значением функции приспособленности
  invalid_ind = [ind for ind in population if not ind.fitness.valid]
  fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
  for ind, fit in zip(invalid_ind, fitnesses):
      ind.fitness.values = fit

  if halloffame is None:
      raise ValueError("Зал славы (halloffame) не может быть пустым!")

  # Добавление начальной популяции в зал славы
  halloffame.update(population)
  hof_size = len(halloffame.items) if halloffame.items else 0

  # Сбор статистики по начальной популяции (если stats задан)
  record = stats.compile(population) if stats else {}
  logbook.record(gen=0, nevals=len(invalid_ind), **record)
  if verbose:
      print(logbook.stream)

  # Цикл поколений
  for gen in range(1, ngen + 1):

      # Отбор особей для следующего поколения (исключая лучших из зала славы)
      offspring = toolbox.select(population, len(population) - hof_size)

      # Вариация пула особей (скрещивание и мутация)
      offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

      # Оценка особей с невалидным значением функции приспособленности
      invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
      fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
      for ind, fit in zip(invalid_ind, fitnesses):
          ind.fitness.values = fit

      # Добавление лучших особей из зала славы обратно в популяцию
      offspring.extend(halloffame.items)

      # Обновление зала славы новыми особями
      halloffame.update(offspring)

      # Замена текущей популяции на следующее поколение
      population[:] = offspring

      # Сбор статистики по новому поколению (если stats задан)
      record = stats.compile(population) if stats else {}
      logbook.record(gen=gen, nevals=len(invalid_ind), **record)
      if verbose:
          print(logbook.stream)

  return population, logbook