# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import threading
from header_printing_web_server import PythonHttpHandler
import pytest
import http

g_serverThread = threading.Thread
g_run = True

def httpd(handler_class=PythonHttpHandler, server_address=('127.0.0.1', 8008), ):
    for i in range(2):
        server = http.server.HTTPServer(server_address, handler_class)
        server.handle_request()  # serve_forever

g_serverThread = threading.Thread(target=httpd, args=())

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    g_serverThread.start()

def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    g_run = False
    g_serverThread.join()

[pytest]
class TestPythonHttpHandler:

    [pytest]
    def test_do_GET(self):
        #with mock.patch.object(PythonHttpHandler, 'do_GET') as patched_do_GET:
            h1 = http.client.HTTPConnection('127.0.0.1:8008')
            h1.request("GET", "/")
            r1 = h1.getresponse()
            assert(r1.status == 200)
            assert(r1.reason == 'OK')

    [pytest]
    def test_do_POST(self):
        #with mock.patch.object(PythonHttpHandler, 'do_POST') as patched_do_POST:
            h1 = http.client.HTTPConnection('127.0.0.1:8008')
            h1.request("GET", "/")
            r1 = h1.getresponse()
            assert(r1.status == 200)
            assert(r1.reason == 'OK')

