import gauss.Algorithm;
import gauss.MyEquation;
import gauss.LinearSystem;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    private static int DEFAULT_EQUATIONS_NUMBER = 5;
    private static int DEFAULT_VARIABLES_NUMBER = 5;

    public static void main(String args[]) {
//        LinearSystem<Double, MyEquation> list = generateSystem();
        System.out.println("Введите название файла, с которого нужно считать СЛАУ");
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine().trim();
        LinearSystem<Double, MyEquation> list = readSystemFromFile(line);

        System.out.println("Matrix before transformation: ");
        printSystem(list);

        int i, j;
        Algorithm<Double, MyEquation> alg = new Algorithm<>(list);

        try {
            alg.calculate();
        } catch (NullPointerException | ArithmeticException e) {
            System.out.println(e.getMessage());
            System.exit(0);
        }

        Double[] x = new Double[DEFAULT_EQUATIONS_NUMBER];
        for (i = list.size() - 1; i >= 0; i--) {
            Double sum = 0.0;
            for (j = list.size() - 1; j > i; j--) {
                sum += list.itemAt(i, j) * x[j];
            }
            x[i] = (list.itemAt(i, list.size()) - sum) / list.itemAt(i, j);
        }
        System.out.println("Matrix in triangular form after transformation: ");
        printSystem(list);
        System.out.printf("Determinant: %.2f \n\n", getDeterminant(list) * Math.pow(-1, alg.getCountZero()));
        System.out.println("Solutions:");
        printVector(x);
        System.out.println("Вектор невязок:");
        printArray(alg.getResidualVector(x));
    }

    public static void printArray(ArrayList<? extends Number> x) {
        StringBuilder s = new StringBuilder();
        x.forEach(number -> s.append(String.format("%.2f; ", number)));
        System.out.println(s);
    }

    public static Double getDeterminant(LinearSystem<Double, MyEquation> matrix) {
        double r = 1;
        for (int i = 0; i < matrix.size(); i++) {
            r *= matrix.get(i).at(i);
        }
        return r;
    }

    public static LinearSystem<Double, MyEquation> generateSystem() {
        LinearSystem<Double, MyEquation> list = new LinearSystem<>();
        for (int i = 0; i < DEFAULT_EQUATIONS_NUMBER; i++) {
            MyEquation eq = new MyEquation();
            eq.generate(DEFAULT_VARIABLES_NUMBER + 1);
            list.push(eq);
        }
        return list;
    }

    public static void printSystem(LinearSystem<Double, MyEquation> system) {
        for (int i = 0; i < system.size(); i++) {
            MyEquation temp = system.get(i);
            StringBuilder s = new StringBuilder();
            for (int j = 0; j < temp.size(); j++) {
                if (j == temp.size() - 1) {
                    s.append("|");
                }
                s.append(String.format(" %.2f; %s", system.itemAt(i, j), " "));
            }
            System.out.println(s);
        }
        System.out.println();
    }

    public static void printVector(Double[] x) {
        StringBuilder s = new StringBuilder();
        for (int i = 0; i < x.length; i++) {
            s.append(String.format("x%d = %.2f; ", i, x[i]));
        }
        System.out.println(s);
    }

    public static LinearSystem<Double, MyEquation> readSystemFromFile(String filename) {
        File file = new File("src/tests/" + filename);
        LinearSystem<Double, MyEquation> list = new LinearSystem<>();
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
                            eq.add(Double.parseDouble(el));
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
            System.exit(0);
        }
        return list;
    }

    public static void setDefault(int n) {
        DEFAULT_EQUATIONS_NUMBER = n;
        DEFAULT_VARIABLES_NUMBER = n + 1;
    }
}