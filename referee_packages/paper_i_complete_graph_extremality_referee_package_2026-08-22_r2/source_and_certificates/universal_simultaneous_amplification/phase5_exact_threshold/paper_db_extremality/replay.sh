#!/bin/sh
set -eu

case ${PYTHONOPTIMIZE-} in
  ""|0) ;;
  *)
    echo "Refusing inherited PYTHONOPTIMIZE=${PYTHONOPTIMIZE}" >&2
    exit 2
    ;;
esac
unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME PYTHONSTARTUP PYTHONINSPECT \
  PYTHONWARNINGS PYTHONPYCACHEPREFIX PYTHONCASEOK PYTHONPLATLIBDIR \
  PYTHONUSERBASE PYTHONEXECUTABLE MAKEFLAGS MFLAGS GNUMAKEFLAGS MAKEOVERRIDES
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$paper_dir/../.." && pwd)
if [ -x "$root/.venv-paper1/bin/python" ]; then
  default_python="$root/.venv-paper1/bin/python"
else
  default_python="$root/.venv/bin/python"
fi
python=${PYTHON:-"$default_python"}

case "$python" in
  */*)
    if [ ! -x "$python" ]; then
      echo "Selected Paper I Python is not executable: $python" >&2
      exit 2
    fi
    ;;
  *)
    if ! command -v "$python" >/dev/null 2>&1; then
      echo "Selected Paper I Python is unavailable: $python" >&2
      exit 2
    fi
    python=$(command -v "$python")
    ;;
esac

if ! preflight_output=$("$python" -I \
  "$paper_dir/submission/verify_execution_safety.py" \
  --runtime --dependencies --audit-sources); then
  echo "Selected interpreter failed the Paper I safety preflight: $python" >&2
  exit 2
fi
case "$preflight_output" in
  *PAPER1_EXECUTION_SAFETY_OK*) ;;
  *)
    echo "Selected command did not execute the Paper I safety preflight: $python" >&2
    exit 2
    ;;
esac
printf '%s\n' "$preflight_output"

cd "$root"

# Strong-selection, directed-support, triangle, K4, and lumpability suite.
# Invoke each check directly so unrelated project Make targets and inherited
# Make behavior are outside this standalone certificate.
run_python() {
  PYTHONPATH="$root" "$python" "$@"
}
run_python -m unittest discover -s tests -v
run_python verification/verify_obstruction.py
run_python phase1_directed/verify_directed_db_strong.py
run_python phase2_triangle/derive_certificate.py
run_python phase2_triangle/crosscheck_exact_solver.py
run_python phase2_triangle/audit/independent_triangle_audit.py
run_python phase2_n4/derive_lumped_certificates.py
run_python phase2_n4/crosscheck_full_chain.py
run_python phase3_asymptotic/verify_lumping.py

# Fitness-two dual, complete-refresh, and all three physical Hessian sectors.
cd "$root/phase5_exact_threshold/r2_determinant"
run_python verify_r2_determinant.py
run_python verify_complete_refresh_forest.py
run_python verify_antisymmetric_hessian.py
run_python verify_true_inverse_rank_symmetric_phase.py
run_python verify_hessian_sectors.py

cd "$root/phase5_exact_threshold/r2_standard_physical_phase"
run_python verify_physical_standard_phase.py

# General directed OR dual and active-Perron bridge (no reversibility used).
cd "$root/phase4_landmark_closure/obstruction/r2_marked_lift_v2"
run_python verify_marked_lift.py

# Independent direct generator check on the regular undirected sector.
cd "$root/phase5_exact_threshold/r2_regular_sector"
run_python verify_local_complete_hessian.py

# Paper-level normalization and theorem-integration audit.
cd "$paper_dir"
run_python verify_paper_claims.py
