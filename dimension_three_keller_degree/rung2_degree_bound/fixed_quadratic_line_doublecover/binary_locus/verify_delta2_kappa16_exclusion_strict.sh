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
    "$script_dir/verify_delta2_kappa16_exclusion_sympy.py" 2>&1); then
    printf '%s\n' "$sympy_output"
    printf '%s\n' "ERROR: SymPy kappa=16 exclusion failed" >&2
    exit 1
fi
printf '%s\n' "$sympy_output"
sympy_expected='PASS E6 r^3 kills the k=2 r^1 tangent on a+d != 0
PASS E6 r^1 kills W and both quadratic r coefficients
PASS complete E6 solve, including a=d and a!=d branches
PASS lam=0 forces a zero third column of the linear part
PASS a=d full E5 solve and decisive E4 r coefficient
ALL EXACT KAPPA=16 DELTA=2 EXCLUSION CHECKS PASSED'
if [ "$sympy_output" != "$sympy_expected" ]; then
    printf '%s\n' "ERROR: SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pari_output=$("$gp_bin" -q -s 512M \
    "$script_dir/verify_delta2_kappa16_exclusion_pari.gp" 2>&1); then
    printf '%s\n' "$pari_output"
    printf '%s\n' "ERROR: PARI kappa=16 exclusion failed" >&2
    exit 1
fi
printf '%s\n' "$pari_output"
pari_expected='PASS PARI full E8/E7 and E6 r^3
PASS PARI E6 endpoints and complete kernel
PASS PARI lambda-zero rank guards
PASS PARI a=d E5 solve and E4 contradiction
ALL PARI KAPPA=16 DELTA=2 EXCLUSION CHECKS PASSED'
if [ "$pari_output" != "$pari_expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
