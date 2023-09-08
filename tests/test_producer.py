import unittest
from unittest.mock import patch, Mock
from src.producer import Producer


class TestProducer(unittest.TestCase):

    def test_sanitize_url_valid_scheme(self):
        producer = Producer([])
        sanitized_url = producer.sanitize_url('https://www.example.com')
        self.assertEqual(sanitized_url, 'https://www.example.com')

    def test_sanitize_url_invalid_scheme(self):
        producer = Producer([])
        sanitized_url = producer.sanitize_url('javascript:alert(1)')
        self.assertIsNone(sanitized_url)

    def test_is_valid_url(self):
        producer = Producer([])
        self.assertTrue(producer.is_valid_url('https://www.example.com'))
        self.assertFalse(producer.is_valid_url('example.com'))
        self.assertFalse(producer.is_valid_url('https:/www.example.com'))

    def test_prepare_urls(self):
        producer = Producer(['https://www.valid.com', 'javascript:alert(1)', 'www.invalid.com'])
        self.assertEqual(producer.url_list, ['https://www.valid.com'])

    @patch('requests.Session.get')  # Patching get method of the requests.Session
    def test_fetch_html_content_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html></html>'
        mock_get.return_value = mock_response

        producer = Producer([])
        content = producer.fetch_html_content('https://www.example.com')
        self.assertEqual(content, '<html></html>')

    @patch('requests.Session.get')
    def test_fetch_html_content_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        producer = Producer([])
        content = producer.fetch_html_content('https://www.example.com')
        self.assertIsNone(content)

    @patch('requests.Session.get')
    def test_fetch_html_content_exception(self, mock_get):
        mock_get.side_effect = Exception("Fake exception")

        producer = Producer([])
        content = producer.fetch_html_content('https://www.example.com')
        self.assertIsNone(content)

    @patch('requests.Session.get')
    def test_run(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html></html>'
        mock_get.return_value = mock_response

        producer = Producer(['https://www.example.com'])
        producer.run()

        self.assertEqual(producer.successful_fetches, 1)
        self.assertEqual(producer.errors, 0)


if __name__ == '__main__':
    unittest.main()
