#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../../.." && pwd)
PYTHON="$ROOT/.venv/bin/python"

PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/verify_exact.py"
