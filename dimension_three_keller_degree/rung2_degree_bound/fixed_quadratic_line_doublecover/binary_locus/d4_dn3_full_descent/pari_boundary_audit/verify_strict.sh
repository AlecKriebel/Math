#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_bin=${KELLER_PARI_GP:-gp}
baseline_output=$(mktemp)
mutant_s=$(mktemp)
mutant_s_output=$(mktemp)
mutant_origin=$(mktemp)
mutant_origin_output=$(mktemp)
trap 'rm -f "$baseline_output" "$mutant_s" "$mutant_s_output" "$mutant_origin" "$mutant_origin_output"' EXIT HUP INT TERM

cd "$audit_dir"

if ! "$gp_bin" -q verify_boundary_pari.gp >"$baseline_output" 2>&1; then
  cat "$baseline_output"
  echo "FAIL: baseline PARI verifier exited nonzero" >&2
  exit 1
fi
cat "$baseline_output"

if grep -Eq 'FAIL:|syntax error|user error|at top-level|in function' "$baseline_output"; then
  echo "FAIL: baseline PARI verifier emitted a diagnostic" >&2
  exit 1
fi
grep -Fx "D4_DN3_PARI_PUNCTURED_INTERSECTION_PASS_DETL_ZERO" "$baseline_output" >/dev/null
grep -Fx "D4_DN3_PARI_ORIGIN_PASS_BINARY_COLLAPSE_PLANE_REDUCTION" "$baseline_output" >/dev/null
grep -Fx "D4_DN3_PARI_BOUNDARY_AUDIT_ALL_PASS" "$baseline_output" >/dev/null

# Mutation guard 1: corrupt the first coefficient that forces S=0.
sed 's|+9\*k\^3\*S/4,"E4 p\^2 r\^2 explicitly forces S"|+7*k^3*S/4,"E4 p^2 r^2 explicitly forces S"|' \
  verify_boundary_pari.gp >"$mutant_s"
if "$gp_bin" -q "$mutant_s" >"$mutant_s_output" 2>&1; then
  cat "$mutant_s_output"
  echo "FAIL: S-forcing mutation was not rejected" >&2
  exit 1
fi
grep -F "FAIL: E4 p^2 r^2 explicitly forces S" "$mutant_s_output" >/dev/null
if grep -F "D4_DN3_PARI_BOUNDARY_AUDIT_ALL_PASS" "$mutant_s_output" >/dev/null; then
  echo "FAIL: S-forcing mutant reached the terminal marker" >&2
  exit 1
fi

# Mutation guard 2: corrupt the first origin square.
sed 's|-3\*b4\^2,"origin E4 p\^3 r square"|-5*b4^2,"origin E4 p^3 r square"|' \
  verify_boundary_pari.gp >"$mutant_origin"
if "$gp_bin" -q "$mutant_origin" >"$mutant_origin_output" 2>&1; then
  cat "$mutant_origin_output"
  echo "FAIL: origin-square mutation was not rejected" >&2
  exit 1
fi
grep -F "FAIL: origin E4 p^3 r square" "$mutant_origin_output" >/dev/null
if grep -F "D4_DN3_PARI_BOUNDARY_AUDIT_ALL_PASS" "$mutant_origin_output" >/dev/null; then
  echo "FAIL: origin-square mutant reached the terminal marker" >&2
  exit 1
fi

echo "D4_DN3_PARI_BOUNDARY_STRICT_PASS"
