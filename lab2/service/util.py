import numpy as np
import matplotlib.pyplot as plt


def check_monotonicity(func, a, b):
    """
    Проверяет, является ли функция f(x) монотонной на заданном промежутке [a, b].

    Аргументы:
    func -- функция, которую нужно проверить на монотонность.
    a, b -- границы промежутка.

    Возвращает:
    True, если функция монотонна на промежутке, False в противном случае.
    """
    # Проверяем монотонность на участке [a, b]
    df = func(b) - func(a)
    if df > 0:
        is_monotonic = all(func(x) <= func(x + 1e-6) for x in np.arange(a, b, 0.01))
    elif df < 0:
        is_monotonic = all(func(x) >= func(x + 1e-6) for x in np.arange(a, b, 0.01))
    else:
        is_monotonic = True

    return is_monotonic


def check_solution_on_interval(func, interval_left, interval_right):
    if func(interval_left) * func(interval_right) >= 0:
        return False
    return True


def draw_function_graph(func, a, b, step):
    a = float(a)
    b = float(b)
    step = float(step)

    if a > b:
        raise IOError('input the correct intervals')

    dots_x = np.arange(a, b + step, step)
    dots_y = []
    for x in dots_x:
        try:
            if str(func.__class__) == "<class 'code'>":
                dots_y.append(eval(func))
            elif str(func.__class__) == "<class 'function'>":
                dots_y.append(func(x))
            else:
                raise IOError('Failed to recognize the function')
        except:
            dots_y.append(None)

    if dots_y.count(None) == len(dots_y):
        raise ArithmeticError(f'Can not draw function on the interval: [{a}; {b}]')

    plt.plot(dots_x, dots_y, 'r')
    plt.plot(dots_x, [0 for _ in range(len(dots_x))], 'g')
    plt.show()


def count_accuracy(a) -> int:
    count = 0
    a = abs(a)
    while a < 1:
        count += 1
        a = a * 10
    return count


def calculate_derivative(func, x):
    dx = 1e-7
    return (func(x + dx) - func(x)) / dx


def check_sign_derivative_on_interval(func, a, b):
    dots_x = np.arange(a, b + 0.1, 0.1)
    sign = -1 if calculate_derivative(func, a) < 0 else 1
    for x in dots_x:
        next_sign = -1 if calculate_derivative(func, x) < 0 else 1
        if sign != next_sign:
            return False

    return True


def draw_linear_system(system_eqs, a: float, b: float):
    # Определите диапазон значений x и y
    x_range = np.linspace(a, b, 100)
    y_range = np.linspace(a, b, 100)

    # Создайте сетку значений x и y
    X, Y = np.meshgrid(x_range, y_range)

    # Вычислите значения системы уравнений на сетке
    Z1, Z2 = system_eqs([X, Y])[0], system_eqs([X, Y])[1]

    # Постройте график контуров системы уравнений
    plt.contour(X, Y, Z1, levels=[0])
    plt.contour(X, Y, Z2, levels=[0])

    # Добавьте заголовок и подписи осей
    plt.title('System of Nonlinear Equations')
    plt.xlabel('x')
    plt.ylabel('y')

    # Показать график
    plt.show()
