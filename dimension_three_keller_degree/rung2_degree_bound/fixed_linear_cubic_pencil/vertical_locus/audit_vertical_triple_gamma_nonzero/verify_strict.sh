#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_file=$(mktemp "${TMPDIR:-/tmp}/vertical-gamma-nonzero-audit.XXXXXX")
optimized_output=$(mktemp "${TMPDIR:-/tmp}/vertical-gamma-nonzero-audit-opt.XXXXXX")
trap 'rm -f "$output_file" "$optimized_output"' EXIT HUP INT TERM

if ! /usr/bin/python3 \
    "$script_dir/verify_vertical_triple_gamma_nonzero_sparse.py" \
    >"$output_file" 2>&1; then
    cat "$output_file" >&2
    exit 1
fi

expected='PASS q_C: raw/exterior E6, claims, and mutations
PASS q_B: raw/exterior E6, claims, and mutations
PASS q_E: raw/exterior E6, claims, and mutations
PASS: HOSTILE_VERTICAL_TRIPLE_GAMMA_NONZERO_SPARSE_8D41C6'
actual=$(cat "$output_file")
if [ "$actual" != "$expected" ]; then
    cat "$output_file" >&2
    exit 1
fi

if /usr/bin/python3 -O \
    "$script_dir/verify_vertical_triple_gamma_nonzero_sparse.py" \
    >"$optimized_output" 2>&1; then
    echo 'optimized Python unexpectedly passed' >&2
    exit 1
fi

printf '%s\n' 'PASS: HOSTILE_VERTICAL_TRIPLE_GAMMA_NONZERO_STRICT_119F2A'
