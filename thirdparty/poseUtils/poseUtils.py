import sys
import cv2
import os
import numpy as np
import warnings
# from deprecated.sphinx import deprecated
from mmpose.apis import (init_pose_model, inference_top_down_pose_model)

warnings.filterwarnings('always')


def getModel(poseConfig, checkpoints, device='cuda:0'):
    '''生成姿态估计模型
    :param poseConfig: 姿态估计模型的配置文件
    :param checkpoints: 姿态估计模型文件
    :param device: 指定运行在哪张显卡上，默认为0号显卡
    :return: 返回姿态估计模型
    '''
    print(poseConfig)
    return init_pose_model(poseConfig, checkpoints, device=device)


# @deprecated(version='0.0.1', reason='此方法只适用测试单张图片，将会被弃用')
# def getPose(img, personBoxes, poseConfig, checkpoints, device='cuda:0'):
#     '''获取图片中所有人的姿态信息
#     :param img: cv2读取的图片，如 cv2.imread(imgPath)
#     :param personBoxes: 图片中所有的的人体框，如：
#     [
#         [cx, cy, w, h],
#         [cx, cy, w, h],
#         ...
#     ]
#     :param poseConfig:姿态估计模型的配置文件
#     :param checkpoints:姿态估计模型文件
#     :param device:指定运行在哪张显卡上，默认为0号显卡
#     :return: 返回值是图中所有人的对应人体关键点信息，人体关键点信息的顺序按照personBoxes中的人体顺序，如：
#     [
#
#         [(x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y)],
#         [(x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y)],
#         [(x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y)],
#         ...
#     ]
#     '''
#     poseModel = init_pose_model(poseConfig, checkpoints, device=device)
#     dataset = poseModel.cfg.data['test']['type']
#     res = []
#     for personBox in personBoxes:
#         cx, cy, w, h = personBox
#         x = max(0, int(cx - w / 2))
#         y = max(0, int(cy - h / 2))
#         personImg = img[y:y + h, x:x + w]
#         personResults = [{'bbox': np.array([0, 0, w, h])}]
#         poseResults, returnedOutputs = inference_top_down_pose_model(
#             poseModel,
#             personImg,
#             personResults,
#             format='xyxy',
#             dataset=dataset,
#             return_heatmap=False,
#             outputs=None
#         )
#         if len(poseResults) == 0:
#             res.append([])
#             continue
#         detPoints = poseResults[0]['keypoints'].tolist()
#         points = []
#         for detPoint in detPoints:
#             px, py, pc = detPoint
#             px = int(px)
#             py = int(py)
#             pc = int(pc)
#             if (px == 0 and py == 0) or (px < 0 or py < 0):
#                 points.append(None)
#             else:
#                 points.append((px + x, py + y))
#         res.append(points)
#     return res


def getPose(img, personBoxes, poseModel):
    '''获取图片中所有人的姿态信息。相比于之前的版本的getPose函数，这个版本将模型的创建解耦，方便多次测试

    :param img: cv2读取的图片，如 cv2.imread(imgPath)
    :param personBoxes:
    :param poseModel: 图片中所有的的人体框，如：
    [
        [cx, cy, w, h],
        [cx, cy, w, h],
        ...
    ]
    :return: 返回值是图中所有人的对应人体关键点信息，人体关键点信息的顺序按照personBoxes中的人体顺序，如：
    [

        [(x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y)],
        [(x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y)],
        [(x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y), (x,y)],
        ...
    ]
    '''
    dataset = poseModel.cfg.data['test']['type']
    res = []
    for personBox in personBoxes:
        cx, cy, w, h = personBox
        x = max(0, int(cx - w / 2))
        y = max(0, int(cy - h / 2))
        personImg = img[y:y + h, x:x + w]
        personResults = [{'bbox': np.array([0, 0, w, h])}]
        poseResults, returnedOutputs = inference_top_down_pose_model(
            poseModel,
            personImg,
            personResults,
            format='xyxy',
            dataset=dataset,
            return_heatmap=False,
            outputs=None
        )
        if len(poseResults) == 0:
            res.append([])
            continue
        detPoints = poseResults[0]['keypoints'].tolist()
        points = []
        for detPoint in detPoints:
            px, py, pc = detPoint
            px = int(px)
            py = int(py)
            pc = int(pc)
            if (px == 0 and py == 0) or (px < 0 or py < 0):
                points.append(None)
            else:
                points.append((px + x, py + y))
        res.append(points)
    return res
