#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}

if ! sympy_output=$("$python_bin" -u \
    "$script_dir/verify_delta2_11_interior_double_fixed_sympy.py" 2>&1); then
    printf '%s\n' "$sympy_output"
    exit 1
fi
printf '%s\n' "$sympy_output"
sympy_expected='PASS three deeper-incidence boundary gcd reruns
PASS four residual contact-minor identities
PASS projective contact-rank cover by resultants and endpoint gcd
PASS fresh triple-fixed pivot chart has full contact rank
PASS constant E6 full rank and all-binary exit
ALL INTERIOR DOUBLE-FIXED {1,1} EXCLUSION CHECKS PASSED'
if [ "$sympy_output" != "$sympy_expected" ]; then
    printf '%s\n' "ERROR: SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pari_output=$("$gp_bin" -q -s 512M \
    "$script_dir/verify_delta2_11_interior_double_fixed_pari.gp" 2>&1); then
    printf '%s\n' "$pari_output"
    exit 1
fi
printf '%s\n' "$pari_output"
pari_expected='PASS PARI three deeper-incidence boundary gcd reruns
PASS PARI four residual contact-minor identities
PASS PARI projective resultant cover and endpoint gcd
PASS PARI fresh triple-fixed pivot chart
PASS PARI constant E6 full rank and all-binary exit
ALL PARI INTERIOR DOUBLE-FIXED {1,1} CHECKS PASSED'
if [ "$pari_output" != "$pari_expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
