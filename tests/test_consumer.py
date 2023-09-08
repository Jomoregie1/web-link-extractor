import unittest
from unittest.mock import patch, mock_open
from src.consumer import Consumer
import queue


class TestConsumer(unittest.TestCase):

    def setUp(self):
        self.q = queue.Queue()
        self.consumer = Consumer(self.q, 'test_output.txt')

    # Test that valid hyperlinks are extracted
    def test_extract_hyperlinks(self):
        html_content = '<a href="http://example.com">Example</a>'
        links = self.consumer.extract_hyperlinks(html_content, "http://test.com")
        self.assertEqual(links, ["http://example.com"])

    # Test exception handling in extract_hyperlinks
    def test_extract_hyperlinks_exception(self):
        with patch('src.consumer.logging.error') as mock_error:
            links = self.consumer.extract_hyperlinks(None, "http://test.com")
            self.assertEqual(links, [])
            mock_error.assert_called()

    # Test write_to_file
    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_file(self, mock_file):
        self.consumer.write_to_file("http://test.com", ["http://example.com"])

        # Check if the file has been opened in append mode
        mock_file.assert_called_once_with(self.consumer.output_filename, 'a')

        # Get the mock file handle and check its method calls
        mock_handle = mock_file()
        mock_handle.write.assert_called_once()

        written_data = mock_handle.write.call_args[0][0]
        self.assertIn("http://example.com", written_data)

    # Test exception handling in write_to_file
    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_file_exception(self, mock_file):
        mock_file.side_effect = IOError("Cannot open file")

        with patch('src.consumer.logging.error') as mock_error:
            self.consumer.write_to_file("http://test.com", ["http://example.com"])

            mock_error.assert_called()

    # Test run method: (We will test only one condition to keep it concise, but in real scenarios, you may want to
    # test each path)
    def test_run_method(self):
        with patch.object(self.consumer, 'extract_hyperlinks', return_value=["http://example.com"]), \
                patch.object(self.consumer, 'write_to_file') as mock_write:
            self.q.put(("http://test.com", "<html></html>"))
            self.q.put(None)  # sentinel value to end the run loop

            self.consumer.run()
            mock_write.assert_called_once_with("http://test.com", ["http://example.com"])



if __name__ == "__main__":
    unittest.main()
