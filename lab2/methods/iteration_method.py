from lab2.service.util import calculate_derivative


def iterative_method(func, a, b, eps):
    derivative_sign = -1 if calculate_derivative(func, a) < 0 else 1
    d_a = abs(calculate_derivative(func, a))
    d_b = abs(calculate_derivative(func, b))
    m = min(d_a, d_b)
    M = max(d_a, d_b)
    iter_count = 0
    lam = 1 / M
    alpha = 1 - lam * d_a
    # phi = lambda x: x + func(x) * lam
    if not 0 <= 1 - (d_b / M) < 1 and not 0 <= alpha < 1:
        raise ValueError("The convergence condition is not met")

    x0 = a
    x1 = a + 2 * eps

    while abs(x1 - x0) > eps or abs(func(x1)) > eps:
        x0 = x1
        if not a <= x1 <= b:
            raise ValueError("No solutions")
        if derivative_sign > 0:
            x1 = x0 - lam * func(x0)
        else:
            x1 = x0 + lam * func(x0)
        iter_count += 1

    if not a <= x1 <= b:
        raise ValueError("No solutions")
    print(f"Количество итераций: {iter_count}")
    print(f"f(x) = {func(x1)}")
    return x1
