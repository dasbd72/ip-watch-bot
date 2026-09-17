import pytest

from ip_watch_bot.config import (
    ConfigError,
    is_configured,
    load_config,
    write_credentials,
)


def test_load_config_reads_saved_credentials():
    write_credentials("test-token", "12345")

    config = load_config()

    assert config.bot_token == "test-token"
    assert config.chat_id == "12345"
    assert config.state_file.name == "last_ip.txt"


def test_write_credentials_sets_restrictive_permissions():
    write_credentials("test-token", "12345")

    from ip_watch_bot.config import config_file

    mode = config_file().stat().st_mode & 0o777
    assert mode == 0o600


def test_load_config_raises_when_not_configured():
    with pytest.raises(ConfigError, match="ip-watch-bot configure"):
        load_config()


def test_load_config_raises_when_chat_id_missing():
    write_credentials("test-token", "")

    with pytest.raises(ConfigError):
        load_config()


def test_is_configured_false_when_missing():
    assert is_configured() is False


def test_is_configured_true_after_write_credentials():
    write_credentials("test-token", "12345")

    assert is_configured() is True
