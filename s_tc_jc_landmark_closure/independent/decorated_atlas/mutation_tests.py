#!/usr/bin/env python3
"""Mutation-sensitive tests for primitive and relation bindings."""

from __future__ import annotations

import argparse
import copy
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Callable, Mapping

from graphcanon import digest, merkle_root
from verify_contract import (
    VerificationError,
    jsonl_gzip,
    record_body_hash,
    verify_primitive,
    verify_relation,
    verify_selected_audit_record,
)
from fourier import parameter_permutation_witness, verify_parameter_permutation_witness


HERE = Path(__file__).resolve().parent


def reseal_primitive(record: dict[str, Any]) -> None:
    record["graph_hash"] = digest(record["canonical_graph"])
    record["record_hash"] = record_body_hash(record)


def reseal_relation(record: dict[str, Any]) -> None:
    binding = {
        "source_graph_hash": record["source_graph_hash"],
        "target_graph_hash": record["target_graph_hash"],
        "direction": record["direction"],
        "port_map": record["port_map"],
        "relation_graph_hash": record["relation_graph_hash"],
        "classification": record["classification"],
        "witness": record["witness"],
    }
    record["witness_binding_hash"] = digest(binding)
    body = dict(record)
    body.pop("record_hash", None)
    body.pop("relation_id", None)
    record["relation_id"] = digest(body)
    record["record_hash"] = record_body_hash(record)


