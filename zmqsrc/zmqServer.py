from libTask.Dispatcher import Dispatcher
from common.configParams import ConfigParams
from zmqSender import ZmqSender
import zmqMessage
import zmq
import json
from common import common
import logging
from common.error import Error
from threading import Thread
from libTask.Queue import DQueue
from libTask import HandlerBase

class ZmqWorker:
    def __init__(self,cp:ConfigParams,dispatcher:Dispatcher,context:zmq.Context):
        """
        负责将收到的zmq消息分发到相应的工作进程中
        :param cp:配置信息
        :param dispatcher:线程调度
        :param context:zmq上下文
        """
        self.cp = cp
        self.dispatcher = dispatcher
        self.context = context

        #TODO:线程是否需要创建就运行
        self.thread = Thread(target=self.run, args=())



        pass

    def fillResponse(self,errorMsg,request_id:str=""):
        response = {}
        response["request_id"] = request_id
        response["error_id"] = errorMsg[0]
        if len(errorMsg[1]) > 0:
            response["error_message"] = errorMsg[1]
        response["time_used"] = 0
        response_s = json.dumps(response)
        return response_s

    def Join(self):
        self.thread.join()



    def run(self):

        #rspSock连接Dealer对应端口
        rspSock = self.context.socket(zmq.DEALER)
        try:
            #zmqAddr为dealer对应ip，可在configParams里进行修改
            rspSock.connect(self.cp.zmqAddr)
        except Exception as e:
            print(e)
            self.context.term()
            return

        #进程内协议通信,套接字类型使用DEALER，绑定进程#1
        rspSockSend = self.context.socket(zmq.DEALER)
        try:
            rspSockSend.bind("inproc://#1")
        except Exception as e:
            print(e)
            self.context.term()
            return

        #创建ZMQ_DEALER类型套接字，连接进程#1进行通信
        self.zmqSender = ZmqSender(self.context,"inproc://#1")

        #使用poller模块接受多种类型套接字的消息
        poller = zmq.Poller()
        poller.register(rspSock)
        poller.register(rspSockSend)
        while True:
            try:
                socks = dict(poller.poll())
            except KeyboardInterrupt:
                break

            if rspSockSend in socks:
                #将进程间消息发送给Router
                message = rspSockSend.recv()
                rspSock.send(message)




            if rspSock in socks:
                #收到Router传来请求，根据格式返回错误，或者继续根据接口ID转发给别的地方

                ident, message = rspSock.recv_multipart()
                # process task
                value = {}
                # 解析从router发送过来的请求,并转成json格式
                try:
                    value = json.loads(str(message))
                except Exception as e:
                    print(e)
                    response = self.fillResponse(Error.ERROR_JSON_SYNTAX)

                    # 将错误消息发送回Router
                    rspSock.send_multipart([ident,bytes(response, encoding="utf-8")])
                    # rspSock.send(bytes(response, encoding="utf-8"))


                if "interface" not in value:
                    # TODO:send request error msg to router
                    response = self.fillResponse(Error.ERROR_JSON_SYNTAX)

                    # 将错误消息发送回Router
                    rspSock.send_multipart([ident, bytes(response, encoding="utf-8")])


                else:
                    interface = int(value["interface"])
                    if interface >= 0 and interface < common.INTERFACEID_COUNT:
                        value_str = str(message)
                        logging.debug("receive the request :" + value_str)

                        """
                        # TODO:Don't Know what for But it only needed by [hover,regioninvade,channeloccupy,itemsteal,itemstrand]
                        channel_id = 0
                        if "camera_channel" in value:
                            channel_id = int(value["camera_channel"])

                        interface_ext = interface

                        if interface == common.INTERFACEID_REGIONINVADE and len(self.cp.crowd_ids["crowd"]) > 0:
                            interface_ext = (channel_id % len(
                                self.cp.crowd_ids["crowd"])) * common.INTERFACEID_REGIONINVADE + interface
                        # 跟摄像头channel有关的，pass
                        """

                        logging.info("worker 1 receive the request json "+ value_str)
                        #封装消息以便放入分发器
                        msg = zmqMessage.ZmqMessage()
                        msg.zmgInit(self.zmqSender.get(),interface,value_str,0,ident)

                        # 分发任务,将格式正确的数据发送给相应的分发器
                        # self.dispatcher.dispatchDq(msg)
                    else:

                        # 获取请求发送过来的request_id
                        request_id = ""
                        if "request_id" in value:
                            request_id = value["request_id"]

                        # 根据错误返回相应消息
                        response = self.fillResponse(Error.FINDER_NOT_INTERFACE_ID, request_id)

                        # 将错误消息发送回Router
                        rspSock.send(bytes(response, encoding="utf-8"))

        rspSock.close()



