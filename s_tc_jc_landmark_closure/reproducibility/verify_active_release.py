#!/usr/bin/env python3
"""Fail-closed semantic and hash checks for the final bioRxiv release."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
TITLE = (
    "Strong Tree-Childness Is a Sharp Identifiability Boundary for "
    "Level-2 Jukes-Cantor Networks"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def active_surface_checks(final, metadata) -> None:
    status = (PROJECT / "STATUS.md").read_text(encoding="utf-8")
    dependency = (PROJECT / "CLAIM_DEPENDENCY_GRAPH.md").read_text(encoding="utf-8")
    crosswalk = (PROJECT / "THEOREM_CERTIFICATE_CROSSWALK.md").read_text(
        encoding="utf-8"
    )
    for name, text in {
        "STATUS.md": status,
        "CLAIM_DEPENDENCY_GRAPH.md": dependency,
        "THEOREM_CERTIFICATE_CROSSWALK.md": crosswalk,
    }.items():
        require("FINAL OUTCOME A" in text, f"{name}: final outcome disagrees")
        require("Strong Tree-Childness Is a Sharp Identifiability Boundary" in text,
                f"{name}: manuscript title missing")
    require(final["outcome"] == metadata["outcome"] == "A",
            "machine-readable outcome is not A")
    require(final["status"] == metadata["status"] == "PROVED",
            "machine-readable status is not PROVED")
    require(final["title"] == metadata["title"] == TITLE,
            "machine-readable titles disagree")
    require(final["sharpness"]["omega"]["status"] ==
            metadata["omega_disposition"] == "OMEGA-PASS-ALL-(n)",
            "Omega disposition disagrees")
    require(re.fullmatch(r"[0-9a-f]{40}", metadata["release_source_commit"]),
            "release source commit is not sealed")
    require(final["release_source_commit"] == metadata["release_source_commit"],
            "active commit fields disagree")


def artifact_checks(metadata) -> None:
    required = {
        "manuscript_source", "bibliography", "main_pdf", "supplement_pdf",
        "source_zip", "pdf_visual_audit", "omega_record", "omega_reviewer", "theta_verifier",
        "final_referee_report", "quick_transcript", "full_transcript",
        "regenerate_transcript", "persistent_archive", "archive_checksum",
    }
    require(set(metadata["artifacts"]) == required,
            "release artifact inventory is incomplete or contains stale entries")
    release_manifest = REPO / "release_artifacts/RELEASE_ASSET_SHA256SUMS"
    manifest_text = release_manifest.read_text(encoding="utf-8") if release_manifest.is_file() else ""
    for name, record in metadata["artifacts"].items():
        path = (REPO / record["path"]).resolve()
        if path.is_file():
            require(sha256(path) == record["sha256"],
                    f"release artifact hash changed: {name}")
        else:
            require(record.get("distribution") == "release_asset",
                    f"repository artifact missing: {name}: {record['path']}")
            commitment = f"{record['sha256']}  {record['path']}"
            require(commitment in manifest_text.splitlines(),
                    f"release-asset commitment missing: {name}")


def manuscript_checks() -> None:
    paper = (PROJECT / "source/paper/main.tex").read_text(encoding="utf-8")
    required = [
        r"\begin{theorem}[Strong-class classification]",
        r"N\preceqjc N'",
        "There is no proper one-sided",
        r"\begin{theorem}[Triangle-free sharpness]",
        r"\Omega_n,\Omega_n'\in\TCw\setminus\TCs",
        "dimension is $9+2(n-4)=2n+1$",
        r"\begin{theorem}[Theta pendant-transfer sharpness]",
        "does not recover physical bridge multipliers",
        "intersection of this ambient incidence orbit",
        "the slice tensors need not themselves be physical",
        "Theorem~2.2.1",
        "Sections~2.8--2.9",
        "choose the lexicographically least one",
        "Proposition~2.15",
        r"\texttt{omega\_audit/}",
    ]
    for needle in required:
        require(needle in paper, f"paper scope/proof phrase missing: {needle}")
    prohibited = [
        "physical bridge multipliers are identifiable",
        "Theta is an S_TC move",
        "complete open stochastic images are equal",
        "every rooted network that can collapse to the same final mixed graph",
    ]
    compact = " ".join(paper.split())
    for phrase in prohibited:
        require(phrase not in compact, f"withdrawn claim leaked into paper: {phrase}")
    require("/Users/" not in paper, "absolute local path leaked into manuscript")


def component_checks() -> None:
    universe = load_json(
        PROJECT / "reviews/n3_universe_generator/n3_universe_certificate.json"
    )
    require(universe["status"] == "VERIFIED" and
            universe["counts"]["raw_necessary_relations"] == 10826 and
            universe["counts"]["canonical_merged_relations"] == 10466 and
            all(universe["checks"].values()), "three-outgoing universe changed")

    quotient = load_json(
        PROJECT / "reviews/theta2_signature_gate/canonical_quotient_certificate.json"
    )
    require(quotient["status"] == "VERIFIED" and
            quotient["intrinsic_partition"] == {
                "direct_no_omitted_roles": 18,
                "nonretaining_marginalized_incoming": 132,
                "nonretaining_selected_incoming": 42,
            }, "four-outgoing partition changed")

    direct = load_json(
        PROJECT / "reviews/direct_anchor_probe_closure/certificates/summary.json"
    )
    require(direct["status"] == "EXACTLY_COMPUTED" and
            direct["counts"]["anchors"] == 62 and
            direct["counts"]["A_plus_p"] == 2642 and
            direct["counts"]["A_plus_p_plus_q"] == 18224 and
            direct["separator_search"]["unresolved"] == [],
            "direct-anchor closure changed")

    compact = load_json(
        PROJECT /
        "reviews/compact_probe_clean_clone_gate/certificates/compact_only_semantic_replay.json"
    )
    families = {row["family"]: row for row in compact["families"]}
    require(compact["status"] == "VERIFIED" and
            sum(families["n3"]["classification_counts"].values()) == 101148 and
            sum(families["theta2_n4"]["classification_counts"].values()) == 168582 and
            families["theta2_n4"]["maximum_probe_port_count"] == 10,
            "coherent-probe certificate changed")

    triangle = load_json(PROJECT / "primary/certificates/jc_triangle_redirection_active.json")
    require(triangle["status"] == "VERIFIED" and
            triangle["stochastic_conclusion"]["complete_open_stochastic_image_equality"] ==
            "NOT CLAIMED", "ordinary triangle scope changed")

    omega = load_json(REPO / "omega_audit/independent/output/omega_release_audit.json")
    require(omega["status"] == "OMEGA-PASS-ALL-(n)" and
            omega["all_n"]["dimension_formula"] == "2*n+1" and
            omega["stochastic"]["local_dimensions"] == {
                "M_Omega": 9, "M_Omega_prime": 9,
                "intersection_at_common_point": 9,
            } and len(omega["mandatory_mutations"]) == 12 and
            all(row["rejected"] for row in omega["mandatory_mutations"]),
            "Omega release record changed")
    for topology in omega["topology"].values():
        require(topology["admissible_rooting_count"] == 7 and
                topology["tree_child_rooting_count"] == 2 and
                topology["statistics"]["cycle_lengths"] == [4, 4, 6],
                "Omega topology census changed")


def release_review_checks() -> None:
    report = PROJECT / "reviews/final_biorxiv_referee/REPORT.md"
    require(report.is_file(), "final bioRxiv adversarial report missing")
    text = report.read_text(encoding="utf-8")
    require("VERIFIED" in text and "NO LOAD-BEARING DEFECT" in text.upper(),
            "final bioRxiv referee did not issue a verified verdict")


def main() -> None:
    final = load_json(PROJECT / "FINAL_OUTCOME.json")
    metadata = load_json(PROJECT / "RELEASE_METADATA.json")
    active_surface_checks(final, metadata)
    artifact_checks(metadata)
    manuscript_checks()
    component_checks()
    release_review_checks()
    print(json.dumps({
        "status": "VERIFIED",
        "outcome": "A",
        "release_source_commit": metadata["release_source_commit"],
        "omega": metadata["omega_disposition"],
        "main_pdf_sha256": metadata["artifacts"]["main_pdf"]["sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FALSE: {exc}", file=sys.stderr)
        raise
