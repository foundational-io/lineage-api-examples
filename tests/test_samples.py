import unittest
from unittest.mock import patch
from io import StringIO

from hello_lineage_graph.main import main  # Adjust import based on your actual structure

class TestMain(unittest.TestCase):  # Use 'class' and 'unittest.TestCase'

    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout):  # Use 'self' and 'mock_stdout'
        # Call the main function
        main()

        # Get the output
        output = mock_stdout.getvalue

        # Assert that the output contains expected elements
        self.assertIn("Entity and Dependencies:", output)  # Use 'self.assertIn'
        self.assertIn("Downstream Dependencies:", output)
        self.assertIn("Upstream Dependencies:", output)

if __name__ == '__main__':
    unittest.main()