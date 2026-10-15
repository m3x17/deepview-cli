import typer
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

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
        # Pull out the clean text we extracted inside load_data
        text_content = df["content"].iloc[0]
        
        # Print a stylish divider and the formatted Markdown text
        console.rule(f"[bold blue]{path}[/bold blue]")
        console.print(Markdown(text_content))
        console.rule()

    

@app.command()
def purpose():
    typer.echo("This Command line tool was made by the developer because it " \
    " always looks so cool to view things at command line and it would be a fun" \
    " way to access data on CL and make someone who's not very comfortable with CL" \
    " to view and data.")