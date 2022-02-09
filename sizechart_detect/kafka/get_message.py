# 作者 ：duty
# 创建时间 ：2022/1/11 9:52 上午
# 文件 ：get_message.py
import logging

from kafka import KafkaConsumer
import json
# from sizechart_detect.global_config import KAFKA_SERVER, KAFKA_PRODUCER_TOPIC


def kafka_consumer():
    consumer = KafkaConsumer(
        "image_recognize",
        sasl_mechanism="SCRAM-SHA-256",
        security_protocol='SASL_PLAINTEXT',
        sasl_plain_username="search",
        sasl_plain_password="345a3b326679448b787f0e0e56858e47",
        bootstrap_servers='zjk-search-kafka-pub.duolainc.com:9092',
        auto_offset_reset='earliest', consumer_timeout_ms=1000*60*60, group_id = "tizi")
    print("kafka消费连接成功！！")
    for msg in consumer:
        consumer.commit()
        recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
        value = str(msg.value,"utf-8")
        msg_dict = json.loads(value)
        print(msg_dict)
        print(msg_dict["columnValueMap"])
        print(value)
    consumer.close()



if __name__=="__main__":
    kafka_consumer()
    print("ddd")