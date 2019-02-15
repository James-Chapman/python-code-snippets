# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) James Chapman 2019
#

import queue
import threading
from ThreadWorker import ThreadWorker
import pytest
import mock

waiting_q = queue.Queue()
waiting_lk = threading.Lock()
complete_q = queue.Queue()
complete_lk = threading.Lock()

[pytest]
class TestThreadWorker:

    [pytest]
    def test_Contructor(self):
        worker = ThreadWorker(waiting_q, waiting_lk, complete_q, complete_lk)
        assert(type(worker) is ThreadWorker)

    [pytest]
    def test_run(self):
        with mock.patch.object(ThreadWorker, 'doStuff') as patched_doStuff:
            worker = ThreadWorker(waiting_q, waiting_lk, complete_q, complete_lk)
            worker.run()
        patched_doStuff.assert_called()

    [pytest]
    def test_stop(self):
        with mock.patch.object(ThreadWorker, 'stop_thread') as patched_stop_thread:
            worker = ThreadWorker(waiting_q, waiting_lk, complete_q, complete_lk)
            worker.run()
            worker.stop()
        patched_stop_thread.asseert(set)
