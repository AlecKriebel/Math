#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
PYTHONDONTWRITEBYTECODE=1 "$ROOT/.venv/bin/python" \
  "$HERE/verify_optional_reduction.py"
