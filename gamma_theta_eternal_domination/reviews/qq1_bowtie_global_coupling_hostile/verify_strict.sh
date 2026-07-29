#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
actual=$(mktemp)
trap 'rm -f "$actual"' EXIT HUP INT TERM

python3 "$here/independent_verify.py" >"$actual"
python3 -m json.tool "$actual" >/dev/null
cmp "$actual" "$here/expected_result.json"
python3 "$here/audit_manifest.py"
echo "QQ1 global-coupling hostile review: VERIFIED"
