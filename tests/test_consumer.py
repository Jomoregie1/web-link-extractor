import queue
import unittest
from unittest.mock import patch
from src.consumer import Consumer


class TestConsumer(unittest.TestCase):

    def setUp(self):
        self.q = queue.Queue()
        self.consumer = Consumer(self.q)


    def test_extract_hyperlinks(self):
        html_content = '<a href="http://example.com">Example</a>'
        links = self.consumer.extract_hyperlinks(html_content, "http://test.com")
        self.assertEqual(links, ["http://example.com"])


    def test_extract_hyperlinks_invalid_content(self):
        with patch('src.consumer.logging.error') as mock_error:
            links = self.consumer.extract_hyperlinks(None, "http://test.com")
            self.assertEqual(links, [])
            mock_error.assert_called()

    @patch("builtins.print")
    def test_write_to_terminal(self, mock_print):
        self.consumer.write_to_terminal("http://test.com", ["http://example.com"])
        mock_print.assert_called_once()


    @patch("src.consumer.BeautifulSoup", side_effect=Exception("Parsing error"))
    def test_extract_hyperlinks_parsing_exception(self, mock_soup):
        with patch('src.consumer.logging.error') as mock_error:
            self.consumer.extract_hyperlinks("<html></html>", "http://test.com")
            mock_error.assert_called()

    def test_run_method(self):
        with patch.object(self.consumer, 'extract_hyperlinks', return_value=["http://example.com"]), \
                patch.object(self.consumer, 'write_to_terminal') as mock_write:
            self.q.put(("http://test.com", "<html></html>"))
            self.q.put(None)  # sentinel value to end the run loop

            self.consumer.run()
            mock_write.assert_called_once_with("http://test.com", ["http://example.com"])


if __name__ == "__main__":
    unittest.main()
