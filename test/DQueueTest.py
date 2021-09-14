from libTask import Queue
from common import configParams
from common import common
def main():
    cp = configParams.ConfigParams("config.json")
    detectGeneralQueue = Queue.DQueue(cp, len(cp.detect_general_ids), cp.modelPath, common.GENERALDETECT_METHOD_ID,
                                cp.GPUDevices, cp.detect_general_ids)
    print("Run Into Next step")
    smokeQueue = Queue.DQueue(cp, len(cp.smoke_ids), cp.modelPath, common.PEOPLESMOKE_METHOD_ID,cp.GPUDevices, cp.smoke_ids)




if __name__ == '__main__':
    main()