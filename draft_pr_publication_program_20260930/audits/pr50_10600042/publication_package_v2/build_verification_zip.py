#!/usr/bin/env python3
"""Build and read back the compact portable support ZIP; Python 3.9+.
Writes only the named ZIP beside this file and refuses to overwrite it.
SPDX-License-Identifier: MIT
"""
from pathlib import Path
import hashlib
import json
import zipfile

MEMBERS = (
    "LICENSE-CODE.txt", "LICENSE-TEXT.md", "README.md", "SHA256SUMS",
    "SOURCE_QUALIFICATIONS.md", "VERIFICATION_RECORD.json",
    "build_verification_zip.py", "even_strand_markov.tex",
    "expected_results.json", "verify_even_calculus.py",
)
base = Path(__file__).absolute().parent
destination = base / "even-strand-markov-verification-v2.zip"
if destination.exists():
    raise SystemExit("Refusing to overwrite an existing verification ZIP.")
expected = {}
for row in (base / "SHA256SUMS").read_text(encoding="ascii").splitlines():
    digest, name = row.split("  ", 1)
    if name in expected or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("Invalid checksum row")
    expected[name] = digest
if set(expected) != set(MEMBERS) - {"SHA256SUMS"}:
    raise ValueError("Checksum member set differs")
bodies = {}
for name in MEMBERS:
    path = base / name
    if path.is_symlink() or not path.is_file():
        raise ValueError("Nonregular member: " + name)
    body = path.read_bytes()
    if name != "SHA256SUMS" and hashlib.sha256(body).hexdigest() != expected[name]:
        raise ValueError("Member hash differs: " + name)
    bodies[name] = body
with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name in MEMBERS:
        info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
        info.create_system = 3
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, bodies[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
with zipfile.ZipFile(destination, "r") as archive:
    if archive.namelist() != list(MEMBERS) or archive.testzip() is not None:
        raise ValueError("Archive topology/CRC differs")
    for name in MEMBERS:
        if archive.read(name) != bodies[name]:
            raise ValueError("Archive readback differs: " + name)
body = destination.read_bytes()
print(json.dumps({"status": "PASS_ARCHIVE_BUILD_AND_EXACT_MEMBER_READBACK",
                  "file": destination.name, "members": len(MEMBERS),
                  "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}, indent=2))
