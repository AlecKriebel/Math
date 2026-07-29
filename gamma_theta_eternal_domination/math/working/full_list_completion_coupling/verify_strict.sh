#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT HUP INT TERM

python3 "$here/verify_candidate.py" > "$tmp"
cmp "$tmp" "$here/expected_result.json"

actual_sha=$(shasum -a 256 "$tmp" | awk '{print $1}')
expected_sha=$(python3 - "$here/MANIFEST.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as stream:
    print(json.load(stream)["strict_result_sha256"])
PY
)

test "$actual_sha" = "$expected_sha"
printf '%s\n' "PASS supported-pair completion fan strict replay $actual_sha"
