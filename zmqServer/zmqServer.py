from libTask.Dispatcher import Dispatcher
from common.configParams import ConfigParams
from zmqServer.zmqSender import ZmqSender
from zmqServer import zmqMessage
import zmq
import json
from common import common
from common.error import Error
from threading import Thread
from libTask.Queue import DQueue
from zmqtest.asyncsrv import tprint
import threading
from common.log import log
from common.common import mylog
import traceback
import time





class ZmqWorker(threading.Thread):
    def __init__(self, cp: ConfigParams, dispatcher: Dispatcher, context: zmq.Context):
        """
        负责将收到的zmq消息分发到相应的工作进程中
        :param cp:配置信息
        :param dispatcher:线程调度
        :param context:zmq上下文
        """
        super().__init__()
        self.cp = cp
        self.dispatcher = dispatcher
        self.context = context
        self.log = log(common.LOG_LEVEL)
        self.start_time = time.time()

        self.request = {common.Interface_dict[i]:0 for i in common.Interface_dict.keys()}




        # #TODO:线程是否需要创建就运行
        # self.thread = Thread(target=self.run, args=())

    def fillResponse(self, errorMsg, request_id: str = ""):
        """
        填充返回消息
        :param errorMsg:错误消息
        :param request_id: 请求id
        :return:在json中添加相应的消息体并转成string类型然后返回
        """
        response = {}
        response["request_id"] = request_id
        response["error_id"] = errorMsg[0]
        if len(errorMsg[1]) > 0:
            response["error_message"] = errorMsg[1]
        response["time_used"] = 0
        response_s = json.dumps(response)
        return response_s

    def run(self):
        """
        主程序的zmq接受消息工作线程
        :return:
        """

        # rspSock连接Dealer对应端口
        rspSock = self.context.socket(zmq.DEALER)
        self.log.info("Zmq Server Worker start to run")
        # tprint("Zmq Server Worker start to run")
        try:
            # zmqAddr为dealer对应ip，可在configParams里进行修改
            rspSock.connect(self.cp.zmqAddr)
        except Exception as e:

            self.log.error(e)
            self.log.error(traceback.format_exc())
            self.context.term()
            return
        self.log.info("Zmq Server Worker complete connection of zmqAddr")
        # tprint("Zmq Server Worker complete connection of zmqAddr")

        # 使用poller模块接受多种类型套接字的消息
        poller = zmq.Poller()
        poller.register(rspSock)
        # poller.register(rspSockSend)


        while True:

            try:
                socks = dict(poller.poll())
            except KeyboardInterrupt:
                break


            self.zmqSender = ZmqSender(self.context, self.cp.zmqAddr)

            if rspSock in socks:
                # 收到Router传来请求，根据格式返回错误，或者继续根据接口ID转发给别的地方

                try:
                    ident, message = rspSock.recv_multipart()
                except ValueError as e:
                    self.log.error(e)
                    continue
                    # self.dispatcher.shutdownDq()
                    # os.kill(os.getpid(), signal.SIGKILL)


                # ident,message = rspSock.recv_multipart()
                self.log.debug("zmqServer Worker receive message")
                # tprint("zmqServer Worker receive message")



                # process task
                value = {}
                # 解析从router发送过来的请求,并转成json格式
                try:
                    value = json.loads(str(message, 'utf-8'))
                except Exception as e:
                    self.log.error(e)
                    # tprint(str(e))
                    response = self.fillResponse(Error.ERROR_JSON_SYNTAX)

                    # 将错误消息发送回Router
                    rspSock.send_multipart([ident, bytes(response, encoding="utf-8")])
                    continue
                    # rspSock.send(bytes(response, encoding="utf-8"))

                if "interface" not in value:
                    # TODO:send request error msg to router
                    response = self.fillResponse(Error.ERROR_JSON_SYNTAX)

                    # 将错误消息发送回Router
                    rspSock.send_multipart([ident, bytes(response, encoding="utf-8")])




                else:
                    #此处接收到正确的interface编号，
                    interface = int(value["interface"])
                    if interface >= 0 and interface < common.INTERFACEID_COUNT:
                        if interface not in common.Interface_dict.keys():
                            mylog.error("receive interface not deployed")
                            response = self.fillResponse(Error.FINDER_PARAMETERS_ERROR)
                            rspSock.send_multipart([ident, bytes(response, encoding="utf-8")])
                            continue

                        # 封装消息以便放入分发器
                        msg = zmqMessage.ZmqMessage()
                        msg.zmgInit(self.zmqSender, interface, value, 0, ident)

                        # tprint("zmqServer Worker complete zmqMessage Init")





                        #消息进队列，相应的工作线程开始工作
                        self.dispatcher.dispatchDq(msg)

                        end_time = time.time()
                        if end_time - self.start_time < 60:
                            self.request[common.Interface_dict[interface]] += 1
                        else:
                            self.start_time = time.time()
                            self.log.info("*" * 30)
                            self.log.info(self.request)
                            self.log.info("*" * 30)
                            self.request = {common.Interface_dict[i]: 0 for i in common.Interface_dict.keys()}






                    else:
                        #interface 不正确返回错误消息

                        # 获取请求发送过来的request_id
                        request_id = ""
                        if "request_id" in value:
                            request_id = value["request_id"]

                        # 根据错误返回相应消息
                        response = self.fillResponse(Error.FINDER_NOT_INTERFACE_ID, request_id)

                        # 将错误消息发送回Router
                        rspSock.send_multipart([ident,bytes(response, encoding="utf-8")])

        rspSock.close()




