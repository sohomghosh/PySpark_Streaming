#https://medium.com/@kass09/spark-streaming-kafka-in-python-a-test-on-local-machine-edd47814746
#Get extact package from https://spark.apache.org/docs/2.1.0/streaming-kafka-0-8-integration.html [Change 2.1.0 to your desired version]
#spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 spark_streaming_code.py localhost:9092 new_topic
#spark-submit --jars /usr/local/spark/jars/spark-streaming-kafka-0-8-assembly_2.11.jar spark_streaming_code.py localhost:9092 new_topic

import sys
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1

if __name__ == "__main__":
    sc = SparkContext(appName="PythonStreamingRecieverKafkaWordCount")
    sc.setLogLevel('ERROR')
    ssc = StreamingContext(sc, 2) # 2 second window
    broker, topic = sys.argv[1:]
    #broker = 'localhost:9092'
    #topic = 'new_topic'
    kvs = KafkaUtils.createStream(ssc, \
                                  broker, \
                                  "raw-event-streaming-consumer",\
                                  {topic:1}) 
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(" "))\
                  .map(lambda word: (word, 1)) \
                  .reduceByKey(lambda a, b: a+b)
    counts.pprint()
    ssc.start()
    ssc.awaitTermination()
