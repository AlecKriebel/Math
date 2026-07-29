#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/qq1-global-coupling.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

python3 -I -B -W error "$here/verify_global_coupling.py" \
  > "$temporary/result.json"
cmp "$here/expected_result.json" "$temporary/result.json"
python3 -I -B -W error "$here/audit_manifest.py"
printf '%s\n' 'QQ1 bow-tie global coupling: PASS'
