#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$HERE/../../.venv/bin/python"

export PYTHONDONTWRITEBYTECODE=1

cd "$HERE"
"$PYTHON" -B exact_fixation.py
"$PYTHON" -B audit_unweighted_atlas.py
"$PYTHON" -B audit_structured_grid.py --max-n 7
"$PYTHON" -B audit_weighted_trees.py --max-n 6
"$PYTHON" -B audit_reversible_f0.py
"$PYTHON" -B audit_directed_kernels.py
"$PYTHON" -B audit_permutation_midpoint.py

cd "$HERE/../../phase4_landmark_closure/obstruction/orbital_symmetrization"
"$PYTHON" -B verify_failed_annealing_routes.py

echo "PASS: exact bounded r=2 hostile package"
echo "OPEN: universal dB complete-graph maximality at r=2"
