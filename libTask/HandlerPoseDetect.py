from libTask.HandlerBase import HandlerBase
import os
from zmqtest.asyncsrv import tprint
from common.error import Error
from zmqServer.zmqMessage import ZmqMessage
from thirdparty.poseUtils.poseUtils import (getModel,getPose)
import numpy as np
import base64
import cv2
import torch
import time
from common import common
from common.log import log

class HandlerPoseDetect(HandlerBase):
    def __init__(self,cp,modelPath="",gpuID:str="0",gpuNums=1):
        super(HandlerPoseDetect, self).__init__()
        self.cp = cp
        self.modelPath = modelPath
        self.gpuID = gpuID
        self.gpuNums=gpuNums
        self.log = log(common.LOG_LEVEL)
        self.setApiKey(cp.api_key)
        self.preDetect(modelPath)


    def handle(self,message:ZmqMessage):

        # USE_LICENSE
        # NOT USE_LICENSE

        return self.poseDetect(message.st,message.timePoint)



    def preDetect(self,modelPath):
        """
        推理前准备：
        1、初始化，加载模型和配置文件
        2、从前的模型转引擎部分可以在这里做
        :param modelPath:项目模型主目录
        :param gpuId:str 算法运行在哪个gpu卡上
        :param gpuNums:暂时未用到
        :return:
        """
        path = os.path.join(modelPath,"pose_detect")
        self.posemodel = os.path.join(path,"hrnet_w32_coco_256x192_udp-aba0be42_20210220.pth")
        self.poseconfig = os.path.join(path,"hrnet_w32_coco_256x192_udp.py")
        # print("posemodel Path is {}".format(self.posemodel))
        # print("pose config Path is {}".format(self.poseconfig))




        self.log.info("pose device init ")
        device = "cuda:"+self.gpuID
        # device = "cpu"
        self.log.info("pose model load start")

        self.model = getModel(self.poseconfig,self.posemodel,device)
        self.log.info("pose model load end")


    def poseDetect(self,request,timePoints):
        """
        功  能：对图片数据进行预处理；对图片检测结果进行汇总

        :param request:图片Mat数据及相关参数
        :param timePoints:时间打点
        :return:返回图片识别结果，耗时和错误信息
        """
        interfaceName = "poseDetect"

        #validate可以直接省略
        responseBody = self.validate(interfaceName,request)


        # self.log.debug("request is : "+str(request))
        request_id = ""

        if "request_id" in request and isinstance(request["request_id"],str):
            request_id = request["request_id"]

        #查看请求结构体是否格式正确
        if responseBody != None:

            responseBody = self.fillResponse(interfaceName,{},request_id,Error.FINDER_PARAMETERS_ERROR)
            return responseBody

        #此处查看请求参数中是否有传入图片的参数
        if "image_base64" not in request or not isinstance(request["image_base64"],str):
            responseBody = self.fillResponse(interfaceName,{},request_id,Error.FINDER_PARAMETERS_ERROR)
            return responseBody

        if len(request["image_base64"]) == 0:
            return self.fillResponse(interfaceName, {}, request_id, Error.FINDER_IMG_NUM_ERROR)


        #TODO:原有的步骤会从base64的图片数据转成cv的mat格式
        #pass


        #返回格式
        res = {}

        #TODO:根据规定的传输格式接收发送数据
        #base64解码
        decode_img = base64.b64decode(bytes(request["image_base64"], encoding='utf-8'))
        #bytes To array
        nparr = np.frombuffer(decode_img, dtype=np.uint8)

        assert nparr.shape[0] != 0,"receive empty image"

        de_start = time.time()
        #decode
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        de_end = time.time()

        torch.cuda.synchronize()
        start = time.time()
        if "person_boxes" not in request:
            h, w, c = img.shape

            x = w / 2
            y = h / 2
            w = w
            h = h
            personBoxes = [[x, y, w, h]]
            ret = getPose(img,personBoxes,self.model)
        else:
            ret = getPose(img,request["person_boxes"],self.model)
        torch.cuda.synchronize()
        end = time.time()
        self.log.debug("pose image decode spend time {}".format(round((de_end-de_start)*1000,4)))
        self.log.debug("pose detect spend time {}".format(round((end-start)*1000,4)))

        # ret = {"test":"sucess"}
        # ret = {"test":"sucess"}
        res["detect_info"] = []
        for i in ret:
            result = {}
            result['pose_info'] =[]
            for j in i:

                result_pose= {}
                result_pose['confidence']=j[2]
                result_pose['x']=j[0]
                result_pose['y']=j[1]
                result['pose_info'].append(result_pose)


            res["detect_info"].append(result)

        # self.log.debug("HandlerposeDetect inference end")
        res = self.fillResponse_(interfaceName,res,request_id,Error.FINDER_POSE_DETECT_SUCCESS,timePoints)
        return res



