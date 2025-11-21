from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from main import cli

@patch("main.display_timeline")
@patch("main.analyze_repository")
def test_main_cli_analyze(mock_analyze, mock_display):
    mock_analyze.return_value = [
        {
            "hash": "abc1234",
            "date": MagicMock(strftime=lambda fmt: "2025-01-01"),
            "author": "Author X",
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

    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "https://repo.com"])

    assert result.exit_code == 0
    mock_analyze.assert_called_once_with("https://repo.com", None, None)
    mock_display.assert_called_once_with(mock_analyze.return_value)
