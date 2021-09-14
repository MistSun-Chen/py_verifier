import zmq
import queue
import threading
import logging
class ZmqSender:
    def __init__(self,context:zmq.Context,zmqAddr:str,status:bool = True):
        self.context = context
        self.zmqAddr = zmqAddr
        self.status = status
        self.msg_list = queue.Queue()
        #TODO :change
        self.thread = threading.Thread(target=self.run, args=()).start()
        pass


    def run(self):
        rspSock = self.context.socket(zmq.DEALER)
        try:
            rspSock.connect(self.zmqAddr)
        except Exception as e:
            print(e)
            self.context.term()
            return

        while self.status:
            if(self.status is False):
                break
            #TODO:此处应有判断空阻塞进程代码，但还未理解透彻，后续添加
            if self.msg_list.empty():
                break

            msg = self.msg_list.get()

            if msg.flag == 0:
                rspSock.send(bytes(msg.response))
                #TODO: destroy msg

        rspSock.close()

    def Join(self):
        self.thread.join()


    def push(self,msg):
        self.msg_list.put(msg)


    def shutdown(self):
        self.status = False
        self.Join()

    def get(self,time_second=1):
        """
        从队列中取消息，如果一段时间内取不出来，则返回空值
        :param time_second:阻塞时间
        :return:
        """
        try:
            return self.msg_list.get(timeout = time_second)
        except queue.Empty as e:
            logging.error(e)
            return None


