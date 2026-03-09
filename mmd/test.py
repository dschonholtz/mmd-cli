"""Test runner — invokes UE automation tests headlessly via UnrealEditor-Cmd."""
import subprocess
import re
import typer
from .config import EDITOR_CMD, PROJECT_FILE, LOG_DIR

app = typer.Typer(help="Run Unreal automation tests.")

# Matches lines like: LogAutomationController: Test Succeeded: MMD.Core.PlayerState
_RESULT_RE = re.compile(r"(Test Succeeded|Test Failed|Error): (.+)")


@app.command()
def run(
    filter: str = typer.Argument("MMD", help="Test filter prefix, e.g. 'MMD' or 'MMD.Core'"),
):
    """Run automation tests matching FILTER and report pass/fail."""
    typer.echo(f"Running tests: {filter}")
    log_file = LOG_DIR / "AutomationTest.log"

    cmd = [
        str(EDITOR_CMD),
        str(PROJECT_FILE),
        "-ExecCmds=Automation RunTests {filter}; Quit".format(filter=filter),
        "-unattended",
        "-nopause",
        "-nosplash",
        f"-log={log_file}",
        "-nullrhi",
    ]

    result = subprocess.run(["cmd", "/c"] + cmd, capture_output=True, text=True)

    if not log_file.exists():
        typer.echo("No log file produced — editor may have crashed.", err=True)
        raise typer.Exit(1)

    passed, failed = [], []
    for line in log_file.read_text(encoding="utf-8", errors="replace").splitlines():
        m = _RESULT_RE.search(line)
        if m:
            (passed if "Succeeded" in m.group(1) else failed).append(m.group(2))

    for name in passed:
        typer.echo(f"  PASS  {name}")
    for name in failed:
        typer.echo(f"  FAIL  {name}", err=True)

    typer.echo(f"\n{len(passed)} passed, {len(failed)} failed.")
    if failed:
        raise typer.Exit(1)
