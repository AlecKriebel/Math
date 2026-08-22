#!/usr/bin/env python3
"""Independent byte, path, mode, order, and manifest audit of both deliverable archives."""

from __future__ import annotations

import hashlib
import pathlib
import posixpath
import stat
import sys
import tarfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "delivered_copy"
OUTER = ROOT / "paper_ii_referee_package_v2.0.2.tar.gz"
SOURCE = PACKAGE / "simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz"
PREFIX = "paper_ii_simultaneous_amplification_referee_package_2026-08-22/"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(name: str) -> bool:
    if not name or name.startswith(("/", "\\")) or "\\" in name:
        return False
    return posixpath.normpath(name) == name and name not in (".", "..") and not name.startswith("../")


def regular_members(archive: pathlib.Path) -> list[tarfile.TarInfo]:
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
    names = [member.name for member in members]
    if len(names) != len(set(names)):
        fail(f"duplicate archive path in {archive.name}")
    for member in members:
        if not safe_path(member.name):
            fail(f"unsafe archive path in {archive.name}: {member.name}")
        if not member.isfile():
            fail(f"non-regular archive member in {archive.name}: {member.name} ({member.type!r})")
    if names != sorted(names):
        fail(f"archive paths are not bytewise sorted in {archive.name}")
    return members


def compare_archive_to_tree(archive: pathlib.Path, tree: pathlib.Path, prefix: str = "") -> None:
    members = regular_members(archive)
    archive_paths = []
    with tarfile.open(archive, "r:gz") as handle:
        for member in members:
            if prefix and not member.name.startswith(prefix):
                fail(f"unexpected top-level path in {archive.name}: {member.name}")
            relative = member.name[len(prefix):]
            archive_paths.append(relative)
            disk_path = tree / relative
            if not disk_path.is_file() or disk_path.is_symlink():
                fail(f"archive member lacks regular disk counterpart: {relative}")
            extracted = handle.extractfile(member)
            if extracted is None or extracted.read() != disk_path.read_bytes():
                fail(f"archive/disk byte mismatch: {relative}")
            disk_mode = stat.S_IMODE(disk_path.stat().st_mode)
            if member.mode != disk_mode:
                fail(f"archive/disk mode mismatch for {relative}: {oct(member.mode)} vs {oct(disk_mode)}")
    disk_paths = sorted(str(path.relative_to(tree)) for path in tree.rglob("*") if path.is_file() and not path.is_symlink())
    if archive_paths != disk_paths:
        fail(f"archive/tree path set mismatch in {archive.name}")
    print(f"PASS {archive.name}: {len(members)} safe, unique, sorted regular files; bytes and modes match tree")


def parse_manifest(path: pathlib.Path) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fields = line.split("  ", 1)
        if len(fields) != 2 or len(fields[0]) != 64 or fields[1] in parsed:
            fail(f"malformed manifest line {path}:{line_number}")
        parsed[fields[1]] = fields[0]
    if list(parsed) != sorted(parsed):
        fail(f"manifest is not sorted: {path}")
    return parsed


def check_manifest(path: pathlib.Path, tree: pathlib.Path, exclusions: set[str]) -> None:
    entries = parse_manifest(path)
    actual = sorted(str(item.relative_to(tree)) for item in tree.rglob("*") if item.is_file() and not item.is_symlink() and str(item.relative_to(tree)) not in exclusions)
    if list(entries) != actual:
        fail(f"manifest path set mismatch: {path}")
    for relative, expected in entries.items():
        observed = sha256((tree / relative).read_bytes())
        if observed != expected:
            fail(f"manifest hash mismatch: {relative}")
    print(f"PASS {path.name}: exact sorted path set and {len(entries)} SHA-256 values")


def main() -> None:
    if sha256(OUTER.read_bytes()) != "2216c6a31545b38d9ca89c9d43c5a309bfcc6c2c1f7ab63ea5fabc171116e1d2":
        fail("outer archive identity mismatch")
    if sha256(SOURCE.read_bytes()) != "d2145513f8abe295e9e7fab62f062fa9d0f7a6282de95e8155f3db4621485274":
        fail("source archive identity mismatch")

    compare_archive_to_tree(OUTER, PACKAGE, PREFIX)
    compare_archive_to_tree(SOURCE, PACKAGE / "source_and_certificates")
    check_manifest(PACKAGE / "PACKAGE_MANIFEST.sha256", PACKAGE, {"PACKAGE_MANIFEST.sha256"})
    check_manifest(PACKAGE / "source_and_certificates" / "MANIFEST.sha256", PACKAGE / "source_and_certificates", {"MANIFEST.sha256"})
    print("PASS frozen archive SHA-256 identities")


if __name__ == "__main__":
    main()
