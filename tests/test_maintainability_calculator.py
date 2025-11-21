import pytest
from analyzer.maintainability_calculator import (
    calculate_maintainability,
    get_maintainability_level,
    get_complexity_level
)

def test_calculate_maintainability_normal_case():
	cc = 10
	loc = 100
	h_vol = 500
	mi = calculate_maintainability(cc, loc, h_vol)
	assert 0 <= mi <= 100
	assert isinstance(mi, float)

def test_calculate_maintainability_zero_loc():
	assert calculate_maintainability(5, 0, 100) == 100.0

def test_calculate_maintainability_fallback_volume():
	mi = calculate_maintainability(5, 50, 0)
	assert 0 <= mi <= 100

def test_calculate_maintainability_error_handling():
	mi = calculate_maintainability(10, -5, -5)
	assert mi == 50.0

@pytest.mark.parametrize("score, expected_level, expected_color", [
	(90, 'Excelente', 'green'),  # >= 85
	(85, 'Excelente', 'green'),  # Limite
	(75, 'Bom', 'yellow'),       # >= 70
	(70, 'Bom', 'yellow'),       # Limite
	(60, 'Aceitável', 'orange'), # >= 50
	(50, 'Aceitável', 'orange'), # Limite
	(40, 'Crítico', 'red'),      # < 50
])
def test_get_maintainability_level(score, expected_level, expected_color):
	result = get_maintainability_level(score)
	assert result['level'] == expected_level
	assert result['color'] == expected_color

@pytest.mark.parametrize("complexity, expected_label", [
	(3, 'Simples'),   # <= 5
	(5, 'Simples'),   # Limite
	(8, 'Moderada'),  # <= 10
	(10, 'Moderada'), # Limite
	(15, 'Alta'),     # <= 20
	(20, 'Alta'),     # Limite
	(25, 'Crítica'),  # > 20
])
def test_get_complexity_level(complexity, expected_label):
	assert get_complexity_level(complexity) == expected_label