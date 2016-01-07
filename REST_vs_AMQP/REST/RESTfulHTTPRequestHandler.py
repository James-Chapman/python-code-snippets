# -*- coding: utf-8 -*-
#===============================================================================
# Author      : J.Chapman
# License     : BSD
# Date        : 4 August 2013
# Description : Python 3 HTTP Request Handler for REST calls
#===============================================================================

import json
import logging
import sys
import http.client
from DefaultHTTPRequestHandler import DefaultHTTPRequestHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class RESTfulHTTPRequestHandler(DefaultHTTPRequestHandler):
    """
    Default HTTP Request Handler Interface class.
    """

    def _handle_OPTIONS(self):
        """
        Handle OPTIONS function.
        """
        try:
            self.send_response(200, "OK")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.end_headers()
            logger.debug("Sent response: \"200 OK\"")
        except Exception as ex:
            logger.error(str(ex))
            raise ex


    def _handle_POST(self):
        """
        Handle POST function.
        """
        try:
            if (self.path == "/rest/post/data"):
                logger.debug("Sent response: \"200 OK\"")
                try:
                    self.headers = http.client.parse_headers(self.rfile,
                                                             _class=self.MessageClass)
                except http.client.LineTooLong:
                    self.send_error(400, "Line too long")
                data = self.rfile.read(self.headers.get('content-length')).decode("UTF-8")
                logger.info("Size of data received is: {0}".format(sys.getsizeof(data)))
                json.loads(data)
                self.send_response(200, "OK")
                self.end_headers()
            else:
                self.send_response(404, "Not found")
                self.end_headers()
                logger.debug("Sent response: \"404 Not found\"")
        except Exception as ex:
            logger.error(str(ex))
            raise ex
