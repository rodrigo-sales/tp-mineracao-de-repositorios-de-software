import pytest
from unittest.mock import patch, MagicMock
from analyzer.metrics_extractor import extract_metrics

@patch("analyzer.metrics_extractor.detect_smells")
@patch("analyzer.metrics_extractor.lizard.analyze_file.analyze_source_code")
def test_extract_metrics_complexity(mock_analyze, mock_smells):
    mock_function1 = MagicMock(cyclomatic_complexity=3)
    mock_function2 = MagicMock(cyclomatic_complexity=5)

    mock_analysis = MagicMock()
    mock_analysis.function_list = [mock_function1, mock_function2]
    mock_analyze.return_value = mock_analysis
    mock_smells.return_value = 1

    complexity, smells = extract_metrics("print('hello')")

    assert complexity == 8
    assert smells == 1
    mock_smells.assert_called_once_with(mock_analysis)

@patch("analyzer.metrics_extractor.detect_smells")
@patch("analyzer.metrics_extractor.lizard.analyze_file.analyze_source_code")
def test_extract_metrics_smells_result(mock_analyze, mock_smells):
    mock_analysis = MagicMock()
    mock_analysis.function_list = []
    mock_analyze.return_value = mock_analysis
    mock_smells.return_value = 2

    _, smells = extract_metrics("x = 1")

    assert smells == 2
