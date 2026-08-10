#!/usr/bin/env python3
"""Independent contract verifier for emitted primitive-atlas records."""

from __future__ import annotations

import argparse
import gzip
from hashlib import sha256
import json
from pathlib import Path
import shutil
from typing import Any, Iterable, Iterator, Mapping

from graphcanon import canonical_json, canonicalize, digest, merkle_root
from primitive import reconstruct_graph
from rootings import rooting_census
from fourier import (
    compile_switchings,
    displayed_parameter_signature,
    complete_tensor_hash,
    tensor_probe_hash,
    verify_parameter_permutation_witness,
)
from relations import decorated_relation, ordinary_t_related
from selected_restrictions import audit as selected_restriction_audit


HERE = Path(__file__).resolve().parent


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def file_hash(path: Path) -> str:
    hasher = sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            hasher.update(block)
    return hasher.hexdigest()


def jsonl_gzip(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                yield json.loads(line)
            except Exception as exc:
                raise VerificationError(f"{path.name}:{line_number}: invalid JSON: {exc}") from exc


def record_body_hash(record: Mapping[str, Any]) -> str:
    body = dict(record)
    body.pop("record_hash", None)
    return digest(body)


def relation_id(record: Mapping[str, Any]) -> str:
    body = dict(record)
    body.pop("record_hash", None)
    body.pop("relation_id", None)
    return digest(body)


def verify_selected_audit_record(selected_stored: Mapping[str, Any]) -> None:
    selected_body = dict(selected_stored)
    selected_hash = selected_body.pop("payload_hash")
    require(selected_hash == digest(selected_body), "selected audit payload hash mismatch")
    selected_expected = selected_restriction_audit()
    selected_expected["pre_correction_manifest_hash"] = selected_stored[
        "pre_correction_manifest_hash"
    ]
    selected_expected["existing_primitive_T_relation_count_impact"] = selected_stored[
        "existing_primitive_T_relation_count_impact"
    ]
    selected_expected["selected_completion_core_retention_impact"] = {
        count: {
            "promoted_from_dummy_false_negative_to_retains_strong_core": row.get(
                "false_negative_under_dummy_rule", 0
            ),
            "retains_strong_core": row["retains_strong_core"],
            "does_not_retain_strong_core": row["does_not_retain_strong_core"],
        }
        for count, row in selected_expected["per_selected_count"].items()
    }
    selected_expected["payload_hash"] = digest(selected_expected)
    require(selected_expected == selected_stored, "selected-core-retention audit does not regenerate")


def verify_primitive(record: Mapping[str, Any]) -> None:
    require(record["record_hash"] == record_body_hash(record), "primitive record hash mismatch")
    require(record["graph_hash"] == digest(record["canonical_graph"]), "primitive graph hash mismatch")
    graph = reconstruct_graph(record)
    code, mapping = canonicalize(graph)
    require(code == record["canonical_graph"], "stored primitive graph is not canonical")
    require(set(mapping.values()) == set(range(len(mapping))), "canonical vertex map is not bijective")
    compiled = compile_switchings(record)
    stored_signature = record["displayed_parameter_signature"]
    require(
        compiled == stored_signature["switchings"],
        f"switching/mask mismatch for {record['graph_hash']}",
    )
    recomputed_signature = displayed_parameter_signature(record)
    require(
        recomputed_signature == stored_signature,
        f"displayed-parameter signature mismatch for {record['graph_hash']}",
    )
    require(tensor_probe_hash(record) == record["tensor_probe_hash"], "tensor probe hash mismatch")
    if int(record["port_count"]) <= 5:
        require(
            complete_tensor_hash(record) == record["complete_tensor_hash"],
            "complete exact tensor hash mismatch",
        )


def _decorations_from_roles(roles: Mapping[str, list[str]]) -> dict[str, list[int]]:
    decorations: dict[str, list[int]] = {}
    for label_text, entries in roles.items():
        label = int(label_text)
        for entry in entries:
            if entry in {"IN", "OUT", "SINK"}:
                continue
            decorations.setdefault(entry.lower(), []).append(label)
    return decorations


def verify_relation(
    relation: Mapping[str, Any], primitives: Mapping[str, Mapping[str, Any]]
) -> None:
    require(relation["record_hash"] == record_body_hash(relation), "relation record hash mismatch")
    require(relation["relation_id"] == relation_id(relation), "relation ID mismatch")
    require(
        relation["relation_graph_hash"] == digest(relation["canonical_relation_graph"]),
        "relation graph hash mismatch",
    )
    source = primitives.get(relation["source_graph_hash"])
    target = primitives.get(relation["target_graph_hash"])
    require(source is not None and target is not None, "relation references absent primitive")
    port_map = {int(k): int(v) for k, v in relation["port_map"].items()}
    rebuilt = decorated_relation(
        source,
        target,
        port_map=port_map,
        source_decorations=_decorations_from_roles(relation["source_port_roles"]),
        target_decorations=_decorations_from_roles(relation["target_port_roles"]),
        classification=relation["classification"],
        witness=relation["witness"],
    )
    rebuilt["record_hash"] = record_body_hash(rebuilt)
    require(rebuilt == relation, f"decorated relation does not regenerate: {relation['relation_id']}")
    if relation["classification"] == "ordinary_T_topological_relation":
        require(ordinary_t_related(source, target), "stored ordinary-T pair is not a T relation")
        require(
            relation["witness"].get("source_graph_hash") == relation["source_graph_hash"]
            and relation["witness"].get("target_graph_hash") == relation["target_graph_hash"],
            "ordinary-T witness is bound to a different ordered pair",
        )
    if relation["classification"] in {
        "ordinary_T",
        "non_T_equal_displayed_parameter_signature",
    }:
        require(
            verify_parameter_permutation_witness(source, target, relation["witness"]),
            "displayed-parameter witness is invalid",
        )


def verify_manifest(certificate_dir: Path) -> dict[str, Any]:
    manifest_path = certificate_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    body = dict(manifest)
    stored_body_hash = body.pop("manifest_body_hash")
    require(stored_body_hash == digest(body), "manifest body hash mismatch")
    definitions = Path(manifest["definitions_lock"]["path"])
    require(definitions.is_file(), "locked definitions file is absent")
    require(file_hash(definitions) == manifest["definitions_lock"]["sha256"], "definitions hash mismatch")
    for name, expected in manifest["source_hashes"].items():
        require(file_hash(HERE / name) == expected, f"source hash mismatch: {name}")

    selected_metadata = manifest["selected_core_retention_audit"]
    selected_path = certificate_dir / selected_metadata["path"]
    require(selected_path.is_file(), "selected-core-retention audit is absent")
    require(file_hash(selected_path) == selected_metadata["sha256"], "core-retention audit file hash mismatch")
    selected_stored = json.loads(selected_path.read_text())
    verify_selected_audit_record(selected_stored)
    require(
        selected_stored["payload_hash"] == selected_metadata["payload_hash"],
        "selected audit manifest binding mismatch",
    )

    failure_metadata = manifest["preserved_dummy_repair_failure"]
    failure_path = certificate_dir / failure_metadata["path"]
    require(failure_path.is_file(), "pre-correction dummy-repair failure is absent")
    require(file_hash(failure_path) == failure_metadata["sha256"], "failure file hash mismatch")
    failure = json.loads(failure_path.read_text())
    failure_body = dict(failure)
    failure_hash = failure_body.pop("payload_hash")
    require(failure_hash == digest(failure_body), "failure payload hash mismatch")
    require(failure_hash == failure_metadata["payload_hash"], "failure manifest binding mismatch")
    require(
        failure["counterexample"] == selected_stored["first_dummy_rule_false_negative"],
        "preserved failure counterexample does not match corrected audit",
    )

    limitation_metadata = manifest["preserved_intrinsic_membership_overclaim"]
    limitation_path = certificate_dir / limitation_metadata["path"]
    require(limitation_path.is_file(), "intrinsic-membership overclaim is not preserved")
    require(
        file_hash(limitation_path) == limitation_metadata["sha256"],
        "semantic-limitation file hash mismatch",
    )
    limitation = json.loads(limitation_path.read_text())
    limitation_body = dict(limitation)
    limitation_hash = limitation_body.pop("payload_hash")
    require(limitation_hash == digest(limitation_body), "semantic-limitation payload hash mismatch")
    require(
        limitation_hash == limitation_metadata["payload_hash"],
        "semantic-limitation manifest binding mismatch",
    )
    require(
        limitation["counterexample"]
        == selected_stored["sink_omission_intrinsic_STC_counterexample"],
        "sink-omission semantic counterexample does not match core-retention audit",
    )
    require(
        selected_stored["intrinsic_selected_STC_membership_classified"] is False,
        "core-retention audit overclaims intrinsic selected S_TC membership",
    )

    totals = {"roles": 0, "primitives": 0, "transports": 0, "relations": 0}
    for universe in manifest["universes"]:
        p = int(universe["port_count"])
        for name, metadata in universe["files"].items():
            path = certificate_dir / name
            require(path.is_file(), f"missing certificate file {name}")
            require(file_hash(path) == metadata["sha256"], f"file hash mismatch: {name}")

        roles = list(jsonl_gzip(certificate_dir / f"p{p}_role_classes.jsonl.gz"))
        primitives_list = list(jsonl_gzip(certificate_dir / f"p{p}_labelled_primitives.jsonl.gz"))
        transports = list(jsonl_gzip(certificate_dir / f"p{p}_raw_to_labelled_transports.jsonl.gz"))
        relations = list(jsonl_gzip(certificate_dir / f"p{p}_decorated_relations.jsonl.gz"))
        primitives = {record["graph_hash"]: record for record in primitives_list}
        require(len(primitives) == len(primitives_list), f"duplicate primitive graph at p={p}")
        require(len({record["record_hash"] for record in roles}) == len(roles), f"duplicate role at p={p}")
        require(
            len({record["record_hash"] for record in transports}) == len(transports),
            f"duplicate raw-to-labelled transport at p={p}",
        )
        require(
            len({record["relation_id"] for record in relations}) == len(relations),
            f"duplicate relation at p={p}",
        )
        for role in roles:
            require(role["record_hash"] == record_body_hash(role), "role record hash mismatch")
            require(role["role_hash"] == digest(role["canonical_graph"]), "role graph hash mismatch")
            require(role["raw_transport_count"] == len(role["raw_transports"]), "role transport count mismatch")
            role_graph = reconstruct_graph(role)
            require(
                rooting_census(role_graph) == role["independent_admissible_rooting_census"],
                "admissible-rooting census mismatch",
            )
            require(role["independent_admissible_rooting_census"]["S_TC"], "role is not S_TC")
        for transport in transports:
            require(transport["record_hash"] == record_body_hash(transport), "transport hash mismatch")
            require(transport["graph_hash"] in primitives, "transport references absent primitive")
        for primitive in primitives_list:
            verify_primitive(primitive)
        for relation in relations:
            verify_relation(relation, primitives)

        require(
            merkle_root(role["record_hash"] for role in roles) == universe["role_record_merkle_root"],
            f"role Merkle mismatch at p={p}",
        )
        require(
            merkle_root(record["record_hash"] for record in primitives_list)
            == universe["primitive_record_merkle_root"],
            f"primitive Merkle mismatch at p={p}",
        )
        require(
            merkle_root(record["record_hash"] for record in transports)
            == universe["transport_record_merkle_root"],
            f"transport Merkle mismatch at p={p}",
        )
        require(
            merkle_root(record["record_hash"] for record in relations)
            == universe["relation_record_merkle_root"],
            f"relation Merkle mismatch at p={p}",
        )
        file_records = universe["files"]
        require(file_records[f"p{p}_role_classes.jsonl.gz"]["records"] == len(roles), "role count mismatch")
        require(
            file_records[f"p{p}_labelled_primitives.jsonl.gz"]["records"] == len(primitives_list),
            "primitive count mismatch",
        )
        require(
            file_records[f"p{p}_raw_to_labelled_transports.jsonl.gz"]["records"] == len(transports),
            "transport count mismatch",
        )
        require(
            file_records[f"p{p}_decorated_relations.jsonl.gz"]["records"] == len(relations),
            "relation count mismatch",
        )
        totals["roles"] += len(roles)
        totals["primitives"] += len(primitives_list)
        totals["transports"] += len(transports)
        totals["relations"] += len(relations)
    return {"status": "VERIFIED", "manifest_body_hash": stored_body_hash, "totals": totals}


def regenerate_and_compare(certificate_dir: Path) -> dict[str, Any]:
    from build_atlas import build

    manifest = json.loads((certificate_dir / "manifest.json").read_text())
    regenerated = certificate_dir.parent / ".regenerated_contract_review"
    if regenerated.exists():
        require(regenerated.parent == certificate_dir.parent, "unsafe regeneration path")
        shutil.rmtree(regenerated)
    regenerated.mkdir()
    try:
        build(list(manifest["ports"]), regenerated, Path(manifest["definitions_lock"]["path"]))
        expected_files = sorted(path.name for path in certificate_dir.iterdir() if path.is_file())
        actual_files = sorted(path.name for path in regenerated.iterdir() if path.is_file())
        require(expected_files == actual_files, "regenerated file set mismatch")
        mismatches = [name for name in expected_files if file_hash(certificate_dir / name) != file_hash(regenerated / name)]
        require(not mismatches, f"regenerated byte mismatch: {mismatches}")
        return {"status": "BYTE_IDENTICAL_REGENERATION", "file_count": len(expected_files)}
    finally:
        if regenerated.exists():
            shutil.rmtree(regenerated)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate_dir", type=Path, nargs="?", default=HERE / "certificates")
    parser.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    result = verify_manifest(args.certificate_dir.resolve())
    if args.regenerate:
        result["regeneration"] = regenerate_and_compare(args.certificate_dir.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
