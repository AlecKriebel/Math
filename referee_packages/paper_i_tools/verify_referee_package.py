#!/usr/bin/env python3
"""Verify the frozen Paper I referee package without third-party modules."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
import re
import tarfile


PACKAGE = Path(__file__).resolve().parent
ARCHIVE_NAME = "complete_graph_extremality_db_source_and_certificates.tar.gz"
PDF_NAME = "complete_graph_extremality_db.pdf"
SOURCE_PDF = PurePosixPath(
    "universal_simultaneous_amplification/phase5_exact_threshold/"
    "paper_db_extremality/output/pdf/complete_graph_extremality_db.pdf"
)
HEX64 = re.compile(r"[0-9a-f]{64}")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def parse_manifest(text: str, label: str) -> dict[PurePosixPath, str]:
    expected: dict[PurePosixPath, str] = {}
    for number, line in enumerate(text.splitlines(), 1):
        try:
            claimed, raw_name = line.split("  ", 1)
        except ValueError as exc:
            raise RuntimeError(f"{label}:{number}: malformed line") from exc
        name = PurePosixPath(raw_name)
        if not HEX64.fullmatch(claimed):
            raise RuntimeError(f"{label}:{number}: malformed SHA-256")
        if name.is_absolute() or ".." in name.parts or name.as_posix() != raw_name:
            raise RuntimeError(f"{label}:{number}: unsafe or noncanonical path")
        if name in expected:
            raise RuntimeError(f"{label}:{number}: duplicate path")
        expected[name] = claimed
    if not expected:
        raise RuntimeError(f"{label}: empty manifest")
    return expected


def verify_package_manifest() -> int:
    manifest_path = PACKAGE / "PACKAGE_MANIFEST.sha256"
    expected = parse_manifest(
        manifest_path.read_text(encoding="ascii"), manifest_path.name
    )
    actual: set[PurePosixPath] = set()
    for path in PACKAGE.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(f"package contains a symlink: {path}")
        if not path.is_file() or path == manifest_path:
            continue
        relative = PurePosixPath(path.relative_to(PACKAGE).as_posix())
        actual.add(relative)
    if actual != set(expected):
        missing = sorted(str(path) for path in set(expected) - actual)
        unexpected = sorted(str(path) for path in actual - set(expected))
        raise RuntimeError(
            f"package file-set mismatch; missing={missing}, unexpected={unexpected}"
        )
    for name, claimed in expected.items():
        if digest(PACKAGE / name) != claimed:
            raise RuntimeError(f"package hash mismatch: {name}")
    return len(expected)


def verify_source_archive() -> tuple[int, str]:
    archive_path = PACKAGE / ARCHIVE_NAME
    archive_digest = digest(archive_path)
    sidecar = (PACKAGE / f"{ARCHIVE_NAME}.sha256").read_text(
        encoding="ascii"
    )
    if sidecar != f"{archive_digest}  {ARCHIVE_NAME}\n":
        raise RuntimeError("detached source-archive checksum mismatch")

    with tarfile.open(archive_path, mode="r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        if names != sorted(names) or len(names) != len(set(names)):
            raise RuntimeError("source archive members are not unique and sorted")
        if any(not member.isfile() for member in members):
            raise RuntimeError("source archive contains a non-regular member")
        for member in members:
            name = PurePosixPath(member.name)
            if (
                name.is_absolute()
                or ".." in name.parts
                or name.as_posix() != member.name
            ):
                raise RuntimeError(f"unsafe source archive member: {member.name}")
        payloads = {
            PurePosixPath(member.name): archive.extractfile(member).read()
            for member in members
        }

    manifest_bytes = payloads.pop(PurePosixPath("MANIFEST.sha256"), None)
    if manifest_bytes is None:
        raise RuntimeError("source archive lacks MANIFEST.sha256")
    internal = parse_manifest(
        manifest_bytes.decode("ascii"), "source archive MANIFEST.sha256"
    )
    if set(internal) != set(payloads):
        raise RuntimeError("source archive manifest and payload sets differ")
    extracted_root = PACKAGE / "source_and_certificates"
    extracted_files = {
        PurePosixPath(path.relative_to(extracted_root).as_posix())
        for path in extracted_root.rglob("*")
        if path.is_file()
    }
    expected_extracted = set(payloads) | {PurePosixPath("MANIFEST.sha256")}
    if extracted_files != expected_extracted:
        raise RuntimeError("extracted tree and source archive file sets differ")
    for name, data in payloads.items():
        if hashlib.sha256(data).hexdigest() != internal[name]:
            raise RuntimeError(f"internal archive hash mismatch: {name}")
        if (extracted_root / name).read_bytes() != data:
            raise RuntimeError(f"extracted file differs from archive: {name}")
    if (extracted_root / "MANIFEST.sha256").read_bytes() != manifest_bytes:
        raise RuntimeError("extracted internal manifest differs from archive")

    nested_pdf = extracted_root / SOURCE_PDF
    if (PACKAGE / PDF_NAME).read_bytes() != nested_pdf.read_bytes():
        raise RuntimeError("convenience PDF differs from source-tree PDF")

    pdf_digest = digest(PACKAGE / PDF_NAME)
    version = (PACKAGE / "VERSION.md").read_text(encoding="utf-8")
    readme = (PACKAGE / "README_FIRST.md").read_text(encoding="utf-8")
    for label, text in (("VERSION.md", version), ("README_FIRST.md", readme)):
        if archive_digest not in text:
            raise RuntimeError(f"{label} has a stale source-archive digest")
        if pdf_digest not in text:
            raise RuntimeError(f"{label} has a stale PDF digest")
    version_commit = re.search(
        r"Scientific source commit: `([0-9a-f]{40})`", version
    )
    readme_commit = re.search(
        r"Scientific source commit: `([0-9a-f]{40})`", readme
    )
    if (
        not version_commit
        or not readme_commit
        or version_commit.group(1) != readme_commit.group(1)
    ):
        raise RuntimeError("README_FIRST.md and VERSION.md source commits disagree")
    if f"Internal source-archive members: {len(members)}" not in version:
        raise RuntimeError("VERSION.md has a stale source-archive member count")
    return len(members), archive_digest


def verify_neutral_prompt() -> None:
    prompt = (PACKAGE / "REFEREE_PROMPT.md").read_text(encoding="utf-8")
    for verdict in (
        "fully validated",
        "valid after minor corrections",
        "major correction required",
        "invalid",
    ):
        if verdict not in prompt.lower():
            raise RuntimeError(f"referee prompt omits verdict option: {verdict}")
    if "you have not been told whether the results are correct" not in prompt.lower():
        raise RuntimeError("referee prompt lacks explicit neutrality instruction")


def main() -> None:
    package_count = verify_package_manifest()
    source_count, archive_digest = verify_source_archive()
    verify_neutral_prompt()
    print(f"PASS: {package_count} package payload files match PACKAGE_MANIFEST.sha256")
    print(f"PASS: {source_count} source-archive members match the internal manifest")
    print(f"SOURCE_ARCHIVE_SHA256: {archive_digest}")
    print(f"PDF_SHA256: {digest(PACKAGE / PDF_NAME)}")
    print("PASS: extracted source tree, convenience PDF, and neutral prompt are bound")


if __name__ == "__main__":
    main()
