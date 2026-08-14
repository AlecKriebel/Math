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


REPO = Path(__file__).resolve().parents[1]
PROJECT = REPO / "s_tc_jc_landmark_closure"
RELEASE = REPO / "release_artifacts"
ARCHIVE = RELEASE / "stc_jc_sharp_boundary_reproducibility.tar.gz"
ARCHIVE_PREFIX = "stc_jc_sharp_boundary_reproducibility"
SOURCE_BINDING = {
    "scheme": "external-envelope-v1",
    "archive_marker": "ARCHIVE_SOURCE_COMMIT.txt",
    "outer_envelope": "release_artifacts/RELEASE_ENVELOPE.json",
    "description": (
        "The core manifest is commit-independent and lives inside the archive; "
        "the outer envelope binds the immutable source commit and archive hash."
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
        "main_pdf": record("biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC.pdf"),
        "supplement_pdf": record(
            "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf"
        ),
        "source_zip": record(
            "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_source.zip"
        ),
        "pdf_visual_audit": record("release/final_biorxiv/PDF_VISUAL_AUDIT.md"),
        "omega_record": record("omega_audit/independent/output/omega_release_audit.json"),
        "omega_reviewer": record("omega_audit/reports/ADVERSARIAL_O6_REVIEW.md"),
        "theta_verifier": record("s_tc_jc_sharp_boundary/reproducibility/verify_release.py"),
        "final_mathematical_referee": record(
            "s_tc_jc_landmark_closure/reviews/final_biorxiv_referee/REPORT.md"
        ),
        "preseal_release_hold": record(
            "s_tc_jc_landmark_closure/reviews/final_release_engineering/PRESEAL_HOLD.md"
        ),
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
    path = f"release_artifacts/clean_clone_transcripts/{name}"
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
    archived = archive_member_bytes(f"release/final_biorxiv/transcripts/{name}")
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
            "release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz",
            distribution="release_asset",
        ),
        "archive_checksum": record(
            "release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz.sha256"
        ),
    }
    final_report = (
        "s_tc_jc_landmark_closure/reviews/final_release_engineering/REPORT.md"
    )
    if (REPO / final_report).is_file():
        external["final_release_referee"] = record(final_report)

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

    manifest_lines = [
        f"{value['sha256']}  {value['path']}"
        for _, value in sorted(external.items())
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
