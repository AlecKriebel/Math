#!/bin/sh
set -eu

cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python3}"

"$PYTHON_BIN" -u verify_marked_delta1_sympy.py
"/opt/homebrew/bin/gp" -q verify_marked_delta1_pari.gp

if PYTHONOPTIMIZE=1 "$PYTHON_BIN" verify_marked_delta1_sympy.py \
    >/dev/null 2>&1; then
    echo "FAIL optimized Python bypassed the assertion guard" >&2
    exit 1
fi

echo "ALL MARKED FIXED-LINEAR DELTA1 CHECKS PASSED"
