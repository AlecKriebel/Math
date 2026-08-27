#!/usr/bin/env python3
"""Build the self-excluding final artifact index for the r3 referee review."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import sys
from pathlib import Path


SCHEMA = "k2p-same-r3-final-artifact-index-v1"
DEFAULT_OUTPUT = "FINAL_ARTIFACT_INDEX.json"
EXCLUDED_TOP_LEVEL = frozenset({"isolated", "execution", "tmp", "pdf_render"})
EXCLUDED_NAMES = frozenset({".DS_Store"})
EXCLUDED_SUFFIXES = frozenset({".pyc", ".pyo"})


class IndexError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IndexError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_hash(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def excluded(relative: Path, output_relative: Path) -> bool:
    if relative == output_relative:
        # A file cannot contain its own stable byte hash.  The final report
        # records the index file hash separately after publication.
        return True
    if not relative.parts:
        return True
    if relative.parts[0] in EXCLUDED_TOP_LEVEL:
        return True
    if ".git" in relative.parts or "__pycache__" in relative.parts:
        return True
    if relative.name in EXCLUDED_NAMES or relative.suffix in EXCLUDED_SUFFIXES:
        return True
    return False


def build(root: Path, output: Path) -> dict[str, object]:
    root = root.resolve()
    output = output.resolve()
    require(root.is_dir(), f"review root is not a directory: {root}")
    try:
        output_relative = output.relative_to(root)
    except ValueError as error:
        raise IndexError("output must be inside the review root") from error

    rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if excluded(relative, output_relative):
            continue
        mode = path.lstat().st_mode
        require(not stat.S_ISLNK(mode), f"symbolic path in final scope: {relative}")
        if stat.S_ISDIR(mode):
            continue
        require(stat.S_ISREG(mode), f"non-regular path in final scope: {relative}")
        rows.append(
            {
                "path": relative.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

    paths = [str(row["path"]) for row in rows]
    require(paths == sorted(paths), "artifact paths are not sorted")
    require(len(paths) == len(set(paths)), "duplicate artifact path")
    require(paths, "empty final artifact scope")

    value: dict[str, object] = {
        "schema": SCHEMA,
        "status": "PASS",
        "scope": {
            "root": ".",
            "excluded_top_level_directories": sorted(EXCLUDED_TOP_LEVEL),
            "self_excluded": output_relative.as_posix(),
            "self_exclusion_reason": "a byte-stable file cannot hash itself",
        },
        "file_count": len(rows),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
        "files": rows,
    }
    value["payload_sha256"] = canonical_hash(value)
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if not __debug__:
        raise SystemExit("FINAL_ARTIFACT_INDEX_OPTIMIZED_MODE_FORBIDDEN")

    root = args.root.resolve()
    output = (args.output or root / DEFAULT_OUTPUT).resolve()
    value = build(root, output)
    encoded = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

    if args.write:
        require(not output.is_symlink(), "artifact index output is symbolic")
        output.write_text(encoded, encoding="utf-8")
    elif args.check:
        require(output.is_file() and not output.is_symlink(), "artifact index missing")
        require(output.read_text(encoding="utf-8") == encoded, "artifact index is stale")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except IndexError as error:
        raise SystemExit(f"FINAL_ARTIFACT_INDEX_FAIL:{error}") from error
