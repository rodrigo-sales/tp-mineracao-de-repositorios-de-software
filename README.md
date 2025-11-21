# Engenharia de Software II - Ferramenta CodeThermometer

Ferramenta de análise evolutiva de código que utiliza mineração de repositórios para identificar a progressão de complexidade, acoplamento e code smells ao longo do tempo.  

## Membros do Grupo

- Deborah Vieira Vilas Boas de Almeida 
- Isabela Saenz Cardoso
- Lucas Almeida Santos de Souza
- Rodrigo Sales Nascimento
---

## 1. Visão Geral

O CodeThermometer analisa o histórico de commits de um repositório Git hospedado (por exemplo, GitHub) e calcula métricas de qualidade de código para cada versão.  
Os resultados são apresentados em uma linha do tempo no terminal, exibindo a evolução da complexidade e a ocorrência de possíveis problemas ao longo do tempo.

---

## 2. Tecnologias utilizadas

- **Python 3.8+**
- **PyDriller** – extração e análise de commits
- **GitPython** – dependência interna do PyDriller
- **Lizard** – cálculo de métricas de código
- **Click** – interface de linha de comando (CLI)
- **Rich** – visualização formatada no terminal

---

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

Analisar um repositório:

```bash
python src/main.py analyze https://github.com/usuario/repositorio
```

Com filtro de datas:

```bash
python src/main.py analyze https://github.com/usuario/repositorio --since 2025-01-01 --until 2025-12-31
```

Modo verbose (estatísticas por autor):

```bash
python src/main.py analyze https://github.com/usuario/repositorio -v
```

Gerar relatório agregado:

```bash
python src/main.py report https://github.com/usuario/repositorio
```

## Métricas Coletadas

- Complexidade Cíclomática (CC)
- Acoplamento (0-10)
- Índice de Manutenibilidade (0-100)
- Linhas de Código (LOC)
- Code Smells (8 tipos detectados)
- Contagem de Funções
- Comprimento Médio de Função

## Detecção de Code Smells

Detecta 8 tipos de problemas:

1. Funções muito complexas (CC > 15)
2. Funções muito longas (> 100 linhas)
3. Código duplicado
4. Variáveis não utilizadas
5. Imports não utilizados
6. Aninhamento profundo (> 5 níveis)
7. Muitos parâmetros (> 5)
8. Nomes genéricos

## Visualização

A ferramenta exibe:

- Tabela de métricas por commit
- Painel de estatísticas agregadas
- Indicadores de tendência
- Gráfico ASCII de evolução

## Testes

Executar testes:

```bash
pytest tests/ -v
```

Com cobertura:

```bash
pytest tests/ --cov=analyzer --cov=visualizer
```