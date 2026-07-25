#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}

if ! sympy_output=$("$python_bin" -u \
    "$script_dir/verify_delta2_11_doubled_simple_fixed_sympy.py" 2>&1); then
    printf '%s\n' "$sympy_output"
    exit 1
fi
printf '%s\n' "$sympy_output"
sympy_expected='PASS exact-open gcd mutations and residual stabilizer
PASS generic Delta-nonzero contact determinant
PASS fresh Delta-zero contact determinant and exact-open cover
PASS uniform constant E6 determinant and all-binary exit
ALL DOUBLED-NONBRANCH SIMPLE-FIXED {1,1} CHECKS PASSED'
if [ "$sympy_output" != "$sympy_expected" ]; then
    printf '%s\n' "ERROR: SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pari_output=$("$gp_bin" -q -s 256M \
    "$script_dir/verify_delta2_11_doubled_simple_fixed_pari.gp" 2>&1); then
    printf '%s\n' "$pari_output"
    exit 1
fi
printf '%s\n' "$pari_output"
pari_expected='PASS PARI exact-open gcd mutations and residual stabilizer
PASS PARI generic Delta-nonzero contact determinant
PASS PARI fresh Delta-zero contact determinant and exact-open cover
PASS PARI uniform constant E6 determinant and all-binary exit
ALL PARI DOUBLED-NONBRANCH SIMPLE-FIXED {1,1} CHECKS PASSED'
if [ "$pari_output" != "$pari_expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
