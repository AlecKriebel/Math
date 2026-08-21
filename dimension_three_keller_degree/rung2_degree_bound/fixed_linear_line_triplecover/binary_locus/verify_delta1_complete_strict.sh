#!/bin/zsh
set -euo pipefail

package_dir=${0:A:h}

"$package_dir/verify_abstract_transfer_strict.sh"
"$package_dir/power_fibre/verify_general_power_fibre_strict.sh"
"$package_dir/delta1_marked/verify_marked_delta1_strict.sh"
"$package_dir/delta1_unmarked/verify_unmarked_delta1_all_strict.sh"
print "ALL FIXED-LINEAR EXACT-DELTA1 PRIMARY AND LEAF CHECKS PASSED"
