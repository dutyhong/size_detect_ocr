# 作者 ：duty
# 创建时间 ：2022/1/10 11:13 上午
# 文件 ：whole_stages.py
import os
import time

import torch

from sizechart_detect.detect import config
from sizechart_detect.column_detect.darknet_yolo3_detect import load_net, load_meta, detect_and_boxing
from sizechart_detect.detect.ctpn_model import CTPN_Model
from sizechart_detect.global_config import YOLO_MODELS_DIR
from sizechart_detect.ocr import  ocr2
import logging

from sizechart_detect.recognize.crnn_recognizer import PytorchOcr

logger = logging.getLogger('django')
cfg_data = bytes(YOLO_MODELS_DIR+"col_detect.cfg",encoding="utf-8")
weights_data = bytes(YOLO_MODELS_DIR+"col_detect.weights", encoding="utf-8")
meta_data = bytes(YOLO_MODELS_DIR+"col_detect.data", encoding="utf-8")
# net = load_net(b"/Users/duty/publicdata/yolo_weights/col_detect.cfg", b"/Users/duty/publicdata/yolo_weights/col_detect.weights", 0)
# meta = load_meta(b"/Users/duty/publicdata/yolo_weights/col_detect.data")
net = load_net(cfg_data, weights_data, 0)
meta = load_meta(meta_data)
logger.info("yolo模型记载完成！！")
gpu = True
if not torch.cuda.is_available():
    gpu = False
device = torch.device('cuda:0' if gpu else 'cpu')
weights = os.path.join(config.checkpoints_dir, 'CTPN.pth')
model = CTPN_Model()
model.load_state_dict(torch.load(weights, map_location=device)['model_state_dict'])
model.to(device)
model.eval()
logger.info("CTPN模型加载完成")
recognizer = PytorchOcr()
logger.info("CRNN模型加载完成")
detector = model
def whole_stages(image_filepath):
	# b_path = str.encode("/Users/duty/PycharmProjects/ocr/data/image_data/0_1.jpg")
	# raw_path = "/Users/duty/PycharmProjects/ocr/data/image_data/0_1.jpg"
	# save_path = "/Users/duty/PycharmProjects/ocr/data/image_data/0_1_res.jpg"
	b_path = str.encode(image_filepath)
	raw_path = image_filepath
	save_path = ""
	###列检查和识别
	start_time = int(1000*time.time())
	col_detect_images = detect_and_boxing(net, meta, b_path=b_path, raw_path=raw_path, save_path=save_path)
	end_time = int(1000*time.time())
	logger.info("商品：%s 列识别完成, 耗时为：%s毫秒"%(image_filepath, end_time-start_time))
	col_texts = []
	if len(col_detect_images)==0:
		logger.info("Nothing detect !!!")
		return None
	for image in col_detect_images:
		# col_detect_results, image_framed = single_pic_proc2(image)
		col_detect_results, image_framed = ocr2(image, detector, recognizer)
		col_text = []
		for num, col_detect_result in col_detect_results.items():
			text = col_detect_result[1]
			col_text.append(text)
			# print(tex)
		logger.info(col_text)
		col_texts.append(col_text)
	logger.info("商品： %s 文本识别完成" % (image_filepath))
	return col_texts



if __name__=="__main__":
	image_filepath = "/Users/duty/PycharmProjects/ocr/data/image_data/0_10.jpg"
	col_texts = whole_stages(image_filepath)
	print("ddd")



