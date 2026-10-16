#!/usr/bin/env python3
"""Read-only integrity checks; optionally write own pre-seal verification result.

Run `python3 VERIFY_AUDIT.py --write-result` before creating MANIFEST.json.
Run `python3 VERIFY_AUDIT.py` after sealing to verify without any file writes.
This checks packet integrity, not the universal mathematical assertions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT_ROOT = HERE.parents[1]
EXPECTED_HEAD = "704685791ec0053dc0a52590fdef49ed4aae61d9"
EXPECTED_PROOF = "78be2da0b8831461e0268eb230cf47273a629a81a9dc2db997234f9fb5036464"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    snapshot = json.loads((AUDIT_ROOT / "ORIGINAL_SNAPSHOT.json").read_text())
    originals = AUDIT_ROOT / "original"
    assert snapshot["head"] == EXPECTED_HEAD
    assert len(snapshot["files"]) == 27
    actual_paths = {str(p.relative_to(originals)) for p in originals.rglob("*") if p.is_file()}
    assert actual_paths == set(snapshot["files"])
    mismatches = [name for name, expected in snapshot["files"].items()
                  if sha(originals / name) != expected]
    assert not mismatches, mismatches
    proof = originals / "unsolved_math_prioritization/attempts/30002555/public/PROOF.md"
    assert sha(proof) == EXPECTED_PROOF
    result = json.loads((HERE / "RESULT.json").read_text())
    assert result["status"] == "PASS" and not result["required_issues"]
    assert result["original_head"] == EXPECTED_HEAD
    assert result["original_proof_sha256"] == EXPECTED_PROOF
    assert result["author_proof_search_turns_added"] == 0
    manifest_path = HERE / "MANIFEST.json"
    if args.write_result:
        assert not manifest_path.exists(), "Refuse to alter a sealed packet"
        record = {
            "utc": datetime.now(timezone.utc).isoformat(),
            "status": "PASS",
            "original_head_in_snapshot": EXPECTED_HEAD,
            "original_files_checked": 27,
            "original_hash_mismatches": [],
            "original_inventory_exact_match": True,
            "proof_sha256": EXPECTED_PROOF,
            "result_schema_checks": "PASS",
            "manifest_status": "not yet created; final read-only verifier must check it",
            "scope": "Integrity only; mathematical evidence is the written derivation and audit"
        }
        (HERE / "VERIFICATION.json").write_text(json.dumps(record, indent=2) + "\n")
    manifest_checked = False
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        assert manifest["self_excluded"] == "MANIFEST.json"
        allowlist = manifest["public_allowlist"]
        assert len(allowlist) == len(set(allowlist))
        assert set(manifest["files"]) == set(allowlist)
        actual_own = {str(p.relative_to(HERE)) for p in HERE.rglob("*") if p.is_file()}
        assert actual_own == set(allowlist) | {"MANIFEST.json"}
        for name, expected in manifest["files"].items():
            path = HERE / name
            assert path.stat().st_size == expected["bytes"], name
            assert sha(path) == expected["sha256"], name
        manifest_checked = True
    print(json.dumps({"status": "PASS", "original_files_checked": 27,
                      "original_hash_mismatches": 0,
                      "proof_sha256": EXPECTED_PROOF,
                      "sealed_manifest_verified": manifest_checked}, indent=2))


if __name__ == "__main__":
    main()
