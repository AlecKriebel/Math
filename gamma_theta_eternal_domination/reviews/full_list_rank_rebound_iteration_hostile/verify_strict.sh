#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
candidate="$here/../../math/working/full_list_rank_rebound_iteration"

"$candidate/verify_strict.sh"
actual=$(python3 "$here/verify_clean.py")
expected=$(tr -d '\n' < "$here/expected_clean.json")
test "$actual" = "$expected"

grep -Fq '## Verdict: unconditional PASS' "$here/REVIEW.md"
grep -Fq '### Lemma 1.1 (tight-shell descent) — PROVED' "$candidate/NOTE.md"
grep -Fq '### Theorem 3.1 (rank-one anchor exit) — PROVED' "$candidate/NOTE.md"
grep -Fq '### Theorem 4.1 (two-fan target crossing) — PROVED' "$candidate/NOTE.md"

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

printf '%s\n' "PASS full-list rank rebound hostile replay"
