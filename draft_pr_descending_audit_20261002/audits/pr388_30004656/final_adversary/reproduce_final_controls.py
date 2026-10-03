#!/usr/bin/env python3
"""Read-only final gate, replaying supplied controls in private copies.

All generated files remain below final_adversary. Historical receipts are read,
never overwritten. Finite controls supplement the final analytic review.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
REPO = BASE.parents[2]
HEAD = "96a7e52e738546107c163834ef104419cd8be4e0"
PRIVATE = OUT / "private_replays"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def json_at(path):
    return json.loads(path.read_text())

def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)

started = datetime.now(timezone.utc).isoformat()
frozen = json_at(OUT / "REVIEWED_INPUT_HASHES.json")
assert frozen["reviewed_head"] == HEAD
for row in frozen["files"]:
    data = (BASE / row["path"]).read_bytes()
    assert len(data) == row["bytes"] and sha(data) == row["sha256"], row["path"]

snapshot = BASE / "snapshot"
head_records = []
for row in json_at(BASE / "snapshot_manifest.json"):
    data = (snapshot / row["path"]).read_bytes()
    assert len(data) == row["size"] and sha(data) == row["sha256"]
    current = git("show", HEAD + ":" + row["path"])
    assert current == data, row["path"]
    head_records.append(row["path"])
metadata = json_at(BASE / "pr_metadata.json")
paths = git("diff", "--name-only", metadata["baseRefOid"], HEAD).decode().splitlines()
assert set(paths) == set(head_records) == {r["path"] for r in metadata["files"]}
qpath = "unsolved_math_prioritization/QUEUE.md"
old = git("show", metadata["baseRefOid"] + ":" + qpath).decode().splitlines()
new = git("show", HEAD + ":" + qpath).decode().splitlines()
assert len(old) == len(new)
changes = [(a, b) for a, b in zip(old, new) if a != b]
assert len(changes) == 1 and "30004656 / OWR-4990384-001" in changes[0][0]
oldcells, newcells = [s.split("|") for s in changes[0]]
assert [(i, a.strip(), b.strip()) for i, (a, b) in enumerate(zip(oldcells, newcells)) if a != b] == [(8, "queued", "unsolved"), (9, "0/5", "5/5")]

candidate = snapshot / "problems" / "30004656_robustness"
# Independently bind each historical remote receipt's stated local content. This
# checks byte/ID consistency, not a new assertion of historical network access.
receipt_bindings = 0
for receipt in sorted(candidate.glob("TURN_*_REMOTE_RECEIPT.json")):
    for row in json_at(receipt)["files"]:
        data = (candidate / row["path"]).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert len(data) == row["size"] and blob == row["sha"], (receipt.name, row["path"])
        receipt_bindings += 1
binding = json_at(candidate / "review" / "REMOTE_BINDING.json")
for key in ["original_files", "all_corrected_tree_files"]:
    for row in binding[key]:
        data = (candidate / row["path"]).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert len(data) == row["bytes"] and blob == row["git_blob_sha"]

PRIVATE.mkdir(exist_ok=True)
private_candidate = PRIVATE / "snapshot" / "problems" / "30004656_robustness"
shutil.copytree(candidate, private_candidate, dirs_exist_ok=True)
for family, script in [("geometry_review", "independent_geometry_controls.py"), ("architecture_review", "independent_controls.py"), ("source_review", "check_source_bindings.py")]:
    target = PRIVATE / family
    target.mkdir(exist_ok=True)
    shutil.copyfile(BASE / family / script, target / script)
shutil.copytree(BASE / "source_review" / "raw_sources", PRIVATE / "source_review" / "raw_sources", dirs_exist_ok=True)

jobs = {
    "public": [sys.executable, "-B", str(private_candidate / "review" / "verify_review.py"), "--author", str(private_candidate)],
    "geometry": [sys.executable, "-B", str(PRIVATE / "geometry_review" / "independent_geometry_controls.py")],
    "architecture": [sys.executable, "-B", str(PRIVATE / "architecture_review" / "independent_controls.py")],
    "source": [sys.executable, "-B", str(PRIVATE / "source_review" / "check_source_bindings.py")],
}

def run_job(item):
    name, argv = item
    start = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(argv, cwd=PRIVATE, capture_output=True)
    (PRIVATE / (name + ".stdout")).write_bytes(result.stdout)
    (PRIVATE / (name + ".stderr")).write_bytes(result.stderr)
    assert result.returncode == 0, (name, result.stderr.decode())
    return name, {"argv": argv, "started_at_utc": start, "finished_at_utc": datetime.now(timezone.utc).isoformat(), "exit_code": result.returncode, "stdout_sha256": sha(result.stdout), "stderr_sha256": sha(result.stderr)}

with ThreadPoolExecutor(max_workers=4) as pool:
    receipts = dict(pool.map(run_job, jobs.items()))
public = json_at(PRIVATE / "public.stdout")
assert public == json_at(BASE / "root_replay.stdout")
assert public["author_assertions"] == 329914 and public["independent_assertions"] == 91084
for family, result_file, timestamp in [("geometry_review", "INDEPENDENT_GEOMETRY_CONTROLS.json", "created_utc"), ("architecture_review", "CONTROLS_RECEIPT.json", "completed_at_utc")]:
    original = json_at(BASE / family / result_file)
    fresh = json_at(PRIVATE / family / result_file)
    original.pop(timestamp)
    fresh.pop(timestamp)
    assert original == fresh, family
    receipts[family.split("_")[0]]["all_stable_fields_equal"] = True
assert json_at(PRIVATE / "source.stdout") == json_at(BASE / "source_review" / "SOURCE_CHECKS.json")
assert json_at(PRIVATE / "source.stdout") == json_at(BASE / "root_replays" / "source" / "stdout.json")
receipts["source"]["entire_json_equal"] = True

# Verify family manifests and preservation of every frozen input after execution.
geom = json_at(BASE / "geometry_review" / "GEOMETRY_REVIEW_MANIFEST.json")
for row in geom["candidate_files"] + geom["review_outputs"]:
    data = Path(row["path"]).read_bytes()
    assert len(data) == row["bytes"] and sha(data) == row["sha256"]
for row in frozen["files"]:
    data = (BASE / row["path"]).read_bytes()
    assert len(data) == row["bytes"] and sha(data) == row["sha256"], row["path"]

report = {"status": "PASS_SCOPED_FINAL_REPRODUCTION", "reviewed_head": HEAD,
          "started_at_utc": started, "finished_at_utc": datetime.now(timezone.utc).isoformat(),
          "script_sha256": sha(Path(__file__).read_bytes()), "frozen_input_files": len(frozen["files"]),
          "exact_head_files": len(head_records), "historical_remote_content_bindings": receipt_bindings,
          "historical_receipts_preserved": True, "queue_changed_cells": [8, 9],
          "public_result": public, "fresh_replays": receipts,
          "source_pdf_byte_bindings_checked": 5, "historical_png_bytes_reproduced": False,
          "new_source_search": False,
          "note": "Public probability proofs are analytic. Finite checks do not certify infinity or novelty; historical search/ref observations are not newly recertified."}
(OUT / "FINAL_REPLAY_RECEIPT.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": report["status"], "exact_head_files": len(head_records), "historical_bindings": receipt_bindings, "jobs": list(receipts), "author_assertions": public["author_assertions"], "independent_assertions": public["independent_assertions"], "architecture_assertions": 168007, "frozen_inputs_preserved": True}, indent=2))
