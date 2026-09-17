import os
from dataclasses import dataclass
from pathlib import Path

import yaml

APP_NAME = "ip-watch-bot"
CONFIG_FILE_NAME = "config.yaml"
STATE_FILE_NAME = "last_ip.txt"


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Config:
    bot_token: str
    chat_id: str
    state_file: Path


@dataclass(frozen=True)
class Credentials:
    bot_token: str
    chat_id: str

    @property
    def is_complete(self) -> bool:
        return bool(self.bot_token and self.chat_id)


def _xdg_config_home() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")


def _xdg_state_home() -> Path:
    return Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state")


def config_dir() -> Path:
    return _xdg_config_home() / APP_NAME


def config_file() -> Path:
    return config_dir() / CONFIG_FILE_NAME


def state_file() -> Path:
    return _xdg_state_home() / APP_NAME / STATE_FILE_NAME


def read_credentials() -> Credentials:
    path = config_file()
    if not path.exists():
        return Credentials(bot_token="", chat_id="")
    data = yaml.safe_load(path.read_text()) or {}
    return Credentials(
        bot_token=str(data.get("telegram_bot_token") or ""),
        chat_id=str(data.get("telegram_chat_id") or ""),
    )


def write_credentials(bot_token: str, chat_id: str) -> None:
    path = config_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        yaml.safe_dump(
            {"telegram_bot_token": bot_token, "telegram_chat_id": chat_id},
            f,
            default_flow_style=False,
        )
    path.chmod(0o600)


def is_configured() -> bool:
    return read_credentials().is_complete


def load_config() -> Config:
    creds = read_credentials()
    if not creds.is_complete:
        raise ConfigError(
            f"Missing configuration. Run `ip-watch-bot configure` first "
            f"(expected at {config_file()})."
        )
    return Config(
        bot_token=creds.bot_token, chat_id=creds.chat_id, state_file=state_file()
    )
