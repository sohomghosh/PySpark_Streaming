#To run this
#spark-submit spark_streaming_code_netcat server.py localhost 9999

#From another terminal write the following
#nc -lk 9999
#Write words over here

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "NetworkWordCount")
ssc = StreamingContext(sc, 1)
sc.setLogLevel('ERROR')

# Create a DStream that will connect to hostname:port, like localhost:9092
lines = ssc.socketTextStream("localhost", 9999)

# Split each line into words
words = lines.flatMap(lambda line: line.split(" "))

# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)

# Print the first ten elements of each RDD generated in this DStream to the console
wordCounts.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate

#Reference: https://spark.apache.org/docs/latest/streaming-programming-guide.html

