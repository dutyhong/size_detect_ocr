# 作者 ：duty
# 创建时间 ：2022/2/9 11:36 上午
# 文件 ：message_consume.py
import json
import logging
import os

from sizechart_detect.global_config import KAFKA_PRODUCER_TOPIC, ORIGINAL_IMAGE_FILEPATH
from sizechart_detect.kafka.connect_kafka import kafka_consumer, kafka_producer

from sizechart_detect.image_process.image_load_save import load_save_image
from sizechart_detect.utils.size_chart_normal import size_chart_normal
from sizechart_detect.whole_stages import whole_stages

logger = logging.getLogger('django')



def consume_send(msg):
	res_dic = {}
	value = str(msg.value, "utf-8")
	logger.info(value)
	msg_dict = json.loads(value)
	size_attrs = msg_dict["columnValueMap"]
	item_id = str(msg_dict["extId"])
	image_urls = msg_dict["images"]
	# sizes = msg_dict["rowMapAsc"]
	# kafka_msgs.append(value)
	# 获取图片并保存
	image_file_suffix = load_save_image(item_id, image_urls)
	logger.info("商品：%s图片保存完成！！" % (item_id))
	## 开始进行图片识别，是否有尺码表
	image_num = len(image_urls)
	if image_num > 30 or image_file_suffix is None or item_id=="2253":
		res_dic['extId'] = item_id
		res_dic['status'] = 'failed'
		res_dic['columnValueMap'] = size_attrs
		res_dic['valueMap'] = None
		res_dic['recognizedImage'] = None
		# res_dic['rowMapAsc'] = sizes
		res_dic = json.dumps(res_dic, ensure_ascii=False)
		kafka_producer.send(KAFKA_PRODUCER_TOPIC, res_dic.encode())
	# return res_dic
	else:
		col_texts = []
		recognize_ind = 0
		for i in range(image_num):
			filepath = ORIGINAL_IMAGE_FILEPATH + os.sep + str(item_id) + "_" + str(i + 1) + image_file_suffix
			try:
				detect_texts = whole_stages(filepath)
			except Exception:
				logger.error("图片尺寸出错！！！！")
				detect_texts = None
			if detect_texts is None:
				continue
			else:
				col_texts = detect_texts
				recognize_ind = i
				break
		logger.info("商品：%s 识别完成！！！" % (item_id))
		## 将识别出来的列名和尺码表的列名对齐，转化为id
		if len(col_texts) == 0:
			res_dic['extId'] = item_id
			res_dic['status'] = 'failed'
			res_dic['columnValueMap'] = size_attrs
			res_dic['valueMap'] = None
			res_dic['recognizedImage'] = None
			# res_dic['rowMapAsc'] = sizes
			res_dic = json.dumps(res_dic, ensure_ascii=False)
			kafka_producer.send(KAFKA_PRODUCER_TOPIC, res_dic.encode())
			logger.info("未识别生产成功！！")
		else:
			normal_col_texts = size_chart_normal(col_texts, size_attrs)
			res_dic['valueMap'] = normal_col_texts
			res_dic['status'] = 'success'
			res_dic['extId'] = item_id
			res_dic['columnValueMap'] = size_attrs
			res_dic['recognizedImage'] = image_urls[recognize_ind]
			# res_dic['rowMapAsc'] = sizes
			res_dic = json.dumps(res_dic, ensure_ascii=False)
			kafka_producer.send(KAFKA_PRODUCER_TOPIC, res_dic.encode())
			logger.info("生产成功！！")