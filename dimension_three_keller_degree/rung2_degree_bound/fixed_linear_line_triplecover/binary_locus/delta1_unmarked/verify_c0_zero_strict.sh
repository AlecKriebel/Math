#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

/usr/bin/python3 "$script_dir/verify_c0_zero_sympy.py"
/opt/homebrew/bin/gp -q "$script_dir/verify_c0_zero_pari.gp"
echo "ALL C0-ZERO BOUNDARY CHECKS PASSED"
