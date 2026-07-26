#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
keller_python=${KELLER_D4_DN3_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
output_file=$(mktemp)
trap 'rm -f "$output_file"' EXIT HUP INT TERM

"$keller_python" "$audit_dir/verify_zero_binary_slice.py" | tee "$output_file"
grep -Fx "D4_DN3_BOUNDED_SCOPE_AUDIT_STRICT_PASS" "$output_file" >/dev/null

echo "D4_DN3_FULL_AUDIT_BOUNDED_PASS"
