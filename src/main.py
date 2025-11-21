import click
from analyzer.repo_miner import analyze_repository
from visualizer.cli_view import display_timeline

@click.group()
def cli():
    pass

@cli.command()
@click.argument("repo_url", required=True)
@click.option("--since", default=None, help="Data inicial no formato YYYY-MM-DD")
@click.option("--until", default=None, help="Data final no formato YYYY-MM-DD")
@click.option("--verbose", "-v", is_flag=True, help="Modo verbose com mais detalhes")
def analyze(repo_url, since, until, verbose):
    """
    Analisa a evolução de métricas de um repositório Git.
    
    Exemplo:
        python src/main.py analyze https://github.com/user/repo
        python src/main.py analyze https://github.com/user/repo --since 2025-01-01 --until 2025-12-31
    """
    click.echo(click.style("CodeThermometer - Iniciando análise...", fg="cyan", bold=True))
    
    try:
        # Analisa repositório
        click.echo(f"Analisando repositório: {repo_url}")
        results = analyze_repository(repo_url, since, until)
        
        if not results:
            click.echo(click.style("Nenhum resultado encontrado!", fg="red", bold=True))
            return
        
        click.echo(click.style(f"Análise concluída: {len(results)} commits processados", fg="green"))
        
        # Exibe timeline
        display_timeline(results)
        
        # Modo verbose: exibe mais detalhes
        if verbose:
            _print_verbose_stats(results)
        
    except Exception as e:
        click.echo(click.style(f"Erro: {str(e)}", fg="red", bold=True))
        if verbose:
            import traceback
            traceback.print_exc()
        raise click.Exit(1)


@cli.command()
@click.argument("repo_url", required=True)
@click.option("--since", default=None, help="Data inicial no formato YYYY-MM-DD")
@click.option("--until", default=None, help="Data final no formato YYYY-MM-DD")
def report(repo_url, since, until):
    """
    Gera um relatório detalhado de análise evolutiva.
    """
    click.echo(click.style("Gerando relatório...", fg="cyan", bold=True))
    
    results = analyze_repository(repo_url, since, until)
    
    if not results:
        click.echo(click.style("Nenhum resultado encontrado!", fg="red"))
        return
    
    # Calcula estatísticas agregadas
    stats = _calculate_aggregated_stats(results)
    
    # Exibe relatório
    click.echo("\n" + "="*80)
    click.echo(click.style("RELATÓRIO DE EVOLUÇÃO DE CÓDIGO", fg="cyan", bold=True).center(80))
    click.echo("="*80)
    
    click.echo(f"\nRepositório: {repo_url}")
    click.echo(f"Total de commits analisados: {stats['total_commits']}")
    click.echo(f"Período: {stats['first_date']} até {stats['last_date']}")
    click.echo(f"Autores: {stats['total_authors']}")
    
    click.echo("\n" + "-"*80)
    click.echo(click.style("COMPLEXIDADE", fg="yellow", bold=True))
    click.echo("-"*80)
    click.echo(f"  Média: {stats['avg_complexity']:.2f}")
    click.echo(f"  Máxima: {stats['max_complexity']}")
    click.echo(f"  Mínima: {stats['min_complexity']}")
    click.echo(f"  Tendência: {stats['complexity_trend']}")
    
    click.echo("\n" + "-"*80)
    click.echo(click.style("CODE SMELLS", fg="red", bold=True))
    click.echo("-"*80)
    click.echo(f"  Total: {stats['total_smells']}")
    click.echo(f"  Média por commit: {stats['avg_smells']:.2f}")
    click.echo(f"  Commit com mais smells: {stats['worst_commit_smells']}")
    
    click.echo("\n" + "-"*80)
    click.echo(click.style("MANUTENIBILIDADE", fg="green", bold=True))
    click.echo("-"*80)
    click.echo(f"  Índice médio: {stats['avg_maintainability']:.2f}")
    click.echo(f"  Saúde geral: {stats['health_level']}")
    
    click.echo("\n" + "-"*80)
    click.echo(click.style("ACOPLAMENTO", fg="blue", bold=True))
    click.echo("-"*80)
    click.echo(f"  Score médio: {stats['avg_coupling']:.2f}")
    
    click.echo("\n" + "="*80)


def _print_verbose_stats(results):
    """Exibe estatísticas detalhadas em modo verbose."""
    click.echo("\n" + click.style("ESTATÍSTICAS DETALHADAS", fg="cyan", bold=True))
    
    # Agrupa por autor
    by_author = {}
    for r in results:
        author = r['author']
        if author not in by_author:
            by_author[author] = []
        by_author[author].append(r)
    
    click.echo("\nCommits por autor:")
    for author, commits in sorted(by_author.items(), key=lambda x: len(x[1]), reverse=True):
        avg_cc = sum(c.get('complexity', 0) for c in commits) / len(commits)
        # CORREÇÃO: usar "code_smells" em vez de "smells"
        total_smells = sum(c.get('code_smells', 0) for c in commits)
        click.echo(f"  {author:20} - {len(commits):3} commits (CC avg: {avg_cc:.1f}, smells: {total_smells})")


def _calculate_aggregated_stats(results):
    """Calcula estatísticas agregadas dos resultados."""
    import statistics
    from datetime import datetime
    
    complexities = [r.get('complexity', 0) for r in results]
    # CORREÇÃO: usar "code_smells" em vez de "smells"
    smells = [r.get('code_smells', 0) for r in results]
    couplings = [r.get('coupling', 0) for r in results]
    maintainabilities = [r.get('maintainability_index', 50) for r in results]
    
    # Tendência de complexidade
    if len(complexities) > 1:
        trend = "↑ Piorando" if complexities[-1] > complexities[0] else "↓ Melhorando" if complexities[-1] < complexities[0] else "→ Estável"
    else:
        trend = "→ Indeterminado"
    
    # Nível de saúde
    avg_mi = statistics.mean(maintainabilities)
    if avg_mi >= 85:
        health = "Excelente"
    elif avg_mi >= 70:
        health = "Bom"
    elif avg_mi >= 50:
        health = "Aceitável"
    else:
        health = "Crítico"
    
    # Autores
    unique_authors = len(set(r['author'] for r in results))
    
    return {
        'total_commits': len(results),
        'total_authors': unique_authors,
        'first_date': results[0]['date'].strftime("%Y-%m-%d") if results else "N/A",
        'last_date': results[-1]['date'].strftime("%Y-%m-%d") if results else "N/A",
        'avg_complexity': statistics.mean(complexities) if complexities else 0,
        'max_complexity': max(complexities) if complexities else 0,
        'min_complexity': min(complexities) if complexities else 0,
        'complexity_trend': trend,
        'total_smells': sum(smells),
        'avg_smells': statistics.mean(smells) if smells else 0,
        'worst_commit_smells': max(smells) if smells else 0,
        'avg_maintainability': statistics.mean(maintainabilities) if maintainabilities else 50,
        'health_level': health,
        'avg_coupling': statistics.mean(couplings) if couplings else 0
    }


if __name__ == "__main__":
    cli()