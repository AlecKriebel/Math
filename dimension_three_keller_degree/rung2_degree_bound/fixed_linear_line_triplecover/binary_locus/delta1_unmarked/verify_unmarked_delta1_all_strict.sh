#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

/usr/bin/python3 "$script_dir/verify_generic_contact_decomposition_sympy.py"
"$script_dir/verify_unmarked_half_strict.sh"
"$script_dir/verify_unmarked_cubic_strict.sh"
"$script_dir/verify_b1_zero_strict.sh"
"$script_dir/verify_c0_zero_strict.sh"
"$script_dir/verify_a2_zero_strict.sh"
echo "ALL UNMARKED DELTA1 PRIMARY AND LEAF CHECKS PASSED"
