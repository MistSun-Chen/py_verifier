#
#   Request-reply service in Python
#   Connects REP socket to tcp://localhost:5560
#   Expects "Hello" from client, replies with "World"
#
import time
import zmq
import json
import cv2
import numpy as np
import base64


def receive_str_bytes():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:5560")

    while True:
        message = socket.recv()

        message = str(message, 'utf-8')
        # print(message)
        message = json.loads(message)


        # cv2_list = message["img"]
        # img = np.array(cv2_list, dtype=np.uint8)
        # img_decode = cv2.imdecode(img,cv2.IMREAD_COLOR)

        img_bytes = str.encode(message["img"])

        nparr = np.frombuffer(img_bytes, dtype=np.uint8)

        img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # print(f"Received request: {message}")
        print(f"Received request: 111")
        socket.send(b"00000")

def receive_base64_bytes():
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect("tcp://localhost:5560")

    while True:


        indent,message = socket.recv_multipart()
        start_time = time.time()
        print("receive the request time {}".format(str(start_time)))

        message = str(message, 'utf-8')
        byToString = time.time()
        print("transfer bytes to string {}".format(round((byToString - start_time) * 1000, 4)))
        # print(message)
        message = json.loads(message)

        strloadjson = time.time()
        print("transfer string to json {}".format(round((strloadjson - byToString) * 1000, 4)))

        # cv2_list = message["img"]
        # img = np.array(cv2_list, dtype=np.uint8)
        # img_decode = cv2.imdecode(img,cv2.IMREAD_COLOR)

        decode_img = base64.b64decode(bytes(message["img"],encoding='utf-8'))

        listToarray = time.time()
        print("transfer base64 to buffer {}".format(round((listToarray - strloadjson) * 1000, 4)))

        nparr = np.frombuffer(decode_img, dtype=np.uint8)
        buffToarray = time.time()
        print("transfer buffer to array {}".format(round((buffToarray - listToarray) * 1000, 4)))

        img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        decodetime = time.time()

        print("img_decode spend {}".format(round((decodetime - buffToarray) * 1000, 4)))

        # print(f"Received request: {message}")
        print(f"Received request: 111")
        print(img_decode.shape)
        # cv2.imwrite(str(message["req"]) + '.jpg', img_decode)
        print("save in "+str(message["req"]) + '.jpg')
        socket.send_multipart([indent, b"00000"])


def receive_list_bytes():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:5560")

    while True:

        message = socket.recv()
        start_time = time.time()
        print("receive the request time {}".format(str(start_time)))

        message = str(message, 'utf-8')
        byToString = time.time()
        print("transfer bytes to string {}".format(round((byToString - start_time) * 1000, 4)))
        # print(message)
        message = json.loads(message)

        strloadjson = time.time()
        print("transfer string to json {}".format(round((strloadjson - byToString) * 1000, 4)))

        # cv2_list = message["img"]
        # img = np.array(cv2_list, dtype=np.uint8)
        # img_decode = cv2.imdecode(img,cv2.IMREAD_COLOR)

        nparr = np.array(message["img"],dtype=np.uint8)
        listToarray = time.time()
        print("transfer list to array {}".format(round((listToarray - strloadjson) * 1000, 4)))

        img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        decodetime = time.time()
        print("img_decode spend {}".format(round((decodetime - listToarray) * 1000, 4)))

        # print(f"Received request: {message}")
        print(f"Received request: 111")
        socket.send(b"00000")


if __name__ == '__main__':

    # receive_str_bytes()
    # receive_list_bytes()
    receive_base64_bytes()