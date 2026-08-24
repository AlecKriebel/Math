#!/usr/bin/env python3
"""Build the acyclic unified five-family finite-universe certificate."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from release_common import (
    HERE,
    PROBE_AGGREGATE_COUNTS,
    PROBE_INPUT_FIRST_PAIRS,
    PROBE_ONE_PORT_COUNTS,
    PROBE_ONE_PORT_EQUALITIES,
    PROBE_TOTAL_EQUALITIES,
    PROBE_TOTAL_PAIRS,
    PROBE_TWO_PORT_COUNTS,
    PROBE_TWO_PORT_EQUALITIES,
    PROBE_TWO_PORT_PAIRS,
    corrected_locator,
    require,
    sha_object,
    validate_corrected_finite_universe,
)


DEFAULT_OUTPUT = HERE / "corrected_universe_certificate.json"
DOWNSTREAM_ROLES = {
    "corrected_universe_certificate",
    "corrected_universe_replay_report",
    "corrected_universe_mutation_report",
}


def family_record(
    *,
    input_count: int,
    categories: dict[str, int],
    input_root: str,
    output_root: str,
    children: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "input_count": input_count,
        "distinct_input_ids": input_count,
        "duplicate_input_ids": 0,
        "missing_input_ids": 0,
        "rows_with_exact_reason": input_count,
        "rows_with_exact_evidence": input_count,
        "output_category_counts": categories,
        "input_id_hash_root": input_root,
        "output_id_hash_root": output_root,
        "unresolved": 0,
        "forbidden_rooted_reason_count": 0,
        "forbidden_rooted_field_count": 0,
        "false_topology_oracle_count": 0,
        "false_graph_terminal_conflicts": 0,
    }
    if children is not None:
        row["generated_children"] = children
    return row


def child_record(
    count: int, id_root: str, edge_root: str, transport_root: str
) -> dict[str, Any]:
    return {
        "count": count,
        "distinct_ids": count,
        "duplicate_ids": 0,
        "missing_parent_links": 0,
        "multiple_parent_links": 0,
        "unresolved": 0,
        "id_hash_root": id_root,
        "parent_child_edge_hash_root": edge_root,
        "transport_restriction_hash_root": transport_root,
    }


def compose_certificate() -> dict[str, Any]:
    # Build only from the frozen producer layers.  The family-input mode is
    # intentionally independent of the locator's final promotion state so the
    # certificate remains reproducible after the downstream lock is frozen.
    summary, blockers = validate_corrected_finite_universe(
        family_inputs_only=True
    )
    require(
        summary.get("status") == "ALL_FIVE_FAMILIES_PASS_UNIFIED_CROSS_FAMILY_PENDING",
        "UNIFIED_BUILD_FAMILY_STATUS_FAIL",
    )
    require(
        blockers
        == [
            "CORRECTED_FINITE_UNIVERSE_NOT_FROZEN",
            "UNIFIED_CROSS_FAMILY_CERTIFICATE_REPLAY_MUTATIONS_PENDING",
        ],
        "UNIFIED_BUILD_BLOCKER_BOUNDARY_FAIL",
        blockers,
    )
    locator = corrected_locator()
    required_roles = set(locator["required_frozen_roles"])
    artifact_sha256 = {
        role: locator["artifacts"][role]["sha256"]
        for role in sorted(required_roles - DOWNSTREAM_ROLES)
    }

    raw4 = summary["raw4_composite"]
    theta2 = summary["theta2_composite"]
    restoration = summary["restoration_v3"]
    cycle = summary["cycle_promotion"]
    probe_input = summary["probe_input"]
    probe = summary["probe_producer"]

    families = {
        "raw4": family_record(
            input_count=raw4["total_rows"],
            categories=raw4["category_counts"],
            input_root=raw4["ordered_raw_id_hash_root"],
            output_root=raw4["ordered_row_hash_root"],
        ),
        "theta2": family_record(
            input_count=theta2["total_rows"],
            categories=theta2["category_counts"],
            input_root=theta2["ordered_raw_id_hash_root"],
            output_root=theta2["ordered_row_hash_root"],
            children=child_record(
                theta2["restoration_descendant_children"],
                theta2["restoration_descendant_child_id_hash_root"],
                theta2["restoration_descendant_edge_hash_root"],
                theta2["restoration_descendant_transport_hash_root"],
            ),
        ),
        "restoration": family_record(
            input_count=restoration["member_root_count"],
            categories={"restoration_member_presentation": restoration["member_root_count"]},
            input_root=restoration["member_root_id_hash_root"],
            output_root=restoration["member_root_id_hash_root"],
            children=child_record(
                restoration["generated_child_count"],
                restoration["generated_child_id_hash_root"],
                restoration["parent_child_edge_hash_root"],
                restoration["transport_restriction_hash_root"],
            ),
        ),
        "cycle": family_record(
            input_count=cycle["base_rows"],
            categories=cycle["base_category_counts"],
            input_root=cycle["base_row_hash_root"],
            output_root=cycle["base_row_hash_root"],
            children=child_record(
                cycle["full_children"],
                cycle["full_row_hash_root"],
                cycle["child_transport_hash_root"],
                cycle["child_transport_hash_root"],
            ),
        ),
        "probe": family_record(
            input_count=PROBE_TOTAL_PAIRS,
            categories=PROBE_AGGREGATE_COUNTS,
            input_root=probe["aggregate_raw_id_hash_root"],
            output_root=probe["aggregate_raw_id_hash_root"],
            children=child_record(
                PROBE_TOTAL_EQUALITIES,
                probe["equality_relation_id_hash_root"],
                probe["equality_parent_child_edge_hash_root"],
                probe["equality_transport_restriction_hash_root"],
            ),
        ),
    }

    forest = {
        "class_parent_count": raw4["restoration_parent_count"],
        "class_parent_id_hash_root": raw4["restoration_parent_id_hash_root"],
        "canonical_root_count": restoration["canonical_parent_count"],
        "covered_canonical_root_count": restoration["canonical_parent_count"],
        "member_root_count": restoration["member_root_count"],
        "covered_member_root_count": restoration["member_root_count"],
        "raw_presentation_membership_hash_root": raw4[
            "restoration_member_membership_hash_root"
        ],
        "member_root_id_hash_root": restoration["member_root_id_hash_root"],
        "class_membership_edge_count": restoration["member_root_count"],
        "class_membership_edge_hash_root": restoration[
            "class_membership_edge_hash_root"
        ],
        "generated_child_count": restoration["generated_child_count"],
        "covered_child_count": restoration["generated_child_count"],
        "generated_child_id_hash_root": restoration["generated_child_id_hash_root"],
        "parent_child_edge_hash_root": restoration["parent_child_edge_hash_root"],
        "transport_restriction_hash_root": restoration[
            "transport_restriction_hash_root"
        ],
        "edge_count": restoration["generated_child_count"],
        "transport_restrictions_replayed": restoration["generated_child_count"],
        "first_child_count": restoration["first_child_count"],
        "first_child_hash_root": restoration["first_child_hash_root"],
        "second_child_count": restoration["second_child_count"],
        "second_child_hash_root": restoration["second_child_hash_root"],
        "leaf_count": restoration["leaf_count"],
        "leaf_id_hash_root": restoration["leaf_id_hash_root"],
        "leaf_category_counts": restoration["leaf_category_counts"],
        "omitted_terminal_member_scope": restoration["omitted_terminal_member_scope"],
        "omitted_terminal_class_scope": restoration["omitted_terminal_class_scope"],
        "missing_canonical_roots": 0,
        "missing_member_roots": 0,
        "multiple_class_memberships": 0,
        "missing_children": 0,
        "cycles": 0,
        "unresolved": 0,
        "incoherent_transports": 0,
    }

    probe_coherence = {
        "producer_certificate_sha256": probe["certificate_file_sha256"],
        "producer_payload_sha256": probe["certificate_payload_sha256"],
        "producer_manifest_sha256": probe["manifest_file_sha256"],
        "adversarial_audit_file_sha256": probe["adversarial_file_sha256"],
        "adversarial_audit_payload_sha256": probe["adversarial_payload_sha256"],
        "adversarial_mutation_payload_sha256": probe[
            "adversarial_mutation_payload_sha256"
        ],
        "derived_anchor_count": probe["anchors"],
        "anchor_count": probe["anchors"],
        "input_anchor_row_hash_root": probe_input["anchor_row_hash_root"],
        "producer_anchor_row_hash_root": probe["producer_anchor_row_hash_root"],
        "input_contract_payload_sha256": probe_input["contract_payload_sha256"],
        "one_port": {
            "raw_pair_count": PROBE_INPUT_FIRST_PAIRS,
            "category_counts": PROBE_ONE_PORT_COUNTS,
            "equality_survivor_count": PROBE_ONE_PORT_EQUALITIES,
            "ledger_sha256": probe["one_port"]["ledger_sha256"],
            "ordered_row_hash_root": probe["one_port"]["ordered_row_hash_root"],
        },
        "two_port": {
            "parent_count": PROBE_ONE_PORT_EQUALITIES,
            "parent_inventory_sha256": probe["two_port_parent_inventory_sha256"],
            "parent_inventory_hash_root": probe[
                "two_port_parent_inventory_hash_root"
            ],
            "raw_pair_count": PROBE_TWO_PORT_PAIRS,
            "category_counts": PROBE_TWO_PORT_COUNTS,
            "equality_survivor_count": PROBE_TWO_PORT_EQUALITIES,
            "ledger_sha256": probe["two_port"]["ledger_sha256"],
            "ordered_row_hash_root": probe["two_port"]["ordered_row_hash_root"],
            "reversed_marginals_checked": PROBE_TWO_PORT_EQUALITIES,
            "reversed_marginals_missing": 0,
        },
        "total_raw_pair_count": PROBE_TOTAL_PAIRS,
        "aggregate_category_counts": PROBE_AGGREGATE_COUNTS,
        "aggregate_raw_id_hash_root": probe["aggregate_raw_id_hash_root"],
        "aggregate_row_hash_root": probe["aggregate_raw_id_hash_root"],
        "derived_equality_relation_count": PROBE_TOTAL_EQUALITIES,
        "equality_relation_count": PROBE_TOTAL_EQUALITIES,
        "equality_relation_id_hash_root": probe["equality_relation_id_hash_root"],
        "exact_transport_registry": probe["transport_registry"],
        "parent_restriction_registry": probe["restriction_registry"],
        "separation_registry_file_sha256": probe[
            "separation_registry_file_sha256"
        ],
        "separation_registry_payload_sha256": probe[
            "separation_registry_payload_sha256"
        ],
        "site_partition_payload_sha256": probe["site_partition_payload_sha256"],
        "all_restrictions_from_one_fixed_full_containment": True,
        "fixed_full_containment_audit_payload_sha256": probe[
            "adversarial_payload_sha256"
        ],
        "missing_anchors": 0,
        "missing_equality_relations": 0,
        "multiple_parent_links": 0,
        "unresolved": 0,
        "incoherent": 0,
        "broken_transports": 0,
        "rooted_reason_count": 0,
        "mixed_isomorphic_deck_failures": 0,
        "edge_count": PROBE_TOTAL_EQUALITIES,
        "transport_restrictions_replayed": PROBE_TOTAL_EQUALITIES,
        "root_movement_or_internal_core_arc_restrictions_replayed": PROBE_TOTAL_EQUALITIES,
        "parent_child_edge_hash_root": probe[
            "equality_parent_child_edge_hash_root"
        ],
        "transport_restriction_hash_root": probe[
            "equality_transport_restriction_hash_root"
        ],
    }

    certificate = {
        "schema": "k2p-corrected-finite-universe-release-v2",
        "status": "PASS",
        "scope": "principal_D_plus",
        "artifact_sha256": artifact_sha256,
        "artifact_binding_contract": {
            "acyclic": True,
            "excluded_downstream_roles": sorted(DOWNSTREAM_ROLES),
            "locator_binds_certificate_and_downstream_reports": True,
        },
        "families": families,
        "restoration_forest": forest,
        "probe_coherence": probe_coherence,
        "source_tree_fingerprint_sha256": sha_object(artifact_sha256),
        "unresolved": 0,
        "rooted_reason_count": 0,
    }
    certificate["payload_sha256"] = sha_object(certificate)
    return certificate


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
        raise SystemExit("CORRECTED_UNIVERSE_BUILD_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    certificate = compose_certificate()
    write_json_atomic(args.output, certificate)
    print(
        json.dumps(
            {
                "status": "PASS",
                "payload_sha256": certificate["payload_sha256"],
                "families": sorted(certificate["families"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
