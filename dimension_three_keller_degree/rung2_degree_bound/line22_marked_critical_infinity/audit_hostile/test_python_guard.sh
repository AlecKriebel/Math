#!/bin/sh
set -eu

audit_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
package_directory=$(CDPATH= cd -- "$audit_directory/.." && pwd)
script="$package_directory/verify_line22_marked_critical_infinity_sympy.py"
output_file=$(mktemp "${TMPDIR:-/tmp}/line22-mci-opt.XXXXXX")
trap 'rm -f "$output_file"' EXIT HUP INT TERM

set +e
/usr/bin/python3 -O "$script" >"$output_file" 2>&1
status_code=$?
set -e

if [ "$status_code" -eq 0 ]; then
    cat "$output_file"
    echo "FAIL: SymPy verifier accepted optimized mode" >&2
    exit 1
fi
if ! grep -Fq 'verification must not run with Python optimization' "$output_file"; then
    cat "$output_file"
    echo "FAIL: SymPy verifier failed for an unexpected reason" >&2
    exit 1
fi

echo "PASS: SymPy verifier rejects optimized mode"
