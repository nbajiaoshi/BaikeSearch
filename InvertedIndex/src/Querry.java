
import java.io.*;
import java.util.HashMap;
import java.util.Vector;

/**
 * Created by hadoop on 16-6-11.
 */
public class Querry {
    static private HashMap<String,Vector<String>> invertedTable = new HashMap<String, Vector<String>>();
    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream("output1/part-r-00000")));
        while (true) {
            String line = in.readLine();
            if (line == null || line.isEmpty())
                break;
            String ss[] = line.split("\\s+");
            invertedTable.put(ss[0],new Vector<String>());
            for (int i = 1; i < ss.length; i++)
                invertedTable.get(ss[0]).add(ss[i]);
        }
        in  = new BufferedReader(new InputStreamReader(System.in));
        while (true){
            System.out.println("input the words:");
            String line = in.readLine();
            String ss[] = line.split("\\s+");
            HashMap<String, Integer> dict= new HashMap<String, Integer>();
            for (String s:invertedTable.get(ss[0]))
                dict.put(s,1);
            for (int i = 1; i < ss.length; i++)
                for (String s:invertedTable.get(ss[i]))
                    if (dict.containsKey(s))
                        dict.put(s, dict.get(s) + 1);
            for (String s:dict.keySet())
                if (dict.get(s).equals(ss.length))
                    System.out.print(s + ",");
            System.out.println();

        }

    }
}
