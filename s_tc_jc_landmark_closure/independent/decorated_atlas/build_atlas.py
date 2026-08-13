#!/usr/bin/env python3
"""Build deterministic primitive and decorated-relation certificates."""

from __future__ import annotations

import argparse
import gzip
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from graphcanon import canonical_json, digest, merkle_root
from primitive import enumerate_role_classes, enumerate_labelled_classes, serializable_role_class
from fourier import displayed_parameter_signature, complete_tensor_hash, tensor_probe_hash
from relations import ordinary_t_relations, equal_displayed_parameter_relations
from selected_restrictions import audit as selected_restriction_audit


SCHEMA = "independent-decorated-atlas-v2"
HERE = Path(__file__).resolve().parent
DEFAULT_DEFINITIONS = HERE.parents[1] / "docs" / "DEFINITIONS_LOCK.md"
SOURCE_FILES = (
    "graphcanon.py",
    "primitive.py",
    "rootings.py",
    "fourier.py",
    "relations.py",
    "selected_restrictions.py",
    "build_atlas.py",
    "verify_contract.py",
    "mutation_tests.py",
)

PRE_SELECTED_STRENGTH_CORRECTION_MANIFEST = (
    "16e15131c2a77cc51f75626286e01c0f815a0b8b4811299dba876a172ed6f333"
)
PRE_CORE_RETENTION_SEMANTIC_CORRECTION_MANIFEST_BODY_HASH = (
    "62da7d21262aba940b2e4576aa8937bd2be59e40b12a21dc05073396082fd20d"
)
PRE_CORE_RETENTION_SEMANTIC_CORRECTION_MANIFEST_FILE_SHA256 = (
    "ea6690c606d8150229ec4e9cefafdaf0262a3c39e893c2b825f99bb0a7d70bfb"
)


def file_hash(path: Path) -> str:
    hasher = sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            hasher.update(block)
    return hasher.hexdigest()


def _write_json(path: Path, value: Any) -> str:
    payload = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    path.write_bytes(payload)
    return sha256(payload).hexdigest()


def _write_jsonl_gzip(path: Path, records: Iterable[Mapping[str, Any]]) -> tuple[str, int]:
    count = 0
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as handle:
            for record in records:
                handle.write(canonical_json(record).encode())
                handle.write(b"\n")
                count += 1
    return file_hash(path), count


def _record_hash(record: Mapping[str, Any]) -> str:
    body = dict(record)
    body.pop("record_hash", None)
    return digest(body)


