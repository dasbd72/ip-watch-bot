import sys

from ip_watch_bot.config import Config, ConfigError, load_config
from ip_watch_bot.ip import get_public_ip
from ip_watch_bot.storage import read_last_ip, write_last_ip
from ip_watch_bot.telegram import send_message


def run(config: Config) -> None:
    current_ip = get_public_ip()
    last_ip = read_last_ip(config.state_file)

    if current_ip != last_ip:
        send_message(
            token=config.bot_token,
            chat_id=config.chat_id,
            text=f"Public IP changed: {current_ip}",
        )
        write_last_ip(config.state_file, current_ip)


def main() -> None:
    try:
        config = load_config()
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        raise SystemExit(1) from e

    run(config)
