#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
campaign=$(CDPATH= cd -- "$here/../.." && pwd)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/higher-rank-hostile.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

python3 -I -B -W error "$here/review_check.py" > "$temporary/result.json"
cmp "$here/expected_result.json" "$temporary/result.json"

python3 -I -B -W error - "$here" "$campaign" <<'PY'
import hashlib
import json
import pathlib
import sys

review = pathlib.Path(sys.argv[1])
campaign = pathlib.Path(sys.argv[2])
manifest = json.loads((review / "MANIFEST.json").read_text())
for name, expected in manifest["review_sha256"].items():
    actual = hashlib.sha256((review / name).read_bytes()).hexdigest()
    assert actual == expected, (name, expected, actual)
for name, expected in manifest["candidate_sha256"].items():
    actual = hashlib.sha256((campaign / name).read_bytes()).hexdigest()
    assert actual == expected, (name, expected, actual)
PY

printf '%s\n' 'higher-rank fan descent hostile review: PASS'
