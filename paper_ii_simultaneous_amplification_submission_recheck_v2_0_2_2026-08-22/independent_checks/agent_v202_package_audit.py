#!/usr/bin/env python3
"""Independent, standard-library-only audit of the revised referee package."""

from __future__ import annotations

import ast
import base64
import csv
import gzip
import hashlib
import io
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tarfile
import zipfile


PACKAGE = Path(sys.argv[1]).resolve()
ARCHIVE_NAME = (
    "simultaneous_amplifier_beyond_three_halves_"
    "source_and_certificates.tar.gz"
)
PDF_NAME = "simultaneous_amplification_beyond_three_halves.pdf"
SOURCE_PDF = PurePosixPath(
    "universal_simultaneous_amplification/phase4_landmark_closure/"
    "paper_hybrid_threshold/output/pdf/"
    "simultaneous_amplification_beyond_three_halves.pdf"
)
PAPER = PurePosixPath(
    "universal_simultaneous_amplification/phase4_landmark_closure/"
    "paper_hybrid_threshold"
)
EXPECTED_ARCHIVE_SHA256 = (
    "d2145513f8abe295e9e7fab62f062fa9d0f7a6282de95e8155f3db4621485274"
)
EXPECTED_PDF_SHA256 = (
    "4e86597bb0baff388e8ce7ccf6ffd808f86b5ea846acf6f2188b31016fd2572c"
)
EXPECTED_EPOCH = 1_787_356_800
EXPECTED_WHEELS = {
    "mpmath-1.3.0-py3-none-any.whl": (
        "mpmath",
        "1.3.0",
        "a0b2b9fe80bbcd81a6647ff13108738cfb482d481d826cc0e02f5b35e5c88d2c",
    ),
    "sympy-1.14.0-py3-none-any.whl": (
        "sympy",
        "1.14.0",
        "e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5",
    ),
}
PACKAGE_EXECUTABLES = {
    PurePosixPath("run_all_referee_checks.sh"),
    PurePosixPath("verify_git_binding.py"),
    PurePosixPath("verify_referee_package.py"),
}
SOURCE_EXECUTABLES = {
    PAPER / "all.sh",
    PAPER / "bootstrap_replay.sh",
    PAPER / "build.sh",
    PAPER / "bundle_manifest.py",
    PAPER / "release_bundle.sh",
    PAPER / "replay.sh",
    PAPER / "verify_paper_claims.py",
}
HEX64 = re.compile(r"[0-9a-f]{64}")


class AuditFailure(RuntimeError):
    pass


