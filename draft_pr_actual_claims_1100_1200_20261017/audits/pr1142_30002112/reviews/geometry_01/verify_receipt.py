#!/usr/bin/env python3
"""Read-only verification of every pinned artifact/input in the receipt."""

import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    own = Path(__file__).resolve().parent
    path = own / "READ_RECEIPT.json"
    data = path.read_bytes()
    receipt = json.loads(data)
    pins = (receipt["nonself_semantic_reads"] + receipt["derived_primary_semantic_reads"]
            + receipt["own_artifact_pins"])
    seen = set()
    for record in pins:
        artifact = Path(record["path"])
        require(artifact != path, "circular receipt self-pin")
        current = artifact.read_bytes()
        require(len(current) == record["bytes"], f"byte count mismatch: {artifact}")
        require(hashlib.sha256(current).hexdigest() == record["sha256"], f"hash mismatch: {artifact}")
        seen.add(str(artifact))
    recorded_own = {r["path"] for r in receipt["own_artifact_pins"]}
    actual_own = {str(p) for p in own.rglob("*") if p.is_file() and p != path}
    require(recorded_own == actual_own, "missing or extra own artifact relative to receipt")
    require(not receipt["exposure"]["old_audit_status_contents_read"], "old audit exposure declared")
    require(not receipt["exposure"]["root_or_concurrent_report_contents_read"], "concurrent/root report exposure declared")
    print(json.dumps({"result": "PASS", "unique_pinned_files": len(seen),
                      "own_artifacts_excluding_receipt": len(recorded_own),
                      "receipt_sha256": hashlib.sha256(data).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
