import zmq
from threading import Thread
import json
import argparse
import os
import logging
CONFIG_ERROR="Config file error. "


def generateDefaultConfig(configPath):
    routerConfig = {}
    routerConfig["front_addr"] = "tcp://*:5559"
    routerConfig["back_addr"] = "tcp://*:5560"

    config ={}
    config["routerParams"] = routerConfig
    try:
        with open(configPath,'w')as f:
            f.write(json.dumps(config))
    except IOError:
        return False
    return True

def create_router(front_addr,back_addr):
    context = zmq.Context()
    frontEnd = context.socket(zmq.ROUTER)
    backEnd = context.socket(zmq.DEALER)

    frontEnd.bind(front_addr)
    backEnd.bind(back_addr)

    print("zmq.proxy started ")
    zmq.proxy(frontEnd,backEnd)

    # We never get here...
    frontEnd.close()
    backEnd.close()
    context.term()




def main_router():
    print("Current libzmq version is %s" % zmq.zmq_version())
    print("Current  pyzmq version is %s" % zmq.pyzmq_version())
    parser = argparse.ArgumentParser()
    parser.add_argument("--configPath",type=str,default = "router.json")
    args = parser.parse_args()

    front_addr = ""
    back_addr = ""

    if os.path.exists(args.configPath) == False:
        if(generateDefaultConfig(args.configPath) == False):
            print("Generate default config file failed.")

        front_addr = "tcp://*:5559"
        back_addr = "tcp://*:5560"
        print("Using default config parameters.")

    else:
        try:
            with open(args.configPath,'r')as f:
                config = json.loads(f.read())
                if "routerParams" in config:
                    if "front_addr" in config["routerParams"]:
                        front_addr = config["routerParams"]["front_addr"]
                    else:
                        logging.error(CONFIG_ERROR + "Missing front_addr")
                    if "back_addr" in config["routerParams"]:
                        back_addr = config["routerParams"]["back_addr"]
                    else:
                        logging.error(CONFIG_ERROR + "Missing back_addr.")
                else:
                    logging.error(CONFIG_ERROR + "Missing routerParams.")
        except IOError:
            print("File is not accessible.")
    print("front_addr             :  ",front_addr)
    print("back_addr              :  ",back_addr)

    broker_verifier = Thread(target=create_router, args=(front_addr, back_addr))
    broker_verifier.start()


    # auto broker_verifier = std::make_shared < std::thread > (create_router, front_addr, back_addr);

    # if(broker_verifier){
    #     broker_verifier->join();
    # }


