# -*- coding: utf-8 -*-
#===============================================================================
# Author      : J.Chapman
# License     : BSD
# Date        : 4 August 2013
# Description : Python 3 REST server
#===============================================================================

from DefaultHTTPServer import DefaultHTTPServer
from RESTfulHTTPRequestHandler import RESTfulHTTPRequestHandler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console and file handlers and set log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s %(threadName)s %(filename)s %(lineno)d [%(levelname)s] : %(funcName)s : %(message)s')

# set formatter for console and file handlers
ch.setFormatter(formatter)

# add console and file handlers to logger
logger.addHandler(ch)

logging.getLogger("DefaultHTTPServer").addHandler(ch)
logging.getLogger("DefaultHTTPRequestHandler").addHandler(ch)
logging.getLogger("RESTfulHTTPRequestHandler").addHandler(ch)

def main():
    """
    main program function
    """
    SERVER_IP = "0.0.0.0"
    SERVER_PORT = 8080

    server = DefaultHTTPServer((SERVER_IP, SERVER_PORT), RESTfulHTTPRequestHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()


if __name__ == '__main__':
    main()
