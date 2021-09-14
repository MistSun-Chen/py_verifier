import json
import cv2
import numpy as np
import time
if __name__ == '__main__':

    # # img = cv2.imread(r"D:\git\py_verifier\test\test.jpg")
    # img = cv2.imread(r"D:\git\verifier\test\data\dog.jpg")
    # print(img.shape)
    # # height,width,channel
    # img_list = img.tolist()
    # #BGR
    #
    # newimg = np.array(img_list,dtype=np.uint8)
    #
    # cv2.imshow("test.jpg",newimg)
    #
    # cv2.waitKey()

    # result = b'{"req": 1, "interface": 0, "api_key": "", "minFaceSize": 80, "field": "normal", "shape": [224, 224, 3]}'
    # str_result = str(result,'utf-8')
    # print(json.loads(str_result))

    start_time = time.time()

    time.sleep(1)

    end_time = time.time()
    print(end_time-start_time)
