#!/usr/bin/env python3
"""Build or verify the deterministic Version 1.2.2 release archive."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT / "REPRODUCIBILITY.env"
MANIFEST = PROJECT / "supplement" / "MANIFEST.sha256"
MANIFEST_COPY = PROJECT / "validation" / "MANIFEST.sha256"
DEFAULT_ARCHIVE = PROJECT.parent / f"{PROJECT.name}.zip"
EXECUTABLES = {
    "code/reproduce.sh",
    "manuscript/build.sh",
    "validation/replay_release.sh",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reproducibility_environment() -> dict[str, str]:
    values: dict[str, str] = {}
    for line_number, raw in enumerate(ENV_FILE.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"malformed {ENV_FILE.name} line {line_number}")
        key, value = line.split("=", 1)
        if not key or key in values:
            raise ValueError(f"invalid or duplicate key on line {line_number}: {key!r}")
        values[key] = value
    return values


def manifest_paths() -> list[str]:
    paths: list[str] = []
    seen: set[str] = set()
    for line_number, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if not raw:
            continue
        try:
            digest, relative = raw.split("  ", 1)
        except ValueError as exc:
            raise ValueError(f"malformed manifest line {line_number}") from exc
        candidate = PurePosixPath(relative)
        if (
            len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
            or "\\" in relative
            or candidate.is_absolute()
            or ".." in candidate.parts
            or candidate.as_posix() != relative
            or relative in seen
        ):
            raise ValueError(f"unsafe or duplicate manifest entry on line {line_number}")
        path = PROJECT / relative
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"manifest member is missing, non-file, or symlink: {relative}")
        if sha256(path) != digest:
            raise ValueError(f"manifest digest mismatch: {relative}")
        paths.append(relative)
        seen.add(relative)
    return sorted(paths)


def archive_timestamp() -> tuple[int, int, int, int, int, int]:
    values = reproducibility_environment()
    if values.get("ZIP_FORMAT") != "stored":
        raise ValueError("REPRODUCIBILITY.env must set ZIP_FORMAT=stored")
    try:
        epoch = int(values["SOURCE_DATE_EPOCH"])
    except (KeyError, ValueError) as exc:
        raise ValueError("SOURCE_DATE_EPOCH must be an integer") from exc
    instant = datetime.fromtimestamp(epoch, timezone.utc)
    if instant.second % 2:
        raise ValueError("ZIP timestamps require an even second")
    return (
        instant.year,
        instant.month,
        instant.day,
        instant.hour,
        instant.minute,
        instant.second,
    )


def member_info(name: str, timestamp: tuple[int, int, int, int, int, int], mode: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, timestamp)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_STORED
    info.external_attr = (stat.S_IFREG | mode) << 16
    info.extra = b""
    info.comment = b""
    return info


def build_archive(output: Path) -> None:
    subprocess.run([sys.executable, str(PROJECT / "supplement" / "verify_manifest.py")], check=True)
    if MANIFEST.read_bytes() != MANIFEST_COPY.read_bytes():
        raise ValueError("manifest copies are not byte-identical")

    relative_paths = manifest_paths() + [
        "supplement/MANIFEST.sha256",
        "validation/MANIFEST.sha256",
    ]
    relative_paths = sorted(relative_paths)
    if len(relative_paths) != len(set(relative_paths)):
        raise ValueError("duplicate archive member path")

    resolved_output = output.resolve()
    if resolved_output == PROJECT or PROJECT in resolved_output.parents:
        raise ValueError("release archive must be written outside the package directory")
    output.parent.mkdir(parents=True, exist_ok=True)
    timestamp = archive_timestamp()

    temporary = output.with_name(f".{output.name}.tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_STORED) as archive:
            archive.comment = b""
            for relative in relative_paths:
                source = PROJECT / relative
                if not source.is_file() or source.is_symlink():
                    raise ValueError(f"archive source is missing, non-file, or symlink: {relative}")
                member = f"{PROJECT.name}/{relative}"
                mode = 0o755 if relative in EXECUTABLES else 0o644
                archive.writestr(member_info(member, timestamp, mode), source.read_bytes())
        with zipfile.ZipFile(temporary) as archive:
            if archive.testzip() is not None:
                raise ValueError("new archive failed its CRC test")
            expected = [f"{PROJECT.name}/{relative}" for relative in relative_paths]
            if archive.namelist() != expected:
                raise ValueError("new archive has noncanonical member ordering")
        temporary.replace(output)
    finally:
        if temporary.exists():
            temporary.unlink()
    print(f"wrote {len(relative_paths)} files to {output}")
    print(f"archive sha256: {sha256(output)}")


def check_archive() -> None:
    if not DEFAULT_ARCHIVE.is_file():
        raise FileNotFoundError(f"committed archive is missing: {DEFAULT_ARCHIVE}")
    with tempfile.TemporaryDirectory(prefix="bimolecular-v122-archive-") as directory:
        candidate = Path(directory) / DEFAULT_ARCHIVE.name
        build_archive(candidate)
        if candidate.read_bytes() != DEFAULT_ARCHIVE.read_bytes():
            raise ValueError("rebuilt archive differs from the committed archive")
    print(f"archive verification passed: {sha256(DEFAULT_ARCHIVE)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="archive destination")
    parser.add_argument("--check", action="store_true", help="rebuild and compare with committed archive")
    args = parser.parse_args()
    if args.check and args.output is not None:
        parser.error("--check and --output are mutually exclusive")
    if args.check:
        check_archive()
    else:
        build_archive((args.output or DEFAULT_ARCHIVE).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
