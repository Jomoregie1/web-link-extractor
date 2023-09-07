import queue
from urllib.parse import urlparse, urlunparse
import requests
import threading
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

# logging configurations
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler("producer.log"),
        logging.StreamHandler()
    ]
)


class Producer:
    def __init__(self, url_list, max_threads=10, max_queue_size=100, cache_size=50):
        self.url_list = url_list
        self.prepare_urls()
        self.shared_queue = queue.Queue()
        self.successful_fetches = 0
        self.errors = 0
        self.lock = threading.Lock()
        self.max_threads = max_threads
        self.max_queue_size = max_queue_size
        self.cache_size = cache_size

    def sanitize_url(self, url):
        parsed = urlparse(url)

        if parsed.scheme not in ['http', 'https']:
            logging.warning(f"Disallowed URL scheme in {url}")
            return None

        sanitized_url = urlunparse(parsed)
        return sanitized_url

    def is_valid_url(self, url):
        parsed = urlparse(url)

        if not parsed.scheme or not parsed.netloc:
            logging.error(f"Invalid URL: {url}")
            return False

        return True

    def prepare_urls(self):
        sanitized_urls = []
        for url in self.url_list:
            sanitized_url = self.sanitize_url(url)
            if sanitized_url and self.is_valid_url(sanitized_url):
                sanitized_urls.append(sanitized_url)
            else:
                logging.error(f"Removing invalid or potentially harmful URL: {url}")

        self.url_list = sanitized_urls

    @lru_cache(maxsize=None)
    def fetch_html_content(self, url):
        try:
            response = requests.get(url)
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
        def fetch_and_enqueue(url):
            html_content = self.fetch_html_content(url)
            with self.lock:
                if html_content:
                    while self.shared_queue.qsize() >= self.max_queue_size:
                        self.shared_queue.get()
                    self.shared_queue.put(html_content)
                    self.successful_fetches += 1
                else:
                    self.errors += 1

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            executor.map(fetch_and_enqueue, self.url_list)

        logging.info(f"Total URLs processed: {len(self.url_list)}")
        logging.info(f"Successful fetches: {self.successful_fetches}")
        logging.info(f"Errors encountered: {self.errors}")

