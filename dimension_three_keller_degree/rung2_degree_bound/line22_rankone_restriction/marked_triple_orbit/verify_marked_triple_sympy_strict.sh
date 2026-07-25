#!/bin/sh
set -eu

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_file=$(mktemp "${TMPDIR:-/tmp}/marked-triple-sympy.XXXXXX")
trap 'rm -f "$output_file"' EXIT HUP INT TERM

if ! /usr/bin/python3 -u \
  "$artifact_dir/verify_marked_triple_sympy.py" \
  >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

cat "$output_file"

if grep -E 'Traceback|AssertionError|FAIL:' "$output_file" >/dev/null; then
  echo "FAIL: SymPy emitted an error diagnostic" >&2
  exit 1
fi

if ! grep -Fx \
  'ALL MARKED TRIPLE-ORBIT SYMPY CERTIFICATES PASSED' \
  "$output_file" >/dev/null; then
  echo "FAIL: final SymPy success marker missing" >&2
  exit 1
fi
