from urllib.parse import urlparse, urlunparse
import requests
import threading
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from log_config import setup_logging

setup_logging(log_level=logging.DEBUG, log_filename="producer.log")


class Producer:
    """
    The Producer class is responsible for fetching and processing URLs
    and then placing the fetched HTML content in a shared queue for consumption.
    """

    def __init__(self, shared_queue, url_list, max_threads=10, max_queue_size=100, cache_size=50):
        """
        Initializes the Producer with a list of URLs and configurations.

        Args:
        - shared_queue (queue.Queue): A shared queue where fetched content is placed.
        - url_list (list): List of URLs to be fetched.
        - max_threads (int): Maximum number of threads for concurrent fetch operations.
        - max_queue_size (int): Maximum size of the shared queue.
        - cache_size (int): Size of the cache for fetched URLs.
        """
        self.url_list = url_list
        self.prepare_urls()
        self.shared_queue = shared_queue
        self.successful_fetches = 0
        self.errors = 0
        self.lock = threading.Lock()
        self.max_threads = max_threads
        self.max_queue_size = max_queue_size
        self.cache_size = cache_size
        self.session = self.setup_session()

    def sanitize_url(self, url):
        """
        Sanitizes and validates the scheme of the given URL.

        Args:
        - url (str): The URL to be sanitized.

        Returns:
        - str or None: Sanitized URL or None if the URL scheme is not allowed.
        """
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            logging.warning(f"Disallowed URL scheme in {url}")
            return None
        return urlunparse(parsed)

    def is_valid_url(self, url):
        """
        Checks if the given URL is valid.

        Args:
        - url (str): The URL to be checked.

        Returns:
        - bool: True if the URL is valid, otherwise False.
        """
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            logging.error(f"Invalid URL: {url}")
            return False
        return True

    def prepare_urls(self):
        """
        Sanitizes and validates the list of URLs.
        """
        sanitized_urls = [self.sanitize_url(url) for url in self.url_list if
                          self.sanitize_url(url) and self.is_valid_url(self.sanitize_url(url))]
        self.url_list = sanitized_urls

    def setup_session(self):
        """
        Sets up and returns a requests Session with appropriate retry settings.

        Returns:
        - requests.Session: Configured session for making requests.
        """
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    @lru_cache(maxsize=None)
    def fetch_html_content(self, url):
        """
        Fetches and returns the HTML content of the given URL.

        Args:
        - url (str): The URL to be fetched.

        Returns:
        - str or None: Fetched HTML content or None in case of errors.
        """
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                logging.warning(f"Non-successful HTTP response for URL {url}: {response.status_code}")
                return None
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Error fetching URL {url}: {req_err}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while fetching URL {url}: {str(e)}")
            return None

    def run(self):
        """
        Fetches the HTML content for all URLs in the list concurrently
        and enqueues the content into the shared queue.
        """

        def fetch_and_enqueue(url):
            html_content = self.fetch_html_content(url)
            with self.lock:
                if html_content:
                    while self.shared_queue.qsize() >= self.max_queue_size:
                        self.shared_queue.get()
                    self.shared_queue.put((url, html_content))
                    self.successful_fetches += 1
                else:
                    self.errors += 1

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            executor.map(fetch_and_enqueue, self.url_list)

        self.shared_queue.put(None)

        self.session.close()

        logging.info(f"Total URLs processed: {len(self.url_list)}")
        logging.info(f"Successful fetches: {self.successful_fetches}")
        logging.info(f"Errors encountered: {self.errors}")
