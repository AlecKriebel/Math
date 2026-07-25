#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

"$script_dir/verify_a0_external_pari_strict.sh"
"$script_dir/../aopen_independent/verify_aopen_pari_strict.sh"
"$script_dir/../aopen_independent/test_fail_closed.sh"

echo "PASS full rank-one triple coverage: external A=0 plus audited A!=0"