def build_port_universe(port_count: int, output: Path) -> dict[str, Any]:
    roles, role_summary = enumerate_role_classes(port_count)
    labelled, summary, labelled_transports = enumerate_labelled_classes(
        port_count, roles=roles, role_summary=role_summary
    )

    enriched: list[dict[str, Any]] = []
    for record0 in labelled:
        record = dict(record0)
        signature = displayed_parameter_signature(record)
        record["displayed_parameter_signature"] = signature
        record["tensor_probe_hash"] = tensor_probe_hash(record)
        if port_count <= 5:
            record["complete_tensor_hash"] = complete_tensor_hash(record)
            record["complete_tensor_hash_scope"] = "all zero-sum Fourier coordinates"
        else:
            record["complete_tensor_hash"] = None
            record["complete_tensor_hash_scope"] = "compiler present; bounded regression probes stored"
        record["record_hash"] = _record_hash(record)
        enriched.append(record)

    t_relations, t_summary = ordinary_t_relations(enriched)
    equal_relations, equal_summary = equal_displayed_parameter_relations(enriched)
    relation_by_id = {relation["relation_id"]: relation for relation in t_relations}
    for relation in equal_relations:
        existing = relation_by_id.get(relation["relation_id"])
        if existing is not None and canonical_json(existing) != canonical_json(relation):
            raise AssertionError("relation ID collision across relation classes")
        relation_by_id[relation["relation_id"]] = relation
    relations = [relation_by_id[key] for key in sorted(relation_by_id)]

    role_records = [serializable_role_class(role) for role in roles]
    if not all(role["independent_admissible_rooting_census"]["S_TC"] for role in role_records):
        raise AssertionError("a generated primitive role is not S_TC under the narrow rooting census")
    for role in role_records:
        role["record_hash"] = _record_hash(role)
    for transport in labelled_transports:
        transport["record_hash"] = _record_hash(transport)
    for relation in relations:
        relation["record_hash"] = _record_hash(relation)

    prefix = f"p{port_count}"
    role_path = output / f"{prefix}_role_classes.jsonl.gz"
    primitive_path = output / f"{prefix}_labelled_primitives.jsonl.gz"
    transport_path = output / f"{prefix}_raw_to_labelled_transports.jsonl.gz"
    relation_path = output / f"{prefix}_decorated_relations.jsonl.gz"
    failures_path = output / f"{prefix}_preserved_failures.json"

    role_sha, role_count = _write_jsonl_gzip(role_path, role_records)
    primitive_sha, primitive_count = _write_jsonl_gzip(primitive_path, enriched)
    transport_sha, transport_count = _write_jsonl_gzip(transport_path, labelled_transports)
    relation_sha, relation_count = _write_jsonl_gzip(relation_path, relations)
    failures = {
        "schema": SCHEMA,
        "port_count": port_count,
        "orientation_rejections": summary["orientation_audit"],
        "ordinary_T_variants_outside_fixed_incoming_universe": t_summary["missing_T_variants"],
        "non_T_equal_displayed_parameter_signature_relation_ids": equal_summary["non_T_relation_ids"],
    }
    failures_sha = _write_json(failures_path, failures)

    return {
        "port_count": port_count,
        "summary": summary,
        "ordinary_T_summary": t_summary,
        "equal_displayed_parameter_summary": equal_summary,
        "files": {
            role_path.name: {"sha256": role_sha, "records": role_count},
            primitive_path.name: {"sha256": primitive_sha, "records": primitive_count},
            transport_path.name: {"sha256": transport_sha, "records": transport_count},
            relation_path.name: {"sha256": relation_sha, "records": relation_count},
            failures_path.name: {"sha256": failures_sha, "records": 1},
        },
        "role_record_merkle_root": merkle_root(role["record_hash"] for role in role_records),
        "primitive_record_merkle_root": merkle_root(record["record_hash"] for record in enriched),
        "transport_record_merkle_root": merkle_root(
            transport["record_hash"] for transport in labelled_transports
        ),
        "relation_record_merkle_root": merkle_root(record["record_hash"] for record in relations),
    }


