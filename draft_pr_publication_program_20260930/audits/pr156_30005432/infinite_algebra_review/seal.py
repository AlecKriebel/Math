#!/usr/bin/env python3
"""Create or verify exact byte-hash seals of owned output and original inputs."""
from datetime import datetime, timezone
from hashlib import sha1, sha256
from pathlib import Path
import argparse
import json

root = Path(__file__).resolve().parent
manifest_path = root / "IO_BYTEHASH_MANIFEST.json"
seal_path = root / "SEAL.json"
excluded = {manifest_path.name, seal_path.name}


def record(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def create():
    original_manifest = root.parent / "ORIGINAL_FILE_MANIFEST.json"
    fixture = json.loads(original_manifest.read_text())
    head = "aec31742f3f26c5b1e533404da57539d17dc94a1"
    if fixture["original_head"] != head:
        raise RuntimeError("Original fixture head differs from assigned immutable head")
    expected_names = {"COUNTEREXAMPLE.md", "source_record.json", "verify.py", "SOURCE_RECONCILIATION.md"}
    inputs = []
    for item in fixture["files"]:
        if item["relative_attempt_path"] not in expected_names:
            continue
        path = Path(item["local_path"])
        raw = path.read_bytes()
        actual = record(path)
        git_blob = sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if actual["sha256"] != item["sha256"] or actual["bytes"] != item["bytes"] or git_blob != item["Git_blob"]:
            raise RuntimeError(f"Original input identity mismatch: {path}")
        actual["fixture_Git_blob"] = git_blob
        actual["fixture_identity_verified"] = True
        inputs.append(actual)
    if len(inputs) != len(expected_names):
        raise RuntimeError("Original input set is incomplete")
    inputs.append(record(original_manifest))
    outputs = [record(path) for path in sorted(root.iterdir()) if path.is_file() and path.name not in excluded]
    manifest = {"schema": "exact-input-output-bytehash-v1", "sealed_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"), "original_head": head, "inputs": sorted(inputs, key=lambda item: item["path"]), "outputs": outputs, "excluded_self_referential_files": sorted(excluded), "note": "Only original inputs actually read by this audit are hashed; historical/sibling reviews and private downloaded source bodies were not read. Original input SHA256, byte counts, and Git blob identities are verified against the supplied immutable manifest. All owned non-seal files, including empty stderr receipts, are hashed."}
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    main_names = ("INITIAL_ASSESSMENT.md", "REVIEW.md", "RESULT.json", "RUN_RECEIPT.json", "IO_BYTEHASH_MANIFEST.json")
    seals = {name: record(root / name)["sha256"] for name in main_names}
    seal_path.write_text(json.dumps({"schema": "audit-bytehash-seal-v1", "sealed_at_utc": manifest["sealed_at_utc"], "sha256": seals, "input_count": len(inputs), "output_count": len(outputs)}, indent=2, sort_keys=True) + "\n")
    verify()


def verify():
    manifest, seal = json.loads(manifest_path.read_text()), json.loads(seal_path.read_text())
    for group in ("inputs", "outputs"):
        for item in manifest[group]:
            actual = record(Path(item["path"]))
            if actual["bytes"] != item["bytes"] or actual["sha256"] != item["sha256"]:
                raise RuntimeError(f"Byte seal mismatch: {item['path']}")
    actual_owned = {str(path) for path in root.iterdir() if path.is_file() and path.name not in excluded}
    recorded_owned = {item["path"] for item in manifest["outputs"]}
    if actual_owned != recorded_owned:
        raise RuntimeError("Owned output inventory changed after sealing")
    for name, expected in seal["sha256"].items():
        if record(root / name)["sha256"] != expected:
            raise RuntimeError(f"Main seal mismatch: {name}")
    print(json.dumps({"verdict": "PASS_BYTEHASH_SEAL", "sha256": seal["sha256"], "SEAL.json_sha256": record(seal_path)["sha256"], "input_count": seal["input_count"], "output_count": seal["output_count"]}, indent=2, sort_keys=True))


parser = argparse.ArgumentParser()
parser.add_argument("--verify", action="store_true")
args = parser.parse_args()
if args.verify:
    verify()
else:
    create()
