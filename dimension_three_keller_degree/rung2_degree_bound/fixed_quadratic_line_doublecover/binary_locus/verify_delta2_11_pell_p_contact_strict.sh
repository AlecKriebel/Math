#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}

if ! sympy_output=$("$python_bin" -u \
    "$script_dir/verify_delta2_11_pell_p_contact_sympy.py" 2>&1); then
    printf '%s\n' "$sympy_output"
    exit 1
fi
printf '%s\n' "$sympy_output"
sympy_expected='PASS fresh C=0 and C=-T delta-three boundary reruns
PASS generic lifted contact determinant
PASS fresh 16C=9T pivot chart has full contact rank
PASS fresh 12C=-7T kernel misses the Veronese cone
PASS constant E6 full rank and all-binary exit
ALL PELL FIXED-P CONTACT {1,1} EXCLUSION CHECKS PASSED'
if [ "$sympy_output" != "$sympy_expected" ]; then
    printf '%s\n' "ERROR: SymPy transcript differs from whitelist" >&2
    exit 1
fi

if ! pari_output=$("$gp_bin" -q -s 256M \
    "$script_dir/verify_delta2_11_pell_p_contact_pari.gp" 2>&1); then
    printf '%s\n' "$pari_output"
    exit 1
fi
printf '%s\n' "$pari_output"
pari_expected='PASS PARI fresh C=0 and C=-T delta-three reruns
PASS PARI generic lifted contact determinant
PASS PARI fresh 16C=9T pivot chart
PASS PARI fresh 12C=-7T kernel misses Veronese
PASS PARI constant E6 full rank and all-binary exit
ALL PARI PELL FIXED-P CONTACT {1,1} CHECKS PASSED'
if [ "$pari_output" != "$pari_expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
