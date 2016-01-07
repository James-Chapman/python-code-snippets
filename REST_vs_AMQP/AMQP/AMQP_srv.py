# -*- coding: utf-8 -*-
#===============================================================================
# Author      : James Chapman
# License     : BSD
# Date        : 4 August 2015
# Description : AMQP server
#===============================================================================

import pika


def main():
    parameters = pika.URLParameters('amqp://user:password@hostname:5672/%2F')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Get ten messages and break out
    for method_frame, properties, body in channel.consume('RMQ_Test_queue'):

        # Display the message parts
        #print(method_frame)
        #print(properties)
        #print(body)

        # Acknowledge the message
        channel.basic_ack(method_frame.delivery_tag)

        # Escape out of the loop after 100 messages
        #if method_frame.delivery_tag == 100:
        #    break


    # Cancel the consumer and return any pending messages
    requeued_messages = channel.cancel()
    print("Requeued {0} messages".format(requeued_messages))

    # Close the channel and the connection
    channel.close()
    connection.close()


if __name__ == '__main__':
    main()