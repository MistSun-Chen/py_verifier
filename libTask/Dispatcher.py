from common import common

class Dispatcher:
    def __init__(self):
        """
        初始化分发器
        分发器分为DQ类型和BQ类型，根据队列的功能不同使用不同的分发器
        """

        self.MAX_MQ_TYPE_NUM = common.INTERFACEID_COUNT * common.MAX_THREADS_PER_ALGORITHM
        self.dqs = [None] * self.MAX_MQ_TYPE_NUM
        self.bqs = [None] * self.MAX_MQ_TYPE_NUM

    def dispatchDq(self,message):
        if message.msgType >= self.MAX_MQ_TYPE_NUM:
            return -1

        if self.dqs[message.msgType] is not None:
            return self.dqs[message.msgType].push(message)
        else:
            return -1

    def dispatchBq(self,message):
        if message.msgType >= self.MAX_MQ_TYPE_NUM:
            return -1

        if self.bqs[message.msgType] is not None:
            return self.bqs[message.msgType].push(message)
        else:
            return -1

    def registerDq(self,message_type,mq):
        if message_type >= self.MAX_MQ_TYPE_NUM:
            return -1
        if self.dqs[message_type]:
            return -1

        self.dqs[message_type] = mq
        return 0


        pass

    def registerBq(self,message_type,bq):
        if message_type >= self.MAX_MQ_TYPE_NUM:
            return -1
        if self.dqs[message_type]:
            return -1

        self.dqs[message_type] = bq
        return 0


    def shutdownDq(self):
        for dq in self.dqs:
            if dq is not None:
                dq.shutdown()

    def shutdownBq(self):
        for bq in self.bqs:
            if bq is not None:
                bq.shutdown()




