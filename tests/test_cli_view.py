from unittest.mock import patch
from visualizer.cli_view import display_timeline

@patch("visualizer.cli_view.console.print")
def test_display_timeline_empty(mock_print):
    display_timeline([])

    mock_print.assert_any_call("[bold red]Nenhum commit encontrado![/bold red]")