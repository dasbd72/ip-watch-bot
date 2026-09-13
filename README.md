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
(stored in `last_ip.txt` by default, configurable via `IP_DETECT_STATE_FILE`), and
sends a Telegram message only if the IP has changed.

Schedule it periodically with cron, e.g. every 15 minutes:

```
*/15 * * * * cd /path/to/ip-watch-bot && uv run ip-watch-bot
```
