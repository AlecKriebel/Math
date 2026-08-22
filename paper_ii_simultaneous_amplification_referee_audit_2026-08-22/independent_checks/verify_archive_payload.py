#!/usr/bin/env python3
"""Independent safety and byte-identity check for the delivered tar archive."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
import shutil
import tarfile


AUDIT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = AUDIT_ROOT / "delivered_copy"
ARCHIVE = PACKAGE_ROOT / "simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz"
REFERENCE = PACKAGE_ROOT / "source_and_certificates"
EXTRACTED = AUDIT_ROOT / "work" / "manual_archive_extract"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def regular_files(root: Path) -> dict[str, Path]:
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }


def main() -> None:
    if EXTRACTED.exists():
        raise RuntimeError(f"refusing to replace existing extraction: {EXTRACTED}")
    EXTRACTED.mkdir(parents=True)

    with tarfile.open(ARCHIVE, "r:gz") as archive:
        members = archive.getmembers()
        if len(members) != 19:
            raise AssertionError(f"expected 19 archive members, found {len(members)}")
        names: set[str] = set()
        for member in members:
            path = PurePosixPath(member.name)
            if path.is_absolute() or not path.parts or ".." in path.parts:
                raise AssertionError(f"unsafe archive path: {member.name!r}")
            if "\\" in member.name or member.name in names:
                raise AssertionError(f"ambiguous or duplicate archive path: {member.name!r}")
            if not member.isfile():
                raise AssertionError(
                    f"non-regular archive member: {member.name!r}, type={member.type!r}"
                )
            names.add(member.name)

        for member in members:
            source = archive.extractfile(member)
            if source is None:
                raise AssertionError(f"cannot read regular member: {member.name!r}")
            destination = EXTRACTED / PurePosixPath(member.name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with source, destination.open("xb") as output:
                shutil.copyfileobj(source, output)

    extracted_files = regular_files(EXTRACTED)
    reference_files = regular_files(REFERENCE)
    if set(extracted_files) != set(reference_files):
        missing = sorted(set(reference_files) - set(extracted_files))
        extra = sorted(set(extracted_files) - set(reference_files))
        raise AssertionError(f"tree mismatch: missing={missing}, extra={extra}")

    mismatches = [
        name
        for name in sorted(extracted_files)
        if digest(extracted_files[name]) != digest(reference_files[name])
    ]
    if mismatches:
        raise AssertionError(f"byte mismatches: {mismatches}")

    convenience_pdf = PACKAGE_ROOT / "simultaneous_amplification_beyond_three_halves.pdf"
    archived_pdf = (
        EXTRACTED
        / "universal_simultaneous_amplification"
        / "phase4_landmark_closure"
        / "paper_hybrid_threshold"
        / "output"
        / "pdf"
        / "simultaneous_amplification_beyond_three_halves.pdf"
    )
    if digest(convenience_pdf) != digest(archived_pdf):
        raise AssertionError("convenience PDF differs from archived PDF")

    print(f"archive_members={len(members)}")
    print("member_types=all_safe_regular_files")
    print(f"extracted_files={len(extracted_files)}")
    print("extracted_tree=byte_identical")
    print(f"pdf_sha256={digest(convenience_pdf)}")
    print("convenience_pdf=byte_identical_to_archive_payload")


if __name__ == "__main__":
    main()
