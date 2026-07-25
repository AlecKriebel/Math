#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

/usr/bin/python3 "$script_dir/verify_vertical_ell_zero_nontriple_sympy.py"

if /usr/bin/python3 -O "$script_dir/verify_vertical_ell_zero_nontriple_sympy.py" \
    >/dev/null 2>&1
then
    echo "FAIL: optimized Python was not rejected" >&2
    exit 1
fi

echo "VERTICAL_ELL_ZERO_NONTRIPLE_STRICT_PASS_0B36A2"
