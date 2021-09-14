from ctypes import *
import math
import random
import cv2
import os
import time
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


# lib = CDLL("/home/pjreddie/documents/darknet/libdarknet.so", RTLD_GLOBAL)
lib = CDLL("./libdarknet.so", RTLD_GLOBAL)
# lib = CDLL("./Release/darknet.dll", RTLD_GLOBAL)
# if os.name == "posix":
#     cwd = os.path.dirname(__file__)
#     lib = CDLL(cwd + "/libdarknet.so", RTLD_GLOBAL)
# elif os.name == "nt":
#     cwd = os.path.dirname(__file__)
#     os.environ['PATH'] = cwd + ';' + os.environ['PATH']
#     lib = CDLL("darknet.dll", RTLD_GLOBAL)
# else:
#     print("Unsupported OS")
#     exit
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


def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res

def detect_cv(net,meta,img_cv,thresh = .5,hier_thresh = .5,nms = .45):
    h,w,c = img_cv.shape
    im = make_image(w,h,c)
    count = 0
    for i in range(c):
        for j in range(h):
            for k in range(w):
                im.data[count] = img_cv[j, k, i] / 255
                count = count + 1



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

def detect_im(net,meta,im,thresh = .5,hier_thresh = .5,nms = .45):
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


def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = load_image(image, 0, 0)

    # img_cv = cv2.imread(image, 1)
    #
    # h, w, c = img_cv.shape
    # im = make_image(w, h, c)
    # count = 0
    # for i in range(c):
    #     for j in range(h):
    #         for k in range(w):
    #             im.data[count] = img_cv[j, k, i] / 255
    #             count = count + 1

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

def print_im(im):
    for i in range(im.c):
        for j in range(im.h):
            for k in range(im.w):
                print("index : ", k + j * im.w + i * im.h * im.w, im.data[k + j * im.w + i * im.h * im.w])



# if __name__ == "__main__":
#     # net = load_net("cfg/densenet201.cfg", "/home/pjreddie/trained/densenet201.weights", 0)
#     # im = load_image("data/wolf.jpg", 0, 0)
# #     # meta = load_meta("cfg/imagenet1k.data")
# #     # r = classify(net, meta, im)
# #     # print r[:10]
#     net = load_net(b"../cfg/yolov3.cfg", b"../cfg/yolov3.weights", 0)
#     meta = load_meta(b"../cfg/coco.data")
# #
#     name_list = ['000000254016.jpg','000000453001.jpg','000000351559.jpg','000000231549.jpg','000000308328.jpg']
#     for i in name_list:
#         path = "/home/oceanai/Downloads/COCO/val2017/"+str(i)
#         cv_image = cv2.imread(path,1)
#         r = detect_cv(net,meta,cv_image)
#         print(r)
    # cv_image = cv2.imread('/home/oceanai/Downloads/COCO/val2017/000000254016.jpg',1)
#     a = time.time()
#     r = detect_cv(net,meta,cv_image)
#     print(r)
#
#     b = time.time()
#     print("spend ", str(b-a),'s')
#     #19s
#     r = detect(net,meta,b'/home/oceanai/Downloads/COCO/val2017/000000254016.jpg')
#     c = time.time()
#     print(r)
#     print("spend ", str(c-b),'s')
#     #16s


    # cv_image = cv2.imread("/home/oceanai/Downloads/COCO/val2017/000000231549.jpg",1)
    # r = detect_cv(net,meta,cv_image)
    # print(r)
    # h, w, c = cv_image.shape
    # im = make_image(w, h, c)
    # count = 0
    # for i in range(c):
    #     for j in range(h):
    #         for k in range(w):
    #             im.data[count] = cv_image[j, k, i] / 255
    #             # print("count :", count, im.data[count])
    #             count = count + 1
    # print(im.data[0],im.data[1],im.data[2])
    # print_im(im)

    # r = detect_cv(net, meta, cv_image)
    # print(r)
#
#     # [(b'dog', 0.999338686466217, (224.18377685546875, 378.4237060546875, 178.60214233398438, 328.1665954589844)),
#     #  (b'bicycle', 0.9933530688285828, (344.39508056640625, 286.08282470703125, 489.40667724609375, 323.8568420410156)),
#     #  (b'truck', 0.9153000116348267, (580.7305908203125, 125.11731719970703, 208.38641357421875, 87.00074768066406))]
#
#     # [(b'bowl', 0.99997878074646, (64.93450927734375, 94.59498596191406, 31.539180755615234, 0.0016200790414586663)), (
#     # b'cell phone', 0.9973439574241638,
#     # (156.6815643310547, 157.23922729492188, 0.035793207585811615, 0.002661647740751505)), (
#     #  b'remote', 0.9973094463348389,
#     #  (156.6815643310547, 157.23922729492188, 0.035793207585811615, 0.002661647740751505)),
#     #  (b'vase', 0.9332147836685181, (156.6815643310547, 157.23922729492188, 0.035793207585811615, 0.002661647740751505)),
#     #  (b'umbrella', 0.8040791153907776, (740.83251953125, 480.33636474609375, 437.53912353515625, 6.066642761230469)),
#     #  (b'umbrella', 0.624094545841217, (741.8377685546875, 490.9327392578125, 374.3318176269531, 5.1523027420043945)),
#     #  (b'umbrella', 0.5078584551811218, (740.283447265625, 470.27667236328125, 340.28070068359375, 6.498147010803223))]
#
#     # [(b'dog', 0.9987696409225464, (224.79208374023438, 376.9918212890625, 179.19064331054688, 321.45953369140625)),
#     #  (b'bicycle', 0.9985112547874451, (343.56170654296875, 284.6434326171875, 479.3537292480469, 343.27337646484375)),
#     #  (b'truck', 0.9498139023780823, (584.6522216796875, 125.15755462646484, 213.15806579589844, 91.28204345703125))]
#
#     print(r)


