#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}
if [ ! -x "$gp_bin" ]; then
    printf '%s\n' "ERROR: PARI/GP executable not found: $gp_bin" >&2
    exit 1
fi

if ! transcript=$("$gp_bin" -q -s 192M \
    "$audit_dir/verify_hostile_pari.gp" 2>&1); then
    printf '%s\n' "$transcript"
    printf '%s\n' "ERROR: hostile PARI audit returned nonzero status" >&2
    exit 1
fi

printf '%s\n' "$transcript"
expected='ALL HOSTILE UNMARKED c^2=9 PARI AUDIT CHECKS PASSED'
if [ "$transcript" != "$expected" ]; then
    printf '%s\n' "ERROR: hostile PARI transcript differs from whitelist" >&2
    exit 1
fi
