import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.*;
/**
 * Created by hadoop on 16-6-10.
 */
public class PageRank {
    public static class Map extends Mapper<Text, Text, Text, Text>
    {
        @Override
        protected void map(Text key,Text value, Context context)
                throws IOException, InterruptedException {
            String [] ss = value.toString().split("\\|");
            if (ss.length != 2 || ss[1].isEmpty()){
                context.write(key,new Text());
                return;
            }
            double currentRank = Double.parseDouble(ss[0]);
            context.write(key,new Text(ss[1]));
            String[] links = ss[1].split(",");
            for (String link:links){
                context.write(new Text(link),new Text(Double.toString(currentRank / links.length)));
            }
        }
    }

    public static class Combine extends Reducer<Text, Text, Text, Text>
    {
        @Override
        protected void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            double sum = 0;
            String s;
            for (Text t : values){
                s = t.toString();
                if (s.matches("[0-9]+\\.?[0-9]*(E-?[0-9]+)?"))
                    sum += Double.parseDouble(s);
                else
                    context.write(key,t);
            }
            context.write(key,new Text(Double.toString(sum)));
        }
    }

    public static class Reduce extends Reducer<Text, Text, Text, Text>
    {
        final private static double d = 0.85;
        @Override
        protected void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            double sum = 0;
            String links = "";
            String s;
            for (Text t : values){
                s = t.toString();
                if (s.matches("[0-9]+\\.?[0-9]*(E-?[0-9]+)?"))
                    sum += Double.parseDouble(s);
                else
                    links = "|" + s;
            }

            context.write(key,new Text(1 - d + d * sum + links));
        }
    }

    private static boolean initialInvertedIndex(String inputPath, String outputPath) throws Exception {
        Configuration conf = new Configuration();
        Job job = new Job(conf, "Page Rank");
        job.setJarByClass(PageRank.class);
        job.setMapperClass(Map.class);//为job设置Mapper类
        job.setCombinerClass(Combine.class);
        job.setReducerClass(Reduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        job.setInputFormatClass(KeyValueTextInputFormat.class);
        FileInputFormat.setInputPaths(job, new Path(inputPath));
        FileOutputFormat.setOutputPath(job, new Path(outputPath));
        cleanInput(inputPath);
        return job.waitForCompletion(true);
    }

    private static void cleanInput(String inputPath){
        deleteFile(inputPath + "/._SUCCESS.crc");
        deleteFile(inputPath + "/.part-r-00000.crc");
        deleteFile(inputPath + "/_SUCCESS");
    }

    private static void deleteFile(String fileName){
        File f = new File(fileName);
        if (f.exists())
            f.delete();
    }

    public static void main(String[] args) throws Exception  {
        for (int i = 1; i < 51;i++){
            System.out.println("========================================" + i + "        begin!!!");
            if (!initialInvertedIndex("output/" + i,"output/" + (i + 1)))
                return;
        }
//        System.exit(initialInvertedIndex(args[0],"output") ?0:1);
    }
}
