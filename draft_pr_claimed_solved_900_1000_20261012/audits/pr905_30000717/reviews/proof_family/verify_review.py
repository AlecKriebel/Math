#!/usr/bin/env python3
"""Replay this family's controls and portable fixed-input guards.

Temporary test material is created only inside this review directory and is
removed on exit. This program never writes the supplied original snapshot.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PREFIX = "unsolved_math_prioritization/attempts/30000717/"
EXPECTED_SNAPSHOT_SHA256 = "66f676321be328c27103531c1ffe4ca5d3bbe4a6c0c3098ce46c70a871b52b48"
FIXED_ANCHORS = {
    "author/PROOF.md": "a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1",
    "author/MANIFEST.json": "0256537fe98d411ca8911c22b341785d029e1f4b51f3a20207e056789bc8e380",
    "PUBLIC_MANIFEST.json": "1492167c7a7cfeb168976aa4d91b32c0be56c3b58de4090c417785a9d324a765",
}
snapshot_bytes = (ROOT / "ORIGINAL_SNAPSHOT.json").read_bytes()
if hashlib.sha256(snapshot_bytes).hexdigest() != EXPECTED_SNAPSHOT_SHA256:
    raise RuntimeError("Fixed original snapshot record hash differs")
snapshot = json.loads(snapshot_bytes)
if not all(name.startswith(PREFIX) for name in snapshot["files"]):
    raise RuntimeError("Snapshot contains a path outside the fixed candidate packet")
expected_inputs = {name[len(PREFIX):]: digest for name,digest in snapshot["files"].items()}
archive_packet = ROOT / "original_packet"
original_root = archive_packet if archive_packet.exists() else ROOT / "original" / PREFIX.rstrip("/")
if not original_root.is_dir():
    raise RuntimeError("Original packet directory is missing")
observed = {str(p.relative_to(original_root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in original_root.rglob("*") if p.is_file()}
if observed != expected_inputs:
    raise RuntimeError("Original snapshot file set or bytes changed")
for name,digest in FIXED_ANCHORS.items():
    if observed.get(name) != digest:
        raise RuntimeError("Fixed original proof/manifest anchor differs: " + name)

expected = (HERE / "RESULTS.json").read_bytes()
for option in ([], ["-O"]):
    subprocess.run([sys.executable, *option, str(HERE / "check_exact.py")],
                   check=True, capture_output=True, text=True)
    if (HERE / "RESULTS.json").read_bytes() != expected:
        raise RuntimeError("Independent controls are not byte reproducible")

with tempfile.TemporaryDirectory(prefix="portable_controls_", dir=HERE) as tmp:
    archive_root = Path(tmp)
    review = archive_root / "reviews" / "proof_family"
    review.mkdir(parents=True)
    checker = review / "check_exact.py"
    shutil.copyfile(HERE / "check_exact.py", checker)
    proof = archive_root / "original_packet" / "author" / "PROOF.md"
    shutil.copytree(original_root, archive_root / "original_packet")
    shutil.copyfile(ROOT / "ORIGINAL_SNAPSHOT.json", archive_root / "ORIGINAL_SNAPSHOT.json")
    subprocess.run([sys.executable, str(checker)], check=True, capture_output=True, text=True)
    if (review / "RESULTS.json").read_bytes() != expected:
        raise RuntimeError("Portable layout changed exact results")
    proof.write_bytes(proof.read_bytes() + b"\n")
    rejection = subprocess.run([sys.executable, str(checker)], capture_output=True, text=True)
    if rejection.returncode == 0 or "fixed candidate proof hash matches" not in rejection.stderr:
        raise RuntimeError("Portable guard did not reject altered proof")
    proof.unlink()
    rejection = subprocess.run([sys.executable, str(checker)], capture_output=True, text=True)
    if rejection.returncode == 0 or "fixed candidate proof file exists" not in rejection.stderr:
        raise RuntimeError("Portable guard did not reject missing proof")

result = {
    "utc": datetime.now(timezone.utc).isoformat(),
    "original_snapshot_exact_file_set_and_hashes_unchanged": True,
    "original_file_count": len(observed),
    "original_input_paths_normalized_by_stripping_fixed_prefix": True,
    "fixed_snapshot_record_and_proof_manifest_anchors_checked": True,
    "normal_replay_byte_identical": True,
    "optimized_python_replay_byte_identical": True,
    "standalone_original_packet_layout_byte_identical": True,
    "standalone_test_copied_all_original_files": len(observed),
    "altered_proof_hash_rejected": True,
    "missing_proof_rejected": True,
    "temporary_tests_confined_to_review_directory": True,
    "results_sha256": hashlib.sha256(expected).hexdigest(),
}
(HERE / "REPRODUCIBILITY.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
