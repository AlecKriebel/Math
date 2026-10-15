"""Verify frozen priority-audit inputs and source identities without git mutation."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parents[1]
REPOSITORY = AUDIT.parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


initial = json.loads((ROOT / "INPUT_PINS_INITIAL.json").read_text())
submitted = json.loads((ROOT / "frozen/SUBMITTED_PINS.json").read_text())
assert submitted["head_oid"] == initial["head_oid"]
frozen = []
for row in initial["inputs"]:
    path = ROOT / row["own_snapshot"]
    assert path.stat().st_size == row["bytes"]
    assert digest(path) == row["sha256"]
    frozen.append({"path": row["own_snapshot"], "sha256": row["sha256"]})

originals = []
for row in submitted["files"]:
    path = ROOT / "frozen" / row["snapshot_path"]
    data = subprocess.run(
        ["git", "show", submitted["head_oid"] + ":" + row["repository_path"]],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
    ).stdout
    assert data == path.read_bytes()
    assert digest(AUDIT / row["snapshot_path"]) == row["sha256"]
    originals.append({"path": row["repository_path"], "exact_git_object": True})

checkpoint = json.loads((ROOT / "PRE_OLD_AUDIT_CHECKPOINT.json").read_text())
assert digest(ROOT / checkpoint["path"]) == checkpoint["sha256"]
assert checkpoint["old_source_audit_read"] is False
assert checkpoint["old_provenance_read"] is False
assert checkpoint["old_source_provenance_read"] is False

sources = []
for row in json.loads((ROOT / "SOURCE_RETRIEVAL_FRESH.json").read_text()):
    if "raw_path" not in row:
        continue
    path = ROOT / row["raw_path"]
    assert path.stat().st_size == row["bytes"]
    assert digest(path) == row["sha256"]
    if "text_sha256" in row:
        assert digest(path.with_suffix(".txt")) == row["text_sha256"]
    sources.append({"id": row["id"], "identity_verified": True})

raw_paths = [str(p) for p in (ROOT / "sources/raw").iterdir() if p.is_file()]
ignored = subprocess.run(
    ["git", "check-ignore", "--stdin"],
    input="\n".join(raw_paths) + "\n",
    text=True,
    cwd=REPOSITORY,
    check=True,
    capture_output=True,
).stdout.splitlines()
assert set(ignored) == set(raw_paths)
assert not list(ROOT.rglob("*.pyc"))

verdict = json.loads((ROOT / "VERDICT.json").read_text())
assert verdict["originality_certified"] is False
assert verdict["current_worldwide_open_status_certified"] is False
assert verdict["human_peer_review"] is False
assert verdict["formal_certification"] is False
assert verdict["internal_mathematical_gap"] is None

report = (ROOT / "REPORT.md").read_text()
assert "DDSSS" in report and "weighted" in report and "unknown" in report
assert "priority" in report and "all singleton" in report

result = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "PASS",
    "submitted_head": submitted["head_oid"],
    "all9_exact_git_objects_and_current_submitted_copies": originals,
    "all13_frozen_inputs_unchanged": frozen,
    "pre_old_audit_comparison_hash_verified": True,
    "source_retrieval_identities_verified": sources,
    "all_raw_sources_ignored": len(raw_paths),
    "no_bytecode": True,
    "not_an_originality_or_peer_review_certificate": True,
}
(ROOT / "VALIDATION_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "originals": len(originals), "inputs": len(frozen), "source_retrievals": len(sources), "raw_ignored": len(raw_paths)}))
