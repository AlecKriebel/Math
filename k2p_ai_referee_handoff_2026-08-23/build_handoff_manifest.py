#!/usr/bin/env python3
"""Build or check the deterministic outer handoff manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "PACKAGE_MANIFEST.json"
INNER_ROOT = ROOT / "materials" / "k2p_principal_d_plus_submission_referee"
INNER_MANIFEST = INNER_ROOT / "proof_compression_submission" / "crosswalk" / "REVISED_REFEREE_BUNDLE_MANIFEST.json"
SOURCE_ARCHIVE_SHA256 = "ab7c3cef83d1bd7bb8c330b25ace118ae7ee583a39f7f55c7363b37e3ab4fe3d"
IGNORED_TOP_LEVEL = {".referee_venv", "referee_outputs"}
IGNORED_COMPONENTS = {".venv"}


def fail(message: str) -> None:
    raise SystemExit(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def include(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if relative.as_posix() == "PACKAGE_MANIFEST.json":
        return False
    if relative.parts and relative.parts[0] in IGNORED_TOP_LEVEL:
        return False
    if any(part in IGNORED_COMPONENTS for part in relative.parts):
        return False
    if "__pycache__" in relative.parts or path.name == ".DS_Store":
        return False
    if path.suffix in {".pyc", ".pyo"}:
        return False
    return True


def collect() -> dict[str, dict[str, int | str]]:
    files: dict[str, dict[str, int | str]] = {}
    for path in sorted(ROOT.rglob("*")):
        if path.is_dir() or not include(path):
            continue
        if not path.is_file() or path.is_symlink():
            fail(f"non-regular or symbolic package file: {path}")
        relative = PurePosixPath(path.relative_to(ROOT).as_posix())
        if relative.is_absolute() or ".." in relative.parts:
            fail(f"unsafe package path: {relative}")
        data = path.read_bytes()
        files[relative.as_posix()] = {"bytes": len(data), "sha256": sha256(data)}
    return files


def build() -> dict[str, Any]:
    if not __debug__:
        fail("optimized Python is forbidden")
    if not INNER_MANIFEST.is_file():
        fail("inner revised referee manifest is missing")
    inner = json.loads(INNER_MANIFEST.read_text(encoding="utf-8"))
    files = collect()
    value: dict[str, Any] = {
        "schema": "k2p-post-submission-ai-referee-handoff-v1",
        "status": "READY_FOR_INDEPENDENT_REVIEW",
        "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
        "inner_manifest": {
            "path": INNER_MANIFEST.relative_to(ROOT).as_posix(),
            "payload_sha256": inner.get("payload_sha256"),
            "combined_content_root_sha256": inner.get("combined_content_root_sha256"),
            "frozen_file_count": inner.get("frozen_evidence", {}).get("file_count"),
            "submission_file_count": inner.get("submission_sources", {}).get("file_count"),
        },
        "policy": {
            "symlinks_allowed": False,
            "excluded_top_level": sorted(IGNORED_TOP_LEVEL),
            "excluded_components": sorted(IGNORED_COMPONENTS),
            "excluded_manifest": "PACKAGE_MANIFEST.json",
            "excluded_cache_components": ["__pycache__", ".DS_Store", "*.pyc", "*.pyo"],
        },
        "file_count_excluding_manifest": len(files),
        "total_bytes_excluding_manifest": sum(int(row["bytes"]) for row in files.values()),
        "content_root_sha256": sha256(canonical(files)),
        "files": files,
    }
    value["payload_sha256"] = sha256(canonical(value))
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = build()
    encoded = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.write:
        MANIFEST.write_text(encoded, encoding="utf-8")
    elif not MANIFEST.is_file() or MANIFEST.read_text(encoding="utf-8") != encoded:
        fail("outer handoff manifest is stale")
    print(json.dumps({
        "status": "PASS",
        "files": value["file_count_excluding_manifest"],
        "bytes": value["total_bytes_excluding_manifest"],
        "payload_sha256": value["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
