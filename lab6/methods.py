from tabulate import tabulate

def milne(x0, y0, h, x_last, func, solution, eps, log=False):
    while round(x0 + 3 * h, 5) > x_last:
        h *= 0.5
        # raise Exception("Необходимо от 4 значений x")
    xValues, yValues = rungeKutte(x0, y0, h, round(x0 + 3 * h, 5), func, solution, log=log)
    calculation_table = []
    f = []
    for i in range(1, 4):
        f.append(func(xValues[i], yValues[i]))
    x = round(xValues[-1] + h, 5)
    i = 5

    while x <= x_last:
        xValues.append(round(x, 5))

        y_predicted = yValues[-4] + 4 * h * (2 * f[0] - f[1] + 2 * f[2]) / 3
        new_f = func(x, y_predicted)
        y_corrected = yValues[-2] + h * (f[1] + 4 * f[2] + new_f) / 3
        while abs(y_corrected - y_predicted) > eps:
            y_predicted = y_corrected
            new_f = func(x, y_predicted)
            y_corrected = yValues[-2] + h * (f[1] + 4 * f[2] + new_f) / 3
        yValues.append(y_predicted)
        f = f[1:]
        f.append(new_f)

        calculation_table.append([i, x, y_predicted, new_f, solution(x)])
        x = round(x + h, 5)
        i += 1

    if log:
        field_names = ["i", "x", "y", "F(x,y)", "Точное решение"]
        print(tabulate(calculation_table, field_names, tablefmt='grid', floatfmt='2.4f'))
    return xValues, yValues


def rungeKutte(x0, y0, h, x_last, f, solution, eps=None, log=False):
    xValues = [x0]
    yValues = [y0]
    calculation_table = []

    while round(x0 + 3 * h, 5) > x_last:
        h *= 0.5

    while xValues[-1] <= x_last:
        prX = xValues[-1]
        prY = yValues[-1]
        k1 = h * f(prX, prY)
        k2 = h * f(prX + 0.5 * h, prY + 0.5 * k1)
        k3 = h * f(prX + 0.5 * h, prY + 0.5 * k2)
        k4 = h * f(prX + h, prY + k3)
        calculation_table.append([len(xValues), prX, k1, k2, k3, k4, prY, f(prX, prY), solution(prX, y0)])

        error = abs((1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4))  # Вычисление ошибки

        if eps is not None and error > eps:  # Проверка точности и изменение шага h
            h *= 0.5
            continue

        if prX == x_last:
            break
        yValues.append(prY + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4))
        xValues.append(round(prX + h, 5))

    if log:
        field_names = ["i", "x", "k1", "k2", "k3", "k4", "y", "F(x,y)", "Точное решение"]
        print(tabulate(calculation_table, field_names, tablefmt='grid', floatfmt='2.4f'))
    return xValues, yValues



def euler(x0, y0, h, x_last, f, solution, eps=None, log=False):
    xValues = [x0]
    yValues = [y0]
    calculation_table = []

    while round(x0 + 3 * h, 5) > x_last:
        h *= 0.5

    while xValues[-1] <= x_last:
        x = xValues[-1]
        y = yValues[-1]
        calculation_table.append([len(xValues), x, y, f(x, y), solution(x, y0)])

        if x == x_last:
            break

        # Вычисление следующего значения y с использованием метода Эйлера
        y_next = y + h * f(x, y)
        x_next = round(x + h, 5)

        xValues.append(x_next)
        yValues.append(y_next)
    calculation_table.append([len(xValues), x_next, y_next, f(x, y), solution(x, y0)])
    
    field_names = ["i", "x", "y", "F(x,y)", "Точное решение"]
    print(tabulate(calculation_table, field_names, tablefmt='grid', floatfmt='2.4f'))

    # Вычисление погрешности по правилу Рунге
    if eps is not None:
        h_half = h / 2
        x2h, Y2h = euler(x0, y0, h_half, x_last, f, solution)
        R = abs((yValues[-1] - Y2h[-1]) / (2 ** 1 - 1))

        if R > eps:
            # Уменьшаем шаг и повторяем вычисления
            return euler(x0, y0, h_half, x_last, f, solution, eps, log)
        else:
            print(f"По правилу Рунге точность: {round(yValues[-1], 5)} - {round(Y2h[-1], 5)} = {round(R, 5)}")
            print(h_half)
    
    return xValues, yValues


def adams(x0, y0, h, x_last, f, solution, eps=None, log=False):
    xValues = [x0]
    yValues = [y0]
    calculation_table = []
    while round(x0 + 3 * h, 5) > x_last:
        h *= 0.5
    # Вычисление начальных значений с помощью метода Рунге-Кутты
    x, y = rungeKutte(x0, y0, h, x0 + 3 * h, f, solution, eps=None, log=False)
    yValues.extend(y[1:4])
    xValues.extend(x[1:4])  
    fValues = [f(x, y) for x, y in zip(xValues, yValues)]

    x = round(xValues[-1] + h, 5)
    i = 4

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

        calculation_table.append([i, x, y_corrected, new_f, solution(x, y0)])
        x = round(x + h, 5)
        i += 1

    if log:
        field_names = ["i", "x", "y", "F(x,y)", "Точное решение"]
        print(tabulate(calculation_table, field_names, tablefmt='grid', floatfmt='2.4f'))
    return xValues, yValues