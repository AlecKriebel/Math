#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)
PYTHON="$ROOT/.venv/bin/python"
BASE="$ROOT/universal_simultaneous_amplification/phase4_landmark_closure/threshold/one_third_separator"

export PYTHONDONTWRITEBYTECODE=1

"$PYTHON" "$BASE/verify_one_third_poisson.py" --all
"$PYTHON" "$BASE/verify_one_third_poisson.py" --pendant
"$PYTHON" "$BASE/verify_clique_pendant_affine_limit.py"
"$PYTHON" "$BASE/verify_weighted_triangle.py"
"$PYTHON" "$BASE/verify_common_correction_barrier.py"
"$PYTHON" "$BASE/verify_near_disconnected_artifact.py"
