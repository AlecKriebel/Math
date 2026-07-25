#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}
if [ ! -x "$gp_bin" ]; then
    printf '%s\n' "ERROR: PARI/GP executable not found: $gp_bin" >&2
    exit 1
fi
if ! output=$("$gp_bin" -q -s 128M \
    "$script_dir/verify_resonance_c3_pari.gp" 2>&1); then
    printf '%s\n' "$output"
    printf '%s\n' "ERROR: PARI/GP returned nonzero status" >&2
    exit 1
fi
printf '%s\n' "$output"
expected='ALL UNMARKED c=3 RESONANCE PARI CERTIFICATES PASSED'
if [ "$output" != "$expected" ]; then
    printf '%s\n' "ERROR: PARI/GP transcript differs from exact whitelist" >&2
    exit 1
fi
