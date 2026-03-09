"""Smoke tests for config — verifies paths are strings and nothing crashes on import."""
from mmd.config import REPO_ROOT, PROJECT_FILE, ENGINE_ROOT, UBT, EDITOR_CMD, LOG_DIR


def test_config_values_are_paths():
    # All config values should be Path objects, not None or empty
    for p in (REPO_ROOT, PROJECT_FILE, ENGINE_ROOT, UBT, EDITOR_CMD, LOG_DIR):
        assert p is not None
        assert str(p) != ""


def test_project_file_name():
    assert PROJECT_FILE.name == "MultiMagicDungeon.uproject"


def test_engine_root_name():
    assert "UE_5.7" in str(ENGINE_ROOT)
