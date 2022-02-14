# 作者 ：duty
# 创建时间 ：2022/1/13 11:44 上午
# 文件 ：connect_kafka.py
from kafka import KafkaConsumer, KafkaProducer

from sizechart_detect.global_config import KAFKA_SERVER, KAFKA_CONSUMER_TOPIC
# kafka_producer = KafkaProducer(
#     sasl_mechanism="SCRAM-SHA-256",
#     security_protocol='SASL_PLAINTEXT',
#     sasl_plain_username="search",
#     sasl_plain_password="345a3b326679448b787f0e0e56858e47",
#     bootstrap_servers='zjk-search-kafka-pub.duolainc.com:9092'
#   )
kafka_producer = KafkaProducer(
    bootstrap_servers='nx1-kafka-test-inner.fordealinc.com:9092'
  )
print("生产者连接完成")
# kafka_consumer = KafkaConsumer(
#         # "image_recognize",
#         sasl_mechanism="SCRAM-SHA-256",
#         security_protocol='SASL_PLAINTEXT',
#         sasl_plain_username="search",
#         sasl_plain_password="345a3b326679448b787f0e0e56858e47",
#         bootstrap_servers='zjk-search-kafka-pub.duolainc.com:9092',
#         auto_offset_reset='earliest', group_id = "tizi")
kafka_consumer = KafkaConsumer(
        bootstrap_servers='nx1-kafka-test-inner.fordealinc.com:9092',
        auto_offset_reset='earliest', group_id = "tizi")
# kafka_consumer_priority = KafkaConsumer(
#         # "image_recognize_priority",
#         sasl_mechanism="SCRAM-SHA-256",
#         security_protocol='SASL_PLAINTEXT',
#         sasl_plain_username="search",
#         sasl_plain_password="345a3b326679448b787f0e0e56858e47",
#         bootstrap_servers='zjk-search-kafka-pub.duolainc.com:9092',
#         auto_offset_reset='earliest', group_id = "tizi",
#         consumer_timeout_ms = 1000*3)
kafka_consumer.subscribe(topics=['image_recognize_priority', 'image_recognize'])
print("消费者连接完成")
