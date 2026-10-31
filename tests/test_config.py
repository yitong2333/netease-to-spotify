import pytest

from src.config import REQUIRED_ENV_VARS, load_settings


def configure_required_environment(monkeypatch):
    for name in REQUIRED_ENV_VARS:
        monkeypatch.setenv(name, f"test-{name.lower()}")


def test_match_level_defaults_to_balanced(monkeypatch):
    configure_required_environment(monkeypatch)
    monkeypatch.delenv("MATCH_LEVEL", raising=False)

    assert load_settings().match_level == "balanced"


@pytest.mark.parametrize("level", ["strict", "balanced", "relaxed", " RELAXED "])
def test_match_level_is_configurable_and_normalized(monkeypatch, level):
    configure_required_environment(monkeypatch)
    monkeypatch.setenv("MATCH_LEVEL", level)

    assert load_settings().match_level == level.strip().lower()


def test_invalid_match_level_has_actionable_error(monkeypatch):
    configure_required_environment(monkeypatch)
    monkeypatch.setenv("MATCH_LEVEL", "aggressive")

    with pytest.raises(ValueError, match="strict, balanced, relaxed"):
        load_settings()
