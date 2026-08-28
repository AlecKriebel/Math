#!/usr/bin/env python3
"""Check the release's current/historical/revoked authority partition."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(), object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        raise ValueError(f"not an object: {path}")
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()
    lock = load(root / "work/final_theorem_release/RELEASE_LOCK.json")
    registry = load(root / "work/final_theorem_release/HISTORICAL_ARTIFACT_REGISTRY.json")
    manifest = load(root / "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json")
    crosswalk = load(root / "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json")
    frozen = manifest["frozen_evidence"]["files"]

    registry_unsigned = dict(registry)
    registry_payload = registry_unsigned.pop("payload_sha256")
    bad_hashes: list[str] = []
    missing_replacements: list[str] = []
    replacements_not_frozen: list[str] = []
    promotion_authority_true: list[str] = []
    for row in registry["artifacts"]:
        relative = row["path"]
        path = root / relative
        if not path.is_file() or sha(path) != row["sha256"]:
            bad_hashes.append(relative)
        if row.get("promotion_authority") is not False:
            promotion_authority_true.append(relative)
        for replacement in row["authoritative_replacements"]:
            if not (root / replacement).is_file():
                missing_replacements.append(replacement)
            if replacement not in frozen:
                replacements_not_frozen.append(replacement)

    legacy_crosswalk_bindings: list[dict[str, str]] = []
    for claim in crosswalk["claims"]:
        for field in (
            "authoritative_artifacts",
            "producer_artifacts",
            "replay_artifacts",
            "mutation_artifacts",
        ):
            for row in claim[field]:
                layer = (lock["files"].get(row["path"]) or {}).get("layer") or ""
                if any(token in layer.lower() for token in ("historical", "legacy", "revoked")):
                    legacy_crosswalk_bindings.append(
                        {
                            "claim_id": claim["claim_id"],
                            "field": field,
                            "path": row["path"],
                            "layer": layer,
                        }
                    )

    scanner_paths = registry["scanner"]["scope_paths"]
    registry_paths = [row["path"] for row in registry["artifacts"]]
    authority = registry["authoritative_theorem_path"]
    layer_counts = Counter(row["layer"] for row in lock["files"].values())
    result = {
        "registry": {
            "schema": registry.get("schema"),
            "status": registry.get("status"),
            "payload_sha256": registry_payload,
            "recomputed_payload_sha256": canonical_hash(registry_unsigned),
            "artifact_count": len(registry_paths),
            "unique_artifact_paths": len(registry_paths) == len(set(registry_paths)),
            "scanner_scope_exactly_matches_registry": scanner_paths == registry_paths,
            "scanner_classified_count": registry["scanner"]["classified_count"],
            "scanner_unclassified_count": registry["scanner"]["unclassified_count"],
            "bad_artifact_hashes": bad_hashes,
            "promotion_authority_true": promotion_authority_true,
            "missing_replacements": sorted(set(missing_replacements)),
            "replacements_not_frozen": sorted(set(replacements_not_frozen)),
        },
        "current_authority": {
            "path": authority,
            "exists": (root / authority).is_file(),
            "in_frozen_closure": authority in frozen,
            "sha256": sha(root / authority),
        },
        "legacy_or_historical_crosswalk_bindings": legacy_crosswalk_bindings,
        "outer_lock_layer_counts": dict(sorted(layer_counts.items())),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
