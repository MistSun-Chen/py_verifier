import time
class ZmqMessage:
    def __init__(self):
        self.timePoint = []


    def zmgInit_empty(self):
        self.makeTimePoint()


    def zmgInit(self,zmqSender,msgType,st,flags,addr):
        self.zmqSender = zmqSender
        self.msgType = msgType
        self.st = st
        self.flags = flags
        self.addr = addr
        self.makeTimePoint()

    def zmgSet(self,msg):
        self.addr = msg.addr
        self.st = msg.st
        self.msgType = msg.msgType
        self.zmqSender = msg.zmqSender
        self.response = msg.response
        self.timePoint = msg.timePoint

    def call(self,response):
        self.response = response
        self.zmqSender.push(self)


    def makeTimePoint(self):
        self.timePoint.append(time.time())

