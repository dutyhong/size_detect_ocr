# 作者 ：duty
# 创建时间 ：2022/1/18 12:17 下午
# 文件 ：rocket_mq.py
from rocketmq.client import Producer, Message
import json
# from rocketmq.client import Producer, Message

import argparse


# def ProducerSend(body):
# 	accesskey = "testaccess"
# 	secretkey = "test123"
# 	gid = "GID_test"
#
# 	producer = Producer(gid)
# 	producer.set_namesrv_addr('127.0.0.1:9876')
# 	producer.set_session_credentials(accesskey, secretkey, '')
# 	producer.start()
#
# 	msg = Message('test')
# 	msg.set_body(body)
# 	ret = producer.send_sync(msg)
# 	print(ret.status, ret.msg_id, ret.offset)
# 	producer.shutdown()
#

accesskey = "search"
secretkey = "Fd0b6b0ddd95"
producer = Producer('test')
producer.set_name_server_address('zjk-rocketmq-namesrv-pub.fordealinc.com:9876')  #rocketmq队列接口地址（服务器ip:port）
producer.set_session_credentials(accesskey, secretkey, '')
producer.start()

msg_body = {"id":"001","name":"test_mq","message":"abcdefg"}
ss = json.dumps(msg_body).encode('utf-8')

msg = Message('image_result')   #topic名称
msg.set_keys('xxxxxx')
msg.set_tags('xxxxxx')
msg.set_body(ss)      #message body

retmq = producer.send_sync(msg)
print(retmq.status, retmq.msg_id, retmq.offset)
producer.shutdown()


import time

# from rocketmq.client import PushConsumer
#
#
# accesskey = "testaccess"
# secretkey = "test123"
#
# def callback(msg):
#     print(msg.id, msg.body)
#
#
# consumer = PushConsumer('GID_Lcrmcnn')
# consumer.set_name_server_address('127.0.0.1:9876')
# # consumer.set_session_credentials(accesskey, secretkey, '')
# consumer.subscribe('lcrm_test', callback)
# consumer.start()
#
# # while True:
# #     time.sleep(3600)
#
# consumer.shutdown()