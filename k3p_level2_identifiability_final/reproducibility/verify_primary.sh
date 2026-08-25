#!/bin/bash
# One-command, fail-closed replay of the twenty-eight primary K3P gates.

set -u
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"
PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "PRIMARY_GATE_BLOCKED: missing project-local Python at .venv/bin/python" >&2
  exit 2
fi

LOG_DIR="$PROJECT_ROOT/reproducibility/logs"
mkdir -p "$LOG_DIR"
RUN_ID="$(date -u '+%Y%m%dT%H%M%SZ')"
TRANSCRIPT="$LOG_DIR/primary_${RUN_ID}.log"

cd "$PROJECT_ROOT" || exit 2
PYTHONDONTWRITEBYTECODE=1 /usr/bin/time -l "$PYTHON_BIN" reproducibility/verify_primary.py 2>&1 | tee "$TRANSCRIPT"
STATUS=${PIPESTATUS[0]}

echo "PRIMARY_TRANSCRIPT ${TRANSCRIPT#$PROJECT_ROOT/}"
exit "$STATUS"
