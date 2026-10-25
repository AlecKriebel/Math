#!/usr/bin/env python3
"""Fail-closed verifier for the authoritative cycle promotion projection."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import decode_json_document, iter_canonical_gzip_jsonl  # noqa: E402
CYCLE = PROJECT / "work/cycle_three_port_closure"
ARTIFACTS = CYCLE / "artifacts"
DEFAULT_PROMOTION = CYCLE / "promotion"
DEFAULT_TRUTH = HERE / "cycle_tree_sunlet_full_map_certificate.json"
DEFAULT_REPORT = HERE / "cycle_promotion_independent_verification.json"
FORBIDDEN_KEYS = {
    "topology_exclusion_reason", "historical_proof", "historical_reason",
    "rooted_restriction", "rooted_type", "source_type", "target_type",
}
FORBIDDEN_TEXT = ("tree_sunlet", "pointwise", "rooted restriction", "historical_proof")


class PromotionFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise PromotionFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rows(path):
    yield from iter_canonical_gzip_jsonl(path, label=path.name)


def no_revoked_provenance(value, context):
    if isinstance(value, dict):
        overlap = FORBIDDEN_KEYS.intersection(value)
        require(not overlap, f"forbidden fields:{context}:{sorted(overlap)}")
        for key, child in value.items():
            no_revoked_provenance(child, f"{context}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            no_revoked_provenance(child, f"{context}[{index}]")
    elif isinstance(value, str):
        lowered = value.lower()
        require(not any(token in lowered for token in FORBIDDEN_TEXT), f"forbidden text:{context}")


def transport_hash(row):
    return sha({
        "schema": "k2p-cycle-fixed-full-child-transport-v1",
        "root_id": row["root_id"], "base_raw_id": row["base_raw_id"],
        "full_raw_id": row["raw_id"], "source_index": row["source_index"],
        "target_index": row["target_index"], "permutation_index": row["permutation_index"],
        "dummy_roles_in_label_order": row["dummy_roles_in_label_order"],
        "source_placement_path": row["source_placement_path"], "port_count": row["port_count"],
        "source_operation": "iterated_labelled_edge_subdivision_attachment",
        "target_operation": "simultaneous_labelled_dummy_role_promotion",
    })


def self_hash(row):
    payload = dict(row)
    claimed = payload.pop("authoritative_row_sha256", None)
    require(claimed == sha(payload), f"authoritative self hash:{row.get('raw_id')}")
    return claimed


def main():
    if not __debug__:
        raise PromotionFailure("CYCLE_PROMOTION_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--promotion-root", type=Path, default=DEFAULT_PROMOTION)
    parser.add_argument("--truth-certificate", type=Path, default=DEFAULT_TRUTH)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    arguments = parser.parse_args()
    promotion = arguments.promotion_root
    summary_path = promotion / "cycle_promotion_certificate.json"
    base_path = promotion / "cycle_base_authoritative.jsonl.gz"
    full_path = promotion / "cycle_full_authoritative.jsonl.gz"
    summary = decode_json_document(
        summary_path.read_bytes(), label=summary_path.name, require_object=True
    )
    unhashed = dict(summary)
    payload = unhashed.pop("payload_sha256", None)
    require(payload == sha(unhashed), "summary payload")
    require(summary.get("schema") == "k2p-cycle-three-port-authoritative-promotion-v1", "schema")
    require(summary.get("status") == "PASS", "status")
    require(summary.get("legacy_rooted_reason_or_type_fields") == 0, "legacy field claim")
    require(summary.get("unresolved") == summary.get("incoherent") == 0, "terminal status")

    fixed_inputs = {
        "atlas_sha256": PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py",
        "cycle_common_sha256": CYCLE / "cycle_common.py",
        "cycle_generator_sha256": CYCLE / "generate_cycle_closure.py",
        "historical_base_ledger_sha256": ARTIFACTS / "base_raw_ledger.jsonl.gz",
        "historical_full_ledger_sha256": ARTIFACTS / "full_completion_ledger.jsonl.gz",
        "restoration_roots_sha256": ARTIFACTS / "restoration_roots.jsonl.gz",
        "topology_witnesses_sha256": ARTIFACTS / "topology_witnesses.json",
        "transport_certificates_sha256": ARTIFACTS / "transport_certificates.json",
        "quadratic_certificates_sha256": ARTIFACTS / "quadratic_certificates.json",
        "physical_anchors_sha256": ARTIFACTS / "physical_anchors.json",
        "whole_map_truth_file_sha256": arguments.truth_certificate,
    }
    for field, path in fixed_inputs.items():
        require(summary["inputs"].get(field) == sha_file(path), f"input binding:{field}")
    require(summary["outputs"][base_path.name]["sha256"] == sha_file(base_path), "base output hash")
    require(summary["outputs"][full_path.name]["sha256"] == sha_file(full_path), "full output hash")

    truth = decode_json_document(
        arguments.truth_certificate.read_bytes(),
        label=arguments.truth_certificate.name,
        require_object=True,
    )
    truth_unhashed = dict(truth)
    truth_payload = truth_unhashed.pop("payload_sha256", None)
    require(truth_payload == sha(truth_unhashed), "truth payload")
    require(truth.get("status") == "PASS" and truth.get("unresolved") == 0, "truth status")
    require(summary["inputs"]["whole_map_truth_payload_sha256"] == truth_payload, "truth payload binding")
    base_truth = truth["families"]["cycle_base"]["ordered_truth_row_hashes"]
    full_truth = truth["families"]["cycle_full_equal_topology"]["ordered_truth_row_hashes"]
    require(len(base_truth) == 7452 and len(full_truth) == 300, "truth coverage")

    topology_path = ARTIFACTS / "topology_witnesses.json"
    transport_path = ARTIFACTS / "transport_certificates.json"
    quadratic_path = ARTIFACTS / "quadratic_certificates.json"
    topology = decode_json_document(
        topology_path.read_bytes(), label=topology_path.name, require_object=True
    )["witnesses"]
    transports = decode_json_document(
        transport_path.read_bytes(), label=transport_path.name, require_object=True
    )["certificates"]
    quadratics = decode_json_document(
        quadratic_path.read_bytes(), label=quadratic_path.name, require_object=True
    )["certificates"]
    roots_by_raw = {row["base_raw_id"]: row for row in rows(ARTIFACTS / "restoration_roots.jsonl.gz")}
    require(len(roots_by_raw) == 5964, "root census")

    base_counts = collections.Counter()
    base_hashes = []
    base_truth_index = 0
    historical_base = rows(ARTIFACTS / "base_raw_ledger.jsonl.gz")
    authoritative_base = rows(base_path)
    for ordinal, (old, row) in enumerate(zip(historical_base, authoritative_base, strict=True)):
        require(row["raw_id"] == ordinal == old["raw_id"], f"base order:{ordinal}")
        no_revoked_provenance(row, f"base:{ordinal}")
        base_hashes.append(self_hash(row))
        expected_common = {
            "raw_id": old["raw_id"], "source_index": old["source_index"],
            "target_index": old["target_index"], "permutation_index": old["permutation_index"],
            "port_permutation": old["port_permutation"], "dummy_roles": old["dummy_roles"],
        }
        for key, value in expected_common.items():
            require(row.get(key) == value, f"base field:{ordinal}:{key}")
        old_kind = old["category"]
        if old_kind == "tree_sunlet_pointwise_excluded":
            require(row["terminal_kind"] == "full_map_Ti_strict_sign", f"base sign kind:{ordinal}")
            require(row["whole_map_truth_row_sha256"] == base_truth[base_truth_index], f"base truth:{ordinal}")
            require(row["whole_map_truth_payload_sha256"] == truth_payload, f"base truth payload:{ordinal}")
            base_truth_index += 1
        elif old_kind == "restoration_root":
            require(row["terminal_kind"] == "fixed_full_restoration_obligation", f"base root kind:{ordinal}")
            require(row["root_id"] == roots_by_raw[ordinal]["root_id"], f"base root id:{ordinal}")
        elif old_kind == "isomorphic":
            require(row["terminal_kind"] == "labelled_isomorphism", f"base iso kind:{ordinal}")
            require(row["transport_certificate_id"] == old["certificate_id"] in transports, f"base iso transport:{ordinal}")
        elif old_kind == "triangle":
            require(row["terminal_kind"] == "ordinary_triangle_relation", f"base triangle kind:{ordinal}")
            require(row["transport_certificate_id"] == old["certificate_id"] in transports, f"base triangle transport:{ordinal}")
        else:
            raise PromotionFailure(f"unknown historical base kind:{old_kind}")
        base_counts[row["terminal_kind"]] += 1
    require(base_truth_index == len(base_truth), "base truth exhaustion")
    require(len(base_hashes) == 13440, f"base rows:{len(base_hashes)}")

    full_counts = collections.Counter()
    full_hashes = []
    transport_hashes = []
    child_counts = collections.Counter()
    full_truth_index = 0
    historical_full = rows(ARTIFACTS / "full_completion_ledger.jsonl.gz")
    authoritative_full = rows(full_path)
    for ordinal, (old, row) in enumerate(zip(historical_full, authoritative_full, strict=True)):
        require(row["raw_id"] == ordinal == old["raw_id"], f"full order:{ordinal}")
        no_revoked_provenance(row, f"full:{ordinal}")
        full_hashes.append(self_hash(row))
        for key in (
            "raw_id", "root_id", "base_raw_id", "source_index", "target_index",
            "permutation_index", "dummy_roles_in_label_order", "source_placement_path", "port_count",
        ):
            require(row.get(key) == old[key], f"full field:{ordinal}:{key}")
        expected_transport = transport_hash(old)
        require(row["fixed_full_transport_sha256"] == expected_transport, f"full transport:{ordinal}")
        transport_hashes.append(expected_transport)
        child_counts[row["root_id"]] += 1
        old_kind = old["category"]
        if old_kind == "quartet_pointwise_excluded":
            require(row["terminal_kind"] == "displayed_quartet_strict_separator", f"quartet kind:{ordinal}")
            require(row["proof_certificate_id"] == old["certificate_id"] in topology, f"quartet proof:{ordinal}")
            require(row["proof_certificate_id"].startswith("QW:"), f"non-quartet proof:{ordinal}")
        elif old_kind == "tree_sunlet_pointwise_excluded":
            require(row["terminal_kind"] == "full_map_Ti_strict_sign", f"full sign kind:{ordinal}")
            require(row["whole_map_truth_row_sha256"] == full_truth[full_truth_index], f"full truth:{ordinal}")
            require(row["whole_map_truth_payload_sha256"] == truth_payload, f"full truth payload:{ordinal}")
            full_truth_index += 1
        elif old_kind == "quadratic_separated":
            require(row["terminal_kind"] == "exact_directional_quadratic", f"quadratic kind:{ordinal}")
            require(row["proof_certificate_id"] == old["certificate_id"] in quadratics, f"quadratic proof:{ordinal}")
        elif old_kind == "isomorphic":
            require(row["terminal_kind"] == "labelled_isomorphism", f"full iso kind:{ordinal}")
            require(row["transport_certificate_id"] == old["certificate_id"] in transports, f"full iso transport:{ordinal}")
        else:
            raise PromotionFailure(f"unknown historical full kind:{old_kind}")
        full_counts[row["terminal_kind"]] += 1
    require(full_truth_index == len(full_truth), "full truth exhaustion")
    require(len(full_hashes) == 536364, f"full rows:{len(full_hashes)}")
    require(set(child_counts) == {row["root_id"] for row in roots_by_raw.values()}, "root child coverage")

    expected_base = collections.Counter({
        "full_map_Ti_strict_sign": 7452, "fixed_full_restoration_obligation": 5964,
        "labelled_isomorphism": 8, "ordinary_triangle_relation": 16,
    })
    expected_full = collections.Counter({
        "displayed_quartet_strict_separator": 535920, "full_map_Ti_strict_sign": 300,
        "exact_directional_quadratic": 132, "labelled_isomorphism": 12,
    })
    require(base_counts == expected_base, f"base census:{base_counts}")
    require(full_counts == expected_full, f"full census:{full_counts}")
    require(summary["base"]["rows"] == len(base_hashes), "summary base rows")
    require(summary["base"]["terminal_census"] == dict(base_counts), "summary base census")
    require(summary["base"]["ordered_authoritative_row_hash_root"] == sha(base_hashes), "summary base root")
    require(summary["full"]["rows"] == len(full_hashes), "summary full rows")
    require(summary["full"]["terminal_census"] == dict(full_counts), "summary full census")
    require(summary["full"]["ordered_authoritative_row_hash_root"] == sha(full_hashes), "summary full root")
    require(summary["fixed_full_restoration"]["roots"] == 5964, "summary roots")
    require(summary["fixed_full_restoration"]["children"] == len(full_hashes), "summary children")
    require(summary["fixed_full_restoration"]["roots_with_zero_children"] == 0, "summary missing children")
    require(
        summary["fixed_full_restoration"]["ordered_child_transport_hash_root"] == sha(transport_hashes),
        "summary transport root",
    )

    result = {
        "schema": "k2p-cycle-authoritative-promotion-independent-verification-v1",
        "status": "PASS", "promotion_payload_sha256": payload,
        "promotion_certificate_sha256": sha_file(summary_path),
        "base_rows": len(base_hashes), "restoration_roots": len(roots_by_raw),
        "full_children": len(full_hashes), "legacy_rooted_fields_or_reasons": 0,
        "unresolved": 0, "incoherent": 0,
    }
    result["payload_sha256"] = sha(result)
    arguments.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (PromotionFailure, KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"CYCLE_PROMOTION_VERIFY_FAIL:{exc}") from exc
