#!/usr/bin/env python3
"""Rebuild the sealed referee ZIP twice without importing submitted code."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath


PREFIX = "k2p_principal_d_plus_submission_referee"
MANIFEST = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
TIMESTAMP = (2026, 8, 27, 0, 0, 0)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def same_bytes(first: Path, second: Path) -> bool:
    if first.stat().st_size != second.stat().st_size:
        return False
    with first.open("rb") as left, second.open("rb") as right:
        while True:
            a = left.read(1024 * 1024)
            b = right.read(1024 * 1024)
            if a != b:
                return False
            if not a:
                return True


def safe(root: Path, relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or not pure.parts or any(x in {"", ".", ".."} for x in pure.parts):
        raise SystemExit(f"unsafe path: {relative}")
    return root.joinpath(*pure.parts)


def build(root: Path, output: Path, paths: list[str]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in paths:
            info = zipfile.ZipInfo(f"{PREFIX}/{relative}", date_time=TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, safe(root, relative).read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--source-archive", type=Path, required=True)
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--second", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()
    manifest = json.loads(safe(root, MANIFEST).read_text(encoding="utf-8"))
    frozen = manifest["frozen_evidence"]["files"]
    submission = manifest["submission_sources"]["files"]
    paths = sorted(set(frozen) | set(submission) | {MANIFEST})
    for relative in paths:
        path = safe(root, relative)
        if not path.is_file() or path.is_symlink():
            raise SystemExit(f"missing/nonregular input: {relative}")
        if relative in frozen and (
            path.stat().st_size != frozen[relative]["bytes"] or sha(path) != frozen[relative]["sha256"]
        ):
            raise SystemExit(f"frozen row mismatch: {relative}")
        if relative in submission and (
            path.stat().st_size != submission[relative]["bytes"] or sha(path) != submission[relative]["sha256"]
        ):
            raise SystemExit(f"submission row mismatch: {relative}")
    build(root, args.first, paths)
    build(root, args.second, paths)
    source_sha = sha(args.source_archive)
    first_sha = sha(args.first)
    second_sha = sha(args.second)
    passed = (
        source_sha == first_sha == second_sha
        and same_bytes(args.source_archive, args.first)
        and same_bytes(args.first, args.second)
    )
    result = {
        "schema": "k2p-r6-independent-archive-rebuild-v1",
        "status": "PASS" if passed else "FAIL",
        "file_count": len(paths),
        "source": {"bytes": args.source_archive.stat().st_size, "sha256": source_sha},
        "first": {"bytes": args.first.stat().st_size, "sha256": first_sha},
        "second": {"bytes": args.second.stat().st_size, "sha256": second_sha},
        "byte_identical_three_way": passed,
    }
    unsigned = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(unsigned).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
