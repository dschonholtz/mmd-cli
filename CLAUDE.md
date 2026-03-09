# mmd CLI — Claude Project Context

## What This Repo Is

`mmd` is the developer CLI for MultiMagicDungeon, an Unreal Engine 5.7 multiplayer game.
It is a **pure Python tool** — no C++, no Unreal code. It wraps external processes and APIs
so that both the developer and Claude Code can drive the UE build pipeline, test runner,
server deployment, and backend from the command line.

The game repo lives at: https://github.com/dschonholtz/MultiMagicDungeon
This CLI is included there as a git submodule at `tools/mmd-cli/`.

---

## What This Tool Can Do

### Currently implemented
| Command | What it does |
|---|---|
| `mmd build client` | Compiles the UE5 game client (Win64) via UnrealBuildTool |
| `mmd build server` | Compiles the Linux dedicated server target via UBT |
| `mmd test run [filter]` | Runs UE automation tests headlessly, parses pass/fail from log |
| `mmd logs local [-f]` | Tails `Saved/Logs/<name>.log` in real time |

### Planned (not yet implemented — add when the phase needs it)
| Command | Phase | What it will do |
|---|---|---|
| `mmd package` | 5 | Package client or server via UAT |
| `mmd deploy` | 5 | rsync server binary to Hetzner VPS + restart service |
| `mmd logs remote [-f]` | 5 | SSH tail from Hetzner server |
| `mmd db migrate` | 4 | Push Supabase schema migrations |
| `mmd db seed` | 4 | Seed local/dev Supabase data |
| `mmd editor <cmd>` | TBD | Remote Control API calls into running UE editor |

---

## What This Tool Cannot Do

- **Cannot open or control the Unreal Editor UI** — it drives headless processes only.
  Blueprint visual editing is not possible through this CLI without the Remote Control
  API plugin being enabled (planned for a future phase).
- **Cannot hot-reload C++ into a running editor** — that is Live Coding, editor-only.
- **Cannot talk to Supabase yet** — db commands are stubs until Phase 4.
- **Cannot run on Linux** — build commands call Windows .bat files. The server build
  cross-compiles to Linux but the CLI itself runs on Windows.
- **Cannot replace PIE (Play In Editor)** — multiplayer testing still requires the
  developer to launch PIE from the UE editor with multiple players.

---

## Architecture

```
mmd/
├── config.py      # All paths (engine, project, logs). Single place to edit.
├── main.py        # Typer app wiring — registers sub-apps by name
├── build.py       # mmd build — wraps UBT via subprocess
├── test.py        # mmd test — wraps UnrealEditor-Cmd automation commandlet
└── logs.py        # mmd logs — tails log files
```

**Adding a new command group:**
1. Create `mmd/<domain>.py` with a `app = typer.Typer(...)` and commands
2. Register in `main.py`: `app.add_typer(domain.app, name="domain")`
3. Add dependencies to `pyproject.toml` if needed, then `uv sync`
4. Document in this file under "What This Tool Can Do"

**One responsibility per module.** No module should do more than one domain.
`build.py` only builds. `test.py` only runs tests. Config is never duplicated — always import from `config.py`.

---

## Environment

- Engine: `C:\Program Files\Epic Games\UE_5.7`
- Project root: set via `MMD_PROJECT_ROOT` env var or auto-detected as two levels above `config.py`
- Python: 3.11+, managed by `uv`
- Target server OS: Ubuntu 22.04 on Hetzner (SSH credentials in env, never committed)

---

## Dev Setup

```bash
# Install uv if not present
winget install astral-sh.uv

# Install deps (creates .venv automatically)
uv sync

# Run
uv run mmd --help

# Lint
uv run ruff check .

# Type check
uv run mypy mmd/

# Test
uv run pytest
```

---

## Conventions

- **No magic numbers or hardcoded strings** outside `config.py`
- **subprocess calls always via `cmd /c` on Windows** for .bat files
- **All commands must exit with code 0 on success, non-zero on failure** — Claude's
  pre-commit gate reads exit codes
- **No `print()`** — use `typer.echo()` for stdout, `typer.echo(..., err=True)` for stderr
- **Errors raise `typer.Exit(code=1)`**, never `sys.exit()` directly
- **Tests live in `tests/`**, one file per module, use `pytest-subprocess` to mock
  subprocess calls — never call real UBT or UE binaries in tests

---

## Secrets

Never commit secrets. Credentials belong in environment variables:
- `MMD_SUPABASE_URL` — Supabase project URL
- `MMD_SUPABASE_KEY` — Supabase anon key
- `MMD_HETZNER_HOST` — VPS IP or hostname
- `MMD_HETZNER_USER` — SSH user (default: `ubuntu`)

Use a `.env` file locally (gitignored). Load with `python-dotenv` when Phase 4 adds db commands.
