import re
from collections import defaultdict

def analyze_coupling(source_code):
    """
    Analisa o acoplamento externo (dependências) do código.
    
    Métricas:
    - Número de imports externos
    - Número de classes/funções usadas de outros módulos
    - Índice de acoplamento efetivo
    
    Retorna:
        float: Score de acoplamento (0.0 - 10.0)
    """
    
    # Imports externos
    imports = _count_external_imports(source_code)
    
    # Referências cruzadas
    cross_references = _count_cross_references(source_code)
    
    # Análise de dependências internas
    internal_deps = _analyze_internal_dependencies(source_code)
    
    # Cálculo do índice de acoplamento (escala 0-10)
    # Baseado em: imports + referências cruzadas + dependências internas
    coupling_score = min(10.0, (imports * 0.5 + cross_references * 0.3 + internal_deps * 0.2))
    
    return coupling_score


def _count_external_imports(source_code):
    """Conta imports externos (não-stdlib e não-locais)."""
    import_patterns = [
        r'^import\s+(\w+)',
        r'^from\s+(\w+)\s+import',
        r'^\s+import\s+(\w+)',
        r'^\s+from\s+(\w+)\s+import'
    ]
    
    stdlib_modules = {
        'os', 'sys', 're', 'json', 'time', 'datetime', 'collections',
        'itertools', 'functools', 'math', 'random', 'logging', 'unittest'
    }
    
    imports = set()
    for pattern in import_patterns:
        matches = re.findall(pattern, source_code, re.MULTILINE)
        for match in matches:
            module_name = match.split('.')[0]
            if module_name not in stdlib_modules and not module_name.startswith('_'):
                imports.add(module_name)
    
    return len(imports)


def _count_cross_references(source_code):
    """Conta referências a outros módulos/classes dentro do código."""
    # Padrão: Class.method() ou module.function()
    pattern = r'(\w+)\.(\w+)\s*\('
    references = len(re.findall(pattern, source_code))
    return min(references / 10, 5)  # Normaliza para escala 0-5


def _analyze_internal_dependencies(source_code):
    """Analisa dependências entre funções/classes internas."""
    
    # Extrai definições de classes e funções
    class_pattern = r'class\s+(\w+)'
    func_pattern = r'def\s+(\w+)'
    
    classes = set(re.findall(class_pattern, source_code))
    functions = set(re.findall(func_pattern, source_code))
    defined_items = classes | functions
    
    # Conta referências a items definidos
    dependency_count = 0
    for item in defined_items:
        # Conta quantas vezes cada item é referenciado
        pattern = rf'\b{item}\s*\('
        refs = len(re.findall(pattern, source_code))
        if refs > 1:  # Mais de uma referência indica dependência
            dependency_count += 1
    
    return min(dependency_count / 5, 3)  # Normaliza para escala 0-3