from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

def display_timeline(results):
    if not results:
        console.print("[bold red]Nenhum commit encontrado![/bold red]")
        return

    table = Table(title="CodeThermometer 🔥 - Timeline de Evolução")
    table.add_column("Data", style="cyan")
    table.add_column("Commit", style="magenta")
    table.add_column("Autor", style="green")
    table.add_column("Complexidade", justify="right")
    table.add_column("Smells", justify="right")

    for r in track(results, description="Gerando relatório..."):
        table.add_row(
            r["date"].strftime("%Y-%m-%d"),
            r["hash"],
            r["author"],
            str(r["complexity"]),
            str(r["smells"])
        )

    console.print(table)
    console.print("\n[bold yellow]Análise concluída![/bold yellow]")