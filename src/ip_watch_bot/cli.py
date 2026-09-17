import argparse
import subprocess
import sys

from ip_watch_bot.config import (
    Config,
    ConfigError,
    config_file,
    is_configured,
    load_config,
    read_credentials,
    write_credentials,
)
from ip_watch_bot.ip import get_public_ip
from ip_watch_bot.storage import read_last_ip, write_last_ip
from ip_watch_bot.telegram import send_message

TIMER_UNIT = "ip-watch-bot.timer"
SERVICE_ACTIONS = ["enable", "disable", "status"]


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


def _mask(value: str) -> str:
    if len(value) <= 6:
        return "*" * len(value)
    return f"{value[:2]}...{value[-4:]}"


def _prompt(label: str, current: str, flag_value: str | None) -> str:
    if flag_value is not None:
        return flag_value

    hint = f" [{_mask(current)}]" if current else ""
    entered = input(f"{label}{hint}: ").strip()
    return entered or current


def cmd_check(args: argparse.Namespace) -> int:
    try:
        config = load_config()
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1

    run(config)
    return 0


def cmd_configure(args: argparse.Namespace) -> int:
    current = read_credentials()

    token = _prompt("Bot token", current.bot_token, args.token)
    chat_id = _prompt("Chat ID", current.chat_id, args.chat_id)

    if not token or not chat_id:
        print("Both bot token and chat ID are required.", file=sys.stderr)
        return 1

    write_credentials(token, chat_id)
    print(f"Saved configuration to {config_file()}")
    return 0


def cmd_service(args: argparse.Namespace) -> int:
    if args.action == "enable" and not is_configured():
        print(
            "ip-watch-bot is not configured yet. Run `ip-watch-bot configure` first.",
            file=sys.stderr,
        )
        return 1

    systemctl_args = ["systemctl", "--user", args.action]
    if args.action in ("enable", "disable"):
        systemctl_args.append("--now")
    systemctl_args.append(TIMER_UNIT)

    result = subprocess.run(systemctl_args)
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ip-watch-bot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser(
        "check", help="Check the public IP and notify via Telegram if it changed"
    )
    check_parser.set_defaults(func=cmd_check)

    configure_parser = subparsers.add_parser(
        "configure", help="Set the Telegram bot token and chat ID"
    )
    configure_parser.add_argument("--token", help="Telegram bot token")
    configure_parser.add_argument("--chat-id", help="Telegram chat ID")
    configure_parser.set_defaults(func=cmd_configure)

    service_parser = subparsers.add_parser(
        "service", help="Manage the ip-watch-bot systemd user timer"
    )
    service_parser.add_argument("action", choices=SERVICE_ACTIONS)
    service_parser.set_defaults(func=cmd_service)

    return parser
