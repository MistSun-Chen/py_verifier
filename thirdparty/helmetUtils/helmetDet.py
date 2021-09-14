import os
import cv2
import torch
import numpy as np
from thirdparty.helmetUtils.models.experimental import attempt_load
from thirdparty.helmetUtils.utils.general import check_img_size, non_max_suppression, scale_coords, xyxy2xywh
from thirdparty.helmetUtils.utils.torch_utils import select_device, time_synchronized


def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = img.shape[:2]

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    dw, dh = np.mod(dw, stride), np.mod(dh, stride)
    dw /= 2
    dh /= 2

    if shape[::-1] != new_unpad:
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return img, ratio, (dw, dh)


def getDetection(img,model,device,conf_thres=0.25,iou_thres=0.5):

    names = model.module.names if hasattr(model, 'module') else model.names

    res = []
    imSize = img.shape
    img = letterbox(img, (640, 640), stride=32)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    pred = model(img, augment=False)[0]
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=False)

    for _, det in enumerate(pred):
        gn = torch.tensor(imSize)[[1, 0, 1, 0]]
        if det is not None and len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], imSize).round()
            for *xyxy, conf, cls in reversed(det):
                x, y, w, h = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                res.append([names[int(cls)], float(conf), x, y, w, h])

    detections = []
    for box in res:
        x1, y1, x2, y2 = box[2:]

        x = int(x1 * imSize[1])
        y = int(y1 * imSize[0])
        w = int(x2 * imSize[1])
        h = int(y2 * imSize[0])

        a = int(x - w / 2)
        b = int(y - h / 2)
        c = int(x + w / 2)
        d = int(y + h / 2)

        if a < 10 or b < 10:
            continue
        detections.append([box[0], box[1], a, b, c, d])
    return detections
    pass


def getDetection_(img, helmetModel, conf_thres=0.25, iou_thres=0.5, deviceID='0'):
    '''
    获取图片中人体与安全帽的检测结果
    :param img: cv2读取的图片(RoI方形区域)，如 cv2.imread(imgPath)
    :param helmetModel: 人体安全帽检测模型的文件路径，如 './weights/helmet.pt'
    :param conf_thres: 检测阈值，默认为0.25
    :param iou_thres: IoU阈值，默认为0.5
    :param deviceID: 指定运行的显卡，如 deviceID = 'cpu' or '0' or '0,1,2,3'，默认为0号显卡
    :return: 返回值为图片中人体与安全帽的检测结果，(a,b)为左上角坐标，(c,d)为右下角坐标，如
        [
            ['person', 0.8301451206207275, 691, 40, 866, 385],
            ['helmet', 0.8656536936759949, 743, 45, 814, 104],
            ...
        ]
    '''
    device = select_device(deviceID)
    model = attempt_load(helmetModel, map_location=device)
    return getDetection(img,model,device, conf_thres=conf_thres, iou_thres=iou_thres)
