#!/usr/bin/env python3
"""Build and internally verify Paper I's deterministic release archive."""

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
PAPER = f"{PROJECT}/phase5_exact_threshold/paper_db_extremality"
EPOCH = 1_787_270_400

# Directories are included recursively after applying EXCLUDED_PARTS and
# EXCLUDED_SUFFIXES. Individual files make the replay dependency graph
# explicit without taking unrelated phase-4/phase-5 research programs.
INCLUDE = (
    f"{PROJECT}/LICENSE",
    f"{PROJECT}/Makefile",
    f"{PROJECT}/requirements.txt",
    f"{PROJECT}/src",
    f"{PROJECT}/tests",
    f"{PROJECT}/verification",
    f"{PROJECT}/phase1_directed",
    f"{PROJECT}/phase2_triangle",
    f"{PROJECT}/phase2_n4",
    f"{PROJECT}/phase3_asymptotic",
    f"{PROJECT}/phase5_exact_threshold/r2_determinant/ACTIVE_R2_DETERMINANT.md",
    f"{PROJECT}/phase5_exact_threshold/r2_determinant/COMPLETE_REFRESH_FOREST.md",
    f"{PROJECT}/phase5_exact_threshold/r2_determinant/FIXED_COUNT_TWO_REPLICA.md",
    f"{PROJECT}/phase5_exact_threshold/r2_determinant/TRUE_INVERSE_RANK_SYMMETRIC_PHASE_CONTRACTION.md",
    f"{PROJECT}/phase5_exact_threshold/r2_determinant/verify_r2_determinant.py",
    f"{PROJECT}/phase5_exact_threshold/r2_determinant/verify_complete_refresh_forest.py",
    f"{PROJECT}/phase5_exact_threshold/r2_determinant/verify_antisymmetric_hessian.py",
    f"{PROJECT}/phase5_exact_threshold/r2_determinant/verify_true_inverse_rank_symmetric_phase.py",
    f"{PROJECT}/phase5_exact_threshold/r2_determinant/verify_hessian_sectors.py",
    f"{PROJECT}/phase5_exact_threshold/r2_standard_physical_phase",
    f"{PROJECT}/phase5_exact_threshold/r2_regular_sector/LOCAL_COMPLETE_HESSIAN_THEOREM.md",
    f"{PROJECT}/phase5_exact_threshold/r2_regular_sector/verify_local_complete_hessian.py",
    f"{PROJECT}/phase4_landmark_closure/obstruction/r2_marked_lift_v2/MARKED_ONE_SAMPLE_REDUCTION.md",
    f"{PROJECT}/phase4_landmark_closure/obstruction/r2_marked_lift_v2/verify_marked_lift.py",
    f"{PROJECT}/phase4_landmark_closure/obstruction/r2_entropy_certificate/"
    "chi_square_channel/verify_resolvent_identities.py",
    f"{PROJECT}/phase4_landmark_closure/obstruction/r2_collision_closure/"
    "verify_direct_flow_screen.py",
    f"{PROJECT}/phase4_landmark_closure/obstruction/r2_collision_closure/"
    "verify_fisher_route.py",
    PAPER,
)

EXCLUDED_PARTS = frozenset(
    {
        ".git",
        ".venv",
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
EXCLUDED_PREFIXES = ("explore_", "scan_", "search_")
EXCLUDED_SUFFIXES = frozenset(
    {".aux", ".log", ".out", ".pyc", ".synctex.gz", ".toc"}
)
PUBLIC_SUBMISSION_FILES = frozenset(
    {
        f"{PAPER}/submission/BUNDLE_REPRODUCTION.md",
        f"{PAPER}/submission/DECLARATIONS.md",
        f"{PAPER}/submission/ENVIRONMENT.md",
        f"{PAPER}/submission/PROVENANCE_AND_RELATED_RELEASES.md",
        f"{PAPER}/submission/REPRODUCTION_TEST.md",
        f"{PAPER}/submission/bootstrap_replay.sh",
    }
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def excluded(relative: PurePosixPath) -> bool:
    name = relative.as_posix()
    if name.startswith(f"{PAPER}/submission/"):
        return name not in PUBLIC_SUBMISSION_FILES
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return True
    if relative.name in EXCLUDED_NAMES:
        return True
    if relative.name.startswith(EXCLUDED_PREFIXES):
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
        "Package: Local Complete-Graph Optimality at Fitness Two and "
        "Strong-Selection Rigidity under Death--Birth Updating\n"
        "Contents: manuscript PDF and source, exact certificates, and replay dependencies\n"
        "Archive format: deterministic POSIX tar compressed with deterministic gzip\n"
        f"SOURCE_DATE_EPOCH: {EPOCH}\n"
        "Python: 3.14.6\n"
        "SymPy: 1.14.0\n"
        "python-flint: 0.9.0\n"
        "mpmath: 1.3.0\n"
        "PDF toolchain: Tectonic 0.16.9; Poppler 26.08.0\n"
        "Replay entry point: universal_simultaneous_amplification/"
        "phase5_exact_threshold/paper_db_extremality/replay.sh\n"
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
                with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                    for name, data, executable in payloads:
                        info = tar_info(name, len(data), executable)
                        archive.addfile(info, io.BytesIO(data))
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
        extracted = {
            member.name: archive.extractfile(member).read()  # type: ignore[union-attr]
            for member in members
        }

    manifest = extracted.pop("MANIFEST.sha256").decode("utf-8")
    submission_prefix = f"{PAPER}/submission/"
    bundled_submission = {
        name for name in extracted if name.startswith(submission_prefix)
    }
    if bundled_submission != PUBLIC_SUBMISSION_FILES:
        raise RuntimeError("archive public-submission allowlist mismatch")
    private_token = b"[[POSTAL" + b"_ADDRESS]]"
    if any(private_token in data for data in extracted.values()):
        raise RuntimeError("archive contains the private postal-address token")
    expected: dict[str, str] = {}
    for line in manifest.splitlines():
        digest, name = line.split("  ", 1)
        expected[name] = digest
    if set(expected) != set(extracted):
        raise RuntimeError("manifest and archive file sets differ")
    for name, data in extracted.items():
        if sha256(data) != expected[name]:
            raise RuntimeError(f"archive hash verification failed: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output = args.output.resolve()
    if not (repo_root / PROJECT / "Makefile").is_file():
        raise SystemExit(f"not the expected repository root: {repo_root}")

    count, digest = write_archive(repo_root, output)
    print(f"WROTE: {output}")
    print(f"FILES: {count + 2} (including metadata and manifest)")
    print(f"SHA256: {digest}")


if __name__ == "__main__":
    main()
