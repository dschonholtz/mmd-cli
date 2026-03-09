# mmd CLI — Claude Project Context

## What This Repo Is

`mmd` is the **Unreal Engine CLI** for MultiMagicDungeon. Its scope is strictly:
**wrapping Unreal Engine processes** — compile, test, package, log, and editor automation.

It is NOT a general project CLI. Supabase tooling, server deploy, and other concerns
belong in separate, single-purpose CLI tools when those needs arise.

The game repo: https://github.com/dschonholtz/MultiMagicDungeon
Included as a git submodule at `tools/mmd-cli/`.

---

## Scope Boundary

**In scope — Unreal Engine interactions only:**
- UnrealBuildTool (compile client, compile server)
- UnrealAutomationTool (package)
- UE automation test runner (headless commandlet)
- UE log file streaming (`Saved/Logs/`)
- UE Remote Control API (editor automation — future)

**Out of scope — belongs in a separate tool:**
- Database / Supabase operations → future `mmd-db` tool
- Server deploy / SSH / rsync → future `mmd-deploy` tool
- Any non-UE subprocess

If you find yourself adding a command that doesn't invoke a UE binary or the Remote Control API,
stop and ask whether it belongs here.

---

## What This Tool Can Do

### Currently implemented
| Command | What it does |
|---|---|
| `mmd build client` | Compiles the UE5 game client (Win64) via UnrealBuildTool |
| `mmd build server` | Compiles the Linux dedicated server target via UBT |
| `mmd test run [filter]` | Runs UE automation tests headlessly, parses pass/fail from log |
| `mmd logs local [-f]` | Tails `Saved/Logs/<name>.log` in real time |

### Planned UE commands (add when the phase needs it)
| Command | Phase | What it will do |
|---|---|---|
| `mmd package client` | 5 | Package game client via UAT |
| `mmd package server` | 5 | Package Linux dedicated server via UAT |
| `mmd editor <cmd>` | TBD | Remote Control API calls into running UE editor |

---

## What This Tool Cannot Do

- **Cannot open or control the Unreal Editor UI** — headless processes only.
  Blueprint visual editing requires the Remote Control API plugin (future).
- **Cannot hot-reload C++** — that is Live Coding, editor-only.
- **Cannot run on Linux** — calls Windows `.bat` files. Server binary cross-compiles
  to Linux but the CLI itself runs on Windows.
- **Cannot replace PIE** — multiplayer testing requires launching PIE from the UE editor.

---

## Architecture

```
mmd/
├── config.py   # Engine + project paths. One place to edit.
├── main.py     # Typer app — registers sub-apps only
├── build.py    # mmd build — wraps UBT
├── test.py     # mmd test — wraps UnrealEditor-Cmd automation commandlet
└── logs.py     # mmd logs — tails UE log files
tests/
├── test_config.py
└── (one test file per module)
```

**Adding a UE command:**
1. Create `mmd/<domain>.py` with `app = typer.Typer(...)`
2. Register in `main.py`: `app.add_typer(domain.app, name="domain")`
3. Add deps to `pyproject.toml` if needed, run `uv sync`
4. Add a test in `tests/test_<domain>.py` using `pytest-subprocess`
5. Document here

---

## Dev Setup

```bash
winget install astral-sh.uv   # if not installed
uv sync                        # creates .venv, installs deps
uv run mmd --help
uv run ruff check .
uv run mypy mmd/
uv run pytest
```

---

## Conventions

- **All paths in `config.py`** — never hardcode engine/project paths elsewhere
- **`.bat` files via `cmd /c`** — bash cannot call them directly on Windows
- **Exit code 0 = success, non-zero = failure** — the pre-commit gate reads exit codes
- **`typer.echo()` not `print()`** — stdout; `typer.echo(..., err=True)` for stderr
- **`raise typer.Exit(1)`** not `sys.exit()` for error exits
- **Never call real UBT/UE in tests** — use `pytest-subprocess` to mock subprocess calls
