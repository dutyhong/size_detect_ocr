# 作者 ：duty
# 创建时间 ：2022/1/7 4:54 下午
# 文件 ：darknet_yolo3_detect.py
import time
from ctypes import *
import random
import cv2

from sizechart_detect.global_config import LIBDARKNET_DIR


def sample(probs):
    s = sum(probs)
    probs = [a / s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs) - 1


def c_array(ctype, values):
    arr = (ctype * len(values))()
    arr[:] = values
    return arr


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


# lib = CDLL("/Users/duty/work/darknet/python/libdarknet.so", RTLD_GLOBAL)
lib = CDLL(LIBDARKNET_DIR+"libdarknet.so",RTLD_GLOBAL )
# lib = CDLL("libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)


# net_d = load_net(b"../cfg/yolov3.cfg", b"../yolov3.weights", 0)
# meta_d = load_meta(b"../cfg/coco.data")
print("lib加载完成")

def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res


def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = load_image(image, 0, 0)
    num = c_int(0)
    pnum = pointer(num)
    predict_image(net, im)
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    if (nms): do_nms_obj(dets, num, meta.classes, nms);

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_detections(dets, num)
    return res


def detect_and_boxing(net, meta, b_path, raw_path, save_path,
                      color=(0.255, 255), line_type=1):
    image = cv2.imread(raw_path)
    r = detect(net, meta, b_path)
    result_images = []
    if not len(r) > 0:
        # print("nothing detected in this picture!")
        return []
    else:
        for i in range(len(r)):
            box_i = r[i]
            label_i = box_i[0]
            prob_i = box_i[1]
            x_ = box_i[2][0]
            y_ = box_i[2][1]
            w_ = box_i[2][2]
            h_ = box_i[2][3]
            text_ = str(label_i) + "," + str(round(prob_i, 3))

            # cv2.rectangle(image, (int(x_ - w_ / 2), int(y_ - h_ / 2)),
            #               (int(x_ + w_ / 2), int(y_ + h_ / 2)),
            #               color, line_type)
            # cv2.putText(image, text_, (int(x_ - w_ / 2 - 5), int(y_ - h_ / 2 - 5)), cv2.FONT_HERSHEY_DUPLEX, 0.7, color,
            #             2)
            rec_image = image[int(y_ - h_ / 2): int(y_ + h_ / 2),int(x_ - w_ / 2):int(x_ + w_ / 2)]
            ### 将识别的列图片进行保存
            # cv2.imwrite("../../data/image_data/"+str(i)+".jpg",rec_image)
            result_images.append(rec_image)
            # cv2.imwrite(save_path, image)
            # print("boxing ", i, " found ", label_i, "with prob = ", prob_i, ", finished!")
            # print("box position is :", box_i[2])
    return result_images


if __name__ == "__main__":
    # net = load_net("cfg/densenet201.cfg", "/home/pjreddie/trained/densenet201.weights", 0)
    # im = load_image("data/wolf.jpg", 0, 0)
    # meta = load_meta("cfg/imagenet1k.data")
    # r = classify(net, meta, im)
    # print(r)
    net = load_net(b"/Users/duty/publicdata/yolo_weights/col_detect.cfg", b"/Users/duty/publicdata/yolo_weights/col_detect.weights", 0)
    meta = load_meta(b"/Users/duty/publicdata/yolo_weights/col_detect.data")

    b_path = b"../../data/image_data/0_1.jpg"
    raw_path = "../../data/image_data/0_1.jpg"
    save_path = "../../data/image_data/0_1_res.jpg"
    start_time = int(1000 * time.time())

    detect_and_boxing(net, meta, b_path=b_path, raw_path=raw_path, save_path=save_path)
    end_time = int(1000 * time.time())
    print("耗时为：%s毫秒！！"%(end_time-start_time))
    print("ddd")