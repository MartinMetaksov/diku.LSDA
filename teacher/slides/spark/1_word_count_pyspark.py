text = sc.textFile("hdfs:///user/lsda/lsda.txt")
words = text.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)
