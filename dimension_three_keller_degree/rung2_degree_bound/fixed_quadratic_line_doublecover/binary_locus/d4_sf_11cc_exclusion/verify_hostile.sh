#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
keller_python=${KELLER_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
output_file=$(mktemp)
optimized_output=$(mktemp)
trap 'rm -f "$output_file" "$optimized_output"' EXIT HUP INT TERM

"$keller_python" "$audit_dir/hostile_verify.py" | tee "$output_file"
grep -Fx "D4_SF_11CC_HOSTILE_AUDIT_EXACT_PASS" "$output_file" >/dev/null

if "$keller_python" -O "$audit_dir/hostile_verify.py" >"$optimized_output" 2>&1; then
  echo "FAIL: optimized Python was accepted" >&2
  exit 1
fi
grep -F "FAIL: assertions disabled" "$optimized_output" >/dev/null

echo "D4_SF_11CC_HOSTILE_AUDIT_STRICT_PASS"
