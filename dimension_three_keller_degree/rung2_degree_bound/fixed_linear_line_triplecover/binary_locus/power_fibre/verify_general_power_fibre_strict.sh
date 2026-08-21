#!/bin/sh
set -eu

cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python3}"

"$PYTHON_BIN" -u verify_general_power_fibre_sympy.py
"/opt/homebrew/bin/gp" -q verify_general_power_fibre_pari.gp

if PYTHONOPTIMIZE=1 "$PYTHON_BIN" verify_general_power_fibre_sympy.py \
    >/dev/null 2>&1; then
    echo "FAIL optimized Python bypassed the assertion guard" >&2
    exit 1
fi

echo "ALL FIXED-LINEAR POWER-FIBRE PRIMARY CHECKS PASSED"
