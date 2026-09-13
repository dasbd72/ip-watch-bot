# ip-watch-bot

Checks your public IP address and sends a Telegram notification when it changes.

## Setup

1. Create a Telegram bot via [@BotFather](https://t.me/BotFather) and get its token.
2. Find your chat ID (e.g. message your bot, then check `https://api.telegram.org/bot<token>/getUpdates`).
3. Copy `.env.example` to `.env` and fill in `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

## Usage

```
uv run ip-watch-bot
```

On each run, it fetches your current public IP, compares it to the last known IP
(stored in `last_ip.txt` by default, configurable via `IP_WATCH_BOT_STATE_FILE`), and
sends a Telegram message only if the IP has changed.

## Scheduling

This repo includes a systemd user timer that runs the bot every 5 minutes
(useful on systems without a cron daemon):

```
./scripts/install.sh    # installs + enables ip-watch-bot.timer
./scripts/uninstall.sh  # stops + removes it
```

Check status and logs with:

```
systemctl --user status ip-watch-bot.timer
journalctl --user -u ip-watch-bot.service -f
```

If you'd rather use cron, schedule `uv run ip-watch-bot` directly instead.
