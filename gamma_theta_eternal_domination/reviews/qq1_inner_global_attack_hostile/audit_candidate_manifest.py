#!/usr/bin/env python3
"""Audit the candidate manifest and its strict replay entry point."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parents[1] / "math" / "working" / "qq1_inner_global_attack"
MANIFEST = CANDIDATE / "CANDIDATE_MANIFEST.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data["schema"] != "QQ1-inner-global-attack-candidate-v1":
        raise AssertionError("unexpected candidate schema")
    expected_classification = {
        "cross_layer_bridge": "PROVED_CANDIDATE",
        "fixed_controls": "CERTIFIED_FINITE_CANDIDATE",
        "sat_and_cegar_traces": "OBSERVED_DISCOVERY_ONLY",
    }
    if data["classification"] != expected_classification:
        raise AssertionError("candidate classifications changed")

    actual_hashes = {}
    for relative, expected in sorted(data["files_sha256"].items()):
        path = CANDIDATE / relative
        if not path.is_file():
            raise AssertionError(f"missing candidate file: {relative}")
        actual = sha256(path)
        if actual != expected:
            raise AssertionError(
                f"candidate hash mismatch for {relative}: {actual} != {expected}"
            )
        actual_hashes[relative] = actual

    graph6_hashes = {}
    for label, control in sorted(data["controls"].items()):
        actual = hashlib.sha256(control["graph6"].encode("ascii")).hexdigest()
        if actual != control["graph6_sha256"]:
            raise AssertionError(f"graph6 string hash mismatch: {label}")
        graph6_hashes[label] = actual

    strict_relative = data["strict_reproduction"].split(maxsplit=1)[1]
    expected_strict = (
        "math/working/qq1_inner_global_attack/verify_strict.sh"
    )
    if strict_relative != expected_strict:
        raise AssertionError("candidate strict replay path changed")
    strict_path = CANDIDATE.parents[2] / strict_relative
    if not strict_path.is_file():
        raise AssertionError("candidate strict replay script is absent")

    result = {
        "schema": "qq1-inner-global-candidate-manifest-audit-v1",
        "status": "PASS",
        "candidate_manifest_sha256": sha256(MANIFEST),
        "file_hashes": actual_hashes,
        "graph6_hashes": graph6_hashes,
        "strict_replay_path": strict_relative,
        "classification": data["classification"],
        "scope_exclusion_count": len(data["scope_exclusions"]),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
