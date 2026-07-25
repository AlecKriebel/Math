#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
checker="$script_dir/verify_vertical_szero_w0_sympy.py"
expected='PASS: s=0, W0=0 vertical companion excluded on 2 nontriple + 3 minimal triple-root charts'
gp_checker="$script_dir/verify_vertical_szero_w0_pari.gp"
gp_expected='VERTICAL_SZERO_W0_PARI_PASS_C5E4A2'
scratch=$(mktemp -d "${TMPDIR:-/tmp}/vertical-szero-w0.XXXXXX")
trap 'rm -rf "$scratch"' EXIT HUP INT TERM

/usr/bin/python3 "$checker" >"$scratch/output" 2>&1
if [ "$(cat "$scratch/output")" != "$expected" ]; then
    cat "$scratch/output"
    echo 'FAIL: exact checker did not emit the unique pass marker'
    exit 1
fi

if /usr/bin/python3 -O "$checker" >"$scratch/optimized" 2>&1; then
    cat "$scratch/optimized"
    echo 'FAIL: exact checker accepted optimized Python'
    exit 1
fi

if ! gp -q "$gp_checker" >"$scratch/pari" 2>&1; then
    cat "$scratch/pari"
    exit 1
fi
if grep -Eq '^  \*\*\*|FAIL:' "$scratch/pari"; then
    cat "$scratch/pari"
    echo 'FAIL: PARI/GP reported a diagnostic'
    exit 1
fi
if [ "$(cat "$scratch/pari")" != "$gp_expected" ]; then
    cat "$scratch/pari"
    echo 'FAIL: PARI/GP did not emit the unique pass marker'
    exit 1
fi

printf '%s\n' "$expected"
printf '%s\n' "$gp_expected"
printf '%s\n' 'PASS: optimized-Python false-pass guard'
