from libTask.HandlerBase import HandlerBase
import os
from zmqtest.asyncsrv import tprint
from common.error import Error
# from thirdparty.general_detect import GeneralDetector
from zmqServer.zmqMessage import ZmqMessage
import base64
import cv2
import torch
import time

class HandlerGeneralDetect(HandlerBase):
    def __init__(self,cp,modelPath="",gpuID:str="0",gpuNums=1):
        super(HandlerGeneralDetect, self).__init__()
        self.cp = cp
        self.modelPath = modelPath
        self.gpuID = gpuID
        self.gpuNums=gpuNums

        self.setApiKey(cp.api_key)


    def handle(self,message:ZmqMessage):

        # USE_LICENSE
        # NOT USE_LICENSE

        return self.generalDetect(message.st,message.timePoint)



    def preDetect(self,modelPath,cp,gpuId,gpuNums):
        """
        推理前准备：
        1、初始化，加载模型和配置文件
        2、从前的模型转引擎部分可以在这里做
        :param modelPath:项目模型主目录
        :param cp:配置参数
        :param gpuId:
        :param gpuNums:
        :return:
        """
        path = os.path.join(modelPath,"general_detect")
        net_cfg = os.path.join(path,"yolov3.cfg")
        weight = os.path.join(path,"yolov3.weight")
        meta = os.path.join(path,"coco.data")
        # self.generaldetector = GeneralDetector(net_cfg,weight,meta)





        pass


    def generalDetect(self,request,timePoints):
        """
        功  能：对图片数据进行预处理；对图片检测结果进行汇总

        :param request:图片Mat数据及相关参数
        :param timePoints:时间打点
        :return:返回图片识别结果，耗时和错误信息
        """
        # tprint("HandlerGeneralDetect,yolov3 inference begin")
        interfaceName = "yolov3GeneralDetect"

        #validate或许可以直接省略
        responseBody = self.validate(interfaceName,request)

        # tprint("responseBody is : "+str(responseBody))
        # tprint("request is : "+str(request))
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


        #TODO:原有的步骤会从base64的图片数据转成cv的mat格式
        #pass


        #返回格式
        res = {}

        index = 0
        #TODO:此处的循环需要把请求里的图片组解析成图片像素的正确格式之后在开始循环，不应该直接使用json中的参数
        img = request["image_base64"]

        # tprint("receive the request img : {}".format(str(img)))
        ret = {}
        if "threshold" in request:
            threshold = request["threshold"]
            # ret = self.handlerGeneralDetect(img,threshold)
        else:

            # ret = self.handlerGeneralDetect(img)
            pass

        ret = {"test":"sucess"}
        res["detect_info"] = ret


        # tprint("HandlerGeneralDetect,yolov3 inference end")
        res = self.fillResponse_(interfaceName,res,request_id,Error.FINDER_GENERAL_DETECT_SUCCESS,timePoints)
        # res = self.fillResponse(interfaceName,res,request_id,Error.FINDER_CARCARD_DETECT_SUCCESS)
        return res


    # def handlerGeneralDetect(self,image,threshold = 0.7):
    #     tprint("HandlerDetect,yolov3 inference begin")
    #     interfaceName = "yolov3"
    #
    #
    #
    #     result = {"Debug Program"}
    #
    #     # result = self.generaldetector.Detect(image,threshold)
    #
    #
    #     return result
    #     #inference
    #     # self.validate(interfaceName,request)
    #
    #     # writeLog
