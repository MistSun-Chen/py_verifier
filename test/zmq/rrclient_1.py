#
#   Request-reply client in Python
#   Connects REQ socket to tcp://localhost:5559
#   Sends "Hello" to server, expects "World" back
#
import zmq
import cv2
import json
#  Prepare our context and sockets
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5559")

img = cv2.imread(r'D:\git\py_verifier\pythonProject\data\dog.jpg',1)

#  Do 10 requests, waiting each time for a response
for request in range(1, 11):
    print(img.shape)
    req = {
        "interface":1111,
        "api_key":"",
        #json不认numpy的array
        # "image_base64":img.tolist(),
        "minFaceSize":80,
        "field":"normal",
        "shape":img.shape
        # "num":request
    }
    req = json.dumps(req)
    socket.send(bytes(req,encoding="utf-8"))
    message = socket.recv()
    print(f"Received reply {request} [{message}]")