# (1) parallelize collection via driver program
lines = sc.parallelize(["when", "nothing is", "going right", "go left"])

# (2) load from external sources
passwd = sc.textFile("file:///etc/passwd")
air = sc.textFile("hdfs:///user/lsda/airline_data/2016_1.csv")
air_all = sc.textFile("hdfs:///user/lsda/airline_data/*.csv")
