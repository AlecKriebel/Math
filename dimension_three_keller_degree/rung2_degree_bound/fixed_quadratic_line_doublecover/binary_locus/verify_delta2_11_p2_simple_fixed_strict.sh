#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}

if ! sympy_output=$("$python_bin" -u \
    "$script_dir/verify_delta2_11_p2_simple_fixed_sympy.py" 2>&1); then
    printf '%s\n' "$sympy_output"
    exit 1
fi
printf '%s\n' "$sympy_output"
sympy_expected='PASS signed-minor/Veronese certificate for 256*A*C+11*B^2
PASS Delta=0 endpoint chart and B=0/C=0 mutations
PASS mandatory rational E6 survivor and full E5 obstruction
ALL P2 SIMPLE-FIXED {1,1} EXCLUSION CHECKS PASSED'
if [ "$sympy_output" != "$sympy_expected" ]; then
    printf '%s\n' "ERROR: SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pari_output=$("$gp_bin" -q -s 512M \
    "$script_dir/verify_delta2_11_p2_simple_fixed_pari.gp" 2>&1); then
    printf '%s\n' "$pari_output"
    exit 1
fi
printf '%s\n' "$pari_output"
pari_expected='PASS PARI signed-minor/Veronese contact divisor
PASS PARI Delta=0 endpoint and B=0/C=0 mutations
PASS PARI mandatory rational survivor and full E5 obstruction
ALL PARI P2 SIMPLE-FIXED {1,1} CHECKS PASSED'
if [ "$pari_output" != "$pari_expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
