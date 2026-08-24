#!/bin/sh
set -eu

referee_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_root="$referee_root/materials/k2p_principal_d_plus_submission_referee"
venv_root="$project_root/.venv"
requirements="$project_root/work/final_theorem_release/requirements.txt"

python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else "Python 3.10 or newer is required")'
test -f "$requirements"

python3 -m venv "$venv_root"
"$venv_root/bin/python" -m pip install --upgrade pip
"$venv_root/bin/python" -m pip install -r "$requirements"
"$venv_root/bin/python" -c 'import networkx, sympy; assert networkx.__version__ == "3.5"; assert sympy.__version__ == "1.14.0"; print("Python environment PASS")'

if command -v tectonic >/dev/null 2>&1; then
  tectonic --version
else
  echo "WARNING: Tectonic is not installed; clean manuscript compilation will fail closed." >&2
fi
