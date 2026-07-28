#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
actual=$(mktemp "${TMPDIR:-/tmp}/full-list-cross-ban-rank.XXXXXX")
trap 'rm -f "$actual"' EXIT HUP INT TERM

python3 -I -B -W error "$here/verify_control.py" > "$actual"
cmp "$here/expected_result.json" "$actual"

python3 -I -B -W error \
  "$here/search_single_trapped_transfer.py" --help >/dev/null
python3 -I -B -W error \
  "$here/cegar_trapped_pairs.py" --help >/dev/null
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
assert observed["classification"] == "OBSERVED"
assert observed["not_used_in_proof"] is True
runs = observed["single_trap_search"]["runs"]
assert [row["order"] for row in runs] == list(range(8, 17))
assert all(
    row["status"] == "UNSAT_NO_PROOF_LOG"
    for row in runs[:-1]
)
assert runs[-1]["status"] == "TIMEOUT_NO_RESULT"
assert "five minutes" in observed["single_trap_search"]["termination_gate"]
PY

grep -Fq 'Theorem 2.1 (trapped-witness escape) — PROVED' "$here/NOTE.md"
grep -Fq 'At deletion rank zero' "$here/NOTE.md"
grep -Fq 'y\notin S\cup\{x,q,r,w\}' "$here/NOTE.md"
grep -Fq 'operatorname{rank}_6' "$here/NOTE.md"
grep -Fq 'does not prove that a color-restricted kernel survives' "$here/NOTE.md"
grep -Fq '**OBSERVED**' "$here/NOTE.md"

actual_sha=$(shasum -a 256 "$actual" | awk '{print $1}')
expected_sha=$(shasum -a 256 "$here/expected_result.json" | awk '{print $1}')
test "$actual_sha" = "$expected_sha"
echo "PASS full-list cross-ban rank strict replay $actual_sha"
