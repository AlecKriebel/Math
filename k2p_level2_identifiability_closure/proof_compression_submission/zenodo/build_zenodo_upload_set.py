#!/usr/bin/env python3
"""Build and validate the seven-file Zenodo upload set."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import build_zenodo_reproducibility_package as reproducibility
import verify_zenodo_reproducibility_package as checker


PROJECT = Path(__file__).resolve().parents[2]
REPRODUCIBILITY_NAME = "K2P_SAME_Reproducibility_Package_v1.0.5-r1.zip"
DEPOSIT_MANIFEST_NAME = "K2P_SAME_Zenodo_Manifest_v1.0.5-r1.json"
CHECKSUM_NAME = "SHA256SUMS"
UPLOAD_SOURCES = {
    "K2P_SAME_Principal_Domain_Article.pdf": (
        "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
        "article PDF",
        "application/pdf",
        "CC-BY-4.0",
    ),
    "K2P_SAME_Reader_Supplement.pdf": (
        "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
        "reader supplement PDF",
        "application/pdf",
        "CC-BY-4.0",
    ),
    "K2P_SAME_bioRxiv_Source_20260829.zip": (
        "proof_compression_submission/output/K2P_SAME_bioRxiv_Source_20260829.zip",
        "compile-complete bioRxiv source archive",
        "application/zip",
        "CC-BY-4.0",
    ),
    "LICENSES.md": (
        "LICENSES.md",
        "paper, data, and code license terms",
        "text/markdown",
        "CC-BY-4.0 AND MIT",
    ),
}
EXPECTED_UPLOAD_HASHES = {
    "K2P_SAME_Principal_Domain_Article.pdf": "e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4",
    "K2P_SAME_Reader_Supplement.pdf": "0448cfc078f91d0bb5f08097e3055d302e1ef5308664dc3a7443e728f38ffd9d",
    "K2P_SAME_bioRxiv_Source_20260829.zip": "66527a3e3018b054f9e6b618a6c9e81a4ddbc6e2d0cced81542a0a7fe3eb3cd3",
    "LICENSES.md": "9f8d28b470f185905d0469d45168d72d56d0152a1667a299328a3af00041465e",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def reject_optimized_mode() -> None:
    if not __debug__:
        fail("optimized Python is forbidden")


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def atomic_copy(source: Path, destination: Path) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copyfile(source, temporary)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_write(path: Path, data: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        temporary.write_bytes(data)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def git_commit() -> str:
    root_result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=PROJECT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if root_result.returncode != 0:
        fail("could not determine Git repository root")
    repository = Path(root_result.stdout.strip()).resolve()
    try:
        project_relative = PROJECT.relative_to(repository)
    except ValueError:
        fail("project root is outside the Git repository")
    tracked_paths = [
        (project_relative / relative).as_posix()
        for relative in reproducibility.PACKAGING_FILES
    ]
    for relative in tracked_paths:
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", relative],
            cwd=repository,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if tracked.returncode != 0:
            fail(f"packaging source is not tracked: {relative}")
    clean = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", *tracked_paths],
        cwd=repository,
        timeout=30,
        check=False,
    )
    if clean.returncode != 0:
        fail("packaging sources differ from HEAD")
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    value = result.stdout.strip()
    if result.returncode != 0 or re.fullmatch(r"[0-9a-f]{40}", value) is None:
        fail("could not determine packaging source commit")
    return value


def artifact_row(path: Path, role: str, media_type: str, license_name: str) -> dict[str, Any]:
    return {
        "filename": path.name,
        "role": role,
        "media_type": media_type,
        "license": license_name,
        "bytes": path.stat().st_size,
        "sha256": sha256_path(path),
    }


def build_manifest(output: Path, packaging_commit: str) -> dict[str, Any]:
    artifacts = [
        artifact_row(
            output / name,
            role,
            media_type,
            license_name,
        )
        for name, (_relative, role, media_type, license_name) in sorted(UPLOAD_SOURCES.items())
    ]
    artifacts.append(
        artifact_row(
            output / REPRODUCIBILITY_NAME,
            "complete publication reproducibility package",
            "application/zip",
            "CC-BY-4.0 AND MIT",
        )
    )
    artifacts.sort(key=lambda row: row["filename"])
    return {
        "schema": "k2p-same-zenodo-deposit-manifest-v1",
        "release": {
            "title": (
                "Generic Identifiability and Directed Containment for Strongly "
                "Tree-Child Level-2 Networks under Positive-Fourier K2P: The "
                "Principal Positive Domain and Strict Continuous Time"
            ),
            "version": "1.0.5-r1",
            "publication_date": "2026-08-29",
            "type": "publication",
            "publication_type": "preprint",
            "access_right": "open",
            "creators": [
                {
                    "name": "Kriebel, Alec",
                    "orcid": "0009-0001-9320-500X",
                }
            ],
            "description": (
                "Article, reader supplement, compile-complete source, and exact "
                "reproducibility package for the K2P-SAME classification on the "
                "principal positive Fourier domain, including strict continuous "
                "time and the 4n-3 weak-class sharpness theorem."
            ),
            "keywords": [
                "algebraic statistics",
                "generic identifiability",
                "Kimura two-parameter model",
                "phylogenetic networks",
                "semi-directed networks",
                "tree-child networks",
            ],
            "license": "CC-BY-4.0",
            "notes": (
                "The record contains mixed-license material: article, supplement, "
                "figures, tables, and certificate data are CC BY 4.0; verifier "
                "and build code are MIT. LICENSES.md is authoritative."
            ),
        },
        "git_bindings": {
            "repository": "https://github.com/AlecKriebel/Math",
            "manuscript_tag": "k2p-same-biorxiv-v1.0.5",
            "manuscript_commit": "5628a08f6bf3e5573ebbbf3e2dd8636ad00b338e",
            "accepted_evidence_tag": "k2p-same-referee-package-v1.0.5-r1",
            "accepted_evidence_commit": "e2f6e32e6fe885e90c8e83a8c5b00785e663a4ae",
            "zenodo_package_tag": "k2p-same-zenodo-v1.0.5-r1",
            "packaging_source_commit": packaging_commit,
        },
        "evidence_authority": {
            "frozen_file_count": reproducibility.EXPECTED_FROZEN_COUNT,
            "frozen_total_bytes": reproducibility.EXPECTED_FROZEN_BYTES,
            "frozen_content_ledger_root_sha256": reproducibility.EXPECTED_FROZEN_ROOT,
            "release_lock_sha256": reproducibility.EXPECTED_LOCK_SHA256,
            "release_lock_payload_sha256": reproducibility.EXPECTED_LOCK_PAYLOAD,
            "publication_file_count": len(reproducibility.PUBLIC_SUBMISSION_FILES),
            "publication_total_bytes": reproducibility.EXPECTED_PUBLICATION_BYTES,
            "publication_content_ledger_root_sha256": reproducibility.EXPECTED_PUBLICATION_ROOT,
        },
        "doi_policy": (
            "The Zenodo DOI is repository metadata and is deliberately not "
            "embedded in the immutable artifact set."
        ),
        "checksum_policy": (
            "SHA256SUMS covers every upload file except SHA256SUMS itself. The "
            "deposit manifest lists the five substantive artifacts and is itself "
            "covered by SHA256SUMS."
        ),
        "substantive_artifact_count": len(artifacts),
        "artifacts": artifacts,
    }


def manifest_bytes(value: dict[str, Any]) -> bytes:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"


def write_checksums(output: Path) -> None:
    names = sorted([*UPLOAD_SOURCES, REPRODUCIBILITY_NAME, DEPOSIT_MANIFEST_NAME])
    lines = [f"{sha256_path(output / name)}  {name}" for name in names]
    atomic_write(output / CHECKSUM_NAME, ("\n".join(lines) + "\n").encode("utf-8"))


def check_upload_set(output: Path) -> dict[str, Any]:
    expected = set(UPLOAD_SOURCES) | {
        REPRODUCIBILITY_NAME,
        DEPOSIT_MANIFEST_NAME,
        CHECKSUM_NAME,
    }
    entries = list(output.iterdir())
    if any(not path.is_file() or path.is_symlink() for path in entries):
        fail("upload set contains a directory, symlink, or special entry")
    actual = {path.name for path in entries}
    if actual != expected:
        fail(f"upload-set allowlist mismatch: expected={sorted(expected)} actual={sorted(actual)}")
    for name, expected_hash in EXPECTED_UPLOAD_HASHES.items():
        if sha256_path(output / name) != expected_hash:
            fail(f"accepted upload source mismatch: {name}")
    archive_result = checker.verify_archive(output / REPRODUCIBILITY_NAME)
    manifest_data = (output / DEPOSIT_MANIFEST_NAME).read_bytes()
    manifest = checker.strict_json_bytes(manifest_data, DEPOSIT_MANIFEST_NAME)
    if not isinstance(manifest, dict):
        fail("deposit manifest is not an object")
    if manifest_data != manifest_bytes(manifest):
        fail("deposit manifest byte representation mismatch")
    if manifest.get("schema") != "k2p-same-zenodo-deposit-manifest-v1":
        fail("deposit manifest schema mismatch")
    packaging_commit = manifest.get("git_bindings", {}).get("packaging_source_commit")
    if not isinstance(packaging_commit, str) or re.fullmatch(r"[0-9a-f]{40}", packaging_commit) is None:
        fail("deposit packaging-source commit mismatch")
    if manifest != build_manifest(output, packaging_commit):
        fail("deposit manifest semantic mismatch")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != 5:
        fail("deposit artifact census mismatch")
    expected_artifacts = set(UPLOAD_SOURCES) | {REPRODUCIBILITY_NAME}
    if {row.get("filename") for row in artifacts if isinstance(row, dict)} != expected_artifacts:
        fail("deposit artifact allowlist mismatch")
    for row in artifacts:
        if not isinstance(row, dict):
            fail("malformed deposit artifact row")
        path = output / row["filename"]
        if (
            row["filename"] not in set(UPLOAD_SOURCES) | {REPRODUCIBILITY_NAME}
            or row.get("bytes") != path.stat().st_size
            or row.get("sha256") != sha256_path(path)
        ):
            fail(f"deposit artifact binding mismatch: {row.get('filename')}")
    expected_lines = [
        f"{sha256_path(output / name)}  {name}"
        for name in sorted([*UPLOAD_SOURCES, REPRODUCIBILITY_NAME, DEPOSIT_MANIFEST_NAME])
    ]
    if (output / CHECKSUM_NAME).read_text(encoding="utf-8") != "\n".join(expected_lines) + "\n":
        fail("SHA256SUMS mismatch")
    return {
        "schema": "k2p-same-zenodo-upload-set-check-v1",
        "status": "PASS",
        "upload_file_count": 7,
        "reproducibility_archive_sha256": archive_result["archive_sha256"],
        "deposit_manifest_sha256": sha256_path(output / DEPOSIT_MANIFEST_NAME),
        "checksums_sha256": sha256_path(output / CHECKSUM_NAME),
    }


def main() -> None:
    reject_optimized_mode()
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if args.check_only:
        print(json.dumps(check_upload_set(output), sort_keys=True))
        return
    if args.output_dir.is_symlink():
        fail("output directory must not be a symlink")
    packaging_commit = git_commit()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        fail("output directory must be empty")
    for name, (relative, _role, _media_type, _license_name) in UPLOAD_SOURCES.items():
        source = PROJECT / relative
        if not source.is_file() or source.is_symlink():
            fail(f"missing or symbolic upload source: {relative}")
        atomic_copy(source, output / name)
    reproducibility.write_archive(
        output / REPRODUCIBILITY_NAME,
        reproducibility.build_manifest(reproducibility.collect_files()),
    )
    checker.verify_archive(output / REPRODUCIBILITY_NAME)
    manifest = build_manifest(output, packaging_commit)
    atomic_write(output / DEPOSIT_MANIFEST_NAME, manifest_bytes(manifest))
    write_checksums(output)
    print(json.dumps(check_upload_set(output), sort_keys=True))


if __name__ == "__main__":
    main()
