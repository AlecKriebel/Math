#!/usr/bin/env python3
"""Independently rebuild the five-file bioRxiv source archive twice."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


FILES = [
    "article/main.tex", "article/references.bib", "supplement/supplement.tex",
    "supplement/compression_tables.tex", "supplement/certificate_appendix.tex",
]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in FILES:
            info = zipfile.ZipInfo(relative, date_time=(2026, 8, 29, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (source / relative).read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--second", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.source_root, args.first)
    build(args.source_root, args.second)
    digest = sha(args.archive)
    passed = digest == sha(args.first) == sha(args.second)
    result = {
        "schema": "k2p-r6-independent-biorxiv-source-rebuild-v1",
        "status": "PASS" if passed else "FAIL", "file_count": len(FILES),
        "files": FILES, "archive_sha256": digest,
        "first_sha256": sha(args.first), "second_sha256": sha(args.second),
        "bytes": args.archive.stat().st_size, "byte_identical_three_way": passed,
        "fixed_timestamp": "2026-08-29T00:00:00", "mode": "100644",
    }
    result["payload_sha256"] = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
