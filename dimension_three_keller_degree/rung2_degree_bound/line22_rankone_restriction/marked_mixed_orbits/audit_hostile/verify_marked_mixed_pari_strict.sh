#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}
if [ ! -x "$gp_bin" ]; then
    printf '%s\n' "ERROR: PARI/GP executable not found: $gp_bin" >&2
    exit 1
fi

if ! output=$("$gp_bin" -q -s 256M \
    "$audit_dir/verify_marked_mixed_pari.gp" 2>&1); then
    printf '%s\n' "$output"
    printf '%s\n' "ERROR: PARI/GP returned nonzero status" >&2
    exit 1
fi
printf '%s\n' "$output"

expected='PASS R=xq raw E7: complete five-gauge/three-normal kernel and exact quotient
PASS R=x(p-q) raw E7: complete five-gauge/three-normal kernel and exact quotient
PASS R=xq E6/E5: complete constant-pivot converses, including d=0, and det L=0
PASS R=x(p-q) E6/E5: complete constant-pivot converses, including d=0, and det L=0
ALL HOSTILE PARI/GP MARKED-MIXED AUDIT CHECKS PASSED'
if [ "$output" != "$expected" ]; then
    printf '%s\n' "ERROR: PARI/GP transcript differs from exact whitelist" >&2
    exit 1
fi
