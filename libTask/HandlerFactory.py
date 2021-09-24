from common import common
from libTask.HandlerHelmetDetect import HandlerHelmetDetect
from libTask.HandlerPoseDetect import HandlerPoseDetect
from libTask.HandlerSmokePhone import HandlerSmokePhone
from libTask.HandlerTrackCoal import HandlerTrackCoal
from zmqtest.asyncsrv import tprint
class HandlerFactory:

    def __init__(self):
        #C++中实现单例模式需要使用的变量，此处可以忽略
        self.factory = 0


    def create(self,handler_id,path,cp,gpu_id:str,gpu_num):
        """
        相当于switch分支选择，根据handler_id选择相应的算法进行实例化
        :param handler_id:
        :param path:
        :param cp:
        :param gpu_id:
        :param gpu_num:
        :return:
        """
        # if handler_id == common.PEOPLESMOKE_METHOD_ID:
        #     #单独抽烟
        #     return HandlerSmokeClassify(cp,path,gpu_id,gpu_num)
        # elif handler_id == common.PEOPLEPHONE_METHOD_ID:
        #     #单独打电话
        #     return HandlerPhoneClassify(cp,path,gpu_id,gpu_num)
        if handler_id == common.SMOKEPHONE_METHOD_ID:
            #抽烟打电话
            return HandlerSmokePhone(cp,path,gpu_id,gpu_num)
        elif handler_id == common.HELMET_METHOD_ID:
            #安全帽
            return HandlerHelmetDetect(cp,path,gpu_id,gpu_num)
        elif handler_id == common.POSE_METHOD_ID:
            #姿态
            return HandlerPoseDetect(cp,path,gpu_id,gpu_num)
        elif handler_id == common.TRACK_COAL_METHOD_ID:
            return HandlerTrackCoal(cp,path,gpu_id,gpu_num)
        elif handler_id == common.COAL_2_METHOD_ID:
            return None
        else: return None







    def instance(self):
        """
        以factory为标准，当他为零时，加互斥锁，创建工厂
        :return:
        """
        pass


handlerFactoryInstance = HandlerFactory()