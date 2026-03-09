# mmd — MultiMagicDungeon Dev CLI

Developer CLI for [MultiMagicDungeon](https://github.com/dschonholtz/MultiMagicDungeon).
Wraps UnrealBuildTool, the UE test runner, log streaming, and (later) server deploy and Supabase.

## Setup

```bash
winget install astral-sh.uv   # if not installed
uv sync
uv run mmd --help
```

## Commands

```
mmd build client              # compile game client (Win64 Development)
mmd build client --config Shipping
mmd build server              # compile Linux dedicated server
mmd test run                  # run all MMD automation tests
mmd test run MMD.Core         # run a subset
mmd logs local                # tail Saved/Logs/MultiMagicDungeon.log
mmd logs local --no-follow
```

See [CLAUDE.md](CLAUDE.md) for full documentation including what this tool cannot do,
planned commands, architecture, and conventions.
