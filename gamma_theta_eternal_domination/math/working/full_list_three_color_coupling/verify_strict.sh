#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
campaign=$(CDPATH= cd -- "$here/../../.." && pwd)
actual=$(mktemp "${TMPDIR:-/tmp}/full-list-three-color.XXXXXX")
trap 'rm -f "$actual"' EXIT HUP INT TERM

python3 -I -B -W error "$here/verify_transfer.py" > "$actual"
cmp "$here/expected_result.json" "$actual"

python3 -I -B -W error \
  "$here/search_cyclic_corridor_control.py" --help >/dev/null

python3 -I -B -W error - "$here" <<'PY'
import hashlib
import json
import pathlib
import sys

directory = pathlib.Path(sys.argv[1])
manifest = json.loads(
    (directory / "MANIFEST.json").read_text(encoding="utf-8")
)
for name, expected in manifest["candidate_hashes"].items():
    actual = hashlib.sha256((directory / name).read_bytes()).hexdigest()
    assert actual == expected, (name, expected, actual)
observed = json.loads(
    (directory / "OBSERVED_RESULTS.json").read_text(encoding="utf-8")
)
generator_hash = hashlib.sha256(
    (directory / observed["generator"]).read_bytes()
).hexdigest()
assert observed["classification"] == "OBSERVED"
assert generator_hash == observed["generator_sha256"]
assert [row["order"] for row in observed["runs"]] == list(range(10, 17))
assert all(
    row["status"] == "UNSAT_NO_PROOF_LOG"
    for row in observed["runs"][:-1]
)
assert observed["runs"][-1]["status"] == "TIMEOUT_NO_RESULT"
PY

grep -Fq 'v\in Q(q)\cup Q(w)' "$here/NOTE.md"
grep -Fq 'Open cross-ban rank gate' "$here/NOTE.md"
grep -Fq 'OBSERVED only' "$here/NOTE.md"
grep -Fq 'does not resolve the gamma--theta conjecture' "$here/NOTE.md"

actual_sha=$(shasum -a 256 "$actual" | awk '{print $1}')
expected_sha=$(shasum -a 256 "$here/expected_result.json" | awk '{print $1}')
test "$actual_sha" = "$expected_sha"
echo "PASS full-list three-color coupling strict replay $actual_sha"
