#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin="${PYTHON_BIN:-/usr/bin/python3}"

"$python_bin" -u "$script_dir/verify_mixed_k20_sympy.py"
/opt/homebrew/bin/gp -q "$script_dir/verify_mixed_k20_pari.gp"

if PYTHONOPTIMIZE=1 "$python_bin" "$script_dir/verify_mixed_k20_sympy.py" \
    >/dev/null 2>&1; then
    echo "FAIL optimized Python bypassed the assertion guard" >&2
    exit 1
fi

echo "ALL FIXED-LINEAR MIXED {2,0} DELTA2 CHECKS PASSED"
