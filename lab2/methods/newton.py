import numpy as np


def newton_system(f, df, x0, tol=1e-6, max_iter=1000):
    # if f.shape[0] == 0:
    #     raise ValueError("Матрица не должна быть пустой")
    # if f.shape != f.shape[0]:
    #     raise ValueError("Матрица должна быть квадратной")

    x = x0
    J = df(x)
    b = -f(x)
    dx = np.linalg.solve(J, b)
    x += dx
    iter_count = 1
    while abs(dx[0]) > tol or abs(dx[1]) > tol:
        # x0 = x
        J = df(x)
        b = -f(x)
        dx = np.linalg.solve(J, b)
        x += dx
        iter_count += 1
    print(f"Количество итераций: {iter_count}")
    # print(f(x))
    """
        нужно исправить решение матрицы, до этого был метод гаусса
    """
    # print(x)
    return x, f(x)

    # for i in range(max_iter):
    #     J = df(x)
    #     b = -f(x)
    #     dx = solve(J, b)
    #     x += dx
    #     iter_count += 1
    #     if np.linalg.norm(dx) / np.linalg.norm(x) < tol:
    #           print(f"Количество итераций: {iter_count}")
    #           return x
    # raise Exception("Метод Ньютона не сошелся за максимальное число итераций.")


def solve(matrix, b):
    n = matrix.shape[0]

    # Gaussian elimination with partial pivoting
    for j in range(n):
        # Partial pivoting
        max_row = j
        for i in range(j + 1, n):
            if abs(matrix[i, j]) > abs(matrix[max_row, j]):
                max_row = i
        matrix[[j, max_row]] = matrix[[max_row, j]]
        b[[j, max_row]] = b[[max_row, j]]

        # Elimination
        for i in range(j + 1, n):
            if np.isnan(matrix[i, j] / matrix[j, j]) or np.isinf(matrix[i, j] / matrix[j, j]):
                break
            m = matrix[i, j] / matrix[j, j]
            matrix[i, j + 1:n] -= m * matrix[j, j + 1:n]
            b[i] -= m * b[j]

    # Back substitution
    x = np.zeros(n)
    if np.isnan(matrix[n - 1, n - 1]) or matrix[n - 1, n - 1] == 0:
        return x
    x[n - 1] = b[n - 1] / matrix[n - 1, n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = (b[i] - np.dot(matrix[i, i + 1:n], x[i + 1:n])) / matrix[i, i]

    return x

# 0.009744149992758189
# -0.48828125

# f(x) = 0.007244539031071806
# Ответ: -0.7496665455148286
