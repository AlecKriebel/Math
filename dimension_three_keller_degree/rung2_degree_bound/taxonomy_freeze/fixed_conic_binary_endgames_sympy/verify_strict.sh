#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

/usr/bin/python3 -c 'import sympy, sys; sys.exit(0 if sympy.__version__ == "1.14.0" else "required exact SymPy version: 1.14.0")'
/usr/bin/python3 -O "$HERE/verify_binary_fixed_conic_endgames.py"
