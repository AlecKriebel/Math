#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/qq1-hot-layer-verify.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

python3 -I "$here/verify_implication.py" > "$temporary/result.json"
cmp "$here/expected_result.json" "$temporary/result.json"
printf '%s\n' 'QQ1 hot-layer endgame audit: PASS'
