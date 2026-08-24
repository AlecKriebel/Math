#!/usr/bin/env python3
"""Independent, standard-library-only audit of the frozen v2.0.3 package."""

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
OUTER_ARCHIVE = Path(sys.argv[2]).resolve()
ROOT_NAME = "paper_ii_simultaneous_amplification_referee_package_2026-08-22"
SOURCE_ARCHIVE = "simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz"
PDF = "simultaneous_amplification_beyond_three_halves.pdf"
PAPER = PurePosixPath(
    "universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold"
)
SOURCE_PDF = PAPER / "output/pdf" / PDF
EXPECTED_SOURCE_SHA256 = "e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae"
EXPECTED_PDF_SHA256 = "1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9"
EXPECTED_OUTER_SHA256 = "f4baf76a66a12e4942f13bd7c73bbead0ff31555df5b69a489b914064c597bdf"
EXPECTED_EPOCH = 1_787_356_800
HEX64 = re.compile(r"[0-9a-f]{64}")
SOURCE_EXECUTABLES = {
    PAPER / name
    for name in (
        "all.sh",
        "bootstrap_replay.sh",
        "build.sh",
        "bundle_manifest.py",
        "release_bundle.sh",
        "replay.sh",
        "verify_paper_claims.py",
    )
}
PACKAGE_EXECUTABLES = {
    PurePosixPath("run_all_referee_checks.sh"),
    PurePosixPath("verify_git_binding.py"),
    PurePosixPath("verify_referee_package.py"),
}
WHEELS = {
    "mpmath-1.3.0-py3-none-any.whl": (
        "mpmath", "1.3.0",
        "a0b2b9fe80bbcd81a6647ff13108738cfb482d481d826cc0e02f5b35e5c88d2c",
    ),
    "sympy-1.14.0-py3-none-any.whl": (
        "sympy", "1.14.0",
        "e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5",
    ),
}


class Failure(RuntimeError):
    pass


def require(value: object, message: str) -> None:
    if not bool(value):
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe(raw: str, label: str) -> PurePosixPath:
    name = PurePosixPath(raw)
    require(raw != "", f"{label}: empty path")
    require(not name.is_absolute(), f"{label}: absolute path: {raw!r}")
    require(".." not in name.parts, f"{label}: traversal path: {raw!r}")
    require(name.as_posix() == raw, f"{label}: noncanonical path: {raw!r}")
    return name


def manifest(data: bytes, label: str) -> dict[PurePosixPath, str]:
    require(data.endswith(b"\n"), f"{label}: no final newline")
    rows: dict[PurePosixPath, str] = {}
    for line_number, line in enumerate(data.decode("ascii").splitlines(), 1):
        fields = line.split("  ", 1)
        require(len(fields) == 2, f"{label}:{line_number}: malformed")
        sha, raw = fields
        require(HEX64.fullmatch(sha), f"{label}:{line_number}: invalid digest")
        name = safe(raw, f"{label}:{line_number}")
        require(name not in rows, f"{label}:{line_number}: duplicate {name}")
        rows[name] = sha
    return rows


def source_mode(name: PurePosixPath) -> int:
    return 0o755 if name in SOURCE_EXECUTABLES else 0o644


def package_mode(name: PurePosixPath) -> int:
    if name in PACKAGE_EXECUTABLES:
        return 0o755
    if name.parts[:1] == ("source_and_certificates",):
        return source_mode(PurePosixPath(*name.parts[1:]))
    return 0o644


def filesystem_payloads() -> dict[PurePosixPath, bytes]:
    expected = manifest((PACKAGE / "PACKAGE_MANIFEST.sha256").read_bytes(), "outer manifest")
    actual: dict[PurePosixPath, bytes] = {}
    for path in sorted(PACKAGE.rglob("*")):
        require(not path.is_symlink(), f"package symlink: {path}")
        if path.is_dir():
            continue
        require(path.is_file(), f"package nonregular node: {path}")
        name = PurePosixPath(path.relative_to(PACKAGE).as_posix())
        required = 0o644 if name == PurePosixPath("PACKAGE_MANIFEST.sha256") else package_mode(name)
        require(stat.S_IMODE(path.stat().st_mode) == required, f"package mode mismatch: {name}")
        if name != PurePosixPath("PACKAGE_MANIFEST.sha256"):
            actual[name] = path.read_bytes()
    require(set(actual) == set(expected), "outer manifest file-set mismatch")
    for name, data in actual.items():
        require(digest(data) == expected[name], f"outer manifest hash mismatch: {name}")
    print(f"PASS package manifest: {len(actual)} payload files; exact modes")
    return actual


