from libTask.HandlerBase import HandlerBase
import os
from zmqtest.asyncsrv import tprint
from common.error import Error
from zmqServer.zmqMessage import ZmqMessage
from thirdparty.helmetUtils.helmetDet import getDetection,getDetection_
from thirdparty.helmetUtils.models.experimental import attempt_load
from thirdparty.helmetUtils.utils.torch_utils import select_device
import numpy as np


class HandlerHelmetDetect(HandlerBase):
    def __init__(self,cp,modelPath="",gpuID:str="0",gpuNums=1):
        super(HandlerHelmetDetect, self).__init__()
        self.cp = cp
        self.modelPath = modelPath
        self.gpuID = gpuID
        self.gpuNums=gpuNums

        self.setApiKey(cp.api_key)
        self.preDetect(modelPath,gpuID,gpuNums)


    def handle(self,message:ZmqMessage):

        # USE_LICENSE
        # NOT USE_LICENSE

        return self.helmetDetect(message.st,message.timePoint)



    def preDetect(self,modelPath,gpuId:str,gpuNums):
        """
        推理前准备：
        1、初始化，加载模型和配置文件
        2、从前的模型转引擎部分可以在这里做
        :param modelPath:项目模型主目录
        :param gpuId:str 算法运行在哪个gpu卡上
        :param gpuNums:暂时未用到
        :return:
        """
        path = os.path.join(modelPath,"helmet_detect")
        self.helmetModelPath = os.path.join(path,"helmet_model.pt")
        print("helmentModel Path is {}".format(self.helmetModelPath))

        #TODO:debug cpu model
        # self.device = select_device(gpuId)
        tprint("device start")
        self.device = select_device('cpu')
        tprint("device end")
        tprint("model load start")
        self.model = attempt_load(self.helmetModelPath,self.device)
        tprint("model load end")


    def helmetDetect(self,request,timePoints):
        """
        功  能：对图片数据进行预处理；对图片检测结果进行汇总

        :param request:图片Mat数据及相关参数
        :param timePoints:时间打点
        :return:返回图片识别结果，耗时和错误信息
        """
        tprint("helmetDetect inference begin")
        interfaceName = "helmetDetect"

        #validate可以直接省略
        responseBody,value = self.validate(interfaceName,request)

        tprint("responseBody is : "+str(responseBody))
        tprint("value is : "+str(value))
        request_id = ""

        if "request_id" in value and isinstance(value["request_id"],str):
            request_id = value["request_id"]

        #查看请求结构体是否格式正确
        if responseBody != None:

            responseBody = self.fillResponse(interfaceName,{},request_id,Error.FINDER_PARAMETERS_ERROR)
            return responseBody

        #此处查看请求参数中是否有传入图片的参数
        if "img" not in value or not isinstance(value["img"],list):
            responseBody = self.fillResponse(interfaceName,{},request_id,Error.FINDER_PARAMETERS_ERROR)
            return responseBody


        #TODO:原有的步骤会从base64的图片数据转成cv的mat格式
        #pass


        #返回格式
        res = {}


        #TODO:此处的循环需要把请求里的图片组解析成图片像素的正确格式之后在开始循环，不应该直接使用json中的参数
        img_list = value["img"]
        img = np.array(img_list, dtype=np.uint8)
        assert len(img_list) == 0,"receive empty image"


        if "conf_thres" in value and "iou_thres" in value:

            ret = self.handlerhelmetDetect(img,value["conf_thres"],value["iou_thres"])

        elif "conf_thres" in value:
            ret = self.handlerhelmetDetect(img,value["conf_thres"])

        elif "iou_thres" in value:
            ret = self.handlerhelmetDetect(img,iou_thres=value["iou_thres"])

        else:
            ret = self.handlerhelmetDetect(img)

        # ret = {"test":"sucess"}
        res["detect_info"] = {}
        res["detect_info"] = ret

        tprint("HandlerhelmetDetect inference end")
        res = self.fillResponse_(interfaceName,res,request_id,Error.FINDER_HELMET_DETECT_SUCCESS,timePoints)
        return res




    def handlerhelmetDetect(self,image,conf_thres = 0.25,iou_thres=0.5):
        tprint("HandlerDetect,yolov3 inference begin")

        # return getDetection(image,self.model,self.device,conf_thres=conf_thres,iou_thres=iou_thres)
        return getDetection(image,self.helmetModelPath,'cpu',conf_thres=conf_thres,iou_thres=iou_thres)
        #inference
        # self.validate(interfaceName,request)

        # writeLog