def expect_rejection(name: str, operation: Callable[[], None]) -> dict[str, Any]:
    try:
        operation()
    except Exception as exc:
        return {"mutation": name, "rejected": True, "exception": type(exc).__name__, "message": str(exc)}
    return {"mutation": name, "rejected": False, "exception": None, "message": "mutation escaped"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate_dir", type=Path, nargs="?", default=HERE / "certificates")
    parser.add_argument("--output", type=Path, default=HERE / "mutation_transcript.json")
    parser.add_argument("--fixture-port-count", type=int, default=4)
    args = parser.parse_args()
    certificate_dir = args.certificate_dir.resolve()
    manifest = json.loads((certificate_dir / "manifest.json").read_text())
    p = args.fixture_port_count
    universe = next(item for item in manifest["universes"] if int(item["port_count"]) == p)
    primitives_list = list(jsonl_gzip(certificate_dir / f"p{p}_labelled_primitives.jsonl.gz"))
    relations = list(jsonl_gzip(certificate_dir / f"p{p}_decorated_relations.jsonl.gz"))
    transports = list(jsonl_gzip(certificate_dir / f"p{p}_raw_to_labelled_transports.jsonl.gz"))
    primitives = {record["graph_hash"]: record for record in primitives_list}
    if len(relations) < 2 or len(primitives_list) < 2 or len(transports) < 2:
        raise RuntimeError("p=4 fixture is unexpectedly too small")

    results: list[dict[str, Any]] = []

    selected_audit = json.loads((certificate_dir / "selected_core_retention_audit.json").read_text())

    def mutate_core_retention() -> None:
        record = copy.deepcopy(selected_audit)
        record["first_dummy_rule_false_negative"]["selected_retains_strong_core"] = False
        body = dict(record)
        body.pop("payload_hash", None)
        record["payload_hash"] = digest(body)
        verify_selected_audit_record(record)

    results.append(
        expect_rejection("misclassify_dummy_repair_core_retention", mutate_core_retention)
    )

    def mutate_semantic_scope() -> None:
        record = copy.deepcopy(selected_audit)
        record["intrinsic_selected_STC_membership_classified"] = True
        body = dict(record)
        body.pop("payload_hash", None)
        record["payload_hash"] = digest(body)
        verify_selected_audit_record(record)

    results.append(
        expect_rejection("promote_core_retention_to_intrinsic_selected_STC", mutate_semantic_scope)
    )

    expected_primitive_hashes = sorted(record["record_hash"] for record in primitives_list)
    expected_primitive_root = universe["primitive_record_merkle_root"]

    def check_primitive_set(records: list[Mapping[str, Any]]) -> None:
        hashes = [record["record_hash"] for record in records]
        if len(hashes) != len(expected_primitive_hashes):
            raise VerificationError("primitive record count changed")
        if len(set(hashes)) != len(hashes):
            raise VerificationError("duplicate primitive record")
        if sorted(hashes) != expected_primitive_hashes:
            raise VerificationError("primitive record set changed")
        if merkle_root(hashes) != expected_primitive_root:
            raise VerificationError("primitive Merkle root changed")

    results.append(expect_rejection("delete_primitive", lambda: check_primitive_set(primitives_list[:-1])))
    results.append(
        expect_rejection(
            "duplicate_primitive",
            lambda: check_primitive_set(primitives_list[:-1] + [primitives_list[0], primitives_list[0]]),
        )
    )

    def mutate_edge() -> None:
        record = copy.deepcopy(primitives_list[0])
        upper = list(record["canonical_graph"]["upper_triangle"])
        index = next(i for i, value in enumerate(upper) if value != "0")
        upper[index] = "0"
        record["canonical_graph"]["upper_triangle"] = "".join(upper)
        reseal_primitive(record)
        verify_primitive(record)

    results.append(expect_rejection("alter_mixed_edge_and_reseal", mutate_edge))

    def mutate_inheritance_parent() -> None:
        record = copy.deepcopy(next(item for item in primitives_list if len(item["reticulations"]) == 2))
        record["incoming_parent_edges"][0][0] = record["incoming_parent_edges"][1][0]
        reseal_primitive(record)
        verify_primitive(record)

    results.append(expect_rejection("replace_inheritance_parent_edge_and_reseal", mutate_inheritance_parent))

    expected_relation_ids = sorted(record["relation_id"] for record in relations)
    expected_relation_root = universe["relation_record_merkle_root"]

    def check_relation_set(records: list[Mapping[str, Any]]) -> None:
        ids = [record["relation_id"] for record in records]
        hashes = [record["record_hash"] for record in records]
        if len(ids) != len(expected_relation_ids):
            raise VerificationError("relation record count changed")
        if len(set(ids)) != len(ids):
            raise VerificationError("duplicate relation ID")
        if sorted(ids) != expected_relation_ids:
            raise VerificationError("relation ID set changed")
        if merkle_root(hashes) != expected_relation_root:
            raise VerificationError("relation Merkle root changed")

    results.append(expect_rejection("delete_decorated_relation", lambda: check_relation_set(relations[:-1])))
    results.append(
        expect_rejection(
            "duplicate_decorated_relation",
            lambda: check_relation_set(relations[:-1] + [relations[0], relations[0]]),
        )
    )

    def mutate_port_map() -> None:
        relation = copy.deepcopy(relations[0])
        relation["port_map"]["1"], relation["port_map"]["2"] = (
            relation["port_map"]["2"],
            relation["port_map"]["1"],
        )
        reseal_relation(relation)
        verify_relation(relation, primitives)

    results.append(expect_rejection("alter_port_correspondence_and_reseal", mutate_port_map))

    def mutate_vertex_transport() -> None:
        relation = copy.deepcopy(relations[0])
        keys = sorted(relation["source_vertex_transport"], key=int)[:2]
        relation["source_vertex_transport"][keys[0]], relation["source_vertex_transport"][keys[1]] = (
            relation["source_vertex_transport"][keys[1]],
            relation["source_vertex_transport"][keys[0]],
        )
        reseal_relation(relation)
        verify_relation(relation, primitives)

    results.append(expect_rejection("alter_raw_to_canonical_vertex_map_and_reseal", mutate_vertex_transport))

    def reverse_direction() -> None:
        relation = copy.deepcopy(relations[0])
        relation["source_graph_hash"], relation["target_graph_hash"] = (
            relation["target_graph_hash"],
            relation["source_graph_hash"],
        )
        reseal_relation(relation)
        verify_relation(relation, primitives)

    results.append(expect_rejection("reverse_source_target_and_reseal", reverse_direction))

    def swap_witness() -> None:
        relation = copy.deepcopy(relations[0])
        relation["witness"] = copy.deepcopy(relations[1]["witness"])
        reseal_relation(relation)
        verify_relation(relation, primitives)

    results.append(expect_rejection("swap_witness_between_relations_and_reseal", swap_witness))

    def mutate_relation_edge_transport() -> None:
        relation = copy.deepcopy(relations[0])
        keys = sorted(relation["source_edge_transport"], key=int)[:2]
        relation["source_edge_transport"][keys[0]], relation["source_edge_transport"][keys[1]] = (
            relation["source_edge_transport"][keys[1]],
            relation["source_edge_transport"][keys[0]],
        )
        reseal_relation(relation)
        verify_relation(relation, primitives)

    results.append(
        expect_rejection("alter_relation_edge_transport_and_reseal", mutate_relation_edge_transport)
    )

    def mutate_relation_parent_transport() -> None:
        relation = copy.deepcopy(relations[0])
        relation["source_inheritance_parent_edge_transport"][0].reverse()
        reseal_relation(relation)
        verify_relation(relation, primitives)

    results.append(
        expect_rejection(
            "alter_relation_inheritance_parent_transport_and_reseal",
            mutate_relation_parent_transport,
        )
    )

    def mutate_parameter_normalizer() -> None:
        source = primitives_list[0]
        witness = parameter_permutation_witness(source, source)
        if witness is None:
            raise AssertionError("self-witness unexpectedly absent")
        witness["source_normalizer"]["old_to_new_choice"].reverse()
        if verify_parameter_permutation_witness(source, source, witness):
            return
        raise VerificationError("normalizer mutation rejected")

    results.append(expect_rejection("alter_parameter_normalizer", mutate_parameter_normalizer))

    def remove_cover_key() -> None:
        relation = copy.deepcopy(relations[0])
        del relation["source_vertex_transport"]
        reseal_relation(relation)
        verify_relation(relation, primitives)

    results.append(expect_rejection("remove_required_transport_key_and_reseal", remove_cover_key))

    # Same target, wrong source embedding: even after all superficial hashes
    # are resealed, rebuilding the jointly canonical relation must disagree.
    def collapse_source_embedding() -> None:
        relation = copy.deepcopy(relations[0])
        replacement = next(
            record
            for record in primitives_list
            if record["graph_hash"] not in {
                relation["source_graph_hash"],
                relation["target_graph_hash"],
            }
        )
        relation["source_graph_hash"] = replacement["graph_hash"]
        reseal_relation(relation)
        verify_relation(relation, primitives)

    results.append(expect_rejection("collapse_distinct_source_embedding_and_reseal", collapse_source_embedding))

    passed = all(item["rejected"] for item in results)
    transcript = {
        "status": "ALL_MUTATIONS_REJECTED" if passed else "MUTATION_ESCAPED",
        "certificate_manifest_hash": manifest["manifest_body_hash"],
        "fixture_port_count": p,
        "mutations": results,
    }
    args.output.write_text(json.dumps(transcript, indent=2, sort_keys=True) + "\n")
    print(json.dumps(transcript, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