class ZmqWorker2:
    def __init__(self,cp:ConfigParams,dispatcher:Dispatcher,context:zmq.Context):
        """
        负责将收到的zmq消息分发到相应的工作进程中
        :param cp:配置信息
        :param dispatcher:线程调度
        :param context:zmq上下文
        """
        self.cp = cp
        self.dispatcher = dispatcher
        self.context = context

        # TODO:线程是否需要创建就运行
        self.thread = Thread(target=self.run, args=())


        pass

    def fillResponse(self,errorMsg,request_id:str=""):
        response = {}
        response["request_id"] = request_id
        response["error_id"] = errorMsg[0]
        if len(errorMsg[1]) > 0:
            response["error_message"] = errorMsg[1]
        response["time_used"] = 0
        response_s = json.dumps(response)
        return response_s


    def Join(self):
        self.thread.join()




    def run(self):
        #rspSock连接Dealer对应端口
        rspSock = self.context.socket(zmq.REQ)
        try:
            rspSock.connect(self.cp.zmqAddr2)
        except Exception as e:
            print(e)
            self.context.term()
            return

        #进程内协议通信,绑定
        rspSockSend = self.context.socket(zmq.DEALER)
        try:
            rspSockSend.bind("inproc://#2")
        except Exception as e:
            print(e)
            self.context.term()
            return


        zmqSender = ZmqSender(self.context,"inproc://#2")

        poller = zmq.Poller()
        poller.register(rspSock)
        poller.register(rspSockSend)
        while True:
            try:
                socks = dict(poller.poll())
            except KeyboardInterrupt:
                break

            if rspSockSend in socks:
                #将进程间消息发送给Router
                message = rspSockSend.recv()
                rspSock.send(message)




            if rspSock in socks:
                #收到Router传来请求，根据格式返回错误，或者继续根据接口ID转发给别的地方

                message = rspSock.recv()
                # process task
                value = {}
                # 解析从router发送过来的请求,并转成json格式
                try:
                    value = json.loads(str(message))
                except Exception as e:

                    # 返回json解析错误消息
                    response = self.fillResponse(Error.ERROR_JSON_SYNTAX)
                    rspSock.send(bytes(response, encoding="utf-8"))
                    print(e)

                if "interface" not in value:
                    # TODO:send request error msg to router
                    response = self.fillResponse(Error.FINDER_NOT_INTERFACE_ID)
                    rspSock.send(bytes(response, encoding="utf-8"))
                    pass


                else:
                    interface = int(value["interface"])
                    if interface >= 0 and interface < common.INTERFACEID_COUNT:
                        logging.debug("receive the request :" + json.dumps(value))

                        # 分发任务
                        # self.dispatcher->dispathchDq(msg)
                    else:

                        # 获取请求发送过来的request_id
                        request_id = ""
                        if "request_id" in value:
                            request_id = value["request_id"]

                        # 根据错误返回相应消息
                        response = self.fillResponse(Error.FINDER_NOT_INTERFACE_ID, request_id)

                        # 将错误消息发送回Router
                        rspSock.send(bytes(response, encoding="utf-8"))

        rspSock.close()





