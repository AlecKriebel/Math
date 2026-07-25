#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_file=${1:-"$script_dir/verify_resonance_pari.gp"}
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}
output_file=$(mktemp "${TMPDIR:-/tmp}/companion-resonance-pari.XXXXXX")
trap 'rm -f "$output_file"' EXIT HUP INT TERM

if [ ! -x "$gp_bin" ]; then
  echo "FAIL: PARI/GP executable not found: $gp_bin" >&2
  exit 1
fi

if ! "$gp_bin" -fq "$gp_file" >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

expected='PARI hostile resonance audit: orbit ledger
PASS orbit ledger: finite, outer, endpoint, and reciprocal resonance charts exhaust the modulus
PARI hostile resonance audit: raw E7 and legal gauges
PASS raw resonance: rank 14/nullity 12, five legal gauges, and seven normals are complete
PARI hostile resonance audit: E6 square compatibility and converse
PASS resonance E6: polynomial syzygies force the square chain globally; constant rank-8 solve is complete
PARI hostile resonance audit: E5 K=0/K!=0 split
PASS resonance E5: K!=0 kills l7,l8; K=0 leaves two proportional columns
ALL HOSTILE PARI COMPANION-INFINITY RESONANCE CHECKS PASSED'

output=$(cat "$output_file")
if [ "$output" != "$expected" ]; then
  cat "$output_file"
  echo "FAIL: hostile resonance transcript differs from exact whitelist" >&2
  exit 1
fi

cat "$output_file"
