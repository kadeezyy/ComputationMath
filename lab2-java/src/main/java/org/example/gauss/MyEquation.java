package org.example.gauss;

import org.example.interfaces.Equation;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.List;
import java.util.ListIterator;
import java.util.Random;

public class MyEquation implements Equation<BigDecimal, MyEquation> {
    private final List<BigDecimal> equation = new ArrayList<>();

    /**
     * @return Список коэффициентов уравнения
     */
    public List<BigDecimal> getEquation() {
        return equation;
    }

    /**
     * @param item добавляет коэффициент в список -> добавляет переменную в уравнение
     */
    public void add(BigDecimal item) {
        this.equation.add(item);
    }

    /**
     * Очищает список -> удаляет уравнение из СЛАУ
     */
    public void clear() {
        this.equation.clear();
    }

    /**
     * Генерирует заданное количество переменных со случайными коэффициентами
     *
     * @param size Количество переменных
     */
    public void generate(int size) {
        if (size < 2) size = 2;
        clear();
        for (int i = 0; i < size; i++) {
            Random random = new Random();
            this.equation.add(BigDecimal.valueOf((random.nextInt() % 10) + 1));
        }
    }

    /**
     * @return Количество переменных в уравнении
     */
    @Override
    public int size() {
        return equation.size();
    }

    /**
     * Складывает два уравнения между собой
     *
     * @param item Второе уравнение, с которым нужно сложить текущее
     */
    @Override
    public void addEquation(MyEquation item) {
        ListIterator<BigDecimal> i = equation.listIterator();
        ListIterator<BigDecimal> j = item.getEquation().listIterator();
        while (i.hasNext() && j.hasNext()) {
            BigDecimal a = i.next();
            BigDecimal b = j.next();
            i.set(a.add(b));
        }
    }

    /**
     * Умножает все элементы уравнения на заданное число
     *
     * @param coefficient Коэффициент, на который необходимо умножить уравнение
     */
    @Override
    public void mul(BigDecimal coefficient) {
        for (ListIterator<BigDecimal> i = equation.listIterator(); i.hasNext(); ) {
            BigDecimal next = i.next();
            i.set(next.multiply(coefficient));
        }
    }

    /**
     * Вычисляет коэффициент для метода Гаусса.
     * Коэффициент определяется на основе заданных параметров.
     * Если значение «а» равно 0, метод возвращает значение BigDecimal, равное 1.
     * Это особый случай обработки, когда коэффициент «а» равен нулю, поскольку деление на ноль не определено.
     *
     * @param a значение 'a' в линейном уравнении
     * @param b значение 'b' в линейном уравнении
     * @return вычисленный коэффициент для метода Гаусса
     */
    @Override
    public BigDecimal findCoefficient(BigDecimal a, BigDecimal b) {
        if (a.equals(BigDecimal.valueOf(0))) {
            return BigDecimal.valueOf(1);
        }
        return (b.multiply(BigDecimal.valueOf(-1)).divide(a, RoundingMode.HALF_UP));
    }

    /**
     * Returns the BigDecimal value at the specified index in the equation.
     *
     * @param index the index of the value to retrieve
     * @return the BigDecimal value at the specified index
     */
    @Override
    public BigDecimal at(int index) {
        return equation.get(index);
    }

    /**
     * Устанавливает значение BigDecimal по указанному индексу в уравнении на заданное значение.
     * Если индекс находится в пределах уравнения, значение обновляется.
     *
     * @param index the index at which to set the value
     * @param val   the BigDecimal value to set
     */
    @Override
    public void set(int index, BigDecimal val) {
        if (index < equation.size()) {
            equation.set(index, val);
        }
    }
}
