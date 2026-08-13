#!/usr/bin/env bash
set -euo pipefail

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="$(cd "$PROJECT/.." && pwd)"
VENV="$REPO/.venv"

if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
  "$VENV/bin/python" -m pip install --disable-pip-version-check \
    -r "$PROJECT/requirements.txt"
fi

export PYTHONHASHSEED=0
export PYTHONDONTWRITEBYTECODE=1
export STC_JC_PROJECT="$PROJECT"
export STC_JC_REPO="$REPO"
export STC_JC_PYTHON="$VENV/bin/python"
