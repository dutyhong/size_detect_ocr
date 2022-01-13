# 作者 ：duty
# 创建时间 ：2022/1/13 11:44 上午
# 文件 ：connect_kafka.py
from kafka import KafkaConsumer, KafkaProducer

from sizechart_detect.global_config import KAFKA_SERVER, KAFKA_CONSUMER_TOPIC
kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, api_version=(0,10))
kafka_consumer = KafkaConsumer(KAFKA_CONSUMER_TOPIC, bootstrap_servers=[KAFKA_SERVER], group_id='image', auto_offset_reset='latest', consumer_timeout_ms=1000*60)
