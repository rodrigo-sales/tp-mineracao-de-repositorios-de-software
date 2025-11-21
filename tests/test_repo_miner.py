from unittest.mock import patch, MagicMock
from analyzer.repo_miner import analyze_repository

@patch("analyzer.repo_miner.Repository")
def test_no_commits(mock_repo):
    mock_repo.return_value.traverse_commits.return_value = []

    results = analyze_repository("fake_url")
    assert results == []

@patch("analyzer.repo_miner.extract_metrics")
@patch("analyzer.repo_miner.Repository")
def test_repository_metrics_aggregation(mock_repo, mock_extract):
    mock_extract.side_effect = [
        {
            'cyclomatic_complexity': 3,
            'coupling': 2.0,
            'maintainability_index': 85.0,
            'lines_of_code': 50,
            'code_smells': 1,
            'functions_count': 2,
            'avg_function_length': 25.0
        },
        {
            'cyclomatic_complexity': 10,
            'coupling': 3.0,
            'maintainability_index': 70.0,
            'lines_of_code': 100,
            'code_smells': 0,
            'functions_count': 3,
            'avg_function_length': 33.3
        }
    ]

    fake_mod1 = MagicMock(filename="a.py", source_code="...")
    fake_mod2 = MagicMock(filename="b.py", source_code="...")

    fake_commit = MagicMock(
        hash="abc1234",
        committer_date="2025-01-01",
        author=MagicMock(name="Author X"),
        modified_files=[fake_mod1, fake_mod2]
    )

    mock_repo.return_value.traverse_commits.return_value = [fake_commit]

    results = analyze_repository("fake_url")

    assert results[0]["complexity"] == 13
    assert results[0]["code_smells"] == 1  

@patch("analyzer.repo_miner.extract_metrics")
@patch("analyzer.repo_miner.Repository")
def test_ignore_non_python_files(mock_repo, mock_extract):
    fake_mod = MagicMock(filename="readme.txt", source_code="whatever")
    fake_commit = MagicMock(
        hash="abc1234",
        committer_date="2025-01-01",
        author=MagicMock(name="Author X"),
        modified_files=[fake_mod]
    )
    mock_repo.return_value.traverse_commits.return_value = [fake_commit]

    analyze_repository("fake_url")

    mock_extract.assert_not_called()