def require(condition: object, message: str) -> None:
    if not bool(condition):
        raise AuditFailure(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(raw: str, label: str) -> PurePosixPath:
    name = PurePosixPath(raw)
    require(raw != "", f"{label}: empty path")
    require(not name.is_absolute(), f"{label}: absolute path {raw!r}")
    require(".." not in name.parts, f"{label}: traversal path {raw!r}")
    require(name.as_posix() == raw, f"{label}: noncanonical path {raw!r}")
    return name


def parse_manifest(data: bytes, label: str) -> dict[PurePosixPath, str]:
    rows: dict[PurePosixPath, str] = {}
    text = data.decode("ascii")
    require(text.endswith("\n"), f"{label}: missing final newline")
    for line_number, line in enumerate(text.splitlines(), 1):
        fields = line.split("  ", 1)
        require(len(fields) == 2, f"{label}:{line_number}: malformed row")
        digest, raw = fields
        require(HEX64.fullmatch(digest), f"{label}:{line_number}: bad digest")
        name = safe_name(raw, f"{label}:{line_number}")
        require(name not in rows, f"{label}:{line_number}: duplicate {name}")
        rows[name] = digest
    require(rows, f"{label}: empty")
    return rows


def expected_source_mode(name: PurePosixPath) -> int:
    return 0o755 if name in SOURCE_EXECUTABLES else 0o644


def expected_package_mode(name: PurePosixPath) -> int:
    if name in PACKAGE_EXECUTABLES:
        return 0o755
    if name.parts[:1] == ("source_and_certificates",):
        return expected_source_mode(PurePosixPath(*name.parts[1:]))
    return 0o644


def audit_package_manifest() -> dict[PurePosixPath, bytes]:
    manifest_path = PACKAGE / "PACKAGE_MANIFEST.sha256"
    expected = parse_manifest(manifest_path.read_bytes(), "PACKAGE_MANIFEST.sha256")
    actual: dict[PurePosixPath, bytes] = {}
    for path in sorted(PACKAGE.rglob("*")):
        require(not path.is_symlink(), f"package symlink: {path}")
        if path.is_dir():
            continue
        require(path.is_file(), f"package non-regular node: {path}")
        relative = PurePosixPath(path.relative_to(PACKAGE).as_posix())
        mode = stat.S_IMODE(path.stat().st_mode)
        required_mode = (
            0o644 if relative == PurePosixPath("PACKAGE_MANIFEST.sha256")
            else expected_package_mode(relative)
        )
        require(mode == required_mode, f"package mode {mode:#06o}: {relative}")
        if relative != PurePosixPath("PACKAGE_MANIFEST.sha256"):
            actual[relative] = path.read_bytes()
    require(set(actual) == set(expected), "outer manifest file set mismatch")
    for name, data in actual.items():
        require(sha256(data) == expected[name], f"outer manifest hash mismatch: {name}")
    print(f"PASS independent outer manifest: {len(actual)} payload files")
    return actual


def audit_archive(actual: dict[PurePosixPath, bytes]) -> dict[PurePosixPath, bytes]:
    archive_name = PurePosixPath(ARCHIVE_NAME)
    archive_bytes = actual[archive_name]
    archive_digest = sha256(archive_bytes)
    require(archive_digest == EXPECTED_ARCHIVE_SHA256, "frozen archive digest mismatch")
    sidecar_name = PurePosixPath(f"{ARCHIVE_NAME}.sha256")
    expected_sidecar = f"{archive_digest}  {ARCHIVE_NAME}\n".encode("ascii")
    require(actual[sidecar_name] == expected_sidecar, "detached archive sidecar mismatch")

    require(archive_bytes[:2] == b"\x1f\x8b", "archive is not gzip")
    gzip_mtime = int.from_bytes(archive_bytes[4:8], "little")
    require(gzip_mtime == EXPECTED_EPOCH, f"gzip mtime mismatch: {gzip_mtime}")
    uncompressed = gzip.GzipFile(fileobj=io.BytesIO(archive_bytes)).read()
    payloads: dict[PurePosixPath, bytes] = {}
    modes: dict[PurePosixPath, int] = {}
    with tarfile.open(fileobj=io.BytesIO(uncompressed), mode="r:") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        require(names == sorted(names), "archive member order is not sorted")
        require(len(names) == len(set(names)), "duplicate archive member names")
        require(len(names) == 23, f"unexpected archive member count: {len(names)}")
        for member in members:
            require(member.isfile(), f"non-regular archive member: {member.name}")
            name = safe_name(member.name, "source archive")
            require(name not in payloads, f"duplicate archive member: {name}")
            require(member.mode == expected_source_mode(name), f"archive mode: {name}")
            require(member.uid == 0 and member.gid == 0, f"archive uid/gid: {name}")
            require(member.uname == "root" and member.gname == "root", f"archive owner: {name}")
            require(member.mtime == EXPECTED_EPOCH, f"archive mtime: {name}")
            stream = archive.extractfile(member)
            require(stream is not None, f"unreadable archive member: {name}")
            payloads[name] = stream.read()
            modes[name] = member.mode

    manifest_name = PurePosixPath("MANIFEST.sha256")
    manifest = parse_manifest(payloads[manifest_name], "archive MANIFEST.sha256")
    non_manifest = {name: data for name, data in payloads.items() if name != manifest_name}
    require(set(manifest) == set(non_manifest), "internal manifest file set mismatch")
    for name, data in non_manifest.items():
        require(sha256(data) == manifest[name], f"internal archive hash mismatch: {name}")

    extracted_root = PACKAGE / "source_and_certificates"
    extracted: dict[PurePosixPath, bytes] = {}
    for path in sorted(extracted_root.rglob("*")):
        require(not path.is_symlink(), f"extracted symlink: {path}")
        if path.is_dir():
            continue
        require(path.is_file(), f"extracted non-regular node: {path}")
        name = PurePosixPath(path.relative_to(extracted_root).as_posix())
        require(stat.S_IMODE(path.stat().st_mode) == modes[name], f"extracted mode: {name}")
        extracted[name] = path.read_bytes()
    require(set(extracted) == set(payloads), "extracted/archive file set mismatch")
    for name, data in payloads.items():
        require(extracted[name] == data, f"extracted/archive bytes differ: {name}")

    convenience = actual[PurePosixPath(PDF_NAME)]
    require(convenience == payloads[SOURCE_PDF], "convenience/source PDF mismatch")
    require(sha256(convenience) == EXPECTED_PDF_SHA256, "frozen PDF digest mismatch")
    print(
        "PASS independent archive/sidecar/internal-manifest/extraction/PDF audit: "
        f"23 members; archive={archive_digest}; pdf={sha256(convenience)}"
    )
    return payloads


def wheel_record_digest(data: bytes) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode("ascii").rstrip("=")


def metadata_field(metadata: str, field: str) -> str:
    prefix = f"{field}: "
    matches = [line[len(prefix):] for line in metadata.splitlines() if line.startswith(prefix)]
    require(len(matches) == 1, f"wheel metadata field {field!r}: {matches}")
    return matches[0]


def audit_wheel(path: Path, expected_name: str, expected_version: str, expected_hash: str) -> None:
    data = path.read_bytes()
    require(sha256(data) == expected_hash, f"wheel digest mismatch: {path.name}")
    with zipfile.ZipFile(io.BytesIO(data)) as wheel:
        infos = wheel.infolist()
        names = [info.filename for info in infos]
        require(len(names) == len(set(names)), f"duplicate wheel members: {path.name}")
        for info in infos:
            safe_name(info.filename.rstrip("/"), f"wheel {path.name}")
            require(not (info.flag_bits & 0x1), f"encrypted wheel member: {info.filename}")
            unix_mode = (info.external_attr >> 16) & 0o170000
            require(unix_mode != stat.S_IFLNK, f"wheel symlink: {info.filename}")
        dist_info = f"{expected_name}-{expected_version}.dist-info"
        metadata_name = f"{dist_info}/METADATA"
        wheel_name = f"{dist_info}/WHEEL"
        record_name = f"{dist_info}/RECORD"
        require(metadata_name in names, f"missing METADATA: {path.name}")
        require(wheel_name in names, f"missing WHEEL: {path.name}")
        require(record_name in names, f"missing RECORD: {path.name}")
        metadata = wheel.read(metadata_name).decode("utf-8")
        require(metadata_field(metadata, "Name").lower() == expected_name, f"wheel name: {path.name}")
        require(metadata_field(metadata, "Version") == expected_version, f"wheel version: {path.name}")
        wheel_metadata = wheel.read(wheel_name).decode("utf-8")
        require("Root-Is-Purelib: true" in wheel_metadata, f"not purelib: {path.name}")
        require("Tag: py3-none-any" in wheel_metadata, f"wrong wheel tag: {path.name}")

        rows = list(csv.reader(io.StringIO(wheel.read(record_name).decode("utf-8"))))
        record_paths: set[str] = set()
        for row_number, row in enumerate(rows, 1):
            require(len(row) == 3, f"RECORD row shape {path.name}:{row_number}")
            member_name, digest, size = row
            safe_name(member_name, f"RECORD {path.name}:{row_number}")
            require(member_name not in record_paths, f"duplicate RECORD row: {member_name}")
            record_paths.add(member_name)
            if member_name == record_name:
                require(digest == "" and size == "", f"RECORD self-row not blank: {path.name}")
            else:
                require(member_name in names, f"RECORD names absent member: {member_name}")
                member_data = wheel.read(member_name)
                require(
                    digest == f"sha256={wheel_record_digest(member_data)}",
                    f"RECORD digest mismatch: {member_name}",
                )
                require(size == str(len(member_data)), f"RECORD size mismatch: {member_name}")
        require(record_paths == set(names), f"RECORD/member set mismatch: {path.name}")
        require(
            any("license" in name.lower() for name in names),
            f"wheel lacks license payload: {path.name}",
        )
        print(f"PASS wheel {path.name}: {len(names)} safe RECORD-verified members")


def audit_python_sources(payloads: dict[PurePosixPath, bytes]) -> None:
    parsed = 0
    for name, data in payloads.items():
        if name.suffix != ".py":
            continue
        tree = ast.parse(data.decode("utf-8"), filename=name.as_posix())
        assertions = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Assert)]
        require(not assertions, f"bare asserts remain in {name}: {assertions}")
        parsed += 1
    for outer_name in ("verify_referee_package.py", "verify_git_binding.py"):
        path = PACKAGE / outer_name
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        assertions = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Assert)]
        require(not assertions, f"bare asserts remain in {outer_name}: {assertions}")
        parsed += 1
    print(f"PASS AST fail-closed scan: {parsed} Python programs, zero bare asserts")


def main() -> None:
    require(sys.flags.optimize == 0, "independent audit itself refuses optimized Python")
    actual = audit_package_manifest()
    payloads = audit_archive(actual)
    vendor = PACKAGE / "source_and_certificates" / PAPER / "vendor"
    for filename, (name, version, digest) in EXPECTED_WHEELS.items():
        audit_wheel(vendor / filename, name, version, digest)
    audit_python_sources(payloads)
    print("PASS independent package/software static audit")


if __name__ == "__main__":
    main()
