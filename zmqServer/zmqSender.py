import zmq
import queue
import threading
from zmqtest.asyncsrv import tprint
class ZmqSender(threading.Thread):
    def __init__(self, context: zmq.Context, zmqAddr: str, status: bool = True):
        super().__init__()
        self.context = context
        self.zmqAddr = zmqAddr
        self.status = status
        self.msg_list = queue.Queue()


    def run(self):

        rspSock = self.context.socket(zmq.DEALER)
        while self.status:
            try:
                message = self.get()
                if message:
                    tprint("sender sending message")
                    try:
                        tprint("sender start connecte")

                        rspSock.connect(self.zmqAddr)
                        tprint("sender end connecte")
                    except Exception as e:
                        tprint(str(e))
                        self.context.term()
                        break
                    tprint("sender start sending message")
                    rspSock.send_multipart([message.addr, bytes(message.response, encoding="utf-8")])
                    tprint("sender ending sending message")
            except queue.Empty:
                tprint("sender queue empty ")
                continue


        rspSock.close()



    def push(self,msg):
        self.msg_list.put(msg)


    def shutdown(self):
        self.status = False

    def get(self,time_second=None):
        """
        从队列中取消息，如果一段时间内取不出来，则返回空值
        :param time_second:阻塞时间
        :return:
        """
        try:
            return self.msg_list.get(timeout = time_second)
        except queue.Empty:
            tprint("zmqSender Error:msg_list is empty")
            return None


