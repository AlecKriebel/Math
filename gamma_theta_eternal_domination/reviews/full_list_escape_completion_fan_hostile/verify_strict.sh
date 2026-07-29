#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
candidate="$here/../../math/working/full_list_escape_completion_fan"
actual=$(mktemp "${TMPDIR:-/tmp}/c173-clean.XXXXXX")
trap 'rm -f "$actual"' EXIT HUP INT TERM

sh "$candidate/verify_strict.sh"
python3 -I -B -W error "$here/verify_clean.py" > "$actual"
cmp "$here/expected_clean.json" "$actual"

python3 -I -B -W error - "$here" "$candidate" <<'PY'
import hashlib
import json
import pathlib
import sys

review = pathlib.Path(sys.argv[1])
candidate = pathlib.Path(sys.argv[2])
manifest = json.loads((review / "MANIFEST.json").read_text(encoding="utf-8"))
for name, expected in manifest["review_hashes"].items():
    actual = hashlib.sha256((review / name).read_bytes()).hexdigest()
    assert actual == expected, (name, expected, actual)

assert hashlib.sha256((candidate / "NOTE.md").read_bytes()).hexdigest() == (
    manifest["candidate_note_sha256"]
)
assert hashlib.sha256((candidate / "MANIFEST.json").read_bytes()).hexdigest() == (
    manifest["candidate_manifest_sha256"]
)
candidate_manifest = json.loads(
    (candidate / "MANIFEST.json").read_text(encoding="utf-8")
)
working = candidate.parent
for relative, expected in candidate_manifest["accepted_dependency_hashes"].items():
    actual = hashlib.sha256((working / relative).read_bytes()).hexdigest()
    assert actual == expected, (relative, expected, actual)
PY

grep -Fq '**UNCONDITIONAL PASS**' "$here/REVIEW.md"
grep -Fq 'No mathematical defect' "$here/REVIEW.md"

actual_sha=$(shasum -a 256 "$actual" | awk '{print $1}')
expected_sha=$(shasum -a 256 "$here/expected_clean.json" | awk '{print $1}')
test "$actual_sha" = "$expected_sha"
echo "PASS C-173 hostile review $actual_sha"
