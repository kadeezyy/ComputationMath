package gauss;

import java.util.ArrayList;
import java.util.List;

public class LinearSystem<N extends Number, T extends Gauss<N, T>> {
    private List<T> list = new ArrayList<T>();

    public T get(int index) {
        return list.get(index);
    }

    public void push(T elem) {
        list.add(elem);
    }

    public int size() {
        return list.size();
    }

    public N itemAt(int i, int j) {
        return list.get(i).at(j);
    }

    public boolean replace(int index, int to) {
        if (to < list.size() && index < list.size()){
            var temp = list.get(to);
            list.set(to, list.get(index));
            list.set(index, temp);
            return true;
        }
        return false;
    }
}