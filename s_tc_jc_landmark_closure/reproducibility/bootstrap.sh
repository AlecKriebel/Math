#!/usr/bin/env bash
set -euo pipefail

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="$(cd "$PROJECT/.." && pwd)"
VENV="$REPO/.venv"
LOCK="$PROJECT/requirements.txt"
STAMP="$VENV/.stc_jc_requirements.sha256"

choose_python() {
  local candidate
  local -a candidates=()
  if [[ -n "${STC_JC_BOOTSTRAP_PYTHON:-}" ]]; then
    candidates+=("$STC_JC_BOOTSTRAP_PYTHON")
  fi
  candidates+=(python3.14 python3.13 python3.12 python3.11 python3.10 python3)
  for candidate in "${candidates[@]}"; do
    if command -v "$candidate" >/dev/null 2>&1 &&
      "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 10))'
    then
      command -v "$candidate"
      return 0
    fi
  done
  echo "A Python interpreter of version 3.10 or newer is required." >&2
  return 1
}

BOOTSTRAP_PYTHON="$(choose_python)"
if [[ ! -x "$VENV/bin/python" ]] ||
  ! "$VENV/bin/python" -c 'import sys; raise SystemExit(sys.version_info < (3, 10))'
then
  "$BOOTSTRAP_PYTHON" -m venv --clear "$VENV"
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
