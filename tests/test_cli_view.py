from unittest.mock import patch
from visualizer.cli_view import display_timeline
from datetime import datetime

@patch("visualizer.cli_view.console.print")
def test_display_timeline_empty(mock_print):
    display_timeline([])

    mock_print.assert_any_call("[bold red]Nenhum commit encontrado![/bold red]")


@patch("visualizer.cli_view.console.print")
def test_display_timeline(mock_print):
    results = [
        {
            "hash": "abc1234",
            "date": datetime(2025, 1, 1),
            "author": "Developer",
            "complexity": 10,
            "coupling": 3.0,
            "maintainability_index": 75.0,
            "lines_of_code": 100,
            "code_smells": 1,  
            "functions_count": 5,
            "avg_function_length": 20.0,
            "files_modified": 1
        }
    ]

    display_timeline(results)

    assert mock_print.call_count > 0