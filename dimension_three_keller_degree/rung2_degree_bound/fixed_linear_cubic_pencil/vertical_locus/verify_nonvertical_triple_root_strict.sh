#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_file=$(mktemp "${TMPDIR:-/tmp}/nonvertical-triple-root.XXXXXX")
trap 'rm -f "$output_file"' EXIT HUP INT TERM

if ! /usr/bin/python3 "$script_dir/verify_nonvertical_triple_root_sympy.py" \
    >"$output_file" 2>&1; then
    cat "$output_file"
    exit 1
fi

cat "$output_file"
expected='nonvertical triple-root constant-minor checks passed'
if ! tail -n 1 "$output_file" | grep -Fqx "$expected"; then
    echo "FAIL: exact success sentinel missing" >&2
    exit 1
fi
