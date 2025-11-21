from unittest.mock import MagicMock
from analyzer.smell_detector import detect_smells

def test_smell_high_complexity():
    f = MagicMock(cyclomatic_complexity=20, length=10)
    analysis = MagicMock(function_list=[f])

    source_code = "def foo(): pass"
    assert detect_smells(analysis, source_code) >= 1

def test_smell_long_function():
    f = MagicMock(cyclomatic_complexity=5, length=120)
    analysis = MagicMock(function_list=[f])

    source_code = "def foo():\n" + "    x = 1\n" * 120
    assert detect_smells(analysis, source_code) >= 1

def test_no_smells():
    f = MagicMock(cyclomatic_complexity=10, length=50)
    analysis = MagicMock(function_list=[f])

    source_code = "def foo(x, y):\n    return x + y"
    assert detect_smells(analysis, source_code) < 5