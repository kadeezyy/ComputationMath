from tabulate import tabulate


def rungeKutte(x0, y0, h, x_last, f, solution, eps=None, log=False, from_main=False):
    x_values = [x0]
    y_values = [y0]
    calculation_table = []
    lib_solution_table = []
    while x_values[-1] <= x_last:
        x = x_values[-1]
        y = y_values[-1]

        k1 = h * f(x, y)
        k2 = h * f(x + 0.5 * h, y + 0.5 * k1)
        k3 = h * f(x + 0.5 * h, y + 0.5 * k2)
        k4 = h * f(x + h, y + k3)

        y_next = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        x_next = x + h
        if x == x_last:
            x -= 1e-10
        calculation_table.append([len(x_values), x, y, k1, k2, k3, k4, f(x, y)])
        lib_solution_table.append(solution([x, x_last], y0, f)[1])
        x_values.append(x_next)
        y_values.append(y_next)

    if eps is not None:
        # Расчет значения погрешности по правилу Рунге
        y_half_step = rungeKutte(x0, y0, h / 2.0, x_last, f, solution, eps=None, log=False, from_main=from_main)[1][-1]
        R = abs(y_values[-1] - y_half_step) / (2 ** 4 - 1)
        if R > eps or abs(y_values[-1] - lib_solution_table[0]) > eps:
            return rungeKutte(x0, y0, h / 2.0, x_last, f, solution, eps=eps, log=log, from_main=from_main)

        if R <= eps and log:
            print(f"По правилу Рунге точность: {round(y_values[-1], 5)} - {round(y_half_step, 5)} = {round(R, 5)}")
        for j in range(len(calculation_table)):
            calculation_table[j].append(lib_solution_table[len(calculation_table) - j - 1])
    if log:
        field_names = ["i", "x", "y", "k1", "k2", "k3", "k4", "F(x,y)", "Точное значение"]
        print(tabulate(calculation_table, field_names, tablefmt='grid', floatfmt='2.4f'))

    return x_values, y_values


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
        h *= 0.5  # чтобы избежать выхода за рамки промежутка, т. к. вычисляются первые 4 значения
    # Вычисление начальных значений с помощью метода Рунге-Кутты
    x, y = rungeKutte(x0, y0, h, x0 + 3 * h, f, solution, eps=None, log=False)
    yValues.extend(y[1:4])
    xValues.extend(x[1:4])
    fValues = [f(x, y) for x, y in zip(xValues, yValues)]
    solution_array = [solution([x0, x_last], y0, f)[1]]
    for i in range(1, 4):
        solution_array.append(solution([xValues[i], x_last], y0, f)[1])
    for i in range(4):
        calculation_table.append([i + 1, xValues[i], yValues[i], fValues[i], solution_array[i]])

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

        yValues.append(y_corrected)
        fValues.append(new_f)
        if x == x_last:
            x -= 1e-10
        calculation_table.append([i, x, y_corrected, new_f])
        solution_array.append(solution([x, x_last], y0, f)[1])
        x = round(x + h, 5)
        i += 1

    for i in range(4, len(calculation_table)):
        calculation_table[i].append(solution_array[len(calculation_table) - i - 1])
    if eps is not None:
        h_half = h / 2.0
        x2h, Y2h = adams(x0, y0, h_half, x_last, f, solution)
        R = abs((yValues[-1] - Y2h[-1]) / (2 ** 4 - 1))

        if R > eps or abs(yValues[-1] - solution_array[0]) > eps:
            return adams(x0, y0, h_half, x_last, f, solution, eps, log=log, from_main=from_main)
        print(f"По правилу Рунге точность: {round(yValues[-1], 5)} - {round(Y2h[-1], 5)} = {round(R, 5)}")

    if log:
        field_names = ["i", "x", "y", "F(x,y)", "Точное решение"]
        print(tabulate(calculation_table, field_names, tablefmt='grid', floatfmt='2.4f'))
    return xValues, yValues
