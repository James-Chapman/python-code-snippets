# -*- coding: utf-8 -*-
#===============================================================================
# Author      : J.Chapman
# License     : BSD
# Date        : 4 August 2013
# Description : Python 3 REST client
#===============================================================================

import http.client
import logging
import threading
import time
import sys

g_failed = 0

data = """
[
	{
		"id": "0001",
		"type": "donut",
		"name": "Cake",
		"ppu": 0.55,
		"batters":
			{
				"batter":
					[
						{ "id": "1001", "type": "Regular" },
						{ "id": "1002", "type": "Chocolate" },
						{ "id": "1003", "type": "Blueberry" },
						{ "id": "1004", "type": "Devil's Food" }
					]
			},
		"topping":
			[
				{ "id": "5001", "type": "None" },
				{ "id": "5002", "type": "Glazed" },
				{ "id": "5005", "type": "Sugar" },
				{ "id": "5007", "type": "Powdered Sugar" },
				{ "id": "5006", "type": "Chocolate with Sprinkles" },
				{ "id": "5003", "type": "Chocolate" },
				{ "id": "5004", "type": "Maple" }
			]
	},
	{
		"id": "0002",
		"type": "donut",
		"name": "Raised",
		"ppu": 0.55,
		"batters":
			{
				"batter":
					[
						{ "id": "1001", "type": "Regular" }
					]
			},
		"topping":
			[
				{ "id": "5001", "type": "None" },
				{ "id": "5002", "type": "Glazed" },
				{ "id": "5005", "type": "Sugar" },
				{ "id": "5003", "type": "Chocolate" },
				{ "id": "5004", "type": "Maple" }
			]
	},
	{
		"id": "0003",
		"type": "donut",
		"name": "Old Fashioned",
		"ppu": 0.55,
		"batters":
			{
				"batter":
					[
						{ "id": "1001", "type": "Regular" },
						{ "id": "1002", "type": "Chocolate" }
					]
			},
		"topping":
			[
				{ "id": "5001", "type": "None" },
				{ "id": "5002", "type": "Glazed" },
				{ "id": "5003", "type": "Chocolate" },
				{ "id": "5004", "type": "Maple" }
			]
	}
]
"""

def post_data():
    failed = 0
    for i in range(1000):
        try:
            restConn = http.client.HTTPConnection("10.172.132.88", 8081)
            restConn.connect()
            restConn.putrequest("POST", "/rest/post/data")
            restConn.putheader("content-type", "application/json")
            restConn.putheader("content-length", len(data))
            restConn.putheader("User-Agent", "Python REST client")
            restConn.endheaders()
            restConn.send(bytes(data, 'UTF-8'))
            resp = restConn.getresponse()
            #print(resp.status, resp.reason)
            if resp.status == 200:
                pass
            else:
                print("!", end="")
        except Exception as ex:
            print("!", end="")
            failed += 1
            #print(ex)
    print("failed: {0}".format(failed))


if __name__ == '__main__':
    threads = 48
    timestart = time.time()
    f = open("data.json", "r")
    data = f.read()
    f.close()
    for i in range(threads):
        thread1 = threading.Thread(target=post_data, args=())
        thread1.start()
        if i == threads - 1:
            thread1.join()
    timeend = time.time()
    totaltime = timeend - timestart
    print("\nTime: {0}".format(totaltime))



