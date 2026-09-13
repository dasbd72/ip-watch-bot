import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_STATE_FILE = Path("last_ip.txt")


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Config:
    bot_token: str
    chat_id: str
    state_file: Path


def load_config(dotenv_path: Path | None = None) -> Config:
    load_dotenv(dotenv_path=dotenv_path)

    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ConfigError("TELEGRAM_BOT_TOKEN environment variable is required")

    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        raise ConfigError("TELEGRAM_CHAT_ID environment variable is required")

    state_file = Path(os.environ.get("IP_DETECT_STATE_FILE", DEFAULT_STATE_FILE))

    return Config(bot_token=bot_token, chat_id=chat_id, state_file=state_file)
