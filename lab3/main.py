from draw_func import draw_function_graph
from simpson_method import simpson_method
from rectange_method import main_rect_func
from trapezoid_method import trapezoid_rule
from function import Function

print("Выберите какой метод хотите использовать:\n"
      "1: Метод прямоугольников\n"
      "2: Метод трапеций\n"
      "3: Метод Симпсона")
choice = input().replace(" ", "")
while choice != "1" and choice != "2" and choice != "3":
    choice = input().replace(" ", "")

my_func = Function()

print("Введите интервал")
left_interval, right_interval = map(float, input().split())
draw_function_graph(my_func, left_interval, right_interval)

print("Введите точность")
eps = float(input()) * 1

print("Введите количество сегментов")
n = int(input())

if choice == "1":
    print("Ответ методом прямоугольников: ", main_rect_func(my_func, left_interval, right_interval, n, eps))
elif choice == "2":
    print("Ответ методом трапеций: ", trapezoid_rule(my_func, left_interval, right_interval, n, eps))
elif choice == "3":
    print('Ответ методом Симпсона: ', simpson_method(my_func, left_interval, right_interval, n, eps, percent=True))

print('Точный ответ: ', my_func.get_value_integrate(left_interval, right_interval))

# examples
# sin(x) [0; 1]
# sin(x) [-1; 1]
# sin(x) [-100; 100] n = 100, n = 1000
# 5 * x ** 3 + 2 * x ** 2 - 10 * x + 3 [0; 4]
# log(x) [-1; 1]
# 2.7 ** (1 / x) [-1; 1]
# 2 * x * (abs(x + 3) / (x + 3)) + 6 [-4; -2]
# 2 * x * (abs(x + 3) / (x + 3)) + 6 [-3.2; -2.8] n = 10000, n = 100 + idea
# 2 * x * (abs(x + 3) / (x + 3)) + 6 [-3; -2]
