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

## 3. Estrutura do projeto

```
code_thermometer/
│
├── main.py
├── analyzer/
│   ├── repo_miner.py
│   ├── metrics_extractor.py
│   └── smell_detector.py
└── visualizer/
    └── cli_view.py
```

---

## 4. Instalação

1. Clone o repositório do CodeThermometer

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Verifique se o Git está instalado e configurado:

```bash
git --version
```

Caso esse comando retorne um erro, instale o Git:  
https://git-scm.com/download/win

---

## 5. Execução

Para executar a análise em um repositório público:

```bash
python main.py analyze https://github.com/pallets/flask.git --since 2025-01-01
```

**Parâmetros opcionais:**

- `--since`: data inicial no formato YYYY-MM-DD
- `--until`: data final no formato YYYY-MM-DD

**Exemplo:**

```bash
python main.py analyze https://github.com/psf/requests.git --since 2025-01-01 --until 2025-10-31
```

---

## 6. Saída esperada

O resultado será exibido em formato de tabela no terminal:

```
CodeThermometer - Timeline de Evolução

┏━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Data       ┃ Commit    ┃ Autor      ┃ Complexidade┃ Smells  ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━┩
│ 2023-02-10 │ 3f21a7e   │ Armin Ron… │ 123         │ 4       │
│ 2023-05-03 │ 7ac8b99   │ David Lor… │ 140         │ 7       │
│ 2023-10-11 │ b5120cc   │ Jorge San… │ 111         │ 3       │
└────────────┴───────────┴────────────┴─────────────┴─────────┘

Análise concluída!
```

---

## 7. Troubleshooting

### Erro: "Bad git executable" ou "Failed to initialize GitPython"

O PyDriller depende do GitPython, que precisa acessar o executável do Git.  
Se o Git não for encontrado, execute os passos abaixo:

1. Verifique se o Git está instalado:

```bash
git --version
```

2. Caso o Git esteja instalado mas o erro persista, adicione-o ao PATH:

```bash
setx PATH "%PATH%;C:\Program Files\Git\cmd"
```

3. Ou defina explicitamente para o Python:

```bash
setx GIT_PYTHON_GIT_EXECUTABLE "C:\Program Files\Git\cmd\git.exe"
```

4. Feche e reabra o VS Code (ou terminal) e tente novamente:

```bash
python main.py analyze <url-do-repositorio>
```

### Erro: "Nenhum commit encontrado"

- Verifique se a URL é de um repositório Git válido.
- Confirme que o repositório é público (PyDriller não acessa repositórios privados sem token).
- Use o parâmetro `--since` apenas se o repositório possuir commits após essa data.

### Erro: "Permission denied" ou "SSL error"

- Certifique-se de estar conectado à internet.
- Se estiver em rede corporativa, configure o proxy do Git:

```bash
git config --global http.proxy http://proxy:porta
```

---

## 8. Próximos passos

- Adicionar detecção de acoplamento entre módulos.

- Exportar resultados em CSV ou JSON.

- Adicionar pelo menos 10 testes de unidade.
Os testes devem ser executados automaticamente via GitHub Actions.
