#!/usr/bin/env bash
set -euo pipefail

REVIEW_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$REVIEW_DIR/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

cd "$PROJECT_DIR"

"$PYTHON_BIN" reviews/compact_probe_format/cleanroom_compare.py

audit_before="$($PYTHON_BIN -c 'import hashlib,pathlib; p=pathlib.Path("reviews/compact_probe_format/certificates/compact_smoke_cleanroom_audit.json"); print(hashlib.sha256(p.read_bytes()).hexdigest())')"
mutation_before="$($PYTHON_BIN -c 'import hashlib,pathlib; p=pathlib.Path("reviews/compact_probe_format/certificates/compact_smoke_mutations.json"); print(hashlib.sha256(p.read_bytes()).hexdigest())')"
"$PYTHON_BIN" reviews/compact_probe_format/cleanroom_compare.py
audit_after="$($PYTHON_BIN -c 'import hashlib,pathlib; p=pathlib.Path("reviews/compact_probe_format/certificates/compact_smoke_cleanroom_audit.json"); print(hashlib.sha256(p.read_bytes()).hexdigest())')"
mutation_after="$($PYTHON_BIN -c 'import hashlib,pathlib; p=pathlib.Path("reviews/compact_probe_format/certificates/compact_smoke_mutations.json"); print(hashlib.sha256(p.read_bytes()).hexdigest())')"
test "$audit_before" = "$audit_after"
test "$mutation_before" = "$mutation_after"

set +e
"$PYTHON_BIN" reviews/compact_probe_format/audit_merge_manifest.py
merge_rc=$?
set -e
test "$merge_rc" -eq 1

"$PYTHON_BIN" - <<'PY'
import json
from pathlib import Path

root = Path("reviews/compact_probe_format/certificates")
audit = json.loads((root / "compact_smoke_cleanroom_audit.json").read_text())
mutations = json.loads((root / "compact_smoke_mutations.json").read_text())
merge = json.loads((root / "merge_manifest_adversarial_audit.json").read_text())
assert audit["status"] == "VERIFIED"
assert audit["semantic_comparison"]["total_relations"] == 1705
assert mutations["status"] == "VERIFIED"
assert all(row["rejected"] for row in mutations["mutations"])
assert merge["status"] == "FALSE"
assert set(merge["accepted_malformed_cases"]) == {
    "forged_inventory_count",
    "forged_classification_counts",
    "unresolved_but_status_computed",
    "wrong_schema_specification_hash",
    "wrong_inventory_commitment",
}
assert not (Path("reviews/compact_probe_format/history") /
            "FIRST_SEMANTIC_FAILURE.json").exists()
print("compact probe format audit: expected verdict reproduced")
PY
