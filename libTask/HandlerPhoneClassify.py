from libTask.HandlerBase import HandlerBase
import os
from zmqtest.asyncsrv import tprint
from common.error import Error
from zmqServer.zmqMessage import ZmqMessage
from thirdparty.classificationUtils.classificationUtils import (getModel,getPredict)
import numpy as np
import base64
import cv2
import torch
import time
from PIL import Image

class HandlerPhoneClassify(HandlerBase):
    def __init__(self,cp,modelPath="",gpuID:str="0",gpuNums=1):
        super(HandlerPhoneClassify, self).__init__()
        self.cp = cp
        self.modelPath = modelPath
        self.gpuID = gpuID
        self.gpuNums=gpuNums

        self.setApiKey(cp.api_key)
        self.preDetect(modelPath)


    def handle(self,message:ZmqMessage):

        #TODO USE_LICENSE
        
        #TODO NOT USE_LICENSE

        return self.phoneClassify(message.st,message.timePoint)



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
        path = os.path.join(modelPath,"phone_class")
        self.phoneModelPath = os.path.join(path,"phone_resnet_304.pth")
        # print("phoneModelPath Path is {}".format(self.helmetModelPath))

        #TODO:debug cpu model
        # self.device = select_device('cpu')

        self.metaPath = os.path.join(path,'phone_classIndices.json')

        tprint("phone model device init ")

        if self.gpuID != "cpu":
            self.device = "cuda:"+self.gpuID
        else:
            self.device = "cpu"


        tprint("phone model load start")
        self.model = getModel(2,self.phoneModelPath,self.device)
        tprint("phone model load end")


    def phoneClassify(self,request,timePoints):
        """
        功  能：对图片数据进行预处理；对图片检测结果进行汇总

        :param request:图片Mat数据及相关参数
        :param timePoints:时间打点
        :return:返回图片识别结果，耗时和错误信息
        """

        interfaceName = "phoneClassify"

        #validate可以直接省略
        responseBody = self.validate(interfaceName,request)

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


        #TODO:根据规定的传输格式接收发送数据
        #base64解码
        decode_img = base64.b64decode(bytes(request["image_base64"], encoding='utf-8'))
        #bytes To array
        nparr = np.frombuffer(decode_img, dtype=np.uint8)

        assert nparr.shape[0] != 0,"receive empty image"

        #decode
        img_BGR = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


        #transfer BGR to RGB
        img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img_RGB)




        torch.cuda.synchronize()
        start = time.time()

        # XXX
        ret = getPredict(img, self.metaPath, self.model, device=self.device)

        torch.cuda.synchronize()
        end  = time.time()
        tprint("phone classify spend time {}".format(round((end-start)*1000,4)))

        res = {}


        res["detect_info"]={
            "type":ret[0],
            "accuracy":ret[1]
        }

        # tprint("HandlerhelmetDetect inference end")
        res = self.fillResponse_(interfaceName,res,request_id,Error.FINDER_PEOPLEPHONE_CLASSIFY_SUCCESS,timePoints)
        return res

