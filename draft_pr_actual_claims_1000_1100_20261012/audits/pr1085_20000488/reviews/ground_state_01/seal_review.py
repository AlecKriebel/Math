#!/usr/bin/env python3
"""Create or verify a nonrecursive, exact-byte review artifact seal."""
from pathlib import Path
import gzip
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
EXCLUDED = {"OUTPUT_PINS.json", "REVIEW_SEAL.json"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def members():
    return sorted(p for p in HERE.rglob("*") if p.is_file()
                  and p.relative_to(HERE).parts[0] not in {"private_sources", "__pycache__"}
                  and p.name not in EXCLUDED)


def inventory():
    return {str(p.relative_to(HERE)): {"bytes": p.stat().st_size,
                                     "sha256": digest(p.read_bytes())}
            for p in members()}


def verify():
    pinfile = HERE / "OUTPUT_PINS.json"
    pinbytes = pinfile.read_bytes()
    pins = json.loads(pinbytes)
    seal = json.loads((HERE / "REVIEW_SEAL.json").read_text())
    if digest(pinbytes) != seal["output_pins_sha256"]:
        raise RuntimeError("OUTPUT_PINS bytes fail seal")
    actual = inventory()
    if actual != pins["files"]:
        raise RuntimeError("Review artifact member/hash/size mismatch")
    capture = json.loads((HERE / "ACTUAL_GIT_CAPTURE.json").read_text())
    row = capture["status"]
    zipped = (HERE / row["full_stdout_compressed_file"]).read_bytes()
    if digest(zipped) != row["compressed_sha256"]:
        raise RuntimeError("Global Git status compressed hash mismatch")
    original = gzip.decompress(zipped)
    if len(original) != row["uncompressed_bytes"] or digest(original) != row["uncompressed_sha256"]:
        raise RuntimeError("Global Git status full capture mismatch")
    return {"result": "PASS", "sealed_member_count": len(actual),
            "output_pins_sha256": digest(pinbytes),
            "full_global_git_status_losslessly_verified": True,
            "raw_primary_sources_excluded_from_public_review_members": True}


if __name__ == "__main__":
    if sys.argv[1:] == ["--create"]:
        pins = {"schema_version": 1,
                "claim_scope": "Full six-file PR1085 candidate at 5e23f0c801d23976830657d2eef2b32bdc7da05a",
                "excluded": ["OUTPUT_PINS.json", "REVIEW_SEAL.json", "private_sources/", "__pycache__/"],
                "files": inventory()}
        pinbytes = (json.dumps(pins, indent=2, sort_keys=True) + "\n").encode()
        (HERE / "OUTPUT_PINS.json").write_bytes(pinbytes)
        (HERE / "REVIEW_SEAL.json").write_text(json.dumps(
            {"schema_version": 1, "output_pins_sha256": digest(pinbytes),
             "member_count": len(pins["files"]), "result": "SEALED"},
            indent=2) + "\n")
    elif sys.argv[1:]:
        raise SystemExit("Usage: python3 seal_review.py [--create]")
    print(json.dumps(verify(), indent=2))
