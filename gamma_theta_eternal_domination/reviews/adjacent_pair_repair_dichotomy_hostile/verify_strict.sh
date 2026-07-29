#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
campaign=$(CDPATH= cd -- "$here/../.." && pwd)
candidate="$campaign/math/working/adjacent_pair_repair_dichotomy"
actual=$(mktemp "${TMPDIR:-/tmp}/adjacent-pair-hostile.XXXXXX")
trap 'rm -f "$actual"' EXIT HUP INT TERM

test "$(git -C "$campaign/.." rev-parse 9c07f284af010e7ba9508e7039138ffff57c4de1)" = \
  "9c07f284af010e7ba9508e7039138ffff57c4de1"

sh "$candidate/verify_strict.sh" >/dev/null
python3 -I -B -W error "$here/verify_independent.py" > "$actual"
cmp "$here/expected_independent.json" "$actual"

python3 -I -B -W error - "$here" "$candidate" <<'PY'
import hashlib
import json
import pathlib
import sys

review = pathlib.Path(sys.argv[1])
candidate = pathlib.Path(sys.argv[2])
manifest = json.loads((review / "MANIFEST.json").read_text(encoding="utf-8"))

assert manifest["verdict"] == "UNCONDITIONAL_PASS"
assert manifest["candidate_commit"] == (
    "9c07f284af010e7ba9508e7039138ffff57c4de1"
)

for name, expected in manifest["candidate_hashes"].items():
    actual = hashlib.sha256((candidate / name).read_bytes()).hexdigest()
    assert actual == expected, ("candidate", name, expected, actual)

for name, expected in manifest["review_hashes"].items():
    actual = hashlib.sha256((review / name).read_bytes()).hexdigest()
    assert actual == expected, ("review", name, expected, actual)

candidate_manifest = json.loads(
    (candidate / "CANDIDATE_MANIFEST.json").read_text(encoding="utf-8")
)
assert candidate_manifest["status"] == "CANDIDATE_AWAITING_HOSTILE_REVIEW"
candidate_log = (candidate / "RESEARCH_LOG.md").read_text(encoding="utf-8")
assert "proof logs or coverage theorem" in candidate_log
assert "reported UNSAT through order 26" in candidate_log
assert "support no finite or all-order claim" in candidate_log
PY

grep -Fq '**UNCONDITIONAL PASS**' "$here/REVIEW.md"
grep -Fq 'The “or” is inclusive' "$here/REVIEW.md"
grep -Fq 'No attack is made at an occupied vertex' "$here/REVIEW.md"
grep -Fq 'does not promote it' "$here/REVIEW.md"
grep -Fq 'does not eliminate QQ1' "$here/REVIEW.md"

actual_sha=$(shasum -a 256 "$actual" | awk '{print $1}')
expected_sha=$(shasum -a 256 "$here/expected_independent.json" | awk '{print $1}')
test "$actual_sha" = "$expected_sha"
echo "PASS adjacent-pair repair hostile review $actual_sha"
