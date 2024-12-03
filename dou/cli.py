# dou/cli.py

import typer

app = typer.Typer(help="A simple CLI application for dou.")


@app.command()
def hello():
    typer.echo("Utils for Dou Inc.")


# Additional commands can be added here


def main():
    app()
