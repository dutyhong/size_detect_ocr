import time

from django.shortcuts import render

# Create your views here.
import json
import logging
import os

from sizechart_detect.global_config import ORIGINAL_IMAGE_FILEPATH, KAFKA_PRODUCER_TOPIC
# from sizechart_detect.kafka.connect_kafka import kafka_consumer, kafka_producer

logger = logging.getLogger('django')
from django.http import HttpResponse

from sizechart_detect.image_process.image_load_save import load_save_image
from sizechart_detect.utils.size_chart_normal import size_chart_normal
from sizechart_detect.whole_stages import whole_stages

def post(request):
	res_dic = {}
	post_body = request.body
	post_body = json.loads(post_body.decode())
	item_id = post_body.get('item_id', None)
	image_urls = post_body.get('image_urls', None)
	size_attrs= post_body.get('size_attrs', None)
	sizes = post_body.get('sizes', None)
	# print(request.get_json())
	if item_id is None or image_urls is None or size_attrs is None or sizes is None:
		logging.error("输入参数有问题！！！")
		res_dic['status'] = 'failed'
		res_dic['item_id'] = item_id
		res_dic["msg"] = "输入参数有问题！！"
		res_dic['request'] = post_body
		res_dic = json.dumps(res_dic,ensure_ascii=False)
		return HttpResponse(res_dic)
	# image_urls = json.loads(image_urls)
	# size_attrs = json.loads(size_attrs)
	# sizes = json.loads(sizes)
	start_time = int(1000*time.time())
	##获取图片并保存
	image_file_suffix = load_save_image(item_id, image_urls)
	logger.info("商品：%s图片保存完成！！"%(item_id))
	## 开始进行图片识别，是否有尺码表
	image_num = len(image_urls)
	if image_num>30 or image_file_suffix is None:
		res_dic['item_id'] = item_id
		res_dic['status'] = 'failed'
		res_dic['request'] = post_body
		res_dic["mag"] = "picture too many or load failed"
		res_dic = json.dumps(res_dic,ensure_ascii=False)
		return HttpResponse(res_dic)
	col_texts = []
	for i in range(image_num):
		filepath = ORIGINAL_IMAGE_FILEPATH + os.sep + str(item_id) + "_" + str(i + 1) + image_file_suffix
		detect_texts = whole_stages(filepath)
		if detect_texts is None:
			continue
		else:
			col_texts = detect_texts
			break
	logger.info("商品：%s 识别完成！！！"%(item_id))
	end_time = int(1000*time.time())
	total_time = end_time-start_time
	logger.info("一个商品总耗时为：%s毫秒"%(total_time))
	## 将识别出来的列名和尺码表的列名对齐，转化为id
	normal_col_texts = size_chart_normal(col_texts, size_attrs)
	res_dic['size_chart'] = normal_col_texts
	res_dic['iem_id'] = item_id
	res_dic['request'] = post_body
	res_dic['status'] = 'success'
	res_dic = json.dumps(res_dic,ensure_ascii=False)
	return HttpResponse(res_dic)

def kafka_post(request):
	res_dic = {}
	# post_body = request.body
	# post_body = json.loads(post_body.decode())
	# command = post_body.get('command', 'start')
	# kafka_msgs = []
	# if command=='start':
	# 	for msg in kafka_consumer:
	# 		kafka_consumer.commit()
	# 		# recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
	# 		value = str(msg.value, "utf-8")
	# 		logging.info(value)
	# 		kafka_msgs.append(value)
	# 		print(value)
	# 	for kafka_msg in kafka_msgs:
	# 		kafka_producer.send(KAFKA_PRODUCER_TOPIC, kafka_msg.encode())
	# 	kafka_producer.close()
	# res_dic['msg'] = "数据消费完成！！"
	#获取图片并保存
	# image_file_suffix = load_save_image(item_id, image_urls)
	# logger.info("商品：%s图片保存完成！！"%(item_id))
	# ## 开始进行图片识别，是否有尺码表
	# image_num = len(image_urls)
	# if image_num>20:
	# 	res_dic['item_id'] = item_id
	# 	res_dic['status'] = 'failed'
	# 	res_dic = json.dumps(res_dic)
	# 	return res_dic
	# col_texts = []
	# for i in range(image_num):
	# 	filepath = ORIGINAL_IMAGE_FILEPATH + os.sep + str(item_id) + "_" + str(i + 1) + image_file_suffix
	# 	detect_texts = whole_stages(filepath)
	# 	if detect_texts is None:
	# 		continue
	# 	else:
	# 		col_texts = detect_texts
	# 		break
	# logger.info("商品：%s 识别完成！！！"%(item_id))
	# ## 将识别出来的列名和尺码表的列名对齐，转化为id
	# normal_col_texts = size_chart_normal(col_texts, size_attrs)
	# res_dic['size_chart'] = normal_col_texts
	# res_dic['status'] = 'success'
	# res_dic = json.dumps(res_dic,ensure_ascii=False)
	return HttpResponse(res_dic)