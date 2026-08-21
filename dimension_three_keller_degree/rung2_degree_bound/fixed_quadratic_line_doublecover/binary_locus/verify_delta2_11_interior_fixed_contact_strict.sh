#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}

if ! sympy_output=$("$python_bin" -u \
    "$script_dir/verify_delta2_11_interior_fixed_contact_sympy.py" 2>&1); then
    printf '%s\n' "$sympy_output"
    exit 1
fi
printf '%s\n' "$sympy_output"
sympy_expected='PASS three deeper-incidence boundary gcd reruns
PASS generic D*H contact chart
PASS fresh D=0 and H=0 contact charts
PASS uniform constant E6 full rank
PASS primitive quartic survivor and top-only E5 obstruction
ALL INTERIOR FIXED/CONTACT {1,1} EXCLUSION CHECKS PASSED'
if [ "$sympy_output" != "$sympy_expected" ]; then
    printf '%s\n' "ERROR: main SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pivot_output=$("$python_bin" -u \
    "$script_dir/verify_delta2_11_interior_fixed_contact_pivots_sympy.py" 2>&1); then
    printf '%s\n' "$pivot_output"
    exit 1
fi
printf '%s\n' "$pivot_output"
pivot_expected='PASS D=0,u=-1 E7 rank 6; contact rank 5; constant rank 5
PASS D=0,u=3/5 E7 rank 6; contact rank 5; constant rank 5
PASS H=0,u=9/11 E7 rank 6; contact rank 4, non-Veronese kernel; constant rank 5
PASS D=H=0,J(u)=0 E7 rank 6; contact rank 4, non-Veronese kernel; constant rank 5
ALL INTERIOR FIXED/CONTACT PIVOT CHECKS PASSED'
if [ "$pivot_output" != "$pivot_expected" ]; then
    printf '%s\n' "ERROR: pivot SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pari_output=$("$gp_bin" -q -s 512M \
    "$script_dir/verify_delta2_11_interior_fixed_contact_pari.gp" 2>&1); then
    printf '%s\n' "$pari_output"
    exit 1
fi
printf '%s\n' "$pari_output"
pari_expected='PASS PARI three deeper-incidence boundary gcd reruns
PASS PARI generic D*H contact chart
PASS PARI fresh D=0 and H=0 contact charts
PASS PARI uniform constant E6 full rank
PASS PARI primitive quartic survivor and top-only E5 obstruction
PASS PARI D=0,u=-1 E7 rank 6; contact rank 5; constant rank 5
PASS PARI D=0,u=3/5 E7 rank 6; contact rank 5; constant rank 5
PASS PARI H=0,u=9/11 E7 rank 6; contact rank 4, non-Veronese kernel; constant rank 5
PASS PARI D=H=0,J(u)=0 E7 rank 6; contact rank 4, non-Veronese kernel; constant rank 5
ALL PARI INTERIOR FIXED/CONTACT {1,1} CHECKS PASSED'
if [ "$pari_output" != "$pari_expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
