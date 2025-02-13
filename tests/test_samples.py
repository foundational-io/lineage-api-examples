from unittest.mock import patch
from io import StringIO

from hello-lineage-graph.main import main

@patch('sys.stdout', new_callable=StringIO)
def test_main(mock_stdout):
    # Call the main function
    main()

    # Get the output
    output = mock_stdout.getvalue()

    # Assert that the output contains expected elements
    assert "Entity:" in output
    assert "Downstreams:" in output
    assert "Upstreams:" in output