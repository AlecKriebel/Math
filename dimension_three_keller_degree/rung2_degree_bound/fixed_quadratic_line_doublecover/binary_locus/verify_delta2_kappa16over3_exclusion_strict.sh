#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}

if ! sympy_output=$("$python_bin" -u \
    "$script_dir/verify_delta2_kappa16over3_exclusion_sympy.py" 2>&1); then
    printf '%s\n' "$sympy_output"
    exit 1
fi
printf '%s\n' "$sympy_output"
sympy_expected='PASS exact open and E6 r^3 tangent obstruction
PASS E6 r^1 kills both r^0 tangents and quadratic r terms
PASS complete E6 kernel solve
PASS lambda split: singular column or nonzero plane-exit normal
ALL EXACT KAPPA=16/3 DELTA=2 EXCLUSION CHECKS PASSED'
if [ "$sympy_output" != "$sympy_expected" ]; then
    printf '%s\n' "ERROR: SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pari_output=$("$gp_bin" -q -s 512M \
    "$script_dir/verify_delta2_kappa16over3_exclusion_pari.gp" 2>&1); then
    printf '%s\n' "$pari_output"
    exit 1
fi
printf '%s\n' "$pari_output"
pari_expected='PASS PARI full E8/E7 and E6 r^3
PASS PARI E6 r endpoint mutations
PASS PARI complete E6 kernel and lambda-zero rank guards
ALL PARI KAPPA=16/3 DELTA=2 EXCLUSION CHECKS PASSED'
if [ "$pari_output" != "$pari_expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
