#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_INSTALLER="${SCRIPT_DIR}/install_codex_daily_digest.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but was not found in PATH." >&2
  exit 1
fi

if [ ! -f "${PYTHON_INSTALLER}" ]; then
  echo "Missing installer: ${PYTHON_INSTALLER}" >&2
  exit 1
fi

exec python3 "${PYTHON_INSTALLER}"
