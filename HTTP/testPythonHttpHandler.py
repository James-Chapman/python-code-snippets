# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import threading
from header_printing_web_server import PythonHttpHandler
import pytest
import http
from parameterized import parameterized, parameterized_class

def httpd(handler_class=PythonHttpHandler, server_address=('127.0.0.1', 8008), ):
    for i in range(7):
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
            assert(r1.read(200) == b'<html><head><title>do_GET</title></head><body><h1>do_GET</h1></body></html>')

    [pytest]
    def test_do_POST(self):
        #with mock.patch.object(PythonHttpHandler, 'do_POST') as patched_do_POST:
            h1 = http.client.HTTPConnection('127.0.0.1:8008')
            h1.request("POST", "/")
            r1 = h1.getresponse()
            assert(r1.status == 200)
            assert(r1.reason == 'OK')
            assert(r1.read(200) == b'<html><head><title>do_POST</title></head><body><h1>do_POST</h1></body></html>')

    # Parameterized makes testing easy...
    # Specify variations and expected results. This isn't really testing single functions though
    @parameterized.expand([
        ("GET", "/", 200, 'OK', b'<html><head><title>do_GET</title></head><body><h1>do_GET</h1></body></html>'),
        ("GET", "/doesntexist", 404, 'Not found', b'<html><head><title>404</title></head><body><h1>404</h1></body></html>'),
        ("GET", "/favicon.ico", 200, 'OK', b'icon'),
        ("POST", "/", 200, 'OK', b'<html><head><title>do_POST</title></head><body><h1>do_POST</h1></body></html>'),
        ("POST", "/doesntexist", 404, 'Not found', b'<html><head><title>404</title></head><body><h1>404</h1></body></html>'),
    ])
    def test_Request(self, request, path, code, reason, expected):
        h1 = http.client.HTTPConnection('127.0.0.1:8008')
        h1.request(request, path)
        r1 = h1.getresponse()
        assert(r1.status == code)
        assert(r1.reason == reason)
        assert(r1.read(200) == expected)
