#!/usr/bin/env python3
"""Verify the frozen Paper I referee package without third-party modules."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import stat
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


def implied_directories(files: set[PurePosixPath]) -> set[PurePosixPath]:
    directories: set[PurePosixPath] = set()
    for name in files:
        parent = name.parent
        while parent != PurePosixPath("."):
            directories.add(parent)
            parent = parent.parent
    return directories


def inspect_tree(
    root: Path, label: str
) -> tuple[set[PurePosixPath], set[PurePosixPath]]:
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
                details = entry.stat(follow_symlinks=False)
                mode = details.st_mode
                if stat.S_ISLNK(mode):
                    raise RuntimeError(f"{label} contains a symlink: {relative}")
                if stat.S_ISDIR(mode):
                    if entry.name.casefold() == "__pycache__":
                        raise RuntimeError(
                            f"{label} contains a forbidden bytecode/cache directory: {relative}"
                        )
                    directories.add(relative)
                    visit(Path(entry.path), relative)
                elif stat.S_ISREG(mode):
                    if relative.suffix.casefold() in {".pyc", ".pyo"}:
                        raise RuntimeError(
                            f"{label} contains forbidden bytecode: {relative}"
                        )
                    files.add(relative)
                else:
                    raise RuntimeError(f"{label} contains a special node: {relative}")

    visit(root, PurePosixPath("."))
    return files, directories


def require_exact_tree(
    root: Path,
    expected_files: set[PurePosixPath],
    label: str,
) -> None:
    actual_files, actual_directories = inspect_tree(root, label)
    expected_directories = implied_directories(expected_files)
    if actual_files != expected_files or actual_directories != expected_directories:
        missing_files = sorted(str(path) for path in expected_files - actual_files)
        unexpected_files = sorted(str(path) for path in actual_files - expected_files)
        missing_directories = sorted(
            str(path) for path in expected_directories - actual_directories
        )
        unexpected_directories = sorted(
            str(path) for path in actual_directories - expected_directories
        )
        raise RuntimeError(
            f"{label} node-set mismatch; missing_files={missing_files}, "
            f"unexpected_files={unexpected_files}, "
            f"missing_directories={missing_directories}, "
            f"unexpected_directories={unexpected_directories}"
        )


def verify_package_manifest() -> int:
    manifest_path = PACKAGE / "PACKAGE_MANIFEST.sha256"
    actual_files, _ = inspect_tree(PACKAGE, "package")
    if PurePosixPath(manifest_path.name) not in actual_files:
        raise RuntimeError(f"package lacks regular {manifest_path.name}")
    expected = parse_manifest(
        manifest_path.read_text(encoding="ascii"), manifest_path.name
    )
    if PurePosixPath(manifest_path.name) in expected:
        raise RuntimeError(f"{manifest_path.name} must not list itself")
    expected_files = set(expected) | {PurePosixPath(manifest_path.name)}
    require_exact_tree(PACKAGE, expected_files, "package")
    for name, claimed in expected.items():
        if digest(PACKAGE / name) != claimed:
            raise RuntimeError(f"package hash mismatch: {name}")
    return len(expected)


def write_verified_extraction(
    target: Path,
    payloads: dict[PurePosixPath, bytes],
    modes: dict[PurePosixPath, int],
) -> None:
    target = target.absolute()
    details = target.lstat()
    if not stat.S_ISDIR(details.st_mode):
        raise RuntimeError(f"extraction target is not a regular directory: {target}")
    target = target.resolve(strict=True)
    if any(target.iterdir()):
        raise RuntimeError(f"extraction target is not empty: {target}")
    for name in sorted(payloads, key=lambda path: path.as_posix()):
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payloads[name])
        destination.chmod(0o755 if modes[name] & 0o111 else 0o644)
    require_exact_tree(target, set(payloads), "verified extraction")


def verify_source_archive(extract_to: Path | None = None) -> tuple[int, str]:
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
        payloads = {}
        modes = {}
        for member in members:
            name = PurePosixPath(member.name)
            source = archive.extractfile(member)
            if source is None:
                raise RuntimeError(f"cannot read source archive member: {name}")
            payloads[name] = source.read()
            modes[name] = member.mode

    manifest_bytes = payloads.pop(PurePosixPath("MANIFEST.sha256"), None)
    if manifest_bytes is None:
        raise RuntimeError("source archive lacks MANIFEST.sha256")
    internal = parse_manifest(
        manifest_bytes.decode("ascii"), "source archive MANIFEST.sha256"
    )
    if set(internal) != set(payloads):
        raise RuntimeError("source archive manifest and payload sets differ")
    extracted_root = PACKAGE / "source_and_certificates"
    expected_extracted = set(payloads) | {PurePosixPath("MANIFEST.sha256")}
    require_exact_tree(extracted_root, expected_extracted, "convenience extraction")
    for name, data in payloads.items():
        if hashlib.sha256(data).hexdigest() != internal[name]:
            raise RuntimeError(f"internal archive hash mismatch: {name}")
        if (extracted_root / name).read_bytes() != data:
            raise RuntimeError(f"extracted file differs from archive: {name}")
    if (extracted_root / "MANIFEST.sha256").read_bytes() != manifest_bytes:
        raise RuntimeError("extracted internal manifest differs from archive")

    if extract_to is not None:
        complete_payloads = dict(payloads)
        complete_payloads[PurePosixPath("MANIFEST.sha256")] = manifest_bytes
        complete_modes = dict(modes)
        complete_modes[PurePosixPath("MANIFEST.sha256")] = 0o644
        write_verified_extraction(extract_to, complete_payloads, complete_modes)

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
    normalized_prompt = " ".join(prompt.lower().split())
    for verdict in (
        "fully validated",
        "valid after minor corrections",
        "major correction required",
        "invalid",
    ):
        if verdict not in normalized_prompt:
            raise RuntimeError(f"referee prompt omits verdict option: {verdict}")
    if (
        "you have not been told whether the results are correct"
        not in normalized_prompt
    ):
        raise RuntimeError("referee prompt lacks explicit neutrality instruction")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extract-to", type=Path)
    args = parser.parse_args()
    package_count = verify_package_manifest()
    source_count, archive_digest = verify_source_archive(args.extract_to)
    verify_neutral_prompt()
    print(f"PASS: {package_count} package payload files match PACKAGE_MANIFEST.sha256")
    print(f"PASS: {source_count} source-archive members match the internal manifest")
    print(f"SOURCE_ARCHIVE_SHA256: {archive_digest}")
    print(f"PDF_SHA256: {digest(PACKAGE / PDF_NAME)}")
    if args.extract_to is not None:
        print(f"WROTE_VERIFIED_EXTRACTION: {args.extract_to.resolve()}")
    print("PASS: extracted source tree, convenience PDF, and neutral prompt are bound")


if __name__ == "__main__":
    main()
