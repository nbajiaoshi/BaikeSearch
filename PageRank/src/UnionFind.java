import java.util.HashMap;
import java.util.Set;

/**
 * Created by hadoop on 16-6-15.
 */
public class UnionFind {
    private HashMap<String, String> father;
    public boolean hasKey(String name){
        return father.containsKey(name);
    }
    public String getFather(String name){
        if (father.containsKey(name) && !father.get(name).equals(name))
            father.put(name, getFather(father.get(name)));
        else
            father.put(name, name);
        return father.get(name);
    }
    UnionFind(){
        father = new HashMap<String, String>();
    }
    public void merge(String a, String b){
        this.father.put(a, getFather(b));
    }

    public Set<String> getKeySet(){
        return father.keySet();
    }
}
