#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_root=$(CDPATH= cd -- "$paper_dir/../.." && pwd)
bootstrap_python=${BOOTSTRAP_PYTHON:-python3}
venv="$project_root/.venv-paper2"

"$bootstrap_python" -c '
import sys
assert sys.version_info[:3] == (3, 14, 6), sys.version
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
assert sys.version_info[:3] == (3, 14, 6), sys.version
assert metadata.version("sympy") == "1.14.0"
assert metadata.version("mpmath") == "1.3.0"
print("PASS: Python 3.14.6, SymPy 1.14.0, and mpmath 1.3.0")
'

PYTHON="$venv/bin/python" "$paper_dir/replay.sh"
