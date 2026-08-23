#!/usr/bin/env python3
"""Independent, standard-library identity checks for the frozen R3 delivery."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tarfile


AUDIT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = AUDIT_ROOT / "work" / "package"
ARCHIVE_NAME = "complete_graph_extremality_db_source_and_certificates.tar.gz"
HEX64 = re.compile(r"[0-9a-f]{64}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def parse_manifest(data: bytes, label: str) -> dict[PurePosixPath, str]:
    result: dict[PurePosixPath, str] = {}
    for number, line in enumerate(data.decode("ascii").splitlines(), 1):
        pieces = line.split("  ", 1)
        if len(pieces) != 2:
            raise RuntimeError(f"{label}:{number}: malformed line")
        claimed, raw_name = pieces
        name = PurePosixPath(raw_name)
        if HEX64.fullmatch(claimed) is None:
            raise RuntimeError(f"{label}:{number}: malformed digest")
        if name.is_absolute() or ".." in name.parts or name.as_posix() != raw_name:
            raise RuntimeError(f"{label}:{number}: unsafe/noncanonical path")
        if name in result:
            raise RuntimeError(f"{label}:{number}: duplicate path")
        result[name] = claimed
    if not result:
        raise RuntimeError(f"{label}: empty manifest")
    return result


def implied_directories(files: set[PurePosixPath]) -> set[PurePosixPath]:
    result: set[PurePosixPath] = set()
    for name in files:
        parent = name.parent
        while parent != PurePosixPath("."):
            result.add(parent)
            parent = parent.parent
    return result


def inspect_tree(root: Path, label: str) -> tuple[set[PurePosixPath], set[PurePosixPath]]:
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise RuntimeError(f"{label}: root is not a physical directory")
    files: set[PurePosixPath] = set()
    directories: set[PurePosixPath] = set()

    def visit(directory: Path, relative_directory: PurePosixPath) -> None:
        with os.scandir(directory) as entries:
            for entry in entries:
                relative = (
                    PurePosixPath(entry.name)
                    if relative_directory == PurePosixPath(".")
                    else relative_directory / entry.name
                )
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISLNK(mode):
                    raise RuntimeError(f"{label}: symlink: {relative}")
                if stat.S_ISDIR(mode):
                    directories.add(relative)
                    visit(Path(entry.path), relative)
                elif stat.S_ISREG(mode):
                    files.add(relative)
                else:
                    raise RuntimeError(f"{label}: special node: {relative}")

    visit(root, PurePosixPath("."))
    return files, directories


def require_exact_tree(
    root: Path, expected_files: set[PurePosixPath], label: str
) -> None:
    files, directories = inspect_tree(root, label)
    expected_directories = implied_directories(expected_files)
    if files != expected_files or directories != expected_directories:
        raise RuntimeError(
            f"{label}: node mismatch: "
            f"missing_files={sorted(map(str, expected_files - files))}; "
            f"extra_files={sorted(map(str, files - expected_files))}; "
            f"missing_dirs={sorted(map(str, expected_directories - directories))}; "
            f"extra_dirs={sorted(map(str, directories - expected_directories))}"
        )


def main() -> None:
    package_manifest_path = PACKAGE / "PACKAGE_MANIFEST.sha256"
    package_manifest = parse_manifest(
        package_manifest_path.read_bytes(), "PACKAGE_MANIFEST.sha256"
    )
    package_files = set(package_manifest) | {PurePosixPath("PACKAGE_MANIFEST.sha256")}
    require_exact_tree(PACKAGE, package_files, "package")
    for name, claimed in package_manifest.items():
        actual = sha256_file(PACKAGE / name)
        if actual != claimed:
            raise RuntimeError(f"package hash mismatch: {name}: {actual} != {claimed}")
    print(
        f"PASS package exact tree: {len(package_files)} regular files, "
        f"{len(implied_directories(package_files))} implied directories"
    )

    archive_path = PACKAGE / ARCHIVE_NAME
    archive_digest = sha256_file(archive_path)
    expected_sidecar = f"{archive_digest}  {ARCHIVE_NAME}\n".encode("ascii")
    if (PACKAGE / f"{ARCHIVE_NAME}.sha256").read_bytes() != expected_sidecar:
        raise RuntimeError("archive sidecar mismatch")

    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        if names != sorted(names):
            raise RuntimeError("archive names are not sorted")
        if len(names) != len(set(names)):
            raise RuntimeError("archive contains duplicate names")
        payloads: dict[PurePosixPath, bytes] = {}
        for member in members:
            name = PurePosixPath(member.name)
            if name.is_absolute() or ".." in name.parts or name.as_posix() != member.name:
                raise RuntimeError(f"unsafe/noncanonical archive name: {member.name}")
            if not member.isfile():
                raise RuntimeError(f"non-regular archive member: {member.name}")
            handle = archive.extractfile(member)
            if handle is None:
                raise RuntimeError(f"unreadable archive member: {member.name}")
            payloads[name] = handle.read()

    manifest_name = PurePosixPath("MANIFEST.sha256")
    manifest_bytes = payloads.pop(manifest_name)
    archive_manifest = parse_manifest(manifest_bytes, "archive MANIFEST.sha256")
    if set(archive_manifest) != set(payloads):
        raise RuntimeError("archive manifest and payload member sets differ")
    for name, claimed in archive_manifest.items():
        actual = sha256_bytes(payloads[name])
        if actual != claimed:
            raise RuntimeError(f"archive payload hash mismatch: {name}: {actual} != {claimed}")
    print(
        f"PASS archive: digest={archive_digest}; {len(members)} unique sorted "
        f"regular members; {len(payloads)} manifest-bound payloads"
    )

    convenience = PACKAGE / "source_and_certificates"
    convenience_files = set(payloads) | {manifest_name}
    require_exact_tree(convenience, convenience_files, "convenience extraction")
    for name, data in payloads.items():
        if (convenience / name).read_bytes() != data:
            raise RuntimeError(f"convenience/archive byte mismatch: {name}")
    if (convenience / manifest_name).read_bytes() != manifest_bytes:
        raise RuntimeError("convenience/archive MANIFEST mismatch")
    print(
        f"PASS convenience extraction: {len(convenience_files)} regular files, "
        f"{len(implied_directories(convenience_files))} implied directories, byte-identical"
    )

    top_pdf = PACKAGE / "complete_graph_extremality_db.pdf"
    nested_pdf = convenience / (
        "universal_simultaneous_amplification/phase5_exact_threshold/"
        "paper_db_extremality/output/pdf/complete_graph_extremality_db.pdf"
    )
    if top_pdf.read_bytes() != nested_pdf.read_bytes():
        raise RuntimeError("top-level and nested PDFs differ")
    print(f"PASS PDF binding: {sha256_file(top_pdf)}")


if __name__ == "__main__":
    main()
