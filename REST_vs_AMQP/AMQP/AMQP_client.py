# -*- coding: utf-8 -*-
#===============================================================================
# Author      : James Chapman
# License     : BSD
# Date        : 4 August 2015
# Description : AMQP client
#===============================================================================
import threading

import pika
import sys
import time

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


def amqp_publish():
    failed = 0
    for i in range(1000):
        try:
            parameters = pika.URLParameters('amqp://user:password@hostname:5672/%2F')
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.basic_publish('RMQ_Test_exchange',
                                  'RMQ_Test_key',
                                  data,
                                  pika.BasicProperties(content_type='text/plain',
                                                       delivery_mode=1))
            connection.close()

        except Exception as ex:
            print("!", end="")
            failed += 1
    print("failed: {0}".format(failed))




if __name__ == '__main__':
    threads = 48
    timestart = time.time()
    f = open("data.json", "r")
    data = f.read()
    f.close()
    for i in range(threads):
        thread1 = threading.Thread(target=amqp_publish, args=())
        thread1.start()
        if i == threads - 1:
            thread1.join()
    timeend = time.time()
    totaltime = timeend - timestart
    print("\nTime: {0}".format(totaltime))