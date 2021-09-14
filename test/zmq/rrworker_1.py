#
#   Request-reply service in Python
#   Connects REP socket to tcp://localhost:5560
#   Expects "Hello" from client, replies with "World"
#
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5560")

while True:
    message = socket.recv()
    message = str(message,'utf-8')
    print(message)
    json_meg = json.loads(message)
    # print(len(json_meg["shape"]))


    # for key in json_meg:
    #     print("key: "+str(key)+",value "+ str(json_meg[key]))

    # print(f"Received request: {str(message,'utf-8')}")
    socket.send(b"111111")