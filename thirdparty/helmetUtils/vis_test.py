import os
import cv2
from helmetDet import getDetection

img = cv2.imread('test.jpg')
helmetModel = './weight/helmet_model.pt'

print(img)

detections = getDetection(img, helmetModel)
print(detections)

for name,conf,a,b,c,d in detections:
    cv2.rectangle(img, (a, b), (c, d), (255, 0, 0), 2)
    cv2.putText(img, name+str(conf), (a,b), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)

cv2.imwrite('vis.jpg',img)
