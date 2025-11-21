import lizard
from analyzer.smell_detector import detect_smells
from analyzer.coupling_analyzer import analyze_coupling
from analyzer.maintainability_calculator import calculate_maintainability

def extract_metrics(source_code, filename="temp.py"):
    """
    Extrai métricas abrangentes do código.
    
    Retorna:
        dict: {
            'cyclomatic_complexity': int,
            'coupling': float,
            'maintainability_index': float,
            'lines_of_code': int,
            'code_smells': int,
            'functions_count': int,
            'avg_function_length': float
        }
    """
    try:
        analysis = lizard.analyze_file.analyze_source_code(filename, source_code)
        
        # Complexidade cíclomática
        total_complexity = sum(f.cyclomatic_complexity for f in analysis.function_list)
        
        # Acoplamento
        coupling = analyze_coupling(source_code)
        
        # Linhas de código - CORRIGIDO: usar nloc em vez de loc
        # nloc = non-comment lines of code (mais preciso)
        lines_of_code = analysis.nloc if hasattr(analysis, 'nloc') else len(source_code.split('\n'))
        
        # Índice de manutenibilidade
        # Usar token_count como proxy para halstead_volume
        token_count = analysis.token_count if hasattr(analysis, 'token_count') else lines_of_code
        
        maintainability = calculate_maintainability(
            cyclomatic_complexity=total_complexity,
            loc=lines_of_code,
            halstead_volume=token_count
        )
        
        # Code smells avançados
        code_smells = detect_smells(analysis, source_code)
        
        # Métricas adicionais
        functions_count = len(analysis.function_list)
        avg_function_length = (
            lines_of_code / functions_count if functions_count > 0 else 0
        )
        
        return {
            'cyclomatic_complexity': int(total_complexity),
            'coupling': round(coupling, 2),
            'maintainability_index': round(maintainability, 2),
            'lines_of_code': int(lines_of_code),
            'code_smells': int(code_smells),
            'functions_count': int(functions_count),
            'avg_function_length': round(avg_function_length, 2)
        }
    
    except Exception as e:
        print(f"Erro ao analisar {filename}: {e}")
        return {
            'cyclomatic_complexity': 0,
            'coupling': 0.0,
            'maintainability_index': 100.0,
            'lines_of_code': 0,
            'code_smells': 0,
            'functions_count': 0,
            'avg_function_length': 0.0
        }