from tabulate import tabulate


def rungeKutte(x0, y0, h, x_last, f, solution, eps=None, log=False, from_main=False):
    xValues = [x0]
    yValues = [y0]
    calculation_table = []

    while round(x0 + 3 * h, 5) > x_last:
        h *= 0.5
    solution_array = []
    while xValues[-1] <= x_last:
        prX = xValues[-1]
        prY = yValues[-1]
        k1 = h * f(prX, prY)
        k2 = h * f(prX + 0.5 * h, prY + 0.5 * k1)
        k3 = h * f(prX + 0.5 * h, prY + 0.5 * k2)
        k4 = h * f(prX + h, prY + k3)
        if prX == x_last:
            break
        try:
            calculation_table.append([len(xValues), prX, k1, k2, k3, k4, prY, f(prX, prY)])
            solution_array.append(solution([prX, x_last], y0, f)[1])
        except Exception as ex:
            print(ex)
        yValues.append(prY + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4))
        xValues.append(round(prX + h, 5))
    calculation_table.append([len(xValues), xValues[-1], k1, k2, k3, k4, yValues[-1], f(xValues[-1], yValues[-1])])
    solution_array.append(solution([prX, prX + h], y0, f)[1])
    if eps is not None:  # Проверка точности и изменение шага h
        h_half = h * 0.5
        x2h, y2h = rungeKutte(x0, y0, h_half, x_last, f, solution, log=log)
        R = abs((yValues[-1] - y2h[-1]) / (2 ** 1 - 1))
        if R > eps:
            return rungeKutte(x0, y0, h_half, f, solution, eps, log=log, from_main=from_main)
        else:
            print(f"По правилу Рунге точность: {round(yValues[-1], 5)} - {round(y2h[-1], 5)} = {round(R, 5)}")
            # print(f"По правилу Рунге точность: {yValues[-1]} - {(y2h[-1])} = {(R)}")
            # return xValues, yValues

    for j in range(len(calculation_table)):
        try:
            calculation_table[j].append(solution_array[len(calculation_table) - j - 1])
        except Exception as ex:
            print(ex)
    if log and from_main:
        print(f"Шаг: {h}")
        field_names = ["i", "x", "k1", "k2", "k3", "k4", "y", "F(x,y)", "Точное решение"]
        print(tabulate(calculation_table, field_names, tablefmt='grid', floatfmt='2.4f'))
    return xValues, yValues


def euler(x0, y0, h, x_last, f, solution, eps=None, log=False, from_main=False):
    xValues = [x0]
    yValues = [y0]
    calculation_table = []

    while round(x0 + 3 * h, 5) > x_last:
        print(f"Шаг изменяем с {h} на {h * 0.5}, поскольку шаг слишком большой для данного промежутка")
        h *= 0.5
    i = 1
    solution_array = []
    while xValues[-1] <= x_last:
        x = xValues[-1]
        y = yValues[-1]
        if x == x_last:  # it can result in a potential issue because this indicates that you are trying to solve the differential equation over a single point in time.
            break
        try:
            calculation_table.append([i, x, y, f(x, y)])
            solution_array.append(solution([x, x_last], y0, f)[1])
        except Exception as ex:
            print(ex)

        # Вычисление следующего значения y с использованием метода Эйлера
        y_next = y + h * f(x, y)
        x_next = round(x + h, 5)

        xValues.append(x_next)
        yValues.append(y_next)
        i += 1
    calculation_table.append([i, x_next, y_next, f(x, y)])  # ???
    solution_array.append(solution([x_next, xValues[-1] + h], y0, f)[1])  # ???
    for j in range(len(calculation_table)):
        try:
            calculation_table[j].append(solution_array[len(calculation_table) - j - 1])
        except IndexError:
            pass
    # Вычисление погрешности по правилу Рунге
    if eps is not None:
        h_half = h / 2
        x2h, Y2h = euler(x0, y0, h_half, x_last, f, solution, from_main=from_main)
        R = abs((yValues[-1] - Y2h[-1]) / (2 ** 1 - 1))

        if R > eps:
            # Уменьшаем шаг и повторяем вычисления
            return euler(x0, y0, h_half, x_last, f, solution, eps, from_main=from_main)
        else:
            print(f"По правилу Рунге точность: {round(yValues[-1], 5)} - {round(Y2h[-1], 5)} = {round(R, 5)}")
            # print(f"Шаг: {h}")
            return xValues, yValues
    if from_main:
        print(f"Шаг: {h}")
        field_names = ["i", "x", "y", "F(x,y)", "Точное решение"]
        print(tabulate(calculation_table, field_names, tablefmt='grid', floatfmt='2.4f'))
    return xValues, yValues


def adams(x0, y0, h, x_last, f, solution, eps=None, log=False, from_main=False):
    xValues = [x0]
    yValues = [y0]
    calculation_table = []
    while round(x0 + 3 * h, 5) > x_last:
        h *= 0.5
    # Вычисление начальных значений с помощью метода Рунге-Кутты
    x, y = rungeKutte(x0, y0, h, x0 + 3 * h, f, solution, eps=None, log=True)
    yValues.extend(y[1:4])
    xValues.extend(x[1:4])
    fValues = [f(x, y) for x, y in zip(xValues, yValues)]
    solution_array = [solution([x0, x_last], y0, f)[1]]
    solution_array.append(solution([xValues[1], x_last], y0, f)[1])
    solution_array.append(solution([xValues[2], x_last], y0, f)[1])
    solution_array.append(solution([xValues[3], x_last], y0, f)[1])
    calculation_table.append([1, xValues[0], yValues[0], fValues[0]])
    calculation_table.append([2, xValues[1], yValues[1], fValues[1]])
    calculation_table.append([3, xValues[2], yValues[2], fValues[2]])
    calculation_table.append([4, xValues[3], yValues[3], fValues[3]])
    x = round(xValues[-1] + h, 5)
    i = 5
    while x <= x_last:
        xValues.append(round(x, 5))

        # Предсказание значения y с помощью формулы Адамса
        y_predicted = yValues[-1] + h * (
                55 * fValues[-1] - 59 * fValues[-2] + 37 * fValues[-3] - 9 * fValues[-4]
        ) / 24

        # Вычисление нового значения y с использованием коррекции
        new_f = f(x, y_predicted)
        y_corrected = yValues[-1] + h * (
                9 * new_f + 19 * fValues[-1] - 5 * fValues[-2] + fValues[-3]
        ) / 24

        # Проверка погрешности с использованием правила Рунге
        if eps is not None and abs(y_corrected - y_predicted) > eps:
            # Уменьшение шага h
            h /= 2
            return adams(x0, y0, h, x_last, f, solution, eps, log)

        yValues.append(y_corrected)
        fValues.append(new_f)
        try:
            calculation_table.append([i, x, y_corrected, new_f])
            solution_array.append(solution([x, x_last], y0, f)[1])
        except IndexError as ex:
            solution_array.append(solution([x, x_last + h], y0, f)[1])
            print(ex)
        x = round(x + h, 5)
        i += 1
    for j in range(len(calculation_table)):
        try:
            calculation_table[j].append(solution_array[len(calculation_table) - j - 1])
        except IndexError as ex:
            print(ex)

    if log:
        field_names = ["i", "x", "y", "F(x,y)", "Точное решение"]
        print(tabulate(calculation_table, field_names, tablefmt='grid', floatfmt='2.4f'))
    return xValues, yValues
