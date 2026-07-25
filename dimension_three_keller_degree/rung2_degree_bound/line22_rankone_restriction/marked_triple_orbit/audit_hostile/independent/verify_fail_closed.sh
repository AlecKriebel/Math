#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch_dir=$(mktemp -d "${TMPDIR:-/tmp}/marked-triple-fail-closed.XXXXXX")
trap 'rm -rf "$scratch_dir"' EXIT HUP INT TERM

# Corrupt one exact raw-kernel certificate.  The verifier must reject it.
sed 's/483729408/483729409/' \
  "$audit_dir/verify_marked_triple_pari.gp" \
  >"$scratch_dir/tampered.gp"

if gp -s 1000000000 -fq "$scratch_dir/tampered.gp" \
  >"$scratch_dir/output.txt" 2>&1; then
  cat "$scratch_dir/output.txt"
  echo "FAIL: corrupted exact certificate was accepted" >&2
  exit 1
fi

if ! grep -F 'FAIL: raw E7 fixed maximal minor mismatch' \
  "$scratch_dir/output.txt" >/dev/null; then
  cat "$scratch_dir/output.txt"
  echo "FAIL: corruption failed for an unexpected reason" >&2
  exit 1
fi

echo "PASS fail-closed: corrupted raw E7 minor is rejected"
