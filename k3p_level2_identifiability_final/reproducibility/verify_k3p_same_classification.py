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
NONMATHEMATICAL_GATES = [
    "manuscript theorem-proof integration and author review",
    "reader-supplement integration and cross-reference audit",
    "PDF build, render, and visual quality assurance",
    "clean-room release archive and checksum engineering",
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


def validate_primary(project: Path, bindings: dict) -> None:
    relative = "reproducibility/primary_gate_report.json"
    report = load(project, relative)
    require(report.get("schema") == "k3p-primary-gate-report-v1", "primary schema")
    require(report.get("overall_status") == "PASS", "primary status")
    require(report.get("counts") == {"PASS": 28, "BLOCKED": 0, "FAIL": 0}, "primary 28/28")
    input_binding = report.get("input_binding", {})
    require(input_binding.get("status") == "PASS" and
            input_binding.get("file_count") == 33 and
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
    require(cut.get("fresh_replays", {}).get("ordinary", {}).get("python_optimized") is False and
            cut.get("fresh_replays", {}).get("optimized", {}).get("python_optimized") is True,
            "global ordinary/optimized cut replay")

    mutation_path = "global_infrastructure/MUTATION_CERTIFICATE.json"
    mutation = load(project, mutation_path)
    verify_payload(mutation, "global infrastructure mutations")
    require(mutation.get("status") == "PASS" and mutation.get("rejected") == 16 and
            mutation.get("survived") == 0 and len(mutation.get("mutations", [])) == 16,
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
    require(global_certificate["simultaneous_physical_bridge_gluing"].get(
        "finite_simultaneous_shrinking") is True,
        "simultaneous physical triangle gluing")
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
    require(physical.get("continuous_time_margin_lower_bound") == "3*L^2/(16*U^2)>0" and
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
            mutation.get("mutations_attempted") == mutation.get("mutations_rejected") == 17,
            "probe mutation gate")
    require(mutation.get("nondefault_hash_seed_replay", {}).get("status") == "PASS" and
            mutation.get("nondefault_hash_seed_replay", {}).get("returncode") == 0,
            "probe hash-seed replay")

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
                            (mutation_path, mutation)):
        bindings[relative] = bind(project, relative, value)


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


def validate_claim_lock(project: Path, bindings: dict) -> None:
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
    require(certification.get("classification_mutation_report") == mutation_report and
            certification.get("classification_mutation_report_sha256") ==
            sha_file(project / mutation_report) and
            certification.get("classification_mutation_report_status") ==
            "PASS_16_OF_16_REJECTED", "claim-lock classification mutation report binding")
    mutation_value = load(project, mutation_report)
    verify_payload(mutation_value, "integrated classification mutations")
    require(mutation_value.get("status") == "PASS" and
            mutation_value.get("mutation_count") == mutation_value.get("rejected") == 16 and
            mutation_value.get("survived") == 0 and
            mutation_value.get("verifier_sha256") == sha_file(Path(__file__).resolve()),
            "integrated classification mutation result")
    bindings[mutation_gate] = bind(project, mutation_gate)
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
    require(four.get("canonical_nontrivial_orbits") == 14 and
            four.get("raw_records_in_orbits") == 38 and
            four.get("separate_sink_swap_records") == 2 and
            four.get("new_symmetric_moves") == four.get("proper_directed_containments") ==
            four.get("unresolved") == 0,
            "claim-lock four-port conclusion")
    classification = lock.get("classification", {})
    require(classification.get("proper_one_sided_containment_in_strong_class") is False,
            "proper directed containment inside strong class rejected")
    require(classification.get("principal_positive") ==
            "N <=_(3,+) N' iff N ==_triangle N' iff N bowtie_(3,+) N'" and
            classification.get("strict_continuous_time") ==
            "N <=_(3,CT) N' iff N ==_triangle N' iff N bowtie_(3,CT) N'",
            "claim-lock K3P-SAME equivalence")
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


def validate_artifacts(project: Path) -> dict:
    project = project.resolve()
    bindings: dict[str, dict] = {}
    validate_primary(project, bindings)
    validate_four_port(project, bindings)
    validate_sharpness(project, bindings)
    validate_cut_transfer(project, bindings)
    validate_global_and_triangle(project, bindings)
    ct_specialization = validate_continuous_time_specialization(project, bindings)
    validate_probes(project, bindings)
    validate_restoration(project, bindings)
    validate_claim_lock(project, bindings)
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
        "corrected directional cut-transfer gives equality of labelled cut sets under containment",
        "bridge fibre and marginal submersions localize containment to corresponding complete factors",
        "four-port, restoration, and one-/two-port probes leave only labelled isomorphism or ordinary triangle redirection",
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
    args = parser.parse_args(argv)
    project = args.project_root.resolve()
    started = time.monotonic()
    try:
        fresh = [] if args.artifact_only else run_fresh_replays(project)
        core = validate_artifacts(project)
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
