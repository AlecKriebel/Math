#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
temporary_dir=$(mktemp -d "${TMPDIR:-/tmp}/nonvertical-mutations.XXXXXX")
trap 'rm -rf "$temporary_dir"' EXIT HUP INT TERM

source_file="$script_dir/verify_nonvertical_nontriple_e4_sympy.py"

mutate_and_require_failure() {
    label=$1
    old=$2
    new=$3
    target="$temporary_dir/$label.py"
    sed "s|$old|$new|" "$source_file" >"$target"
    if /usr/bin/python3 "$target" >"$temporary_dir/$label.out" 2>&1; then
        echo "FAIL: mutation $label escaped the verifier" >&2
        cat "$temporary_dir/$label.out"
        exit 1
    fi
    echo "  PASS mutation rejected: $label"
}

# Violate the first E4 leaf by inserting an xz term into A.
mutate_and_require_failure \
    branch_a \
    'coefficient_equations(q0, alpha \* z\*\*2, B, L1)' \
    'coefficient_equations(q0, alpha * z**2 + x*z, B, L1)'

# Violate the second E4 leaf by inserting a nonzero binary part into B.
mutate_and_require_failure \
    branch_b \
    'B2 = b3 \* x \* z + b4 \* y \* z + b5 \* z\*\*2' \
    'B2 = x**2 + b3 * x * z + b4 * y * z + b5 * z**2'

echo "PASS: both nonvertical E4 branch mutations fail closed"
