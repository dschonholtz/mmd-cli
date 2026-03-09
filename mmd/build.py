"""Build commands — wraps UnrealBuildTool."""
import subprocess
import sys
import typer
from .config import UBT, PROJECT_FILE

app = typer.Typer(help="Compile the project via UnrealBuildTool.")


def _run_ubt(target: str, platform: str, config: str) -> int:
    cmd = [
        str(UBT),
        target,
        platform,
        config,
        f"-Project={PROJECT_FILE}",
        "-WaitMutex",
    ]
    # UBT is a .bat file — must run via cmd.exe on Windows
    result = subprocess.run(["cmd", "/c"] + cmd, text=True)
    return result.returncode


@app.command()
def client(
    config: str = typer.Option("Development", help="Build config: Development|Shipping|DebugGame"),
):
    """Compile the game client (Win64)."""
    typer.echo(f"Building client [{config}]...")
    code = _run_ubt("MultiMagicDungeon", "Win64", config)
    if code != 0:
        typer.echo("Build FAILED.", err=True)
        raise typer.Exit(code)
    typer.echo("Build succeeded.")


@app.command()
def server(
    config: str = typer.Option("Development", help="Build config"),
):
    """Compile the dedicated server target (Linux)."""
    typer.echo(f"Building server [{config}] for Linux...")
    code = _run_ubt("MultiMagicDungeonServer", "Linux", config)
    if code != 0:
        typer.echo("Server build FAILED.", err=True)
        raise typer.Exit(code)
    typer.echo("Server build succeeded.")
