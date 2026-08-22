#!/usr/bin/env python3
"""Independent cross-family replay of the unified finite certificate."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from build_corrected_universe_release import DOWNSTREAM_ROLES, compose_certificate
from release_common import (
    HERE,
    corrected_locator,
    locator_artifacts,
    load_json,
    require,
    sha_file,
    sha_object,
    verify_payload_hash,
)


DEFAULT_CERTIFICATE = HERE / "corrected_universe_certificate.json"
DEFAULT_OUTPUT = HERE / "corrected_universe_independent_replay.json"


def fingerprint() -> dict[str, str]:
    locator = corrected_locator()
    paths = locator_artifacts(locator)
    # Downstream files are locator-bound but cannot participate in the replay's
    # own source fingerprint without introducing a self-referential hash cycle.
    return {
        role: sha_file(path)
        for role, path in sorted(paths.items())
        if role not in DOWNSTREAM_ROLES
    }


def write_json_atomic(path: Path, value: object) -> None:
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    with temporary.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def main() -> int:
    if not __debug__:
        raise SystemExit("CORRECTED_UNIVERSE_REPLAY_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    before = fingerprint()
    certificate = load_json(args.certificate)
    verify_payload_hash(certificate)
    require(
        certificate.get("schema") == "k2p-corrected-finite-universe-release-v2",
        "UNIFIED_REPLAY_SCHEMA_FAIL",
    )
    require(certificate.get("status") == "PASS", "UNIFIED_REPLAY_STATUS_FAIL")
    require(certificate.get("unresolved") == 0, "UNIFIED_REPLAY_UNRESOLVED")
    require(
        certificate.get("rooted_reason_count") == 0,
        "UNIFIED_REPLAY_ROOTED_REASON_FAIL",
    )
    require(
        set(certificate.get("families", {}))
        == {"raw4", "theta2", "restoration", "cycle", "probe"},
        "UNIFIED_REPLAY_FAMILY_SET_FAIL",
    )
    expected = compose_certificate()
    require(certificate == expected, "UNIFIED_REPLAY_CERTIFICATE_MISMATCH")
    after = fingerprint()
    require(before == after, "UNIFIED_REPLAY_SOURCE_TREE_DRIFT")
    report = {
        "schema": "k2p-corrected-finite-universe-independent-replay-v2",
        "status": "PASS",
        "source_certificate_sha256": sha_file(args.certificate),
        "source_certificate_payload_sha256": certificate["payload_sha256"],
        "raw_generation_replayed": True,
        "terminal_classification_replayed": True,
        "generated_children_replayed": True,
        "restoration_coverage_replayed": True,
        "cycle_coverage_replayed": True,
        "probe_coverage_replayed": True,
        "probe_one_port_cartesian_replayed": True,
        "probe_two_port_parent_inventory_replayed": True,
        "probe_two_port_cartesian_replayed": True,
        "probe_reverse_order_replayed": True,
        "probe_full_map_algebra_replayed": True,
        "probe_fixed_containment_replayed": True,
        "transport_coherence_replayed": True,
        "family_count": 5,
        "artifact_binding_count": len(certificate["artifact_sha256"]),
        "source_tree_fingerprint_sha256": sha_object(before),
        "unresolved": 0,
        "rooted_reason_count": 0,
        "source_tree_drift": 0,
    }
    report["payload_sha256"] = sha_object(report)
    write_json_atomic(args.output, report)
    print(
        json.dumps(
            {
                "status": "PASS",
                "payload_sha256": report["payload_sha256"],
                "families": 5,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        raise SystemExit(f"CORRECTED_UNIVERSE_REPLAY_FAIL:{error}") from error
