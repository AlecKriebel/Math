#!/usr/bin/env python3
"""Create the non-self-referential core manifest and outer release envelope."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
RELEASE = PROJECT / "release_artifacts"
ARCHIVE = RELEASE / "stc_jc_sharp_boundary_reproducibility.tar.gz"
ARCHIVE_PREFIX = "stc_jc_sharp_boundary_reproducibility"
SOURCE_BINDING = {
    "scheme": "certificate-bundle-envelope-v1",
    "archive_marker": "ACTIVE_MANIFEST.json",
    "outer_envelope": "release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json",
    "description": (
        "The curated certificate archive carries its clean immutable source "
        "commit in ACTIVE_MANIFEST.json; the external envelope binds that "
        "commit, the archive bytes, and the archive SHA-256."
    ),
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def record(path: str, *, distribution: str = "repository") -> dict[str, str]:
    target = REPO / path
    if not target.is_file():
        raise FileNotFoundError(target)
    return {"path": path, "sha256": digest(target), "distribution": distribution}


def core_artifacts() -> dict[str, dict[str, str]]:
    return {
        "manuscript_source": record("s_tc_jc_landmark_closure/source/paper/main.tex"),
        "bibliography": record("s_tc_jc_landmark_closure/source/paper/references.bib"),
        "supplement_source": record(
            "s_tc_jc_landmark_closure/source/supplement/supplement.tex"
        ),
        "main_pdf": record("s_tc_jc_landmark_closure/biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC.pdf"),
        "supplement_pdf": record(
            "s_tc_jc_landmark_closure/biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf"
        ),
        "source_zip": record(
            "s_tc_jc_landmark_closure/biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_source.zip"
        ),
        "biorxiv_verifier_capsule": record(
            "s_tc_jc_landmark_closure/biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_verifier_entrypoints.zip"
        ),
        "pdf_visual_audit": record("s_tc_jc_landmark_closure/release/final_biorxiv/PDF_VISUAL_AUDIT.md"),
        "omega_record": record("s_tc_jc_landmark_closure/omega_audit/independent/output/omega_release_audit.json"),
        "omega_reviewer": record("s_tc_jc_landmark_closure/omega_audit/reports/ADVERSARIAL_O6_REVIEW.md"),
        "theta_verifier": record("s_tc_jc_landmark_closure/s_tc_jc_sharp_boundary/reproducibility/verify_release.py"),
        "v1_1_primary_report": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_proof_hardening/PRIMARY_REVISION_REPORT.md"
        ),
        "v1_1_adversarial_review": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_proof_hardening/ADVERSARIAL_REVIEW.md"
        ),
        "v1_1_repair_response": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_proof_hardening/REPAIR_RESPONSE.md"
        ),
        "v1_1_noncut_verifier": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_proof_hardening/verify_noncut_compression.py"
        ),
        "v1_1_endpoint_verifier": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_proof_hardening/verify_endpoint_and_analytic_regressions.py"
        ),
        "zero_sum_descriptor_verifier": record(
            "s_tc_jc_landmark_closure/reviews/zero_sum_descriptor_cleanroom/cleanroom_verifier.py"
        ),
        "v1_1_1_referee_regression": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_1_referee_revision/verify_referee_regressions.py"
        ),
        "v1_1_1_referee_response": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_1_referee_revision/REFEREE_RESPONSE.md"
        ),
        "v1_1_1_adversarial_review": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_1_referee_revision/ADVERSARIAL_REVIEW.md"
        ),
        "core_atlas_figure": record(
            "s_tc_jc_landmark_closure/source/paper/figures/core_atlas.tex"
        ),
        "biorxiv_metadata": record(
            "s_tc_jc_landmark_closure/biorxiv_submission/BIORXIV_METADATA.md"
        ),
        "biorxiv_upload_map": record(
            "s_tc_jc_landmark_closure/biorxiv_submission/BIORXIV_UPLOAD_MAP.md"
        ),
        "biorxiv_human_checklist": record(
            "s_tc_jc_landmark_closure/biorxiv_submission/FINAL_HUMAN_CHECKLIST.md"
        ),
        "submission_sha256s": record(
            "s_tc_jc_landmark_closure/biorxiv_submission/SHA256SUMS"
        ),
        "journal_package_builder": record(
            "s_tc_jc_landmark_closure/reproducibility/build_journal_packages.py"
        ),
        "verifier_capsule_builder": record(
            "s_tc_jc_landmark_closure/reproducibility/build_verifier_entrypoint_capsule.py"
        ),
        "submission_source_archive_replay": record(
            "s_tc_jc_landmark_closure/reproducibility/verify_submission_source_archives.py"
        ),
        "public_release_verifier": record(
            "s_tc_jc_landmark_closure/reproducibility/verify_public_release.py"
        ),
        "release_hardening_regression": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_2_release_hardening/verify_release_hardening.py"
        ),
        "release_hardening_disposition": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_2_release_hardening/REVIEW_DISPOSITION.md"
        ),
        "release_hardening_math_review": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_2_release_hardening/ADVERSARIAL_MATHEMATICAL_SCOPE_REVIEW.md"
        ),
        "release_hardening_package_review": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_2_release_hardening/ADVERSARIAL_RELEASE_PACKAGE_REVIEW.md"
        ),
        "englander_revision_disposition": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_3_englander_revision/FEEDBACK_DISPOSITION.md"
        ),
        "englander_v4_crosswalk": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_3_englander_revision/ENGLANDER_V4_CROSSWALK.md"
        ),
        "englander_revision_regression": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_3_englander_revision/verify_englander_revision.py"
        ),
        "v1_1_3_mathematical_review": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_3_englander_revision/ADVERSARIAL_MATHEMATICAL_REVIEW.md"
        ),
        "v1_1_3_reproducibility_review": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_3_englander_revision/ADVERSARIAL_REPRODUCIBILITY_REVIEW.md"
        ),
        "theta_pair_figure": record(
            "s_tc_jc_landmark_closure/source/paper/figures/theta_pair.tex"
        ),
        "v1_1_4_disposition": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_4_bcr_and_figure_revision/FEEDBACK_DISPOSITION.md"
        ),
        "v1_1_4_bcr_audit": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_4_bcr_and_figure_revision/BCR_CITATION_AUDIT.md"
        ),
        "v1_1_4_bcr_record": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_4_bcr_and_figure_revision/BCR_SOURCE_AUDIT.json"
        ),
        "v1_1_4_revision_regression": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_4_bcr_and_figure_revision/verify_v1_1_4_revision.py"
        ),
        "v1_1_4_mathematical_review": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_4_bcr_and_figure_revision/ADVERSARIAL_MATHEMATICAL_REVIEW.md"
        ),
        "v1_1_4_release_review": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_4_bcr_and_figure_revision/ADVERSARIAL_RELEASE_REVIEW.md"
        ),
        "v1_1_5_disposition": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_5_referee_repair/FEEDBACK_DISPOSITION.md"
        ),
        "v1_1_5_revision_regression": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_5_referee_repair/verify_referee_repairs.py"
        ),
        "v1_1_5_mathematical_review": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_5_referee_repair/ADVERSARIAL_MATHEMATICAL_REVIEW.md"
        ),
        "v1_1_5_release_review": record(
            "s_tc_jc_landmark_closure/reviews/v1_1_5_referee_repair/ADVERSARIAL_RELEASE_REVIEW.md"
        ),
        "prior_work_comparison": record(
            "s_tc_jc_landmark_closure/PRIOR_WORK_COMPARISON.md"
        ),
        "public_release_assets": record(
            "s_tc_jc_landmark_closure/release/PUBLIC_RELEASE_ASSETS.md"
        ),
        "release_upload_instructions": record(
            "s_tc_jc_landmark_closure/release/UPLOAD_RELEASE_ASSETS.md"
        ),
        "submission_package_index": record(
            "s_tc_jc_landmark_closure/SUBMISSION_PACKAGE_INDEX.md"
        ),
        "superseded_history_manifest": record(
            "s_tc_jc_landmark_closure/history/superseded_release_evidence/outcome_p_2026-08-13/SHA256SUMS"
        ),
        "systematic_biology_main_pdf": record(
            "s_tc_jc_landmark_closure/journal_submission/systematic_biology/SB_Main_Manuscript.pdf"
        ),
        "systematic_biology_supplement_pdf": record(
            "s_tc_jc_landmark_closure/journal_submission/systematic_biology/SB_Supplementary_Material.pdf"
        ),
        "systematic_biology_cover_letter": record(
            "s_tc_jc_landmark_closure/journal_submission/systematic_biology/SB_Cover_Letter.pdf"
        ),
        "systematic_biology_source_zip": record(
            "s_tc_jc_landmark_closure/journal_submission/systematic_biology/SB_LaTeX_Source.zip"
        ),
        "systematic_biology_verifier_capsule": record(
            "s_tc_jc_landmark_closure/journal_submission/systematic_biology/SB_Exact_Verifier_Entry_Points.zip"
        ),
        "systematic_biology_upload_map": record(
            "s_tc_jc_landmark_closure/journal_submission/systematic_biology/SYSTEMATIC_BIOLOGY_UPLOAD_MAP.md"
        ),
        "systematic_biology_sha256s": record(
            "s_tc_jc_landmark_closure/journal_submission/systematic_biology/SHA256SUMS"
        ),
        "jmb_main_pdf": record(
            "s_tc_jc_landmark_closure/journal_submission/journal_of_mathematical_biology/JMB_Main_Manuscript.pdf"
        ),
        "jmb_supplement_pdf": record(
            "s_tc_jc_landmark_closure/journal_submission/journal_of_mathematical_biology/JMB_Supplementary_Information.pdf"
        ),
        "jmb_cover_letter": record(
            "s_tc_jc_landmark_closure/journal_submission/journal_of_mathematical_biology/JMB_Cover_Letter.pdf"
        ),
        "jmb_source_zip": record(
            "s_tc_jc_landmark_closure/journal_submission/journal_of_mathematical_biology/JMB_LaTeX_Source.zip"
        ),
        "jmb_verifier_capsule": record(
            "s_tc_jc_landmark_closure/journal_submission/journal_of_mathematical_biology/JMB_Exact_Verifier_Entry_Points.zip"
        ),
        "jmb_upload_map": record(
            "s_tc_jc_landmark_closure/journal_submission/journal_of_mathematical_biology/JMB_UPLOAD_MAP.md"
        ),
        "jmb_sha256s": record(
            "s_tc_jc_landmark_closure/journal_submission/journal_of_mathematical_biology/SHA256SUMS"
        ),
        "requirements_lock": record("s_tc_jc_landmark_closure/requirements.txt"),
    }


def seal_core() -> None:
    metadata_path = PROJECT / "RELEASE_METADATA.json"
    final_path = PROJECT / "FINAL_OUTCOME.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    final = json.loads(final_path.read_text(encoding="utf-8"))
    metadata.pop("release_source_commit", None)
    final.pop("release_source_commit", None)
    metadata["source_binding"] = SOURCE_BINDING
    final["source_binding"] = SOURCE_BINDING
    metadata["artifacts"] = core_artifacts()
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    final_path.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "CORE-SEALED",
        "artifacts": len(metadata["artifacts"]),
        "binding": SOURCE_BINDING["scheme"],
    }, sort_keys=True))


def resolve_commit(value: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{value}^{{commit}}"],
        cwd=REPO,
        text=True,
    ).strip()


def archive_member_bytes(name: str) -> bytes:
    with tarfile.open(ARCHIVE, "r:gz") as archive:
        member = archive.extractfile(f"{ARCHIVE_PREFIX}/{name}")
        if member is None:
            raise AssertionError(f"archive member missing: {name}")
        return member.read()


def transcript_record(name: str, source_commit: str) -> dict[str, str]:
    path = f"s_tc_jc_landmark_closure/release_artifacts/clean_clone_transcripts/{name}"
    target = REPO / path
    text = target.read_text(encoding="utf-8", errors="replace")
    required = [
        f"commit={source_commit}",
        "CLEAN_BEFORE=yes",
        "exit_status=0",
        "CLEAN_AFTER=yes",
    ]
    for needle in required:
        if needle not in text:
            raise AssertionError(f"{path}: missing {needle}")
    archived = archive_member_bytes(
        f"s_tc_jc_landmark_closure/release/final_biorxiv/transcripts/{name}"
    )
    if archived != target.read_bytes():
        raise AssertionError(f"archive transcript differs: {name}")
    return record(path, distribution="release_asset")


def seal_envelope(source_commit_arg: str) -> None:
    source_commit = resolve_commit(source_commit_arg)
    if not ARCHIVE.is_file():
        raise FileNotFoundError(ARCHIVE)
    marker = archive_member_bytes("ARCHIVE_SOURCE_COMMIT.txt").decode().strip()
    if marker != source_commit:
        raise AssertionError(("archive source commit", marker, source_commit))
    for relative in (
        "s_tc_jc_landmark_closure/RELEASE_METADATA.json",
        "s_tc_jc_landmark_closure/FINAL_OUTCOME.json",
    ):
        if archive_member_bytes(relative) != (REPO / relative).read_bytes():
            raise AssertionError(f"archive core metadata differs: {relative}")

    external = {
        "quick_transcript": transcript_record("verify_quick.log", source_commit),
        "full_transcript": transcript_record("verify_full.log", source_commit),
        "regenerate_transcript": transcript_record(
            "verify_regenerate_all.log", source_commit
        ),
        "persistent_archive": record(
            "s_tc_jc_landmark_closure/release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz",
            distribution="release_asset",
        ),
        "archive_checksum": record(
            "s_tc_jc_landmark_closure/release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz.sha256",
            distribution="release_asset",
        ),
    }
    final_report = "s_tc_jc_landmark_closure/release_artifacts/FINAL_RELEASE_ENGINEERING_REPORT.md"
    if not (REPO / final_report).is_file():
        raise FileNotFoundError(REPO / final_report)
    external["final_release_referee"] = record(
        final_report, distribution="release_asset"
    )

    envelope = {
        "schema": "stc-jc-external-release-envelope-v1",
        "status": "SEALED",
        "outcome": "A",
        "source_commit": source_commit,
        "core_metadata_sha256": digest(PROJECT / "RELEASE_METADATA.json"),
        "final_outcome_sha256": digest(PROJECT / "FINAL_OUTCOME.json"),
        "external_artifacts": external,
    }
    envelope_path = RELEASE / "RELEASE_ENVELOPE.json"
    envelope_path.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n")

    flat_records = {
        Path(value["path"]).name: value["sha256"]
        for value in external.values()
    }
    if len(flat_records) != len(external):
        raise AssertionError("release asset basenames are not unique")
    flat_records[envelope_path.name] = digest(envelope_path)
    manifest_lines = [
        f"{sha256}  {name}" for name, sha256 in sorted(flat_records.items())
    ]
    (RELEASE / "RELEASE_ASSET_SHA256SUMS").write_text(
        "\n".join(manifest_lines) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": "ENVELOPE-SEALED",
        "source_commit": source_commit,
        "external_artifacts": len(external),
        "archive_sha256": external["persistent_archive"]["sha256"],
    }, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)
    subparsers.add_parser("core")
    envelope = subparsers.add_parser("envelope")
    envelope.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    if args.mode == "core":
        seal_core()
    else:
        seal_envelope(args.source_commit)


if __name__ == "__main__":
    main()
