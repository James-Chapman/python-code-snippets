# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) James Chapman 2019
#
import queue
import threading
import time
from pythonsnippets.Parallel.ThreadWorker import ThreadWorker


def main():

    # Create Queues
    waiting_q = queue.Queue()
    waiting_lk = threading.Lock()
    complete_q = queue.Queue()
    complete_lk = threading.Lock()

    for i in range(100):
        waiting_q.put(i)

    # Create and start threads using different methods
    worker = ThreadWorker(waiting_q, waiting_lk, complete_q, complete_lk)
    thread1 = threading.Thread(target=worker.doStuff, args=())
    thread1.start()

    # thread2 works because our ThreadWorker class inherits threading.Thread (see class definition)
    thread2 = ThreadWorker(waiting_q, waiting_lk, complete_q, complete_lk)
    thread2.start()

    # Let the threads run for 10 seconds before setting stop event
    time.sleep(10)
    worker.stop()
    thread2.stop()

    # Wait for threads to exit.
    while (thread1.is_alive() or thread2.is_alive()):
        time.sleep(1)

    print("Waiting Q size: {0}".format(waiting_q.qsize()))
    print("Complete Q size: {0}".format(complete_q.qsize()))



if __name__ == '__main__':
    main()
    
