package gauss;

import java.util.ArrayList;

public class Algorithm<N extends Number, T extends Gauss<N, T>> {
    LinearSystem<N, T> list;
    int countZero = 0;
    public Algorithm(LinearSystem<N, T> system) {
        list = system;
    }

    public void calculate() throws NullPointerException, ArithmeticException {
        if (list == null) {
            throw new NullPointerException("LinearSystem instance is null");
        }
        if (!checkSystem(list)) {
            throw new ArithmeticException("Incorrect system for Gauss Method");
        }
        if (countZero == list.size()) {
            throw new ArithmeticException("Incorrect system for Gauss Method");
        }

        for (int i = 0; i < list.size() - 1; i++) {
            for (int j = i + 1; j < list.size(); j++) {
                var k = list.get(j).findCoefficient(list.get(j).at(i), list.get(i).at(i));
                list.get(j).mul(k);
                if (Double.parseDouble(String.valueOf(k)) == 1.0) continue;
                list.get(j).addEquation(list.get(i));
            }
        }
    }

    public int getCountZero() {
        return countZero;
    }

    public ArrayList<N> getResidualVector(N[] x) {
        ArrayList<N> results = new ArrayList<>();
        for (int i = 0; i < list.size(); i++) {
            Double r = Double.parseDouble(String.valueOf(list.get(i).at(list.size())));
            for (int j = 0; j < list.get(i).size() - 1; j++) {
                Double a = Double.parseDouble(String.valueOf(list.get(i).at(j)));
                Double b = Double.parseDouble(String.valueOf(x[j]));
                r -= (a * b);
            }
            results.add((N) r);
        }
        return results;
    }

    private boolean checkSystem(LinearSystem<N, T> system) {
        if (system.size() < 2) return false;
        boolean check = true;
        for (int i = 0; i < system.size(); i++) {
            if (system.get(i).size() != (system.size() + 1)) {
                return false;
            }
            if (Double.parseDouble(String.valueOf(system.get(i).at(i))) == 0) {
                countZero++;
                if (i < system.size() - 1) {
                    check = system.replace(i, i + 1);
                    i--;
                } else {
                    check = system.replace(i, i - 1);
                }
                if (!check) return false;
                if (countZero == system.size()) return false;
            }
        }
        return true;
    }
}