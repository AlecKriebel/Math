#!/usr/bin/env python3
"""Seal this review's artifacts after checking the immutable input snapshot."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SNAPSHOT = ROOT / "ORIGINAL_SNAPSHOT.json"
PREFIX = "unsolved_math_prioritization/attempts/30000717/"
EXPECTED_SNAPSHOT_SHA256 = "66f676321be328c27103531c1ffe4ca5d3bbe4a6c0c3098ce46c70a871b52b48"
FIXED_ANCHORS = {
    "author/PROOF.md": "a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1",
    "author/MANIFEST.json": "0256537fe98d411ca8911c22b341785d029e1f4b51f3a20207e056789bc8e380",
    "PUBLIC_MANIFEST.json": "1492167c7a7cfeb168976aa4d91b32c0be56c3b58de4090c417785a9d324a765",
}
snapshot_bytes = SNAPSHOT.read_bytes()
if hashlib.sha256(snapshot_bytes).hexdigest() != EXPECTED_SNAPSHOT_SHA256:
    raise RuntimeError("Cannot seal: fixed original snapshot record hash differs")
snapshot = json.loads(snapshot_bytes)
if not all(name.startswith(PREFIX) for name in snapshot["files"]):
    raise RuntimeError("Cannot seal: snapshot path is outside the fixed candidate packet")
expected_inputs = {name[len(PREFIX):]: digest for name,digest in snapshot["files"].items()}
archive_packet = ROOT / "original_packet"
original = archive_packet if archive_packet.exists() else ROOT / "original" / PREFIX.rstrip("/")
if not original.is_dir():
    raise RuntimeError("Cannot seal: original packet directory is missing")
observed = {str(p.relative_to(original)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in original.rglob("*") if p.is_file()}
if observed != expected_inputs:
    raise RuntimeError("Cannot seal: original snapshot differs")
for name,digest in FIXED_ANCHORS.items():
    if observed.get(name) != digest:
        raise RuntimeError("Cannot seal: fixed original proof/manifest anchor differs: " + name)
artifacts = {}
for p in sorted(HERE.iterdir()):
    if p.is_file() and p.name != "MANIFEST.json":
        raw = p.read_bytes()
        artifacts[p.name] = {"bytes":len(raw), "sha256":hashlib.sha256(raw).hexdigest()}
manifest = {
    "utc": datetime.now(timezone.utc).isoformat(),
    "review_family": "proof_family",
    "problem_id": "30000717",
    "pr": 905,
    "verdict": "PASS for frozen v2 mathematical claims",
    "original_snapshot_record_sha256": hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest(),
    "original_snapshot_file_count":len(observed),
    "original_exact_file_set_and_hashes_unchanged":True,
    "reviewed_candidate_proof_sha256":"a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1",
    "input_files_sha256":observed,
    "input_files_relative_to":"original_packet or original/unsolved_math_prioritization/attempts/30000717",
    "input_snapshot_prefix_stripped":PREFIX,
    "fixed_original_proof_manifest_anchors":FIXED_ANCHORS,
    "artifacts":artifacts,
    "manifest_self_hash_excluded":True,
    "verification":"Recompute artifact hashes; compare original input files to the independent ORIGINAL_SNAPSHOT.json record. No hash is an external trust anchor by itself.",
}
(HERE / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"original_files":len(observed),"artifacts":len(artifacts),"manifest":"MANIFEST.json"},indent=2))
