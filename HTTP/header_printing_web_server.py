# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#===============================================================================
# Author      : James Chapman
# Copyright   : See LICENSE.md
# Date        : 01/01/2015
# Description : Web server that will print client headers. Useful in client
#               client development. Requires Python3
#===============================================================================

import http.server
import socketserver

class PythonHttpHandler( http.server.BaseHTTPRequestHandler ):
    server_version= "PythonHttpHandler/0.1"
    def do_GET( self ):
        self.log_message( "Command: %s Path: %s Headers: %r"
                          % ( self.command, self.path, self.headers.items() ) )
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'html')
        self.end_headers()
        self.wfile.write(bytes("<html> <head><title> do_GET </title> </head> <body> </body> </html>", 'UTF-8'))

    def do_POST( self ):
        self.log_message( "Command: %s Path: %s Headers: %r"
                          % ( self.command, self.path, self.headers.items() ) )
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'html')
        self.end_headers()
        self.wfile.write(bytes("<html> <head><title> do_POST </title> </head> <body> </body> </html>", 'UTF-8'))


def httpd(handler_class=PythonHttpHandler, server_address = ('', 8008), ):
    while (1):
        server = http.server.HTTPServer(server_address, handler_class)
        server.handle_request() # serve_forever

if __name__ == "__main__":
    httpd( )