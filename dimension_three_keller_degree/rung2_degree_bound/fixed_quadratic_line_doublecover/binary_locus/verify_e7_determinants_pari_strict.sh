#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}
if [ ! -x "$gp_bin" ]; then
    printf '%s\n' "ERROR: PARI/GP executable not found: $gp_bin" >&2
    exit 1
fi

if ! output=$("$gp_bin" -q -s 192M \
    "$script_dir/verify_e7_determinants_pari.gp" 2>&1); then
    printf '%s\n' "$output"
    printf '%s\n' "ERROR: PARI determinant verifier failed" >&2
    exit 1
fi
printf '%s\n' "$output"
expected='ALL BINARY FIXED-QUADRATIC E7 DETERMINANTS PASSED'
if [ "$output" != "$expected" ]; then
    printf '%s\n' "ERROR: PARI transcript differs from whitelist" >&2
    exit 1
fi
