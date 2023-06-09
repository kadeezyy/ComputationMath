from Function import Function
import numpy as np
import logging
from prettytable import PrettyTable


class Approximation:
    function_type = None

    @staticmethod
    def solve_matrix22(a, b):
        delta = a[0][0] * a[1][1] - a[0][1] * a[1][0]
        delta1 = a[0][0] * b[1] - b[0] * a[1][0]
        delta2 = b[0] * a[1][1] - a[0][1] * b[1]
        return (delta1 / delta, delta2 / delta) if delta != 0 else (None, None)

    @staticmethod
    def solve_matrix33(a, b):
        delta = (a[0][0] * a[1][1] * a[2][2] + a[1][0] * a[2][1] * a[0][2] + a[0][1] * a[1][2] * a[2][0]
                 - a[0][2] * a[1][1] * a[2][0] - a[0][1] * a[1][0] * a[2][2] - a[0][0] * a[1][2] * a[2][1])
        delta2 = (a[0][0] * b[1] * a[2][2] + a[1][0] * b[2] * a[0][2] + b[0] * a[1][2] * a[2][0]
                  - a[0][2] * b[1] * a[2][0] - b[0] * a[1][0] * a[2][2] - a[0][0] * a[1][2] * b[2])
        delta1 = (a[0][0] * a[1][1] * b[2] + a[1][0] * a[2][1] * b[0] + a[0][1] * b[1] * a[2][0]
                  - b[0] * a[1][1] * a[2][0] - a[0][1] * a[1][0] * b[2] - a[0][0] * b[1] * a[2][1])
        delta3 = (b[0] * a[1][1] * a[2][2] + b[1] * a[2][1] * a[0][2] + a[0][1] * a[1][2] * b[2]
                  - a[0][2] * a[1][1] * b[2] - a[0][1] * b[1] * a[2][2] - b[0] * a[1][2] * a[2][1])
        return (delta1 / delta, delta2 / delta, delta3 / delta) if delta != 0 else (None, None, None)

    @staticmethod
    def solve_matrix44(a, b):
        a, b, c, d = np.linalg.solve(a, b)
        return (a, b, c, d)

    @staticmethod
    def print_approximation_table(function_table: dict,
                                  f: Function, function_type: str, decimals=3):
        x = np.around(list(function_table.keys()), decimals)
        y = np.around(list(function_table.values()), decimals)
        approximated_y = np.around(list(round(f.function(x), decimals) for x in function_table.keys()), decimals)

        logging.info(function_type)
        approximation_table = PrettyTable()
        approximation_table.field_names = ["", *(i for i in range(1, len(y) + 1))]
        approximation_table.add_row(["x", *x])
        approximation_table.add_row(["y", *y])
        approximation_table.add_row([f.text, *approximated_y])
        approximation_table.add_row(["E", *(round(approximated_y[i] - y[i], decimals) for i in range(len(y)))])
        logging.info(approximation_table)
