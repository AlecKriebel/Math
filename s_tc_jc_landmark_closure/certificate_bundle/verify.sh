#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:-quick}"
case "$MODE" in
  quick|full|regenerate-all) ;;
  *) echo "usage: bash verify.sh {quick|full|regenerate-all}" >&2; exit 2 ;;
esac

VENV="$ROOT/.venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  BOOTSTRAP="${STC_JC_BOOTSTRAP_PYTHON:-python3.11}"
  command -v "$BOOTSTRAP" >/dev/null 2>&1 || BOOTSTRAP=python3
  "$BOOTSTRAP" -m venv "$VENV"
fi

STAMP="$VENV/.requirements.sha256"
LOCK_SHA="$(shasum -a 256 "$ROOT/environment/requirements.txt" | awk '{print $1}')"
if [[ "$(cat "$STAMP" 2>/dev/null || true)" != "$LOCK_SHA" ]]; then
  "$VENV/bin/python" -m pip install --disable-pip-version-check \
    -r "$ROOT/environment/requirements.txt"
  printf '%s\n' "$LOCK_SHA" > "$STAMP"
fi

export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
exec "$VENV/bin/python" "$ROOT/verifiers/run_gate.py" "$MODE"

