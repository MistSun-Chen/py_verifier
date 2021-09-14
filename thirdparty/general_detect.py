from darknet import load_net,load_meta,detect_cv

class GeneralDetector:
    #Load from model
    def __init__(self,net_cfg,weight,meta):
        self.net = load_net(bytes(net_cfg,encoding="utf-8"),bytes(weight,encoding="utf-8"), 0)
        self.meta = load_meta(bytes(meta,encoding="utf-8"))

        pass

    def prepareImage(self,img):
        pass

    def postProcessImage(self,img,detections,threshold):
        pass

    def DoNms(self,detections,nmsThresh):
        pass


    def Detect(self,img,threshold=0.5):
        return detect_cv(self.net,self.meta,img,thresh = threshold,hier_thresh = .5,nms = .45)
