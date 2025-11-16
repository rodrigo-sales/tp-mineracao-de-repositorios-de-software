import pytest
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
    mock_extract.side_effect = [(3, 1), (10, 0)]

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
    assert results[0]["smells"] == 1

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