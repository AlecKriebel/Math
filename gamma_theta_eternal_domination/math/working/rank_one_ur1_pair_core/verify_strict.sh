#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/rank-one-QQ1-controls.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

python3 -I "$here/verify_control.py" > "$temporary/result.json"
actual=$(shasum -a 256 "$temporary/result.json" | awk '{print $1}')
expected=$(tr -d '[:space:]' < "$here/expected.sha256")
test "$actual" = "$expected"
printf '%s\n' 'rank-one QQ1 collision controls: PASS'
