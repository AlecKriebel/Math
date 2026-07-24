#!/usr/bin/env python3
"""Build a metadata-normalized tar.gz of this release."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARCHIVE_ROOT = ROOT.name


def is_generated_python_cache(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    return (
        "__pycache__" in relative.parts
        and path.suffix in {".pyc", ".pyo"}
    )


def is_repository_metadata(path: Path) -> bool:
    return ".git" in path.relative_to(ROOT).parts


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def add_directory(archive: tarfile.TarFile, relative: Path) -> None:
    name = f"{ARCHIVE_ROOT}/{relative.as_posix()}".rstrip("/")
    info = tarfile.TarInfo(name)
    info.type = tarfile.DIRTYPE
    info.mode = 0o755
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    archive.addfile(info)


def add_file(
    archive: tarfile.TarFile, relative: Path, payload: bytes
) -> None:
    info = tarfile.TarInfo(f"{ARCHIVE_ROOT}/{relative.as_posix()}")
    info.size = len(payload)
    info.mode = 0o644
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    archive.addfile(info, io.BytesIO(payload))


def build(output: Path) -> None:
    output = output.resolve()
    try:
        output.relative_to(ROOT)
    except ValueError:
        pass
    else:
        raise ValueError("archive output must be outside the bundle")

    files = sorted(
        path
        for path in ROOT.rglob("*")
        if (
            path.is_file()
            and not is_generated_python_cache(path)
            and not is_repository_metadata(path)
        )
    )
    directories = sorted(
        path
        for path in ROOT.rglob("*")
        if (
            path.is_dir()
            and path.name not in {"__pycache__", ".git"}
            and not is_repository_metadata(path)
        )
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, mtime=0
        ) as compressed:
            with tarfile.open(
                fileobj=compressed,
                mode="w",
                format=tarfile.USTAR_FORMAT,
            ) as archive:
                root_info = tarfile.TarInfo(ARCHIVE_ROOT)
                root_info.type = tarfile.DIRTYPE
                root_info.mode = 0o755
                root_info.uid = 0
                root_info.gid = 0
                root_info.uname = ""
                root_info.gname = ""
                root_info.mtime = 0
                archive.addfile(root_info)
                for directory in directories:
                    add_directory(archive, directory.relative_to(ROOT))
                for path in files:
                    add_file(
                        archive,
                        path.relative_to(ROOT),
                        path.read_bytes(),
                    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=ROOT.parent / f"{ARCHIVE_ROOT}.tar.gz",
    )
    arguments = parser.parse_args()
    build(arguments.output)
    output = arguments.output.resolve()
    print(
        json.dumps(
            {
                "archive": str(output),
                "bytes": output.stat().st_size,
                "sha256": sha256(output),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
