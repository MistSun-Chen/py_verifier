#
#   Request-reply client in Python
#   Connects REQ socket to tcp://localhost:5559
#   Sends "Hello" to server, expects "World" back
#
import zmq
import cv2
import json
import time


def main():
    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect("tcp://192.168.1.4:5559")
    #h,w,c
    # image = cv2.imread(r"D:\git\py_verifier\thirdparty\poseUtils\test.png")
    image = cv2.imread(r"D:\git\py_verifier\thirdparty\helmetUtils\test.jpg")
    image_list = image.tolist()
    #  Do 10 requests, waiting each time for a response
    sum = 0
    for request in range(1, 11):
        req = {
            "img":image_list,
            "request_id":str(request),
            "personBoxes":[[49.0, 126.0, 98, 252]],
            "interface":"40",
            "api_key":"",
            #json不认numpy的array
            # "image_base64":img.tolist(),
            "minFaceSize":80,
            "field":"normal"
            # "num":request
        }
        req = json.dumps(req)
        socket.send(bytes(req,encoding="utf-8"))
        message = socket.recv()
        print(f"Received reply {request} [{message}]")
        message = json.loads(str(message,"utf-8"))
        sum = sum + message["time_used"]
    print("average time is "+str(sum/10))


if __name__ == '__main__':
    main()