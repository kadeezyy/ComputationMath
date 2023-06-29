package org.example.gauss;

import org.example.interfaces.Equation;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Represents a linear system of equations.
 * <p>
 * The LinearSystem class manages a list of equations of type T.
 *
 * @param <N> the type of the coefficients in the equations, extending BigDecimal
 * @param <T> the type of the equations, extending Gauss<N, T>
 */
public class LinearSystem<N extends BigDecimal, T extends Equation<N, T>> {
    private List<T> list = new ArrayList<T>();

    /**
     * Получает уравнение по указанному индексу.
     *
     * @param index индекс уравнения для получения
     * @return уравнение по указанному индексу
     */
    public T get(int index) {
        return list.get(index);
    }

    public List<T> getAll() {
        return list;
    }

    /**
     * Добавляет уравнение в линейную систему.
     *
     * @param val уравнение для добавления
     */
    public void push(T val) {
        list.add(val);
    }

    /**
     * Возвращает количество уравнений в линейной системе.
     *
     * @return размер линейной системы
     */
    public int size() {
        return list.size();
    }


    /**
     * Swaps the positions of two rows in the linear system.
     *
     * @param first  the index of the first row
     * @param second the index of the second row
     * @return {@code true} if the swap is successful, {@code false} otherwise
     */
    public boolean swapRows(int first, int second) {
        if (first < 0 || first >= list.size() || second < 0 || second >= list.size())
            return false;

        var temp = list.get(first);
        list.set(first, list.get(second));
        list.set(second, temp);
        return true;
    }

    /**
     * Получает коэффициент по указанным строке (i) и столбцу (j) в линейной системе.
     *
     * @param i строка индекс
     * @param j столбец индекс
     * @return коэффициент указанной позиции
     */
    public N itemAt(int i, int j) {
        return list.get(i).at(j);
    }

    /**
     * Заменяет уравнение по указанному индексу на уравнение с целевым индексом.
     *
     * @param index индекс уравнения для замены
     * @param to    целевой индекс уравнения
     * @return true, если замена успешна, false в противном случае
     */
    public boolean replace(int index, int to) {
        if (to < list.size() && index < list.size()) {
            var temp = list.get(to);
            list.set(to, list.get(index));
            list.set(index, temp);
            return true;
        }
        return false;
    }
}
