#!/usr/bin/env python3
"""Fail-closed release audit over the producer and independent adversary.

This layer intentionally sits above, and does not import, either verifier.
The independent adversarial audit byte-binds the stable producer verifier and
report.  Keeping those files immutable avoids a circular hash dependency:
this release verifier instead checks both sealed layers and records their
hashes in one final report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]

CERTIFICATE = HERE / "GLOBAL_TRANSFER_CERTIFICATE.json"
UNIVERSE = HERE / "GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json"
CUT_EVIDENCE = HERE / "K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json"
PRODUCER_VERIFIER = HERE / "verify_global_transfer.py"
PRODUCER_REPORT = HERE / "VERIFICATION_REPORT.json"
PRODUCER_OPTIMIZED_REPORT = HERE / "OPTIMIZED_VERIFICATION_REPORT.json"

ADVERSARIAL = HERE / "adversarial"
ADVERSARIAL_AUDIT = ADVERSARIAL / "ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json"
ADVERSARIAL_REPORT = ADVERSARIAL / "VERIFICATION_REPORT.json"
ADVERSARIAL_MUTATIONS = ADVERSARIAL / "MUTATION_RESULTS.json"
ADVERSARIAL_VERIFIER = ADVERSARIAL / "verify_global_transfer_adversarial.py"
ADVERSARIAL_MANIFEST = ADVERSARIAL / "MANIFEST.sha256"

DEFAULT_REPORT = HERE / "RELEASE_VERIFICATION_REPORT.json"

ADVERSARIAL_MANIFEST_FILES = {
    "ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json",
    "ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.md",
    "MUTATION_RESULTS.json",
    "VERIFICATION_REPORT.json",
    "WORK_LOG.md",
    "test_global_transfer_adversarial_mutations.py",
    "verify_global_transfer_adversarial.py",
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: object) -> None:
    if not condition:
        raise VerificationError(str(label))


def sha256(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(PROJECT))


def binding(path: Path) -> dict[str, str]:
    require(path.is_file(), ("missing release input", path))
    return {"path": relative(path), "sha256": sha256(path)}


def load(path: Path) -> dict:
    require(path.is_file(), ("missing JSON", path))
    value = json.loads(path.read_text())
    require(isinstance(value, dict), ("JSON object required", path))
    return value


def verify_producer_layer() -> dict:
    certificate = load(CERTIFICATE)
    universe = load(UNIVERSE)
    cut_evidence = load(CUT_EVIDENCE)
    ordinary = load(PRODUCER_REPORT)
    optimized = load(PRODUCER_OPTIMIZED_REPORT)

    require(certificate["schema"] == "k3p-lost-bridge-global-transfer-certificate-v2",
            "producer certificate schema")
    require(certificate["status"] == "PASS" and certificate["blocked_reason"] is None,
            "producer certificate status")
    require(certificate["local_204_dependency_pass"] is True,
            "producer local dependency")
    require(universe["schema"] == "k3p-global-transfer-direction-universe-v1",
            "producer universe schema")
    require(universe["status"] == "PASS" and len(universe["directions"]) == 204,
            "producer universe status")
    require(cut_evidence["schema"] == "k3p-directed-cut-inclusion-evidence-v1",
            "K3P cut-inclusion evidence schema")
    require(cut_evidence["status"] == "PASS" and
            cut_evidence["remaining_gaps"] == [],
            "K3P cut-inclusion evidence status")
    require(cut_evidence["provenance_policy"] == {
        "jc_algebra_used": False,
        "jc_manuscript_is_load_bearing": False,
        "legacy_global_logic_report_is_load_bearing": False,
        "model_independent_graph_certificate_names_retained": True,
    }, "K3P cut-inclusion evidence provenance")
    require(certificate["load_bearing_inputs"][
        "k3p_directed_cut_inclusion_evidence"
    ] == binding(CUT_EVIDENCE), "producer K3P cut-inclusion evidence binding")

    for report, optimized_flag in ((ordinary, False), (optimized, True)):
        require(report["schema"] == "k3p-lost-bridge-global-transfer-verification-v2",
                "producer report schema")
        require(report["status"] == "PASS", "producer verification status")
        require(report["python_optimized"] is optimized_flag,
                "producer Python mode")
        require(report["artifact_sha256"] == sha256(CERTIFICATE),
                "producer certificate binding")
        require(report["universe_sha256"] == sha256(UNIVERSE),
                "producer universe binding")
        require(report["cut_evidence_sha256"] == sha256(CUT_EVIDENCE),
                "producer K3P cut-evidence binding")
        require(report["verifier_sha256"] == sha256(PRODUCER_VERIFIER),
                "producer verifier binding")
        require(report["direction_count"] == 204, "producer direction count")
        require(report["proof_step_count"] == 15, "producer proof step count")
        require(report["mutation_count"] == 39, "producer mutation count")
        require(report["cut_inclusion_evidence"] == {
            "balanced_words": 808642,
            "implication_steps": 9,
            "jc_cut_theorem_used": False,
            "legacy_global_logic_used": False,
            "minor_terms": 2,
            "palette_presentations": 379742,
            "palette_survivors": 0,
        }, "producer K3P cut-evidence summary")
        require(report["two_terminal_mixture_components_checked"] == 7,
                "producer side-blob mixture replay")
        require(report["common_bridge_tree_used"] is False,
                "producer common bridge tree")
        require(report["fourteen_orbit_used"] is False,
                "producer fourteen-orbit use")

    require(ordinary["mutations"] == optimized["mutations"],
            "producer mutation mode agreement")
    require(all(row["result"] == "REJECTED" for row in ordinary["mutations"]),
            "producer mutation rejection")
    return {
        "direction_count": ordinary["direction_count"],
        "proof_step_count": ordinary["proof_step_count"],
        "mutation_count": ordinary["mutation_count"],
        "two_terminal_mixture_components_checked": ordinary[
            "two_terminal_mixture_components_checked"
        ],
        "cut_inclusion_evidence": ordinary["cut_inclusion_evidence"],
    }


def verify_adversarial_manifest() -> int:
    require(ADVERSARIAL_MANIFEST.is_file(), "missing adversarial manifest")
    filenames = []
    for line in ADVERSARIAL_MANIFEST.read_text().splitlines():
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        require(len(parts) == 2, ("malformed adversarial manifest row", line))
        expected, filename = parts
        require(len(expected) == 64, ("malformed SHA-256", filename))
        path = ADVERSARIAL / filename
        require(path.is_file(), ("missing adversarial file", filename))
        require(sha256(path) == expected, ("adversarial manifest hash", filename))
        filenames.append(filename)
    require(len(filenames) == len(set(filenames)),
            "duplicate adversarial manifest row")
    require(set(filenames) == ADVERSARIAL_MANIFEST_FILES,
            "adversarial manifest file set")
    return len(filenames)


def verify_adversarial_layer() -> dict:
    manifest_rows = verify_adversarial_manifest()
    audit = load(ADVERSARIAL_AUDIT)
    report = load(ADVERSARIAL_REPORT)
    mutations = load(ADVERSARIAL_MUTATIONS)

    require(audit["schema"] == "k3p-global-transfer-adversarial-audit-v2",
            "adversarial audit schema")
    require(audit["status"] == "PASS" and audit["remaining_gaps"] == [],
            "adversarial audit status")
    require(audit["claim_boundary"] == {
        "conclusion": "Cut(N)=Cut(Nprime)_under_source_relative_containment_in_the_strong_class",
        "strong_class_cut_transfer": "PROVED",
        "universal_pointwise_K3P_cut_recovery": "WITHDRAWN_NOT_USED",
    }, "adversarial claim boundary")
    require(audit["finding_during_audit"]["severity"] == "LOAD_BEARING",
            "adversarial finding severity")
    require(audit["finding_during_audit"]["disposition"] ==
            "CLOSED_BY_PATCH_AND_INDEPENDENT_REPLAY",
            "adversarial finding disposition")
    require(audit["input_sha256"]["global_certificate"] == binding(CERTIFICATE),
            "adversarial certificate input binding")
    require(audit["input_sha256"]["global_universe"] == binding(UNIVERSE),
            "adversarial universe input binding")
    require(audit["input_sha256"]["global_verifier"] == binding(PRODUCER_VERIFIER),
            "adversarial producer-verifier input binding")
    require(audit["input_sha256"]["global_verification"] == binding(PRODUCER_REPORT),
            "adversarial producer-report input binding")

    require(report["schema"] == "k3p-global-transfer-adversarial-verification-v2",
            "adversarial report schema")
    require(report["status"] == "PASS" and report["remaining_gaps"] == [],
            "adversarial report status")
    require(report["audit_sha256"] == sha256(ADVERSARIAL_AUDIT),
            "adversarial audit binding")
    require(report["verifier_sha256"] == sha256(ADVERSARIAL_VERIFIER),
            "adversarial verifier binding")
    require(report["finite_handoff"]["wrong_split_directions"] == 204,
            "adversarial direction count")
    require(report["tree_dichotomy"] == {
        "central_component_cases": 10270,
        "counterexamples": 0,
        "crossing_bridge_cases": 9000,
        "labelled_trees_with_at_least_four_leaves": 6108,
        "maximum_vertices": 7,
        "noncut_two_colorings_modulo_color_swap": 19270,
    }, "adversarial tree replay")
    require(report["side_blob_closure"]["switching_components"] == 7,
            "adversarial side-blob switching components")
    require(report["side_blob_closure"]["switching_weight_polynomial_checks"] == 3,
            "adversarial switching-weight checks")
    require(report["producer_imported"] is False,
            "adversarial producer import")
    require(report["common_bridge_tree_used"] is False,
            "adversarial common bridge tree")
    require(report["fourteen_orbit_used"] is False,
            "adversarial fourteen-orbit use")
    require(report["universal_pointwise_cut_claim_used"] is False,
            "adversarial universal pointwise claim")
    k3p_evidence = report["directed_cut_inclusion_evidence"]
    require(k3p_evidence["schema"] == "k3p-directed-cut-inclusion-evidence-v1",
            "adversarial K3P cut-evidence schema")
    require({key: k3p_evidence[key] for key in (
        "balanced_words", "palette_presentations", "palette_survivors",
        "exact_minor_terms", "implication_steps", "legacy_global_logic_used",
        "jc_cut_theorem_used",
    )} == {
        "balanced_words": 808642,
        "palette_presentations": 379742,
        "palette_survivors": 0,
        "exact_minor_terms": 2,
        "implication_steps": 9,
        "legacy_global_logic_used": False,
        "jc_cut_theorem_used": False,
    }, "adversarial K3P cut-evidence replay")
    require(report["legacy_global_logic_used"] is False and
            report["jc_cut_theorem_used"] is False,
            "adversarial retired-premise exclusion")
    require(report["logic"]["producer_proof_steps"] == 15 and
            report["logic"]["producer_mutations_bound"] == 39 and
            report["logic"]["active_k3p_implication_steps"] == 9 and
            report["logic"]["active_legacy_premises"] == 0,
            "adversarial active K3P logic summary")

    require(mutations["schema"] == "k3p-global-transfer-adversarial-mutations-v1",
            "adversarial mutation schema")
    require(mutations["status"] == "PASS", "adversarial mutation status")
    require(mutations["audit_sha256"] == sha256(ADVERSARIAL_AUDIT),
            "adversarial mutation audit binding")
    require(mutations["all_mutations_rejected"] is True,
            "adversarial mutation rejection flag")
    require(mutations["mutation_count"] == mutations["rejected_count"] == 35,
            "adversarial mutation count")
    require(len(mutations["mutations"]) == 35 and
            all(row["result"] == "REJECTED" for row in mutations["mutations"]),
            "adversarial mutation rows")

    return {
        "manifest_rows_checked": manifest_rows,
        "direction_count": report["finite_handoff"]["wrong_split_directions"],
        "tree_colorings_checked": report["tree_dichotomy"][
            "noncut_two_colorings_modulo_color_swap"
        ],
        "tree_counterexamples": report["tree_dichotomy"]["counterexamples"],
        "side_blob_switching_components": report["side_blob_closure"][
            "switching_components"
        ],
        "cut_inclusion_evidence": {
            "balanced_words": k3p_evidence["balanced_words"],
            "exact_minor_terms": k3p_evidence["exact_minor_terms"],
            "implication_steps": k3p_evidence["implication_steps"],
            "jc_cut_theorem_used": k3p_evidence["jc_cut_theorem_used"],
            "legacy_global_logic_used": k3p_evidence["legacy_global_logic_used"],
            "palette_presentations": k3p_evidence["palette_presentations"],
            "palette_survivors": k3p_evidence["palette_survivors"],
        },
        "mutation_count": mutations["mutation_count"],
    }


def verify() -> dict:
    producer = verify_producer_layer()
    adversarial = verify_adversarial_layer()
    require(producer["direction_count"] == adversarial["direction_count"] == 204,
            "producer/adversary direction agreement")
    require(producer["two_terminal_mixture_components_checked"] ==
            adversarial["side_blob_switching_components"] == 7,
            "producer/adversary side-blob agreement")
    return {
        "schema": "k3p-lost-bridge-global-transfer-release-verification-v2",
        "status": "PASS",
        "producer": producer,
        "adversarial": adversarial,
        "bindings": {
            "certificate": binding(CERTIFICATE),
            "universe": binding(UNIVERSE),
            "k3p_cut_inclusion_evidence": binding(CUT_EVIDENCE),
            "producer_verifier": binding(PRODUCER_VERIFIER),
            "producer_report": binding(PRODUCER_REPORT),
            "producer_optimized_report": binding(PRODUCER_OPTIMIZED_REPORT),
            "adversarial_audit": binding(ADVERSARIAL_AUDIT),
            "adversarial_report": binding(ADVERSARIAL_REPORT),
            "adversarial_mutations": binding(ADVERSARIAL_MUTATIONS),
            "adversarial_verifier": binding(ADVERSARIAL_VERIFIER),
            "adversarial_manifest": binding(ADVERSARIAL_MANIFEST),
        },
        "producer_imported": False,
        "adversarial_verifier_imported": False,
        "circular_hash_dependency": False,
        "remaining_gaps": [],
        "python_optimized": not __debug__,
        "release_verifier_sha256": sha256(Path(__file__).resolve()),
    }


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--no-write-report", action="store_true")
    args = parser.parse_args()
    result = verify()
    if not args.no_write_report:
        atomic_json(args.report, result)
    print(json.dumps({
        "status": result["status"],
        "directions": result["producer"]["direction_count"],
        "tree_colorings": result["adversarial"]["tree_colorings_checked"],
        "adversarial_mutations": result["adversarial"]["mutation_count"],
        "python_optimized": result["python_optimized"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
