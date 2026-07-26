#!/bin/sh
set -eu

python_bin=${KELLER_DN3_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
test -x "$python_bin"
"$python_bin" verify_full_e6_elimination.py

pari_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn3-pari.XXXXXX")
trap 'rm -f "$pari_output"' EXIT HUP INT TERM
if ! gp -s 128000000 -q verify_full_e6_pari.gp >"$pari_output" 2>&1; then
    cat "$pari_output"
    exit 1
fi
if grep -q '\*\*\*' "$pari_output"; then
    cat "$pari_output"
    exit 1
fi
grep -Fx 'D4_DN3_PARI_FULL_18_LOWER_ATLAS_PASS' "$pari_output"

printf '%s\n' 'D4_DN3_FULL_REBUILD_STRICT_PASS'
