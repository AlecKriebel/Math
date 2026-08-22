#!/usr/bin/env python3
"""Fail-closed semantic and hash checks for the final bioRxiv release."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
TITLE = (
    "Strong Tree-Childness Is a Sharp Generic-Identifiability Boundary for "
    "Level-2 Jukes-Cantor Networks"
)
SOURCE_BINDING_SCHEME = "certificate-bundle-envelope-v1"
RELEASE_TAG = "stc-jc-sharp-boundary-v1.1.5"


def clean_git_environment() -> dict[str, str]:
    allowed = {"PATH", "LANG", "LC_ALL", "LC_CTYPE", "SYSTEMROOT"}
    environment = {
        key: value for key, value in os.environ.items() if key in allowed
    }
    environment["LC_ALL"] = "C"
    return environment


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


def archived_bundle_manifest(archive_path: Path) -> dict:
    with tarfile.open(archive_path, "r:gz") as archive:
        matches = [
            member for member in archive.getmembers()
            if member.name.endswith("/ACTIVE_MANIFEST.json") and member.isfile()
        ]
        require(len(matches) == 1,
                "certificate archive does not contain one active manifest")
        stream = archive.extractfile(matches[0])
        require(stream is not None, "cannot read archived active manifest")
        return json.loads(stream.read().decode("utf-8"))


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
        normalized = " ".join(text.split())
        require("FINAL OUTCOME A" in text, f"{name}: final outcome disagrees")
        require("Strong Tree-Childness Is a Sharp Generic-Identifiability Boundary"
                in normalized,
                f"{name}: manuscript title missing")
    require(all(node in dependency and node in crosswalk for node in
                ("V111", "V112", "V113", "V114", "V115")),
            "a v1.1.1--v1.1.5 release gate is absent from the dependency records")
    require(final["outcome"] == metadata["outcome"] == "A",
            "machine-readable outcome is not A")
    require(final["status"] == metadata["status"] == "PROVED",
            "machine-readable status is not PROVED")
    require(final["title"] == metadata["title"] == TITLE,
            "machine-readable titles disagree")
    require(final["release_revision"] == metadata["release_revision"] ==
            RELEASE_TAG, "release revision disagrees")
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
        "supplement_source", "source_zip", "biorxiv_verifier_capsule",
        "pdf_visual_audit", "omega_record",
        "omega_reviewer", "theta_verifier", "v1_1_primary_report",
        "v1_1_adversarial_review", "v1_1_repair_response",
        "v1_1_noncut_verifier", "v1_1_endpoint_verifier",
        "zero_sum_descriptor_verifier", "v1_1_1_referee_regression",
        "v1_1_1_referee_response", "v1_1_1_adversarial_review",
        "core_atlas_figure", "biorxiv_metadata", "submission_sha256s",
        "biorxiv_upload_map", "biorxiv_human_checklist",
        "journal_package_builder", "verifier_capsule_builder",
        "submission_source_archive_replay",
        "public_release_verifier", "release_hardening_regression",
        "release_hardening_disposition", "release_hardening_math_review",
        "release_hardening_package_review", "englander_revision_disposition",
        "englander_v4_crosswalk", "englander_revision_regression",
        "v1_1_3_mathematical_review", "v1_1_3_reproducibility_review",
        "prior_work_comparison", "public_release_assets",
        "release_upload_instructions", "submission_package_index",
        "superseded_history_manifest",
        "systematic_biology_main_pdf",
        "systematic_biology_supplement_pdf", "systematic_biology_cover_letter",
        "systematic_biology_source_zip", "systematic_biology_verifier_capsule",
        "systematic_biology_upload_map",
        "systematic_biology_sha256s", "jmb_main_pdf", "jmb_supplement_pdf",
        "jmb_cover_letter", "jmb_source_zip", "jmb_verifier_capsule",
        "jmb_upload_map", "jmb_sha256s",
        "requirements_lock", "theta_pair_figure", "v1_1_4_disposition",
        "v1_1_4_bcr_audit", "v1_1_4_bcr_record",
        "v1_1_4_revision_regression", "v1_1_4_mathematical_review",
        "v1_1_4_release_review",
        "v1_1_5_disposition", "v1_1_5_revision_regression",
        "v1_1_5_mathematical_review", "v1_1_5_release_review",
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
    certificate_envelope = PROJECT / "release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json"
    if certificate_envelope.is_file():
        envelope = load_json(certificate_envelope)
        require(envelope["schema"] == "stc-jc-certificate-bundle-envelope-v1" and
                envelope["version"] == "1.1.7" and
                envelope["source_tree_clean"] is True,
                "curated certificate envelope status changed")
        source_commit = envelope["source_commit"]
        require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
                "curated certificate source commit is invalid")
        commit_check = subprocess.run(
            ["git", "cat-file", "-e", f"{source_commit}^{{commit}}"],
            cwd=REPO,
            env=clean_git_environment(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        require(commit_check.returncode == 0,
                "curated certificate source commit is not a local Git object")
        archive = PROJECT / "release_artifacts" / envelope["archive"]
        sidecar = archive.with_suffix(archive.suffix + ".sha256")
        require(archive.is_file() and sidecar.is_file(),
                "curated certificate archive or sidecar missing")
        require(sha256(archive) == envelope["archive_sha256"],
                "curated certificate archive hash changed")
        require(sidecar.read_text(encoding="utf-8").split() ==
                [envelope["archive_sha256"], archive.name],
                "curated certificate sidecar changed")
        manifest = archived_bundle_manifest(archive)
        require(manifest["source_commit"] == source_commit and
                manifest["source_tree_clean"] is True and
                manifest["prepared_payload_sha256"] ==
                envelope["prepared_payload_sha256"],
                "archive manifest and external source envelope disagree")
        log_dir = PROJECT / "release_artifacts/certificate_bundle_logs"
        for name in ("verify_quick.log", "verify_full.log",
                     "verify_regenerate_all.log"):
            log = log_dir / name
            require(log.is_file(), f"curated certificate transcript missing: {name}")
            text = log.read_text(encoding="utf-8", errors="replace")
            require(f"source_commit={source_commit}" in text and
                    "exit_status=0" in text,
                    f"curated certificate transcript is not source-bound: {name}")
        return source_commit
    envelope_path = PROJECT / "release_artifacts/RELEASE_ENVELOPE.json"
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
        manifest_path = PROJECT / "release_artifacts/RELEASE_ASSET_SHA256SUMS"
        require(manifest_path.is_file(), "outer release-asset manifest missing")
        manifest_rows = manifest_path.read_text(encoding="utf-8").splitlines()
        manifest = {}
        for row in manifest_rows:
            match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", row)
            require(match is not None, f"malformed public release-manifest row: {row}")
            value, basename = match.groups()
            require(basename not in manifest,
                    f"duplicate public release-manifest name: {basename}")
            manifest[basename] = value
        expected_public = {
            Path(record["path"]).name: record["sha256"]
            for record in envelope["external_artifacts"].values()
        }
        require(len(expected_public) == len(envelope["external_artifacts"]),
                "external release asset basenames collide")
        expected_public["RELEASE_ENVELOPE.json"] = sha256(envelope_path)
        require(manifest == expected_public,
                "public flat release manifest is incomplete or stale")
        for name, record in envelope["external_artifacts"].items():
            target = REPO / record["path"]
            require(target.is_file(), f"external release artifact missing: {name}")
            require(sha256(target) == record["sha256"],
                    f"external release artifact hash changed: {name}")
        for name in ("verify_quick.log", "verify_full.log", "verify_regenerate_all.log"):
            transcript_checks(
                PROJECT / "release_artifacts/clean_clone_transcripts" / name,
                source_commit,
            )
        sidecar = PROJECT / "release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz.sha256"
        archive = PROJECT / "release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz"
        require(sidecar.read_text(encoding="utf-8").split()[0] == sha256(archive),
                "persistent-archive sidecar changed")
        return source_commit
    if archive_marker.is_file():
        source_commit = archive_marker.read_text(encoding="utf-8").strip()
        require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
                "archive source-commit marker is invalid")
        transcript_dir = PROJECT / "release/final_biorxiv/transcripts"
        for name in ("verify_quick.log", "verify_full.log", "verify_regenerate_all.log"):
            transcript_checks(transcript_dir / name, source_commit)
        return source_commit
    # A bare source checkout is not a sealed release.  The fallback is accepted
    # only when the exact advertised annotated tag peels to this clean commit.
    # This makes deletion of the external envelope fail closed before tagging,
    # while allowing the immutable public source tag to be verified without
    # downloading the separately distributed large archive.
    try:
        source_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, text=True,
            env=clean_git_environment(),
        ).strip()
        status = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=REPO,
            text=True,
            env=clean_git_environment(),
        )
        tag_type = subprocess.check_output(
            ["git", "cat-file", "-t", f"refs/tags/{RELEASE_TAG}"],
            cwd=REPO,
            text=True,
            stderr=subprocess.DEVNULL,
            env=clean_git_environment(),
        ).strip()
        tagged_commit = subprocess.check_output(
            ["git", "rev-parse", f"{RELEASE_TAG}^{{commit}}"],
            cwd=REPO,
            text=True,
            env=clean_git_environment(),
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
    compact = " ".join(paper.split())
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
        r"P_v(0,\ldots,0)=1",
        "componentwise normalized tensor locus",
        "the slice tensors need not themselves be physical",
        r"\{Y_\tau\}_{\tau\in\mathcal T}",
        r"\phi_{\rm selected}\circ\delta_R",
        "certificate assigns every canonical decorated directed relation",
        "orbit rows $(A,B,C,D,E,F)$ and columns",
        "Theorem~2.2.1, applied iteratively",
        "Proposition~2.8.5(i), applied to the finite atlas",
        "Theorem~2.8.8",
        r"\newcommand{\preceqproj}",
        r"\PM_H\preceqproj\PM_{H'}",
        "choose the lexicographically least one",
        "Proposition~2.15",
        "type~(2c)",
        "contains no type-(2c)-versus-type-(2c) distinction",
        r"\mathcal I_{\mathrm{tri}}",
        "denoted $q_{111}$",
        "HoltgrefeEtAl2025Quartets",
        "displayed-rooting source and target minors listed with their",
        r"\path{sharpness/omega/}",
        r"\path{atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz}",
        "both have zero survivors",
        "$72$ active-labelled tensors",
        "same zero-sum JC indicator",
        "selected split mask with its complement",
        "Discard the all-zero signature",
        "not an independent human review",
        "complete central singleton-signature edge class",
        "three monochromatic runs $c,d,c$",
        "No target parameter section is chosen",
        r"C(g;\mathbf h,c)\overline Q_u(\mathbf h)",
        "one-dimensional representative slice",
        "$df_i$ has rank one",
        "three effective boundary scales $\\mathbf z$ retain all four",
        "no application of \\cref{lem:product-chart}",
    ]
    for needle in required:
        require(needle in compact, f"paper scope/proof phrase missing: {needle}")
    prohibited = [
        "physical bridge multipliers are identifiable",
        "Theta is an S_TC move",
        "complete open stochastic images are equal",
        "every rooted network that can collapse to the same final mixed graph",
        "Distinct complete mask rows give distinct selected edge coordinates",
    ]
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

    omega = load_json(PROJECT / "omega_audit/independent/output/omega_release_audit.json")
    require(omega["status"] == "OMEGA-PASS-ALL-(n)" and
            omega["all_n"]["dimension_formula"] == "2*n+1" and
            omega["stochastic"]["local_dimensions"] == {
                "M_Omega": 9, "M_Omega_prime": 9,
                "intersection_at_common_point": 9,
            } and len(omega["mandatory_mutations"]) == 12 and
            all(row["rejected"] for row in omega["mandatory_mutations"]),
            "Omega release record changed")
    require(
        omega["stochastic"]["exact_common_parameter_vectors"] == {
            "order": "e_0,...,e_11,lambda_V,lambda_X0",
            "vectors": {
                "N16_source": [
                    "1/2", "1/4", "1/2", "1/2", "1/2", "1/2", "1/2",
                    "1/20", "1/2", "1/2", "1/10", "1/2", "1/2", "1/2",
                ],
                "N16_target": [
                    "7/12", "1/7", "1/2", "41/48", "28/41", "1/2", "1/2",
                    "12/205", "1/2", "1/2", "3/40", "1/2", "1/2", "1/2",
                ],
                "N26_source": [
                    "1/4", "1/2", "1/2", "3/4", "2/3", "1/4", "1/2",
                    "1/20", "1/2", "1/2", "1/10", "1/2", "1/2", "1/2",
                ],
                "N26_target": [
                    "1/7", "1/2", "41/48", "19/24", "14/19", "14/41", "1/2",
                    "12/205", "1/2", "1/2", "3/40", "1/2", "1/2", "1/2",
                ],
            },
        },
        "Omega exact common parameter vectors changed",
    )
    for topology in omega["topology"].values():
        require(topology["admissible_rooting_count"] == 7 and
                topology["tree_child_rooting_count"] == 2 and
                topology["statistics"]["cycle_lengths"] == [4, 4, 6],
                "Omega topology census changed")

    cut_reduction = load_json(
        PROJECT / "independent/bridge_cut/palette_reduction_certificate.json"
    )
    require(
        cut_reduction["failure_count"] == 0
        and cut_reduction["totals"] == {
            "balanced_total": 808642,
            "direct_palette": 544350,
            "singleton_doubled_palette": 34304,
            "three_run_path_obstruction": 229988,
        },
        "arbitrary-word cut reduction changed",
    )
    cut_cleanroom = load_json(
        PROJECT / "reviews/global_bridge/palette_cleanroom_certificate.json"
    )
    require(
        cut_cleanroom["total_valid_palette_presentations"] == 379742
        and cut_cleanroom["survivor_count"] == 0,
        "clean-room cut-palette replay changed",
    )

    parameter = load_json(
        PROJECT / "reviews/root_probe/parameter_submersion_certificate.json"
    )
    require(
        parameter["completion_count"] == 42908
        and parameter["full_row_rank_failure_count"] == 0
        and parameter["normalization_mutation_tests"][
            "all_mutations_rejected"
        ],
        "split-normalized submersion certificate changed",
    )
    probe = load_json(PROJECT / "reviews/root_probe/probe_coherence_certificate.json")
    require(
        probe["one_port_ambiguity_group_count"] == 372
        and probe["one_port_max_two_port_completion_multiplicity"] == 2
        and "coherence_collision_count" not in probe,
        "honest one-port ambiguity diagnostic changed",
    )

    omega_rank = load_json(
        PROJECT / "omega_audit/independent/output/omega_rank_readability.json"
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
    for name in (
        "ADVERSARIAL_MATHEMATICAL_SCOPE_REVIEW.md",
        "ADVERSARIAL_RELEASE_PACKAGE_REVIEW.md",
    ):
        current = PROJECT / "reviews/v1_1_2_release_hardening" / name
        require(current.is_file(), f"v1.1.2 adversarial review missing: {name}")
        review_text = current.read_text(encoding="utf-8").rstrip()
        require(review_text.endswith("PASS") and "HOLD" not in review_text.splitlines()[-1],
                f"v1.1.2 adversarial review did not pass: {name}")
    for name in (
        "ADVERSARIAL_MATHEMATICAL_REVIEW.md",
        "ADVERSARIAL_REPRODUCIBILITY_REVIEW.md",
    ):
        current = PROJECT / "reviews/v1_1_3_englander_revision" / name
        require(current.is_file(), f"v1.1.3 adversarial review missing: {name}")
        review_text = current.read_text(encoding="utf-8").rstrip()
        require(review_text.endswith("PASS"),
                f"v1.1.3 adversarial review did not pass: {name}")
    for name in (
        "ADVERSARIAL_MATHEMATICAL_REVIEW.md",
        "ADVERSARIAL_RELEASE_REVIEW.md",
    ):
        current = PROJECT / "reviews/v1_1_4_bcr_and_figure_revision" / name
        require(current.is_file(), f"v1.1.4 adversarial review missing: {name}")
        review_text = current.read_text(encoding="utf-8").rstrip()
        require(review_text.endswith("PASS"),
                f"v1.1.4 adversarial review did not pass: {name}")
    for name in (
        "ADVERSARIAL_MATHEMATICAL_REVIEW.md",
        "ADVERSARIAL_RELEASE_REVIEW.md",
    ):
        current = PROJECT / "reviews/v1_1_5_referee_repair" / name
        require(current.is_file(), f"v1.1.5 adversarial review missing: {name}")
        review_text = current.read_text(encoding="utf-8").rstrip()
        require(review_text.endswith("PASS"),
                f"v1.1.5 adversarial review did not pass: {name}")


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
