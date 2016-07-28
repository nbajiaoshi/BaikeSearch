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
    public static class Map extends Mapper<LongWritable, Text, Text, LongWritable>
    {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        private FileSystem fs;

        @Override
        protected void setup(Context context) throws IOException, InterruptedException {
            FileSplit fs = (FileSplit)context.getInputSplit();
            String fileName = fs.getPath().getName();
            Matcher prefixFilter = Pattern.compile("\\d+").matcher(fileName);
            if (prefixFilter.find())
                fileName = prefixFilter.group(0);
            System.out.println("========================================:" + fileName);
        }

        @Override
        protected void map(LongWritable key,Text value, Context context)
                throws IOException, InterruptedException {
            FileSplit fs = (FileSplit)context.getInputSplit();
            String line = value.toString().toLowerCase();
            String fileName = fs.getPath().getName();
            Matcher prefixFilter = Pattern.compile("\\d+").matcher(fileName);
            if (prefixFilter.find())
                fileName = prefixFilter.group(0);
            Pattern pattern = Pattern.compile("\\w+|[\\u4e00-\\u9fa5]+");
            Matcher m = pattern.matcher(line);
            while (m.find()){
                word.set(line.substring(m.start(),m.end()));
                context.write(word,new LongWritable(Integer.parseInt(fileName)));
            }
        }
    }
    public static class Reduce extends Reducer<Text, LongWritable, Text, Text>
    {
        protected void reduce(Text key, Iterable<LongWritable> values, Context context)
                throws IOException, InterruptedException {
            Set<String> docs = new HashSet<String>();
            StringBuilder s = new StringBuilder();
            for (LongWritable t : values){
                String doc = t.toString();
                if (!docs.contains(doc)){
                    docs.add(doc);
                    s.append(doc + ",");
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
        job.setOutputValueClass(LongWritable.class);
        FileInputFormat.setInputPaths(job, new Path(inputPath));
        FileOutputFormat.setOutputPath(job, new Path("output1"));
        return job.waitForCompletion(true);
    }

    public static void main(String[] args) throws Exception    {
        System.exit(initialInvertedIndex(args[0]) ?0:1);
    }
}
