import pytest

from ip_detect.config import ConfigError, load_config


def test_load_config_reads_required_env_vars(monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")
    monkeypatch.delenv("IP_DETECT_STATE_FILE", raising=False)

    config = load_config(dotenv_path=tmp_path / "missing.env")

    assert config.bot_token == "test-token"
    assert config.chat_id == "12345"
    assert config.state_file.name == "last_ip.txt"


def test_load_config_uses_custom_state_file(monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")
    monkeypatch.setenv("IP_DETECT_STATE_FILE", str(tmp_path / "state.txt"))

    config = load_config(dotenv_path=tmp_path / "missing.env")

    assert config.state_file == tmp_path / "state.txt"


def test_load_config_falls_back_to_default_when_state_file_empty(monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")
    monkeypatch.setenv("IP_DETECT_STATE_FILE", "")

    config = load_config(dotenv_path=tmp_path / "missing.env")

    assert config.state_file.name == "last_ip.txt"


def test_load_config_raises_when_token_missing(monkeypatch, tmp_path):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")

    with pytest.raises(ConfigError, match="TELEGRAM_BOT_TOKEN"):
        load_config(dotenv_path=tmp_path / "missing.env")


def test_load_config_raises_when_chat_id_missing(monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    with pytest.raises(ConfigError, match="TELEGRAM_CHAT_ID"):
        load_config(dotenv_path=tmp_path / "missing.env")
