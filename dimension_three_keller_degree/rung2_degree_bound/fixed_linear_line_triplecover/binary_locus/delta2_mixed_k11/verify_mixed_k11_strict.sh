#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin="${PYTHON_BIN:-/usr/bin/python3}"

"$python_bin" -u "$script_dir/verify_mixed_k11_sympy.py"

gp_output=$(/opt/homebrew/bin/gp -q "$script_dir/verify_mixed_k11_pari.gp" 2>&1)
printf '%s\n' "$gp_output"
if ! printf '%s\n' "$gp_output" |
    grep -Fq "PASS independent PARI mixed {1,1} reconstruction"; then
    echo "FAIL PARI replay did not reach its terminal certificate" >&2
    exit 1
fi
if printf '%s\n' "$gp_output" |
    grep -Eq 'skipping file|at top-level|syntax error|not a function|incorrect type'; then
    echo "FAIL PARI replay emitted an interpreter error" >&2
    exit 1
fi

if PYTHONOPTIMIZE=1 "$python_bin" "$script_dir/verify_mixed_k11_sympy.py" \
    >/dev/null 2>&1; then
    echo "FAIL optimized Python bypassed the assertion guard" >&2
    exit 1
fi

echo "ALL FIXED-LINEAR MIXED {1,1} DELTA2 CHECKS PASSED"
