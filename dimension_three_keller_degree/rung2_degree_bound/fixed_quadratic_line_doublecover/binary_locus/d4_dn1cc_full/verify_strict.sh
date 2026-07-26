#!/bin/sh
set -eu

python_bin=${KELLER_DN1CC_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}

test -x "$python_bin"
"$python_bin" verify_full_contact_sympy.py

pari_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn1cc-pari.XXXXXX")
trap 'rm -f "$pari_output"' EXIT HUP INT TERM
if ! gp -q verify_full_contact_pari.gp >"$pari_output" 2>&1; then
    cat "$pari_output"
    exit 1
fi
if grep -q '\*\*\*' "$pari_output"; then
    cat "$pari_output"
    exit 1
fi
grep -Fx 'D4_DN1CC_PARI_INDEPENDENT_PASS_ONE_LINE' "$pari_output"

printf '%s\n' 'D4_DN1CC_FAIL_CLOSED_STRICT_PASS'
