#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
campaign=$(CDPATH= cd -- "$here/../.." && pwd)
candidate="$campaign/math/working/full_list_cross_ban_rank"
actual=$(mktemp "${TMPDIR:-/tmp}/cross-ban-hostile.XXXXXX")
trap 'rm -f "$actual"' EXIT HUP INT TERM

test "$(git -C "$campaign/.." rev-parse 2a49be9355261175f81f9c28f9be13f010ea2709)" = \
  "2a49be9355261175f81f9c28f9be13f010ea2709"

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
    "2a49be9355261175f81f9c28f9be13f010ea2709"
)

for name, expected in manifest["candidate_hashes"].items():
    actual = hashlib.sha256((candidate / name).read_bytes()).hexdigest()
    assert actual == expected, ("candidate", name, expected, actual)

for name, expected in manifest["review_hashes"].items():
    actual = hashlib.sha256((review / name).read_bytes()).hexdigest()
    assert actual == expected, ("review", name, expected, actual)

for relative, expected in manifest["dependency_hashes"].items():
    actual = hashlib.sha256(
        (candidate.parents[2] / relative).read_bytes()
    ).hexdigest()
    assert actual == expected, ("dependency", relative, expected, actual)

observed = json.loads(
    (candidate / "OBSERVED_RESULTS.json").read_text(encoding="utf-8")
)
assert observed["classification"] == "OBSERVED"
assert observed["not_used_in_proof"] is True
PY

grep -Fq '**UNCONDITIONAL PASS**' "$here/REVIEW.md"
grep -Fq 'No missing palette entry or omitted family response' "$here/REVIEW.md"
grep -Fq 'does **not** prove a surviving color-restricted kernel' "$here/REVIEW.md"

actual_sha=$(shasum -a 256 "$actual" | awk '{print $1}')
expected_sha=$(shasum -a 256 "$here/expected_independent.json" | awk '{print $1}')
test "$actual_sha" = "$expected_sha"
echo "PASS full-list cross-ban hostile review $actual_sha"