class ZmqServer:
    def __init__(self,cp):
        """
        :param cp:配置信息
        """
        self.cp = cp
        self.dispatcher = Dispatcher()
        self.thread = []
        self.thread2 = []
        # self.context = 0

        monitorQueue = DQueue(cp, 1, cp.modelPath, HandlerBase.MONITOR_METHOD_ID, 0)
        self.dispatcher.registerDq(common.INTERFACEID_MONITOR,monitorQueue)
        self.dispatcher.registerDq(common.INTERFACEID_QUERY_SYSTEMINFO,monitorQueue)
        self.dispatcher.registerDq(common.INTERFACEID_QUERY_VERIFIER_VER,monitorQueue)

        #抽烟分发器与抽烟消息队列创建
        if len(cp.smoke_ids) > 0:
            smokeQueue = DQueue(cp, len(cp.smoke_ids), cp.modelPath, HandlerBase.PEOPLESMOKE_METHOD_ID,cp.GPUDevices, cp.smoke_ids)
            self.dispatcher.registerDq(common.INTERFACEID_PEOPLESMOKE,smokeQueue)

        #打电话算法分发器与打电话消息队列创建
        if len(cp.phone_ids) > 0:
            phoneQueue = DQueue(cp, len(cp.phone_ids),cp.modelPath,HandlerBase.PEOPLEPHONE_METHOD_ID,cp.GPUDevices,cp.phone_ids)
            self.dispatcher.registerDq(common.INTERFACEID_PEOPLEPHONE, phoneQueue)

        #安全帽颜色算法分发器与安全帽颜色消息队列创建
        if len(cp.helmet_color_ids) > 0:
            helmetColorQueue = DQueue(cp,len(cp.helmet_color_ids),cp.modelPath,HandlerBase.HELMET_COLOR_METHOD_ID,cp.GPUDevices,cp.helmet_color_ids)
            self.dispatcher.registerDq(common.INTERFACEID_HELMET_COLOR,helmetColorQueue)

        #姿态估计算法分发器与姿态估计消息队列创建
        if len(cp.pose_ids) > 0:
            poseQueue = DQueue(cp,len(cp.pose_ids),cp.modelPath,HandlerBase.POSE_METHOD_ID,cp.GPUDevices,cp.pose_ids)
            self.dispatcher.registerDq(common.INTERFACEID_POSE,poseQueue)

        #人体检测通用方法分发器与其消息队列创建
        if len(cp.detect_general_ids) > 0:
            detectGeneralQueue = DQueue(cp,len(cp.detect_general_ids),cp.modelPath,HandlerBase.GENERALDETECT_METHOD_ID,cp.GPUDevices,cp.detect_general_ids)
            self.dispatcher.registerDq(common.INTERFACEID_DELETE_GENERAL,detectGeneralQueue)

        #断煤场景一分发器与其消息队列创建
        if len(cp.coal_1_ids) > 0:
            coal1Queue = DQueue(cp,len(cp.coal_1_ids),cp.modelPath,HandlerBase.COAL_1_METHOD_ID,cp.GPUDevices,cp.coal_1_ids)
            self.dispatcher.registerDq(common.INTERFACEID_COAL_1,coal1Queue)

        #断煤创景二分发器与其消息队列
        if len(cp.coal_2_ids) > 0:
            coal2Queue = DQueue(cp,len(cp.coal_2_ids),cp.modelPath,HandlerBase.COAL_2_METHOD_ID,cp.GPUDevices,cp.coal_2_ids)
            self.dispatcher.registerDq(common.INTERFACEID_COAL_2, coal2Queue)










    def start(self):
        self.context = zmq.Context.instance()
        self.thread.append(ZmqWorker(self.cp,self.dispatcher,self.context))
        # self.thread2.append(ZmqWorker2(self.cp,self.dispatcher,self.context))
        for thread in self.thread:
            thread.start()



    def shutdown(self):
        self.context.term()
        pass

    def printLog(self,log,flag):
        if flag:
            print(log+" queue load end!")
        else:
            print(log+" queue load start...")
        pass



