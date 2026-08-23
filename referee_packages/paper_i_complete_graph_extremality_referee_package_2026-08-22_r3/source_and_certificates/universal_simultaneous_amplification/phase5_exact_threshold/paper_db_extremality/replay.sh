#!/bin/sh
set -eu

if [ "${PYTHON+x}" = x ]; then
  echo "PYTHON overrides are forbidden for the internal Paper I replay stage" >&2
  exit 2
fi
case ${PYTHONOPTIMIZE-} in
  ""|0) ;;
  *)
    echo "Refusing inherited PYTHONOPTIMIZE=${PYTHONOPTIMIZE}" >&2
    exit 2
    ;;
esac
unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME PYTHONSTARTUP PYTHONINSPECT \
  PYTHONWARNINGS PYTHONPYCACHEPREFIX PYTHONCASEOK PYTHONPLATLIBDIR \
  PYTHONUSERBASE PYTHONEXECUTABLE PYTHON MAKEFLAGS MFLAGS GNUMAKEFLAGS \
  MAKEOVERRIDES
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1

if [ "$#" -ne 2 ] || [ "$1" != "--internal-from-bootstrap" ]; then
  echo "replay.sh is an internal verifier stage; use the enclosing package's run_all_referee_checks.sh" >&2
  exit 2
fi
runtime_dir=$2
case "$runtime_dir" in
  /*) ;;
  *)
    echo "Internal replay runtime must be an absolute directory: $runtime_dir" >&2
    exit 2
    ;;
esac
if [ ! -d "$runtime_dir" ]; then
  echo "Internal replay runtime is missing: $runtime_dir" >&2
  exit 2
fi
runtime_dir=$(CDPATH= cd -- "$runtime_dir" && pwd)
python="$runtime_dir/venv/bin/python"
cache="$runtime_dir/pycache"
if [ ! -x "$python" ]; then
  echo "Fresh Paper I virtual-environment interpreter is missing: $python" >&2
  exit 2
fi
if [ ! -d "$cache" ] || [ -n "$(find "$cache" -mindepth 1 -print -quit)" ]; then
  echo "Fresh Paper I bytecode-cache directory is missing or nonempty: $cache" >&2
  exit 2
fi

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$paper_dir/../.." && pwd)
"$python" -I -B -X "pycache_prefix=$cache" \
  "$paper_dir/submission/verify_execution_safety.py" \
  --runtime --dependencies --audit-sources --expected-cache-prefix "$cache"

cd "$root"

# Strong-selection, directed-support, triangle, K4, and lumpability suite.
# Invoke each check directly so unrelated project Make targets and inherited
# Make behavior are outside this internal verifier stage.
run_python() {
  PYTHONPATH="$root" "$python" -B -X "pycache_prefix=$cache" "$@"
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

if [ -n "$(find "$cache" -mindepth 1 -print -quit)" ]; then
  echo "Controlled Paper I bytecode cache was unexpectedly populated: $cache" >&2
  exit 2
fi
echo "PASS: internal verifier stage completed with an empty controlled cache"
