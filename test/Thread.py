import threading
import sys

class myThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.stop_threads = True

    def run(self):
        while True:

            print(1)

            if self.stop_threads == False:
             break



if __name__ == '__main__':

    test = myThread()

    test.start()
    import time
    time.sleep(1)
    # test.join()
    stop_threads = False
    # sys.exit()
    # sys.exit()
