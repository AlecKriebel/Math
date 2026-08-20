#!/usr/bin/env python3
"""Build and internally verify Paper II's deterministic public archive."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import os
from pathlib import Path, PurePosixPath
import tarfile
import tempfile


PROJECT = "universal_simultaneous_amplification"
PAPER = f"{PROJECT}/phase4_landmark_closure/paper_hybrid_threshold"
EPOCH = 1_787_270_400

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
    f"{PAPER}/verify_paper_claims.py",
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


def excluded(relative: PurePosixPath) -> bool:
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return True
    if relative.name in EXCLUDED_NAMES:
        return True
    return any(relative.name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)


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
        "Package: A fitness-independent simultaneous amplifier beyond fitness 3/2\n"
        "Contents: manuscript source, PDF, exact certificates, and replay tooling\n"
        "Archive format: deterministic POSIX tar compressed with deterministic gzip\n"
        f"SOURCE_DATE_EPOCH: {EPOCH}\n"
        "Python: 3.14.6\n"
        "SymPy: 1.14.0\n"
        "mpmath: 1.3.0\n"
        "PDF toolchain: Tectonic 0.16.9; Poppler 26.08.0\n"
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
        executable = bool(source.stat().st_mode & 0o111)
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
        expected_names = sorted({"BUNDLE_METADATA.txt", "MANIFEST.sha256", *INCLUDE})
        if names != expected_names:
            raise RuntimeError("archive differs from the exact public-file whitelist")
        extracted = {
            member.name: archive.extractfile(member).read()  # type: ignore[union-attr]
            for member in members
        }

    manifest = extracted.pop("MANIFEST.sha256").decode("utf-8")
    expected: dict[str, str] = {}
    for line in manifest.splitlines():
        digest, name = line.split("  ", 1)
        expected[name] = digest
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
