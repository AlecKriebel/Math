#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
PYTHON="$REPO_ROOT/.venv/bin/python"
export PYTHONDONTWRITEBYTECODE=1
"$PYTHON" "$SCRIPT_DIR/verify_lumping.py"
"$PYTHON" "$SCRIPT_DIR/certify_counterexample.py"
"$PYTHON" "$SCRIPT_DIR/verify_independent.py"
