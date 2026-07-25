#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_file=$(mktemp "${TMPDIR:-/tmp}/vertical-nonzero-ell.XXXXXX")
optimized_output=$(mktemp "${TMPDIR:-/tmp}/vertical-nonzero-ell-opt.XXXXXX")
trap 'rm -f "$output_file" "$optimized_output"' EXIT HUP INT TERM

if ! /usr/bin/python3 \
    "$script_dir/verify_vertical_nonzero_ell_nontriple_sympy.py" \
    >"$output_file" 2>&1; then
    cat "$output_file" >&2
    exit 1
fi

expected='VERTICAL_NONZERO_ELL_NONTRIPLE_SYMPY_PASS_6E2C91'
actual=$(cat "$output_file")
if [ "$actual" != "$expected" ]; then
    cat "$output_file" >&2
    exit 1
fi

if /usr/bin/python3 -O \
    "$script_dir/verify_vertical_nonzero_ell_nontriple_sympy.py" \
    >"$optimized_output" 2>&1; then
    echo 'optimized Python unexpectedly passed' >&2
    exit 1
fi

printf '%s\n' 'VERTICAL_NONZERO_ELL_NONTRIPLE_STRICT_PASS_57AD24'
