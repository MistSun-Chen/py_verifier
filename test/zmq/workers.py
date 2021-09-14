# Task worker
# Connects PULL socket to tcp://localhost:5557
# Collects workloads from ventilator via that socket
# Connects PUSH socket to tcp://localhost:5558
# Sends results to sink via that socket
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import sys
import time
import zmq


context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

# Process tasks forever
while True:
    s = receiver.recv()

    # Simple progress indicator for the viewer

    s = s.decode(encoding="utf-8")
    ti = s.split(',')[1]
    num = s.split(',')[0]
    sys.stdout.write('.')
    sys.stdout.write(num)
    sys.stdout.flush()
    # Do the work
    time.sleep(int(ti)*0.001)

    # Send results to sink
    sender.send_string(f"{num}")