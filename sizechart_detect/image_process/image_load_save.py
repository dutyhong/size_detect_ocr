# 作者 ：duty
# 创建时间 ：2022/1/10 3:48 下午
# 文件 ：image_load_save.py
import os
import urllib.request
import ssl
import logging
logger = logging.getLogger('django')
from sizechart_detect.global_config import ORIGINAL_IMAGE_FILEPATH

ssl._create_default_https_context = ssl._create_unverified_context
#
# img_url1 = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1516371301&di=d99af0828bb301fea27c2149a7070" \
#           "d44&imgtype=jpg&er=1&src=http%3A%2F%2Fupload.qianhuaweb.com%2F2017%2F0718%2F1500369506683.jpg"
img_url2 = "https://cbu01.alicdn.com/img/ibank/O1CN01YZiANY23jKN3DydL3_!!2207282997291-0-cib.jpg"
# file_path = '/Users/duty/PycharmProjects/ocr/data/image_data/original_images'

def load_save_image(item_id, img_urls):
    image_num = len(img_urls)
    image_file_suffix = ""
    try:
        # 是否有这个路径
        if not os.path.exists(ORIGINAL_IMAGE_FILEPATH):
            # 创建路径
            os.makedirs(ORIGINAL_IMAGE_FILEPATH)
            # 获得图片后缀
        for i, img_url in enumerate(img_urls):
            file_suffix = os.path.splitext(img_url)[1]
            # print(file_suffix)
            file_name = item_id+"_"+str(i+1)
            # 拼接图片名（包含路径）
            filename = '{}{}{}{}'.format(ORIGINAL_IMAGE_FILEPATH, os.sep, file_name, file_suffix)
            # print(filename)
            # 下载图片，并保存到文件夹中
            urllib.request.urlretrieve(img_url, filename=filename)
            image_file_suffix = file_suffix
        return image_file_suffix
    except IOError as e:
        logger.error("图片读取保存报错！！！")
    except Exception as e:
        logger.error("图片读取保存报错！！！")


if __name__=="__main__":
    image_urls = [ img_url2]
    load_save_image("1", image_urls)
    print("ddd")