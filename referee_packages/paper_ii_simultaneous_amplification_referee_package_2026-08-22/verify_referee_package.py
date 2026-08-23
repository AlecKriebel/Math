#!/usr/bin/env python3
"""Verify the frozen Paper II referee package without third-party modules."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tarfile


PACKAGE = Path(__file__).resolve().parent
ARCHIVE_NAME = (
    "simultaneous_amplifier_beyond_three_halves_"
    "source_and_certificates.tar.gz"
)
PDF_NAME = "simultaneous_amplification_beyond_three_halves.pdf"
SOURCE_PDF = PurePosixPath(
    "universal_simultaneous_amplification/phase4_landmark_closure/"
    "paper_hybrid_threshold/output/pdf/"
    "simultaneous_amplification_beyond_three_halves.pdf"
)
COMMIT = "bd66a3bbf1c530ef67a4b7be5ee69a6825678457"
TAG_OBJECT = "755969d69cdd7f86ad8eceddb4df52a4fe2b23ee"
TAG = "simultaneous-amplification-beyond-three-halves-v2.0.3"
HEX64 = re.compile(r"[0-9a-f]{64}")
PACKAGE_EXECUTABLES = frozenset(
    {
        PurePosixPath("run_all_referee_checks.sh"),
        PurePosixPath("verify_git_binding.py"),
        PurePosixPath("verify_referee_package.py"),
    }
)
SOURCE_EXECUTABLES = frozenset(
    {
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/all.sh"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/bootstrap_replay.sh"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/build.sh"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/bundle_manifest.py"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/release_bundle.sh"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/replay.sh"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/verify_paper_claims.py"
        ),
    }
)


def reject_optimized_python() -> None:
    if sys.flags.optimize != 0:
        raise SystemExit(
            "ERROR: optimized Python is unsupported for referee-package verification"
        )


def expected_package_mode(name: PurePosixPath) -> int:
    if name in PACKAGE_EXECUTABLES:
        return 0o755
    if name.parts[:1] == ("source_and_certificates",):
        source_name = PurePosixPath(*name.parts[1:])
        return expected_source_mode(source_name)
    return 0o644


def expected_source_mode(name: PurePosixPath) -> int:
    return 0o755 if name in SOURCE_EXECUTABLES else 0o644


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
    manifest_mode = stat.S_IMODE(manifest_path.stat().st_mode)
    if manifest_mode != 0o644:
        raise RuntimeError(
            f"package manifest has mode {manifest_mode:#06o}, expected 0o0644"
        )
    expected = parse_manifest(
        manifest_path.read_text(encoding="ascii"), manifest_path.name
    )
    actual: set[PurePosixPath] = set()
    for path in PACKAGE.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(f"package contains a symlink: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise RuntimeError(f"package contains a non-regular node: {path}")
        if path == manifest_path:
            continue
        relative = PurePosixPath(path.relative_to(PACKAGE).as_posix())
        mode = stat.S_IMODE(path.stat().st_mode)
        required_mode = expected_package_mode(relative)
        if mode != required_mode:
            raise RuntimeError(
                f"package file has mode {mode:#06o}, expected "
                f"{required_mode:#06o}: {relative}"
            )
        actual.add(relative)
    if actual != set(expected):
        missing = sorted(str(path) for path in set(expected) - actual)
        unexpected = sorted(str(path) for path in actual - set(expected))
        raise RuntimeError(
            f"package file-set mismatch; missing={missing}, "
            f"unexpected={unexpected}"
        )
    for name, claimed in expected.items():
        if digest(PACKAGE / name) != claimed:
            raise RuntimeError(f"package hash mismatch: {name}")
    return len(expected)


def verify_source_archive() -> tuple[int, str, str]:
    archive_path = PACKAGE / ARCHIVE_NAME
    archive_digest = digest(archive_path)
    sidecar = (PACKAGE / f"{ARCHIVE_NAME}.sha256").read_text(encoding="ascii")
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
            required_mode = expected_source_mode(name)
            if member.mode != required_mode:
                raise RuntimeError(
                    f"source member has mode {member.mode:#06o}, expected "
                    f"{required_mode:#06o}: {name}"
                )
        payloads = {
            PurePosixPath(member.name): archive.extractfile(member).read()
            for member in members
        }
        archive_modes = {
            PurePosixPath(member.name): member.mode for member in members
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
    extracted_files: set[PurePosixPath] = set()
    for path in extracted_root.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(f"extracted tree contains a symlink: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise RuntimeError(f"extracted tree contains a non-regular node: {path}")
        extracted_files.add(
            PurePosixPath(path.relative_to(extracted_root).as_posix())
        )
    expected_extracted = set(payloads) | {PurePosixPath("MANIFEST.sha256")}
    if extracted_files != expected_extracted:
        raise RuntimeError("extracted tree and source archive file sets differ")

    for name, data in payloads.items():
        if hashlib.sha256(data).hexdigest() != internal[name]:
            raise RuntimeError(f"internal archive hash mismatch: {name}")
        extracted_path = extracted_root / name
        if extracted_path.read_bytes() != data:
            raise RuntimeError(f"extracted file differs from archive: {name}")
        extracted_mode = stat.S_IMODE(extracted_path.stat().st_mode)
        if extracted_mode != archive_modes[name]:
            raise RuntimeError(
                f"extracted mode {extracted_mode:#06o} differs from archive "
                f"mode {archive_modes[name]:#06o}: {name}"
            )
    if (extracted_root / "MANIFEST.sha256").read_bytes() != manifest_bytes:
        raise RuntimeError("extracted internal manifest differs from archive")
    extracted_manifest_mode = stat.S_IMODE(
        (extracted_root / "MANIFEST.sha256").stat().st_mode
    )
    if extracted_manifest_mode != archive_modes[PurePosixPath("MANIFEST.sha256")]:
        raise RuntimeError("extracted internal-manifest mode differs from archive")

    nested_pdf = extracted_root / SOURCE_PDF
    if (PACKAGE / PDF_NAME).read_bytes() != nested_pdf.read_bytes():
        raise RuntimeError("convenience PDF differs from source-tree PDF")

    pdf_digest = digest(PACKAGE / PDF_NAME)
    for document_name in ("VERSION.md", "README_FIRST.md"):
        text = (PACKAGE / document_name).read_text(encoding="utf-8")
        for value, label in (
            (archive_digest, "source-archive digest"),
            (pdf_digest, "PDF digest"),
            (COMMIT, "scientific commit"),
            (TAG_OBJECT, "annotated tag object"),
            (TAG, "annotated unsigned tag"),
        ):
            if value not in text:
                raise RuntimeError(f"{document_name} has a stale {label}")
        if f"Internal source-archive members: {len(members)}" not in text:
            raise RuntimeError(f"{document_name} has a stale member count")
    return len(members), archive_digest, pdf_digest


def verify_neutral_prompt() -> None:
    prompt = (PACKAGE / "REFEREE_PROMPT.md").read_text(encoding="utf-8")
    normalized = " ".join(prompt.lower().split())
    for verdict in (
        "fully validated",
        "valid after minor corrections",
        "major correction required",
        "invalid",
        "inconclusive / review incomplete",
    ):
        if verdict not in normalized:
            raise RuntimeError(f"referee prompt omits verdict option: {verdict}")
    if "you have not been told whether the results are correct" not in normalized:
        raise RuntimeError("referee prompt lacks explicit neutrality instruction")
    if "do not infer a proof from a successful program run" not in normalized:
        raise RuntimeError("referee prompt fails to separate replay from proof")


def main() -> None:
    reject_optimized_python()
    package_count = verify_package_manifest()
    source_count, archive_digest, pdf_digest = verify_source_archive()
    verify_neutral_prompt()
    print(
        f"PASS: {package_count} package payload files match "
        "PACKAGE_MANIFEST.sha256"
    )
    print(
        f"PASS: {source_count} source-archive members match the internal manifest"
    )
    print(f"SOURCE_ARCHIVE_SHA256: {archive_digest}")
    print(f"PDF_SHA256: {pdf_digest}")
    print("PASS: extracted source tree, convenience PDF, and neutral prompt are bound")


if __name__ == "__main__":
    main()
