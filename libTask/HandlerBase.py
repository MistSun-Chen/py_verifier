from abc import ABCMeta, abstractmethod
from zmqsrc.zmqMessage import ZmqMessage
import uuid
import time
import json
import datetime
from zmqtest.asyncsrv import tprint
from common.error import Error
import traceback
from common.common import mylog


class HandlerBase(metaclass=ABCMeta):
    def __init__(self):
        self.super_switch = False

    def generateRequestID(self):
        """
        利用python的uuid模块生成requestID
        :return: requestID
        """

        # uuid1()：这个是根据当前的时间戳和MAC地址生成的，最后的12个字符408d5c985711对应的就是MAC地址，因为是MAC地址，那么唯一性应该不用说了。但是生成后暴露了MAC地址这就很不好了。
        #
        # uuid3()：里面的namespace和具体的字符串都是我们指定的，然后呢···应该是通过MD5生成的，这个我们也很少用到，莫名其妙的感觉。
        #
        # uuid4()：这是基于随机数的uuid，既然是随机就有可能真的遇到相同的，但这就像中奖似的，几率超小，因为是随机而且使用还方便，所以使用这个的还是比较多的。
        #
        # uuid5()：这个看起来和uuid3()貌似并没有什么不同，写法一样，也是由用户来指定namespace和字符串，不过这里用的散列并不是MD5，而是SHA1.
        return uuid.uuid4()

    def setApiKey(self, api_key: str):
        self.api_key = api_key

    # /***********************************************************************************************************************
    # * 功  能：填充返回信息
    # * 参  数：IN:
    # *         interface ---------------------功能接口
    # *         errorMsg ----------------------错误信息
    # *         timePoints ----------------------当前时间
    # *        OUT:
    # *         response ----------------------传递的信息，包括检测结果，错误信息，耗时
    # * 返回值：返回检测结果，错误信息，耗时
    # ***********************************************************************************************************************/
    def fillResponse(self, interface: str, response, request_id, errorMsg):
        return self.fillResponse_(interface, response, request_id, errorMsg, [time.time()])

    def fillResponse_(self, interface: str, response, request_id, errorMsg, timePoints):

        if len(request_id) == 0:
            response["request_id"] = str(self.generateRequestID())
        else:
            response["request_id"] = request_id

        response["time_used"] = int((time.time()-timePoints[0])*1000)
        if "error_id" not in response:
            response["error_id"] = errorMsg[0]
            if len(errorMsg[1]):
                response["error_message"] = errorMsg[1]

        self.writeLog(interface, response, timePoints)
        # mylog.info("fillResponse is " + json.dumps(response))
        return json.dumps(response)

    # /***********************************************************************************************************************
    # * 功  能：填充返回信息(含错误ID)
    # * 参  数：IN:
    # *         interface ---------------------功能接口
    # *         errorMsg ----------------------错误信息及ID
    # *         timePoints ----------------------当前时间
    # *        OUT:
    # *         response ----------------------传递的信息，包括检测结果，错误信息及ID，耗时
    # * 返回值：返回检测结果，错误信息及ID，耗时
    # ***********************************************************************************************************************/
    #
    def fillResponse_errorId(self, interface, response, request_id, errorMsg):
        return self.fillResponse_errorId_(interface, response, request_id, errorMsg, timePoints=[time.time()])

    def fillResponse_errorId_(self, interface, response, request_id, errorMsg, timePoints):

        if len(request_id) == 0:
            response["request_id"] = self.generateRequestID()
        else:
            response["request_id"] = request_id

        response["time_used"] = round((time.time() - timePoints[0]) * 1000, 4)

        if errorMsg is not None and errorMsg != "":
            response["error_message"] = errorMsg
        self.writeLog(interface, response, timePoints)
        return json.dumps(response)

    # / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
    # *功能：填充返回信息(不含request
    # id, 在外面一层填充，主要用于内部调用人脸的接口的返回，其他情况不要调用)
    # *参数：IN:
    # *interface - --------------------功能接口
    # *errorMsg - ---------------------错误信息及ID
    # *timePoints - ---------------------当前时间
    # *OUT:
    # *response - ---------------------传递的信息，包括检测结果，错误信息及ID，耗时
    # *返回值：返回检测结果，错误信息及ID，耗时
    # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /

    def fillResponse_noRequstid_(interface: str, response, errorMsg):

        response["error_id"] = errorMsg[0]
        response["error_message"] = errorMsg[1]
        return json.dumps(response)

    # / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
    # *功能：写日志
    # *参数：IN:
    # *interface - --------------------功能接口
    # *timePoints - ---------------------当前时间
    # *response - ---------------------传递的信息，包括检测结果，错误信息及ID，耗时
    # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /

    def writeLog(self, interface, resp, timePoints):
        timeLong = round((time.time() - timePoints[0]) * 1000, 4)
        timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timePoints[0]))

        if timeLong >= 1000 or timeLong <0:
            mylog.error(
            "|Req Time: {},|Interface:{} ,|Time Used:{} ,ms|Result: {}".format(str(timestr), interface, str(timeLong),
                                                                               str(resp)))
        elif timeLong >= 500:
            mylog.warning(
            "|Req Time: {},|Interface:{} ,|Time Used:{} ,ms|Result: {}".format(str(timestr), interface, str(timeLong),
                                                                               str(resp)))
        else: 
            mylog.debug(
            "|Req Time: {},|Interface:{} ,|Time Used:{} ,ms|Result: {}".format(str(timestr), interface, str(timeLong),
                                                                               str(resp)))

    def auth(self, api_key):
        return (self.api_key == api_key)

    def validate_(self, interface, request):
        value = {}
        request_id = ""
        try:
            value = json.loads(request)

            if "api_key" not in value or not self.auth(value["api_key"]):
                if "request_id" in value and isinstance(value["request_id"], str):
                    request_id = value["request_id"]
                return self.fillResponse(interface, {}, request_id, Error.FINDER_API_KEY_INVALID), value
            return None, value
        except Exception as e:
            mylog.error(e)
            mylog.error(traceback.format_exc())
            # print(e)
            return self.fillResponse(interface, {}, request_id, Error.ERROR_JSON_SYNTAX), value

    def validate(self, interface, request):
        request_id = ""
        try:
            if "api_key" not in request or not self.auth(request["api_key"]):
                if "request_id" in request and isinstance(request["request_id"], str):
                    request_id = request["request_id"]
                return self.fillResponse(interface, {}, request_id, Error.FINDER_API_KEY_INVALID)
            return None
        except Exception as e:
            mylog.error(e)
            mylog.error(traceback.format_exc())
            # print(e)
            return self.fillResponse(interface, {}, request_id, Error.ERROR_JSON_SYNTAX)

    # / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
    # *功能：图片格式base64转CV::Mat
    # *参数：IN:
    # *s - --------------------base64编码的图片
    # *OUT:
    # *decode_img - ---------------------CV::Mat格式的图片
    # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /

    def base64ToMat(self, s, decode_img):
        pass

    @abstractmethod
    def handle(self, message: ZmqMessage):
        pass

    @abstractmethod
    def preDetect(self,modelPath):
        pass

