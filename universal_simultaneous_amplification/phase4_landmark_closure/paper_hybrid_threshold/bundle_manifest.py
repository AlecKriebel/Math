#!/usr/bin/env python3
"""Build and internally verify Paper II's deterministic public archive."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tarfile
import tempfile


PROJECT = "universal_simultaneous_amplification"
PAPER = f"{PROJECT}/phase4_landmark_closure/paper_hybrid_threshold"
EPOCH = 1_787_356_800
HEX64 = re.compile(r"[0-9a-f]{64}")

# This is an exact file whitelist.  No paper directory is included
# recursively, so a future private handoff file or research artifact cannot
# enter the public archive merely by being created under PAPER.
INCLUDE = (
    f"{PROJECT}/LICENSE",
    f"{PAPER}/README.md",
    f"{PAPER}/RELEASE_NOTES.md",
    f"{PAPER}/RESEARCH_LOG.md",
    f"{PAPER}/all.sh",
    f"{PAPER}/bootstrap_replay.sh",
    f"{PAPER}/build.sh",
    f"{PAPER}/bundle_manifest.py",
    f"{PAPER}/certificates/verify_hybrid_coefficients.py",
    f"{PAPER}/certificates/verify_hybrid_lumping.py",
    f"{PAPER}/certificates/verify_leading_algebra.py",
    f"{PAPER}/main.tex",
    f"{PAPER}/output/pdf/simultaneous_amplification_beyond_three_halves.pdf",
    f"{PAPER}/release_bundle.sh",
    f"{PAPER}/replay.sh",
    f"{PAPER}/requirements.txt",
    f"{PAPER}/tests/test_verifier_fail_closed.py",
    f"{PAPER}/vendor/README.md",
    f"{PAPER}/vendor/mpmath-1.3.0-py3-none-any.whl",
    f"{PAPER}/vendor/sympy-1.14.0-py3-none-any.whl",
    f"{PAPER}/verify_paper_claims.py",
)

EXECUTABLES = frozenset(
    {
        f"{PAPER}/all.sh",
        f"{PAPER}/bootstrap_replay.sh",
        f"{PAPER}/build.sh",
        f"{PAPER}/bundle_manifest.py",
        f"{PAPER}/release_bundle.sh",
        f"{PAPER}/replay.sh",
        f"{PAPER}/verify_paper_claims.py",
    }
)

EXCLUDED_PARTS = frozenset(
    {
        ".git",
        ".venv",
        ".venv-paper2",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "tmp",
        "rendered",
        "release",
    }
)
EXCLUDED_NAMES = frozenset({".DS_Store"})
EXCLUDED_SUFFIXES = frozenset(
    {".aux", ".log", ".out", ".pyc", ".synctex.gz", ".toc"}
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reject_optimized_python() -> None:
    if sys.flags.optimize != 0:
        raise SystemExit(
            "ERROR: optimized Python is unsupported for archive verification"
        )


def excluded(relative: PurePosixPath) -> bool:
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return True
    if relative.name in EXCLUDED_NAMES:
        return True
    return any(relative.name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)


def expected_mode(name: str) -> int:
    return 0o755 if name in EXECUTABLES else 0o644


def collect(repo_root: Path) -> list[tuple[PurePosixPath, Path]]:
    found: dict[PurePosixPath, Path] = {}
    for listed in INCLUDE:
        source = repo_root / listed
        if not source.exists():
            raise FileNotFoundError(f"required bundle input is missing: {listed}")
        candidates = [source] if source.is_file() else source.rglob("*")
        for candidate in candidates:
            if candidate.is_symlink():
                raise ValueError(f"symlinks are not permitted in bundle: {candidate}")
            if not candidate.is_file():
                continue
            relative = PurePosixPath(candidate.relative_to(repo_root).as_posix())
            if excluded(relative):
                continue
            mode = stat.S_IMODE(candidate.stat().st_mode)
            required_mode = expected_mode(relative.as_posix())
            if mode != required_mode:
                raise PermissionError(
                    f"bundle input has mode {mode:#06o}, expected "
                    f"{required_mode:#06o}: {relative}"
                )
            found[relative] = candidate
    if not found:
        raise RuntimeError("bundle inclusion set is empty")
    return sorted(found.items(), key=lambda item: item[0].as_posix())


def tar_info(name: str, size: int, executable: bool = False) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.size = size
    info.mtime = EPOCH
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mode = 0o755 if executable else 0o644
    return info


def synthetic_metadata() -> bytes:
    return (
        "Package: A fitness-independent family of simultaneous amplifiers beyond relative fitness 3/2\n"
        "Author: Alec Kriebel\n"
        "ORCID: 0009-0001-9320-500X\n"
        "Status: superseding manuscript submission candidate; no new persistent identifier\n"
        "Licensing: project-authored files MIT; vendored wheels retain upstream BSD licenses\n"
        "Prior source/software DOI: 10.5281/zenodo.21852072\n"
        "Contents: manuscript source, PDF, exact certificates, and replay tooling\n"
        "Archive format: deterministic POSIX tar compressed with deterministic gzip\n"
        f"SOURCE_DATE_EPOCH: {EPOCH}\n"
        "Python: 3.14.6\n"
        "SymPy: 1.14.0\n"
        "mpmath: 1.3.0\n"
        "Python dependency policy: vendored pure-Python wheels; offline hash-pinned installation\n"
        "PDF toolchain: Tectonic 0.16.9; Poppler 26.08.0\n"
        "Document dependency policy: external tools; Tectonic resources may require a populated cache or network access\n"
        "Replay entry point: universal_simultaneous_amplification/"
        "phase4_landmark_closure/paper_hybrid_threshold/replay.sh\n"
    ).encode("utf-8")


def write_archive(repo_root: Path, output: Path) -> tuple[int, str]:
    files = collect(repo_root)
    metadata = synthetic_metadata()
    hashes = [(sha256(metadata), "BUNDLE_METADATA.txt")]
    payloads: list[tuple[str, bytes, bool]] = [
        ("BUNDLE_METADATA.txt", metadata, False)
    ]

    for relative, source in files:
        data = source.read_bytes()
        name = relative.as_posix()
        hashes.append((sha256(data), name))
        executable = expected_mode(name) == 0o755
        payloads.append((name, data, executable))

    manifest = "".join(f"{digest}  {name}\n" for digest, name in hashes).encode(
        "utf-8"
    )
    payloads.append(("MANIFEST.sha256", manifest, False))
    payloads.sort(key=lambda item: item[0])

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=f".{output.name}.", dir=output.parent, delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)

    try:
        with temporary_path.open("wb") as raw:
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=raw, mtime=EPOCH, compresslevel=9
            ) as compressed:
                with tarfile.open(
                    fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT
                ) as archive:
                    for name, data, executable in payloads:
                        archive.addfile(tar_info(name, len(data), executable), io.BytesIO(data))
        os.replace(temporary_path, output)
        os.chmod(output, 0o644)
    finally:
        temporary_path.unlink(missing_ok=True)

    verify_archive(output)
    return len(files), sha256(output.read_bytes())


def verify_archive(output: Path) -> None:
    with tarfile.open(output, mode="r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        if names != sorted(names) or len(names) != len(set(names)):
            raise RuntimeError("archive members are not unique and sorted")
        if any(not member.isfile() for member in members):
            raise RuntimeError("archive contains a non-regular member")
        for member in members:
            required_mode = expected_mode(member.name)
            if member.mode != required_mode:
                raise RuntimeError(
                    f"archive member has mode {member.mode:#06o}, expected "
                    f"{required_mode:#06o}: {member.name}"
                )
        expected_names = sorted({"BUNDLE_METADATA.txt", "MANIFEST.sha256", *INCLUDE})
        if names != expected_names:
            raise RuntimeError("archive differs from the exact public-file whitelist")
        extracted = {
            member.name: archive.extractfile(member).read()  # type: ignore[union-attr]
            for member in members
        }

    manifest = extracted.pop("MANIFEST.sha256").decode("utf-8")
    expected: dict[str, str] = {}
    for number, line in enumerate(manifest.splitlines(), 1):
        try:
            digest, name = line.split("  ", 1)
        except ValueError as exc:
            raise RuntimeError(
                f"MANIFEST.sha256:{number}: malformed line"
            ) from exc
        path = PurePosixPath(name)
        if not HEX64.fullmatch(digest):
            raise RuntimeError(
                f"MANIFEST.sha256:{number}: malformed SHA-256"
            )
        if path.is_absolute() or ".." in path.parts or path.as_posix() != name:
            raise RuntimeError(
                f"MANIFEST.sha256:{number}: unsafe or noncanonical path"
            )
        if name in expected:
            raise RuntimeError(
                f"MANIFEST.sha256:{number}: duplicate path"
            )
        expected[name] = digest
    if not expected:
        raise RuntimeError("MANIFEST.sha256 is empty")
    if set(expected) != set(extracted):
        raise RuntimeError("manifest and archive file sets differ")
    for name, data in extracted.items():
        if sha256(data) != expected[name]:
            raise RuntimeError(f"archive hash verification failed: {name}")

    forbidden_paths = (
        "/submission/",
        "endpoint_affine",
        "audit_core_uniformity.py",
        "/search_",
        "/explore_",
    )
    for name in extracted:
        if any(token in name for token in forbidden_paths):
            raise RuntimeError(f"forbidden non-proof dependency in archive: {name}")


def main() -> None:
    reject_optimized_python()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output = args.output.resolve()
    if not (repo_root / PROJECT / "LICENSE").is_file():
        raise SystemExit(f"not the expected repository root: {repo_root}")

    count, digest = write_archive(repo_root, output)
    print(f"WROTE: {output}")
    print(f"FILES: {count + 2} (including metadata and manifest)")
    print(f"SHA256: {digest}")


if __name__ == "__main__":
    main()
