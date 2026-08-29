#!/usr/bin/env python3
"""Targeted fail-closed mutations for the independent global-transfer audit."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from verify_global_transfer_adversarial import (
    AUDIT,
    HERE,
    PATHS,
    PROJECT,
    VerificationError,
    evidence_payload_digest,
    sha256,
    verify,
    verify_cut_inclusion_evidence,
    verify_global_proof_structure,
)


OUTPUT = HERE / "MUTATION_RESULTS.json"


def require(condition: bool, label: object) -> None:
    if not condition:
        raise RuntimeError(str(label))


def mutation_cases(payload: dict):
    cases = []

    def changed(name, mutate):
        value = copy.deepcopy(payload)
        mutate(value)
        cases.append((name, value))

    changed("audit_status", lambda x: x.__setitem__("status", "BLOCKED"))
    changed("remaining_gap", lambda x: x["remaining_gaps"].append("invented gap"))
    changed("universal_pointwise_promotion", lambda x: x["claim_boundary"].__setitem__(
        "universal_pointwise_K3P_cut_recovery", "PROVED"))
    changed("strong_transfer_withdrawn", lambda x: x["claim_boundary"].__setitem__(
        "strong_class_cut_transfer", "WITHDRAWN"))
    changed("common_bridge_tree", lambda x: x["noncircularity"].__setitem__(
        "common_bridge_tree_assumed", True))
    changed("bridge_tree_equality", lambda x: x["noncircularity"].__setitem__(
        "bridge_tree_equality_assumed", True))
    changed("fourteen_orbit", lambda x: x["noncircularity"].__setitem__(
        "fourteen_orbit_result_used", True))
    changed("target_open", lambda x: x["noncircularity"].__setitem__(
        "target_open_parameter_section_used", True))
    changed("factor_correspondence", lambda x: x["noncircularity"].__setitem__(
        "source_target_factor_correspondence_used", True))
    changed("cut_direction_reversed", lambda x: x["noncircularity"].__setitem__(
        "directed_cut_inclusion_proved_here", "Cut(N)_subseteq_Cut(Nprime)"))
    changed("ordinary_central_tree", lambda x: x["finite_handoff"]["tree_central_factor"].__setitem__(
        "ordinary_trivalent_component_can_be_central", True))
    changed("duplicate_active_label", lambda x: x["finite_handoff"]["actual_label_selection"].__setitem__(
        "four_active_labels", "labels_may_repeat"))
    changed("delete_completion_ports", lambda x: x["finite_handoff"]["completion_contract"].__setitem__(
        "physical_deletion_used", True))
    changed("drop_path_sink", lambda x: x["finite_handoff"]["completion_contract"].__setitem__(
        "path_sink_child_ports", "deleted"))
    changed("direction_count", lambda x: x["finite_handoff"]["replayed_counts"].__setitem__(
        "wrong_split_directions", 203))
    changed("displayed_count", lambda x: x["finite_handoff"]["replayed_counts"].__setitem__(
        "displayed_by_all_removed", 13))
    changed("tree_counterexample", lambda x: x["tree_dichotomy"]["finite_falsification"].__setitem__(
        "counterexamples", 1))
    changed("tree_hull_gap", lambda x: x["tree_dichotomy"]["general_proof"].__setitem__(
        "hull_intersection_nonempty", "assumed"))
    changed("side_bridge_factorization", lambda x: x["side_blob_closure"]["factorization_contract"].__setitem__(
        "bridge_separates_side_latent_variables", False))
    changed("side_choice_correlation", lambda x: x["side_blob_closure"]["factorization_contract"].__setitem__(
        "central_and_side_reticulation_choices_are_disjoint", False))
    changed("mixture_not_strict", lambda x: x["side_blob_closure"]["strictness_proof"].__setitem__(
        "convex_mixture", "not_checked"))
    changed("empty_path_allowed", lambda x: x["side_blob_closure"]["strictness_proof"].__setitem__(
        "strict_path_reason", "path_may_be_empty"))
    changed("switching_components", lambda x: x["side_blob_closure"]["exact_replay"].__setitem__(
        "switching_components", 6))
    changed("reticulation_range", lambda x: x["side_blob_closure"]["exact_replay"].__setitem__(
        "reticulation_range", [0, 1]))
    changed("inheritance_boundary", lambda x: x["inheritance_accounting"].__setitem__(
        "retained_values_strict", False))
    changed("inheritance_factorization", lambda x: x["inheritance_accounting"].__setitem__(
        "side_and_central_choices_factor", False))
    changed("max_reticulation", lambda x: x["inheritance_accounting"].__setitem__(
        "maximum_reticulations_per_blob", 3))
    changed("downgrade_side_gap", lambda x: x["finding_during_audit"].__setitem__(
        "severity", "COSMETIC"))
    changed("unclosed_side_gap", lambda x: x["finding_during_audit"].__setitem__(
        "disposition", "OPEN"))
    changed("logical_step_blocked", lambda x: x["logical_steps"][9].__setitem__(
        "status", "UNPROVED"))
    changed("logical_step_deleted", lambda x: x["logical_steps"].pop(9))
    changed("input_hash", lambda x: x["input_sha256"]["global_certificate"].__setitem__(
        "sha256", "0" * 64))
    return cases


def reseal_evidence(value: dict) -> dict:
    value["payload_sha256"] = evidence_payload_digest(value)
    return value


def semantic_mutation_cases():
    audit = json.loads(AUDIT.read_text())
    evidence = json.loads(PATHS["cut_inclusion_evidence"].read_text())
    global_certificate = json.loads(PATHS["global_certificate"].read_text())
    cases = []

    legacy = PROJECT / "cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json"
    substituted = copy.deepcopy(evidence)
    substituted["load_bearing_inputs"]["displayed_tree_lemma"] = {
        "path": str(legacy.resolve().relative_to(PROJECT)),
        "sha256": sha256(legacy),
    }
    cases.append((
        "coherently_resealed_legacy_provenance_substitution",
        lambda value=reseal_evidence(substituted):
            verify_cut_inclusion_evidence(audit, value),
    ))

    no_minor = copy.deepcopy(evidence)
    no_minor["displayed_tree_minor"] = None
    cases.append((
        "coherently_resealed_exact_minor_removal",
        lambda value=reseal_evidence(no_minor):
            verify_cut_inclusion_evidence(audit, value),
    ))

    no_k0_edge = copy.deepcopy(global_certificate)
    next(row for row in no_k0_edge["proof_steps"]
         if row["id"] == "D1")["depends_on"] = ["H0"]
    cases.append((
        "global_K0_dependency_deletion",
        lambda value=no_k0_edge: verify_global_proof_structure(value),
    ))
    return cases


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> None:
    payload = json.loads(AUDIT.read_text())
    results = []
    with tempfile.TemporaryDirectory(prefix="k3p-global-transfer-mutations-") as directory:
        root = Path(directory)
        for index, (name, changed) in enumerate(mutation_cases(payload)):
            path = root / f"mutation_{index:02d}.json"
            path.write_text(json.dumps(changed, sort_keys=True))
            rejected = False
            message = None
            try:
                verify(path, check_manifest=False)
            except (VerificationError, KeyError, IndexError, TypeError, ValueError) as error:
                rejected = True
                message = str(error)
            require(rejected, ("mutation accepted", name))
            results.append({"name": name, "result": "REJECTED", "reason": message})
        for name, check in semantic_mutation_cases():
            rejected = False
            message = None
            try:
                check()
            except (VerificationError, KeyError, IndexError, TypeError, ValueError) as error:
                rejected = True
                message = str(error)
            require(rejected, ("semantic mutation accepted", name))
            results.append({"name": name, "result": "REJECTED", "reason": message})
    report = {
        "schema": "k3p-global-transfer-adversarial-mutations-v1",
        "status": "PASS",
        "audit_sha256": sha256(AUDIT),
        "mutation_count": len(results),
        "rejected_count": len(results),
        "all_mutations_rejected": True,
        "mutations": results,
    }
    atomic_json(OUTPUT, report)
    print(json.dumps({
        "status": report["status"],
        "mutations": report["mutation_count"],
        "rejected": report["rejected_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
