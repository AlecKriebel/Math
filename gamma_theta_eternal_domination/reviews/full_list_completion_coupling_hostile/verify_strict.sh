#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
campaign=$(CDPATH= cd -- "$here/../.." && pwd)
candidate="$campaign/math/working/full_list_completion_coupling"
actual=$(mktemp "${TMPDIR:-/tmp}/supported-pair-fan-hostile.XXXXXX")
trap 'rm -f "$actual"' EXIT HUP INT TERM

test "$(git -C "$campaign/.." rev-parse f7eb54c7099d71d25e3804977101fa68586135c1)" = \
  "f7eb54c7099d71d25e3804977101fa68586135c1"

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
campaign = review.parent.parent
manifest = json.loads((review / "MANIFEST.json").read_text(encoding="utf-8"))

assert manifest["verdict"] == "UNCONDITIONAL_PASS"
assert manifest["candidate_commit"] == (
    "f7eb54c7099d71d25e3804977101fa68586135c1"
)

for name, expected in manifest["candidate_hashes"].items():
    actual = hashlib.sha256((candidate / name).read_bytes()).hexdigest()
    assert actual == expected, ("candidate", name, expected, actual)

for name, expected in manifest["dependency_hashes"].items():
    actual = hashlib.sha256((campaign / name).read_bytes()).hexdigest()
    assert actual == expected, ("dependency", name, expected, actual)

for name, expected in manifest["review_hashes"].items():
    actual = hashlib.sha256((review / name).read_bytes()).hexdigest()
    assert actual == expected, ("review", name, expected, actual)

candidate_manifest = json.loads(
    (candidate / "MANIFEST.json").read_text(encoding="utf-8")
)
assert candidate_manifest["status"] == "CANDIDATE_AWAITING_HOSTILE_REVIEW"
assert candidate_manifest["not_claimed"][-1] == "the gamma-theta conjecture"
PY

grep -Fq '**UNCONDITIONAL PASS**' "$here/REVIEW.md"
grep -Fq 'genuinely stronger than accepted C-172' "$here/REVIEW.md"
grep -Fq 'No proof step:' "$here/REVIEW.md"
grep -Fq 'No full-target completion instance' "$here/REVIEW.md"
grep -Fq 'safe color, complete parameter three' "$here/REVIEW.md"

actual_sha=$(shasum -a 256 "$actual" | awk '{print $1}')
expected_sha=$(shasum -a 256 "$here/expected_independent.json" | awk '{print $1}')
test "$actual_sha" = "$expected_sha"
echo "PASS supported-pair completion-fan hostile review $actual_sha"
