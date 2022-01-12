# 作者 ：duty
# 创建时间 ：2022/1/11 9:54 上午
# 文件 ：config.py
import os
APP_ENV = os.environ.get('APP_ENV', 'default').lower()
KAFKA_SERVER = "gz-kafka-dev-inner.duolainc.com:9092" if APP_ENV=="default" else "xxx"
ORIGINAL_IMAGE_FILEPATH = '/Users/duty/PycharmProjects/ocr/data/image_data/original_images' if APP_ENV=="default" else "/home/tizi/ocr/data/image_data/original_images"
CTPN_MODELS_DIR = '/Users/duty/PycharmProjects/ocr/data/models/' if APP_ENV=="default" else "/home/tizi/ocr/data/models/"
CRNN_MODELS_DIR = '/Users/duty/PycharmProjects/ocr/data/models/' if APP_ENV=="default" else "/home/tizi/ocr/data/models/"
YOLO_MODELS_DIR = '/Users/duty/publicdata/yolo_weights/' if APP_ENV=="default" else "/home/tizi/publicdata/yolo_weights/"
LIBDARKNET_DIR = '/Users/duty/work/darknet/python/' if APP_ENV=="default" else "/home/tizi/darknet/python/"