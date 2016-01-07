# -*- coding: utf-8 -*-
#===============================================================================
# Author      : J.Chapman
# License     : BSD
# Date        : 4 August 2013
# Description : Python 3 Default HTTP Server
#===============================================================================

import http.server
import socketserver

class DefaultHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    '''
    Threaded HTTP Server
    '''
    daemon_threads = True
