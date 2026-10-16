#!/usr/bin/env python3
"""Read-only exact-head audit and isolated receipt replay for PR 27."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[3]
PACKET = OWN.parent
SNAP = PACKET / "source_snapshot"
HEAD = "84d7f6103b087e431d7afb751501380ebd7ffd42"
PREFIX = "unsolved_math_prioritization/attempts/30003713/"

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)

def digest(data):
    return hashlib.sha256(data).hexdigest()

manifest = json.loads((PACKET / "snapshot_manifest.json").read_text())
pr = json.loads((PACKET / "pr_input.json").read_text())
rows = []
for expected in manifest["files"]:
    name = expected["path"]
    data = (SNAP / name).read_bytes()
    blob = git("show", HEAD + ":" + PREFIX + name)
    oid = git("rev-parse", HEAD + ":" + PREFIX + name).decode().strip()
    checks = {
        "snapshot_equals_git_blob": data == blob,
        "snapshot_sha256_matches": digest(data) == expected["sha256"],
        "bytes_match": len(data) == expected["bytes"],
        "git_blob_oid_matches": oid == expected["git_blob_sha1"],
    }
    assert all(checks.values()), (name, checks)
    rows.append({"path": name, "bytes": len(data), "sha256": digest(data),
                 "git_blob_sha1": oid, "checks": checks})
base = manifest["actual_merge_base"]
changed = git("diff", "--name-only", base, HEAD).decode().splitlines()
assert changed == manifest["changed_paths"]
assert sorted(changed) == sorted(item["path"] for item in pr["files"])
assert len(rows) == 13 and len(changed) == 14
queue = git("show", HEAD + ":unsolved_math_prioritization/QUEUE.md")
queue_lines = [line for line in queue.decode().splitlines() if "30003713" in line]
history = git("log", "--format=%H %aI %s", base + ".." + HEAD).decode().splitlines()

replay = OWN / "tmp" / "replay"
replay.mkdir(parents=True, exist_ok=True)
receipt_rows = []
for script_name, receipt_name in [
    ("verify.py", "verification.json"),
    ("review/independent_checks.py", "review/independent_results.json"),
]:
    target = replay / script_name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SNAP / script_name, target)
    completed = subprocess.run([sys.executable, str(target)], cwd=replay,
                               text=True, capture_output=True, timeout=300)
    assert completed.returncode == 0, completed.stderr
    output = replay / receipt_name
    result = output.read_bytes()
    original = (SNAP / receipt_name).read_bytes()
    copied_receipt_name = "replayed_" + Path(receipt_name).name
    (OWN / copied_receipt_name).write_bytes(result)
    receipt_rows.append({
        "script": script_name,
        "script_sha256": digest(target.read_bytes()),
        "receipt": receipt_name,
        "reproduced_byte_for_byte": result == original,
        "receipt_sha256": digest(result),
        "exit_code": completed.returncode,
        "current_runtime": sys.version.split()[0],
        "current_interpreter": sys.executable,
        "historical_model_attested": False,
    })
    assert result == original

source_rows = []
for expected in json.loads((SNAP / "source_checksums.json").read_text()):
    path = OWN / "tmp" / expected["file"]
    if path.exists():
        data = path.read_bytes()
        source_rows.append({"file": path.name, "bytes": len(data),
                            "sha256": digest(data),
                            "recorded_bytes_match": len(data) == expected["bytes"],
                            "recorded_sha256_match": digest(data) == expected["sha256"]})

out = {
    "audit_utc": datetime.now(timezone.utc).isoformat(),
    "pr": 27, "head": HEAD, "base": base,
    "branch_read_only_check": git("branch", "--show-current").decode().strip(),
    "snapshot_manifest_sha256": digest((PACKET / "snapshot_manifest.json").read_bytes()),
    "pr_input_sha256": digest((PACKET / "pr_input.json").read_bytes()),
    "all_13_attempt_blobs_verified": True, "attempt_blob_checks": rows,
    "all_14_changed_paths_verified": True, "changed_paths": changed,
    "queue_head_sha256": digest(queue), "queue_target_lines": queue_lines,
    "head_commit_history": history,
    "receipt_replays": receipt_rows, "primary_pdf_checksum_rechecks": source_rows,
    "scope": "Current reproduction and Git-byte provenance. Historical model/reasoning fields remain self-reported.",
}
(OWN / "PACKET_PROVENANCE_AND_REPLAY.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"blob_checks": len(rows), "changed_paths": len(changed),
                  "receipt_replays": receipt_rows, "sources": source_rows}, indent=2))
