import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by hadoop on 16-6-10.
 */
public class InvertedIndex {
    public static class Map extends Mapper<LongWritable, Text, Text, Text>
    {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        private static final Set<String> stopWords = new HashSet<String>();
        private FileSystem fs;

        @Override
        protected void setup(Context context) throws IOException, InterruptedException {
            Configuration conf = new Configuration();
            fs = FileSystem.get(conf);
            FSDataInputStream in = fs.open(new Path("output/part-r-00000"));
            while (true) {
                String line = in.readLine();
                if (line == null || line.isEmpty())
                    break;
                String ss[] = line.split("\\s+");
                if (Integer.parseInt(ss[1]) > 40000){
                    System.out.println("============================:" + ss[0] + "   " + ss[1]);
                    stopWords.add(ss[0]);
                }
            }
        }

        @Override
        protected void map(LongWritable key,Text value, Context context)
                throws IOException, InterruptedException {
            FileSplit fs = (FileSplit)context.getInputSplit();
            String line = value.toString().toLowerCase();
            Matcher angleBraket = Pattern.compile("<[^>]+>").matcher(line);
            angleBraket.replaceAll(" ");
            String fileName = fs.getPath().getName();
            Pattern pattern = Pattern.compile("[^\\s]+");
            Matcher m = pattern.matcher(line);
            while (m.find()){
                word.set(line.substring(m.start(),m.end()));
                if (!stopWords.contains(word.toString()))
                    context.write(word,new Text(fileName));
            }
        }
    }
    public static class Reduce extends Reducer<Text, Text, Text, Text>
    {
        protected void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            Set<String> docs = new HashSet<String>();
            StringBuilder s = new StringBuilder();
            for (Text t : values){
                String doc = t.toString();
                if (!docs.contains(doc)){
                    docs.add(doc);
                    s.append(doc + " ");
                }
            }
            context.write(key,new Text(s.toString()));
        }
    }

    private static boolean initialWordCount(String inputPath) throws Exception {
        Configuration conf = new Configuration();
        Job job = new Job(conf, "Word Count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(WordCount.Map.class);         //为job设置Mapper类
        job.setCombinerClass(WordCount.Reduce.class);      //为job设置Combiner类
        job.setReducerClass(WordCount.Reduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.setInputPaths(job, new Path(inputPath));
        FileOutputFormat.setOutputPath(job, new Path("output"));
        return job.waitForCompletion(true);
    }

    private static boolean initialInvertedIndex(String inputPath) throws Exception {
        Configuration conf = new Configuration();
        Job job = new Job(conf, "Inverted Index");
        job.setJarByClass(InvertedIndex.class);
        job.setMapperClass(Map.class);         //为job设置Mapper类
        job.setReducerClass(Reduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.setInputPaths(job, new Path(inputPath));
        FileOutputFormat.setOutputPath(job, new Path("output1"));
        return job.waitForCompletion(true);
    }

    public static void main(String[] args) throws Exception    {
        System.exit(initialWordCount(args[0]) && initialInvertedIndex(args[0]) ?0:1);
    }
}
