# 作者 ：duty
# 创建时间 ：2022/1/10 2:28 下午
# 文件 ：message_send.py
import logging

from kafka import KafkaConsumer
# 实例化一个KafkaProducer示例，用于向Kafka投递消息
import json
from kafka import KafkaProducer
from confluent_kafka import Producer
# from sizechart_detect.global_config import KAFKA_SERVER, KAFKA_PRODUCER_TOPIC
conf = {
    'bootstrap.servers': 'zjk-search-kafka-pub.duolainc.com:9092',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'sasl.username': 'search',
    'sasl.password': '345a3b326679448b787f0e0e56858e47',
}

def kafka_producer2():
  producer = KafkaProducer(
    sasl_mechanism="SCRAM-SHA-256",
    security_protocol='SASL_PLAINTEXT',
    sasl_plain_username="search",
    sasl_plain_password="345a3b326679448b787f0e0e56858e47",
    # bootstrap_servers='zjk-search-kafka-pub.duolainc.com:9092'
    bootstrap_servers = 'x1-kafka-test-inner.fordealinc.com:9092'
  )
  print("生产者创建成功！！")
  msg_dict = {
    "image_urls": ["111", "222"],
    "sizeattrs": {"全胸围/Bust/Chest(厘米)": 125, "袖长/Sleeve/Arm length(厘米)": 129, "衣长/Length(厘米)": 128,
                  "肩宽/Shoulder(厘米)": 124, "身高/Body height(厘米)": 11372},
    "sizes": {"S": 2047426, "L": 2047401}
  }
  msg = json.dumps(msg_dict, ensure_ascii=False)
  producer.send("image_result", msg.encode())  ##, partition=0)
  producer.close()
  print("消息生产成功！！")


def kafka_producer():
  producer = KafkaProducer(bootstrap_servers = 'x1-kafka-test-inner.fordealinc.com:9092')
  logging.info("生产者创建成功！！")
  msg_dict = {
    "image_urls":["111","222"],
    "sizeattrs":{"全胸围/Bust/Chest(厘米)":125,"袖长/Sleeve/Arm length(厘米)":129,"衣长/Length(厘米)":128,"肩宽/Shoulder(厘米)":124,"身高/Body height(厘米)":11372},
    "sizes":{"S":2047426,"L":2047401}
  }
  msg = json.dumps(msg_dict,ensure_ascii=False)
  producer.send("image_result", msg.encode()) ##, partition=0)
  # producer.close()
  logging.info("消息生产成功！！")
  print("消息生产成功！！")

if __name__=="__main__":
  kafka_producer()
  print("dd")
