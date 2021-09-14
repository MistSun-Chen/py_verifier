import sys
import cv2
import os
import darknet
import numpy as np
from poseUtils import (getPose, getModel)


def image_detection(imageOr, network, class_names, class_colors, thresh):
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)
    image_rgb = cv2.cvtColor(imageOr, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height))

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections0 = darknet.detect_image(network, class_names, darknet_image, thresh=thresh, hier_thresh=.5, nms=.4)
    darknet.free_image(darknet_image)
    detections = list()
    t1 = float(imageOr.shape[1]) / float(width)
    t2 = float(imageOr.shape[0]) / float(height)
    t = np.array([t1, t2, t1, t2])
    for i in detections0:
        tempArray = np.asarray(i[2])
        ta = tempArray * t
        detections.append([i[0], i[1], tuple(ta)])
    return detections


def squareImg(img):
    h = img.shape[0]
    w = img.shape[1]
    size = max(h, w)
    square = np.zeros((size, size, 3), np.uint8)
    square[0:h, 0:w] = img[:, :]
    return square


if __name__ == '__main__':
    darknetCfgPath = '/home/guest/lsc/project/mmLab/mmpose/handBicycle/yolov4.cfg'
    darnetWeightPath = '/home/guest/lsc/project/yolov4/darknet/yolov4.weights'
    darknetDataPath = '/home/guest/lsc/project/mmLab/mmpose/handBicycle/coco.data'
    targetClasses = ['person', 'bicycle']
    targetColors = {'person': (255, 0, 0), 'bicycle': (0, 255, 0)}
    boxFrac = 1.3
    thresh = 0.7
    handFrac = 0.6
    bicycleFrac = 0.2
    poseConfig = '/home/guest/lsc/project/mmLab/mmpose/configs/top_down/udp/coco/hrnet_w32_coco_256x192_udp.py'
    checkpoints = '/home/guest/lsc/project/mmLab/mmpose/checkpoints/hrnet_w32_coco_256x192_udp-aba0be42_20210220.pth'

    videoPath = '/home/guest/lsc/data/SanNing/test/video/a0329.mp4'
    savePath = '/home/guest/lsc/project/mmLab/mmpose/poseUtils/vis'
    videoName = os.path.basename(videoPath)
    cap = cv2.VideoCapture(videoPath)
    fps = 5
    size = (1280, 720)
    device = 'cuda:0'


    videowriter = cv2.VideoWriter(os.path.join(savePath, videoName), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)


    network, class_names, class_colors = darknet.load_network(darknetCfgPath, darknetDataPath, darnetWeightPath,
                                                              batch_size=1)
    poseModel = getModel(poseConfig, checkpoints, device)
    cnt=0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cnt+=1
        print(cnt, end='\r')
        imgH = frame.shape[0]
        imgW = frame.shape[1]
        img = frame
        image = squareImg(img)

        yoloDetections = image_detection(image, network, class_names, class_colors, thresh)
        personDetections = []

        for yoloDetection in yoloDetections:
            name, conf, msg = yoloDetection
            if name not in targetClasses:
                continue
            x, y, w, h = msg
            w = min(int(x * 2), int((imgW - x) * 2), int(boxFrac * w))
            h = min(int(y * 2), int((imgH - y) * 2), int(boxFrac * h))
            if name == 'person':
                personDetections.append([x, y, w, h])
        poseRes = getPose(img, personDetections, poseModel)
        for posePoints in poseRes:
            for point in posePoints:
                cv2.circle(img, point, 4, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
        res = cv2.resize(img, size)
        videowriter.write(image)

    cap.release()
    videowriter.release()
