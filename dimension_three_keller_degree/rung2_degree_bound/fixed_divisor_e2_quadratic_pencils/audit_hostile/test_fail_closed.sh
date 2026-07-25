#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch_dir=$(mktemp -d "${TMPDIR:-/tmp}/e2-mixed-fail-closed.XXXXXX")
trap 'rm -rf "$scratch_dir"' EXIT HUP INT TERM

cp "$audit_dir/verify_mixed_orbits_pari_strict.sh" "$scratch_dir/"

# Injection 1: corrupt an exact raw-E7 maximal minor.  The algebraic
# verifier itself must fail at the named certificate.
sed 's/-5308416/-5308417/' \
  "$audit_dir/verify_mixed_orbits_pari.gp" \
  >"$scratch_dir/verify_mixed_orbits_pari.gp"

if "$scratch_dir/verify_mixed_orbits_pari_strict.sh" \
  >"$scratch_dir/tampered-output.txt" 2>&1; then
  cat "$scratch_dir/tampered-output.txt"
  echo "FAIL: corrupted raw-E7 minor was accepted" >&2
  exit 1
fi

if ! grep -F 'FAIL: rank-two: raw maximal minor' \
  "$scratch_dir/tampered-output.txt" >/dev/null; then
  cat "$scratch_dir/tampered-output.txt"
  echo "FAIL: raw-E7 corruption failed for an unexpected reason" >&2
  exit 1
fi

# Injection 2: preserve a successful GP exit while removing the terminal
# attestation.  The strict wrapper must reject the missing unique marker.
cp "$audit_dir/verify_mixed_orbits_pari.gp" \
  "$scratch_dir/verify_mixed_orbits_pari.gp"
sed -i '' \
  's/ALL HOSTILE PARI\/GP FIXED-DIVISOR e=2 MIXED-ORBIT CHECKS PASSED/INCOMPLETE AUDIT/' \
  "$scratch_dir/verify_mixed_orbits_pari.gp"

if "$scratch_dir/verify_mixed_orbits_pari_strict.sh" \
  >"$scratch_dir/missing-marker-output.txt" 2>&1; then
  cat "$scratch_dir/missing-marker-output.txt"
  echo "FAIL: missing terminal attestation was accepted" >&2
  exit 1
fi

if ! grep -F 'FAIL: required unique success marker missing' \
  "$scratch_dir/missing-marker-output.txt" >/dev/null; then
  cat "$scratch_dir/missing-marker-output.txt"
  echo "FAIL: marker removal failed for an unexpected reason" >&2
  exit 1
fi

echo "PASS fail-closed injections: arithmetic corruption and missing attestation rejected"
