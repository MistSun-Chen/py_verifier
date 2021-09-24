from common.configParams import ConfigParams
from common import common
from common.log import log
import queue
from threading import Thread
from libTask.HandlerFactory import handlerFactoryInstance
# from libTask.HandlerFactory import HandlerFactory
from zmqtest.asyncsrv import tprint
import zmq
import traceback

class Worker(Thread):
    def __init__(self, queue, gpu_id, gpu_num, handler_id, model_path, cp):
        super().__init__()
        self.queue = queue
        self.gpu_id = gpu_id
        self.gpu_num = gpu_num
        self.handler_id = handler_id
        self.model_path = model_path
        self.status = True
        self.cp = cp
        self.log = log(common.LOG_LEVEL)



    def run(self):
        if self.cp.CPU == 1:
            self.log.info("Worker::Run CPU")
            #TODO:之前此处设置caffe的CPU工作模式
        else:
            self.log.info("Worker::Run GPU {}".format(str(self.gpu_id)))
            #TODO：之前此处设置caffe的GPU工作模式，并根据gpu_id数加载模型

        # handlerFactoryInstance = HandlerFactory()
        handler = handlerFactoryInstance.create(self.handler_id,self.model_path,self.cp,str(self.gpu_id),self.gpu_num)
        if handler is None:
            return

        while self.status:
            try:
                message = self.queue.get(60)
                if message:
                    response = handler.handle(message)
                    # tprint("handler response is {}".format(str(response)))
                    # tprint("ending queue handle")
                    self.log.debug("zmqServer start sending result message")

                    socket = message.zmqSender.context.socket(zmq.DEALER)
                    # tprint("end create socket ")
                    socket.connect(message.zmqSender.zmqAddr)
                    # tprint("end connect message")
                    socket.send_multipart([message.addr, bytes(response, encoding="utf-8")])
                    # tprint("end sending")
                    #此处必须加close()

                    self.log.debug("zmqServer complete sending result message")
                    socket.close()


                    #原有步骤进队列
                    # message.call(response)

                    #更改成直接发送回去


            except queue.Empty:
                # tprint("{} dispatcher queue empty ".format(self.handler_id))
                continue

            # if self.queue.get(message





class DQueue:
    def __init__(self,cp:ConfigParams,worker_count:int,model_path:str,handler_id:int,gpus:list,gpu_num:str='0'):
        self.status = True
        self.threads = []
        self.msg_list = queue.Queue(maxsize=1000)
        self.worker_count = worker_count
        self.gpus = gpus
        self.gpu_num = gpu_num
        self.handler_id = handler_id
        self.cp = cp
        self.model_path = model_path
        self.log = log(common.LOG_LEVEL)
        try:
            for i in range(self.worker_count):
                # TODO:此处原来依靠caffe模块检测GPU设备是否可用，输出不可用GPU编号
                # 对于不可用gpu直接continue
                # 对于可用gpu，我们new

                self.log.info("worker_count : {}/{}".format(i, self.worker_count - 1))
                worker = Worker(self.msg_list, self.gpus[i], self.gpu_num, self.handler_id, self.model_path, self.cp)
                worker.start()
                self.log.info("Dispatcher Num {} worker thread start  ".format(self.handler_id))
                self.threads.append(worker)

        except Exception as e:
            self.log.error("Thread init failed!")
            self.log.error(e)
            self.log.error(traceback.format_exc())
            



    def push(self,message):
        #消息进队列
        self.msg_list.put(message)

        #查看当前消息队列中的消息数量，数量挤压太多显然不正常
        if self.msg_list.qsize() >= 100:
            self.log.error("There are already over 100 requests in {} Queue".format(common.Handl_dict[self.handler_id]))
        elif self.msg_list.qsize() >= 20:
            self.log.warning("There are already over 20 requests in {} Queue".format(common.Handl_dict[self.handler_id]))



        return 0


    def get(self):
        if self.status == False:
            return None

        if self.msg_list.qsize() == 0:
            return None
        message = self.msg_list.get()
        return message


    def shutdown(self):
        self.status = False
        for i in self.threads:
            if i is not None:
                i.status = False


        pass

class BQueue:
    def __init__(self,work_count:int,model_path:str,handler_id:int,gpu_num:int=0,capacity:int=0):
        self.capacity = capacity
        self.queue = []
        self.threads = []

        try:
            for i in range(work_count):
                self.threads.append(Worker(self,i % gpu_num if gpu_num > 1 else 0,gpu_num,handler_id,model_path))
        except Exception as e:
            tprint("Thread init failed!")
            tprint(e)

        pass

    def push(self):

        pass

    def get(self):

        pass

    def getNow(self,msg):
        pass

    def shutdown(self):
        for i in self.threads:
            if i is not None:
                i.shutdown()