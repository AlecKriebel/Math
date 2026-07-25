#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_file=$(mktemp "${TMPDIR:-/tmp}/c0-hostile-pari.XXXXXX")
trap 'rm -f "$output_file"' EXIT HUP INT TERM

if ! gp -s 400000000 -fq "$audit_dir/verify_hostile_pari.gp" >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

cat "$output_file"

if grep -E '\*\*\*|FAIL:|syntax error|incorrect type|user error' "$output_file" >/dev/null; then
  echo "FAIL: PARI/GP emitted an error diagnostic" >&2
  exit 1
fi

if ! grep -Fx 'ALL HOSTILE PARI/GP c=0 AUDIT CHECKS PASSED' "$output_file" >/dev/null; then
  echo "FAIL: final success marker missing" >&2
  exit 1
fi
