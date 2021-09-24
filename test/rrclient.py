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
import sys
import os


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
    # socket.connect("tcp://192.168.1.4:5559")
    # socket.connect("tcp://192.168.1.4:5562")
    socket.connect("tcp://192.168.1.4:5561")
    # socket.connect("tcp://192.168.1.4:5589")
    # socket.connect("tcp://192.168.1.4:5563")
    # socket.connect("tcp://192.168.1.4:5567")


    # Prepare sending image
    # img = cv2.imread(r"C:\Users\63277\Pictures\car\1.jpg")
    # img = cv2.imread(r'D:\git\py_verifier\thirdparty\poseUtils\test.png')
    # img = cv2.imread(r'/thirdparty/classificationUtils_\test\smoke.jpg')
    # img = cv2.imread(r'D:\git\py_verifier\thirdparty\classificationUtils_\test\phone.jpg')
    # img = cv2.imread(r'D:\git\py_verifier\thirdparty\classificationUtils_\test\smoke.jpg')

    coal_img = []
    for i in range(1,11):
        img = cv2.imread(r"E:\cwy\test\test_{}.jpg".format(i))
        img_encode = cv2.imencode(".jpg",img)[1]
        b64 = str(base64.b64encode(img_encode),encoding='utf-8')
        coal_img.append(b64)

    img = cv2.imread(r'D:\git\py_verifier\thirdparty\helmetUtils\test.jpg')
    # jpg encode
    img_encode = cv2.imencode('.jpg', img)[1]
    #transfer to list
    base_64 = str(base64.b64encode(img_encode),encoding='utf-8')

    # sum the time_used
    sum = 0
    #  Do 10 requests, waiting each time for a response
    for request in range(1, 10000):
        # create json
        req1 = {
            "request_id": str(request),
            "interface": "38",
            "api_key": "",
            # json不认numpy的array
            # "image_base64": ""
            "image_base64": base_64
            # "num":request
        }
        req2 = {
            "request_id": str(request),
            "interface": "40",
            "api_key": "",
            "person_boxes":[[411,441,216,485]],
            # json不认numpy的array
            "image_base64": base_64
            # "image_base64": ""
            # "num":request
        }

        req3 = {
            "request_id": str(request),
            "interface":"42",
            "api_key":"",
            "image_base64":[base_64]
            # "image_base64":[]

        }

        roi_points = [
            [[500, 500], [650, 500], [580, 600], [400, 600]],
            [[1020, 460], [1180, 460], [1330, 525], [1080, 525]]
        ]

        req4 = {
            "request_id": str(request),
            "interface": "43",
            "roi_points":roi_points,
            "api_key": "",
            "threshold":0.04,
            "image_base64": coal_img
        }

        start_time = time.time()
        # sending json str
        socket.send(bytes(json.dumps(req1), encoding="utf-8"))

        # print("sizeof type json {}".format(sys.getsizeof(req1)))
        # print("sizeof type json {}".format(sys.getsizeof("Aa")))
        # socket.send(bytes(json.dumps(req2), encoding="utf-8"))


        # socket.send(bytes(json.dumps(req3), encoding="utf-8"))


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
    socket.connect("tcp://localhost:5561")


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



def send_test():
    Img_base = r'F:\project\sanning'
    img_class_list = ['person_with_smoke','person_without_smoke','person_with_phone','person_without_phone']

    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect("tcp://192.168.1.4:5559")


    for cla in img_class_list:
        Img_dir = os.path.join(Img_base,cla)
        with open(Img_dir+"_package.txt",'a')as f:
            for pic_name in os.listdir(Img_dir):
                pic_path = os.path.join(Img_dir,pic_name)
                img = cv2.imread(pic_path)
                # jpg encode
                img_encode = cv2.imencode('.jpg', img)[1]
                # transfer to list
                base_64 = str(base64.b64encode(img_encode), encoding='utf-8')

                req3 = {
                    "interface": "42",
                    "api_key": "",
                    "image_base64": [base_64]
                    # "image_base64":[]
                }
                socket.send(bytes(json.dumps(req3), encoding="utf-8"))
                rec = socket.recv()
                rec_json = json.loads(str(rec,encoding='utf-8'))
                print(rec_json)
                smoke_res = rec_json["detect_info"][0]["smoke_res"]["type"]
                phone_res = rec_json["detect_info"][0]["phone_res"]["type"]
                #写文件
                line = "{} {} {}\n".format(pic_name,smoke_res,phone_res)
                f.write(line)


def compare(path_1:str,path_2:str):
    with open(path_1,'r')as f:
        lines_1 = f.readlines()
    with open(path_2,'r')as f:
        lines_2 = f.readlines()
    assert len(lines_1) == len(lines_2),"two result not same"
    lines_1.sort()
    lines_2.sort()
    hint = 0
    for i,_ in enumerate(lines_1):
        pic_name_1_1,pic_name_1_2,smoke_type_1,phone_type_1 = lines_1[i].strip().split(" ")
        pic_name_2_1,pic_name_2_2,smoke_type_2,phone_type_2 = lines_2[i].strip().split(" ")
        assert pic_name_1_2 == pic_name_2_2,"two pic_name not same "
        if smoke_type_1 != smoke_type_2 or phone_type_1 != phone_type_2:
            hint+=1
            line = "{} {} {} {} {} {}\n".format(pic_name_1_1,pic_name_1_2,smoke_type_1,phone_type_1,smoke_type_2,phone_type_2)
            with open("error.txt",'a')as f:
                f.write(line)
    return hint,len(lines_1)


def compare_two_file():
    base_path = r'F:\project\sanning'
    cla_list = ['person_with_smoke', 'person_without_smoke', 'person_with_phone', 'person_without_phone']
    for cla in cla_list:
        AI_path = os.path.join(base_path,cla+"_AI.txt")
        package_path = os.path.join(base_path,cla+"_package.txt")
        error_num,sum = compare(AI_path,package_path)
        print("dir:{},error_num:{},sum:{},error_rate{}".format(cla,error_num,sum,round(float(error_num)/float(sum),3)))








if __name__ == '__main__':
    # send_str_bytes()
    # send_list_bytes()
    send_base64_bytes()
    # send_test()
    # compare_two_file()