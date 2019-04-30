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

        f = file_queue.get()

        # Detect end of queue
        if f is None:
            break

        logging.info ("[{}] Processing {}".format(port, f[0]))
        
        try:
            # cmd = ("python3 py/evaluate.py --binary {} --debug_info {} -two_pass --fp_model models/variable/x86/ "
            #         "--n2p_url http://localhost:{} --stat {}").format(f[1], f[0], str(port), f[2])

            cmd = ("python3 py/evaluate.py --binary {} --debug_info {} -two_pass --fp_model models/variable/x64/ "
                    "--n2p_url http://localhost:{} --stat {}").format(f[1], f[0], str(port), f[2])
            logging.info(cmd)

            output = check_output("cd /store/debin; {}".format(cmd), shell=True).decode()
            # logging.info("Output = " + output)
        except Exception as e:
            logging.warn("Error: " + str(e))

        file_queue.task_done()
    
    logging.info ("Killing thread " + str(tid))


if __name__== "__main__":

    setup_logging("log.log")

    dirs = ["/store/binaries/dataset-x64-multiversed/binary"]
    strip_rel = "/../strip/"
    results_rel = "/../result/"
    thread_count = 32

    files = []
    for dir in dirs:
        files_current = [(os.path.join(dir, f), os.path.join(dir + strip_rel, f), os.path.join(dir + results_rel, f + ".txt"))
                            for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        files = files + files_current

    file_queue = queue.Queue()
    for f in files:
        file_queue.put(f)

    for i in range(thread_count):
        file_queue.put(None)


    thread_workers = []
    for i in range(thread_count):
        t = threading.Thread(target=thread_worker_function, args=(i,))
        t.daemon = True
        t.start()
        thread_workers.append(t)


    for t in thread_workers:
        t.join()


