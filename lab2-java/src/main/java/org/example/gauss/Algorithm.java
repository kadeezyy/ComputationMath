package org.example.gauss;

import org.example.interfaces.Equation;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;


public class Algorithm<N extends BigDecimal, T extends Equation<N, T>> {
    /**
     * Решает систему линейных уравнений методом Гаусса-Зейделя.
     *
     * @param linearSystem  система линейных уравнений
     * @param x             список начальных приближений
     * @param maxIterations максимальное количество итераций
     * @param epsilon       допустимая погрешность
     */
    public static void solveGaussSeidel(LinearSystem<BigDecimal, MyEquation> linearSystem,
                                        ArrayList<BigDecimal> x,
                                        int maxIterations,
                                        double epsilon) {
        int n = linearSystem.size();

        for (int iteration = 0; iteration < maxIterations; iteration++) {
            double maxDiff = 0.0;

            for (int i = 0; i < n; i++) {
                BigDecimal sum = BigDecimal.ZERO;

                MyEquation equation = linearSystem.get(i);
                int equationSize = equation.size();

                for (int j = 0; j < equationSize - 1; j++) {
                    if (j != i) {
                        sum = sum.add(equation.at(j).multiply(x.get(j))); //s += a_ij * x_j
                    }
                }

                BigDecimal newX = (equation.at(equationSize - 1).subtract(sum)).divide(equation.at(i),
                        RoundingMode.HALF_UP); //(b_i - sum) / a_ii
                BigDecimal diff = newX.subtract(x.get(i)).abs(); //|x - x_i|
                x.set(i, newX);

                //Проверка монотонности убывания
                if (diff.compareTo(BigDecimal.valueOf(maxDiff)) > 0) {
                    maxDiff = diff.doubleValue();
                }
            }
            //Проверка конечного условия
            if (maxDiff < epsilon) {
                System.out.println("Сошлось спустя " + (iteration + 1) + " итераций");
                return;
            }
        }

        System.out.println("Метод расходится. Прошло " + maxIterations + " итераций ");
        System.exit(1);
    }

    public static boolean checkDiagonal(LinearSystem<BigDecimal, MyEquation> linearSystem) {
        int size = linearSystem.size();

        // Проверяем наличие нулей на главной диагонали
        for (int i = 0; i < size; i++) {
            MyEquation equation = linearSystem.get(i);
            if (equation.at(i).compareTo(BigDecimal.ZERO) == 0) {
                // Найден ноль на главной диагонали

                // Ищем строку для перестановки, где нет нулей на главной диагонали
                int swapIndex = -1;
                for (int j = i + 1; j < size; j++) {
                    MyEquation nextEquation = linearSystem.get(j);
                    if (nextEquation.at(i).compareTo(BigDecimal.ZERO) != 0) {
                        swapIndex = j;
                        break;
                    }
                }

                if (swapIndex != -1) {
                    // Меняем местами текущую строку с строкой, где нет нулей на главной диагонали
                    return linearSystem.swapRows(i, swapIndex); // Произведена перестановка
                }
                return false; // Невозможно выполнить перестановку, нули на главной диагонали продолжаются
            }
        }

        return true; // Нулей на главной диагонали нет
    }
}
