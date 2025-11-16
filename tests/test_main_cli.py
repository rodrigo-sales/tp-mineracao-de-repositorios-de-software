from click.testing import CliRunner
from unittest.mock import patch
from main import cli

@patch("main.display_timeline")
@patch("main.analyze_repository")
def test_main_cli_analyze(mock_analyze, mock_display):
    mock_analyze.return_value = []

    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "https://repo.com"])

    assert result.exit_code == 0
    mock_analyze.assert_called_once_with("https://repo.com", None, None)
    mock_display.assert_called_once_with([])