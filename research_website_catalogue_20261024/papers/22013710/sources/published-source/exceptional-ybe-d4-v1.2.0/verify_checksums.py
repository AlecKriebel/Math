#!/usr/bin/env python3
"""Verify the package-local SHA256SUMS manifest safely and portably."""

from hashlib import sha256
from pathlib import Path, PurePosixPath
import re
import sys


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS"
LINE = re.compile(r"([0-9a-f]{64})  (.+)")


def fail(message):
    print(f"checksum verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def digest(path):
    result = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def main():
    if sys.flags.optimize:
        fail("optimized Python is not permitted")
    try:
        lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        fail(str(exc))
    if not lines:
        fail("SHA256SUMS is empty")

    seen = set()
    for number, line in enumerate(lines, start=1):
        match = LINE.fullmatch(line)
        if match is None:
            fail(f"malformed line {number}")
        expected, name = match.groups()
        relative = PurePosixPath(name)
        if (
            name != relative.as_posix()
            or relative.is_absolute()
            or ".." in relative.parts
            or "\\" in name
            or name in {"", "."}
        ):
            fail(f"unsafe path on line {number}: {name!r}")
        if name in seen:
            fail(f"duplicate path on line {number}: {name}")
        seen.add(name)

        path = ROOT.joinpath(*relative.parts)
        try:
            resolved = path.resolve(strict=True)
        except OSError:
            fail(f"missing file: {name}")
        if ROOT not in resolved.parents or not resolved.is_file():
            fail(f"path escapes package or is not a file: {name}")
        actual = digest(resolved)
        if actual != expected:
            fail(f"hash mismatch: {name}")
        print(f"{name}: OK")

    print(f"Verified {len(seen)} package-local SHA-256 digests.")


if __name__ == "__main__":
    main()
