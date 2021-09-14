from common.configParams import ConfigParams
import queue
from threading import Thread
# from libTask.HandlerFactory import handlerFactoryInstance
from libTask.HandlerFactory import HandlerFactory
from zmqtest.asyncsrv import tprint
import zmq

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



    def run(self):
        if self.cp.CPU == 1:
            tprint("Worker::Run CPU")
            #TODO:之前此处设置caffe的CPU工作模式
        else:
            tprint("Worker::Run GPU {}".format(str(self.gpu_id)))
            #TODO：之前此处设置caffe的GPU工作模式，并根据gpu_id数加载模型

        handlerFactoryInstance = HandlerFactory()
        handler = handlerFactoryInstance.create(self.handler_id,self.model_path,self.cp,str(self.gpu_id),self.gpu_num)
        if handler is None:
            return

        while self.status:
            try:
                message = self.queue.get()
                if message:
                    response = handler.handle(message)
                    # tprint("handler response is {}".format(str(response)))
                    # tprint("ending queue handle")
                    tprint("zmqServer start sending result message")

                    socket = message.zmqSender.context.socket(zmq.DEALER)
                    # tprint("end create socket ")
                    socket.connect(message.zmqSender.zmqAddr)
                    # tprint("end connect message")
                    socket.send_multipart([message.addr, bytes(response, encoding="utf-8")])
                    # tprint("end sending")
                    #此处必须加close()

                    tprint("zmqServer complete sending result message")
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
        try:
            for i in range(self.worker_count):
                # TODO:此处原来依靠caffe模块检测GPU设备是否可用，输出不可用GPU编号
                # 对于不可用gpu直接continue
                # 对于可用gpu，我们new

                tprint("worker_count : {}/{}".format(i, self.worker_count - 1))
                worker = Worker(self.msg_list, self.gpus[i], self.gpu_num, self.handler_id, self.model_path, self.cp)
                worker.start()
                print("Dispatcher Num {} worker thread start  ".format(self.handler_id))
                self.threads.append(worker)

        except Exception as e:
            tprint("Thread init failed!")
            tprint(e)



    def push(self,message):
        self.msg_list.put(message)
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
                i.join()


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