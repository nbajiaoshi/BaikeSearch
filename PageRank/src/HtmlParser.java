import org.apache.hadoop.io.Text;
import org.apache.hadoop.util.hash.Hash;

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by hadoop on 16-6-15.
 */
public class HtmlParser {
    static private HashMap<String,Vector<String>> invertedTable = new HashMap<String, Vector<String>>();
    private UnionFind fatherList;
    private HashMap<String, HashSet<String>> URLLink;

    private static String parseWord(BufferedReader in, String pattern) throws Exception {
        Pattern p = Pattern.compile(pattern);
        while (true) {
            String line = in.readLine();
            if (line == null)
                return "";
            Matcher m = p.matcher(line);
            if (m.find())
                return line;
        }
    }

    private static String parseTitle(BufferedReader in) throws Exception {
        Matcher m = Pattern.compile("<title>([\\w\\s]+)</title>").matcher(parseWord(in, "<title>(\\w+)</title>"));
        if (m.find() && m.groupCount() > 0)
            return m.group(1);
        else
            return "";
    }

    private static String parseText(BufferedReader in) throws Exception {
        String line = parseWord(in, "<text[^>]+>");
        StringBuilder s = new StringBuilder();
        StringBuilder sr = new StringBuilder();
        Matcher m;
        for (;line != null;line = in.readLine()){
            m = Pattern.compile("\\[\\[([\\w\\s]+)]]").matcher(line);
            while (m.find())
                if (m.start() > 10 && line.substring(m.start() - 10,m.start()).equals("#REDIRECT "))
                    sr.append("," + m.group(1));
                else
                    s.append(m.group(1) + ",");
            if (Pattern.compile("</text>").matcher(line).find())
                return sr.toString()+ ":" + s.toString();
        }
        System.out.println(parseWord(in, "</text>"));
        return "";
    }

    private static String parsePage(BufferedReader in) throws Exception {
        parseWord(in, "<page>");
        String title = parseTitle(in);
        String links = parseText(in);
        if (parseWord(in, "</page>") == "")
            return null;
        else
            return title + links;
    }

    protected void initialFatherList() throws IOException {
        fatherList = new UnionFind();
        BufferedReader in = new BufferedReader(new InputStreamReader(
                new FileInputStream("wikiLink.txt")));
        while (true) {
            String line = in.readLine();
            if (line == null)
                break;
            String[] redirectList = line.split(":")[0].split(",");

            for(int i = 0; i < redirectList.length; i++){
                fatherList.merge(redirectList[i],redirectList[0]);
            }
        }
        in.close();
    }

    protected void initialURLLink() throws IOException {
        URLLink = new HashMap<>();
        BufferedReader in = new BufferedReader(new InputStreamReader(
                new FileInputStream("wikiLink.txt")));
        while (true) {
            String line = in.readLine();
            if (line == null)
                break;
            String [] ss = line.split(":");
            String name = fatherList.getFather(ss[0].split(",")[0]);
            String[] linkLists;
            if (!URLLink.containsKey(name))
                URLLink.put(name, new HashSet<String>());
            if (ss.length > 1)
                linkLists = ss[1].split(",");
            else
                continue;
            for (String s:linkLists)
                if (fatherList.hasKey(s))
                    URLLink.get(name).add(fatherList.getFather(s));
        }
    }

    private void initialCurrentPageRank() throws Exception {
        BufferedWriter out = new BufferedWriter(new FileWriter("part-r-00000"));
        initialFatherList();
        initialURLLink();
        System.out.println(fatherList.getFather("Interlego"));
        System.out.println(URLLink.containsKey("Interlego") + "\n"+ URLLink.keySet().size());
        for (String name:URLLink.keySet()){
            if (name.equals("Interlego"))
                System.out.println("God !!!!\n" + name + "\t" + "1|" + URLLink.get(name).toString());
            out.write(name + "\t" + "1|");
            HashSet<String> linkList = URLLink.get(name);
            for (String link:linkList)
                out.write(link + ',');
            out.write("\n");
        }
        out.close();
    }

    private static void parseWikiLink() throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(
                new FileInputStream("/mnt/newdisk/enwiki-latest-pages-articles.xml")));
        BufferedReader iin  = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter out = new BufferedWriter(new FileWriter("wikiLink.txt"));
        int i = 0;
        for (String result = parsePage(in); result != null;result = parsePage(in)){
            i++;
            if (i % 1000 == 0)
                System.out.println(i + "   " +  result);
//            iin.readLine();
            out.write(result);
            out.newLine();
        }
        out.close();
        in.close();
    }

    public void sortResult() throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(
                new FileInputStream("output/51/part-r-00000")));
        BufferedWriter out = new BufferedWriter(new FileWriter("result.txt"));
        ArrayList<Tuple> list  = new ArrayList<>();
        while (true) {
            String line = in.readLine();
            if (line == null)
                break;
            String name = line.split("\t")[0];
            list.add(new Tuple(name,Double.parseDouble(line.split("\t")[1].split("\\|")[0])));
        }
        Collections.sort(list);
        for (Tuple t:list){
            out.write(t.s + "\t" + t.d + "\n");
        }
        in.close();
        out.close();
    }

    public static void main(String[] args) throws Exception {
        HtmlParser parser = new HtmlParser();
        parser.sortResult();

    }
}
