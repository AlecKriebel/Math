#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_bin=/opt/homebrew/bin/gp
output_file=$(mktemp "${TMPDIR:-/tmp}/e2-mixed-pari.XXXXXX")
trap 'rm -f "$output_file"' EXIT HUP INT TERM

if [ ! -x "$gp_bin" ]; then
  echo "FAIL: expected PARI/GP executable is unavailable at $gp_bin" >&2
  exit 1
fi

if ! "$gp_bin" -s 1000000000 -fq \
  "$audit_dir/verify_mixed_orbits_pari.gp" >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

cat "$output_file"

if grep -E '\*\*\*|FAIL:|syntax error|incorrect type|user error|stack overflow' \
  "$output_file" >/dev/null; then
  echo "FAIL: PARI/GP emitted an error diagnostic" >&2
  exit 1
fi

for marker in \
  'PASS raw E7: both rank 14/nullity 12 with complete five-gauge complements' \
  'PASS global E6: constant pivots and specialization-safe residual generators' \
  'PASS rank-two: nonzero normals have cube obstructions; closed branch has literal determinant exit' \
  'PASS rank-one nonzero normals: D^3 and division-free C*f,C*g obstructions, including w4=C' \
  'PASS rank-one zero normals: w4, w5, d=0, and d!=0 charts are exhaustive and force det(L)=0' \
  'ALL HOSTILE PARI/GP FIXED-DIVISOR e=2 MIXED-ORBIT CHECKS PASSED'
do
  if [ "$(grep -Fxc "$marker" "$output_file")" -ne 1 ]; then
    echo "FAIL: required unique success marker missing: $marker" >&2
    exit 1
  fi
done
