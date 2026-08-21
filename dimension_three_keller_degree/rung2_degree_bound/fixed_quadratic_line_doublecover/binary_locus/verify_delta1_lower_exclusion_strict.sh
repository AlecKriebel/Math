#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}

if [ ! -x "$python_bin" ]; then
    printf '%s\n' "ERROR: Python executable not found: $python_bin" >&2
    exit 1
fi
if [ ! -x "$gp_bin" ]; then
    printf '%s\n' "ERROR: PARI/GP executable not found: $gp_bin" >&2
    exit 1
fi

if ! sympy_output=$("$python_bin" -u \
    "$script_dir/verify_delta1_lower_exclusion_sympy.py" 2>&1); then
    printf '%s\n' "$sympy_output"
    printf '%s\n' "ERROR: SymPy delta=1 exclusion failed" >&2
    exit 1
fi
printf '%s\n' "$sympy_output"
sympy_expected='PASS full branch-square E6/E5 solve and E4 kernel
PASS full interior E6/E5 solve and E4 kernel
PASS b,d,c,a-c,k divisor mutations and final kernel vectors
ALL EXACT DELTA=1 LOWER EXCLUSION CHECKS PASSED'
if [ "$sympy_output" != "$sympy_expected" ]; then
    printf '%s\n' "ERROR: SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pari_output=$("$gp_bin" -q -s 256M \
    "$script_dir/verify_delta1_lower_exclusion_pari.gp" 2>&1); then
    printf '%s\n' "$pari_output"
    printf '%s\n' "ERROR: PARI delta=1 exclusion failed" >&2
    exit 1
fi
printf '%s\n' "$pari_output"
pari_expected='ALL PARI DELTA=1 LOWER EXCLUSION CHECKS PASSED'
if [ "$pari_output" != "$pari_expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
