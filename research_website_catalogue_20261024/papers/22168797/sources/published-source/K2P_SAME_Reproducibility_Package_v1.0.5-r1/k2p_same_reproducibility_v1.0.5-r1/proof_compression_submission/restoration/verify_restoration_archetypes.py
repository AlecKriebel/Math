#!/usr/bin/env python3
"""Fail-closed coverage and deterministic-equivalence checks for restoration compression."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import StrictJSONError, decode_json_document  # noqa: E402

ANALYZER = HERE / "analyze_restoration_archetypes.py"
ARTIFACT = HERE / "RESTORATION_ARCHETYPES.json"
REPORT = HERE / "RESTORATION_ARCHETYPE_VERIFICATION.json"
FOREST = PROJECT / "work/restoration_sign_reclassification/corrected_restoration_forest.json"


class Failure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def object_sha256(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_plain_json(path: Path):
    try:
        return decode_json_document(
            path.read_bytes(), label=path.name, require_object=True
        )
    except (OSError, StrictJSONError) as error:
        raise Failure(f"strict JSON:{path}:{error}") from error


def ordered_hash_root(rows) -> str:
    root = object_sha256([])
    for row in rows:
        root = object_sha256({"previous": root, "row_sha256": object_sha256(row)})
    return root


def build_report() -> dict:
    artifact = load_plain_json(ARTIFACT)
    forest = load_plain_json(FOREST)
    require(artifact["schema"] == "k2p-restoration-descriptive-archetypes-v1", "artifact schema")
    require(artifact["status"] == "PC-PARTIAL", "artifact status")
    unhashed = dict(artifact)
    payload = unhashed.pop("payload_sha256")
    require(object_sha256(unhashed) == payload, "artifact payload replay")

    replay = subprocess.run(
        [sys.executable, str(ANALYZER), "--emit"],
        cwd=PROJECT,
        check=False,
        capture_output=True,
        text=True,
    )
    require(replay.returncode == 0, f"analyzer replay failed:{replay.stderr[-1000:]}")
    require(json.loads(replay.stdout) == artifact, "analyzer/artifact deterministic equivalence")

    optimized = subprocess.run(
        [sys.executable, "-O", str(ANALYZER), "--check", str(ARTIFACT)],
        cwd=PROJECT,
        check=False,
        capture_output=True,
        text=True,
    )
    require(optimized.returncode != 0, "optimized analyzer unexpectedly accepted")
    require("RESTORATION_COMPRESSION_OPTIMIZED_MODE_FORBIDDEN" in optimized.stderr, "optimized rejection marker")

    archetypes = artifact["archetypes"]
    assignments = artifact["coverage"]["canonical_parent_assignment"]
    require(len(archetypes) == artifact["census"]["descriptive_archetypes"] == 297, "archetype count")
    require(len({row["archetype_id"] for row in archetypes}) == 297, "archetype id uniqueness")
    parent_keys = [(row["source_index"], row["canonical_class_id"]) for row in assignments]
    require(len(parent_keys) == len(set(parent_keys)) == 997, "canonical parent exact coverage")
    require(parent_keys == sorted(parent_keys), "canonical parent assignment order")
    expanded = []
    for archetype in archetypes:
        require(archetype["canonical_parent_count"] == len(archetype["canonical_parents"]), "archetype parent count")
        expanded.extend(
            (row["source_index"], row["canonical_class_id"], archetype["archetype_id"])
            for row in archetype["canonical_parents"]
        )
    require(
        sorted(expanded)
        == [(row["source_index"], row["canonical_class_id"], row["archetype_id"]) for row in assignments],
        "archetype membership/assignment equivalence",
    )
    require(object_sha256(assignments) == artifact["coverage"]["canonical_parent_assignment_sha256"], "assignment hash")

    first = forest["first_coverage"]
    second = forest["second_coverage"]
    roots = {row["root_id"] for row in first}
    require(len(roots) == artifact["census"]["member_roots"] == 2540, "member root coverage")
    require(len(first) == artifact["census"]["first_children"] == 36568, "first edge coverage")
    require(len(second) == artifact["census"]["second_children"] == 256, "second edge coverage")
    require(len(first) + len(second) == artifact["census"]["forest_edges"] == 36824, "forest edge coverage")
    require(all(row["root_id"] in roots for row in second), "second parent root coverage")
    require(ordered_hash_root(first) == artifact["coverage"]["ordered_first_row_hash_root"], "first ordered root")
    require(ordered_hash_root(second) == artifact["coverage"]["ordered_second_row_hash_root"], "second ordered root")
    require(dict(sorted(collections.Counter(row["proof"] for row in first).items())) == artifact["proof_mechanisms"]["first_layer"], "first proof census")
    require(dict(sorted(collections.Counter(row["proof"] for row in second).items())) == artifact["proof_mechanisms"]["second_layer"], "second proof census")
    require(forest["census"]["cycles"] == forest["census"]["missing_children"] == forest["census"]["unresolved"] == 0, "forest terminal gates")

    text = canonical_bytes(artifact).decode().lower()
    forbidden = ["rooted_" + "triple", "tree_" + "sunlet"]
    require(not any(fragment in text for fragment in forbidden), "deprecated field/reason leaked into compression artifact")
    require(artifact["compression_verdict"]["exact_transport_quotient_count"] is None, "unsafe quotient promotion")
    require(artifact["definition"]["safe_use"] == "compresses exposition and repeated outcome patterns only", "scope boundary")

    report = {
        "schema": "k2p-restoration-archetype-verification-v1",
        "status": "PASS",
        "artifact_sha256": file_sha256(ARTIFACT),
        "artifact_payload_sha256": payload,
        "analyzer_sha256": file_sha256(ANALYZER),
        "deterministic_replay_equal": True,
        "optimized_mode_rejected": True,
        "coverage": {
            "canonical_parents": len(parent_keys),
            "descriptive_archetypes": len(archetypes),
            "member_roots": len(roots),
            "first_children": len(first),
            "second_children": len(second),
            "forest_edges": len(first) + len(second),
            "unassigned_parents": 0,
            "multiply_assigned_parents": 0,
            "orphan_second_rows": 0,
        },
        "equivalence_scope": {
            "member_fingerprint_replay": "exact",
            "archetype_membership_replay": "exact",
            "cross_parent_graph_transport_quotient": "not asserted",
            "authoritative_residue": "corrected restoration forest and its exact transport ledgers",
        },
        "forbidden_field_or_reason_occurrences": 0,
    }
    report["payload_sha256"] = object_sha256(report)
    return report


def main() -> None:
    if not __debug__:
        raise Failure("RESTORATION_ARCHETYPE_VERIFIER_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--emit", action="store_true")
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", type=Path, nargs="?", const=REPORT)
    args = parser.parse_args()
    generated = build_report()
    if args.emit:
        print(json.dumps(generated, indent=2, sort_keys=True))
        return
    if args.write:
        REPORT.write_text(json.dumps(generated, indent=2, sort_keys=True) + "\n")
        print(json.dumps({
            "status": "PASS",
            "report_sha256": file_sha256(REPORT),
            "payload_sha256": generated["payload_sha256"],
        }, sort_keys=True))
        return
    target = args.check or REPORT
    require(target.exists(), f"missing verification report:{target}")
    require(load_plain_json(target) == generated, "verification report drift")
    print(json.dumps({
        "status": "PASS",
        "report_sha256": file_sha256(target),
        "payload_sha256": generated["payload_sha256"],
        **generated["coverage"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
