import zmq
import argparse
from common.configParams import ConfigParams
from zmqServer.zmqServer import ZmqServer
import logging


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
        print(e)

    cp.printParams()
    try:
        zmqServer = ZmqServer(cp)
        zmqServer.start()
        zmqServer.shutdown()
    except Exception as e:
        logging.error(e)





