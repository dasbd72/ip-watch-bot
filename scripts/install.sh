#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UNIT_DIR="${HOME}/.config/systemd/user"
UV_BIN="$(command -v uv)"

mkdir -p "${UNIT_DIR}"

sed -e "s#__REPO_DIR__#${REPO_DIR}#" -e "s#__UV_BIN__#${UV_BIN}#" \
    "${REPO_DIR}/systemd/ip-watch-bot.service" > "${UNIT_DIR}/ip-watch-bot.service"
cp "${REPO_DIR}/systemd/ip-watch-bot.timer" "${UNIT_DIR}/ip-watch-bot.timer"

systemctl --user daemon-reload
systemctl --user enable --now ip-watch-bot.timer

echo "Installed and started ip-watch-bot.timer (runs every 5 minutes)."
echo "Check status with: systemctl --user status ip-watch-bot.timer"
echo "View logs with: journalctl --user -u ip-watch-bot.service -f"
