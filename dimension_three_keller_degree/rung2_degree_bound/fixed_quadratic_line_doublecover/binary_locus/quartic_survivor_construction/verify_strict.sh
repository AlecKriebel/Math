#!/bin/sh
set -eu
out="$(mktemp)"
trap 'rm -f "$out"' EXIT
if ! /usr/local/bin/python "$(dirname "$0")/verify_family_exclusion.py" >"$out" 2>&1; then
  cat "$out"
  exit 1
fi
cat "$out"
grep -Fqx 'D3_BS_N1_CONTACT_FULL_FAMILY_EXCLUSION_PASS' "$out"
