import unittest
from unittest.mock import patch, MagicMock
import os
from src.log_config import setup_logging  # Adjust the import as per your directory structure.
import logging


class TestSetupLogging(unittest.TestCase):

    def setUp(self):
        self.log_file = "test.log"

    def tearDown(self):
        # Remove the log file after tests
        try:
            os.remove(self.log_file)
        except Exception:
            pass

    def test_log_file_creation(self):
        # Call the function to set up logging
        setup_logging(log_filename=self.log_file)

        test_message = "This is a test message."
        logging.info(test_message)

        # Check if the log file was created and has the test_message
        with open(self.log_file, 'r') as f:
            content = f.read()
            self.assertIn(test_message, content)

    @patch('logging.StreamHandler.emit')
    def test_setup_logging(self, mock_emit):
        # Call the function to set up logging
        setup_logging(log_filename=self.log_file)

        test_message = "This is a test message."
        logging.info(test_message)

        # Check if message is logged to console (stream)
        calls = [call for call, _ in mock_emit.call_args_list if isinstance(call[0], logging.StreamHandler)]
        self.assertEqual(len(calls), 1)


if __name__ == '__main__':
    unittest.main()