#!/bin/zsh
set -euo pipefail

package_dir=${0:A:h}
audit_dir="$package_dir/../../fixed_quadratic_line_doublecover/binary_locus/audit_abstract_hb_e6_hostile"

"$audit_dir/verify_strict_and_faults.sh"
print "PASS abstract binary-quartic lemma transfers without a coprimality hypothesis"
