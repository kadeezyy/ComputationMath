package org.example;

import org.example.gauss.Algorithm;
import org.example.gauss.LinearSystem;
import org.example.gauss.MyEquation;

import java.math.BigDecimal;
import java.util.ArrayList;

import static org.example.util.BoilerTemplate.*;

public class Main {
    public static void main(String[] args) {
        String filename = readFilename();
        LinearSystem<BigDecimal, MyEquation> linearSystem = readSystemFromFile(filename);
        int maxIterations = 200; // Максимальное количество итераций
        double epsilon = 0.01; // Критерий сходимости

        ArrayList<BigDecimal> initialGuess;
        System.out.println("Система уравнений перед преобразованиями:");
        printSystem(linearSystem);

        if (Algorithm.checkDiagonal(linearSystem)) { //Проверка главной диагонали
            initialGuess = createNullInitialGuess(linearSystem);
            Algorithm.solveGaussSeidel(linearSystem, initialGuess, maxIterations, epsilon);
            System.out.println("Система уравнений после преобразований:");
            printSystem(linearSystem);
            System.out.println("Решения:");
            printVector(initialGuess);
        } else {
            System.out.println("Невозможно решить итерационным методом");
        }
    }
}