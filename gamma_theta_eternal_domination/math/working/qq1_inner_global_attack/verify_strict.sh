#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/qq1-inner-global.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

python3 "$here/verify_controls.py" >"$temporary/actual.json"
diff -u "$here/expected_result.json" "$temporary/actual.json"
printf '%s\n' 'QQ1 inner global control audit: PASS'
