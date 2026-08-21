#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

/usr/bin/python3 "$script_dir/verify_unmarked_cubic_sympy.py"
/opt/homebrew/bin/gp -q "$script_dir/verify_unmarked_cubic_pari.gp"
echo "ALL UNMARKED CUBIC-CONTACT CHECKS PASSED"
