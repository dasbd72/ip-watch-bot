from pathlib import Path
from unittest.mock import patch

from ip_watch_bot.cli import run
from ip_watch_bot.config import Config


def make_config(tmp_path: Path) -> Config:
    return Config(
        bot_token="abc123",
        chat_id="42",
        state_file=tmp_path / "last_ip.txt",
    )


@patch("ip_watch_bot.cli.send_message")
@patch("ip_watch_bot.cli.get_public_ip")
def test_run_sends_message_when_ip_changed(mock_get_ip, mock_send, tmp_path):
    config = make_config(tmp_path)
    config.state_file.write_text("203.0.113.1")
    mock_get_ip.return_value = "203.0.113.2"

    run(config)

    mock_send.assert_called_once_with(
        token="abc123", chat_id="42", text="Public IP changed: 203.0.113.2"
    )
    assert config.state_file.read_text() == "203.0.113.2"


@patch("ip_watch_bot.cli.send_message")
@patch("ip_watch_bot.cli.get_public_ip")
def test_run_skips_message_when_ip_unchanged(mock_get_ip, mock_send, tmp_path):
    config = make_config(tmp_path)
    config.state_file.write_text("203.0.113.2")
    mock_get_ip.return_value = "203.0.113.2"

    run(config)

    mock_send.assert_not_called()
    assert config.state_file.read_text() == "203.0.113.2"


@patch("ip_watch_bot.cli.send_message")
@patch("ip_watch_bot.cli.get_public_ip")
def test_run_sends_message_on_first_run_with_no_prior_state(
    mock_get_ip, mock_send, tmp_path
):
    config = make_config(tmp_path)
    mock_get_ip.return_value = "203.0.113.2"

    run(config)

    mock_send.assert_called_once_with(
        token="abc123", chat_id="42", text="Public IP changed: 203.0.113.2"
    )
    assert config.state_file.read_text() == "203.0.113.2"
