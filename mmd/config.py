"""Project-wide paths and constants. Edit if your environment differs."""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
PROJECT_FILE = REPO_ROOT / "MultiMagicDungeon.uproject"
ENGINE_ROOT = Path("C:/Program Files/Epic Games/UE_5.7")
UBT = ENGINE_ROOT / "Engine/Build/BatchFiles/Build.bat"
EDITOR_CMD = ENGINE_ROOT / "Engine/Binaries/Win64/UnrealEditor-Cmd.exe"
LOG_DIR = REPO_ROOT / "Saved/Logs"