def read_tar(data: bytes, label: str) -> tuple[dict[PurePosixPath, bytes], dict[PurePosixPath, int]]:
    require(data[:2] == b"\x1f\x8b", f"{label}: not gzip")
    require(int.from_bytes(data[4:8], "little") == EXPECTED_EPOCH, f"{label}: gzip mtime")
    raw = gzip.GzipFile(fileobj=io.BytesIO(data)).read()
    payloads: dict[PurePosixPath, bytes] = {}
    modes: dict[PurePosixPath, int] = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        require(names == sorted(names), f"{label}: unsorted members")
        require(len(names) == len(set(names)), f"{label}: duplicate members")
        for member in members:
            require(member.isfile(), f"{label}: nonregular member {member.name}")
            name = safe(member.name, label)
            require(member.uid == 0 and member.gid == 0, f"{label}: uid/gid {name}")
            require(member.uname == "root" and member.gname == "root", f"{label}: owner {name}")
            require(member.mtime == EXPECTED_EPOCH, f"{label}: mtime {name}")
            stream = archive.extractfile(member)
            require(stream is not None, f"{label}: unreadable {name}")
            payloads[name] = stream.read()
            modes[name] = member.mode
    return payloads, modes


def source_archive(outer: dict[PurePosixPath, bytes]) -> dict[PurePosixPath, bytes]:
    data = outer[PurePosixPath(SOURCE_ARCHIVE)]
    require(digest(data) == EXPECTED_SOURCE_SHA256, "source archive frozen digest")
    sidecar = f"{EXPECTED_SOURCE_SHA256}  {SOURCE_ARCHIVE}\n".encode("ascii")
    require(outer[PurePosixPath(SOURCE_ARCHIVE + ".sha256")] == sidecar, "source sidecar")
    payloads, modes = read_tar(data, "source archive")
    require(len(payloads) == 23, f"source member count: {len(payloads)}")
    for name, mode in modes.items():
        require(mode == source_mode(name), f"source archive mode: {name}")
    internal = manifest(payloads[PurePosixPath("MANIFEST.sha256")], "internal manifest")
    content = {name: data for name, data in payloads.items() if name != PurePosixPath("MANIFEST.sha256")}
    require(set(content) == set(internal), "internal manifest file-set mismatch")
    for name, member_data in content.items():
        require(digest(member_data) == internal[name], f"internal manifest hash mismatch: {name}")
    extracted: dict[PurePosixPath, bytes] = {}
    for path in sorted((PACKAGE / "source_and_certificates").rglob("*")):
        require(not path.is_symlink(), f"extracted symlink: {path}")
        if path.is_dir():
            continue
        name = PurePosixPath(path.relative_to(PACKAGE / "source_and_certificates").as_posix())
        require(stat.S_IMODE(path.stat().st_mode) == modes[name], f"extracted mode: {name}")
        extracted[name] = path.read_bytes()
    require(extracted == payloads, "extracted source tree differs from source archive")
    convenience = outer[PurePosixPath(PDF)]
    require(convenience == payloads[SOURCE_PDF], "convenience/source PDF differ")
    require(digest(convenience) == EXPECTED_PDF_SHA256, "PDF frozen digest")
    print("PASS source archive: 23 safe deterministic members; internal manifest/extraction/PDF exact")
    return payloads


