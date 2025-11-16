from analyzer.smell_detector import detect_smells
from unittest.mock import MagicMock

def test_smell_high_complexity():
    f = MagicMock(cyclomatic_complexity=20, length=10)
    analysis = MagicMock(function_list=[f])

    assert detect_smells(analysis) == 1

def test_smell_long_function():
    f = MagicMock(cyclomatic_complexity=5, length=120)
    analysis = MagicMock(function_list=[f])

    assert detect_smells(analysis) == 1

def test_no_smells():
    f = MagicMock(cyclomatic_complexity=10, length=50)
    analysis = MagicMock(function_list=[f])

    assert detect_smells(analysis) == 0