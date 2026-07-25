#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

"$script_dir/verify_rankone_triple_sympy_strict.sh"
"$script_dir/test_fail_closed.sh"
"$script_dir/verify_a0_pari_strict.sh"
"$script_dir/test_a0_pari_fail_closed.sh"
"$script_dir/audit_hostile_external/verify_a0_external_pari_strict.sh"
"$script_dir/audit_hostile_external/test_fail_closed.sh"
"$script_dir/aopen_independent/verify_aopen_pari_strict.sh"
"$script_dir/aopen_independent/test_fail_closed.sh"

echo "PASS complete rank-one triple-companion verification suite"
