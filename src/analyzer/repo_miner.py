from pydriller import Repository
from datetime import datetime
from analyzer.metrics_extractor import extract_metrics

def analyze_repository(url, since=None, until=None):
    """
    Retorna uma lista de commits com:
    - Complexidade cíclomática
    - Acoplamento
    - Índice de manutenibilidade
    - Linhas de código
    - Code smells avançados
    - Estatísticas por função
    """
    since_dt = datetime.fromisoformat(since) if since else None
    until_dt = datetime.fromisoformat(until) if until else None

    results = []

    try:
        for commit in Repository(url, since=since_dt, to=until_dt).traverse_commits():
            commit_metrics = {
                "hash": commit.hash[:7],
                "date": commit.committer_date,
                "author": commit.author.name,
                "complexity": 0,
                "coupling": 0.0,
                "maintainability_index": 100.0,
                "lines_of_code": 0,
                "code_smells": 0,
                "functions_count": 0,
                "avg_function_length": 0.0,
                "files_modified": 0
            }
            
            file_metrics = []
            
            for mod in commit.modified_files:
                if mod.filename and mod.filename.endswith(".py") and mod.source_code:
                    try:
                        metrics = extract_metrics(mod.source_code, mod.filename)
                        
                        # Agrega métricas
                        commit_metrics["complexity"] += metrics['cyclomatic_complexity']
                        commit_metrics["coupling"] += metrics['coupling']
                        commit_metrics["lines_of_code"] += metrics['lines_of_code']
                        commit_metrics["code_smells"] += metrics['code_smells']
                        commit_metrics["functions_count"] += metrics['functions_count']
                        
                        file_metrics.append({
                            'filename': mod.filename,
                            'metrics': metrics
                        })
                        
                    except Exception as e:
                        print(f"Erro ao processar {mod.filename}: {e}")
                        continue
            
            # Calcula média de manutenibilidade
            if file_metrics:
                commit_metrics["files_modified"] = len(file_metrics)
                
                # Médias ponderadas
                if commit_metrics["functions_count"] > 0:
                    commit_metrics["avg_function_length"] = (
                        commit_metrics["lines_of_code"] / commit_metrics["functions_count"]
                    )
                
                # Recalcula acoplamento como média
                commit_metrics["coupling"] = (
                    commit_metrics["coupling"] / len(file_metrics)
                    if file_metrics else 0
                )
                
                # Calcula índice de manutenibilidade do commit
                from analyzer.maintainability_calculator import calculate_maintainability
                commit_metrics["maintainability_index"] = calculate_maintainability(
                    commit_metrics["complexity"],
                    commit_metrics["lines_of_code"],
                    commit_metrics["lines_of_code"]  # Usando LOC como proxy para volume
                )
            
            # Só adiciona se tem pelo menos um arquivo Python modificado
            if file_metrics:
                results.append(commit_metrics)

    except Exception as e:
        print(f"Erro ao acessar repositório: {e}")
        return []

    results.sort(key=lambda x: x["date"])
    return results