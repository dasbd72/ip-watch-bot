#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UNIT_DIR="${HOME}/.config/systemd/user"
UV_BIN="$(command -v uv)"

mkdir -p "${UNIT_DIR}"

sed -e "s#__REPO_DIR__#${REPO_DIR}#" -e "s#__UV_BIN__#${UV_BIN}#" \
    "${REPO_DIR}/systemd/ip-detect.service" > "${UNIT_DIR}/ip-detect.service"
cp "${REPO_DIR}/systemd/ip-detect.timer" "${UNIT_DIR}/ip-detect.timer"

systemctl --user daemon-reload
systemctl --user enable --now ip-detect.timer

echo "Installed and started ip-detect.timer (runs every 5 minutes)."
echo "Check status with: systemctl --user status ip-detect.timer"
echo "View logs with: journalctl --user -u ip-detect.service -f"
