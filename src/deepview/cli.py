import typer

from deepview import __version__

app = typer.Typer(help="Explore and compare data from the command line.")


@app.callback()
def main():
    pass


@app.command()
def version():
    typer.echo(f"deepview {__version__}")

@app.command()
def purpose():
    typer.echo("This Command line tool was made by the developer because it " \
    " always looks so cool to view things at command line and it would be a fun" \
    " way to access data on CL and make someone who's not very comfortable with CL" \
    " to view and data.")