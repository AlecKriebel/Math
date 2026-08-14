#!/usr/bin/env bash
set -euo pipefail

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="$(cd "$PROJECT/.." && pwd)"
VENV="$REPO/.venv"
LOCK="$PROJECT/requirements.txt"
STAMP="$VENV/.stc_jc_requirements.sha256"

if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
fi

LOCK_SHA="$(shasum -a 256 "$LOCK" | awk '{print $1}')"
INSTALLED_SHA="$(cat "$STAMP" 2>/dev/null || true)"
if [[ "$LOCK_SHA" != "$INSTALLED_SHA" ]]; then
  "$VENV/bin/python" -m pip install --disable-pip-version-check \
    -r "$LOCK"
  printf '%s\n' "$LOCK_SHA" > "$STAMP"
fi

export PYTHONHASHSEED=0
export PYTHONDONTWRITEBYTECODE=1
export STC_JC_PROJECT="$PROJECT"
export STC_JC_REPO="$REPO"
export STC_JC_PYTHON="$VENV/bin/python"
