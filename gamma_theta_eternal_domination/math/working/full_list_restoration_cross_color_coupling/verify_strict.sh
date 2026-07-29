#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
actual=$(python3 "$here/verify_control.py")
expected=$(tr -d '\n' < "$here/expected_result.json")
test "$actual" = "$expected"

grep -Fq '### Theorem 2.1 (reciprocal completion bow tie) — PROVED CANDIDATE' "$here/NOTE.md"
grep -Fq '### Lemma 3.1 (restoration-witness ladder) — PROVED CANDIDATE' "$here/NOTE.md"
grep -Fq '### Theorem 3.3 (no immediate rank-one recurrence) — PROVED CANDIDATE' "$here/NOTE.md"
grep -Fq 'The collision' "$here/NOTE.md"
grep -Fq 'p=u' "$here/NOTE.md"

python3 - "$here" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

here = Path(sys.argv[1])
manifest = json.loads((here / "MANIFEST.json").read_text())
for relative, expected in manifest["files"].items():
    actual = hashlib.sha256((here / relative).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"hash mismatch {relative}: {actual}")
PY

printf '%s\n' "PASS full-list restoration cross-color strict replay"
