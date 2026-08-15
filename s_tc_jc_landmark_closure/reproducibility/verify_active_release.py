#!/usr/bin/env python3
"""Fail-closed semantic and hash checks for the final bioRxiv release."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
TITLE = (
    "Strong Tree-Childness Is a Sharp Identifiability Boundary for "
    "Level-2 Jukes-Cantor Networks"
)
SOURCE_BINDING_SCHEME = "external-envelope-v1"
RELEASE_TAG = "stc-jc-sharp-boundary-v1.1.0"


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
    require(final["sharpness"]["omega"]["common_regular_overlap_dimension"] ==
            "2n+1", "Omega dimension changed")
    require(final["sharpness"]["theta"]["common_regular_overlap_dimension"] ==
            "2n", "Theta dimension changed")
    require(final["source_binding"] == metadata["source_binding"] and
            metadata["source_binding"]["scheme"] == SOURCE_BINDING_SCHEME,
            "non-self-referential source binding disagrees")


def artifact_checks(metadata) -> None:
    required = {
        "manuscript_source", "bibliography", "main_pdf", "supplement_pdf",
        "supplement_source", "source_zip", "pdf_visual_audit", "omega_record",
        "omega_reviewer", "theta_verifier", "v1_1_primary_report",
        "v1_1_adversarial_review", "v1_1_repair_response",
        "v1_1_noncut_verifier", "v1_1_endpoint_verifier",
        "zero_sum_descriptor_verifier",
    }
    require(set(metadata["artifacts"]) == required,
            "release artifact inventory is incomplete or contains stale entries")
    for name, record in metadata["artifacts"].items():
        path = (REPO / record["path"]).resolve()
        require(path.is_file(), f"core artifact missing: {name}: {record['path']}")
        require(sha256(path) == record["sha256"],
                f"core artifact hash changed: {name}")


def transcript_checks(path: Path, source_commit: str) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    for needle in (
        f"commit={source_commit}", "CLEAN_BEFORE=yes", "exit_status=0",
        "CLEAN_AFTER=yes",
    ):
        require(needle in text, f"{path}: missing {needle}")


def source_envelope_checks(final, metadata) -> str:
    """Verify an outer envelope, extracted archive, or immutable tagged source."""
    envelope_path = REPO / "release_artifacts/RELEASE_ENVELOPE.json"
    archive_marker = REPO / "ARCHIVE_SOURCE_COMMIT.txt"
    if envelope_path.is_file():
        envelope = load_json(envelope_path)
        source_commit = envelope["source_commit"]
        require(envelope["schema"] == "stc-jc-external-release-envelope-v1" and
                envelope["status"] == "SEALED" and envelope["outcome"] == "A",
                "outer release envelope status changed")
        require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
                "outer envelope source commit is invalid")
        require(envelope["core_metadata_sha256"] ==
                sha256(PROJECT / "RELEASE_METADATA.json"),
                "outer envelope core-metadata commitment changed")
        require(envelope["final_outcome_sha256"] ==
                sha256(PROJECT / "FINAL_OUTCOME.json"),
                "outer envelope final-outcome commitment changed")
        manifest_path = REPO / "release_artifacts/RELEASE_ASSET_SHA256SUMS"
        require(manifest_path.is_file(), "outer release-asset manifest missing")
        manifest = manifest_path.read_text(encoding="utf-8").splitlines()
        for name, record in envelope["external_artifacts"].items():
            target = REPO / record["path"]
            require(target.is_file(), f"external release artifact missing: {name}")
            require(sha256(target) == record["sha256"],
                    f"external release artifact hash changed: {name}")
            require(f"{record['sha256']}  {record['path']}" in manifest,
                    f"external manifest commitment missing: {name}")
        for name in ("verify_quick.log", "verify_full.log", "verify_regenerate_all.log"):
            transcript_checks(
                REPO / "release_artifacts/clean_clone_transcripts" / name,
                source_commit,
            )
        sidecar = REPO / "release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz.sha256"
        archive = REPO / "release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz"
        require(sidecar.read_text(encoding="utf-8").split()[0] == sha256(archive),
                "persistent-archive sidecar changed")
        return source_commit
    if archive_marker.is_file():
        source_commit = archive_marker.read_text(encoding="utf-8").strip()
        require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
                "archive source-commit marker is invalid")
        transcript_dir = REPO / "release/final_biorxiv/transcripts"
        for name in ("verify_quick.log", "verify_full.log", "verify_regenerate_all.log"):
            transcript_checks(transcript_dir / name, source_commit)
        return source_commit
    # A bare source checkout is not a sealed release.  The fallback is accepted
    # only when the exact advertised annotated tag peels to this clean commit.
    # This makes deletion of the external envelope fail closed before tagging,
    # while allowing the immutable public source tag to be verified without
    # downloading the separately distributed 338 MB archive.
    try:
        source_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
        ).strip()
        status = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=REPO,
            text=True,
        )
        tag_type = subprocess.check_output(
            ["git", "cat-file", "-t", f"refs/tags/{RELEASE_TAG}"],
            cwd=REPO,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        tagged_commit = subprocess.check_output(
            ["git", "rev-parse", f"{RELEASE_TAG}^{{commit}}"],
            cwd=REPO,
            text=True,
        ).strip()
    except Exception as exc:
        raise AssertionError(
            "no release envelope/archive marker and immutable release tag missing"
        ) from exc
    require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
            "source checkout commit is invalid")
    require(status == "", "tagged source checkout is not clean")
    require(tag_type == "tag", "release tag is not an annotated tag")
    require(tagged_commit == source_commit,
            "release tag does not peel to the checked-out source commit")
    return source_commit


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
        "Propositions~2.8.2, 2.8.4, 2.8.5, and",
        "Theorem~2.8.8",
        "choose the lexicographically least one",
        "Proposition~2.15",
        r"\texttt{omega\_audit/}",
        r"reviews/v1\_1\_proof\_hardening/",
        "has zero survivors",
        "$72$ active-labelled tensors",
        "same zero-sum JC indicator",
        "selected split mask with its complement",
        "Discard the all-zero signature",
        "not an independent human review",
    ]
    for needle in required:
        require(needle in paper, f"paper scope/proof phrase missing: {needle}")
    prohibited = [
        "physical bridge multipliers are identifiable",
        "Theta is an S_TC move",
        "complete open stochastic images are equal",
        "every rooted network that can collapse to the same final mixed graph",
        "Distinct complete mask rows give distinct selected edge coordinates",
    ]
    compact = " ".join(paper.split())
    for phrase in prohibited:
        require(phrase not in compact, f"withdrawn claim leaked into paper: {phrase}")
    require("/Users/" not in paper, "absolute local path leaked into manuscript")

    supplement = (PROJECT / "source/supplement/supplement.tex").read_text(
        encoding="utf-8"
    )
    for needle in (
        "For the source $K_4$", "x_{B1}", "(P,s,Q,t,R,u,v,S)",
        "(P',x,y,z,R',w,S',Q')", "root-edge factorization",
    ):
        require(needle in supplement, f"supplement proof data missing: {needle}")


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

    omega_rank = load_json(
        REPO / "omega_audit/independent/output/omega_rank_readability.json"
    )
    require(omega_rank["status"] == "EXACTLY COMPUTED" and
            omega_rank["core_jacobian_shape"] == [14, 10] and
            omega_rank["generic_core_rank"] == 6 and
            omega_rank["strict_point_minor"]["determinant"] ==
            "-723/8589934592" and
            omega_rank["euler_identities_checked"] == 14 and
            omega_rank["complete_rank_upper_bound"] == 9,
            "Omega readable rank certificate changed")


def release_review_checks() -> None:
    report = PROJECT / "reviews/v1_1_proof_hardening/ADVERSARIAL_REVIEW.md"
    require(report.is_file(), "v1.1 adversarial report missing")
    text = report.read_text(encoding="utf-8")
    require("No unresolved blocker" in text and
            "Outcome A was" in text and
            all(f"F{i}" in text for i in range(1, 5)),
            "v1.1 adversarial verdict is incomplete")
    response = PROJECT / "reviews/v1_1_proof_hardening/REPAIR_RESPONSE.md"
    require(response.is_file(), "v1.1 repair response missing")
    response_text = response.read_text(encoding="utf-8")
    require(all(f"F{i}" in response_text for i in range(1, 5)) and
            "No theorem statement" in response_text,
            "v1.1 repair response is incomplete")


def main() -> None:
    final = load_json(PROJECT / "FINAL_OUTCOME.json")
    metadata = load_json(PROJECT / "RELEASE_METADATA.json")
    active_surface_checks(final, metadata)
    artifact_checks(metadata)
    source_commit = source_envelope_checks(final, metadata)
    manuscript_checks()
    component_checks()
    release_review_checks()
    print(json.dumps({
        "status": "VERIFIED",
        "outcome": "A",
        "source_commit": source_commit,
        "omega": metadata["omega_disposition"],
        "main_pdf_sha256": metadata["artifacts"]["main_pdf"]["sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FALSE: {exc}", file=sys.stderr)
        raise
