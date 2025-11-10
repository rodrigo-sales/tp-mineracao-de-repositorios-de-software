import click
from analyzer.repo_miner import analyze_repository
from visualizer.cli_view import display_timeline

@click.group()
def cli():
    """CodeThermometer - Análise Evolutiva de Código"""
    pass

@cli.command()
@click.argument("repo_url")
@click.option("--since", default=None, help="Data inicial no formato YYYY-MM-DD")
@click.option("--until", default=None, help="Data final no formato YYYY-MM-DD")
def analyze(repo_url, since, until):
    """Analisa a evolução de métricas de um repositório."""
    results = analyze_repository(repo_url, since, until)
    display_timeline(results)

if __name__ == "__main__":
    cli()
