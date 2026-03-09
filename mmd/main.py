"""Entry point — `python -m mmd` or `mmd` after pip install -e ."""
import typer
from . import build, test, logs

app = typer.Typer(
    name="mmd",
    help="MultiMagicDungeon dev CLI. Commands grow as the project does.",
    no_args_is_help=True,
)

app.add_typer(build.app, name="build")
app.add_typer(test.app,  name="test")
app.add_typer(logs.app,  name="logs")

if __name__ == "__main__":
    app()
