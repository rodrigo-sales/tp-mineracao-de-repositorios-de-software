def detect_smells(analysis):
    """
    Regras heurísticas simples:
    - Funções com complexidade > 15
    - Funções com mais de 100 linhas
    """
    smells = 0
    for f in analysis.function_list:
        if f.cyclomatic_complexity > 15 or f.length > 100:
            smells += 1
    return smells