def build(ports: list[int], output: Path, definitions: Path) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    if not definitions.is_file():
        raise FileNotFoundError(definitions)
    source_hashes = {}
    for name in SOURCE_FILES:
        path = HERE / name
        if path.is_file():
            source_hashes[name] = file_hash(path)
    per_port = [build_port_universe(port_count, output) for port_count in ports]
    selected_audit = selected_restriction_audit()
    selected_audit["pre_correction_manifest_hash"] = PRE_SELECTED_STRENGTH_CORRECTION_MANIFEST
    selected_audit["existing_primitive_T_relation_count_impact"] = {
        str(item["port_count"]): 0 for item in per_port
    }
    selected_audit["selected_completion_core_retention_impact"] = {
        count: {
            "promoted_from_dummy_false_negative_to_retains_strong_core": row.get(
                "false_negative_under_dummy_rule", 0
            ),
            "retains_strong_core": row["retains_strong_core"],
            "does_not_retain_strong_core": row["does_not_retain_strong_core"],
        }
        for count, row in selected_audit["per_selected_count"].items()
    }
    selected_audit["payload_hash"] = digest(selected_audit)
    selected_audit_path = output / "selected_core_retention_audit.json"
    selected_audit_sha = _write_json(selected_audit_path, selected_audit)
    dummy_failure = {
        "schema": "selected-core-retention-dummy-failure-preservation-v2",
        "status": "FAILURE_PRESERVED_BEFORE_CORRECTION",
        "pre_correction_manifest_hash": PRE_SELECTED_STRENGTH_CORRECTION_MANIFEST,
        "failure": (
            "the primitive relation universe had no dummy-completion classifier; treating the presence "
            "of a dummy repair leaf as failure to retain the strong core gives exact false negatives"
        ),
        "counterexample": selected_audit["first_dummy_rule_false_negative"],
        "false_negative_counts": {
            count: row.get("false_negative_under_dummy_rule", 0)
            for count, row in selected_audit["per_selected_count"].items()
        },
    }
    dummy_failure["payload_hash"] = digest(dummy_failure)
    dummy_failure_path = output / "selected_core_retention_dummy_failure.json"
    dummy_failure_sha = _write_json(dummy_failure_path, dummy_failure)
    semantic_limitation = {
        "schema": "selected-core-retention-semantic-limitation-v1",
        "status": "OVERCLAIM_PRESERVED_BEFORE_CORRECTION",
        "overclaim_manifest_body_hash": PRE_CORE_RETENTION_SEMANTIC_CORRECTION_MANIFEST_BODY_HASH,
        "overclaim_manifest_file_sha256": PRE_CORE_RETENTION_SEMANTIC_CORRECTION_MANIFEST_FILE_SHA256,
        "withdrawn_claim": (
            "all sinks selected plus minimum repair classified intrinsic selected S_TC membership"
        ),
        "corrected_claim": (
            "the predicate classifies retention of the original primitive core as a strong factor only"
        ),
        "counterexample": selected_audit["sink_omission_intrinsic_STC_counterexample"],
    }
    semantic_limitation["payload_hash"] = digest(semantic_limitation)
    semantic_limitation_path = output / "selected_core_retention_semantic_limitation.json"
    semantic_limitation_sha = _write_json(semantic_limitation_path, semantic_limitation)

    # These v1 names carried the withdrawn intrinsic-membership semantics.  Do
    # not leave them beside the active v2 artifacts in a regenerated release.
    for stale_name in (
        "selected_restriction_audit.json",
        "selected_strength_failure_precorrection.json",
    ):
        stale_path = output / stale_name
        if stale_path.exists():
            stale_path.unlink()
    manifest = {
        "schema": SCHEMA,
        "status": "EXACTLY_COMPUTED_PRIMITIVE_UNIVERSE",
        "definitions_lock": {
            "path": str(definitions.resolve()),
            "sha256": file_hash(definitions),
        },
        "ports": ports,
        "source_hashes": source_hashes,
        "universes": per_port,
        "selected_core_retention_audit": {
            "path": selected_audit_path.name,
            "sha256": selected_audit_sha,
            "payload_hash": selected_audit["payload_hash"],
        },
        "preserved_dummy_repair_failure": {
            "path": dummy_failure_path.name,
            "sha256": dummy_failure_sha,
            "payload_hash": dummy_failure["payload_hash"],
        },
        "preserved_intrinsic_membership_overclaim": {
            "path": semantic_limitation_path.name,
            "sha256": semantic_limitation_sha,
            "payload_hash": semantic_limitation["payload_hash"],
        },
        "claim_boundary": {
            "proved": [
                "exhaustive duplicate-free primitive cycle/theta presentations for the listed port counts",
                "canonical decorated directed relation contract with full port matching",
                "graph-derived displayed switchings, descendant masks, and exact JC coordinate compiler",
                "all reported equal displayed-parameter signatures have explicit parameter-permutation witnesses",
                "selected_retains_strong_core is characterized by all selected reticulation sinks plus containment of one minimum repair",
            ],
            "not_proved": [
                "intrinsic S_TC membership of a selected restriction after arbitrary red_* reduction",
                "completeness of any finite invariant deck for stochastic containment",
                "arbitrary-subdivision promotion",
                "the global S_TC identifiability theorem",
            ],
        },
    }
    manifest["manifest_body_hash"] = digest(manifest)
    _write_json(output / "manifest.json", manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ports", nargs="+", type=int, default=[4, 5, 6, 7])
    parser.add_argument("--output", type=Path, default=HERE / "certificates")
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    args = parser.parse_args()
    ports = sorted(set(args.ports))
    if any(port < 3 for port in ports):
        parser.error("every port count must be at least three")
    manifest = build(ports, args.output.resolve(), args.definitions.resolve())
    print(json.dumps({
        "status": manifest["status"],
        "ports": ports,
        "manifest": str((args.output.resolve() / "manifest.json")),
        "manifest_body_hash": manifest["manifest_body_hash"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
