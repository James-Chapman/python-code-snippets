# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) James Chapman 2019
#

import sqlite3
import http.server

class FileServerHTTPHandler(http.server.BaseHTTPRequestHandler):
    server_version = "FileServerHTTPHandler/19.7"
    conn = None

    def __init__(self, request, client_address, server):
        super(FileServerHTTPHandler, self).__init__(request, client_address, server)
        self.server_version = "FileServerHTTPHandler/19.7"
        self.conn = sqlite3.connect('fileStore.db')

    def do_GET( self ):
        self.log_message( "Command: %s Path: %s Headers: %r"
                          % ( self.command, self.path, self.headers.items() ) )
        self.getPathRouter()

    def do_POST( self ):
        self.log_message( "Command: %s Path: %s Headers: %r"
                          % ( self.command, self.path, self.headers.items() ) )
        self.postPathRouter()

    def sendResponse(self, code, reason, responseString):
        self.send_response(code, reason)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-length', len(responseString))
        self.end_headers()
        self.wfile.write(responseString)

    def getPathRouter(self):
        if (self.path == '/'):
            responseString = bytes("<html><head><title>do_GET</title></head><body><h1>do_GET</h1></body></html>",
                                   'UTF-8')
            self.sendResponse(200, 'OK', responseString)
            return

        if (self.path == "/favicon.ico"):
            icon = b''
            with open("favicon.ico", "rb") as f:
                icon = f.read()
            self.sendResponse(200, 'OK', b"%s" % icon)
            return

        path = self.path.split('/')
        route = str(path[1])
        if (route == "download"):
            print("%s" % path[2])
            self.handleDownload("/".join(path[2:]))
        else:
            responseString = bytes(
                "<html><head><title>404</title></head><body><h1>404</h1></body></html>",
                'UTF-8')
            self.sendResponse(404, 'Not found', responseString)

    def postPathRouter(self):
        if (self.path == '/'):
            responseString = bytes("<html><head><title>do_POST</title></head><body><h1>do_POST</h1></body></html>",
                                   'UTF-8')
            self.sendResponse(200, 'OK', responseString)
            return
        else:
            responseString = bytes(
                "<html><head><title>404</title></head><body><h1>404</h1></body></html>",
                'UTF-8')
            self.sendResponse(404, 'Not found', responseString)

    def handleDownload(self, filePath):
        # TODO: Check for '..' chars that try to escape download path
        print(filePath)
        with open(filePath, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(0, 0)
            chunkSize = size
            remainSize = size
            if (size > 0x200):
                chunkSize = 0x200
            self.send_response(200, 'OK')
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', size)
            self.send_header('Content-Disposition', 'attachment; filename="%s"' % filePath)
            self.end_headers()
            while (remainSize > 0):
                if (remainSize < chunkSize):
                    chunkSize = remainSize
                chunk = f.read(chunkSize)
                self.wfile.write(chunk)
                remainSize -= chunkSize




def httpd(handler_class=FileServerHTTPHandler, server_address = ('', 8008), ):
    while (1):
        server = http.server.HTTPServer(server_address, handler_class)
        server.handle_request() # serve_forever

if __name__ == "__main__":
    httpd( )
