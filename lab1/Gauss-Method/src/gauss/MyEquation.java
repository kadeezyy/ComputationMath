package gauss;

import java.util.ArrayList;
import java.util.List;
import java.util.ListIterator;
import java.util.Random;

public class MyEquation implements Gauss<Double, MyEquation> {
    private List<Double> equation = new ArrayList<>();

    public List<Double> getEquation() {
        return equation;
    }

    public void add(double item) {
        this.equation.add(item);
    }
    public void clear(){
        this.equation.clear();
    }

    public void generate(int size) {
        if (size < 2) size = 2;
        this.equation.clear();
        for (int i = 0; i < size; i++) {
            Random random = new Random();
            this.equation.add((double) (random.nextInt() % 10) + 1);
        }
    }

    @Override
    public int size() {
        return equation.size();
    }

    @Override
    public void addEquation(MyEquation item) {
        ListIterator<Double> i = equation.listIterator();
        ListIterator<Double> j = item.getEquation().listIterator();
        while (i.hasNext() && j.hasNext()) {
            Double a = i.next();
            Double b = j.next();
            i.set(a + b);
        }
    }

    @Override
    public void mul(Double coefficient) {
        for (ListIterator<Double> i = equation.listIterator(); i.hasNext(); ) {
            Double next = i.next();
            i.set(next * coefficient);
        }
    }

    @Override
    public Double findCoefficient(Double a, Double b) {
        if (a == 0.0) {
            return 1.0;
        }
        return -b / a;
    }

    @Override
    public Double at(int index) {
        return equation.get(index);
    }
}