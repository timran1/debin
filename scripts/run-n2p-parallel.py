import os
import time
import csv

import queue, threading, logging
from subprocess import check_output

def setup_logging(log_filename):

    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)
    
    fileHandler = logging.FileHandler(log_filename)
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    rootLogger.addHandler(consoleHandler)

    rootLogger.info("Logging setup")

def thread_worker_function(num):

    tid = num
    port = 10000 + tid

    logging.info ("Starting thread " + str(tid))
    while True:

        f = q.get()

        # Detect end of queue
        if f is None:
            break

        # cmd = ('./bazel-bin/n2p/json_server/json_server \
        # --model ../models/crf/x86/model \
        # --valid_labels ../c_valid_labels \
        # -logtostderr \
        # --port {}').format(str(port))

        cmd = ('./bazel-bin/n2p/json_server/json_server \
        --model ../models/crf/x64/model \
        --valid_labels ../c_valid_labels \
        -logtostderr \
        --port {}').format(str(port))

        logging.info(cmd)

        os.system("cd /store/debin/Nice2Predict; {}".format(cmd))  

        q.task_done()
    
    logging.info ("Killing thread " + str(tid))


if __name__== "__main__":

    setup_logging("log-n2p.log")

    thread_count = 32
    q = queue.Queue()

    for i in range(thread_count):
        q.put(i)

    for i in range(thread_count):
        q.put(None)

    thread_workers = []
    for i in range(thread_count):
        t = threading.Thread(target=thread_worker_function, args=(i,))
        t.daemon = True
        t.start()
        thread_workers.append(t)


    for t in thread_workers:
        t.join()


