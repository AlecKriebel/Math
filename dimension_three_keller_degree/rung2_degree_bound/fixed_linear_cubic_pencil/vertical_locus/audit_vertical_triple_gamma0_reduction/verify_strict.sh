#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
helper_dir="$script_dir/../audit_vertical_triple_yz2_gamma0_ell0"
output_file=$(mktemp "${TMPDIR:-/tmp}/audit-gamma0-reduction.XXXXXX")
optimized_output=$(mktemp "${TMPDIR:-/tmp}/audit-gamma0-reduction-opt.XXXXXX")
trap 'rm -f "$output_file" "$optimized_output"' EXIT HUP INT TERM

for source_file in \
    "$script_dir/verify_vertical_triple_gamma0_reduction_sparse.py" \
    "$helper_dir/verify_vertical_triple_yz2_sparse.py"
do
    if rg -n '(^|[[:space:]])(import|from)[[:space:]]+(sympy|sage|cypari|pari)' \
        "$source_file" >/dev/null; then
        echo "FAIL: sparse checker imports a prohibited CAS" >&2
        exit 1
    fi
done

if ! /usr/bin/python3 \
    "$script_dir/verify_vertical_triple_gamma0_reduction_sparse.py" \
    >"$output_file" 2>&1; then
    cat "$output_file"
    exit 1
fi
cat "$output_file"

expected='PASS: independent sparse audit of triple gamma=0 reduction'
if ! tail -n 1 "$output_file" | grep -Fqx "$expected"; then
    echo "FAIL: success sentinel missing" >&2
    exit 1
fi

if /usr/bin/python3 -O \
    "$script_dir/verify_vertical_triple_gamma0_reduction_sparse.py" \
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
