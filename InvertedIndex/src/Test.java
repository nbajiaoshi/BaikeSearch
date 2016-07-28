import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by hadoop on 16-6-8.
 */
public class Test {
    public static void main(String[] args){
        System.out.print("helloworld\n");
        String s = "THOMAS PERCY\tEarl of Worcester. (EARL OF WORCESTER:)";
        String ss[] = s.split("\\s");
        for (int i = 0; i < ss.length;i++){
            System.out.println(ss[i]);
        }
        Pattern p = Pattern.compile("\\w+");
        Matcher m = p.matcher(s);
        while (m.find())
            System.out.print(s.substring(m.start(),m.end()) + " ");


    }
}
