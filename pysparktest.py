# pyspark test
import pyspark

sc = pyspark.SparkContext()
rdd = sc.textFile('tweets_new.txt')
result = rdd.map(lambda s: len(s)).reduce(lambda a, b: a + b)

print result
