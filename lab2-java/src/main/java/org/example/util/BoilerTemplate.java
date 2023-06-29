package org.example.util;

import org.example.gauss.LinearSystem;
import org.example.gauss.MyEquation;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class BoilerTemplate {

    public static int DEFAULT_EQUATIONS_NUMBER = 5;
    private static int DEFAULT_VARIABLES_NUMBER = 5;

    /**
     * @return Filename from stdin
     */
    public static String readFilename() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Введите название файла в каталоге \"testcases\":");
        return sc.nextLine().trim();
    }

    /**
     * Считывает систему линейных уравнений из файла
     * Формат данных в файле должен быть следующий:
     * Размерность матрицы NxN
     * N строк с N + 1 столбцами, последний столбец - свободный член
     *
     * @param filename Имя файла в папке testcases на уроввне иерархии вместе с src/
     * @return Linear system from a specific file
     */
    public static LinearSystem<BigDecimal, MyEquation> readSystemFromFile(String filename) {
        System.out.println(System.getProperty("user.dir"));
        File file = new File("src/testcases/" + filename);
        LinearSystem<BigDecimal, MyEquation> list = new LinearSystem<>();
        try {
            BufferedReader reader = new BufferedReader(new FileReader(file.getPath()));
            int n = Integer.parseInt(reader.readLine());
            setDefault(n);
            for (int i = 0; i < n; i++) {
                MyEquation eq = new MyEquation();
                String line = reader.readLine();
                if (line != null) {
                    String[] array = line.trim().split(" ");
                    if (array.length != n + 1) {
                        throw new ArithmeticException(String.format("Size of input array %d is not equal to N", i));
                    }
                    Arrays.stream(array).forEach(el -> {
                        if (el != null) {
                            eq.add(BigDecimal.valueOf(Double.parseDouble(el)));
                        } else {
                            throw new NullPointerException("Element in a row is null");
                        }
                    });
                }
                list.push(eq);
            }
        } catch (IOException | NumberFormatException | ArithmeticException | NullPointerException e) {
            System.out.println("An exception occurred during reading matrix  from file");
            System.out.println(e.getMessage());
            System.exit(1);
        }
        return list;
    }

    /**
     * Создает список начальных приближений для метода Гаусса-Зейделя на основе системы линейных уравнений.
     *
     * @param linearSystem система линейных уравнений
     * @return список начальных приближений
     */
    public static ArrayList<BigDecimal> createInitialGuess(LinearSystem<BigDecimal, MyEquation> linearSystem) {
        var copySystem = linearSystem;
        int n = copySystem.size();
        ArrayList<BigDecimal> initialGuess = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            MyEquation equation = copySystem.get(i);
            int equationSize = equation.size();
            for (int j = 0; j < equationSize; j++) {
                if (j != i) {
                    equation.set(j, equation.at(j).negate().divide(equation.at(i), RoundingMode.HALF_UP));
                }
            }
            initialGuess.add(equation.at(equationSize - 1));
        }
        return initialGuess;
    }

    /**
     * Создает список начальных приближений с нулевыми значениями для метода Гаусса-Зейделя
     * на основе системы линейных уравнений.
     *
     * @param linearSystem система линейных уравнений
     * @return список начальных приближений с нулевыми значениями
     */
    public static ArrayList<BigDecimal> createNullInitialGuess(LinearSystem<BigDecimal, MyEquation> linearSystem) {
        ArrayList<BigDecimal> initialGuess = new ArrayList<>();
        for (int i = 0; i < linearSystem.size(); i++) {
            initialGuess.add(BigDecimal.ZERO);
        }
        return initialGuess;
    }

    /**
     * Генерирует СЛАУ
     *
     * @return Genereted Linear System of equations
     */
    public static LinearSystem<BigDecimal, MyEquation> generateSystem() {
        LinearSystem<BigDecimal, MyEquation> list = new LinearSystem<>();
        for (int i = 0; i < DEFAULT_EQUATIONS_NUMBER; i++) {
            MyEquation eq = new MyEquation();
            eq.generate(DEFAULT_VARIABLES_NUMBER + 1);
            list.push(eq);
        }
        return list;
    }

    /**
     * Выводит СЛАУ в стандартный поток вывода
     *
     * @param system a system to be printed
     */
    public static void printSystem(LinearSystem<BigDecimal, MyEquation> system) {
        for (int i = 0; i < system.size(); i++) {
            MyEquation temp = system.get(i);
            StringBuilder s = new StringBuilder();
            for (int j = 0; j < temp.size(); j++) {
                if (j == temp.size() - 1) {
                    s.append("|");
                }
                s.append(String.format(" %8.2f; %s", system.itemAt(i, j), " "));
            }
            System.out.println(s);
        }
        System.out.println();
    }

    /**
     * Выводит массив чисел в стандартный поток вывода
     *
     * @param x Массив элементов типа BigDecimal
     */
    public static void printVector(ArrayList<BigDecimal> x) {
        if (x == null) return;

        StringBuilder s = new StringBuilder();
        //Обычный десятичный вывод
//        for (int i = 0; i < x.size(); i++) {
//            s.append(String.format("x%d = %.2f; ", i, x.get(i)));
//        }
        //Экспоненцальный вывод
        for (int i = 0; i < x.size(); i++) {
            s.append(String.format("x%d = %.6E%n", (i + 1), x.get(i)));
        }
        System.out.println(s);
    }

    /**
     * Выводит лист чисел в стандартный поток вывода
     *
     * @param x Список чисел типа, наследующего BigDecimal
     */
    public static void printArray(ArrayList<? extends BigDecimal> x) {
        StringBuilder s = new StringBuilder();
        x.forEach(number -> s.append(String.format("%.2f; ", number)));
        System.out.println(s);
    }

    /**
     * Вычисляет определитель матрицы СЛАУ.
     * Предполагается, что матрица валидна
     *
     * @param matrix a linear system whose determinant to be computed
     * @return determinant
     */
    public static BigDecimal getDeterminant(LinearSystem<BigDecimal, MyEquation> matrix) {
        BigDecimal r = BigDecimal.valueOf(1);
        for (int i = 0; i < matrix.size(); i++) {
            r = r.multiply(matrix.get(i).at(i));
        }
        return r;
    }

    /**
     * Изменяет количество линейно независимых уравнений
     *
     * @param n number to be set
     */
    public static void setDefault(int n) {
        DEFAULT_EQUATIONS_NUMBER = n;
        DEFAULT_VARIABLES_NUMBER = n + 1;
    }
}
