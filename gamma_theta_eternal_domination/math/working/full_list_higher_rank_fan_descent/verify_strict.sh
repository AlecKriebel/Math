#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
actual=$(mktemp "${TMPDIR:-/tmp}/higher-rank-fan.XXXXXX")
trap 'rm -f "$actual"' EXIT HUP INT TERM

python3 -I -B -W error "$here/verify_normal_form.py" > "$actual"
cmp "$here/expected_result.json" "$actual"

python3 -I -B -W error - "$here" <<'PY'
import hashlib
import json
import pathlib
import sys

here = pathlib.Path(sys.argv[1])
manifest = json.loads((here / "MANIFEST.json").read_text(encoding="utf-8"))
for name, expected in manifest["file_hashes"].items():
    actual = hashlib.sha256((here / name).read_bytes()).hexdigest()
    assert actual == expected, (name, expected, actual)
campaign = here.parents[2]
for relative, expected in manifest["dependency_hashes"].items():
    actual = hashlib.sha256((campaign / relative).read_bytes()).hexdigest()
    assert actual == expected, (relative, expected, actual)
PY

grep -Fq 'Theorem 1.1 (descending petal normal form) — PROVED CANDIDATE' "$here/NOTE.md"
grep -Fq 'Theorem 2.1 (finite higher-rank fan exit) — PROVED CANDIDATE' "$here/NOTE.md"
grep -Fq 'Theorem 3.1 (target petals or a common target hub) — PROVED CANDIDATE' "$here/NOTE.md"
actual_sha=$(shasum -a 256 "$actual" | awk '{print $1}')
expected_sha=$(shasum -a 256 "$here/expected_result.json" | awk '{print $1}')
test "$actual_sha" = "$expected_sha"
echo "PASS higher-rank fan normal form $actual_sha"
