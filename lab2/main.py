"""
1 - Метод половинного деления
5 - Метод простой итерации
4 - Метод секущих
6 - Метод Ньютона
"""
import math

from service.util import *
from methods.bisection import bisection_method
from methods.newton import newton_system
from methods.secant import secant_method
from methods.iteration_method import iterative_method

system_of_equations = [[lambda x: x ** 2, lambda x: x ** 2],
                       [lambda x: x ** 3, lambda x: (-1) * x]]

free_column = [1.0, 1.0]

"""
    Ввод точности
    Выбор функции
    Валидация концов промежутка
"""


def my_func1(x):
    return np.array(([
        0.1 * x[0] ** 2 + 0.2 * x[1] ** 2 + x[0] - 0.3,
        0.2 * x[0] ** 2 + x[1] + 0.1 * x[0] * x[1] - 0.7
    ]))


def my_func2(x):
    return np.array([
        x[0] ** 2 + x[1] ** 2 - 1,
        x[0] - x[1] ** 3
    ])


def my_func3(x):
    return np.array([
        x[0] - x[1] - 7,
        x[0] * x[1] - 18
    ])
    # return np.array([
    #     math.sin(x[1] + 2) - x[0] - 15,
    #     x[1] + math.cos(x[0] - 2) - 0.5
    # ])


def my_jacobian1(x):
    return np.array([
        [0.2 * x[0] + 1, 0.4 * x[1]],
        [0.4 * x[0] + 0.1 * x[1] + 0.1, 1 + 0.1 * x[0]]
    ])


def my_jacobian2(x):
    return np.array([
        [2 * x[0], 2 * x[1]],
        [1, -3 * x[1] ** 2]
    ])


def my_jacobian3(x):
    return np.array([
        [1, -1],
        [x[1], x[0]]
    ])
    # return np.array([
    #     [-1, math.cos(x[1] + 2)],
    #     [-math.sin(x[0] - 2), 1]
    # ])


def system_eqs(x, y):
    eq1 = x ** 2 + y ** 2 - 1
    eq2 = np.exp(x) + y - x ** 3

    return eq1, eq2


def main():
    print("Выберите какой метод хотите использовать:\n"
          "1 - Метод половинного деления\n"
          "2 - Метод простой итерации\n"
          "3 - Метод секущих\n"
          "4 - Метод Ньютона")
    var = (input())
    if var == "4":
        eq = input("Выберите какую систему хотите решить:\n"
                   "1: 0.1 * x**2 + 0.2 * y**2 + x - 0.3\n"
                   "   0.2 * x**2 + y + 0.1 * x * y - 0.7\n"
                   "2: x**2 + y**2 - 1\n"
                   "   x - y**3\n"
                   "3: x - y - 7\n"
                   "   x * y - 18\n"
                   # "3: sin(y + 2) - x - 15\n"
                   # "   y + cos(x - 2) - 0.5\n"
                   )
        if eq == "1":
            system = my_func1
            jacobian = my_jacobian1
            pass
        elif eq == "2":
            system = my_func2
            jacobian = my_jacobian2
        elif eq == "3":
            system = my_func3
            jacobian = my_jacobian3
        else:
            print("Необходимо выбрать 1, 2 или 3")
            return
        acc = float(input("Введите точность: \n"))
        a, b = map(float, input("Введите правую и левую границы\n").split())
        draw_linear_system(system, a, b)
        x, y = map(float, input("Введите начальное приближение x0 и y0 соответственно:\n").split())
        result, f = newton_system(system, jacobian, [x, y], tol=acc)
        print(f"Ответ: x = {result}\n"
              f"y = {f}"
              )
        return
    # main function to compute
    func_0_name = "1.62*x^3 - 8.15*x^2 + 4.39*x + 4.29"
    func_1_name = "1.8*x^3 - 2.47*x^2 - 5.53*x + 1.539"
    func_2_name = "x^3 - 3.78*x^2 + 1.25*x + 3.49"
    func_3_name = "exp(x^2)"
    print("Выберите какое уравнение вы хотите вычислить:")
    functions_names = [func_0_name, func_1_name, func_2_name, func_3_name]
    for i in range(len(functions_names)):
        print(f"{i + 1}: {functions_names[i]}")
    option = int(input())

    func_0 = lambda x: 1.62 * x ** 3 - 8.15 * x ** 2 + 4.39 * x + 4.29
    func_1 = lambda x: 1.8 * x ** 3 - 2.47 * x ** 2 - 5.53 * x + 1.539
    func_2 = lambda x: x ** 3 - 3.78 * x ** 2 + 1.25 * x + 3.49
    func_3 = lambda x: math.exp(x ** 2)
    if option == 1:
        func = func_0
    elif option == 2:
        func = func_1
    elif option == 3:
        func = func_2
    elif option == 4:
        func = func_3
    else:
        raise ValueError("Необходимо выбрать от 1 до 4")
    draw_function_graph(func, -5, 5, 0.00001)

    print("Введите начало и конец отрезка:")
    s = input()
    a, b = map(float, s.split())

    result = None
    if not check_sign_derivative_on_interval(func, a, b):
        raise ValueError("Функция должна быть монотонной на промежутке")
    if not check_solution_on_interval(func, a, b):
        raise ValueError("Функция должна иметь корень на заданном промежутке")

    acc = float(input("Введите точность: \n"))
    if var == "1":
        result = bisection_method(func, a, b, acc)
    elif var == "2":
        # x0 = int(input("Введите начальное приближение:\n"))
        # if option == "1":
        #     func = lambda x: 1.62 * x ** 3 - 8.15 * x ** 2 + 4.39 * x + 4.29 + x
        # elif option == 2:
        #     func = lambda x: 1.8 * x ** 3 - 2.47 * x ** 2 - 5.53 * x + 1.539 + x
        # elif option == 3:
        #     func = lambda x: x ** 3 - 3.78 * x ** 2 + 1.25 * x + 3.49 + x
        # elif option == 4:
        #     func = lambda x: math.exp(x ** 2) + x
        result = iterative_method(func, a, b, acc)
    elif var == "3":
        result = secant_method(func, a, b, acc)
    print(f"Ответ: {result}")


main()
