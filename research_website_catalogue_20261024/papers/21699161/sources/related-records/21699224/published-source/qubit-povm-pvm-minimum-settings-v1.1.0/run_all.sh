#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ "${PYTHON+x}" = x ]; then
    python_bin=$PYTHON
elif [ -x "$project_dir/../.venv/bin/python" ]; then
    python_bin="$project_dir/../.venv/bin/python"
else
    python_bin=python3
fi

export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0

printf '%s\n' '== Environment =='
"$python_bin" - <<'PY'
import platform
import sys

import sympy

expected_sympy = "1.14.0"
reference_python = "3.14.6"
if sympy.__version__ != expected_sympy:
    raise SystemExit(
        f"SymPy {expected_sympy} is required; found {sympy.__version__}"
    )

print(f"Python {platform.python_version()}")
print(f"Reference Python {reference_python} (pinned in .python-version)")
print(f"SymPy {sympy.__version__}")
print(f"Executable {sys.executable}")
PY

printf '%s\n' '== Artifact integrity =='
"$python_bin" - "$project_dir/artifacts" <<'PY'
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

artifact_dir = Path(sys.argv[1]).resolve()
manifest = artifact_dir / "SHA256SUMS.txt"
checked = 0

for raw_line in manifest.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()
    if not line or line.startswith("#"):
        continue
    expected, relative_name = line.split(maxsplit=1)
    artifact = (artifact_dir / relative_name).resolve()
    if artifact_dir not in artifact.parents:
        raise SystemExit(f"Manifest path escapes artifact directory: {relative_name}")
    actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(
            f"SHA-256 mismatch for {relative_name}: expected {expected}, got {actual}"
        )
    print(f"[PASS] {relative_name}")
    checked += 1

print(f"Verified {checked} exact artifacts.")
PY

printf '%s\n' '== Exact 3x2 separation =='
"$python_bin" \
    "$project_dir/artifacts/three_by_two_separation/verify_exact.py"

printf '%s\n' '== Exact 2x2 closure identities =='
"$python_bin" \
    "$project_dir/artifacts/two_by_two_closure/verify_exact.py"

printf '%s\n' '== Exact rank-zero construction =='
"$python_bin" \
    "$project_dir/artifacts/two_by_two_closure/rank_zero_simulator.py"

printf '%s\n' '== All exact reproducibility checks passed =='
