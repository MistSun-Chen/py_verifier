#
#   Request-reply client in Python
#   Connects REQ socket to tcp://localhost:5559
#   Sends "Hello" to server, expects "World" back
#
import zmq
import cv2
import json
import time
import base64


#transfer pic in 1920*1080 average 164
#Detect Pose average 90ms

def send_list_bytes():
    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")

    # Prepare sending image
    img = cv2.imread(r"/home/oceanai/project/py_verifier/thirdparty/helmetUtils/test.jpg")

    # jpg encode
    img_encode = cv2.imencode('.jpg', img)[1]
    #transfer to list
    img_list = img_encode.tolist()

    # sum the time_used
    sum = 0
    #  Do 10 requests, waiting each time for a response
    for request in range(1, 11):
        # create json
        req = {
            "req": request,
            "interface": "43",
            "api_key": "",
            # json不认numpy的array
            "image_base64": img_list,
            # "num":request
        }
        start_time = time.time()
        # sending json str
        socket.send(bytes(json.dumps(req), encoding="utf-8"))


        print("sending time is {}".format(str(start_time)))
        message = socket.recv()
        print(f"Received reply {request} [{message}]")

        end_time = time.time()
        print(round((end_time - start_time) * 1000, 4))
        sum = sum + (end_time - start_time) * 1000

    print("average is {}".format(sum / 10))

    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")

    # Prepare sending image
    img = cv2.imread(r'C:\Users\63277\Pictures\car\1.jpg')

    # jpg encode
    img_encode = cv2.imencode('.jpg', img)[1]
    #transfer to list
    img_list = img_encode.tolist()

    # sum the time_used
    sum = 0
    #  Do 10 requests, waiting each time for a response
    for request in range(1, 11):
        # create json
        req = {
            "req": request,
            "interface": "43",
            "api_key": "",
            # json不认numpy的array
            "img": img_list,
            # "num":request
        }
        start_time = time.time()
        # sending json str
        socket.send(bytes(json.dumps(req), encoding="utf-8"))


        print("sending time is {}".format(str(start_time)))
        message = socket.recv()
        print(f"Received reply {request} [{message}]")

        end_time = time.time()
        print(round((end_time - start_time) * 1000, 4))
        sum = sum + (end_time - start_time) * 1000

    print("average is {}".format(sum / 10))



def send_base64_bytes():
    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect("tcp://192.168.1.4:5559")

    # Prepare sending image
    img = cv2.imread(r'D:\git\py_verifier\thirdparty\helmetUtils\test.jpg')

    # jpg encode
    img_encode = cv2.imencode('.jpg', img)[1]
    #transfer to list
    base_64 = str(base64.b64encode(img_encode),encoding='utf-8')

    # sum the time_used
    sum = 0
    #  Do 10 requests, waiting each time for a response
    for request in range(1, 11):
        # create json
        req = {
            "request_id": str(request),
            "interface": "38",
            "api_key": "",
            # json不认numpy的array
            "image_base64": base_64
            # "num":request
        }
        start_time = time.time()
        # sending json str
        socket.send(bytes(json.dumps(req), encoding="utf-8"))


        print("sending time is {}".format(str(start_time)))
        message = socket.recv()
        print(f"Received reply {request} [{message}]")

        end_time = time.time()
        print(round((end_time - start_time) * 1000, 4))
        sum = sum + (end_time - start_time) * 1000

    print("average is {}".format(sum / 10))



def send_str_bytes():
    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")


    #Prepare sending image
    img = cv2.imread(r'C:\Users\63277\Pictures\car\1.jpg')

    #jpg encode
    img_encode = cv2.imencode('.jpg', img)[1]

    # transfer to bytes
    img_bytes = img_encode.tobytes()


    print(type(img_bytes))
    # transfer to string
    img_str = bytes.decode(img_bytes,encoding="ascii")

    # print(type(img_encode))
    # print(type(img_encode.tostring()))
    # img_str = img_encode.tostring()
    # print(type(img_str))

    #sum the time_used
    sum = 0
    #  Do 10 requests, waiting each time for a response
    for request in range(1, 11):
        # create json
        req = {
            "req": request,
            "interface": "43",
            "api_key": "",
            # json不认numpy的array
            "img": img_str,
            # "num":request
        }

        #sending json str
        socket.send(bytes(json.dumps(req), encoding="utf-8"))

        start_time = time.time()

        message = socket.recv()
        print(f"Received reply {request} [{message}]")



        end_time = time.time()
        print(round((end_time - start_time) * 1000, 4))
        sum = sum + (end_time - start_time) * 1000

    print("average is {}".format(sum / 10))




if __name__ == '__main__':
    # send_str_bytes()
    # send_list_bytes()
    send_base64_bytes()