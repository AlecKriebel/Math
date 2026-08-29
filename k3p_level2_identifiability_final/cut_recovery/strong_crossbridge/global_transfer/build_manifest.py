#!/usr/bin/env python3
"""Bind the verified lost-bridge global-transfer package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "GLOBAL_TRANSFER_CERTIFICATE.json"
UNIVERSE = HERE / "GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json"
CUT_EVIDENCE = HERE / "K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json"
REPORT = HERE / "VERIFICATION_REPORT.json"
OPTIMIZED_REPORT = HERE / "OPTIMIZED_VERIFICATION_REPORT.json"
RELEASE_REPORT = HERE / "RELEASE_VERIFICATION_REPORT.json"
RELEASE_OPTIMIZED_REPORT = HERE / "RELEASE_OPTIMIZED_VERIFICATION_REPORT.json"
RELEASE_VERIFIER = HERE / "verify_release.py"
ADVERSARIAL = HERE / "adversarial"
ADVERSARIAL_AUDIT = ADVERSARIAL / "ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json"
ADVERSARIAL_REPORT = ADVERSARIAL / "VERIFICATION_REPORT.json"
ADVERSARIAL_MUTATIONS = ADVERSARIAL / "MUTATION_RESULTS.json"
ADVERSARIAL_MANIFEST = ADVERSARIAL / "MANIFEST.sha256"
OUTPUT = HERE / "THEOREM_MANIFEST.json"
SHA_OUTPUT = HERE / "MANIFEST.sha256"
FILES = (
    "GLOBAL_TRANSFER_CERTIFICATE.json",
    "GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json",
    "K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json",
    "VERIFICATION_REPORT.json",
    "OPTIMIZED_VERIFICATION_REPORT.json",
    "RELEASE_VERIFICATION_REPORT.json",
    "RELEASE_OPTIMIZED_VERIFICATION_REPORT.json",
    "build_global_transfer.py",
    "build_k3p_cut_inclusion_evidence.py",
    "verify_global_transfer.py",
    "verify_release.py",
    "build_manifest.py",
    "GLOBAL_TRANSFER_AUDIT.md",
    "README.md",
    "WORK_LOG.md",
    "adversarial/ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json",
    "adversarial/ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.md",
    "adversarial/VERIFICATION_REPORT.json",
    "adversarial/MUTATION_RESULTS.json",
    "adversarial/MANIFEST.sha256",
    "adversarial/verify_global_transfer_adversarial.py",
    "adversarial/test_global_transfer_adversarial_mutations.py",
    "adversarial/WORK_LOG.md",
)

ADVERSARIAL_MANIFEST_FILES = {
    "ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json",
    "ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.md",
    "MUTATION_RESULTS.json",
    "VERIFICATION_REPORT.json",
    "WORK_LOG.md",
    "test_global_transfer_adversarial_mutations.py",
    "verify_global_transfer_adversarial.py",
}


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def sha_file(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            answer.update(block)
    return answer.hexdigest()


def binding(path: Path):
    return {
        "path": str(path.resolve().relative_to(HERE.parents[2])),
        "sha256": sha_file(path),
    }


def verify_adversarial_manifest():
    rows = []
    for line in ADVERSARIAL_MANIFEST.read_text().splitlines():
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        require(len(parts) == 2, "adversarial manifest row")
        expected, filename = parts
        path = ADVERSARIAL / filename
        require(path.is_file(), f"adversarial manifest missing {filename}")
        require(sha_file(path) == expected, f"adversarial manifest hash {filename}")
        rows.append(filename)
    require(len(rows) == len(set(rows)), "adversarial manifest duplicates")
    require(set(rows) == ADVERSARIAL_MANIFEST_FILES, "adversarial manifest file set")
    return len(rows)


def main():
    certificate = json.loads(CERTIFICATE.read_text())
    report = json.loads(REPORT.read_text())
    optimized = json.loads(OPTIMIZED_REPORT.read_text())
    release = json.loads(RELEASE_REPORT.read_text())
    release_optimized = json.loads(RELEASE_OPTIMIZED_REPORT.read_text())
    adversarial_audit = json.loads(ADVERSARIAL_AUDIT.read_text())
    adversarial_report = json.loads(ADVERSARIAL_REPORT.read_text())
    adversarial_mutations = json.loads(ADVERSARIAL_MUTATIONS.read_text())
    cut_evidence = json.loads(CUT_EVIDENCE.read_text())
    require(certificate["status"] == "PASS", "certificate status")
    require(certificate["schema"] == "k3p-lost-bridge-global-transfer-certificate-v2",
            "certificate schema")
    require(certificate["local_204_dependency_pass"] is True, "local dependency")
    require(report["status"] == optimized["status"] == "PASS", "verification status")
    require(report["python_optimized"] is False and optimized["python_optimized"] is True, "Python modes")
    require(report["artifact_sha256"] == optimized["artifact_sha256"] == sha_file(CERTIFICATE), "artifact binding")
    require(report["universe_sha256"] == optimized["universe_sha256"] == sha_file(UNIVERSE), "universe binding")
    require(report["verifier_sha256"] == optimized["verifier_sha256"] == sha_file(HERE / "verify_global_transfer.py"), "verifier binding")
    require(report["direction_count"] == optimized["direction_count"] == 204, "direction count")
    require(report["schema"] == optimized["schema"] ==
            "k3p-lost-bridge-global-transfer-verification-v2",
            "verification schema")
    require(report["proof_step_count"] == optimized["proof_step_count"] == 15,
            "proof step count")
    require(report["mutation_count"] == optimized["mutation_count"] == 48,
            "mutation count")
    require(report["cut_evidence_sha256"] ==
            optimized["cut_evidence_sha256"] == sha_file(CUT_EVIDENCE),
            "K3P cut-evidence verification binding")
    require(certificate["load_bearing_inputs"][
        "k3p_directed_cut_inclusion_evidence"
    ] == binding(CUT_EVIDENCE), "certificate K3P cut-evidence binding")
    require(cut_evidence["schema"] == "k3p-directed-cut-inclusion-evidence-v2" and
            cut_evidence["status"] == "PASS" and
            cut_evidence["remaining_gaps"] == [], "K3P cut-evidence status")
    require(cut_evidence["provenance_policy"]["jc_algebra_used"] is False and
            cut_evidence["provenance_policy"][
                "legacy_global_logic_report_is_load_bearing"
            ] is False, "K3P cut-evidence provenance")
    require(report["common_bridge_tree_used"] is False, "common bridge tree")
    require(report["fourteen_orbit_used"] is False, "fourteen orbit")
    require(release["schema"] == release_optimized["schema"] ==
            "k3p-lost-bridge-global-transfer-release-verification-v2",
            "release verification schema")
    require(release["status"] == release_optimized["status"] == "PASS",
            "release verification status")
    require(release["python_optimized"] is False and
            release_optimized["python_optimized"] is True,
            "release Python modes")
    require(release["release_verifier_sha256"] ==
            release_optimized["release_verifier_sha256"] ==
            sha_file(RELEASE_VERIFIER), "release verifier binding")
    require(release["bindings"] == release_optimized["bindings"],
            "release binding mode agreement")
    require(release["producer"] == release_optimized["producer"],
            "release producer mode agreement")
    require(release["adversarial"] == release_optimized["adversarial"],
            "release adversarial mode agreement")
    require(release["remaining_gaps"] == release_optimized["remaining_gaps"] == [],
            "release remaining gaps")
    require(
        release["fresh_semantic_replays"]["direct"]["summary"]["status"] ==
        release["fresh_semantic_replays"]["adversarial"]["summary"]["status"] ==
        release_optimized["fresh_semantic_replays"]["direct"]["summary"]["status"] ==
        release_optimized["fresh_semantic_replays"]["adversarial"]["summary"]["status"] ==
        "PASS",
        "fresh semantic release replays",
    )
    require(
        release["fresh_semantic_replays"]["direct"]["python_optimized"] is False and
        release["fresh_semantic_replays"]["adversarial"]["python_optimized"] is False and
        release_optimized["fresh_semantic_replays"]["direct"]["python_optimized"] is True and
        release_optimized["fresh_semantic_replays"]["adversarial"]["python_optimized"] is True,
        "fresh semantic release modes",
    )
    require(release["bindings"]["certificate"] == binding(CERTIFICATE),
            "release certificate binding")
    require(release["bindings"]["universe"] == binding(UNIVERSE),
            "release universe binding")
    require(release["bindings"]["k3p_cut_inclusion_evidence"] ==
            binding(CUT_EVIDENCE), "release K3P cut-evidence binding")
    require(release["bindings"]["adversarial_audit"] == binding(ADVERSARIAL_AUDIT),
            "release adversarial audit binding")
    require(release["bindings"]["adversarial_report"] == binding(ADVERSARIAL_REPORT),
            "release adversarial report binding")
    require(release["bindings"]["adversarial_mutations"] == binding(ADVERSARIAL_MUTATIONS),
            "release adversarial mutation binding")
    require(release["bindings"]["adversarial_manifest"] == binding(ADVERSARIAL_MANIFEST),
            "release adversarial manifest binding")
    manifest_rows = verify_adversarial_manifest()
    require(manifest_rows == release["adversarial"]["manifest_rows_checked"] == 7,
            "adversarial manifest row count")
    require(adversarial_audit["schema"] == "k3p-global-transfer-adversarial-audit-v2",
            "adversarial audit schema")
    require(adversarial_audit["status"] == "PASS" and
            adversarial_audit["remaining_gaps"] == [], "adversarial audit status")
    require(adversarial_report["schema"] ==
            "k3p-global-transfer-adversarial-verification-v2",
            "adversarial verification schema")
    require(adversarial_report["status"] == "PASS" and
            adversarial_report["audit_sha256"] == sha_file(ADVERSARIAL_AUDIT),
            "adversarial verification binding")
    require(adversarial_report["legacy_global_logic_used"] is False and
            adversarial_report["jc_cut_theorem_used"] is False and
            adversarial_report["directed_cut_inclusion_evidence"][
                "implication_steps"
            ] == 9,
            "adversarial K3P cut-evidence replay")
    require(adversarial_mutations["schema"] ==
            "k3p-global-transfer-adversarial-mutations-v1",
            "adversarial mutation schema")
    require(adversarial_mutations["status"] == "PASS" and
            adversarial_mutations["all_mutations_rejected"] is True and
            adversarial_mutations["mutation_count"] ==
            adversarial_mutations["rejected_count"] == 44,
            "adversarial mutation status")

    hashes = {name: sha_file(HERE / name) for name in FILES}
    manifest = {
        "schema": "k3p-lost-bridge-global-transfer-theorem-manifest-v2",
        "status": "PASS",
        "certified_claim": (
            "For binary standard semi-directed strongly tree-child level-2 "
            "networks under source-relative regular full-dimensional containment "
            "on strict D3,+, Cut(N)=Cut(Nprime)."
        ),
        "new_mechanism": (
            "The target two-active crossing alternative supplies a target bridge "
            "crossing the lost source bridge. The already-proved target-to-source "
            "cut inclusion and source-tree split compatibility exclude it, leaving "
            "one of the 204 pointwise-certified one-active directions."
        ),
        "directed_cut_inclusion_mechanism": (
            "A self-contained K3P displayed-tree specialization, the exact "
            "wrong-quartet 5x5 minor, the 808642-word balanced reduction, and "
            "the 379742-presentation reduced-palette replay prove "
            "Cut(Nprime) subset Cut(N) without a JC cut theorem or the legacy "
            "global-logic report."
        ),
        "validation": {
            "topology_directions_rebuilt": report["direction_count"],
            "proof_DAG_steps": report["proof_step_count"],
            "character_homomorphism_checks": report["character_homomorphism_checks"],
            "strict_convolution_product_terms": report["strict_convolution_product_terms"],
            "switching_weight_polynomial_checks": report["switching_weight_polynomial_checks"],
            "two_terminal_mixture_components_checked": report["two_terminal_mixture_components_checked"],
            "local_pointwise_targets_bound": report["local_targets_bound"],
            "local_pointwise_mutations_bound": report["local_mutations_bound"],
            "global_transfer_mutations_rejected": report["mutation_count"],
            "adversarial_manifest_rows_checked": manifest_rows,
            "adversarial_tree_colorings_checked": release["adversarial"]["tree_colorings_checked"],
            "adversarial_tree_counterexamples": release["adversarial"]["tree_counterexamples"],
            "adversarial_mutations_rejected": release["adversarial"]["mutation_count"],
            "fresh_direct_semantic_replay": "PASS",
            "fresh_adversarial_semantic_replay": "PASS",
            "release_ordinary_replay": "PASS",
            "release_optimized_replay": "PASS",
            "ordinary_replay": "PASS",
            "optimized_replay": "PASS",
        },
        "noncircularity": certificate["noncircularity"],
        "load_bearing_inputs": certificate["load_bearing_inputs"],
        "independent_adversarial_audit": {
            "status": "PASS",
            "remaining_gaps": [],
            "audit": binding(ADVERSARIAL_AUDIT),
            "verification_report": binding(ADVERSARIAL_REPORT),
            "mutation_report": binding(ADVERSARIAL_MUTATIONS),
            "manifest": binding(ADVERSARIAL_MANIFEST),
            "release_verifier": binding(RELEASE_VERIFIER),
            "release_report": binding(RELEASE_REPORT),
            "release_optimized_report": binding(RELEASE_OPTIMIZED_REPORT),
            "claim_boundary": adversarial_audit["claim_boundary"],
        },
        "files": hashes,
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    temporary.replace(OUTPUT)
    manifest_files = FILES + ("THEOREM_MANIFEST.json",)
    lines = [f"{sha_file(HERE / name)}  {name}" for name in manifest_files]
    temporary_sha = SHA_OUTPUT.with_suffix(".sha256.tmp")
    temporary_sha.write_text("\n".join(lines) + "\n")
    temporary_sha.replace(SHA_OUTPUT)
    print(json.dumps({"status": "PASS", "files": len(manifest_files), "directions": 204}, sort_keys=True))


if __name__ == "__main__":
    main()
