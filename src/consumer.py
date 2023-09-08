import logging
from datetime import datetime
from bs4 import BeautifulSoup
import queue
from src.log_config import setup_logging

# Set up the logger for consumer
setup_logging(log_level=logging.INFO, log_filename="consumer.log")


class Consumer:
    def __init__(self, shared_queue, output_filename='output.txt'):
        self.shared_queue = shared_queue
        self.output_filename = output_filename

    def extract_hyperlinks(self, html_content, source_url="Unknown URL"):
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

    def write_to_file(self, source_url, hyperlinks):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.output_filename, 'a') as file:
                file.write(
                    f"[{timestamp}] For {source_url}, extracted hyperlinks are: {', '.join(hyperlinks)}\n")
                file.flush()
        except IOError as e:
            logging.error(f"IO error while writing to file: {e}")
        except Exception as e:
            logging.error(f"Unexpected error writing to file: {e}")

    def run(self):
        while True:
            try:
                item = self.shared_queue.get(timeout=10)  # adjust timeout as needed
                if item is None:  # Sentinel value indicating the producer is done
                    break
                source_url, html_content = item
                logging.info(f"Processing content from {source_url}.")
                hyperlinks = self.extract_hyperlinks(html_content, source_url)
                self.write_to_file(source_url, hyperlinks)

            except queue.Empty:
                logging.warning("Queue is empty. Waiting for more content.")
                continue