class ZmqServer:
    def __init__(self, cp):
        """
        :param cp:配置信息
        """
        self.cp = cp
        self.dispatcher = Dispatcher()
        self.thread = []

        # self.thread2 = []
        # self.context = 0

        # 监控性能功能暂时不用
        # monitorQueue = DQueue(cp, 1, cp.modelPath, HandlerBase.MONITOR_METHOD_ID, 0)
        # self.dispatcher.registerDq(common.INTERFACEID_MONITOR,monitorQueue)
        # self.dispatcher.registerDq(common.INTERFACEID_QUERY_SYSTEMINFO,monitorQueue)
        # self.dispatcher.registerDq(common.INTERFACEID_QUERY_VERIFIER_VER,monitorQueue)

        #抽烟打电话合并算法消息队列创建
        if len(cp.smoke_phone_ids) > 0:
            smokephoneQueue = DQueue(cp, len(cp.smoke_phone_ids), cp.modelPath, common.SMOKEPHONE_METHOD_ID,
                                cp.smoke_phone_ids, cp.GPUDevices)
            mylog.info("create smoke&phone DQueue")
            # tprint("create smoke&phone DQueue")
            self.dispatcher.registerDq(common.INTERFACEID_SMOKEPHONE, smokephoneQueue)
            mylog.info("create dispatcher smoke&phone")
            # tprint("create dispatcher smoke")


        # #抽烟分发器与抽烟消息队列创建
        # if len(cp.smoke_ids) > 0:
        #     smokeQueue = DQueue(cp, len(cp.smoke_ids), cp.modelPath, common.PEOPLESMOKE_METHOD_ID,
        #                         cp.smoke_ids, cp.GPUDevices)
        #     tprint("create smoke DQueue")
        #     self.dispatcher.registerDq(common.INTERFACEID_PEOPLESMOKE, smokeQueue)
        #     tprint("create dispatcher smoke")
        #
        # #打电话算法分发器与打电话消息队列创建
        # if len(cp.phone_ids) > 0:
        #     phoneQueue = DQueue(cp, len(cp.phone_ids), cp.modelPath, common.PEOPLEPHONE_METHOD_ID,
        #                         cp.phone_ids, cp.GPUDevices)
        #     self.dispatcher.registerDq(common.INTERFACEID_PEOPLEPHONE, phoneQueue)
        #     tprint("create dispatcher phone")

        #安全帽算法分发器与安全帽颜色消息队列创建
        if len(cp.helmet_ids) > 0:
            helmetQueue = DQueue(cp, len(cp.helmet_ids), cp.modelPath, common.HELMET_METHOD_ID,
                                 cp.helmet_ids, cp.GPUDevices)
            self.dispatcher.registerDq(common.INTERFACEID_HELMET, helmetQueue)
            mylog.info("create dispatcher helmet")

        #姿态估计算法分发器与姿态估计消息队列创建
        # tprint("len pose_id is "+ str(len(cp.pose_ids)))
        if len(cp.pose_ids) > 0:
            poseQueue = DQueue(cp, len(cp.pose_ids), cp.modelPath, common.POSE_METHOD_ID, cp.pose_ids,cp.GPUDevices)
            self.dispatcher.registerDq(common.INTERFACEID_POSE, poseQueue)
            mylog.info("create dispatcher pose")

        # 人体检测通用方法分发器与其消息队列创建
        # if len(cp.detect_general_ids) > 0:
        #     detectGeneralQueue = DQueue(cp, len(cp.detect_general_ids), cp.modelPath, common.GENERALDETECT_METHOD_ID, cp.detect_general_ids,
        #                                 cp.GPUDevices)
        #     self.dispatcher.registerDq(common.INTERFACEID_DELETE_GENERAL, detectGeneralQueue)

        # 履带断煤分发器与其消息队列创建
        if len(cp.track_coal_ids) > 0:
            trackcoalQueue = DQueue(cp, len(cp.track_coal_ids), cp.modelPath, common.TRACK_COAL_METHOD_ID,
                                cp.track_coal_ids, cp.GPUDevices)
            self.dispatcher.registerDq(common.INTERFACEID_TRACK_COAL, trackcoalQueue)
            mylog.info("create dispatcher track coal")

        # 断煤创景二分发器与其消息队列
        # if len(cp.coal_2_ids) > 0:
        #     coal2Queue = DQueue(cp, len(cp.coal_2_ids), cp.modelPath, common.COAL_2_METHOD_ID,
        #                         cp.coal_2_ids, cp.GPUDevices)
        #     self.dispatcher.registerDq(common.INTERFACEID_COAL_2, coal2Queue)

    def start(self):
        self.context = zmq.Context.instance()
        for i in range(1):
            mylog.info("ZmqWorker Thread init start ")
            thread = ZmqWorker(self.cp, self.dispatcher, self.context)
            mylog.info("ZmqWorker Thread  init end")
            self.thread.append(thread)
            thread.start()


    def shutdown(self):
        self.context.term()
        pass



