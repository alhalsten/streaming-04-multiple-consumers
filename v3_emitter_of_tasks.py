"""
    Angela Halsten 9/16/23
    This program sends a message to a queue on the RabbitMQ server.
    Make tasks harder/longer-running by adding dots at the end of the message.

    Author: Denise Case
    Date: January 15, 2023

"""

import pika
import sys
import webbrowser
import csv
import logging

from util_logger import setup_logger
logger, logname = setup_logger(__file__)

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)

       
                
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        logger.info(f" [x] Sent {message}")
    except pika.exceptions.AMQPConnectionError as e:
        logger.info(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
        
    finally:
        # close the connection to the server
        conn.close()

input_file_name = "tasks.csv"



def stream_row(input_file_name):
    """Read from input file and stream data."""
    #logging.info(f"Starting to stream data from {input_file_name}.")

    # Create a file object for input (r = read access)
with open("tasks.csv", 'r') as input_file:
        #logging.info(f"Opened for reading: {"tasks.csv"}.")

        # Create a CSV reader object
    reader = csv.reader(input_file, delimiter= ",")


       
    for row in reader:
        message = " ".join(row)
        send_message("localhost","task_queue3", message)
        
            #logging.info(f"Sent: {MESSAGE} on port {PORT}. Hit CTRL-c to stop.")
        

def offer_rabbitmq_admin_site():
    show_offer = False
    if show_offer == True:
        """Offer to open the RabbitMQ Admin website"""
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()
    




# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    stream_row(input_file_name) 
    offer_rabbitmq_admin_site()

    