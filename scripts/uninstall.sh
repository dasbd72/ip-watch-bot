#!/usr/bin/env bash
set -euo pipefail

UNIT_DIR="${HOME}/.config/systemd/user"

systemctl --user disable --now ip-detect.timer 2>/dev/null || true
rm -f "${UNIT_DIR}/ip-detect.service" "${UNIT_DIR}/ip-detect.timer"

systemctl --user daemon-reload

echo "Removed ip-detect.timer and ip-detect.service."
