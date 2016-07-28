/**
 * Created by hadoop on 16-7-4.
 */
public class Tuple implements Comparable<Tuple>{
    public String s;
    public Double d;
    Tuple(String s, Double d){
        this.s = s;
        this.d = d;
    }

    @Override
    public int compareTo(Tuple tuple) {
        if (tuple == null){
            System.out.println("what the fuck??");
            return 1;
        }
        double f = tuple.d;
        if (Math.abs(f - d) < 0.000000000001)
            return 0;
        if (d < f)
            return 1;
        else
            return -1;
    }
}
