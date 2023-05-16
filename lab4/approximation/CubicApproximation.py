from numpy.ma import sqrt
from Function import Function
from approximation.Approximation import Approximation


class CubicApproximation(Approximation):
    function_type = "Кубическая зависимость"

    def find_an_approximation(self, function_table: dict) -> Function:
        SX = sum(function_table.keys())
        SXX = sum(x * x for x in function_table.keys())
        SXXX = sum(x * x * x for x in function_table.keys())
        SXXXX = sum(x * x * x * x for x in function_table.keys())
        SX5 = sum(x ** 5 for x in function_table.keys())
        SX6 = sum(x ** 6 for x in function_table.keys())
        SY = sum(function_table.values())
        SXY = sum(x * y for x, y in function_table.items())
        SXXY = sum(x * x * y for x, y in function_table.items())
        SXXXY = sum(x ** 3 * y for x, y in function_table.items())
        n = len(function_table)

        a, b, c, d = self.solve_matrix44([[n, SX, SXX, SXXX], [SX, SXX, SXXX, SXXXX], [SXX, SXXX, SXXXX, SX5],
                                          [SXXX, SXXXX, SX5, SX6]], [SY, SXY, SXXY, SXXXY])
        if a is None:
            return None

        fun = lambda x: a * x ** 3 + b * x ** 2 + c * x + d
        s = sum((fun(x) - function_table[x]) ** 2 for x in function_table.keys())
        root_mean_square_deviation = sqrt(s / n)
        f = Function(fun, f'ф = {round(a, 3):+}*x^3 {round(b, 3):+}*x^2 {round(c, 3):+}*x {round(d, 3):+}',
                     s, root_mean_square_deviation)
        self.print_approximation_table(function_table, f, self.function_type)
        return f
