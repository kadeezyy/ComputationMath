import numpy as np
from numpy import linalg as LA


def calculate_derivative(func, x):
    dx = 1e-7
    return (func(x + dx) - func(x)) / dx


def calculate_determinant(matrix: list[list]) -> int:
    return LA.det(matrix)


def simple_iteration_method(matrix: list[list], free_column: list, x0, acc):
    if len(matrix) == 0:
        print("Матрица не должна быть пустой")
        return
    if len(matrix) != len(matrix[0]):
        print("Матрица должна быть квадратной")
        return

    max_error = acc + 1
    x1 = []
    count_of_iter = 1
    while max_error > acc:
        f_x0 = []
        for i in range(len(matrix)):
            funcs_x0 = [func(x0[j]) for j, func in enumerate(matrix[i])]
            funcs_x0.append((-1) * free_column[i])
            f_x0.append(sum(funcs_x0))

        f_der_x0 = []
        for i in range(len(matrix)):
            f_der_x0.append([calculate_derivative(func, x0[j]) for j, func in enumerate(matrix[i])])

        det_f_der_x0 = calculate_determinant(f_der_x0)

        if det_f_der_x0 == 0:
            print("Производная равна 0")
            return

        inverse_matrix_f_der_x0 = list(LA.inv(f_der_x0))
        for i in range(len(f_der_x0)):
            inverse_matrix_f_der_x0[i] = list(inverse_matrix_f_der_x0[i])

        inverse_multiple_func = np.matmul(inverse_matrix_f_der_x0, f_x0)

        x1 = [x0[i] - inverse_multiple_func[i] for i in range(len(x0))]
        max_error = max([abs(x1[i] - x0[i]) for i in range(len(x0))])
        x0 = x1[:]

        count_of_iter += 1

    return x1
