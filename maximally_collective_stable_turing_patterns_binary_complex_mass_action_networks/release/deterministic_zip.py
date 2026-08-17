#!/usr/bin/env python3
"""Create a canonical ZIP archive from a directory tree.

Member order, metadata, timestamps, and compression settings are fixed.  The
result is byte-reproducible under the same Python/zlib toolchain; ZIP contents
remain reproducible across compatible toolchains even if DEFLATE bytes differ.
"""

from __future__ import annotations

import argparse
import os
import stat
import time
import zipfile
from pathlib import Path


DEFAULT_EPOCH = 315532800  # 1980-01-01, the earliest ZIP timestamp.


def zip_timestamp() -> tuple[int, int, int, int, int, int]:
    epoch = int(os.environ.get("SOURCE_DATE_EPOCH", DEFAULT_EPOCH))
    epoch = max(epoch, DEFAULT_EPOCH)
    value = list(time.gmtime(epoch)[:6])
    # The DOS timestamp stored by ZIP has a two-second resolution.
    value[5] -= value[5] % 2
    return tuple(value)  # type: ignore[return-value]


def archive_tree(source: Path, destination: Path) -> None:
    source = source.resolve(strict=True)
    if not source.is_dir():
        raise ValueError(f"source is not a directory: {source}")
    destination = destination.resolve()
    if destination == source or source in destination.parents:
        raise ValueError("destination must be outside the source directory")

    files = sorted(
        (path for path in source.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(source).as_posix(),
    )
    symlinks = [path for path in source.rglob("*") if path.is_symlink()]
    if symlinks:
        listing = ", ".join(str(path.relative_to(source)) for path in symlinks)
        raise ValueError(f"source tree contains symbolic links: {listing}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp")
    temporary.unlink(missing_ok=True)
    timestamp = zip_timestamp()
    try:
        with zipfile.ZipFile(
            temporary,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
            strict_timestamps=True,
        ) as archive:
            for path in files:
                relative = path.relative_to(source).as_posix()
                executable = bool(path.stat().st_mode & stat.S_IXUSR)
                mode = 0o755 if executable else 0o644
                info = zipfile.ZipInfo(relative, date_time=timestamp)
                info.create_system = 3
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (stat.S_IFREG | mode) << 16
                info.flag_bits = 0
                with path.open("rb") as handle:
                    archive.writestr(info, handle.read(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="directory whose contents form the ZIP root")
    parser.add_argument("destination", type=Path, help="output ZIP path")
    args = parser.parse_args()
    archive_tree(args.source, args.destination)


if __name__ == "__main__":
    main()
