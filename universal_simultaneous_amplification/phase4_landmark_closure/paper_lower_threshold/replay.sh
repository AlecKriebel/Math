#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_dir=$(CDPATH= cd -- "$paper_dir/../../.." && pwd)
python_bin="$repo_dir/.venv/bin/python"
log_dir="$paper_dir/output/verification"

mkdir -p "$log_dir"
export PYTHONHASHSEED=0

if [ ! -x "$python_bin" ]; then
  echo "missing project interpreter: $python_bin" >&2
  exit 1
fi

run_check() {
  name=$1
  script=$2
  shift 2
  echo "RUN $name"
  (cd "$(dirname "$script")" && "$python_bin" "$(basename "$script")" "$@") \
    2>&1 | tee "$log_dir/$name.log"
}

{
  "$python_bin" --version
  "$python_bin" -c 'import sympy, scipy; print("sympy", sympy.__version__); print("scipy", scipy.__version__)'
} > "$log_dir/environment.log" 2>&1

base="$repo_dir/universal_simultaneous_amplification/phase4_landmark_closure"
run_check triangle_module "$base/construction/verify_triangle_module.py"
run_check triangle_star_independent "$base/threshold/verify_triangle_star.py"
run_check center_triangle_lumping "$base/construction/verify_center_triangle_lumping.py"
run_check fixed_rank_portal "$base/construction/higher_threshold/asymmetric_portal_incidence/verify_higher_rank_separation.py"
run_check direct_trace_exact "$base/construction/higher_threshold/direct_portal_network/verify_direct_trace_exact.py"
run_check diffuse_growing_portal "$base/construction/higher_threshold/direct_portal_network/growing_portal_network/verify_diffuse_limit_exact.py"
run_check endpoint_product_counterexample "$base/threshold/clique_pendant_product_counterexample/certify_counterexample.py"
run_check endpoint_product_independent "$base/threshold/clique_pendant_product_counterexample/verify_independent.py"
run_check endpoint_product_audit "$base/threshold/clique_pendant_product_audit/verify_clique_pendant_product.py" --exact
run_check growing_endpoint_product "$base/threshold/clique_pendant_asymptotic/verify_asymptotic_constants.py"
run_check one_third_affine "$base/threshold/one_third_separator/verify_clique_pendant_affine_limit.py"
run_check one_third_triangle "$base/threshold/one_third_separator/verify_weighted_triangle.py"
run_check one_third_green "$base/threshold/one_third_separator/verify_one_third_poisson.py" --all
run_check weighted_pendant "$base/threshold/weighted_clique_pendant_endpoint/verify_exact.py"
run_check direct_q2_portal "$base/construction/higher_threshold/direct_portal_network/verify_q2_scalar_separator.py"

echo "ALL EXACT REPLAY CHECKS PASSED"
