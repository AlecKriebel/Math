#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$paper_dir/../.." && pwd)
if [ -x "$root/.venv-paper1/bin/python" ]; then
  default_python="$root/.venv-paper1/bin/python"
else
  default_python="$root/.venv/bin/python"
fi
python=${PYTHON:-"$default_python"}

if [ ! -x "$python" ]; then
  python=${PYTHON:-python3}
fi

if ! "$python" -c 'import sympy, flint' >/dev/null 2>&1; then
  echo "Paper I replay dependencies are missing for: $python" >&2
  echo "Run ./submission/bootstrap_replay.sh first, or set PYTHON to the pinned environment." >&2
  exit 2
fi

export PYTHONDONTWRITEBYTECODE=1

cd "$root"

# Strong-selection, directed-support, triangle, K4, and lumpability suite.
# Deliberately omit the legacy manuscript build from this certificate replay.
make test verify directed triangle n4 phase3-check PYTHON="$python"

# Fitness-two dual, complete-refresh, and all three physical Hessian sectors.
cd "$root/phase5_exact_threshold/r2_determinant"
"$python" verify_r2_determinant.py
"$python" verify_complete_refresh_forest.py
"$python" verify_antisymmetric_hessian.py
"$python" verify_true_inverse_rank_symmetric_phase.py
"$python" verify_hessian_sectors.py

cd "$root/phase5_exact_threshold/r2_standard_physical_phase"
"$python" verify_physical_standard_phase.py

# General directed OR dual and active-Perron bridge (no reversibility used).
cd "$root/phase4_landmark_closure/obstruction/r2_marked_lift_v2"
"$python" verify_marked_lift.py

# Independent direct generator check on the regular undirected sector.
cd "$root/phase5_exact_threshold/r2_regular_sector"
"$python" verify_local_complete_hessian.py

# Paper-level normalization and theorem-integration audit.
cd "$paper_dir"
"$python" verify_paper_claims.py
