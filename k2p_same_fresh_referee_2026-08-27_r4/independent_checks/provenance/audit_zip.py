#!/usr/bin/env python3
"""Independent central-directory and member audit for the supplied referee ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import stat
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath


def digest_stream(handle) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    for block in iter(lambda: handle.read(1024 * 1024), b""):
        digest.update(block)
        size += len(block)
    return digest.hexdigest(), size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("extracted_root", type=Path)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    archive_sha256, archive_bytes = digest_stream(args.archive.open("rb"))
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    expected = ledger["files"]

    rows: dict[str, dict[str, object]] = {}
    unsafe: list[str] = []
    symlinks: list[str] = []
    directories: list[str] = []
    top_levels: Counter[str] = Counter()
    timestamps: Counter[str] = Counter()
    modes: Counter[str] = Counter()
    compression: Counter[str] = Counter()

    with zipfile.ZipFile(args.archive) as archive:
        names = [info.filename for info in archive.infolist()]
        duplicate_names = sorted(name for name, n in Counter(names).items() if n != 1)
        for info in archive.infolist():
            path = PurePosixPath(info.filename)
            top_levels[path.parts[0] if path.parts else ""] += 1
            normalized = posixpath.normpath(info.filename)
            if (
                path.is_absolute()
                or not path.parts
                or any(part in {"", ".", ".."} for part in path.parts)
                or normalized != info.filename.rstrip("/")
            ):
                unsafe.append(info.filename)
            mode = (info.external_attr >> 16) & 0xFFFF
            modes[oct(mode)] += 1
            timestamps[str(info.date_time)] += 1
            compression[str(info.compress_type)] += 1
            if stat.S_ISLNK(mode):
                symlinks.append(info.filename)
            if info.is_dir():
                directories.append(info.filename)
                continue
            with archive.open(info, "r") as handle:
                member_sha256, member_bytes = digest_stream(handle)
            relative = PurePosixPath(*path.parts[1:]).as_posix()
            extracted = args.extracted_root.joinpath(*path.parts[1:])
            extracted_sha256 = None
            extracted_bytes = None
            if extracted.is_file() and not extracted.is_symlink():
                extracted_sha256, extracted_bytes = digest_stream(extracted.open("rb"))
            rows[relative] = {
                "archive_bytes": member_bytes,
                "archive_sha256": member_sha256,
                "central_directory_bytes": info.file_size,
                "central_directory_crc": f"{info.CRC:08x}",
                "extracted_bytes": extracted_bytes,
                "extracted_sha256": extracted_sha256,
            }

    actual_paths = set(rows)
    expected_paths = set(expected)
    missing_from_zip = sorted(expected_paths - actual_paths)
    extra_in_zip = sorted(actual_paths - expected_paths)
    ledger_mismatches = []
    extraction_mismatches = []
    for relative, row in rows.items():
        if relative in expected:
            wanted = expected[relative]
            if row["archive_bytes"] != wanted["bytes"] or row["archive_sha256"] != wanted["sha256"]:
                ledger_mismatches.append(relative)
        if (
            row["archive_bytes"] != row["extracted_bytes"]
            or row["archive_sha256"] != row["extracted_sha256"]
        ):
            extraction_mismatches.append(relative)

    canonical = json.dumps(expected, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    computed_content_root = hashlib.sha256(canonical).hexdigest()
    result = {
        "archive": str(args.archive),
        "archive_bytes": archive_bytes,
        "archive_sha256": archive_sha256,
        "zip_entry_count": len(rows) + len(directories),
        "zip_regular_file_count": len(rows),
        "zip_regular_total_bytes": sum(int(row["archive_bytes"]) for row in rows.values()),
        "duplicate_names": duplicate_names,
        "unsafe_names": unsafe,
        "symlinks": symlinks,
        "directory_entries": directories,
        "top_levels": dict(sorted(top_levels.items())),
        "timestamps": dict(sorted(timestamps.items())),
        "modes": dict(sorted(modes.items())),
        "compression_methods": dict(sorted(compression.items())),
        "declared_ledger_file_count": ledger["file_count"],
        "declared_ledger_total_bytes": ledger["total_bytes"],
        "declared_content_root": ledger["content_ledger_root_sha256"],
        "computed_content_root": computed_content_root,
        "missing_from_zip": missing_from_zip,
        "extra_in_zip": extra_in_zip,
        "ledger_mismatches": ledger_mismatches,
        "extraction_mismatches": extraction_mismatches,
        "members": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in result if k != "members"}, sort_keys=True))


if __name__ == "__main__":
    main()
