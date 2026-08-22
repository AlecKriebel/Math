#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_root=$(CDPATH= cd -- "$paper_dir/../.." && pwd)
bootstrap_python=${BOOTSTRAP_PYTHON:-python3}
venv="$project_root/.venv-paper2"

"$bootstrap_python" -c '
import sys
if sys.flags.optimize != 0:
    raise SystemExit(
        "ERROR: optimized Python is unsupported because verification checks must remain active"
    )
if sys.version_info[:3] != (3, 14, 6):
    raise SystemExit(f"ERROR: Python 3.14.6 is required; found {sys.version}")
'

if [ ! -x "$venv/bin/python" ]; then
  "$bootstrap_python" -m venv "$venv"
fi

"$venv/bin/python" -m pip install \
  --disable-pip-version-check \
  --no-cache-dir \
  --requirement "$paper_dir/requirements.txt"

"$venv/bin/python" -c '
import importlib.metadata as metadata
import sys
if sys.flags.optimize != 0:
    raise SystemExit(
        "ERROR: optimized Python is unsupported because verification checks must remain active"
    )
if sys.version_info[:3] != (3, 14, 6):
    raise SystemExit(f"ERROR: Python 3.14.6 is required; found {sys.version}")
sympy_version = metadata.version("sympy")
mpmath_version = metadata.version("mpmath")
if sympy_version != "1.14.0":
    raise SystemExit(
        f"ERROR: SymPy 1.14.0 is required; found {sympy_version}"
    )
if mpmath_version != "1.3.0":
    raise SystemExit(
        f"ERROR: mpmath 1.3.0 is required; found {mpmath_version}"
    )
print("PASS: Python 3.14.6, SymPy 1.14.0, and mpmath 1.3.0")
'

PYTHON="$venv/bin/python" "$paper_dir/replay.sh"
"$venv/bin/python" "$paper_dir/tests/test_verifier_fail_closed.py"
