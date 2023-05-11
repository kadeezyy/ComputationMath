import sympy as sp

from lab2.service.util import count_accuracy


def secant_method(f, x0, x1, eps):
    """
        Данная функция реализует метод секущих для нахождения корня уравнения func(x) = 0 на интервале [a, b] с заданной точностью acc.

        Аргументы функции:

            f: функция, корень которой необходимо найти.
            x0: начальная точка.
            x1: начальная точка.
            eps: заданная точность.

        Функция возвращает найденное значение корня уравнения.
        """
    count = 0
    while abs(f(x1)) > eps:
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        x0 = x1
        x1 = x2
        count += 1
    print(f"Количество итераций: {count}")
    print(f"f(x) = {f(x1)}")
    return x1


# def secant_method(func, a, b, acc):
#     """
#     Данная функция реализует метод секущих для нахождения корня уравнения func(x) = 0 на интервале [a, b] с заданной точностью acc.
#
#     Аргументы функции:
#
#         func: функция, корень которой необходимо найти.
#         a: левая граница интервала.
#         b: правая граница интервала.
#         acc: заданная точность.
#
#     Функция возвращает найденное значение корня уравнения.
#     """
#
#     x_s = sp.Symbol("x")
#     df = sp.diff(func(x_s), x_s)
#     df = df.subs({x_s: x_s})
#     c = (a + b) / 2
#     f_c = func(c)
#     f_a = func(a)
#     if f_c * f_a < 0:
#         x = a
#     else:
#         x = b
#     if f_a * float(df.subs({x_s: a})) > 0:
#         x0 = a
#     elif func(b) * float(df.subs({x_s: b})) > 0:
#         x0 = b
#     else:
#         x0 = c
#     x0 = float(df.subs({x_s: x0})) * func(x0)
#     x = x0 + acc
#     f_x0, f_x1 = func(x0), func(x)
#     count_of_iter = 0
#     while abs(x - x0) >= acc:
#         temp = x
#         x -= f_x1 * (temp - x0) / (f_x1 - f_x0)
#         x0 = temp
#         count_of_iter += 1
#         f_x0, f_x1 = f_x1, func(x)
#     accuracy = count_accuracy(acc)
#     print(f"Количество итераций: {count_of_iter}")
#     print(f"f(x) = {f_x1}")
#     return x
