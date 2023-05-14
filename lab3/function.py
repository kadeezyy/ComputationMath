from typing import Optional

from sympy import *
import math
import numpy as np


def choose_function() -> list:
    """
    :return: list of functions
    """

    print(f"Please, enter [y/n] for choose the function")
    func = []

    choice = input("a * cos(b * x): ")
    if choice.replace(" ", "") == "y":
        a, b = map(int, input("a, b: ").split())
        func.append(f"{a}*cos({b} * x)")
        return func

    choice = input("a * log2(b * x): ")
    if choice.replace(" ", "") == "y":
        a, b = map(int, input("a, b: ").split())
        func.append(f"{a}*log({b} * x, 2)")
        return func
    choice = input("a * exp(b * x): ")
    if choice.replace(" ", "") == "y":
        a, b = map(int, input("a, b: ").split())
        func.append(f"{a}*exp({b} * x)")
        return func
    choice = input("a*x^3 + b*x^2 + c*x + d: ")
    if choice.replace(" ", "") == "y":
        a, b, c, d = map(int, input("a, b, c, d: ").split())
        func.append(f"{a} * x**3 + {b} * x**2 + {c} * x + {d}")
        return func
    choice = input("a / (x + b)^c: ")
    if choice.replace(" ", "") == "y":
        a, b, c = input("a, b, c: ").split()
        func.append(f"{a} / (x + {b}) ** {c}")
    return func


class Function:
    functions = []

    def __init__(self):
        self.functions = choose_function()

    def print_function(self) -> str:
        s = ''
        for i, f in enumerate(self.functions):
            if i != len(self.functions) - 1:
                s += f'({f}) +'
            else:
                s += f'({f})'
        return s

    def get_list_of_derivative_n_order(self, n) -> list:
        x = Symbol("x")

        func_derivative_n_order = []
        for f in self.functions:
            func_derivative_n_order.append(diff(f, x, n))

        return func_derivative_n_order

    def get_value(self, point) -> Optional[float]:
        x = Symbol("x")

        values = []
        for f in self.functions:
            f = diff(f, x, 0)
            value = f.subs({x: point})
            values.append(value)

        return sum(values)

    def get_value_in_nth_derivative(self, n, point) -> float:
        x = Symbol("x")

        values = []
        for f in self.functions:
            func_der_n = diff(f, x, n)
            value = func_der_n.subs({x: point})
            values.append(value)

        return sum(values)

    def get_max_value_in_range_nth_derivative(self, n, a, b) -> float:
        res = -math.inf
        x_dots = np.arange(a, b + 0.01, 0.01)
        for x in x_dots:
            res = max(res, self.get_value_in_nth_derivative(n, x))

        return res

    def get_value_integrate(self, left, right) -> float:
        res = 0
        x = symbols('x')
        for f in self.functions:
            f = diff(f, x, 0)
            res += integrate(f, (x, left, right))

        return res
