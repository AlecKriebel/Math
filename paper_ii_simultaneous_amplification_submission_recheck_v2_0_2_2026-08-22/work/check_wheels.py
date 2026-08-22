#!/usr/bin/env python3
"""Independent structural and RECORD-integrity audit of vendored wheels."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import pathlib
import posixpath
import stat
import sys
import zipfile


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def safe_member(name: str) -> bool:
    if not name or name.startswith(("/", "\\")) or "\\" in name:
        return False
    normalized = posixpath.normpath(name)
    return normalized == name.rstrip("/") and normalized not in (".", "..") and not normalized.startswith("../")


def record_digest(data: bytes) -> str:
    encoded = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=")
    return "sha256=" + encoded.decode("ascii")


def audit(path: pathlib.Path) -> None:
    with zipfile.ZipFile(path) as wheel:
        infos = wheel.infolist()
        names = [item.filename for item in infos]
        if len(names) != len(set(names)):
            fail(f"duplicate member in {path.name}")
        bad_names = [name for name in names if not safe_member(name)]
        if bad_names:
            fail(f"unsafe members in {path.name}: {bad_names}")

        for info in infos:
            mode = (info.external_attr >> 16) & 0o177777
            file_type = stat.S_IFMT(mode)
            if file_type and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                fail(f"non-regular member {info.filename} in {path.name}: {oct(mode)}")

        record_names = [name for name in names if name.endswith(".dist-info/RECORD")]
        metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
        wheel_names = [name for name in names if name.endswith(".dist-info/WHEEL")]
        if len(record_names) != 1 or len(metadata_names) != 1 or len(wheel_names) != 1:
            fail(f"missing or duplicate wheel metadata in {path.name}")

        rows = list(csv.reader(io.StringIO(wheel.read(record_names[0]).decode("utf-8"))))
        if len(rows) != len(names):
            fail(f"RECORD/member cardinality mismatch in {path.name}: {len(rows)} vs {len(names)}")
        by_name = {}
        for row in rows:
            if len(row) != 3 or row[0] in by_name:
                fail(f"malformed or duplicate RECORD row in {path.name}: {row}")
            by_name[row[0]] = row[1:]
        if set(by_name) != set(names):
            fail(f"RECORD path set mismatch in {path.name}")

        for name in names:
            digest, size = by_name[name]
            data = wheel.read(name)
            if name == record_names[0]:
                if digest or size:
                    fail(f"RECORD self-row must be unhashed in {path.name}")
                continue
            if digest != record_digest(data) or size != str(len(data)):
                fail(f"RECORD mismatch for {name} in {path.name}")

        metadata = wheel.read(metadata_names[0]).decode("utf-8", errors="strict")
        wheel_metadata = wheel.read(wheel_names[0]).decode("utf-8", errors="strict")
        print(f"PASS {path.name}: {len(names)} unique safe members; complete SHA-256 RECORD")
        for line in metadata.splitlines():
            if line.startswith(("Name:", "Version:", "Requires-Python:", "License-Expression:")):
                print(f"  {line}")
        for line in wheel_metadata.splitlines():
            if line.startswith(("Wheel-Version:", "Root-Is-Purelib:", "Tag:")):
                print(f"  {line}")


def main() -> None:
    if len(sys.argv) < 2:
        fail("usage: check_wheels.py WHEEL [WHEEL ...]")
    for argument in sys.argv[1:]:
        audit(pathlib.Path(argument))


if __name__ == "__main__":
    main()
