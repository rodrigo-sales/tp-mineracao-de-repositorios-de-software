import re
from collections import defaultdict

def detect_smells(analysis, source_code):
    """
    Detecta:
    1. Funções muito complexas (CC > 15)
    2. Funções muito longas (> 100 linhas)
    3. Métodos duplicados (código similar)
    4. Variáveis não utilizadas
    5. Imports não utilizados
    6. Funções aninhadas profundas
    7. Parâmetros em excesso
    8. Nomes genéricos (a, b, x, y, etc)
    
    Retorna:
        int: Total de code smells detectados
    """
    
    total_smells = 0
    
    # 1. Complexidade alta e funções longas
    total_smells += _detect_complex_functions(analysis)
    
    # 2. Código duplicado
    total_smells += _detect_code_duplication(source_code)
    
    # 3. Variáveis não utilizadas
    total_smells += _detect_unused_variables(source_code)
    
    # 4. Imports não utilizados
    total_smells += _detect_unused_imports(source_code)
    
    # 5. Aninhamento profundo
    total_smells += _detect_deep_nesting(source_code)
    
    # 6. Muitos parâmetros
    total_smells += _detect_many_parameters(analysis)
    
    # 7. Nomes genéricos
    total_smells += _detect_generic_names(source_code)
    
    return total_smells


def _detect_complex_functions(analysis):
    """Detecta funções com alta complexidade ou muitas linhas."""
    smells = 0
    thresholds = {
        'complexity_high': 15,
        'complexity_critical': 25,
        'length_high': 100,
        'length_critical': 200
    }
    
    for func in analysis.function_list:
        if func.cyclomatic_complexity > thresholds['complexity_critical']:
            smells += 2  # Smell crítico conta como 2
        elif func.cyclomatic_complexity > thresholds['complexity_high']:
            smells += 1
        
        if func.length > thresholds['length_critical']:
            smells += 2
        elif func.length > thresholds['length_high']:
            smells += 1
    
    return smells


def _detect_code_duplication(source_code):
    """Detecta padrões de código duplicado."""
    lines = source_code.split('\n')
    
    # Mapeia sequências de linhas similares
    line_map = defaultdict(int)
    smells = 0
    
    for i in range(len(lines) - 2):
        # Normaliza a linha (remove espaços, comentários)
        normalized = re.sub(r'#.*$', '', lines[i]).strip()
        
        if normalized and len(normalized) > 20:
            line_map[normalized] += 1
    
    # Linhas que aparecem 3+ vezes são consideradas duplicação
    for count in line_map.values():
        if count >= 3:
            smells += 1
    
    return min(smells, 5)  # Máximo 5 smells de duplicação


def _detect_unused_variables(source_code):
    """Detecta variáveis que são definidas mas nunca usadas."""
    smells = 0
    
    # Padrão: variáveis atribuídas
    assignment_pattern = r'^\s*(\w+)\s*='
    # Padrão: variáveis usadas
    usage_pattern = r'\b({var})\b'
    
    assignments = defaultdict(int)
    
    for match in re.finditer(assignment_pattern, source_code, re.MULTILINE):
        var_name = match.group(1)
        if not var_name.startswith('_'):  # Ignora convenção _ para unused
            assignments[var_name] += 1
    
    # Verifica se as variáveis são usadas
    for var_name in assignments.keys():
        pattern = usage_pattern.format(var=re.escape(var_name))
        uses = len(re.findall(pattern, source_code))
        
        # Se é atribuída mas nunca usada (ou usada só uma vez na atribuição)
        if uses <= 1 and assignments[var_name] > 0:
            smells += 1
    
    return min(smells, 5)


def _detect_unused_imports(source_code):
    """Detecta imports que não são utilizados."""
    smells = 0
    
    # Extrai todos os imports
    import_pattern = r'^(?:from\s+(\w+)\s+import|import\s+(\w+))'
    
    for match in re.finditer(import_pattern, source_code, re.MULTILINE):
        module = match.group(1) or match.group(2)
        
        # Verifica se o módulo é usado no código
        usage_count = len(re.findall(rf'\b{module}\b', source_code))
        
        if usage_count <= 1:  # Apenas a linha de import
            smells += 1
    
    return min(smells, 3)


def _detect_deep_nesting(source_code):
    """Detecta aninhamento profundo de blocos (if, for, while, etc)."""
    smells = 0
    max_depth = 0
    current_depth = 0
    
    # Caracteres que indicam abertura/fechamento de blocos
    opening = {':', '(', '[', '{'}
    closing = {':', ')', ']', '}'}
    
    for line in source_code.split('\n'):
        stripped = line.strip()
        
        # Conta a profundidade de indentação
        indent_level = (len(line) - len(line.lstrip())) // 4
        
        # Se tem dois pontos no final, é início de bloco
        if stripped.endswith(':'):
            current_depth = indent_level
            max_depth = max(max_depth, current_depth)
    
    # Aninhamento profundo (5+ níveis) é um smell
    if max_depth >= 5:
        smells += 2
    elif max_depth >= 4:
        smells += 1
    
    return smells


def _detect_many_parameters(analysis):
    """Detecta funções com muitos parâmetros."""
    smells = 0
    threshold = 5
    
    for func in analysis.function_list:
        # Lizard fornece informação sobre parâmetros
        if hasattr(func, 'parameters') and len(func.parameters) > threshold:
            smells += 1
    
    return smells


def _detect_generic_names(source_code):
    """Detecta nomes de variáveis genéricos ou muito curtos."""
    smells = 0
    
    # Nomes muito genéricos
    generic_names = {'a', 'b', 'c', 'x', 'y', 'z', 'i', 'j', 'k', 'tmp', 'temp', 'data', 'value', 'var'}
    
    # Padrão: atribuição de variável
    pattern = r'^\s*(\w+)\s*='
    
    for match in re.finditer(pattern, source_code, re.MULTILINE):
        var_name = match.group(1)
        
        if var_name in generic_names and len(var_name) <= 3:
            smells += 1
    
    return min(smells, 3)