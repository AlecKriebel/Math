#!/bin/sh
set -eu

cd "$(dirname "$0")"

PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python3}"

"$PYTHON_BIN" -u verify_power_fibre_v9_sympy.py
"$PYTHON_BIN" -u verify_power_fibre_v9zero_q_orbits_sympy.py
"$PYTHON_BIN" -u verify_power_fibre_v9zero_p_orbit_sympy.py
"$PYTHON_BIN" -u verify_power_fibre_v9zero_ellzero_sympy.py

if PYTHONOPTIMIZE=1 "$PYTHON_BIN" verify_power_fibre_v9_sympy.py \
    >/dev/null 2>&1; then
    echo "FAIL optimized Python bypassed the assertion guard" >&2
    exit 1
fi

echo "ALL EXCEPTIONAL POWER-FIBRE PRIMARY CHECKS PASSED"
