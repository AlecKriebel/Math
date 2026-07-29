#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
candidate="$here/../../math/working/full_list_rank_one_anchor_exit"
c175_review="$here/../full_list_rank_rebound_iteration_hostile"

"$candidate/verify_strict.sh"
"$c175_review/verify_strict.sh"

actual=$(python3 "$here/verify_clean.py")
expected=$(tr -d '\n' < "$here/expected_clean.json")
test "$actual" = "$expected"

grep -Fq '## Verdict: unconditional PASS' "$here/REVIEW.md"
grep -Fq '### Lemma 2.1 (escape barrier) — PROVED CANDIDATE' "$candidate/NOTE.md"
grep -Fq '### Theorem 3.1 (rank-one fan exit is anchor restoration) — PROVED CANDIDATE' "$candidate/NOTE.md"

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

printf '%s\n' "PASS full-list rank-one anchor-exit hostile replay"
