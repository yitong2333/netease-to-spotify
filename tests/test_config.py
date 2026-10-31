import pytest

from src.config import REQUIRED_ENV_VARS, load_settings


def configure_required_environment(monkeypatch):
    for name in REQUIRED_ENV_VARS:
        value = (
            "https://music-api.example.com/"
            if name == "NETEASE_API_BASE_URL"
            else f"test-{name.lower()}"
        )
        monkeypatch.setenv(name, value)


def test_match_level_defaults_to_balanced(monkeypatch):
    configure_required_environment(monkeypatch)
    monkeypatch.delenv("MATCH_LEVEL", raising=False)

    settings = load_settings()
    assert settings.match_level == "balanced"
    assert settings.netease_api_base_url == "https://music-api.example.com"


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


def test_missing_netease_api_base_url_fails_fast(monkeypatch):
    configure_required_environment(monkeypatch)
    monkeypatch.delenv("NETEASE_API_BASE_URL")

    with pytest.raises(RuntimeError, match="NETEASE_API_BASE_URL"):
        load_settings()
