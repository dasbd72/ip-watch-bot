#!/usr/bin/env bash
set -euo pipefail

UNIT_DIR="${HOME}/.config/systemd/user"

systemctl --user disable --now ip-watch-bot.timer 2>/dev/null || true
rm -f "${UNIT_DIR}/ip-watch-bot.service" "${UNIT_DIR}/ip-watch-bot.timer"

systemctl --user daemon-reload

echo "Removed ip-watch-bot.timer and ip-watch-bot.service."
