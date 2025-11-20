import math

def calculate_maintainability(cyclomatic_complexity, loc, halstead_volume):
    """
    Calcula o Índice de Manutenibilidade (MI) do código.
    
    Baseia-se em:
    - Complexidade cíclomática
    - Linhas de código
    - Volume Halstead (medida de esforço/complexidade baseada em tokens)
    
    Retorna:
        float: MI score (0.0 - 100.0)
        - 85-100: Altamente manutenível (verde)
        - 70-84: Moderadamente manutenível (amarelo)
        - 50-69: Baixa manutenibilidade (laranja)
        - < 50: Crítica (vermelho)
    """
    
    if loc == 0:
        return 100.0
    
    try:
        # Cálculo do Volume Halstead se não fornecido
        if halstead_volume == 0:
            halstead_volume = loc
        
        # Cálculo do MI base usando fórmula publicada
        mi = 171 - 5.2 * math.log(halstead_volume) - 0.23 * cyclomatic_complexity - 16.2 * math.log(loc)
        
        # Normaliza para escala 0-100
        mi = max(0, min(100, mi))
        
        return round(mi, 2)
    
    except (ValueError, ZeroDivisionError):
        # Fallback em caso de erro
        return 50.0


def get_maintainability_level(mi_score):
    """
    Retorna o nível de manutenibilidade com cor e descrição.
    
    Retorna:
        dict: {
            'level': str,
            'color': str,
            'description': str
        }
    """
    if mi_score >= 85:
        return {
            'level': 'Excelente',
            'color': 'green',
            'description': 'Código altamente manutenível'
        }
    elif mi_score >= 70:
        return {
            'level': 'Bom',
            'color': 'yellow',
            'description': 'Código moderadamente manutenível'
        }
    elif mi_score >= 50:
        return {
            'level': 'Aceitável',
            'color': 'orange',
            'description': 'Código com problemas de manutenibilidade'
        }
    else:
        return {
            'level': 'Crítico',
            'color': 'red',
            'description': 'Código requer refatoração urgente'
        }


def get_complexity_level(complexity):
    """
    Classifica o nível de complexidade cíclomática.
    
    Referência: Complexidade Cíclomática de McCabe
    - 1-5: Simples
    - 6-10: Moderada
    - 11-20: Alta
    - 21+: Muito Alta (crítica)
    """
    if complexity <= 5:
        return 'Simples'
    elif complexity <= 10:
        return 'Moderada'
    elif complexity <= 20:
        return 'Alta'
    else:
        return 'Crítica'