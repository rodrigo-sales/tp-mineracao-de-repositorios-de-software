from unittest.mock import patch, MagicMock
from analyzer.metrics_extractor import extract_metrics

@patch("analyzer.metrics_extractor.detect_smells")
@patch("analyzer.metrics_extractor.analyze_coupling")
@patch("analyzer.metrics_extractor.calculate_maintainability")
@patch("analyzer.metrics_extractor.lizard.analyze_file.analyze_source_code")
def test_extract_metrics_complexity(mock_analyze, mock_maintainability, mock_coupling, mock_smells):
    mock_function1 = MagicMock(cyclomatic_complexity=3)
    mock_function2 = MagicMock(cyclomatic_complexity=5)

    mock_analysis = MagicMock()
    mock_analysis.function_list = [mock_function1, mock_function2]
    mock_analysis.nloc = 100
    mock_analysis.token_count = 500
    mock_analyze.return_value = mock_analysis
    mock_coupling.return_value = 3.5
    mock_maintainability.return_value = 75.0
    mock_smells.return_value = 2

    metrics = extract_metrics("print('hello')")

    assert metrics['cyclomatic_complexity'] == 8
    assert metrics['code_smells'] == 2
    mock_smells.assert_called_once()

@patch("analyzer.metrics_extractor.detect_smells")
@patch("analyzer.metrics_extractor.analyze_coupling")
@patch("analyzer.metrics_extractor.calculate_maintainability")
@patch("analyzer.metrics_extractor.lizard.analyze_file.analyze_source_code")
def test_extract_metrics_smells_result(mock_analyze, mock_maintainability, mock_coupling, mock_smells):
    mock_analysis = MagicMock()
    mock_analysis.function_list = []
    mock_analysis.nloc = 10
    mock_analysis.token_count = 50
    mock_analyze.return_value = mock_analysis
    mock_smells.return_value = 2
    mock_coupling.return_value = 1.0
    mock_maintainability.return_value = 85.0

    metrics = extract_metrics("x = 1")

    assert isinstance(metrics, dict)
    assert metrics['code_smells'] == 2