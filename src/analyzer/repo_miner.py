from pydriller import Repository
from datetime import datetime
from analyzer.metrics_extractor import extract_metrics

def analyze_repository(url, since=None, until=None):
    since_dt = datetime.fromisoformat(since) if since else None
    until_dt = datetime.fromisoformat(until) if until else None

    results = []

    for commit in Repository(url, since=since_dt, to=until_dt).traverse_commits():
        total_complexity, total_smells = 0, 0
        for mod in commit.modified_files:
            if mod.filename and mod.filename.endswith(".py") and mod.source_code:
                complexity, smells = extract_metrics(mod.source_code)
                total_complexity += complexity
                total_smells += smells

        results.append({
            "hash": commit.hash[:7],
            "date": commit.committer_date,
            "author": commit.author.name,
            "complexity": total_complexity,
            "smells": total_smells
        })

    results.sort(key=lambda x: x["date"])
    return results
