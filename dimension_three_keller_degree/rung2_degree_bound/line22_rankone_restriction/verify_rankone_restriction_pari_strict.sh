#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}
if [ ! -x "$gp_bin" ]; then
    printf '%s\n' "ERROR: PARI/GP executable not found: $gp_bin" >&2
    exit 1
fi

if ! output=$("$gp_bin" -q \
    "$script_dir/verify_rankone_restriction_pari.gp" 2>&1); then
    printf '%s\n' "$output"
    printf '%s\n' "ERROR: PARI/GP returned nonzero status" >&2
    exit 1
fi
printf '%s\n' "$output"

expected='  PASS stabilizer p transform
  PASS stabilizer q transform
  PASS stabilizer determinant
  PASS open raw-E7 maximal minor
  PASS open raw-E7 eight kernel directions
  PASS kernel independence minor
  PASS unmarked triple raw-E7 rank
  PASS unmarked plus resonance raw-E7 rank
  PASS unmarked minus resonance raw-E7 rank
  PASS unmarked infinity raw-E7 rank
  PASS marked triple raw-E7 rank
  PASS marked coincident mixed raw-E7 rank
  PASS marked distinct mixed raw-E7 rank
  PASS normalized E6 forcing minor
  PASS normalized E6 converse
  PASS E5 x3z2 difference
  PASS E5 y5 difference
  PASS E5 x5 sum
  PASS E5 x4y sum
  PASS forced singular linear part
PASS: independent PARI rank-one-restriction line-(2,2) certificate'
if [ "$output" != "$expected" ]; then
    printf '%s\n' "ERROR: PARI/GP transcript differs from the exact whitelist" >&2
    exit 1
fi
