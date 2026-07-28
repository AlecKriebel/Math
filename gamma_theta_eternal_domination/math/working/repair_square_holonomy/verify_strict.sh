#!/bin/sh
set -eu

base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/repair-square-holonomy.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

PYTHONNOUSERSITE=1 python3 -I "$base/verify_control.py" > "$temporary/result.json"
cmp "$base/expected_result.json" "$temporary/result.json"
actual=$(shasum -a 256 "$temporary/result.json" | awk '{print $1}')
expected=$(awk 'NF {print $1; exit}' "$base/expected.sha256")

test "$actual" = "$expected"
PYTHONNOUSERSITE=1 python3 -I "$base/verify_abstract.py" > "$temporary/abstract.json"
cmp "$base/expected_abstract.json" "$temporary/abstract.json"
printf '%s\n' 'repair-square holonomy boundary audit: PASS'
