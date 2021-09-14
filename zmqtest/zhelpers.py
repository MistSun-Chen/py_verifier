from random import randint

import zmq


# Receives all message parts from socket, prints neatly
def dump(zsocket):
    print("----------------------------------------")
    for part in zsocket.recv_multipart():
        print("[%03d]" % len(part))
        for c in part:
            print(part)
        # if all(31 < ord(c) < 128 for c in part):
        #     print(part)
        # else:
        #     print("".join("%x" % ord(c) for c in part))


# Set simple random printable identity on socket
def set_id(zsocket):
    identity = "%04x-%04x" % (randint(0, 0x10000), randint(0, 0x10000))
    zsocket.setsockopt_string(zmq.IDENTITY, identity)