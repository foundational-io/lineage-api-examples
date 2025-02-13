import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

TESTS_PATH = os.getcwd()
SAMPLES_PATH = os.path.join(TESTS_PATH, '..', 'hello_lineage_graph')
sys.path.append(SAMPLES_PATH)

from hello_lineage_graph.main import main  # Adjust import based on your actual structure

class TestMain(unittest.TestCase):  # Use 'class' and 'unittest.TestCase'

    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout):  # Use 'self' and 'mock_stdout'
        # Call the main function, and just verifies it doesn't crash :)
        main()

if __name__ == '__main__':
    unittest.main()