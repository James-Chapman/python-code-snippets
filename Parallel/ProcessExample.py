# -*- coding: utf-8 -*-

#===============================================================================
# Author      : James Chapman
# Copyright   : See LICENSE.md
# Date        : 11/11/2014
# Description :
#===============================================================================

import queue
import multiprocessing
import time
from pythonsnippets.Parallel.ProcessWorker import ProcessWorker


def main():

    # Create Queues
    waiting_q = multiprocessing.Queue()
    waiting_lk = multiprocessing.Lock()
    complete_q = multiprocessing.Queue()
    complete_lk = multiprocessing.Lock()

    for i in range(100):
        waiting_q.put(i)

    # Create and start processes using different methods
    worker = ProcessWorker(waiting_q, waiting_lk, complete_q, complete_lk)
    proc1 = multiprocessing.Process(target=worker.doStuff, args=())
    proc1.start()

    # proc2 works because our ProcessWorker class inherits multiprocessing.Process (see class definition)
    proc2 = ProcessWorker(waiting_q, waiting_lk, complete_q, complete_lk)
    proc2.start()

    # Let the processes run for 10 seconds before setting stop event
    time.sleep(10)
    worker.stop()
    proc2.stop()

    # Wait for procs to exit.
    while (proc1.is_alive() or proc2.is_alive()):
        time.sleep(1)

    print("Waiting Q size: {0}".format(waiting_q.qsize()))
    print("Complete Q size: {0}".format(complete_q.qsize()))



if __name__ == '__main__':
    main()
    
