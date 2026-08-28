#!/usr/bin/env python3
"""Fail-closed integrated mathematical gate for the K3P-SAME theorem.

The ordinary certification path freshly invokes the independent proof-family
verifiers and then reconstructs the logical implication to K3P-SAME from their
sealed artifacts.  ``--artifact-only`` performs the same cross-binding and
logical checks without executing the expensive replays; it exists solely for
the isolated top-level mutation suite.

This gate certifies a mathematical classification.  It does not certify a
manuscript, PDF, release archive, journal submission, DOI, license, peer
review, or human author review.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent
DEFAULT_PROJECT = HERE.parent
DEFAULT_REPORT = HERE / "K3P_SAME_CLASSIFICATION_GATE_REPORT.json"

EXPECTED_CUT_BOUNDARY = {
    "conclusion": "Cut(N)=Cut(Nprime)_under_source_relative_containment_in_the_strong_class",
    "strong_class_cut_transfer": "PROVED",
    "universal_pointwise_K3P_cut_recovery": "WITHDRAWN_NOT_USED",
}
EXPECTED_ONE = {
    "displayed_quartet_mismatch": 27_758,
    "isomorphic": 1_915,
    "k3p_tree_sunlet_sos": 99,
    "triangle": 192,
}
EXPECTED_TWO = {
    "displayed_quartet_mismatch": 511_266,
    "isomorphic": 30_969,
    "k3p_tree_sunlet_sos": 576,
    "triangle": 1_760,
}
EXPECTED_RESTORATION_COUNTS = {
    "minimal_k3p_terminal_rows": 36_568,
    "legacy_full_forest_leaves": 36_792,
    "legacy_structural_continuations": 32,
    "redundant_depth2_edges": 256,
    "active_k3p_continuations": 0,
}
EXPECTED_POLYNOMIAL_ORBITS = {
    "H21-01", "H21-03", "H21-04", "H21-05", "H21-06",
    "L20-01", "L21a-01", "L21b-01", "L23-02",
}
EXPECTED_RANK_ORBITS = {
    "H21-02", "L20-02", "L21a-02", "L21b-02", "L23-01",
}
EXPECTED_CUT_TOPOLOGY_SHA256 = (
    "edbd4afe566ed0ed5d1c518ffe5b21f8f224d547b9c351cb4e1a8c1c613ac086"
)
EXPECTED_SEMANTIC_PROBE_MUTATIONS = {
    "coherently_resealed_nonincidence_transport",
    "coherently_resealed_wrong_marginal_label",
    "coherently_resealed_false_quartet",
    "coherently_resealed_false_six_circuit_deck",
    "coherently_resealed_incomplete_site_profile",
    "altered_transport_restriction_claim",
    "mixed_sign_Bernstein_polynomial",
}
EXPECTED_FULL_FOUR_PORT_MUTATIONS = {
    "coherent_raw_omission",
    "coherent_isomorphic_triangle_reclassification",
    "coherent_restoration_quadratic_reclassification",
    "coefficientwise_upper_rank_forgery",
    "coherent_quotient_orbit_omission",
    "optimized_mode",
}
EXPECTED_NON_FOUR_ANCHOR_MUTATIONS = {
    "omit_tree_seed",
    "omit_cycle_restored_seed",
    "omit_theta2_k5_seed",
    "omit_theta2_k6_seed",
    "cycle_triangle_relabelled_isomorphic",
    "theta2_source_graph_hash_replaced",
    "theta2_k7_restoration_path_folded",
    "theta2_restored_role_forged",
    "bogus_anchor_appended",
    "incoming_boundary_partition_reclassified",
    "theta2_base_stage_omitted",
    "four_raw_equality_parent_omitted_after_rebinding",
    "used_one_port_equality_status_corrupted_after_rebinding",
    "used_two_port_status_corrupted_after_rebinding",
    "extra_terminal_descendant_identity_corrupted_after_rebinding",
    "optimized_mode",
}
EXPECTED_INTEGRATED_MUTATIONS = {
    "omit_balanced_noncut_word",
    "omit_non_four_anchor_in_complete_crosswalk",
    "admit_unmatched_marginalized_incoming_path",
    "substitute_universal_pointwise_cut_rank_iff",
    "promote_ordinary_triangle_to_rank_15",
    "claim_ambient_open_triangle_germ",
    "allow_proper_directed_containment_inside_strong_class",
    "drop_coherent_boundary_transports",
    "weaken_all_n_sharpness_nontriangle_scope",
    "restore_pending_v1_probe_restoration_manifest",
    "conflate_minimal_terminals_with_legacy_leaves",
    "activate_legacy_restoration_continuation",
    "make_restoration_replay_import_producer",
    "reactivate_historical_k2p_restoration_algebra",
    "impose_k2p_sector_equality_in_restoration",
    "drift_standalone_restoration_hash",
    "accept_restoration_mutation_and_reduce_count",
    "omit_one_semantic_probe_row",
    "accept_one_coherent_semantic_probe_mutation",
    "semantic_probe_case_survives_behind_pass_summary",
    "omit_one_graph_derived_cut_topology_row",
    "omit_one_full_four_port_row_with_resealed_reports",
    "reclassify_full_four_port_row_with_resealed_reports",
    "delete_continuous_time_specialization_bridge",
    "reverse_ct_to_principal_necessity_transfer",
    "claim_submission_ready_without_publication_engineering",
    "optimized_python_bypass",
}
EXPECTED_FULL_FOUR_PORT_RAW_CATEGORIES = {
    "topology_excluded": 377_382,
    "rank_excluded": 23_054,
    "quadratic_separated": 1_968,
    "h14_marginal_separated": 88,
    "restoration_obligation": 2_540,
    "isomorphic": 30,
    "ordinary_triangle": 114,
    "post_quadratic_residue": 40,
}
NONMATHEMATICAL_GATES = [
    "clean quick/full/full-regeneration replay and release-ledger rebinding",
    "clean-room release archive and checksum engineering after the replay",
    "journal submission-format and metadata package engineering",
]


class GateFailure(RuntimeError):
    pass


def require(condition: bool, label: object) -> None:
    if not condition:
        raise GateFailure(str(label))


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load(project: Path, relative: str) -> dict:
    path = (project / relative).resolve()
    try:
        path.relative_to(project.resolve())
    except ValueError as error:
        raise GateFailure(("path resolves outside project", relative)) from error
    require(path.is_file(), ("missing artifact", relative))
    value = json.loads(path.read_text())
    require(isinstance(value, dict), ("JSON object required", relative))
    return value


def verify_payload(value: dict, label: str, exclude: tuple[str, ...] = ()) -> str:
    claimed = value.get("payload_sha256")
    body = dict(value)
    body.pop("payload_sha256", None)
    for field in exclude:
        body.pop(field, None)
    observed = sha_object(body)
    require(claimed == observed, (label, "payload SHA-256", claimed, observed))
    return observed


def verify_file_binding(project: Path, relative: str, expected: str) -> dict:
    path = (project / relative).resolve()
    try:
        path.relative_to(project.resolve())
    except ValueError as error:
        raise GateFailure(("bound path resolves outside project", relative)) from error
    require(path.is_file(), ("missing bound file", relative))
    actual = sha_file(path)
    require(actual == expected, ("file hash", relative, expected, actual))
    return {"path": relative, "sha256": actual}


def bind(project: Path, relative: str, value: dict | None = None) -> dict:
    path = project / relative
    record = {"path": relative, "sha256": sha_file(path)}
    if value is not None:
        if "schema" in value:
            record["schema"] = value["schema"]
        if "status" in value:
            record["status"] = value["status"]
        if "payload_sha256" in value:
            record["payload_sha256"] = value["payload_sha256"]
    return record


def gzip_binding(path: Path) -> dict:
    with gzip.open(path, "rb") as handle:
        payload = handle.read()
    return {
        "sha256": sha_file(path),
        "uncompressed_sha256": hashlib.sha256(payload).hexdigest(),
        "uncompressed_bytes": len(payload),
    }


def validate_primary(project: Path, bindings: dict) -> None:
    relative = "reproducibility/primary_gate_report.json"
    report = load(project, relative)
    require(report.get("schema") == "k3p-primary-gate-report-v1", "primary schema")
    require(report.get("overall_status") == "PASS", "primary status")
    require(report.get("counts") == {"PASS": 28, "BLOCKED": 0, "FAIL": 0}, "primary 28/28")
    input_binding = report.get("input_binding", {})
    require(input_binding.get("status") == "PASS" and
            input_binding.get("file_count") == 31 and
            input_binding.get("mismatches") == [], "primary immutable-input binding")
    gates = report.get("gates", [])
    require([row.get("item") for row in gates] == list(range(1, 29)), "primary gate ordering")
    require(all(row.get("status") == "PASS" for row in gates), "primary non-PASS item")
    item6 = gates[5]
    require(item6.get("claim") == "Strong-class containment cut transfer", "primary item 6 scope")
    qualification = item6.get("qualification") or ""
    require("universal arbitrary-network pointwise" in qualification and
            "withdrawn and not used" in qualification, "primary item 6 claim boundary")
    for path, expected in report.get("active_verifier_hashes", {}).items():
        verify_file_binding(project, path, expected)
    for path, expected in report.get("generated_evidence_sha256", {}).items():
        verify_file_binding(project, path, expected)
    auxiliary = report.get("auxiliary_replays", {})
    require(auxiliary.get("strong_class_cut_transfer", {}).get("status") == "PASS",
            "primary cut replay")
    require(auxiliary["strong_class_cut_transfer"].get("claim_boundary") == EXPECTED_CUT_BOUNDARY,
            "primary cut boundary")
    require(auxiliary["strong_class_cut_transfer"].get(
        "universal_pointwise_K3P_cut_recovery_used") is False,
        "primary universal pointwise substitution")
    require(auxiliary.get("corrected_four_port_transport", {}).get("status") == "PASS",
            "primary four-port replay")
    require(auxiliary.get("independent_sharpness", {}).get("status") == "PASS",
            "primary Krawczyk replay")
    require(auxiliary.get("independent_topology_all_n", {}).get("status") == "PASS",
            "primary all-n replay")
    bindings[relative] = bind(project, relative, report)


def validate_four_port(project: Path, bindings: dict) -> None:
    audit_path = "clean_room/H21_01_TRANSPORT_AUDIT.json"
    audit = load(project, audit_path)
    census = audit.get("census", {})
    require(audit.get("status") == "PASS" and audit.get("exact_remaining_gaps_within_scope") == [],
            "clean-room audit status")
    require(census.get("canonical_orbits") == 14, "four-port orbit count")
    require(census.get("raw_orbit_members") == 38, "four-port raw-member count")
    require(census.get("prelock_sink_swaps") == 2, "four-port sink-swap count")
    require(census.get("transported_h14_quartics") == 5 and
            census.get("remaining_exact_quartics") == 4 and
            census.get("directed_rank_obstructions") == 5, "four-port proof partition")

    mutations_path = "clean_room/CLEAN_ROOM_MUTATION_RESULTS.json"
    mutations = load(project, mutations_path)
    require(mutations.get("schema") == "k3p-clean-room-mutation-results-v2" and
            mutations.get("status") == "PASS", "clean-room mutation status")
    require(mutations.get("mutation_count") == mutations.get("rejected_mutations") == 10 and
            mutations.get("accepted_mutations") == 0 and mutations.get("control_count") == 2,
            "clean-room mutation census")

    hardened_path = "clean_room/adversarial/HARDENED_H21_REAUDIT.json"
    hardened = load(project, hardened_path)
    verdict = hardened.get("verdict", {})
    accounting = hardened.get("accounting", {})
    require(hardened.get("status") == "PASS_ZERO_REMAINING_HARDENING_GAPS" and
            hardened.get("exact_remaining_gaps") == [], "hardened H21 status")
    require(accounting.get("ordinary_mutations_rejected") == 25 and
            accounting.get("optimized_controls_rejected") == 3 and
            accounting.get("active_files_byte_mutated") == 5 and
            accounting.get("rank_upper_bounds_independently_reconstructed") == 5,
            "hardened H21 accounting")
    require(verdict == {
        "H21_mathematical_transport": "PASS",
        "active_input_hash_binding": "PASS",
        "certificate_skip_control": "PASS_FAIL_CLOSED",
        "full_fourteen_orbit_and_two_sink_gate": "PASS",
        "optimized_python_fail_closed": "PASS",
        "port_incoming_repair_raw_binding": "PASS",
        "rank_minor_dimension_binding": "PASS",
        "remaining_blockers": 0,
        "target_rank_upper_bound_reconstruction": "PASS_NONCIRCULAR",
    }, "hardened H21 verdict")
    verifier_path = "clean_room/verify_h21_transport_and_fourteen_orbits.py"
    verify_file_binding(project, verifier_path,
                        hardened["audited_hashes"]["final_hardened_verifier"])
    for record in hardened.get("active_input_hashes", []):
        verify_file_binding(project, "input_frozen/k3p_cloud_artifacts/" + record["filename"],
                            record["sha256"])

    primary_path = "four_port_atlas/primary_exact_evidence.json"
    primary = load(project, primary_path)
    require(primary.get("raw_transport_gate") == "PASS" and
            primary.get("accounting_numerically_consistent") is True and
            primary.get("accounting_classification_certified_by_this_module") is True,
            "primary four-port status")
    transport = primary.get("primary_root_suppressed_mixed_transport", {})
    require(transport.get("canonical_orbits") == 14 and
            transport.get("raw_orbit_members") == 38 and
            transport.get("all_double_cosets_reconstructed") is True and
            transport.get("all_literal_fourier_coordinate_transports_exact") is True,
            "primary four-port transport")
    polynomial = {row["orbit_id"] for row in primary.get("polynomial_separators", [])}
    ranks = {row["orbit_id"] for row in primary.get("directed_rank_separators", [])}
    require(polynomial == EXPECTED_POLYNOMIAL_ORBITS, "nine polynomial orbit separators")
    require(ranks == EXPECTED_RANK_ORBITS, "five directed-rank orbit separators")
    require(len(primary.get("prelock_sink_swap_separators", [])) == 2, "two sink swaps")
    require(polynomial.isdisjoint(ranks) and len(polynomial | ranks) == 14,
            "four-port complete disjoint partition")
    for relative, value in ((audit_path, audit), (mutations_path, mutations),
                            (hardened_path, hardened), (primary_path, primary)):
        bindings[relative] = bind(project, relative, value)


def validate_full_four_port_universe(project: Path, bindings: dict) -> None:
    base = "four_port_atlas/full_universe_replay"
    artifact_base = f"{base}/artifacts"
    summary_path = f"{artifact_base}/FULL_FOUR_PORT_REPLAY.json"
    summary = load(project, summary_path)
    claimed = summary.get("payload_sha256_without_hash")
    summary_body = dict(summary)
    summary_body.pop("payload_sha256_without_hash", None)
    require(claimed == sha_object(summary_body), "full four-port summary payload")
    require(summary.get("schema") == "k3p-full-four-port-universe-replay-v2",
            "full four-port summary schema")
    require(summary.get("scope") == {
        "starts_from_primitive_graph_grammar": True,
        "reads_frozen_fourteen_orbit_lock": False,
        "reads_frozen_companion_raw_ledger": False,
        "reads_missing_cloud_descriptor_corpus": False,
        "rank_note": (
            "Exact nonzero Jacobian minors are regenerated for every literal map; "
            "target upper-rank binding is verified independently by the verifier."
        ),
    }, "full four-port authority boundary")

    producer_path = f"{base}/generate_full_four_port_replay.py"
    core_path = f"{base}/independent_replay_core.py"
    verifier_path = f"{base}/verify_full_four_port_replay.py"
    mutation_runner_path = f"{base}/test_full_four_port_mutations.py"
    atlas_path = "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py"
    require(summary.get("bindings") == {
        "atlas_path": atlas_path,
        "atlas_sha256": sha_file(project / atlas_path),
        "producer_sha256": sha_file(project / producer_path),
    }, "full four-port producer bindings")
    require(summary.get("primitive_counts") == {
        "sources": 6,
        "selected_incoming_targets": 831,
        "marginalized_incoming_targets": 1_983,
        "targets": 2_814,
        "port_permutations": 24,
        "raw_total": 405_216,
        "post_topology": 27_834,
        "compatible_target_permutation_keys": 13_686,
        "unique_map_descriptors_including_sources": 4_379,
    }, "full four-port primitive census")
    require(summary.get("raw_category_counts") ==
            EXPECTED_FULL_FOUR_PORT_RAW_CATEGORIES,
            "full four-port exact raw partition")
    require(sum(summary["raw_category_counts"].values()) == 405_216,
            "full four-port raw partition sum")
    require(summary.get("class_member_category_counts") == {
        "h14_marginal_separated": 32,
        "isomorphic": 24,
        "ordinary_triangle": 69,
        "post_quadratic_residue": 40,
        "quadratic_separated": 1_193,
        "restoration_obligation": 997,
    } and summary.get("eligible_map_class_count") == 2_355,
            "full four-port class partition")
    require(summary.get("rank_upper_certificate_count") == 3_064 and
            summary.get("rank_upper_mechanism") ==
            "coefficientwise multilinear polynomial vector fields J_f V=0" and
            summary.get("source_ranks") == [20, 21, 21, 21, 23, 24],
            "full four-port exact rank evidence")
    require(summary.get("residue_quotient") == {
        "post_quadratic_raw_records": 40,
        "raw_records_in_fourteen_orbits": 38,
        "separate_sink_swap_records": 2,
        "canonical_orbits": 14,
    }, "full four-port derived quotient")

    expected_artifacts = {
        "DERIVED_RESIDUE_QUOTIENT.json",
        "eligible_class_registry.json.gz",
        "exact_rank_minor_registry.json.gz",
        "exact_rank_upper_registry.json.gz",
        "full_directional_ledger.jsonl.gz",
    }
    artifacts = summary.get("artifacts", {})
    require(set(artifacts) == expected_artifacts, "full four-port artifact set")
    for name in sorted(expected_artifacts):
        relative = f"{artifact_base}/{name}"
        path = project / relative
        require(path.is_file(), ("missing full four-port artifact", relative))
        expected = artifacts[name]
        if name.endswith(".gz"):
            require(gzip_binding(path) == expected,
                    ("full four-port gzip binding", name))
        else:
            require(expected == {"sha256": sha_file(path), "bytes": path.stat().st_size},
                    ("full four-port plain binding", name))
        bindings[relative] = bind(project, relative)

    report_path = f"{base}/INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json"
    report = load(project, report_path)
    verify_payload(report, "full four-port independent replay", ("operational",))
    require(report.get("schema") == "k3p-full-four-port-independent-verification-v1" and
            report.get("status") == "PASS", "full four-port independent replay status")
    require(report.get("independence") == {
        "producer_imported": False,
        "historical_atlas_core_imported": False,
        "frozen_fourteen_orbit_lock_read": False,
        "primitive_graph_grammar_reconstructed": True,
    }, "full four-port independent replay boundary")
    require(report.get("counts") == {
        "raw": 405_216,
        "post_topology": 27_834,
        "compatible_target_permutation_keys": 13_686,
        "unique_map_descriptors": 4_379,
        "residue": 40,
        "orbit_members": 38,
        "sink_swaps": 2,
        "canonical_orbits": 14,
        "restoration_presentations": 2_540,
        "restoration_canonical_classes": 997,
        "restoration_first_children": 36_568,
        "probe_four_port_anchors": 43,
    }, "full four-port independent replay census")
    report_bindings = report.get("bindings", {})
    require(report_bindings == {
        "independent_verifier_sha256": sha_file(project / verifier_path),
        "independent_core_sha256": sha_file(project / core_path),
        "mutation_runner_sha256": sha_file(project / mutation_runner_path),
        "producer_sha256": sha_file(project / producer_path),
        "summary_sha256": sha_file(project / summary_path),
        "artifacts": artifacts,
    }, "full four-port independent replay file bindings")
    require(report.get("verified_summary_payload_sha256") == claimed,
            "full four-port summary/replay payload binding")
    rank_proof = report.get("syzygy_rank_upper_proof", {})
    require("coefficient by coefficient" in rank_proof.get("coefficientwise_identity", "") and
            "rank([A;E])-rank(A)" in rank_proof.get("linear_algebra_identity", "") and
            "never as an upper bound" in rank_proof.get("generic_open_argument", ""),
            "full four-port rank-upper proof boundary")

    mutation_path = f"{base}/FULL_FOUR_PORT_MUTATION_REPORT.json"
    mutation = load(project, mutation_path)
    verify_payload(mutation, "full four-port coherent mutations", ("operational",))
    rows = mutation.get("mutations", [])
    require(mutation.get("schema") == "k3p-full-four-port-coherent-mutations-v1" and
            mutation.get("status") == "PASS" and mutation.get("rejected") == 6 and
            mutation.get("survived") == 0 and len(rows) == 6 and
            {row.get("name") for row in rows} == EXPECTED_FULL_FOUR_PORT_MUTATIONS and
            all(row.get("rejected") is True and row.get("expected_failure")
                for row in rows), "full four-port coherent mutation gate")
    require(mutation.get("verifier_sha256") == sha_file(project / verifier_path) and
            mutation.get("core_sha256") == sha_file(project / core_path),
            "full four-port mutation code bindings")

    for relative, value in ((summary_path, summary), (report_path, report),
                            (mutation_path, mutation)):
        bindings[relative] = bind(project, relative, value)
    for relative in (producer_path, core_path, verifier_path, mutation_runner_path):
        bindings[relative] = bind(project, relative)


def validate_anchor_universe(project: Path, bindings: dict) -> None:
    base = "anchor_universe"
    artifact_path = f"{base}/artifacts/NON_FOUR_ANCHOR_UNIVERSE.json"
    artifact = load(project, artifact_path)
    verify_payload(artifact, "non-four anchor producer", ("operational",))
    require(
        artifact.get("schema") == "k3p-model-independent-non-four-anchor-universe-v1"
        and artifact.get("status") == "PASS",
        "non-four anchor producer status",
    )
    expected_census = {
        "total": 133,
        "by_origin": {
            "cycle_physical_k3": 24,
            "cycle_restored_physical_k4": 12,
            "theta2_physical_k5": 24,
            "theta2_physical_k6": 40,
            "theta2_physical_k7": 32,
            "tree_physical_k3": 1,
        },
        "by_relation": {"isomorphic": 117, "triangle": 16},
        "by_port_count": {"3": 25, "4": 12, "5": 24, "6": 40, "7": 32},
    }
    require(artifact.get("census") == expected_census, "non-four anchor census")
    require(artifact.get("stage_counts") == {
        "cycle_base_presentations": 13_440,
        "cycle_restoration_presentations": 536_364,
        "theta2_base_presentations": 2_946_240,
        "theta2_six_port_children": 576,
        "theta2_seven_port_children": 288,
    }, "non-four anchor raw enumeration census")
    anchors = artifact.get("anchors")
    require(isinstance(anchors, list) and len(anchors) == 133 and
            len({row.get("anchor_key") for row in anchors}) == 133,
            "non-four anchor rows and keys")
    producer_path = f"{base}/generate_non_four_anchor_universe.py"
    atlas_path = "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py"
    require(artifact.get("bindings") == {
        "producer_sha256": sha_file(project / producer_path),
        "k3p_atlas_sha256": sha_file(project / atlas_path),
    }, "non-four producer code bindings")
    boundary = artifact.get("claim_boundary", {})
    forbidden = boundary.get("forbidden_and_unused", [])
    require(boundary.get("excluded_marginalized_incoming_parents") == 176 and
            "frozen 176-anchor contract as an enumeration input" in forbidden and
            "K2P polynomial compilation" in forbidden,
            "non-four producer premise boundary")

    independent_path = f"{base}/INDEPENDENT_NON_FOUR_VERIFICATION.json"
    independent = load(project, independent_path)
    verify_payload(independent, "independent non-four anchors", ("operational",))
    require(independent.get("schema") ==
            "k3p-independent-non-four-anchor-universe-verification-v1" and
            independent.get("status") == "PASS",
            "independent non-four verifier status")
    require(independent.get("artifact") == {
        "path": artifact_path,
        "sha256": sha_file(project / artifact_path),
        "schema": artifact["schema"],
        "payload_sha256": artifact["payload_sha256"],
    }, "independent non-four artifact binding")
    independence = independent.get("independence_boundary", {})
    require(independence.get("derivation_completed_before_artifact_read") is True and
            independence.get("contract_reads") == 0 and
            independence.get("frozen_theta_or_cycle_artifact_reads") == 0 and
            independence.get("producer_or_atlas_imports") == 0 and
            independence.get("producer_imports") == 0 and
            independence.get("submitted_atlas_imports") == 0,
            "independent non-four premise boundary")
    comparisons = independent.get("comparisons", {})
    require(comparisons.get("semantic_rows") == 133 and
            all(comparisons.get(field) is True for field in (
                "semantic_key_set_equal", "every_row_body_equal",
                "every_source_graph_hash_equal", "every_target_graph_hash_equal",
                "census_equal",
            )) and comparisons.get("ordered_anchor_key_sha256") ==
            artifact.get("ordered_anchor_key_sha256"),
            "independent non-four rowwise comparison")
    root_movement = independent.get(
        "marginalized_incoming_root_movement_certificate", {}
    )
    mapping_rows = root_movement.get("mapping_rows")
    require(root_movement.get("incoming_boundary_mismatch_parents") == 176 and
            root_movement.get("dummy_multiplicity") == {"1": 56, "2": 88, "3": 32} and
            root_movement.get("terminal_paths_by_restoration_depth") ==
            {"1": 56, "2": 176, "3": 192} and
            root_movement.get("mapped") == 424 and
            root_movement.get("unmatched") == 0 and
            root_movement.get("canonical_seed_class_count") == 15 and
            root_movement.get("prefix_exact_equality_checks") == 984 and
            isinstance(mapping_rows, list) and len(mapping_rows) == 424 and
            root_movement.get("mapping_rows_sha256") == sha_object(mapping_rows),
            "marginalized-incoming root-movement certificate")

    reconciliation_path = f"{base}/MARGINALIZED_THETA_ONE_PORT_RECONCILIATION.json"
    reconciliation = load(project, reconciliation_path)
    verify_payload(reconciliation, "marginalized theta one-port reconciliation")
    require(reconciliation.get("schema") ==
            "k3p-marginalized-theta-one-port-reconciliation-v1" and
            reconciliation.get("status") == "PASS",
            "marginalized theta reconciliation status")
    reconciliation_counts = reconciliation.get("reconciliation_census", {})
    require(reconciliation_counts == {
        "marginalized_incoming_abstract_parents": 176,
        "fully_restored_exact_paths": 424,
        "prefix_exact_equality_checks": 984,
        "theta_seed_presentations": 96,
        "canonical_theta_seed_pair_classes": 15,
        "abstract_transported_site_pairs": 66,
        "existing_isomorphic_one_port_rows": 66,
        "canonical_one_port_relation_classes": 66,
        "mapped": 424,
        "unmatched": 0,
    }, "marginalized theta reconciliation census")
    path_rows = reconciliation.get("path_crosswalk")
    site_rows = reconciliation.get("one_port_site_pairs")
    reconciliation_bindings = reconciliation.get("bindings", {})
    require(isinstance(path_rows, list) and len(path_rows) == 424 and
            isinstance(site_rows, list) and len(site_rows) == 66 and
            all(row.get("one_port_relation") == "isomorphic" for row in site_rows) and
            reconciliation_bindings.get("clean_room_mapping_rows_sha256") ==
            root_movement.get("mapping_rows_sha256") and
            reconciliation_bindings.get("path_crosswalk_sha256") == sha_object(path_rows) and
            reconciliation_bindings.get("one_port_site_pair_rows_sha256") ==
            sha_object(site_rows),
            "marginalized theta reconciliation rows")
    for record in reconciliation.get("inputs", {}).values():
        relative = record.get("path")
        require(isinstance(relative, str), "reconciliation input path")
        verify_file_binding(project, relative, record["sha256"])

    crosswalk_path = f"{base}/COMPLETE_ANCHOR_UNIVERSE_CROSSWALK.json"
    crosswalk = load(project, crosswalk_path)
    verify_payload(crosswalk, "complete anchor crosswalk", ("operational",))
    require(crosswalk.get("schema") == "k3p-complete-anchor-universe-crosswalk-v1" and
            crosswalk.get("status") == "PASS",
            "complete anchor crosswalk status")
    require(crosswalk.get("counts") == {
        "non_four_derived_and_crosswalked": 133,
        "four_port_active_and_crosswalked": 43,
        "complete": 176,
        "excluded_marginalized_incoming_parents": 176,
        "excluded_paths_root_movement_mapped": 424,
        "excluded_paths_root_movement_unmatched": 0,
        "excluded_paths_existing_one_port_rows": 66,
        "excluded_paths_existing_one_port_relation_classes": 66,
        "by_origin": {
            "cycle_physical_k3": 24,
            "cycle_restored_physical_k4": 12,
            "four_port_direct_physical": 26,
            "four_port_restored_physical_k5": 17,
            "theta2_physical_k5": 24,
            "theta2_physical_k6": 40,
            "theta2_physical_k7": 32,
            "tree_physical_k3": 1,
        },
        "by_relation": {"isomorphic": 143, "triangle": 33},
        "by_port_count": {"3": 25, "4": 38, "5": 41, "6": 40, "7": 32},
    }, "complete 176-anchor crosswalk census")
    require(crosswalk.get("claim_boundary") == {
        "non_four_enumeration_input":
            "active graph-only producer plus separate no-import verifier",
        "four_port_enumeration_input":
            "literal graph-only replay of all 144 raw equality parents and all 1,356 fixed-full restoration requests, crosswalked through the 26 direct seeds into existing one-/two-port ledgers; the 43 contract rows remain designated serialization rows",
        "contract_role":
            "regression target for the derived 133 non-four rows; designated four-port serialization of 26 direct generators plus 17 physical descendants, not an exhaustive presentation quotient",
        "legacy_theta_cycle_role":
            "opaque locator expansion only after the derived 133-row set is fixed",
        "marginalized_incoming_role":
            "the independent verifier maps every one of 424 fully physical restoration paths from 176 excluded parents to a canonical theta seed plus one transported downstream port; zero unmatched",
        "k2p_algebra_active": False,
    }, "complete anchor crosswalk premise boundary")
    cross_bindings = crosswalk.get("bindings", {})
    expected_cross_bindings = {
        "crosswalk_verifier_sha256": sha_file(
            project / f"{base}/verify_complete_anchor_crosswalk.py"
        ),
        "producer_sha256": sha_file(project / artifact_path),
        "producer_payload_sha256": artifact["payload_sha256"],
        "independent_verifier_sha256": sha_file(project / independent_path),
        "root_movement_reconciliation_sha256": sha_file(
            project / reconciliation_path
        ),
        "root_movement_reconciliation_payload_sha256": reconciliation["payload_sha256"],
        "contract_sha256": sha_file(project /
            "input_frozen/model_independent_topology_package/anchor_inputs/probe_input_contract.json"),
        "theta_locator_dictionary_sha256": sha_file(project /
            "input_frozen/model_independent_topology_package/anchor_inputs/fixed_full_restoration_closure.json.gz"),
        "cycle_locator_dictionary_sha256": sha_file(project /
            "input_frozen/model_independent_topology_package/cycle/physical_anchors.json"),
        "four_summary_sha256": sha_file(project /
            "four_port_atlas/full_universe_replay/artifacts/FULL_FOUR_PORT_REPLAY.json"),
        "four_independent_verification_sha256": sha_file(project /
            "four_port_atlas/full_universe_replay/INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json"),
        "four_graph_core_sha256": sha_file(project /
            "four_port_atlas/full_universe_replay/independent_replay_core.py"),
        "four_raw_ledger_sha256": sha_file(project /
            "four_port_atlas/full_universe_replay/artifacts/full_directional_ledger.jsonl.gz"),
        "one_port_manifest_sha256": sha_file(project /
            "probes/ONE_PORT_PROBE_MANIFEST.json"),
        "one_port_ledger_sha256": sha_file(project /
            "probes/one_port_ledger.jsonl.gz"),
        "two_port_manifest_sha256": sha_file(project /
            "probes/TWO_PORT_PROBE_MANIFEST.json"),
        "two_port_parent_inventory_sha256": sha_file(project /
            "probes/two_port_parent_inventory.jsonl.gz"),
        "two_port_ledger_sha256": sha_file(project /
            "probes/two_port_ledger.jsonl.gz"),
    }
    require(cross_bindings == expected_cross_bindings,
            "complete anchor crosswalk file bindings")
    # Promote every file whose bytes are consumed by the crosswalk into the
    # integrated report's explicit binding map.  The crosswalk's semantic hash
    # names are sufficient for its own verifier, but package dependency closure
    # must carry the actual paths as well.
    for relative in (
        "input_frozen/model_independent_topology_package/anchor_inputs/probe_input_contract.json",
        "input_frozen/model_independent_topology_package/anchor_inputs/fixed_full_restoration_closure.json.gz",
        "input_frozen/model_independent_topology_package/cycle/physical_anchors.json",
        "four_port_atlas/full_universe_replay/artifacts/FULL_FOUR_PORT_REPLAY.json",
        "four_port_atlas/full_universe_replay/INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json",
        "four_port_atlas/full_universe_replay/independent_replay_core.py",
        "four_port_atlas/full_universe_replay/artifacts/full_directional_ledger.jsonl.gz",
        "probes/ONE_PORT_PROBE_MANIFEST.json",
        "probes/one_port_ledger.jsonl.gz",
        "probes/TWO_PORT_PROBE_MANIFEST.json",
        "probes/two_port_parent_inventory.jsonl.gz",
        "probes/two_port_ledger.jsonl.gz",
    ):
        bindings.setdefault(relative, bind(project, relative))

    descendant = crosswalk.get("four_port_descendant_completeness", {})
    require(descendant.get("method") == {
        "parent_quotient": (
            "exact labelled arrowhead-preserving isomorphism on each "
            "member of the ordered source/target graph pair"
        ),
        "restoration_grammar": (
            "promote each target dummy role and insert the same new label "
            "on every nonroot source arc not ending at a leaf"
        ),
        "site_transport": (
            "unique mixed-edge image compatible with the exact parent "
            "vertex transport"
        ),
        "algebra_used": False,
    }, "four-port descendant method boundary")
    require(descendant.get("counts") == {
        "raw_equality_parents": 144,
        "raw_isomorphic_parents": 30,
        "raw_triangle_parents": 114,
        "active_map_classes": 93,
        "active_isomorphic_map_classes": 24,
        "active_triangle_map_classes": 69,
        "raw_parent_pair_classes": 9,
        "direct_contract_rows": 26,
        "dummy_parent_roots": 114,
        "dummy_multiplicity": {"0": 30, "1": 60, "2": 42, "3": 12},
        "first_restoration_requests": 1_260,
        "first_unique_one_port_rows": 161,
        "first_isomorphic": 15,
        "first_triangle": 24,
        "first_none": 1_221,
        "physical_k5_equality_terminals": 27,
        "physical_k5_terminal_pair_classes": 15,
        "terminal_isomorphic": 15,
        "terminal_triangle": 12,
        "restored_contract_rows": 17,
        "restored_contract_pair_classes": 11,
        "terminal_presentations_in_contract_pair_classes": 19,
        "additional_terminal_presentations": 8,
        "additional_terminal_pair_classes": 4,
        "equality_continuations": 12,
        "second_restoration_requests": 96,
        "second_unique_two_port_rows": 64,
        "second_none": 96,
        "mapped": 1_356,
        "unmatched": 0,
    }, "four-port descendant completeness census")
    require(descendant.get("ledger_status_counts") == {
        "first": {
            "displayed_quartet_mismatch": 1_080,
            "isomorphic": 15,
            "k3p_tree_sunlet_sos": 141,
            "triangle": 24,
        },
        "second": {
            "displayed_quartet_mismatch": 84,
            "k3p_tree_sunlet_sos": 12,
        },
    }, "four-port descendant ledger census")
    descendant_bindings = descendant.get("bindings", {})
    require(descendant_bindings == {
        "parent_mapping_rows_sha256":
            "843b98d9eda327f35eeb0ba56a807162898515018a39a7e2636c179588eca57e",
        "first_mapping_rows_sha256":
            "f628143b748770596cb48b0732ee78aa6b64f3a2e2af3eda3742f57f5beac154",
        "terminal_crosswalk_sha256":
            "f70acd89dffb682ff768ebef88b9ed45a7e1b719c23136309834b69dcdebd478",
        "second_mapping_rows_sha256":
            "b58cb47e904d8e23947c57def47e4f12d5fd094d770dd5cea91f2e4762109628",
        "omitted_terminal_descendants_sha256":
            "470be793f42f874bd5dccf54717f4937d1c0112454a635292c79ba65d9465c2d",
        "continuation_crosswalk_sha256":
            "ed2803e27a06998a5e38387ab77fefeb3d4a5db2881e1ffc91b9b86b528f300e",
    }, "four-port descendant row commitments")
    additional = descendant.get("additional_terminal_descendants")
    continuations = descendant.get("continuation_crosswalk")
    require(isinstance(additional, list) and len(additional) == 8 and
            sha_object(additional) ==
            descendant_bindings["omitted_terminal_descendants_sha256"] and
            all(row.get("relation") == "triangle" for row in additional),
            "four-port omitted terminals are existing triangle descendants")
    require(isinstance(continuations, list) and len(continuations) == 12 and
            sha_object(continuations) ==
            descendant_bindings["continuation_crosswalk_sha256"] and
            len(descendant.get("continuation_parent_ids", [])) == 8,
            "four-port equality continuation crosswalk")

    mutation_path = f"{base}/NON_FOUR_ANCHOR_MUTATION_REPORT.json"
    mutation = load(project, mutation_path)
    verify_payload(mutation, "non-four anchor mutations", ("operational",))
    cases = mutation.get("cases", [])
    require(mutation.get("schema") == "k3p-non-four-anchor-universe-mutations-v3" and
            mutation.get("status") == "PASS" and
            mutation.get("diagnostic_policy") == {
                "stdout_bytes_excluded_from_payload": True,
                "ephemeral_compressed_bytes_excluded_from_payload": True,
                "rejection_signals_checked_before_sealing": True,
                "mutated_ledgers_committed_logically": True,
            } and
            mutation.get("counts") == {
                "clean_controls": 1, "mutations": 16,
                "rejected": 16, "accepted": 0,
                "preserved_non_four_and_runtime_mutations": 12,
                "coherently_rebound_four_port_semantic_mutations": 4,
            } and len(cases) == 17,
            "anchor-universe mutation census")
    clean = [row for row in cases if row.get("name") == "clean_control"]
    rejected = [row for row in cases if row.get("name") != "clean_control"]
    require(len(clean) == 1 and clean[0].get("expected") == "accept" and
            clean[0].get("observed") == "accept" and
            clean[0].get("returncode") == 0 and
            clean[0].get("validated_sentinel") ==
            "K3P_INDEPENDENT_NON_FOUR_ANCHOR_UNIVERSE_PASS" and
            clean[0].get("four_port_crosswalk_control", {}).get("expected") ==
            "accept" and
            clean[0].get("four_port_crosswalk_control", {}).get("observed") ==
            "accept" and
            clean[0].get("four_port_crosswalk_control", {}).get("returncode") == 0 and
            clean[0].get("four_port_crosswalk_control", {}).get(
                "validated_sentinel") ==
            "K3P_COMPLETE_ANCHOR_UNIVERSE_CROSSWALK_PASS" and
            {row.get("name") for row in rejected} == EXPECTED_NON_FOUR_ANCHOR_MUTATIONS and
            all(row.get("expected") == "reject" and
                row.get("observed") == "reject" and row.get("returncode") != 0
                for row in rejected),
            "non-four anchor mutation cases")

    prohibited_case_keys = {
        "stdout_sha256", "stdout_tail", "manifest_ledger_sha256",
        "manifest_payload_sha256", "four_summary_raw_ledger_sha256",
        "four_verification_summary_sha256",
    }
    observed_case_keys: set[str] = set()
    pending: list[object] = [cases]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            observed_case_keys.update(item)
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
    require(not (prohibited_case_keys & observed_case_keys),
            "non-four mutation payload excludes ephemeral diagnostics")

    semantic_codes = {
        "four_raw_equality_parent_omitted_after_rebinding":
            "FOUR_RAW_EQUALITY_COUNT",
        "used_one_port_equality_status_corrupted_after_rebinding":
            "FOUR_ONE_PORT_EQUALITY_STATUS",
        "used_two_port_status_corrupted_after_rebinding":
            "FOUR_TWO_PORT_NONE_STATUS",
        "extra_terminal_descendant_identity_corrupted_after_rebinding":
            "FOUR_EXTRA_TERMINAL_IDS",
    }
    by_name = {row["name"]: row for row in rejected}
    ordinary_names = EXPECTED_NON_FOUR_ANCHOR_MUTATIONS - set(semantic_codes)
    require(all(by_name[name].get("validated_failure_sentinel") ==
                "K3P_INDEPENDENT_NON_FOUR_ANCHOR_UNIVERSE_FAIL"
                for name in ordinary_names),
            "non-four mutation stable rejection sentinels")
    require(all(by_name[name].get("expected_failure_code") == code and
                by_name[name].get("observed_failure_code") == code
                for name, code in semantic_codes.items()) and
            by_name["optimized_mode"].get("expected_failure_code") ==
            "optimized mode forbidden" and
            by_name["optimized_mode"].get("observed_failure_code") ==
            "optimized mode forbidden",
            "non-four mutation stable failure codes")

    def portable_ledger(record: object, rows: int,
                        status_counts: dict[str, int]) -> bool:
        if not isinstance(record, dict):
            return False
        hashes = (record.get("ordered_hash_root"),
                  record.get("uncompressed_sha256"))
        return (
            record.get("matched") == 1 and record.get("rows") == rows and
            record.get("status_counts") == status_counts and
            isinstance(record.get("uncompressed_bytes"), int) and
            record["uncompressed_bytes"] > 0 and
            all(isinstance(value, str) and len(value) == 64 and
                all(char in "0123456789abcdef" for char in value)
                for value in hashes)
        )

    folded = by_name["omit_tree_seed"].get(
        "folded_four_port_raw_equality_omission", {})
    omission = by_name[
        "four_raw_equality_parent_omitted_after_rebinding"
    ].get("coherent_rebinding", {})
    require(folded.get("omitted_raw_id") == 137124 and
            folded.get("expected_failure_code") == "FOUR_RAW_LEDGER_BINDING" and
            folded.get("observed_failure_code") == "FOUR_RAW_LEDGER_BINDING" and
            folded.get("expected") == folded.get("observed") == "reject" and
            folded.get("returncode") != 0 and
            portable_ledger(folded.get("mutated_ledger"), 405_215, {}) and
            by_name["four_raw_equality_parent_omitted_after_rebinding"].get(
                "omitted_raw_id") == 137124 and
            omission.get("rebound_inputs") == [
                "four_port_replay_summary",
                "independent_four_port_verification",
            ] and omission.get("mutated_ledger") == folded.get("mutated_ledger"),
            "folded four-port omission mutation commitment")

    one = by_name[
        "used_one_port_equality_status_corrupted_after_rebinding"
    ].get("coherent_rebinding", {})
    two = by_name[
        "used_two_port_status_corrupted_after_rebinding"
    ].get("coherent_rebinding", {})
    extra = by_name[
        "extra_terminal_descendant_identity_corrupted_after_rebinding"
    ].get("coherent_rebinding", {})
    require(by_name[
                "used_one_port_equality_status_corrupted_after_rebinding"
            ].get("mutated_key") == ["four:raw154873", 0, 0] and
            one.get("rebound_inputs") == ["one_port_probe_manifest"] and
            portable_ledger(one.get("mutated_ledger"), 29_964, {
                "displayed_quartet_mismatch": 27_758,
                "isomorphic": 1_916,
                "k3p_tree_sunlet_sos": 99,
                "triangle": 191,
            }) and
            by_name[
                "used_two_port_status_corrupted_after_rebinding"
            ].get("mutated_key") == ["P1:four:raw154873:0:0", 0, 6] and
            two.get("rebound_inputs") == ["two_port_probe_manifest"] and
            portable_ledger(two.get("mutated_ledger"), 544_571, {
                "displayed_quartet_mismatch": 511_265,
                "isomorphic": 30_970,
                "k3p_tree_sunlet_sos": 576,
                "triangle": 1_760,
            }) and
            by_name[
                "extra_terminal_descendant_identity_corrupted_after_rebinding"
            ].get("mutated_raw_id") == [202225, 999999999] and
            extra.get("rebound_inputs") == [
                "four_port_replay_summary",
                "independent_four_port_verification",
            ] and portable_ledger(extra.get("mutated_ledger"), 405_216, {}),
            "coherently rebound mutation logical commitments")
    require(mutation.get("bindings") == {
        "mutation_driver_sha256": sha_file(
            project / f"{base}/test_non_four_anchor_mutations.py"
        ),
        "artifact_sha256": sha_file(project / artifact_path),
        "verifier_sha256": sha_file(
            project / f"{base}/verify_non_four_anchor_universe.py"
        ),
        "crosswalk_sha256": sha_file(
            project / f"{base}/verify_complete_anchor_crosswalk.py"
        ),
        "four_raw_ledger_sha256": sha_file(project /
            "four_port_atlas/full_universe_replay/artifacts/full_directional_ledger.jsonl.gz"),
        "four_summary_sha256": sha_file(project /
            "four_port_atlas/full_universe_replay/artifacts/FULL_FOUR_PORT_REPLAY.json"),
        "four_verification_sha256": sha_file(project /
            "four_port_atlas/full_universe_replay/INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json"),
        "one_port_manifest_sha256": sha_file(project /
            "probes/ONE_PORT_PROBE_MANIFEST.json"),
        "one_port_ledger_sha256": sha_file(project /
            "probes/one_port_ledger.jsonl.gz"),
        "two_port_manifest_sha256": sha_file(project /
            "probes/TWO_PORT_PROBE_MANIFEST.json"),
        "two_port_parent_inventory_sha256": sha_file(project /
            "probes/two_port_parent_inventory.jsonl.gz"),
        "two_port_ledger_sha256": sha_file(project /
            "probes/two_port_ledger.jsonl.gz"),
    }, "anchor-universe mutation bindings")

    for relative, value in (
        (artifact_path, artifact),
        (independent_path, independent),
        (reconciliation_path, reconciliation),
        (crosswalk_path, crosswalk),
        (mutation_path, mutation),
    ):
        bindings[relative] = bind(project, relative, value)
    for relative in (
        producer_path,
        f"{base}/independent_non_four_core.py",
        f"{base}/verify_non_four_anchor_universe.py",
        f"{base}/verify_marginalized_theta_one_port_reconciliation.py",
        f"{base}/verify_complete_anchor_crosswalk.py",
        f"{base}/test_non_four_anchor_mutations.py",
        f"{base}/README.md",
        f"{base}/PROOF_BOUNDARY.md",
    ):
        bindings[relative] = bind(project, relative)


def validate_sharpness(project: Path, bindings: dict) -> None:
    manifest_path = "sharpness/K3P_SHARPNESS_REPLAY_MANIFEST.json"
    manifest = load(project, manifest_path)
    require(manifest.get("schema") == "k3p-sharpness-independent-replay-manifest-v1" and
            manifest.get("status") == "PASS", "sharpness replay manifest")
    for record in manifest.get("files", []):
        binding = verify_file_binding(project, record["path"], record["sha256"])
        require((project / record["path"]).stat().st_size == record["bytes"],
                ("sharpness file bytes", record["path"]))
        bindings.setdefault(record["path"], binding)
    conclusion = manifest.get("conclusion", {})
    kraw = conclusion.get("krawczyk", {})
    require(all(kraw.get(field) is True for field in (
        "all_checks_pass", "unique_common_parameter_root_in_box",
        "W_rank_15_throughout_box", "Wprime_rank_15_throughout_box",
        "principal_K3P_domain_throughout_box", "strict_continuous_time_throughout_box",
    )), "sharpness Krawczyk conclusion")
    alln = conclusion.get("topology_all_n", {})
    require(alln.get("all_checks_pass") is True and alln.get("all_n_from") == 3 and
            alln.get("dimension_formula") == "6n-3" and
            alln.get("weak_not_strong_persists") is True and
            alln.get("nontriangle_equivalence_persists") is True and
            alln.get("strict_continuous_time") is True, "sharpness all-n conclusion")

    audit_path = "sharpness/adversarial/SHARPNESS_ADVERSARIAL_AUDIT.json"
    audit = load(project, audit_path)
    verdict = audit.get("verdict", {})
    require(audit.get("schema") == "k3p-sharpness-adversarial-audit-v1", "sharpness audit schema")
    require(verdict.get("mathematical_sharpness_claim") == "PASS" and
            verdict.get("proof_gaps") == [] and audit.get("mutation_failures") == [],
            "sharpness adversarial verdict")
    mutations = audit.get("mutations", {})
    require(len(mutations) == 18 and all(row.get("mutation_detected") is True
            for row in mutations.values()), "sharpness 18 mutations")
    bindings[manifest_path] = bind(project, manifest_path, manifest)
    bindings[audit_path] = bind(project, audit_path, audit)


def validate_cut_topology_regeneration(project: Path, bindings: dict) -> None:
    report_path = (
        "cut_recovery/strong_crossbridge/topology_regeneration/"
        "CUT_TOPOLOGY_REGENERATION_REPORT.json"
    )
    report = load(project, report_path)
    verify_payload(report, "cut topology graph regeneration report")
    require(report.get("schema") == "k3p-cut-topology-graph-regeneration-report-v1" and
            report.get("status") == "PASS", "cut topology graph regeneration status")
    require(report.get("census") == {
        "primitive_cores": 5,
        "endpoint_tensors": 77,
        "four_port_tensors": 72,
        "strict_wrong_split_certificates": 204,
        "endpoint_failures": 0,
        "one_active_failures": 0,
        "switching_compression_survivors": 0,
    }, "cut topology graph regeneration census")
    candidate = report.get("fresh_candidate", {})
    downstream = report.get("bound_downstream_input", {})
    require(candidate == {
        "bytes": 2_520_452,
        "sha256": EXPECTED_CUT_TOPOLOGY_SHA256,
    }, "cut topology fresh-candidate binding")
    require(downstream == {
        "path": "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json",
        "bytes": 2_520_452,
        "sha256": EXPECTED_CUT_TOPOLOGY_SHA256,
        "byte_identical_to_fresh_candidate": True,
    }, "cut topology downstream-input binding")
    verify_file_binding(project, downstream["path"], downstream["sha256"])
    programs = report.get("active_programs", {})
    require(set(programs) == {
        "cut_recovery/strong_crossbridge/topology_regeneration/generate_cut_topology.py",
        "cut_recovery/strong_crossbridge/topology_regeneration/verify_cut_topology_regeneration.py",
        "cut_recovery/strong_crossbridge/topology_regeneration/test_cut_topology_regeneration_mutations.py",
        "cut_recovery/strong_crossbridge/topology_regeneration/verify_all.sh",
    }, "cut topology active-program set")
    for relative, expected in programs.items():
        bindings.setdefault(relative, verify_file_binding(project, relative, expected))
    bindings[downstream["path"]] = bind(project, downstream["path"])
    bindings[report_path] = bind(project, report_path, report)


def validate_noncut_witness_evidence(project: Path, bindings: dict) -> None:
    base = "cut_recovery/strong_crossbridge/palette_independent"
    reduction_path = f"{base}/BALANCED_WORD_REDUCTION_CERTIFICATE.json"
    reduction = load(project, reduction_path)
    require(
        reduction.get("schema") == "stc-jc-cut-palette-reduction-v1"
        and reduction.get("status") == "EXACTLY COMPUTED"
        and reduction.get("failure_count") == 0
        and reduction.get("totals") == {
            "balanced_total": 808_642,
            "direct_palette": 544_350,
            "singleton_doubled_palette": 34_304,
            "three_run_path_obstruction": 229_988,
        }
        and len(reduction.get("mutation_results", [])) == 3
        and all(row.get("rejected") is True
                for row in reduction["mutation_results"]),
        "balanced noncut-word reduction evidence",
    )
    palette_path = f"{base}/REDUCED_PALETTE_CLEANROOM_CERTIFICATE.json"
    palette = load(project, palette_path)
    require(
        palette.get("schema") == "stc-jc-reduced-palette-cleanroom-v1"
        and palette.get("status") == "EXACTLY COMPUTED"
        and palette.get("total_valid_palette_presentations") == 379_742
        and palette.get("survivor_count") == 0
        and palette.get("failures") == [],
        "clean-room reduced noncut palette evidence",
    )
    for relative in (
        reduction_path,
        palette_path,
        f"{base}/enumerate_balanced_word_reduction.py",
        f"{base}/verify_reduced_palette_cleanroom.py",
        f"{base}/verify_cut_combinatorics.py",
        f"{base}/verify_displayed_tree_minor.py",
        f"{base}/README.md",
    ):
        bindings[relative] = bind(project, relative)


def validate_cut_transfer(project: Path, bindings: dict) -> None:
    gate_path = "reproducibility/strong_class_cut_transfer_gate_report.json"
    gate = load(project, gate_path)
    require(gate.get("schema") == "k3p-strong-class-cut-transfer-active-gate-v1" and
            gate.get("status") == "PASS" and gate.get("remaining_gaps") == [],
            "cut-transfer active gate")
    require(gate.get("claim_boundary") == EXPECTED_CUT_BOUNDARY,
            "universal pointwise cut-rank iff substitution rejected")
    require(gate.get("universal_pointwise_K3P_cut_recovery_used") is False,
            "universal pointwise cut theorem used")
    fresh = gate.get("fresh_release_replays", {})
    for mode, optimized in (("ordinary", False), ("optimized", True)):
        summary = fresh.get(mode, {}).get("summary", {})
        require(summary == {
            "status": "PASS", "directions": 204, "tree_colorings": 19_270,
            "adversarial_mutations": 32, "python_optimized": optimized,
        }, ("cut release mode", mode))
    require(gate.get("producer_summary", {}).get("direction_count") == 204,
            "cut producer universe")
    require(gate.get("adversarial_summary") == {
        "direction_count": 204,
        "manifest_rows_checked": 7,
        "mutation_count": 32,
        "side_blob_switching_components": 7,
        "tree_colorings_checked": 19_270,
        "tree_counterexamples": 0,
    }, "cut adversarial replay")
    theorem_binding = gate.get("theorem_manifest", {})
    verify_file_binding(project, theorem_binding["path"], theorem_binding["sha256"])
    theorem = load(project, theorem_binding["path"])
    require(theorem.get("status") == "PASS", "cut theorem manifest")
    require(theorem.get("independent_adversarial_audit", {}).get("claim_boundary") ==
            EXPECTED_CUT_BOUNDARY, "cut theorem boundary")
    noncircularity = theorem.get("noncircularity", {})
    require(noncircularity.get("common_bridge_tree_assumed") is False and
            noncircularity.get("bridge_tree_equality_assumed") is False and
            noncircularity.get("fourteen_orbit_classification_imported") is False and
            noncircularity.get("target_open_marginal_assumed") is False and
            noncircularity.get("target_regular_point_assumed") is False,
            "cut-transfer circularity")

    mutation_path = "reproducibility/CUT_TRANSFER_GATE_MUTATION_REPORT.json"
    mutation = load(project, mutation_path)
    require(mutation.get("schema") == "k3p-strong-class-cut-transfer-gate-mutations-v1" and
            mutation.get("status") == "PASS", "cut mutation status")
    require(mutation.get("mutation_count") == mutation.get("rejected_count") == 12 and
            mutation.get("survived_count") == 0 and
            len(mutation.get("clean_replays", [])) == 2 and
            all(row.get("result") == "PASS" for row in mutation["clean_replays"]),
            "cut mutation census and ordinary/optimized safeguards")
    for relative, value in ((gate_path, gate), (mutation_path, mutation),
                            (theorem_binding["path"], theorem)):
        bindings[relative] = bind(project, relative, value)


def validate_global_and_triangle(project: Path, bindings: dict) -> None:
    manifest_path = "global_infrastructure/GLOBAL_INFRASTRUCTURE_MANIFEST.json"
    manifest = load(project, manifest_path)
    verify_payload(manifest, "global infrastructure manifest")
    require(manifest.get("schema") == "k3p-global-infrastructure-manifest-v1" and
            manifest.get("status") == "PASS", "global infrastructure manifest")
    require("universal arbitrary-network pointwise" in manifest.get("claim_boundary", "") and
            "withdrawn and not used" in manifest.get("claim_boundary", ""),
            "global claim boundary")
    for relative, record in manifest.get("artifacts", {}).items():
        verify_file_binding(project, relative, record["sha256"])
        value = load(project, relative)
        verify_payload(value, relative)
        require(value.get("schema") == record["schema"] and
                value.get("payload_sha256") == record["payload_sha256"],
                ("global artifact binding", relative))
        bindings.setdefault(relative, bind(project, relative, value))
    for relative, record in manifest.get("independent_implementations", {}).items():
        verify_file_binding(project, relative, record["sha256"])

    verification_path = "global_infrastructure/INDEPENDENT_VERIFICATION.json"
    verification = load(project, verification_path)
    require(verification.get("status") == "PASS" and
            verification.get("global_theorem_dependency_status") == "PASS",
            "global independent replay")
    require(set(verification.get("checks", {}).values()) == {"PASS"} and
            set(verification.get("checks", {})) == {
                "H14_context", "bridge_fibre", "gluing_genericity_reconstruction",
                "manifest", "marginal_submersion", "strong_class_containment_cut_transfer",
            }, "global independent checks")
    cut = verification.get("cut_transfer_release_replay", {})
    require(cut.get("universal_pointwise_K3P_cut_recovery_used") is False,
            "global replay universal pointwise substitution")
    require(cut.get("theorem_manifest_sha256") == sha_file(
                project / "cut_recovery/strong_crossbridge/global_transfer/THEOREM_MANIFEST.json"
            ) and cut.get("release_verifier_sha256") == sha_file(
                project / "cut_recovery/strong_crossbridge/global_transfer/verify_release.py"
            ), "global replay cut-release hash binding")
    require(cut.get("fresh_replays", {}).get("ordinary", {}).get("python_optimized") is False and
            cut.get("fresh_replays", {}).get("optimized", {}).get("python_optimized") is True,
            "global ordinary/optimized cut replay")

    mutation_path = "global_infrastructure/MUTATION_CERTIFICATE.json"
    mutation = load(project, mutation_path)
    verify_payload(mutation, "global infrastructure mutations")
    require(mutation.get("status") == "PASS" and mutation.get("rejected") == 19 and
            mutation.get("survived") == 0 and len(mutation.get("mutations", [])) == 19,
            "global mutation census")

    global_path = "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json"
    global_certificate = load(project, global_path)
    require(global_certificate.get("internal_infrastructure_status") == "PASS" and
            global_certificate.get("global_theorem_dependency_status") == "PASS",
            "global theorem dependency status")
    dependencies = global_certificate.get("dependencies", {})
    generic_cut = dependencies.get("generic_cut_rank_recovery", {})
    require(generic_cut.get("universal_pointwise_K3P_cut_recovery_claimed") is False and
            "generic" in generic_cut.get("scope", ""),
            "generic cut-rank claim promoted to universal pointwise iff")
    cut_interface = dependencies.get("strong_class_containment_cut_equality_interface", {})
    require(cut_interface.get("accepted_as_pass") is True and
            cut_interface.get("claim_boundary") == EXPECTED_CUT_BOUNDARY and
            cut_interface.get("universal_pointwise_K3P_cut_recovery_used") is False,
            "global cut interface")
    dag = global_certificate.get("logical_dependency_dag", {})
    require(dag.get("local_classification") == [
        "localization", "four_port_atlas", "restoration", "probes"
    ], "global local-classification DAG")
    require(dag.get("sufficiency") == ["H14_context", "simultaneous_physical_bridge_gluing"],
            "triangle contextual sufficiency DAG")

    h14_path = "triangle_h14/K3P_H14_CONTEXT_CERTIFICATE.json"
    h14 = load(project, h14_path)
    verify_payload(h14, "H14 context")
    require(h14.get("status") == "PASS" and h14.get("H14_dimension") == 14 and
            h14.get("H14_codimension") == 1 and
            h14.get("ambient_normalized_dimension") == 15,
            "H14 dimensions")
    require(h14.get("ambient_open_triangle_germ") is False,
            "ambient-rank-15 triangle sufficiency rejected")
    require(set(h14.get("orientations", {})) == {"1", "2", "3"} and
            all(row.get("rank") == 14 for row in h14["orientations"].values()),
            "triangle orientation ranks")
    relative = h14.get("common_relative_germ", {})
    require(relative.get("never_ambient_rank_15") is True and
            relative.get("rank_in_ambient_A15") == 14 and
            relative.get("rank_relative_to_each_complete_triangle_image") == 14,
            "relative H14 germ")
    context = h14.get("contextualization", {})
    require(context.get("conclusion") ==
            "one common contextual germ is full-dimensional relative to every oriented complete-network image" and
            context.get("tensor_product_independence_assumed") is False,
            "triangle contextualization")
    physical = global_certificate["simultaneous_physical_bridge_gluing"]
    require(physical.get("epsilon_formula") == "epsilon=min(1/4,L^2/(8*U))" and
            physical.get("base_common_effective_isotropic_spectrum") == ["epsilon"] * 3 and
            physical.get("effective_bridge_formula") == "z_h=A_h*x_h",
            "capped effective bridge construction")
    require(physical.get("effective_principal_margin_lower_bound") ==
            "1-epsilon>=3/4" and
            physical.get("effective_continuous_time_margin_lower_bound") ==
            "epsilon-epsilon^2>=3*epsilon/4>0",
            "physical effective bridge margins")
    require(physical.get("actual_coordinate_upper_bound") == "epsilon/L<=1/8" and
            physical.get("actual_principal_composition_margin_lower_bound") ==
            "1-2*epsilon/L>=3/4" and
            physical.get("actual_continuous_time_margin_lower_bound") ==
            "epsilon/U-epsilon^2/L^2>=7*epsilon/(8*U)>0",
            "physical actual bridge margins")
    extension = physical.get("open_neighborhood_full_rank_extension", {})
    require(physical.get("finite_simultaneous_shrinking") is True and
            extension.get("section_is_positive_real_analytic") is True and
            extension.get("strict_physicality_persists_after_finite_shrinking") is True and
            extension.get("independent_effective_coordinates_per_bridge") == 3 and
            extension.get("projection_to_pre_gluing_product_coordinates") == "identity" and
            extension.get("full_rank_relative_global_germ_preserved") is True,
            "simultaneous physical full-rank triangle gluing")
    genericity = global_certificate.get("genericity", {})
    require(genericity.get("total_source_rank_drop_locus") ==
            "R_N={theta in Theta_3,+(N):rank D Phi_N(theta)<d_N}" and
            genericity.get("rank_drop_image_dimension") ==
            "at most d_N-1 by finite constant-rank semialgebraic stratification",
            "total source rank-drop interface")
    require(genericity.get("target_incidence_correspondence") ==
            "Z_Nprime={(q,theta_prime):q=Phi_Nprime(theta_prime),q in M_3,+(N),theta_prime physical}" and
            genericity.get("full_projection_section") ==
            "a d_N-rank incidence projection has a local physical real-analytic right inverse s(q)" and
            genericity.get("source_parameter_section") ==
            "sigma=s o Phi_N on a regular source-parameter neighborhood, so Phi_N=Phi_Nprime o sigma",
            "genericity incidence-section interface")
    require(genericity.get("real_to_complex_dimension") ==
            "A to A tensor_R C is finite faithfully flat integral and preserves Krull dimension",
            "genericity real-to-complex dimension interface")
    for relative_path, value in ((manifest_path, manifest), (verification_path, verification),
                                 (mutation_path, mutation), (global_path, global_certificate),
                                 (h14_path, h14)):
        bindings[relative_path] = bind(project, relative_path, value)


def validate_continuous_time_specialization(project: Path, bindings: dict) -> dict:
    """Bind the exact CT-to-principal necessity bridge and CT sufficiency inputs."""
    relative = "model_domain/primary_exact_evidence.json"
    model = load(project, relative)
    require(model.get("schema") == "k3p-primary-model-domain-exact-v1", "model-domain schema")
    require(model.get("ct_exponent_vectors") == {
        "c": [0, -2, -2], "g": [-2, 0, -2], "t": [-2, -2, 0]
    }, "CT spectral exponent parameterization")
    require(model.get("ct_ratio_exponents") == {
        "c/(g*t)": [4, 0, 0],
        "g/(c*t)": [0, 4, 0],
        "t/(c*g)": [0, 0, 4],
    }, "CT strict rate inequalities")
    # With c=yz, g=xz, t=xy and 0<x,y,z<1, the three principal
    # transition margins are strictly bounded by products of positive gaps.
    margins = [
        "1+y*z-x*z-x*y > (1-y)*(1-z) > 0",
        "1+x*z-y*z-x*y > (1-x)*(1-z) > 0",
        "1+x*y-y*z-x*z > (1-x)*(1-y) > 0",
    ]
    h14 = load(project, "triangle_h14/K3P_H14_CONTEXT_CERTIFICATE.json")
    common = h14.get("common_preimage", {})
    require(common.get("strict_D3_plus") is True and
            common.get("strict_continuous_time") is True,
            "strict-CT H14 common preimage")
    gluing = load(project, "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json")
    physical = gluing.get("simultaneous_physical_bridge_gluing", {})
    require(physical.get("effective_continuous_time_margin_lower_bound") ==
            "epsilon-epsilon^2>=3*epsilon/4>0" and
            physical.get("actual_continuous_time_margin_lower_bound") ==
            "epsilon/U-epsilon^2/L^2>=7*epsilon/(8*U)>0" and
            physical.get("finite_simultaneous_shrinking") is True,
            "strict-CT contextual gluing")
    bindings[relative] = bind(project, relative, model)
    return {
        "status": "CERTIFIED",
        "strict_CT_is_open_full_dimensional_subset_of_D3_plus": True,
        "spectral_parameterization": "c=y*z, g=x*z, t=x*y with 0<x,y,z<1",
        "inverse_parameterization": [
            "x=sqrt(g*t/c)", "y=sqrt(c*t/g)", "z=sqrt(c*g/t)"
        ],
        "principal_margin_bounds": margins,
        "necessity_transfer": (
            "Every source-relative regular full-dimensional CT containment witness "
            "is an open D3+ containment witness, so the certified principal-domain "
            "necessity theorem applies."
        ),
        "sufficiency_transfer": (
            "The common H14 triangle germ and simultaneous physical bridge gluing "
            "are independently certified inside the strict continuous-time domain."
        ),
    }


def validate_probes(project: Path, bindings: dict) -> None:
    certificate_path = "probes/K3P_PROBE_COHERENCE_CERTIFICATE.json"
    certificate = load(project, certificate_path)
    verify_payload(certificate, "probe certificate", ("operational",))
    require(certificate.get("schema") == "k3p-corrected-coherent-probe-closure-v1" and
            certificate.get("status") == "PASS", "probe certificate")
    require(certificate.get("uses_k2p_sector_equality") is False,
            "probe K2P sector equality")
    one, two = certificate.get("one_port", {}), certificate.get("two_port", {})
    require(one.get("raw_pairs") == 29_964 and one.get("counts") == EXPECTED_ONE and
            one.get("unresolved") == 0 and one.get("equality_survivors") == 2_107,
            "full one-port census")
    require(two.get("raw_pairs") == 544_571 and two.get("counts") == EXPECTED_TWO and
            two.get("unresolved") == 0 and two.get("parents") == 2_107 and
            two.get("equality_survivors") == 32_729,
            "full two-port census")
    assembly = certificate.get("assembly_theorem", {})
    require(assembly.get("unresolved") == assembly.get("incoherent") == 0,
            "probe assembly zero gate")
    require(assembly.get("one_global_triangle_gate", {}).get(
        "new_triangle_created_above_isomorphic_parent") == 0,
        "probe created a new triangle")

    replay_path = "probes/K3P_PROBE_INDEPENDENT_VERIFICATION.json"
    replay = load(project, replay_path)
    verify_payload(replay, "probe independent replay", ("operational",))
    require(replay.get("status") == "PASS" and replay.get("source_certificate_sha256") ==
            sha_file(project / certificate_path), "probe replay source binding")
    require(replay.get("source_payload_sha256") == certificate["payload_sha256"] and
            replay.get("one_port_counts") == EXPECTED_ONE and
            replay.get("two_port_counts") == EXPECTED_TWO and
            replay.get("unresolved") == replay.get("incoherent") == 0,
            "probe replay content")

    mutation_path = "probes/K3P_PROBE_MUTATION_CERTIFICATE.json"
    mutation = load(project, mutation_path)
    verify_payload(mutation, "probe mutations", ("operational",))
    require(mutation.get("status") == "PASS" and
            mutation.get("source_certificate_sha256") == sha_file(project / certificate_path) and
            mutation.get("mutations_attempted") == mutation.get("mutations_rejected") == 18,
            "probe mutation gate")
    require(mutation.get("nondefault_hash_seed_replay", {}).get("status") == "PASS" and
            mutation.get("nondefault_hash_seed_replay", {}).get("returncode") == 0,
            "probe hash-seed replay")

    semantic_path = "probes/K3P_PROBE_SEMANTIC_VERIFICATION.json"
    semantic = load(project, semantic_path)
    verify_payload(semantic, "probe full semantic replay", ("operational",))
    require(semantic.get("schema") == "k3p-probe-independent-full-semantic-replay-v1" and
            semantic.get("status") == "PASS", "probe semantic replay status")
    require(semantic.get("source_certificate_sha256") ==
            sha_file(project / certificate_path) and
            semantic.get("source_payload_sha256") == certificate["payload_sha256"],
            "probe semantic source binding")
    independence = semantic.get("independence", {})
    require(independence == {
        "atlas_imported": False,
        "graphs_reconstructed_from_public_candidate_profiles": True,
        "producer_imported": False,
        "stored_hashes_used_only_as_bindings": True,
    }, "probe semantic independence boundary")
    require(semantic.get("coverage") == {
        "all_probe_rows": 574_535,
        "anchors": 176,
        "one_port_rows": 29_964,
        "two_port_parent_rows": 2_107,
        "two_port_rows": 544_571,
    } and semantic.get("one_port_counts") == EXPECTED_ONE and
            semantic.get("two_port_counts") == EXPECTED_TWO,
            "probe semantic complete census")
    witnesses = semantic.get("semantic_witnesses", {})
    require(witnesses == {
        "declared_Bernstein_certificates_replayed": 0,
        "exact_transports": 67_741,
        "incoherent": 0,
        "marginal_restrictions": 4_379,
        "new_global_triangles": 0,
        "quartet_certificates": 638,
        "reverse_order_marginals": 32_729,
        "tree_sunlet_six_circuit_certificates": 675,
        "unresolved": 0,
    }, "probe semantic witness census")

    semantic_mutation_path = "probes/K3P_PROBE_SEMANTIC_MUTATIONS.json"
    semantic_mutation = load(project, semantic_mutation_path)
    verify_payload(semantic_mutation, "probe coherent semantic mutations")
    semantic_verifier_path = "probes/verify_k3p_probes_semantic.py"
    require(semantic_mutation.get("schema") ==
            "k3p-probe-semantic-coherent-mutations-v1" and
            semantic_mutation.get("status") == "PASS" and
            semantic_mutation.get("mutations_rejected") == 7 and
            semantic_mutation.get("mutations_survived") == 0 and
            semantic_mutation.get("clean_baselines_required") is True and
            semantic_mutation.get("coherent_inner_hashes_recomputed") is True,
            "probe coherent semantic mutation gate")
    semantic_cases = semantic_mutation.get("mutations", [])
    require(len(semantic_cases) == 7 and
            {row.get("name") for row in semantic_cases} ==
            EXPECTED_SEMANTIC_PROBE_MUTATIONS and
            all(row.get("status") == "REJECTED" and
                isinstance(row.get("diagnostic"), str) and row["diagnostic"]
                for row in semantic_cases),
            "probe coherent semantic mutation cases")
    require(semantic_mutation.get("source_certificate_sha256") ==
            sha_file(project / certificate_path) and
            semantic_mutation.get("source_certificate_payload_sha256") ==
            certificate["payload_sha256"] and
            semantic_mutation.get("mutation_runner_sha256") ==
            sha_file(project / semantic_verifier_path),
            "probe semantic mutation bindings")
    require(semantic.get("mutations", {}).get("report_sha256") ==
            sha_file(project / semantic_mutation_path) and
            semantic.get("mutations", {}).get("payload_sha256") ==
            semantic_mutation["payload_sha256"] and
            semantic.get("mutations", {}).get("rejected") == 7 and
            semantic.get("mutations", {}).get("survived") == 0,
            "probe semantic replay/mutation cross-binding")

    for manifest_name in (
        "ONE_PORT_PROBE_MANIFEST.json", "TWO_PORT_PROBE_MANIFEST.json",
        "GLOBAL_TRANSPORT_MANIFEST.json", "RESTORATION_MANIFEST.json",
    ):
        relative = "probes/" + manifest_name
        manifest = load(project, relative)
        verify_payload(manifest, manifest_name)
        require(manifest.get("status") == "PASS", (manifest_name, "status"))
        require(manifest.get("certificate_sha256") == sha_file(project / certificate_path) and
                manifest.get("independent_replay_sha256") == sha_file(project / replay_path) and
                manifest.get("mutation_certificate_sha256") == sha_file(project / mutation_path),
                (manifest_name, "probe package binding"))
        bindings[relative] = bind(project, relative, manifest)

    for relative, value in ((certificate_path, certificate), (replay_path, replay),
                            (mutation_path, mutation), (semantic_path, semantic),
                            (semantic_mutation_path, semantic_mutation)):
        bindings[relative] = bind(project, relative, value)
    bindings[semantic_verifier_path] = bind(project, semantic_verifier_path)


def validate_restoration(project: Path, bindings: dict) -> None:
    manifest_path = "restoration/RESTORATION_MANIFEST.json"
    manifest = load(project, manifest_path)
    verify_payload(manifest, "restoration manifest")
    require(manifest.get("schema") == "k3p-fixed-full-restoration-manifest-v1" and
            manifest.get("status") == "PASS", "restoration manifest")
    require(manifest.get("uses_historical_k2p_algebra") is False and
            manifest.get("uses_k2p_sector_equality") is False,
            "historical K2P restoration algebra")
    census = manifest.get("census", {})
    for field, expected in EXPECTED_RESTORATION_COUNTS.items():
        require(census.get(field) == expected, ("restoration census", field))
    require(census.get("forest_edges") == 36_824 and census.get("first_edges") == 36_568 and
            census.get("second_edges") == 256 and census.get("unresolved") == 0 and
            census.get("former_continuations_early_terminated_by_k3p_quartic") == 32,
            "restoration forest accounting")
    require(sum(census.get("minimal_first_layer_proof_counts", {}).values()) == 36_568,
            "restoration minimal proof total")
    ledger = manifest.get("ledger", {})
    verify_file_binding(project, ledger["path"], ledger["sha256"])
    require(ledger.get("rows") == 36_824, "restoration ledger rows")
    registry = manifest.get("proof_registry", {})
    verify_file_binding(project, registry["path"], registry["sha256"])
    producer = manifest.get("producer", {})
    verify_file_binding(project, producer["path"], producer["sha256"])
    verify_file_binding(project, producer["support_path"], producer["support_sha256"])
    require(producer.get("optimized_mode_forbidden") is True,
            "restoration producer optimized safeguard")

    replay_path = "restoration/K3P_RESTORATION_INDEPENDENT_VERIFICATION.json"
    replay = load(project, replay_path)
    verify_payload(replay, "restoration independent replay")
    require(replay.get("status") == "PASS" and
            replay.get("manifest_payload_sha256") == manifest["payload_sha256"] and
            replay.get("uses_producer_code") is False and
            replay.get("uses_k2p_sector_equality") is False and
            replay.get("unresolved") == 0,
            "restoration independent replay")
    for field, expected in EXPECTED_RESTORATION_COUNTS.items():
        require(replay.get(field) == expected, ("restoration replay census", field))

    mutation_path = "restoration/K3P_RESTORATION_MUTATION_CERTIFICATE.json"
    mutation = load(project, mutation_path)
    verify_payload(mutation, "restoration mutations")
    verifier_path = "restoration/verify_k3p_restoration.py"
    require(mutation.get("status") == "PASS" and
            mutation.get("manifest_payload_sha256") == manifest["payload_sha256"] and
            mutation.get("mutation_count") == mutation.get("rejected") == 20 and
            mutation.get("accepted") == 0 and len(mutation.get("mutations", [])) == 20,
            "restoration 20 mutations")
    verify_file_binding(project, verifier_path, mutation["verifier_sha256"])

    probe_manifest_path = "probes/RESTORATION_MANIFEST.json"
    probe_manifest = load(project, probe_manifest_path)
    require(probe_manifest.get("schema") == "k3p-restoration-manifest-v2" and
            probe_manifest.get("status") == "PASS" and
            probe_manifest.get("k3p_algebra_status") ==
            "PASS_COMPLETE_INDEPENDENT_K3P_RESTORATION",
            "probe/restoration integration status")
    require(probe_manifest.get("restoration_count_distinctions") == EXPECTED_RESTORATION_COUNTS,
            "stale restoration counts rejected")
    standalone = probe_manifest.get("standalone_k3p_restoration", {})
    expected_bindings = {
        "manifest": (manifest_path, manifest["payload_sha256"]),
        "independent_replay": (replay_path, replay["payload_sha256"]),
        "mutation_certificate": (mutation_path, mutation["payload_sha256"]),
    }
    for name, (relative, payload) in expected_bindings.items():
        record = standalone.get(name, {})
        require(record.get("path") == relative and record.get("sha256") == sha_file(project / relative)
                and record.get("payload_sha256") == payload and record.get("status") == "PASS",
                ("probe restoration binding", name))
    require(standalone.get("independent_replay", {}).get("uses_producer_code") is False and
            standalone.get("mutation_certificate", {}).get("mutation_count") == 20 and
            standalone.get("mutation_certificate", {}).get("rejected") == 20 and
            standalone.get("uses_historical_k2p_algebra") is False and
            standalone.get("uses_k2p_sector_equality") is False,
            "probe restoration independence boundary")
    sealer = project / "probes/seal_probe_manifests.py"
    require(sealer.is_file(), "probe manifest sealer")
    for relative, value in ((manifest_path, manifest), (replay_path, replay),
                            (mutation_path, mutation), (probe_manifest_path, probe_manifest)):
        bindings[relative] = bind(project, relative, value)
    bindings["probes/seal_probe_manifests.py"] = bind(project, "probes/seal_probe_manifests.py")


def validate_claim_lock(project: Path, bindings: dict,
                        *, validate_integrated_mutation_report: bool = True) -> None:
    relative = "FINAL_CLAIM_LOCK.json"
    lock = load(project, relative)
    require(lock.get("status") == "CERTIFIED_K3P_SAME_MATHEMATICAL_CLASSIFICATION" and
            lock.get("claimed_outcome") == "K3P-SAME", "claim lock promotion")
    require(lock.get("network_class") ==
            "binary standard semi-directed strongly tree-child level-2", "claim class")
    expected_ct = {
        "status": "CERTIFIED",
        "strict_CT_is_open_full_dimensional_subset_of_D3_plus": True,
        "spectral_parameterization": "c=y*z, g=x*z, t=x*y with 0<x,y,z<1",
        "inverse_parameterization": [
            "x=sqrt(g*t/c)", "y=sqrt(c*t/g)", "z=sqrt(c*g/t)"
        ],
        "principal_margin_bounds": [
            "1+y*z-x*z-x*y > (1-y)*(1-z) > 0",
            "1+x*z-y*z-x*y > (1-x)*(1-z) > 0",
            "1+x*y-y*z-x*z > (1-x)*(1-y) > 0",
        ],
        "necessity_transfer": (
            "Every source-relative regular full-dimensional CT containment witness "
            "is an open D3+ containment witness, so the certified principal-domain "
            "necessity theorem applies."
        ),
        "sufficiency_transfer": (
            "The common H14 triangle germ and simultaneous physical bridge gluing "
            "are independently certified inside the strict continuous-time domain."
        ),
    }
    require(lock.get("continuous_time_specialization") == expected_ct,
            "continuous-time specialization bridge")
    certification = lock.get("certification", {})
    require(certification.get("classification_gate") ==
            "reproducibility/verify_k3p_same_classification.py" and
            certification.get("classification_gate_sha256") == sha_file(Path(__file__).resolve()),
            "claim-lock classification gate binding")
    require(certification.get("classification_gate_report") ==
            "reproducibility/K3P_SAME_CLASSIFICATION_GATE_REPORT.json" and
            certification.get("classification_gate_report_schema") ==
            "k3p-same-integrated-classification-gate-v2" and
            certification.get("classification_gate_report_status") == "CERTIFIED_K3P_SAME",
            "claim-lock classification report contract")
    mutation_gate = "reproducibility/test_k3p_same_classification_mutations.py"
    mutation_report = "reproducibility/K3P_SAME_CLASSIFICATION_MUTATION_REPORT.json"
    require(certification.get("classification_mutation_gate") == mutation_gate and
            certification.get("classification_mutation_gate_sha256") ==
            sha_file(project / mutation_gate), "claim-lock classification mutation gate binding")
    bindings[mutation_gate] = bind(project, mutation_gate)
    if validate_integrated_mutation_report:
        require(certification.get("classification_mutation_report") == mutation_report and
                certification.get("classification_mutation_report_sha256") ==
                sha_file(project / mutation_report) and
                certification.get("classification_mutation_report_status") ==
                "PASS_27_OF_27_REJECTED",
                "claim-lock classification mutation report binding")
        mutation_value = load(project, mutation_report)
        verify_payload(mutation_value, "integrated classification mutations")
        mutation_rows = mutation_value.get("mutations", [])
        require(mutation_value.get("status") == "PASS" and
                mutation_value.get("mutation_count") ==
                mutation_value.get("rejected") == 27 and
                mutation_value.get("survived") == 0 and
                mutation_value.get("verifier_sha256") ==
                sha_file(Path(__file__).resolve()),
                "integrated classification mutation result")
        require(isinstance(mutation_rows, list) and len(mutation_rows) == 27 and
                {row.get("name") for row in mutation_rows if isinstance(row, dict)} ==
                EXPECTED_INTEGRATED_MUTATIONS and
                all(row.get("status") == "REJECTED" and
                    row.get("diagnostic_observed") is True
                    for row in mutation_rows if isinstance(row, dict)),
                "integrated classification mutation cases")
        bindings[mutation_report] = bind(project, mutation_report, mutation_value)
    cut = lock.get("cut_transfer", {})
    require(cut.get("status") == "CERTIFIED" and
            cut.get("universal_arbitrary_network_pointwise_cut_rank_iff") ==
            "WITHDRAWN_NOT_USED" and cut.get("common_bridge_tree_assumed") is False and
            cut.get("fourteen_orbit_classification_imported") is False,
            "claim-lock cut boundary")
    triangle = lock.get("triangle", {})
    require(triangle.get("generic_normalized_rank") == 14 and
            triangle.get("ambient_normalized_dimension") == 15 and
            triangle.get("common_strict_ct_smooth_germ_dimension") == 14,
            "claim-lock triangle rank")
    four = lock.get("four_port", {})
    require(four.get("full_universe_raw_presentations") == 405_216 and
            four.get("post_topology_presentations") == 27_834 and
            four.get("rigorous_syzygy_rank_exclusions") == 23_054 and
            four.get("full_universe_evidence") == {
                "summary": (
                    "four_port_atlas/full_universe_replay/artifacts/"
                    "FULL_FOUR_PORT_REPLAY.json"
                ),
                "independent_report": (
                    "four_port_atlas/full_universe_replay/"
                    "INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json"
                ),
                "mutation_report": (
                    "four_port_atlas/full_universe_replay/"
                    "FULL_FOUR_PORT_MUTATION_REPORT.json"
                ),
            } and four.get("canonical_nontrivial_orbits") == 14 and
            four.get("raw_records_in_orbits") == 38 and
            four.get("separate_sink_swap_records") == 2 and
            four.get("new_symmetric_moves") == four.get("proper_directed_containments") ==
            four.get("unresolved") == 0,
            "claim-lock four-port conclusion")
    require(lock.get("anchor_universe") == {
        "non_four_derived": 133,
        "four_port_contract_rows_exhaustively_verified": 43,
        "complete": 176,
        "relations": {"isomorphic": 143, "ordinary_triangle": 33},
        "frozen_contract_role": "regression target for 133 derived non-four rows; designated serialization input for 43 four-port rows, not a four-port completeness premise",
        "four_port_raw_equality_parents_covered": 144,
        "four_port_fixed_full_requests_covered": 1_356,
        "four_port_descendant_requests_unmatched": 0,
        "four_port_one_port_rows_reconciled": 161,
        "four_port_two_port_rows_reconciled": 64,
        "k2p_algebra_active": False,
        "marginalized_incoming_parents": 176,
        "marginalized_incoming_physical_paths": 424,
        "marginalized_incoming_paths_unmatched": 0,
        "existing_one_port_rows_reconciled": 66,
        "evidence": {
            "producer": "anchor_universe/artifacts/NON_FOUR_ANCHOR_UNIVERSE.json",
            "independent_verification":
                "anchor_universe/INDEPENDENT_NON_FOUR_VERIFICATION.json",
            "one_port_reconciliation":
                "anchor_universe/MARGINALIZED_THETA_ONE_PORT_RECONCILIATION.json",
            "complete_crosswalk":
                "anchor_universe/COMPLETE_ANCHOR_UNIVERSE_CROSSWALK.json",
            "mutation_report":
                "anchor_universe/NON_FOUR_ANCHOR_MUTATION_REPORT.json",
        },
    }, "claim-lock complete anchor-universe derivation")
    classification = lock.get("classification", {})
    require(classification.get("triangle_equivalence") == {
                "labelled_reduced_trees_of_blobs_agree": True,
                "corresponding_complete_factor_relation":
                    "labelled_mixed_graph_isomorphism_or_ordinary_triangle_redirection",
                "coherent_boundary_transports_required": True,
            }, "claim-lock triangle equivalence definition")
    require(classification.get("proper_one_sided_containment_in_strong_class") is False,
            "proper directed containment inside strong class rejected")
    require(classification.get("principal_positive") ==
            "N <=_(3,+) N' iff N ==_triangle N' iff N bowtie_(3,+) N'" and
            classification.get("strict_continuous_time") ==
            "N <=_(3,CT) N' iff N ==_triangle N' iff N bowtie_(3,CT) N'",
            "claim-lock K3P-SAME equivalence")
    sharpness = lock.get("sharpness", {})
    require(sharpness.get("all_n_minimum") == 3 and
            sharpness.get("all_n_common_germ_dimension") == "6*n-3" and
            sharpness.get("all_n_both_in_weak_not_strong_class") is True and
            sharpness.get("all_n_labelled_nonisomorphic") is True and
            sharpness.get("all_n_nontriangle_equivalent") is True and
            sharpness.get("all_n_common_germ_regular_full_dimensional") is True and
            sharpness.get("strict_continuous_time") is True,
            "claim-lock sharpness all-n scope")
    promotion = lock.get("final_promotion", {})
    require(promotion.get("status") == "CERTIFIED_K3P_SAME" and
            promotion.get("remaining_load_bearing_mathematical_gates") == [] and
            promotion.get("remaining_nonmathematical_gates") == NONMATHEMATICAL_GATES,
            "claim-lock final promotion")
    require(promotion.get("submission_ready") is False and
            promotion.get("human_review_complete") is False and
            promotion.get("doi_assigned") is False and
            promotion.get("license_selected") is False,
            "publication overclaim rejected")
    bindings[relative] = bind(project, relative, lock)


def validate_artifacts(project: Path,
                       *, validate_integrated_mutation_report: bool = True) -> dict:
    project = project.resolve()
    bindings: dict[str, dict] = {}
    validate_primary(project, bindings)
    validate_four_port(project, bindings)
    validate_full_four_port_universe(project, bindings)
    validate_anchor_universe(project, bindings)
    validate_sharpness(project, bindings)
    validate_cut_topology_regeneration(project, bindings)
    validate_noncut_witness_evidence(project, bindings)
    validate_cut_transfer(project, bindings)
    validate_global_and_triangle(project, bindings)
    ct_specialization = validate_continuous_time_specialization(project, bindings)
    validate_probes(project, bindings)
    validate_restoration(project, bindings)
    validate_claim_lock(
        project, bindings,
        validate_integrated_mutation_report=validate_integrated_mutation_report,
    )
    conclusion = {
        "outcome": "K3P-SAME",
        "network_class": "binary standard semi-directed strongly tree-child level-2",
        "principal_positive": "N <=_(3,+) N' iff N ==_triangle N' iff N bowtie_(3,+) N'",
        "strict_continuous_time": "N <=_(3,CT) N' iff N ==_triangle N' iff N bowtie_(3,CT) N'",
        "proper_directed_containment_inside_strong_class": False,
        "new_symmetric_move_inside_strong_class": False,
        "generic_structural_identifiability_modulo_ordinary_triangle_redirection": True,
        "sharp_boundary": "weak_tree_child_minus_strong_tree_child",
    }
    logical_chain = [
        "self-contained displayed-tree noncut recovery and corrected directional cut-transfer give equality of labelled cut sets under containment",
        "bridge fibre and marginal submersions localize containment to corresponding complete factors",
        "the graph-derived 133-anchor non-four universe, all 144 raw four-port equality parents and all 1,356 fixed-full descendant requests, restoration, and all-row semantic one-/two-port probes leave only labelled isomorphism or ordinary triangle redirection",
        "the common relative H14 germ and simultaneous physical bridge gluing prove contextual triangle sufficiency",
        "finite semialgebraic genericity and reconstruction promote the local result to the complete strong class",
        "the strict-CT weak-not-strong Krawczyk family proves sharpness beyond strong tree-childness",
    ]
    rejected_substitutions = {
        "universal_arbitrary_network_pointwise_cut_rank_iff": "REJECTED_WITHDRAWN_NOT_USED",
        "ambient_rank_15_ordinary_triangle_sufficiency": "REJECTED_TRIANGLE_RANK_IS_14_RELATIVE_H14_GERM_USED",
        "restoration_36568_36792_count_conflation": "REJECTED_DISTINCT_MINIMAL_AND_LEGACY_CENSUSES",
        "proper_directed_containment_inside_strong_class": "REJECTED_BY_COMPLETE_LOCAL_CLASSIFICATION",
    }
    return {
        "bindings": dict(sorted(bindings.items())),
        "logical_chain": logical_chain,
        "continuous_time_specialization": ct_specialization,
        "conclusion": conclusion,
        "rejected_substitutions": rejected_substitutions,
        "remaining_mathematical_gates": [],
        "remaining_nonmathematical_gates": NONMATHEMATICAL_GATES,
        "publication_boundary": {
            "submission_ready": False,
            "human_review_complete": False,
            "doi_assigned": False,
            "license_selected": False,
            "peer_review_complete": False,
        },
    }


def run_command(project: Path, name: str, command: list[str], sentinel: str,
                timeout: int = 3600) -> dict:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.monotonic()
    result = subprocess.run(
        command, cwd=project, env=environment, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        check=False, timeout=timeout,
    )
    elapsed = time.monotonic() - started
    seen = sentinel in result.stdout
    require(result.returncode == 0 and seen,
            ("fresh replay failed", name, result.returncode, sentinel, result.stdout[-4000:]))
    return {
        "name": name,
        "command": command,
        "exit_code": result.returncode,
        "sentinel": sentinel,
        "sentinel_seen": seen,
        "runtime_seconds": elapsed,
        "transcript_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        "transcript_tail": result.stdout[-1200:],
        "status": "PASS",
    }


def run_fresh_replays(project: Path) -> list[dict]:
    python = sys.executable
    records = []
    records.append(run_command(
        project, "primary_28_of_28",
        [python, "reproducibility/verify_primary.py"], "PRIMARY_GATE_STATUS PASS", 3600,
    ))
    records.append(run_command(
        project, "clean_room_h21_fourteen_orbits",
        ["sh", "clean_room/verify_clean_room.sh"], "CLEAN_ROOM_FULL_GATE_PASS", 3600,
    ))
    records.append(run_command(
        project, "sharpness_adversarial",
        [python, "sharpness/adversarial/adversarial_audit.py"],
        "SHARPNESS_ADVERSARIAL_MATH_PASS", 3600,
    ))
    records.append(run_command(
        project, "cut_transfer_ordinary_optimized_adversarial",
        [python, "reproducibility/strong_cut_transfer_gate.py"],
        "STRONG_CLASS_CUT_TRANSFER_GATE_PASS", 3600,
    ))
    records.append(run_command(
        project, "cut_transfer_claim_boundary_mutations",
        [python, "reproducibility/test_cut_transfer_gate_mutations.py"],
        "STRONG_CLASS_CUT_TRANSFER_GATE_MUTATIONS_PASS", 3600,
    ))
    records.append(run_command(
        project, "cut_topology_graph_regeneration",
        ["bash", "cut_recovery/strong_crossbridge/topology_regeneration/verify_all.sh"],
        "CUT_TOPOLOGY_GRAPH_REGENERATION_SUITE_PASS", 3600,
    ))
    records.append(run_command(
        project, "cut_noncut_word_combinatorics",
        [python,
         "cut_recovery/strong_crossbridge/palette_independent/verify_cut_combinatorics.py"],
        "K3P_CUT_COMBINATORICS_PASS", 600,
    ))
    records.append(run_command(
        project, "displayed_tree_noncut_minor",
        [python,
         "cut_recovery/strong_crossbridge/palette_independent/verify_displayed_tree_minor.py"],
        "K3P_DISPLAYED_TREE_MINOR_PASS", 600,
    ))
    with tempfile.TemporaryDirectory(prefix="k3p-same-fresh-") as directory:
        temporary = Path(directory)
        global_report = temporary / "global.json"
        records.append(run_command(
            project, "global_infrastructure",
            [python, "global_infrastructure/verify_global_infrastructure.py",
             "--report", str(global_report)], '"status": "PASS"', 3600,
        ))
        fresh_global = json.loads(global_report.read_text())
        require(fresh_global.get("status") == "PASS", "fresh global report")
        records[-1]["fresh_output_payload"] = fresh_global
        records[-1]["fresh_output_payload_sha256"] = sha_object(fresh_global)
        records.append(run_command(
            project, "global_infrastructure_mutations",
            [python, "global_infrastructure/test_global_infrastructure_mutations.py"],
            '"status": "PASS"', 3600,
        ))

        four_port_report = temporary / "full_four_port.json"
        records.append(run_command(
            project, "full_four_port_independent_replay",
            [python,
             "four_port_atlas/full_universe_replay/verify_full_four_port_replay.py",
             "--report", str(four_port_report)],
            "K3P_FULL_FOUR_PORT_INDEPENDENT_VERIFICATION_PASS", 43_200,
        ))
        fresh_four_port = json.loads(four_port_report.read_text())
        verify_payload(fresh_four_port, "fresh full four-port replay", ("operational",))
        stored_four_port = load(
            project,
            "four_port_atlas/full_universe_replay/"
            "INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json",
        )
        require(fresh_four_port["payload_sha256"] == stored_four_port["payload_sha256"],
                "fresh/stored full four-port replay payload")
        records[-1]["fresh_output_payload_sha256"] = fresh_four_port["payload_sha256"]

        four_port_mutations = temporary / "full_four_port_mutations.json"
        records.append(run_command(
            project, "full_four_port_coherent_mutations",
            [python,
             "four_port_atlas/full_universe_replay/test_full_four_port_mutations.py",
             "--report", str(four_port_mutations)],
            "K3P_FULL_FOUR_PORT_COHERENT_MUTATIONS_PASS", 3_600,
        ))
        fresh_four_port_mutations = json.loads(four_port_mutations.read_text())
        verify_payload(fresh_four_port_mutations,
                       "fresh full four-port mutations", ("operational",))
        stored_four_port_mutations = load(
            project,
            "four_port_atlas/full_universe_replay/FULL_FOUR_PORT_MUTATION_REPORT.json",
        )
        require(fresh_four_port_mutations["payload_sha256"] ==
                stored_four_port_mutations["payload_sha256"],
                "fresh/stored full four-port mutation payload")
        records[-1]["fresh_output_payload_sha256"] = (
            fresh_four_port_mutations["payload_sha256"]
        )

        non_four_report = temporary / "non_four_anchors.json"
        records.append(run_command(
            project, "non_four_anchor_independent_replay",
            [python, "anchor_universe/verify_non_four_anchor_universe.py",
             "--report", str(non_four_report)],
            "K3P_INDEPENDENT_NON_FOUR_ANCHOR_UNIVERSE_PASS", 3_600,
        ))
        fresh_non_four = json.loads(non_four_report.read_text())
        verify_payload(fresh_non_four, "fresh independent non-four anchors",
                       ("operational",))
        stored_non_four = load(
            project, "anchor_universe/INDEPENDENT_NON_FOUR_VERIFICATION.json"
        )
        require(fresh_non_four["payload_sha256"] == stored_non_four["payload_sha256"],
                "fresh/stored independent non-four anchor payload")
        records[-1]["fresh_output_payload_sha256"] = fresh_non_four["payload_sha256"]

        reconciliation_report = temporary / "marginalized_theta_reconciliation.json"
        records.append(run_command(
            project, "marginalized_theta_one_port_reconciliation",
            [python,
             "anchor_universe/verify_marginalized_theta_one_port_reconciliation.py",
             "--output", str(reconciliation_report)],
            "MARGINALIZED_THETA_ONE_PORT_RECONCILIATION_PASS", 3_600,
        ))
        fresh_reconciliation = json.loads(reconciliation_report.read_text())
        verify_payload(fresh_reconciliation,
                       "fresh marginalized theta one-port reconciliation")
        stored_reconciliation = load(
            project, "anchor_universe/MARGINALIZED_THETA_ONE_PORT_RECONCILIATION.json"
        )
        require(fresh_reconciliation["payload_sha256"] ==
                stored_reconciliation["payload_sha256"],
                "fresh/stored marginalized theta reconciliation payload")
        records[-1]["fresh_output_payload_sha256"] = (
            fresh_reconciliation["payload_sha256"]
        )

        crosswalk_report = temporary / "complete_anchor_crosswalk.json"
        records.append(run_command(
            project, "complete_anchor_universe_crosswalk",
            [python, "anchor_universe/verify_complete_anchor_crosswalk.py",
             "--verifier", str(non_four_report),
             "--root-movement-reconciliation", str(reconciliation_report),
             "--output", str(crosswalk_report)],
            "K3P_COMPLETE_ANCHOR_UNIVERSE_CROSSWALK_PASS", 3_600,
        ))
        fresh_crosswalk = json.loads(crosswalk_report.read_text())
        verify_payload(fresh_crosswalk, "fresh complete anchor crosswalk",
                       ("operational",))
        stored_crosswalk = load(
            project, "anchor_universe/COMPLETE_ANCHOR_UNIVERSE_CROSSWALK.json"
        )
        require(fresh_crosswalk["payload_sha256"] == stored_crosswalk["payload_sha256"],
                "fresh/stored complete anchor crosswalk payload")
        records[-1]["fresh_output_payload_sha256"] = fresh_crosswalk["payload_sha256"]

        non_four_mutations = temporary / "non_four_anchor_mutations.json"
        records.append(run_command(
            project, "non_four_anchor_mutations",
            [python, "anchor_universe/test_non_four_anchor_mutations.py",
             "--output", str(non_four_mutations)],
            "K3P_NON_FOUR_ANCHOR_MUTATIONS_PASS", 3_600,
        ))
        fresh_non_four_mutations = json.loads(non_four_mutations.read_text())
        verify_payload(fresh_non_four_mutations,
                       "fresh non-four anchor mutations", ("operational",))
        stored_non_four_mutations = load(
            project, "anchor_universe/NON_FOUR_ANCHOR_MUTATION_REPORT.json"
        )
        require(fresh_non_four_mutations["payload_sha256"] ==
                stored_non_four_mutations["payload_sha256"],
                "fresh/stored non-four anchor mutation payload")
        records[-1]["fresh_output_payload_sha256"] = (
            fresh_non_four_mutations["payload_sha256"]
        )

        probe_report = temporary / "probes.json"
        records.append(run_command(
            project, "full_probe_independent_replay",
            [python, "probes/verify_k3p_probes.py", "--output", str(probe_report)],
            '"status": "PASS"', 3600,
        ))
        fresh_probe = json.loads(probe_report.read_text())
        verify_payload(fresh_probe, "fresh probe replay", ("operational",))
        stored_probe = load(project, "probes/K3P_PROBE_INDEPENDENT_VERIFICATION.json")
        require(fresh_probe["payload_sha256"] == stored_probe["payload_sha256"],
                "fresh/stored probe replay payload")
        records[-1]["fresh_output_payload_sha256"] = fresh_probe["payload_sha256"]

        semantic_report = temporary / "probe_semantic.json"
        semantic_mutations = temporary / "probe_semantic_mutations.json"
        records.append(run_command(
            project, "full_probe_semantic_replay",
            [python, "probes/verify_k3p_probes_semantic.py", "--output",
             str(semantic_report), "--mutations-output", str(semantic_mutations)],
            "K3P_PROBE_SEMANTIC_REPLAY_PASS", 14_400,
        ))
        fresh_semantic = json.loads(semantic_report.read_text())
        verify_payload(fresh_semantic, "fresh probe semantic replay", ("operational",))
        stored_semantic = load(project, "probes/K3P_PROBE_SEMANTIC_VERIFICATION.json")
        require(fresh_semantic["payload_sha256"] == stored_semantic["payload_sha256"],
                "fresh/stored probe semantic payload")
        fresh_semantic_mutations = json.loads(semantic_mutations.read_text())
        verify_payload(fresh_semantic_mutations, "fresh probe semantic mutations")
        stored_semantic_mutations = load(
            project, "probes/K3P_PROBE_SEMANTIC_MUTATIONS.json"
        )
        require(fresh_semantic_mutations["payload_sha256"] ==
                stored_semantic_mutations["payload_sha256"],
                "fresh/stored probe semantic mutation payload")
        records[-1]["fresh_output_payload_sha256"] = fresh_semantic["payload_sha256"]
        records[-1]["fresh_mutation_payload_sha256"] = (
            fresh_semantic_mutations["payload_sha256"]
        )

        restoration_report = temporary / "restoration.json"
        records.append(run_command(
            project, "restoration_independent_replay",
            [python, "restoration/verify_k3p_restoration.py", "--output",
             str(restoration_report)], '"status": "PASS"', 7200,
        ))
        fresh_restoration = json.loads(restoration_report.read_text())
        verify_payload(fresh_restoration, "fresh restoration replay")
        stored_restoration = load(project, "restoration/K3P_RESTORATION_INDEPENDENT_VERIFICATION.json")
        require(fresh_restoration["payload_sha256"] == stored_restoration["payload_sha256"],
                "fresh/stored restoration replay payload")
        records[-1]["fresh_output_payload_sha256"] = fresh_restoration["payload_sha256"]
    records.append(run_command(
        project, "restoration_20_mutations",
        [python, "restoration/test_k3p_restoration_mutations.py"],
        '"status": "PASS"', 3600,
    ))
    return records


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent,
        prefix=path.name + ".", delete=False,
    ) as handle:
        handle.write(encoded)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def logical_promotion_payload(report: dict) -> dict:
    """Return the replay-stable mathematical payload sealed by the report.

    Wall-clock timings, temporary output paths, commands, transcript tails, and
    transcript byte hashes are useful operational provenance but are expected
    to vary between clean machines.  The promotion payload instead binds the
    ordered replay names, their required sentinels and exit status, and any
    independently reconstructed logical output payloads.
    """
    logical = dict(report)
    logical.pop("operational", None)
    logical.pop("payload_sha256", None)
    logical["fresh_replays"] = [
        {
            key: row[key]
            for key in (
                "name",
                "exit_code",
                "sentinel",
                "sentinel_seen",
                "status",
                "fresh_output_payload_sha256",
                "fresh_mutation_payload_sha256",
            )
            if key in row
        }
        for row in report.get("fresh_replays", [])
    ]
    return logical


def main(argv: list[str] | None = None) -> int:
    if not __debug__ or sys.flags.optimize:
        print("K3P_SAME_CLASSIFICATION_GATE_FAIL: optimized Python forbidden", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--artifact-only", action="store_true")
    parser.add_argument("--no-write-report", action="store_true")
    parser.add_argument("--mutation-driver-bootstrap", action="store_true",
                        help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    project = args.project_root.resolve()
    started = time.monotonic()
    try:
        require(not args.mutation_driver_bootstrap or
                (args.artifact_only and args.no_write_report),
                "mutation bootstrap is restricted to no-write artifact checks")
        fresh = [] if args.artifact_only else run_fresh_replays(project)
        core = validate_artifacts(
            project,
            validate_integrated_mutation_report=not args.mutation_driver_bootstrap,
        )
        report = {
            "schema": "k3p-same-integrated-classification-gate-v2",
            "status": "CERTIFIED_K3P_SAME",
            "mathematical_classification_status": "CERTIFIED",
            "fresh_replays": fresh,
            **core,
            "operational": {
                "artifact_only": args.artifact_only,
                "python": sys.version,
                "total_runtime_seconds": time.monotonic() - started,
                "fresh_replay_runtime_seconds": {
                    row["name"]: row["runtime_seconds"] for row in fresh
                },
            },
        }
        report["payload_sha256"] = sha_object(logical_promotion_payload(report))
        require(
            report["payload_sha256"] == sha_object(logical_promotion_payload(report)),
            "classification report payload self-verification",
        )
        if not args.no_write_report:
            atomic_json(args.report.resolve(), report)
        print("K3P_SAME_CLASSIFICATION_GATE_PASS")
        print(json.dumps({
            "status": report["status"],
            "outcome": report["conclusion"]["outcome"],
            "bindings": len(report["bindings"]),
            "fresh_replays": len(fresh),
            "payload_sha256": report["payload_sha256"],
        }, sort_keys=True))
        return 0
    except (GateFailure, KeyError, IndexError, TypeError, ValueError, OSError,
            json.JSONDecodeError, subprocess.SubprocessError) as error:
        print(f"K3P_SAME_CLASSIFICATION_GATE_FAIL:{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
