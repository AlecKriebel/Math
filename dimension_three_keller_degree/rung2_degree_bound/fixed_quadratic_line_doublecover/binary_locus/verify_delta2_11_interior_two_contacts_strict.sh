#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}

if ! sympy_output=$("$python_bin" -u \
    "$script_dir/verify_delta2_11_interior_two_contacts_sympy.py" 2>&1); then
    printf '%s\n' "$sympy_output"
    exit 1
fi
printf '%s\n' "$sympy_output"
sympy_expected='PASS exact two-contact generic/alternate charts, algebraic pivots, and full lower singularity'
if [ "$sympy_output" != "$sympy_expected" ]; then
    printf '%s\n' "ERROR: SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pari_output=$("$gp_bin" -q -s 512M \
    "$script_dir/verify_delta2_11_interior_two_contacts_pari.gp" 2>&1); then
    printf '%s\n' "$pari_output"
    exit 1
fi
printf '%s\n' "$pari_output"
pari_expected='PASS PARI generic contact-resultant stratification
PASS PARI alternate contact-resultant stratification
PASS PARI exact octic/quartic/u=-1 boundary routing
PASS PARI K1=K2,a=1 E7/contact/constant pivots
PASS PARI K1=K2,a=-1 E7/contact/constant pivots
PASS PARI B=0,P16 E7/contact/constant pivots
PASS PARI B=0,u=-1,a=0 E7/contact/constant pivots
PASS PARI full lower chain forces col_1(L)=U2 col_3(L)
ALL PARI INTERIOR TWO-CONTACT {1,1} CHECKS PASSED'
if [ "$pari_output" != "$pari_expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
