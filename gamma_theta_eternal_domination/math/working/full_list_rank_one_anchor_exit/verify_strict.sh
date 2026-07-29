#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

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
PY

grep -Fq 'Theorem 3.1 (rank-one fan exit is anchor restoration) — PROVED CANDIDATE' \
  "$here/NOTE.md"
grep -Fq 'the attack is' "$here/NOTE.md"
grep -Fq '\boxed{z=t}' "$here/NOTE.md"
grep -Fq 'The word “unique” concerns retained responses' "$here/NOTE.md"
grep -Fq 'It does not eliminate the surviving anchor' "$here/NOTE.md"

echo "PASS rank-one completion-fan anchor-exit candidate"
