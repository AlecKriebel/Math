#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
PYTHON_BIN=${K3P_RELEASE_PYTHON:-"$PROJECT_DIR/.venv/bin/python"}

if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN=$(command -v python3)
fi

if [ "${K3P_CONFIRM_FULL_REGENERATION:-}" != "YES" ]; then
  echo "Full regeneration includes the hour-scale probe producer." >&2
  echo "Re-run once with K3P_CONFIRM_FULL_REGENERATION=YES and let it finish." >&2
  exit 2
fi

export PYTHONDONTWRITEBYTECODE=1
exec "$PYTHON_BIN" "$SCRIPT_DIR/run_release_suite.py" regenerate "$@"
