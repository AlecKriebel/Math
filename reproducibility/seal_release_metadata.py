#!/usr/bin/env python3
"""Seal Outcome-A metadata against the source commit and release artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


REPO = Path(__file__).resolve().parents[1]
PROJECT = REPO / "s_tc_jc_landmark_closure"


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    source_commit = subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{args.source_commit}^{{commit}}"],
        cwd=REPO,
        text=True,
    ).strip()

    metadata_path = PROJECT / "RELEASE_METADATA.json"
    final_path = PROJECT / "FINAL_OUTCOME.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    final = json.loads(final_path.read_text(encoding="utf-8"))

    artifacts = {
        "manuscript_source": record("s_tc_jc_landmark_closure/source/paper/main.tex"),
        "bibliography": record("s_tc_jc_landmark_closure/source/paper/references.bib"),
        "main_pdf": record("biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC.pdf"),
        "supplement_pdf": record("biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf"),
        "source_zip": record("biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_source.zip"),
        "pdf_visual_audit": record("release/final_biorxiv/PDF_VISUAL_AUDIT.md"),
        "omega_record": record("omega_audit/independent/output/omega_release_audit.json"),
        "omega_reviewer": record("omega_audit/reports/ADVERSARIAL_O6_REVIEW.md"),
        "theta_verifier": record("s_tc_jc_sharp_boundary/reproducibility/verify_release.py"),
        "final_referee_report": record("s_tc_jc_landmark_closure/reviews/final_biorxiv_referee/REPORT.md"),
        "quick_transcript": record(
            "release_artifacts/clean_clone_transcripts/verify_quick.log",
            distribution="release_asset",
        ),
        "full_transcript": record(
            "release_artifacts/clean_clone_transcripts/verify_full.log",
            distribution="release_asset",
        ),
        "regenerate_transcript": record(
            "release_artifacts/clean_clone_transcripts/verify_regenerate_all.log",
            distribution="release_asset",
        ),
        "persistent_archive": record(
            "release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz",
            distribution="release_asset",
        ),
        "archive_checksum": record(
            "release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz.sha256"
        ),
    }

    external_names = {
        key for key, value in artifacts.items() if value["distribution"] == "release_asset"
    }
    manifest_lines = [
        f"{artifacts[key]['sha256']}  {artifacts[key]['path']}"
        for key in sorted(external_names)
    ]
    release_manifest = REPO / "release_artifacts/RELEASE_ASSET_SHA256SUMS"
    release_manifest.parent.mkdir(parents=True, exist_ok=True)
    release_manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    metadata["release_source_commit"] = source_commit
    metadata["artifacts"] = artifacts
    final["release_source_commit"] = source_commit
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    final_path.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "SEALED",
        "source_commit": source_commit,
        "artifacts": len(artifacts),
        "external_manifest": str(release_manifest.relative_to(REPO)),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
