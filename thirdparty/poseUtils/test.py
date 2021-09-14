from poseUtils import (getPose, getModel)
import cv2
import time
import torch

#Detect average 90ms

if __name__ == '__main__':
    poseConfig = r'/home/oceanai/project/py_verifier/thirdparty/poseUtils/weight/hrnet_w32_coco_256x192_udp.py'
    checkpoints = r'/home/oceanai/project/py_verifier/thirdparty/poseUtils/weight/hrnet_w32_coco_256x192_udp-aba0be42_20210220.pth'
    device = r'cuda:1'
    poseModel = getModel(poseConfig, checkpoints, device)
    img = cv2.imread(r'/home/oceanai/project/py_verifier/thirdparty/poseUtils/test.png')
    h,w,c = img.shape

    x = w /2
    y = h /2
    w =w
    h = h

    
    print(img.shape)
    sum = 0
    personDetections = [[x,y,w,h]]
    for i in range(10):
        torch.cuda.synchronize()
        start = time.time()
        poseRes = getPose(img, personDetections, poseModel)
        torch.cuda.synchronize()
        end = time.time()
        print("spend time {}".format(str((end-start)*1000)))
        sum = sum + (end-start)*1000
        print("result is {}".format(str(poseRes)))
    print("average is "+str(sum/10))
    for posePoints in poseRes:
        for point in posePoints:
            cv2.circle(img, point, 4, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

    cv2.imwrite("result.png",img)