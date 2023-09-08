"""
Main module orchestrating the tasks between a producer and a consumer.

This module sets up signal handlers, initialises the producer and consumer threads,
and manages the shared queue between them. It also provides an indication of progress 
to the user and gracefully shuts down upon receiving a termination signal.
"""

import logging
import queue
import signal
import threading
import time

from consumer import Consumer
from producer import Producer
from log_config import setup_logging


def signal_handler(_, __):
    """Handles the termination signals (like SIGINT) to allow for graceful shutdown."""
    global shutdown_flag
    shutdown_flag = True
    logging.info("Received shutdown signal. Attempting graceful shutdown...")


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

shutdown_flag = False


def progress_indicator():
    """Indicates progress to the user until a shutdown flag is received."""
    while not shutdown_flag:
        print("Still processing...")
        time.sleep(5)


def read_urls_from_file(filename):
    """Reads and returns a list of URLs from the specified file.

    Args:
        filename (str): Path to the file containing URLs.

    Returns:
        list[str]: List of URLs.
    """
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def run_producer(shared_queue, url_list):
    """Initializes and runs the producer.

    Args:
        shared_queue (queue.Queue): Shared queue for the producer and consumer.
        url_list (list[str]): List of URLs to be processed by the producer.
    """
    try:
        logging.info("Producer started.")
        producer = Producer(shared_queue=shared_queue, url_list=url_list)
        if not shutdown_flag:
            producer.run()
        logging.info("Producer finished.")
    except Exception as e:
        logging.error(f"Exception occurred in the producer thread: {e}")


def run_consumer(shared_queue):
    """Initializes and runs the consumer.

    Args:
        shared_queue (queue.Queue): Shared queue for the producer and consumer.
    """
    try:
        logging.info("Consumer started.")
        consumer = Consumer(shared_queue)
        if not shutdown_flag:
            consumer.run()
        logging.info("Consumer finished.")
    except Exception as e:
        logging.error(f"Exception occurred in the consumer thread: {e}")


def main():
    print("""

    ░██╗░░░░░░░██╗███████╗██████╗░  ██╗░░░░░██╗███╗░░██╗██╗░░██╗
    ░██║░░██╗░░██║██╔════╝██╔══██╗  ██║░░░░░██║████╗░██║██║░██╔╝
    ░╚██╗████╗██╔╝█████╗░░██████╦╝  ██║░░░░░██║██╔██╗██║█████═╝░
    ░░████╔═████║░██╔══╝░░██╔══██╗  ██║░░░░░██║██║╚████║██╔═██╗░
    ░░╚██╔╝░╚██╔╝░███████╗██████╦╝  ███████╗██║██║░╚███║██║░╚██╗
    ░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░  ╚══════╝╚═╝╚═╝░░╚══╝╚═╝░░╚═╝

    ███████╗██╗░░██╗████████╗██████╗░░█████╗░░█████╗░████████╗░█████╗░██████╗░
    ██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗
    █████╗░░░╚███╔╝░░░░██║░░░██████╔╝███████║██║░░╚═╝░░░██║░░░██║░░██║██████╔╝
    ██╔══╝░░░██╔██╗░░░░██║░░░██╔══██╗██╔══██║██║░░██╗░░░██║░░░██║░░██║██╔══██╗
    ███████╗██╔╝╚██╗░░░██║░░░██║░░██║██║░░██║╚█████╔╝░░░██║░░░╚█████╔╝██║░░██║
    ╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
        """)
    setup_logging(log_level=logging.INFO, log_filename="main.log")

    filepath = input("Enter the path to your file containing URLs: ")

    try:
        url_list = read_urls_from_file(filepath)
        if not url_list:
            logging.warning("URL list is empty. Exiting...")
            return
    except FileNotFoundError:
        logging.error(f"File {filepath} not found. Please check the path and try again.")
        return
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")
        return

    shared_queue = queue.Queue(maxsize=1000)

    progress_thread = threading.Thread(target=progress_indicator, name="ProgressIndicator")
    progress_thread.start()

    logging.info("Starting producer and consumer threads...")
    print("Press Ctrl+C at any time to gracefully shut down the program.")

    producer_thread = threading.Thread(target=run_producer, args=(shared_queue, url_list), name="ProducerThread")
    consumer_thread = threading.Thread(target=run_consumer, args=(shared_queue,), name="ConsumerThread")

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    global shutdown_flag
    shutdown_flag = True
    progress_thread.join()

    logging.info("Processing complete!")


if __name__ == "__main__":
    main()
