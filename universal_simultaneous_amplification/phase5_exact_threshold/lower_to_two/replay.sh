#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"

PYTHONDONTWRITEBYTECODE=1 "$ROOT/.venv/bin/python" "$HERE/verify_response_library.py"
PYTHONDONTWRITEBYTECODE=1 "$ROOT/.venv/bin/python" "$HERE/verify_clone_second_order.py"

echo "PASS: lower-to-two exact response and clone-obstruction package"
