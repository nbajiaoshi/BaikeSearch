/**
 * Created by hadoop on 16-6-6.
 */
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

/**
 *
 * 描述：WordCount explains by Felix
 * @author Hadoop Dev Group
 */
public class WordCount
{
    public static class Map extends Mapper<LongWritable, Text, Text, IntWritable>
    {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        @Override
        protected void map(LongWritable key,Text value, Context context)
                throws IOException, InterruptedException {
            String line = value.toString().toLowerCase();
            Pattern pattern = Pattern.compile("\\w+");
            Matcher m = pattern.matcher(line);
            while (m.find()){
                word.set(line.substring(m.start(),m.end()));
                context.write(word, one);
            }
        }
    }
    public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable>
    {
        @Override
        protected void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable i : values){
                sum += i.get();
            }
            context.write(key,new IntWritable(sum));
        }
    }
}