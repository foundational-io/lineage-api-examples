import unittest
from unittest.mock import patch
from io import StringIO

from lineage_example import main


class TestMain(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout):
        # Call the main function, and just verify it doesn't crash :)
        main()


if __name__ == '__main__':
    unittest.main()
