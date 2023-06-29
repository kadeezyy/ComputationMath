package org.example.interfaces;

import java.math.BigDecimal;

public interface Equation<N extends BigDecimal, T extends Equation<N, T>> {
    void addEquation(T item);

    void mul(N coefficient);

    N findCoefficient(N a, N b);

    N at(int index);

    int size();

    void set(int index, N value);
}