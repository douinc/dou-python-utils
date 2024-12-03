# dou/cli.py

from pathlib import Path

import toml
import typer

app = typer.Typer(help="A simple CLI application for Dou Inc.")
install_app = typer.Typer(help="Install various configurations.")
app.add_typer(install_app, name="install")

PYPROJECT_TOML_CONTENT = """
[tool.ruff]
# Exclude commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
]

# Same as Black.
line-length = 88
indent-width = 4

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F"]
ignore = []

fixable = ["ALL"]
unfixable = []

dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
docstring-code-format = false
docstring-code-line-length = "dynamic"

[dependency-groups]
dev = ["pre-commit>=4.0.1", "ruff>=0.8.1"]
"""
PRE_COMMIT_CONFIG_CONTENT = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
        exclude: ^weekly/
      - id: check-yaml
      - id: check-json
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff
      - id: ruff-format
"""


@app.command()
def hello():
    typer.echo("Utils for Dou Inc.")


@app.command()
def goodbye(name: str):
    typer.echo(f"Goodbye {name}")


@install_app.command()
def formatting():
    """Install formatting configurations."""
    pyproject_path = Path("pyproject.toml")
    pre_commit_path = Path(".pre-commit-config.yaml")

    try:
        # Step 1: Load or create pyproject.toml
        if pyproject_path.exists():
            typer.echo("pyproject.toml found. Loading configuration.")
            with pyproject_path.open("r", encoding="utf-8") as f:
                pyproject_data = toml.load(f)
        else:
            typer.echo("Initiate a project using `uv init`")
            raise typer.Exit(code=1)

        # Step 2: Update pyproject.toml data
        if "tool" not in pyproject_data:
            pyproject_data["tool"] = {}
        if "ruff" not in pyproject_data["tool"]:
            # Parse the PYPROJECT_TOML_CONTENT string into a dictionary
            new_config = toml.loads(PYPROJECT_TOML_CONTENT)
            pyproject_data["tool"].update(new_config["tool"])
            typer.echo("Added Ruff configuration to pyproject.toml.")
        else:
            typer.echo("Ruff configuration already exists in pyproject.toml.")

        # Step 3: Write back to pyproject.toml
        with pyproject_path.open("w", encoding="utf-8") as f:
            toml.dump(pyproject_data, f)
        typer.echo("Updated pyproject.toml with Ruff configuration.")

        # Step 4: Create or overwrite .pre-commit-config.yaml
        with pre_commit_path.open("w", encoding="utf-8") as pre_commit_file:
            pre_commit_file.write(PRE_COMMIT_CONFIG_CONTENT)
        typer.echo("Created or updated .pre-commit-config.yaml.")

    except Exception as e:
        typer.echo(f"An error occurred: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
