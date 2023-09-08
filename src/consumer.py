import logging
from datetime import datetime
from bs4 import BeautifulSoup
import queue
from log_config import setup_logging

setup_logging(log_level=logging.INFO, log_filename="consumer.log")

class Consumer:
    """
    The Consumer class is responsible for processing HTML content
    and extracting hyperlinks.
    """

    def __init__(self, shared_queue):
        """
        Initializes the Consumer with a shared queue.

        Args:
        - shared_queue (queue.Queue): A queue containing HTML content to be processed.
        """
        self.shared_queue = shared_queue

    def extract_hyperlinks(self, html_content, source_url="Unknown URL"):
        """
        Extracts and returns hyperlinks from the given HTML content.

        Args:
        - html_content (str): HTML content from which hyperlinks need to be extracted.
        - source_url (str): The source URL of the HTML content. Default is 'Unknown URL'.

        Returns:
        - list: A list of hyperlinks extracted from the given HTML content.
        """
        hyperlinks = []

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith(('http', 'https')):
                    hyperlinks.append(href)

        except Exception as e:
            logging.error(f"Error while parsing content from {source_url}: {e}")
            return []

        logging.info(f"Extracted {len(hyperlinks)} hyperlinks from {source_url}.")
        return hyperlinks

    def write_to_terminal(self, source_url, hyperlinks):
        """
        Writes the extracted hyperlinks to the terminal.

        Args:
        - source_url (str): The source URL of the HTML content.
        - hyperlinks (list): List of hyperlinks to be displayed.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] For {source_url}, extracted hyperlinks are: {', '.join(hyperlinks)}")

    def run(self):
        """
        Continuously processes items (HTML content) from the shared queue,
        extracts hyperlinks, and writes them to the terminal.
        """
        while True:
            try:
                item = self.shared_queue.get(timeout=10)
                if item is None:  # Sentinel value indicating the producer is done
                    break
                source_url, html_content = item
                logging.info(f"Processing content from {source_url}.")
                hyperlinks = self.extract_hyperlinks(html_content, source_url)
                self.write_to_terminal(source_url, hyperlinks)

            except queue.Empty:
                logging.warning("Queue is empty. Waiting for more content.")
                continue