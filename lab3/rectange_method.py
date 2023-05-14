import numpy as np

from lab3.function import Function


def main_rect_func(func, a, b, n_segments, eps):
    print("Выберите метод прямоугольников:\n"
          "1: Правило левых прямоугольников\n"
          "2: Правило правых прямоугольников\n"
          "3: Правило средних прямоугольников")
    choice = input()
    while choice != "1" and choice != "2" and choice != "3":
        choice = input()
    if choice == "1":
        ans = left_rectangle_rule(func, a, b, n_segments, eps)
    elif choice == "2":
        ans = right_rectangle_rule(func, a, b, n_segments, eps)
    else:
        ans = midpoint_rectangle_rule(func, a, b, n_segments, eps)
    return ans


def _rectangle_rule(func: Function, a, b, n_segments, frac, eps):
    """Обобщённое правило прямоугольников
    :param frac:  0 <= frac <= 1 задаёт долю смещения точки,
    в которой вычисляется функция,
    от левого края отрезка dx """
    i_h2 = None
    dx = 1.0 * (b - a) / n_segments
    int_sum = 0.0
    xstart = a + frac * dx
    # n_count = 1
    for i in range(n_segments):
        int_sum += func.get_value(xstart + i * dx)
    h2_res = 0
    for i in np.linspace(a, b, n_segments * 2 + 1)[:-1]:
        h2_res += func.get_value(i) * dx / 2
    error = abs(int_sum * dx - h2_res) / 3
    if error < eps:
        return int_sum * dx
    else:
        while error > eps:
            dx /= 2
            n_segments *= 2
            x = np.linspace(a, b, n_segments + 1)
            i_h = 0
            for i in x[:-1]:
                i_h += func.get_value(i) * dx

            dx2 = dx / 2
            n2 = n_segments * 2
            x2 = np.linspace(a, b, n2 + 1)
            i_h2 = 0
            for i in x2[:-1]:
                i_h2 += dx2 * func.get_value(i)

            error = abs(i_h2 - i_h) / 3
        print(n_segments)
        return i_h2
        # return _rectangle_rule(func, a, b, n_segments * 2, frac, eps)


def left_rectangle_rule(func, a, b, n_segments, eps):
    """Правило левых прямоугольников"""
    return _rectangle_rule(func, a, b, n_segments, 0.0, eps)


def right_rectangle_rule(func, a, b, n_segments, eps):
    """Правило правых прямоугольников"""
    return _rectangle_rule(func, a, b, n_segments, 1.0, eps)


def midpoint_rectangle_rule(func, a, b, n_segments, eps):
    """Правило прямоугольников со средней точкой"""
    return _rectangle_rule(func, a, b, n_segments, 0.5, eps)
