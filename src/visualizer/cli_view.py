from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from datetime import datetime
import statistics

console = Console()

def display_timeline(results):
    """
    Exibe a timeline evolutiva com visualizações avançadas.
    """
    if not results:
        console.print("[bold red]Nenhum commit encontrado![/bold red]")
        return

    # Layout principal com diferentes seções
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=2)
    )
    
    # Header
    layout["header"].update(Panel(
        Align.center("[bold cyan]CodeThermometer - Timeline Evolutiva de Código[/bold cyan]"),
        style="bold magenta"
    ))
    
    # Main content com split horizontal
    layout["main"].split_row(
        Layout(name="metrics_table", ratio=2),
        Layout(name="stats_panel", ratio=1)
    )
    
    # Tabela de métricas principal
    layout["metrics_table"].update(_create_metrics_table(results))
    
    # Painel de estatísticas
    layout["stats_panel"].update(_create_stats_panel(results))
    
    # Footer
    layout["footer"].update(Panel(
        Align.center("[bold yellow]✓ Análise concluída com sucesso![/bold yellow]"),
        style="green"
    ))
    
    console.print(layout)
    
    # Exibe gráfico evolutivo opcional
    _display_evolution_chart(results)


def _create_metrics_table(results):
    """Cria tabela interativa com todas as métricas."""
    table = Table(title="Histórico de Métricas", show_footer=True)
    
    # Colunas
    table.add_column("Data", style="cyan", width=12)
    table.add_column("Commit", style="magenta", width=8)
    table.add_column("Autor", style="green", width=18)
    table.add_column("CC", justify="right", style="yellow")
    table.add_column("Acoplamento", justify="right", style="blue")
    table.add_column("Manutenibilidade", justify="right", style="white")
    table.add_column("LOC", justify="right", width=6)
    table.add_column("Smells", justify="right", width=8)
    table.add_column("Tendência", justify="center", width=10)
    
    # Adiciona linhas com indicadores de tendência
    previous_complexity = None
    previous_smells = None
    
    for r in track(results, description="Gerando tabela..."):
        # Tendência de complexidade
        trend_cc = _get_trend_indicator(r.get("complexity"), previous_complexity)
        
        # Cor baseada em severity
        complexity_color = _get_severity_color(r.get("complexity", 0))
        # CORREÇÃO: usar "code_smells" em vez de "smells"
        smells_color = _get_smell_color(r.get("code_smells", 0))
        coupling_color = _get_coupling_color(r.get("coupling", 0))
        mi_color = _get_mi_color(r.get("maintainability_index", 50))
        
        # Formata a linha com cores
        table.add_row(
            r["date"].strftime("%Y-%m-%d") if hasattr(r["date"], "strftime") else str(r["date"]),
            r["hash"],
            r["author"][:18],
            Text(str(r.get("complexity", 0)), style=complexity_color),
            Text(f"{r.get('coupling', 0):.1f}", style=coupling_color),
            Text(f"{r.get('maintainability_index', 50):.1f}", style=mi_color),
            Text(str(r.get("lines_of_code", 0)), style="dim"),
            # CORREÇÃO: usar "code_smells" em vez de "smells"
            Text(str(r.get("code_smells", 0)), style=smells_color),
            trend_cc
        )
        
        previous_complexity = r.get("complexity")
        previous_smells = r.get("code_smells")
    
    return table


def _create_stats_panel(results):
    """Cria painel com estatísticas da evolução."""
    
    complexities = [r.get("complexity", 0) for r in results]
    # CORREÇÃO: usar "code_smells" em vez de "smells"
    smells_list = [r.get("code_smells", 0) for r in results]
    couplings = [r.get("coupling", 0) for r in results]
    maintainabilities = [r.get("maintainability_index", 50) for r in results]
    
    # Cálculos
    avg_complexity = statistics.mean(complexities) if complexities else 0
    max_complexity = max(complexities) if complexities else 0
    total_smells = sum(smells_list)
    avg_coupling = statistics.mean(couplings) if couplings else 0
    avg_maintainability = statistics.mean(maintainabilities) if maintainabilities else 0
    
    # Tendência geral
    if len(complexities) > 1:
        trend_cc = "↑" if complexities[-1] > complexities[0] else "↓" if complexities[-1] < complexities[0] else "→"
        trend_text = f"Complexidade {trend_cc}"
    else:
        trend_text = "Sem tendência"
    
    # Cria o texto do painel
    stats_text = (
        f"[bold cyan]ESTATÍSTICAS[/bold cyan]\n\n"
        f"[yellow]Commits:[/yellow] {len(results)}\n"
        f"[yellow]CC Médio:[/yellow] {avg_complexity:.1f}\n"
        f"[yellow]CC Máximo:[/yellow] {max_complexity}\n"
        f"[yellow]Total Smells:[/yellow] {total_smells}\n"
        f"[yellow]Acoplamento Médio:[/yellow] {avg_coupling:.1f}\n"
        f"[yellow]Manutenibilidade:[/yellow] {avg_maintainability:.1f}\n"
        f"[yellow]Tendência:[/yellow] {trend_text}"
    )
    
    return Panel(stats_text, style="blue")


def _display_evolution_chart(results):
    """Exibe um gráfico ASCII simples de evolução."""
    
    console.print("\n[bold cyan]Evolução da Complexidade[/bold cyan]")
    
    complexities = [r.get("complexity", 0) for r in results]
    if not complexities:
        return
    
    max_complexity = max(complexities)
    if max_complexity == 0:
        return
    
    # Cria gráfico ASCII (escala 40 caracteres)
    chart_width = 40
    for i, (r, cc) in enumerate(zip(results, complexities)):
        bar_length = int((cc / max_complexity) * chart_width)
        bar = "█" * bar_length + "░" * (chart_width - bar_length)
        
        # Data simplificada
        date_str = r["date"].strftime("%m-%d") if hasattr(r["date"], "strftime") else str(r["date"])[:5]
        
        console.print(f"{date_str} │{bar}│ {cc}")


def _get_severity_color(value):
    """Define cor baseada na complexidade."""
    if value > 20:
        return "bold red"
    elif value > 15:
        return "bold orange1"
    elif value > 10:
        return "bold yellow"
    else:
        return "bold green"


def _get_smell_color(value):
    """Define cor baseada na quantidade de smells."""
    if value >= 10:
        return "bold red"
    elif value >= 6:
        return "bold orange1"
    elif value >= 3:
        return "bold yellow"
    else:
        return "bold green"


def _get_coupling_color(value):
    """Define cor baseada no acoplamento."""
    if value > 7:
        return "bold red"
    elif value > 5:
        return "bold orange1"
    elif value > 3:
        return "bold yellow"
    else:
        return "bold green"


def _get_mi_color(value):
    """Define cor baseada no índice de manutenibilidade."""
    if value >= 85:
        return "bold green"
    elif value >= 70:
        return "bold yellow"
    elif value >= 50:
        return "bold orange1"
    else:
        return "bold red"


def _get_trend_indicator(current, previous):
    """Retorna indicador de tendência (↑ ↓ →)."""
    if previous is None:
        return Text("→", style="dim")
    
    if current > previous * 1.1:  # 10% de aumento
        return Text("↑", style="bold red")
    elif current < previous * 0.9:  # 10% de diminuição
        return Text("↓", style="bold green")
    else:
        return Text("→", style="dim")