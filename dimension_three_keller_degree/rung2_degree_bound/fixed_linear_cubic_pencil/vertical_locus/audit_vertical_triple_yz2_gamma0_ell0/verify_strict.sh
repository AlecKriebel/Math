#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_file=$(mktemp "${TMPDIR:-/tmp}/audit-vertical-yz2.XXXXXX")
optimized_output=$(mktemp "${TMPDIR:-/tmp}/audit-vertical-yz2-opt.XXXXXX")
trap 'rm -f "$output_file" "$optimized_output"' EXIT HUP INT TERM

if rg -n '(^|[[:space:]])(import|from)[[:space:]]+(sympy|sage|cypari|pari)' \
    "$script_dir/verify_vertical_triple_yz2_sparse.py" >/dev/null; then
    echo "FAIL: independent checker imports a prohibited CAS" >&2
    exit 1
fi

if ! /usr/bin/python3 \
    "$script_dir/verify_vertical_triple_yz2_sparse.py" \
    >"$output_file" 2>&1; then
    cat "$output_file"
    exit 1
fi
cat "$output_file"

expected='PASS: independent sparse audit of vertical yz2 chart'
if ! tail -n 1 "$output_file" | grep -Fqx "$expected"; then
    echo "FAIL: success sentinel missing" >&2
    exit 1
fi

if /usr/bin/python3 -O \
    "$script_dir/verify_vertical_triple_yz2_sparse.py" \
    >"$optimized_output" 2>&1; then
    cat "$optimized_output"
    echo "FAIL: optimized mode was not rejected" >&2
    exit 1
fi
if ! grep -Fq 'refusing optimized Python' "$optimized_output"; then
    cat "$optimized_output"
    echo "FAIL: optimized-mode rejection sentinel missing" >&2
    exit 1
fi

echo "PASS: strict wrapper and fail-closed guard"
