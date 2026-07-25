#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch_dir=$(mktemp -d "${TMPDIR:-/tmp}/e2-ranktwo-triple-fail-closed.XXXXXX")
trap 'rm -rf "$scratch_dir"' EXIT HUP INT TERM

cp "$audit_dir/verify_ranktwo_triple_pari_strict.sh" "$scratch_dir/"

# Injection 1: corrupt the certified raw-E7 maximal minor.  The algebraic
# checker itself must reject the modified certificate at the named check.
sed 's/236196,/236197,/' \
  "$audit_dir/verify_ranktwo_triple_pari.gp" \
  >"$scratch_dir/verify_ranktwo_triple_pari.gp"

if "$scratch_dir/verify_ranktwo_triple_pari_strict.sh" \
  >"$scratch_dir/tampered-output.txt" 2>&1; then
  cat "$scratch_dir/tampered-output.txt"
  echo "FAIL: corrupted raw-E7 minor was accepted" >&2
  exit 1
fi

if ! grep -F 'FAIL: raw E7 maximal minor' \
  "$scratch_dir/tampered-output.txt" >/dev/null; then
  cat "$scratch_dir/tampered-output.txt"
  echo "FAIL: raw-E7 corruption failed for an unexpected reason" >&2
  exit 1
fi

# Injection 2: preserve a successful PARI exit while removing the terminal
# attestation.  The strict wrapper must reject the absent unique marker.
cp "$audit_dir/verify_ranktwo_triple_pari.gp" \
  "$scratch_dir/verify_ranktwo_triple_pari.gp"
sed -i '' \
  's/ALL HOSTILE PARI\/GP RANK-TWO e=2 TRIPLE-COMPANION CHECKS PASSED/INCOMPLETE HOSTILE AUDIT/' \
  "$scratch_dir/verify_ranktwo_triple_pari.gp"

if "$scratch_dir/verify_ranktwo_triple_pari_strict.sh" \
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
