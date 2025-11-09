import lizard
from analyzer.smell_detector import detect_smells

def extract_metrics(source_code):
    analysis = lizard.analyze_file.analyze_source_code("temp.py", source_code)
    total_complexity = sum(f.cyclomatic_complexity for f in analysis.function_list)
    total_smells = detect_smells(analysis)
    return total_complexity, total_smells