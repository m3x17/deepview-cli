import typer
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
import pandas as pd

from deepview.distributions import fit_distributions
from deepview import __version__
from deepview.loader import load_data
from deepview.summary import summarize

app = typer.Typer(help="Explore and compare data from the command line.")
console = Console()


@app.callback()
def main():
    pass


@app.command()
def version():
    typer.echo(f"deepview {__version__}")


@app.command()
def summary(path: str = typer.Argument(..., help="Path to a CSV or JSON file")):
    try:
        df = load_data(path)
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(code=1)

    try:
        stats = summarize(df)
        if stats.empty:
            console.print("[yellow]No numeric columns found.[/yellow]")
            raise typer.Exit(code=1)
        
        table = Table(title=f"Summary of {path} ({len(df)} rows)")
        for name in stats.columns:
            table.add_column(str(name), justify="left" if name == "column" else "right")
        for _, row in stats.iterrows():
            cells = [str(row["column"])]
            for name in stats.columns[1:]:
                value = row[name]
                cells.append(f"{int(value)}" if name in ("count", "missing") else f"{value:.2f}")
            table.add_row(*cells)
        console.print(table)
    except:   
        text_content = df["content"].iloc[0]
        
        console.rule(f"[bold blue]{path}[/bold blue]")
        console.print(Markdown(text_content))
        console.rule()

    
@app.command()
def dist(
    path: str = typer.Argument(..., help="Path to a CSV or JSON file"),
    column: str = typer.Option(..., "--column", "-c", help="Numeric column to fit"),
):
    try:
        df = load_data(path)
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(code=1)

    if column not in df.columns:
        console.print(f"[red]Column not found: {column}[/red]")
        raise typer.Exit(code=1)
    if not pd.api.types.is_numeric_dtype(df[column]):
        console.print(f"[red]Column is not numeric: {column}[/red]")
        raise typer.Exit(code=1)
    values = df[column].dropna()
    if len(values) < 10:
        console.print("[red]Need at least 10 values to fit distributions.[/red]")
        raise typer.Exit(code=1)

    fits = fit_distributions(values)
    if fits.empty:
        console.print("[yellow]No distribution could be fitted.[/yellow]")
        raise typer.Exit(code=1)

    table = Table(title=f"Distribution fits for '{column}' ({len(values)} values)")
    table.add_column("Rank", justify="right")
    table.add_column("Distribution")
    table.add_column("AIC", justify="right")
    table.add_column("KS", justify="right")
    table.add_column("Parameters")
    for rank, row in fits.iterrows():
        params = ", ".join(f"{p:.3f}" for p in row["params"])
        table.add_row(str(rank + 1), row["distribution"], f"{row['aic']:.1f}", f"{row['ks']:.3f}", params)
    console.print(table)

@app.command()
def purpose():
    typer.echo("This Command line tool was made by the developer because it " \
    " always looks so cool to view things at command line and it would be a fun" \
    " way to access data on CL and make someone who's not very comfortable with CL" \
    " to view and data.")