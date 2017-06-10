from pyspark import SparkConf
from pyspark import SparkContext

def word_count(sc):

    text = sc.textFile("hdfs:///user/lsda/lsda.txt")
    words = text.flatMap(lambda line: line.split(" "))
    pairs = words.map(lambda word: (word, 1))
    counts = pairs.reduceByKey(lambda a, b: a + b)
    counts.saveAsTextFile("hdfs:///user/lsda/counts")

if __name__ == "__main__":

    conf = SparkConf().setAppName("Word Count")
    # run job on "local mode" (pseudo-cluster), use as many 
    # threads as the number of processors available for JVM.
    conf = conf.setMaster("local[*]")
    sc = SparkContext(conf=conf)

    word_count(sc)
