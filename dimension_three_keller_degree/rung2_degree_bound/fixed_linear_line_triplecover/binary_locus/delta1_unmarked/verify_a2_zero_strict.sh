#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

/usr/bin/python3 "$script_dir/verify_a2_zero_sympy.py"
/opt/homebrew/bin/gp -q "$script_dir/verify_a2_zero_pari.gp"
echo "ALL A2-ZERO BOUNDARY CHECKS PASSED"
