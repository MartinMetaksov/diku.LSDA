import matplotlib.pyplot as plt

# load Landsat test data from HDFS
train = sc.textFile("hdfs:///user/lsda/landsat_train.csv")

# apply transformation
train = train.take(100000)
pairs = train.map(lambda line: (int(line.split(",")[0]),1))
counts = pairs.reduceByKey(lambda a, b: a + b)
counts_local = counts.collect()

# plot histogram (on driver node)
plt.bar(range(len(counts_local)), counts_local)
plt.show()
