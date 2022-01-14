# 作者 ：duty
# 创建时间 ：2022/1/11 9:52 上午
# 文件 ：get_message.py
import logging

from kafka import KafkaConsumer

# from sizechart_detect.global_config import KAFKA_SERVER, KAFKA_PRODUCER_TOPIC


def kafka_consumer():
    consumer = KafkaConsumer("size_recog_result", bootstrap_servers="ir-search-kafka01.duolainc.com:9092,ir-search-kafka02.duolainc.com:9092,ir-search-kafka03.duolainc.com:9092".split(","), group_id='image', auto_offset_reset='latest', consumer_timeout_ms=1000*60*60)
    logging.info("kafka消费连接成功！！")
    print("kafka消费连接成功！！")
    for msg in consumer:
        consumer.commit()
        # recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
        value = str(msg.value,"utf-8")
        logging.info(value)
        print(value)
    consumer.close()



if __name__=="__main__":
    kafka_consumer()
    print("ddd")