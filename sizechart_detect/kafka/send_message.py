# 作者 ：duty
# 创建时间 ：2022/1/10 2:28 下午
# 文件 ：message_send.py
import logging

from kafka import KafkaConsumer
# 实例化一个KafkaProducer示例，用于向Kafka投递消息
import json
from kafka import KafkaProducer

from sizechart_detect.global_config import KAFKA_SERVER


def kafka_producer():
  producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, api_version=(0,10))
  logging.info("生产者创建成功！！")
  msg_dict = {
    "image_urls":["111","222"],
    "sizeattrs":{"全胸围/Bust/Chest(厘米)":125,"袖长/Sleeve/Arm length(厘米)":129,"衣长/Length(厘米)":128,"肩宽/Shoulder(厘米)":124,"身高/Body height(厘米)":11372},
    "sizes":{"S":2047426,"L":2047401}
  }
  msg = json.dumps(msg_dict,ensure_ascii=False)
  producer.send('image_recognize', msg.encode()) ##, partition=0)
  producer.close()
  logging.info("消息生产成功！！")
  print("消息生产成功！！")

if __name__=="__main__":
  kafka_producer()
  print("dd")
