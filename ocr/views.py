# # 作者 ：duty
# # 创建时间 ：2022/1/7 3:48 下午
# # 文件 ：views.py
# import json
# import logging
# import os
#
# from sizechart_detect.global_config import ORIGINAL_IMAGE_FILEPATH
#
# logger = logging.getLogger('django')
# from django.http import HttpResponse
#
# from sizechart_detect.image_process.image_load_save import load_save_image
# from sizechart_detect.utils.size_chart_normal import size_chart_normal
# from sizechart_detect.whole_stages import whole_stages
#
#
# def post(request):
# 	res_dic = {}
# 	post_body = request.body
# 	post_body = json.loads(post_body.decode())
# 	item_id = post_body.get('item_id', None)
# 	image_urls = post_body.get('image_urls', None)
# 	size_attrs= post_body.get('size_attrs', None)
# 	sizes = post_body.get('sizes', None)
# 	# print(request.get_json())
# 	if item_id is None or image_urls is None or size_attrs is None or sizes is None:
# 		logging.error("输入参数有问题！！！")
# 		res_dic['status'] = 'failed'
# 		res_dic['item_id'] = item_id
# 		res_dic = json.dumps(res_dic)
# 		return HttpResponse(res_dic)
# 	# image_urls = json.loads(image_urls)
# 	# size_attrs = json.loads(size_attrs)
# 	# sizes = json.loads(sizes)
# 	##获取图片并保存
# 	image_file_suffix = load_save_image(item_id, image_urls)
# 	logger.info("商品：%s图片保存完成！！"%(item_id))
# 	## 开始进行图片识别，是否有尺码表
# 	image_num = len(image_urls)
# 	##如果图片数量太多，不识别了
# 	if image_num>4:
# 		res_dic['item_id'] = item_id
# 		res_dic['status'] = 'failed'
# 		res_dic = json.dumps(res_dic)
# 		return res_dic
# 	col_texts = []
# 	for i in range(image_num):
# 		filepath = ORIGINAL_IMAGE_FILEPATH + os.sep + str(item_id) + "_" + str(i + 1) + image_file_suffix
# 		detect_texts = whole_stages(filepath)
# 		if detect_texts is None:
# 			continue
# 		else:
# 			col_texts = detect_texts
# 			break
# 	logger.info("商品：%s 识别完成！！！"%(item_id))
# 	## 将识别出来的列名和尺码表的列名对齐，转化为id
# 	normal_col_texts = size_chart_normal(col_texts, size_attrs)
# 	res_dic['size_chart'] = normal_col_texts
# 	res_dic['status'] = 'success'
# 	res_dic['item_id'] = item_id
# 	res_dic = json.dumps(res_dic,ensure_ascii=False)
# 	return HttpResponse(res_dic)