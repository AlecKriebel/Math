#!/bin/zsh
set -euo pipefail

package_dir=${0:A:h}
export PYTHONDONTWRITEBYTECODE=1

/usr/bin/python3 "$package_dir/../w4_search/test_finite_field_norm.py"
/usr/bin/python3 "$package_dir/test_depth4_evaluator.py"
/usr/bin/python3 "$package_dir/verify_w5_modular.py"
"$package_dir/audit_w5_hostile/verify_strict_and_faults.sh"

print "PASS strict level-five primary and hostile replay"
