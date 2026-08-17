#!/usr/bin/env python3
"""Write or verify the complete release-file SHA-256 manifest.

The manifest covers every durable file under the Version 1.2.3 submission
candidate except the two byte-identical manifest copies themselves.
Regenerable interpreter, test, packaging, and LaTeX scratch files are ignored.
Verification fails on missing, changed, or unexpected durable files, so stale
partial manifests cannot silently pass.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys


PROJECT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name("MANIFEST.sha256")

IGNORED_PARTS = {
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
}
IGNORED_SUFFIXES = {
    ".aux",
    ".bbl",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".pyc",
    ".pyo",
    ".synctex.gz",
    ".toc",
}


def ignored(path: Path) -> bool:
    relative = path.relative_to(PROJECT)
    if relative in {
        Path("supplement/MANIFEST.sha256"),
        Path("validation/MANIFEST.sha256"),
    }:
        return True
    if any(part in IGNORED_PARTS or part.endswith(".egg-info") for part in relative.parts):
        return True
    if path.name == ".DS_Store" or path.name.startswith(".verification_run_"):
        return True
    return any(path.name.endswith(suffix) for suffix in IGNORED_SUFFIXES)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def actual_entries() -> dict[str, str]:
    entries: dict[str, str] = {}
    for path in sorted(PROJECT.rglob("*")):
        if ignored(path):
            continue
        if path.is_symlink():
            relative = path.relative_to(PROJECT).as_posix()
            raise ValueError(f"symbolic links are forbidden in the release tree: {relative}")
        if path.is_file():
            entries[path.relative_to(PROJECT).as_posix()] = digest(path)
    return entries


def parse_manifest() -> dict[str, str]:
    entries: dict[str, str] = {}
    for line_number, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if not raw:
            continue
        try:
            expected, relative = raw.split("  ", 1)
        except ValueError as exc:
            raise ValueError(f"malformed manifest line {line_number}") from exc
        if len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
            raise ValueError(f"invalid SHA-256 on manifest line {line_number}")
        candidate = Path(relative)
        if (
            "\\" in relative
            or candidate.is_absolute()
            or ".." in candidate.parts
            or candidate.as_posix() != relative
        ):
            raise ValueError(f"unsafe or noncanonical path on manifest line {line_number}")
        if relative in entries:
            raise ValueError(f"duplicate manifest path on line {line_number}: {relative}")
        entries[relative] = expected
    return entries


def write_manifest() -> None:
    entries = actual_entries()
    text = "".join(f"{value}  {path}\n" for path, value in sorted(entries.items()))
    MANIFEST.write_text(text, encoding="utf-8")
    print(f"wrote {len(entries)} entries to {MANIFEST.relative_to(PROJECT)}")


def verify_manifest() -> int:
    expected = parse_manifest()
    actual = actual_entries()
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    changed = sorted(path for path in expected.keys() & actual.keys() if expected[path] != actual[path])
    for path in missing:
        print(f"MISSING: {path}")
    for path in unexpected:
        print(f"UNEXPECTED: {path}")
    for path in changed:
        print(f"CHANGED: {path}")
    if missing or unexpected or changed:
        print(
            f"manifest verification failed: {len(missing)} missing, "
            f"{len(unexpected)} unexpected, {len(changed)} changed",
            file=sys.stderr,
        )
        return 1
    print(f"manifest verification passed: {len(actual)} files")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="regenerate the manifest")
    args = parser.parse_args()
    if args.write:
        write_manifest()
        return 0
    return verify_manifest()


if __name__ == "__main__":
    raise SystemExit(main())
