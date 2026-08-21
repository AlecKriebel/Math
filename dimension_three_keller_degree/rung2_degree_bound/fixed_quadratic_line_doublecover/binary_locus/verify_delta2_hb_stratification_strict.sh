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
    "$script_dir/verify_delta2_hb_stratification_sympy.py" 2>&1); then
    printf '%s\n' "$sympy_output"
    printf '%s\n' "ERROR: SymPy delta=2 stratification failed" >&2
    exit 1
fi
printf '%s\n' "$sympy_output"
sympy_expected='PASS every boundary-orbit exact-delta=2 incidence has {1,1} shape
PASS squarefree-interior maximal-minor factorization
PASS doubled-root exact-delta=2 exceptional {2,0} sublocus
PASS literal kappa=16, 16/3, and 4 {2,0} regressions
ALL EXACT DELTA=2 HILBERT--BURCH STRATIFICATION CHECKS PASSED'
if [ "$sympy_output" != "$sympy_expected" ]; then
    printf '%s\n' "ERROR: SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pari_output=$("$gp_bin" -q -s 256M \
    "$script_dir/verify_delta2_hb_stratification_pari.gp" 2>&1); then
    printf '%s\n' "$pari_output"
    printf '%s\n' "ERROR: PARI delta=2 stratification failed" >&2
    exit 1
fi
printf '%s\n' "$pari_output"
pari_expected='PASS PARI kappa=16 gcd, resultant, ranks, and kernel
PASS PARI kappa=4 gcd, resultant, ranks, and kernel
PASS PARI kappa=16/3 primitive row, ranks, and kernel
PASS PARI squarefree exceptional determinant factors
PASS PARI doubled-root exceptional determinant factor
ALL PARI DELTA=2 HILBERT--BURCH CHECKS PASSED'
if [ "$pari_output" != "$pari_expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