def outer_archive(filesystem: dict[PurePosixPath, bytes]) -> None:
    data = OUTER_ARCHIVE.read_bytes()
    require(digest(data) == EXPECTED_OUTER_SHA256, "outer archive frozen digest")
    payloads, modes = read_tar(data, "outer archive")
    stripped: dict[PurePosixPath, bytes] = {}
    stripped_modes: dict[PurePosixPath, int] = {}
    for name, member_data in payloads.items():
        require(name.parts[:1] == (ROOT_NAME,), f"outer archive wrong root: {name}")
        inner = PurePosixPath(*name.parts[1:])
        require(inner.parts, "outer archive root-only member")
        stripped[inner] = member_data
        stripped_modes[inner] = modes[name]
    filesystem_all = dict(filesystem)
    filesystem_all[PurePosixPath("PACKAGE_MANIFEST.sha256")] = (PACKAGE / "PACKAGE_MANIFEST.sha256").read_bytes()
    require(stripped == filesystem_all, "outer archive/folder bytes differ")
    for name, mode in stripped_modes.items():
        required = 0o644 if name == PurePosixPath("PACKAGE_MANIFEST.sha256") else package_mode(name)
        require(mode == required, f"outer archive mode: {name}")
    print(f"PASS outer archive: {len(stripped)} safe deterministic members; folder bytes/modes exact")


def wheel_record(path: Path, expected_name: str, version: str, sha: str) -> None:
    data = path.read_bytes()
    require(digest(data) == sha, f"wheel digest: {path.name}")
    with zipfile.ZipFile(io.BytesIO(data)) as wheel:
        infos = wheel.infolist()
        names = [info.filename for info in infos]
        require(len(names) == len(set(names)), f"wheel duplicate member: {path.name}")
        for info in infos:
            safe(info.filename.rstrip("/"), f"wheel {path.name}")
            require(not (info.flag_bits & 1), f"wheel encrypted member: {info.filename}")
            require(((info.external_attr >> 16) & 0o170000) != stat.S_IFLNK, f"wheel symlink: {info.filename}")
        prefix = f"{expected_name}-{version}.dist-info"
        record_name = f"{prefix}/RECORD"
        metadata = wheel.read(f"{prefix}/METADATA").decode("utf-8")
        require(f"Name: {expected_name}" in metadata, f"wheel metadata name: {path.name}")
        require(f"Version: {version}" in metadata, f"wheel metadata version: {path.name}")
        rows = list(csv.reader(io.StringIO(wheel.read(record_name).decode("utf-8"))))
        seen: set[str] = set()
        for row in rows:
            require(len(row) == 3, f"wheel RECORD shape: {path.name}")
            member_name, member_digest, member_size = row
            safe(member_name, f"RECORD {path.name}")
            require(member_name not in seen, f"wheel RECORD duplicate: {member_name}")
            seen.add(member_name)
            if member_name == record_name:
                require(member_digest == "" and member_size == "", f"wheel RECORD self row: {path.name}")
            else:
                member_data = wheel.read(member_name)
                encoded = base64.urlsafe_b64encode(hashlib.sha256(member_data).digest()).decode().rstrip("=")
                require(member_digest == "sha256=" + encoded, f"wheel RECORD digest: {member_name}")
                require(member_size == str(len(member_data)), f"wheel RECORD size: {member_name}")
        require(seen == set(names), f"wheel RECORD/member set: {path.name}")
    print(f"PASS wheel: {path.name}; safe members and RECORD exact")


def static_python(payloads: dict[PurePosixPath, bytes]) -> None:
    programs = [(name.as_posix(), data) for name, data in payloads.items() if name.suffix == ".py"]
    programs += [(name, (PACKAGE / name).read_bytes()) for name in ("verify_referee_package.py", "verify_git_binding.py")]
    for name, data in programs:
        tree = ast.parse(data.decode("utf-8"), filename=name)
        assertions = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Assert)]
        require(not assertions, f"bare asserts in {name}: {assertions}")
    print(f"PASS Python AST fail-closed scan: {len(programs)} programs; zero bare asserts")


def main() -> None:
    require(sys.flags.optimize == 0, "independent audit refuses optimized Python")
    filesystem = filesystem_payloads()
    payloads = source_archive(filesystem)
    outer_archive(filesystem)
    vendor = PACKAGE / "source_and_certificates" / PAPER / "vendor"
    for filename, (name, version, sha) in WHEELS.items():
        wheel_record(vendor / filename, name, version, sha)
    static_python(payloads)
    print("PASS independent v2.0.3 package/static audit")


if __name__ == "__main__":
    main()
