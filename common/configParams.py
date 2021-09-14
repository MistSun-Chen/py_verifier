import os
class ConfigParams:
    def __init__(self,configPath):
        #权限验证
        self.api_key = ""

        userID = ""
        ip = "0.0.0.0"

        #模型相关存放根目录
        self.modelPath = os.path.join(os.getcwd(),"model")

        cpuCores = 0
        threads = 2
        port = 33388
        batchSize = 10
        #每个算法使用的GPU数量
        self.GPUDevices = 1

        topK = 80
        featureSize = 512

        zmqthreads = 2

        self.CPU = 0
        self.zmqAddr = "tcp://127.0.0.1:5561"
        self.zmqAddr2 = "tcp://*:5050"

        zmqAddr2 = "tcp://*:5050"

        self.smoke_ids = [0]
        self.phone_ids = [0]
        self.helmet_ids = [1]
        self.detect_general_ids = [1]
        self.pose_ids = [1]
        self.coal_1_ids = [0]
        self.coal_2_ids = [0]


    def loadConfig(self,configPath):
        pass
    def generateDefaultConfig(self,configPath):
        pass

    def initEasylogging(self,logConfig):
        pass
    def printParams(self):
        print("run configParams function printParams")
        pass
