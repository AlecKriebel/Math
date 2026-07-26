#!/bin/sh
set -eu

row_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
degree_dir=$(CDPATH= cd -- "$row_dir/.." && pwd)
verticality_dir="$degree_dir/fixed_divisor_verticality"
top_dir="$verticality_dir/all_vertical_top_obstruction"
taxonomy_dir="$degree_dir/taxonomy_freeze"
task_python=${TASK_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}

if [ ! -x "$task_python" ]; then
  echo "FAIL: exact Python interpreter is unavailable" >&2
  exit 2
fi
if ! command -v gp >/dev/null 2>&1; then
  echo "FAIL: PARI/GP is required" >&2
  exit 2
fi

"$task_python" "$verticality_dir/verify_fixed_divisor_verticality_sympy.py"
sh "$verticality_dir/verify_fixed_divisor_verticality_pari_strict.sh"
"$task_python" "$verticality_dir/audit_hostile/audit_reconstruct_modp.py"
sh "$verticality_dir/audit_hostile/test_supplied_runners.sh"

"$task_python" "$top_dir/verify_top_obstruction_sympy.py"
"$task_python" "$top_dir/audit_hostile/audit_reconstruct_mod101.py"
sh "$top_dir/audit_hostile/audit_exact_pari_strict.sh"
sh "$top_dir/audit_hostile/test_audit_guards.sh"

"$task_python" "$row_dir/verify_mixed_orbits_sympy.py"
sh "$row_dir/audit_hostile/verify_mixed_orbits_pari_strict.sh"
sh "$row_dir/audit_hostile/test_fail_closed.sh"

"$task_python" "$row_dir/ranktwo_triple/verify_ranktwo_triple_sympy.py"
sh "$row_dir/ranktwo_triple/audit_hostile/verify_ranktwo_triple_pari_strict.sh"
sh "$row_dir/ranktwo_triple/audit_hostile/test_fail_closed.sh"

sh "$row_dir/rankone_triple/verify_all_strict.sh"
sh "$row_dir/marked_h_distinct/verify_closure_strict.sh"
sh "$taxonomy_dir/audit_bridge_q2_e2_v1/verify_strict.sh"

echo "Q2_E2_A2_B1_D1_N1_FULL_ROW_STRICT_PASS_4D95A1"
