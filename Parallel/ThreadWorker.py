# -*- coding: utf-8 -*-

#===============================================================================
# Author      : James Chapman
# Copyright   : See LICENSE.md
# Date        : 11/11/2014
# Description :
#===============================================================================

import threading
import queue
import time


class ThreadWorker(threading.Thread):
    """
    Class docs
    """

    def __init__(self, _waiting_queue, _waiting_lock, _complete_queue, _complete_lock):
        """
        Constructor
        """
        super(ThreadWorker, self).__init__()
        self.stop_thread = threading.Event()
        self.waiting_queue = _waiting_queue
        self.waiting_lock = _waiting_lock
        self.complete_queue = _complete_queue
        self.complete_lock = _complete_lock


    def doStuff(self):
        """
        This is the method that does the work
        """
        while (not self.stop_thread.is_set()) and (not self.waiting_queue.empty()):

            # Get a job from the queue
            try:
                self.waiting_lock.acquire()
                job = self.waiting_queue.get_nowait()
            except queue.Queue.Empty:
                break
            finally:
                self.waiting_lock.release()

            # Do the work
            print("{0}: Starting {1}".format(threading.current_thread(), job))
            time.sleep(1)
            print("{0}: Finished {1}".format(threading.current_thread(), job))
            time.sleep(1)

            # Put the result back on the result Queue. (Doesn't have to be the same object as Source Q)
            try:
                self.complete_lock.acquire()
                self.complete_queue.put(job)
            except queue.Queue.Empty:
                break
            finally:
                self.complete_lock.release()


    def run(self):
        """
        Override method
        """
        self.doStuff()


    def stop(self):
        """
        Stop the thread
        """
        self.stop_thread.set()
