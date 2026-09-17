# ip-watch-bot

Checks your public IP address and sends a Telegram notification when it changes.

## Install

### From AUR

```
yay -S ip-watch-bot
```

(or build locally: `makepkg -si` from this repo)

### From source

```
uv tool install .
```

## Setup

1. Create a Telegram bot via [@BotFather](https://t.me/BotFather) and get its token.
2. Find your chat ID (e.g. message your bot, then check `https://api.telegram.org/bot<token>/getUpdates`).
3. Run:

   ```
   ip-watch-bot configure
   ```

   This prompts for your bot token and chat ID and saves them to
   `~/.config/ip-watch-bot/config.yaml` (mode 600). You can also pass them
   directly with `--token`/`--chat-id` to skip the prompts, or re-run it later
   to update either value.

## Usage

```
ip-watch-bot check
```

Fetches your current public IP, compares it to the last known IP (stored in
`~/.local/state/ip-watch-bot/last_ip.txt`), and sends a Telegram message only
if the IP has changed.

## Scheduling

Manage the bundled systemd user timer (runs `ip-watch-bot check` every 5
minutes) with:

```
ip-watch-bot service enable   # start on login and now
ip-watch-bot service disable  # stop and don't start on login
ip-watch-bot service status   # show systemctl status
```

`enable` refuses to run until `ip-watch-bot configure` has been completed.

Check status and logs with:

```
systemctl --user status ip-watch-bot.timer
journalctl --user -u ip-watch-bot.service -f
```

If you'd rather use cron, schedule `ip-watch-bot check` directly instead.
