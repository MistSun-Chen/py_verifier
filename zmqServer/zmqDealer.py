import zmq
import argparse
from common.configParams import ConfigParams
from zmqServer.zmqServer import ZmqServer
from zmqtest.asyncsrv import tprint
from common.common import mylog
import traceback

def main_dealer():
    print("Current libzmq version is %s" % zmq.zmq_version())
    print("Current  pyzmq version is %s" % zmq.pyzmq_version())
    parser = argparse.ArgumentParser()
    parser.add_argument("--configPath", type=str, default="config.json")
    args = parser.parse_args()
    cp = None
    try:
        cp = ConfigParams(args.configPath)
    except Exception as e:
        mylog.error(str(e))
        mylog.error(traceback.format_exc())


    cp.printParams()
    try:
        zmqServer = ZmqServer(cp)
        zmqServer.start()
        mylog.info("run to the end of zmqServer")
        # zmqServer.shutdown()
    except Exception as e:
        mylog.error("ZMQServer Error {}".format(str(e)))
        mylog.error(traceback.format_exc())






