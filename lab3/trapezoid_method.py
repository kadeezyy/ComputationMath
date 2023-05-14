from lab3.function import Function
from lab3.rectange_method import midpoint_rectangle_rule


def trapezoid_rule(func: Function, a, b, s_segments=4, eps=1e-6):
    """Правило трапеций
       rtol - желаемая относительная точность вычислений
       s_segments - начальное число отрезков разбиения"""
    nseg = s_segments
    dx = 1.0 * (b - a) / nseg
    ans = 0.5 * (func.get_value(a) + func.get_value(b))
    for i in range(1, nseg):
        ans += func.get_value(a + i * dx)

    ans *= dx
    err_est = max(1.0, abs(ans))
    n_count = 0
    while err_est > abs(eps * ans):
        n_count += 1
        old_ans = ans
        ans = 0.5 * (ans + midpoint_rectangle_rule(func, a, b, nseg, eps))  # новые точки для уточнения интеграла
        # добавляются ровно в середины предыдущих отрезков
        nseg *= 2
        err_est = abs(ans - old_ans)

    print(f"n = {nseg}")
    return ans
