"""Log streaming — local Saved/Logs/ or remote server via SSH."""
import time
import typer
from .config import LOG_DIR

app = typer.Typer(help="Stream game/server logs.")


@app.command()
def local(
    name: str = typer.Argument("MultiMagicDungeon", help="Log file stem (no .log extension)"),
    follow: bool = typer.Option(True, "--follow/--no-follow", "-f/-F"),
):
    """Tail a log file from Saved/Logs/."""
    log_file = LOG_DIR / f"{name}.log"
    if not log_file.exists():
        typer.echo(f"Log not found: {log_file}", err=True)
        raise typer.Exit(1)

    with log_file.open(encoding="utf-8", errors="replace") as f:
        f.seek(0, 2)  # seek to end
        while True:
            line = f.readline()
            if line:
                typer.echo(line, nl=False)
            elif follow:
                time.sleep(0.1)
            else:
                break
