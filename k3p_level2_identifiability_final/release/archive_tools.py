#!/usr/bin/env python3
"""Canonical TAR.GZ/ZIP construction and structural verification."""

from __future__ import annotations

import gzip
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tarfile
import zipfile
import zlib


PROJECT = Path(__file__).resolve().parents[1]
REPRO = PROJECT / "reproducibility"
if str(REPRO) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(REPRO))

from release_common import (  # noqa: E402
    ReleaseFailure,
    atomic_write,
    canonical_json_bytes,
    pretty_json_bytes,
    require,
    safe_relative_path,
    sha256_bytes,
)


MANIFEST_NAME = "ARCHIVE_MANIFEST.json"


def canonical_mode(relative: str) -> int:
    return 0o755 if relative.endswith((".py", ".sh")) else 0o644


def manifest_for(kind: str, archive_root: str, source_commit: str,
                 source_date_epoch: int, members: dict[str, bytes],
                 extra: dict | None = None) -> dict:
    safe_relative_path(archive_root)
    require(len(PurePosixPath(archive_root).parts) == 1, "archive root must be one component")
    require(re.fullmatch(r"[0-9a-f]{40,64}", source_commit) is not None,
            ("invalid archive source commit", source_commit))
    require(isinstance(source_date_epoch, int) and source_date_epoch >= 0,
            ("invalid source-date epoch", source_date_epoch))
    require(MANIFEST_NAME not in members, "manifest name reserved")
    rows = []
    for relative in sorted(members):
        safe_relative_path(relative)
        rows.append({
            "path": relative,
            "bytes": len(members[relative]),
            "sha256": sha256_bytes(members[relative]),
            "mode": format(canonical_mode(relative), "04o"),
        })
    value = {
        "schema": "k3p-canonical-archive-manifest-v1",
        "kind": kind,
        "archive_root": archive_root,
        "source_commit": source_commit,
        "source_date_epoch": source_date_epoch,
        "member_count_excluding_manifest": len(rows),
        "members": rows,
        "outer_archive_hash_included": False,
        "self_referential_hash_forbidden": True,
        "canonical_toolchain": {
            "python": sys.version.split()[0],
            "zlib_compile": zlib.ZLIB_VERSION,
            "zlib_runtime": zlib.ZLIB_RUNTIME_VERSION,
        },
    }
    if extra:
        require("payload_sha256" not in extra, "extra payload_sha256 forbidden")
        value["metadata"] = extra
    value["payload_sha256"] = sha256_bytes(canonical_json_bytes(value))
    return value


def deterministic_tar_gz(output: Path, *, kind: str, archive_root: str,
                         source_commit: str, source_date_epoch: int,
                         members: dict[str, bytes], extra: dict | None = None) -> dict:
    manifest = manifest_for(
        kind, archive_root, source_commit, source_date_epoch, members, extra
    )
    complete = dict(members)
    complete[MANIFEST_NAME] = pretty_json_bytes(manifest)
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0,
                       compresslevel=9) as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
            for relative in sorted(complete):
                data = complete[relative]
                info = tarfile.TarInfo(f"{archive_root}/{relative}")
                info.size = len(data)
                info.mode = canonical_mode(relative)
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                info.mtime = source_date_epoch
                info.pax_headers = {}
                archive.addfile(info, io.BytesIO(data))
    atomic_write(output, buffer.getvalue())
    return {
        "path": str(output),
        "bytes": output.stat().st_size,
        "sha256": sha256_bytes(buffer.getvalue()),
        "manifest_payload_sha256": manifest["payload_sha256"],
        "member_count": len(complete),
    }


def zip_datetime(epoch: int) -> tuple[int, int, int, int, int, int]:
    import datetime as dt
    value = dt.datetime.fromtimestamp(max(epoch, 315532800), tz=dt.timezone.utc)
    # ZIP stores seconds at two-second granularity.
    return (value.year, value.month, value.day, value.hour, value.minute,
            value.second - value.second % 2)


def deterministic_zip(output: Path, *, kind: str, archive_root: str,
                      source_commit: str, source_date_epoch: int,
                      members: dict[str, bytes], extra: dict | None = None) -> dict:
    manifest = manifest_for(
        kind, archive_root, source_commit, source_date_epoch, members, extra
    )
    complete = dict(members)
    complete[MANIFEST_NAME] = pretty_json_bytes(manifest)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9, strict_timestamps=True) as archive:
        for relative in sorted(complete):
            data = complete[relative]
            info = zipfile.ZipInfo(
                f"{archive_root}/{relative}", date_time=zip_datetime(source_date_epoch)
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | canonical_mode(relative)) << 16
            info.flag_bits = 0x800
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    atomic_write(output, buffer.getvalue())
    return {
        "path": str(output),
        "bytes": output.stat().st_size,
        "sha256": sha256_bytes(buffer.getvalue()),
        "manifest_payload_sha256": manifest["payload_sha256"],
        "member_count": len(complete),
    }


def validate_manifest(manifest: dict, *, archive_root: str,
                      observed: dict[str, tuple[bytes, int]]) -> None:
    require("archive_sha256" not in json.dumps(manifest, sort_keys=True),
            "SELF_REFERENTIAL_ARCHIVE_HASH")
    required_keys = {
        "schema", "kind", "archive_root", "source_commit", "source_date_epoch",
        "member_count_excluding_manifest", "members", "outer_archive_hash_included",
        "self_referential_hash_forbidden", "canonical_toolchain", "payload_sha256",
    }
    require(set(manifest) in (required_keys, required_keys | {"metadata"}),
            ("archive manifest field set", sorted(set(manifest) - required_keys)))
    require(manifest.get("schema") == "k3p-canonical-archive-manifest-v1",
            "archive manifest schema")
    require(manifest.get("archive_root") == archive_root, "archive root binding")
    require(re.fullmatch(r"[0-9a-f]{40,64}", str(manifest.get("source_commit"))) is not None,
            "archive source commit format")
    require(isinstance(manifest.get("source_date_epoch"), int) and
            manifest["source_date_epoch"] >= 0, "archive source-date epoch")
    require(manifest.get("outer_archive_hash_included") is False and
            manifest.get("self_referential_hash_forbidden") is True,
            "archive self-reference policy")
    toolchain = manifest.get("canonical_toolchain")
    require(isinstance(toolchain, dict) and set(toolchain) == {
        "python", "zlib_compile", "zlib_runtime"
    } and all(isinstance(value, str) and value for value in toolchain.values()),
            "archive canonical toolchain metadata")
    if "metadata" in manifest:
        require(isinstance(manifest["metadata"], dict), "archive metadata object")
    claimed = manifest.get("payload_sha256")
    body = dict(manifest)
    body.pop("payload_sha256", None)
    require(claimed == sha256_bytes(canonical_json_bytes(body)),
            "archive manifest payload hash")
    expected: dict[str, tuple[str, int, int]] = {}
    require(isinstance(manifest.get("members"), list), "archive manifest members list")
    for row in manifest["members"]:
        require(isinstance(row, dict) and set(row) == {"path", "bytes", "sha256", "mode"},
                "archive manifest member row schema")
        relative = row.get("path")
        safe_relative_path(relative)
        require(relative not in expected, ("duplicate manifest path", relative))
        expected[relative] = (row.get("sha256"), row.get("bytes"),
                              int(row.get("mode"), 8))
        require(expected[relative][2] == canonical_mode(relative),
                ("noncanonical manifest mode", relative, expected[relative][2]))
    require(manifest.get("member_count_excluding_manifest") == len(expected),
            "archive manifest member count")
    require(set(observed) == set(expected),
            ("archive/manifest member set mismatch",
             sorted(set(expected) - set(observed)), sorted(set(observed) - set(expected))))
    for relative, (data, mode) in observed.items():
        digest, size, expected_mode = expected[relative]
        require(sha256_bytes(data) == digest and len(data) == size,
                ("archive member hash or size", relative))
        require(mode == expected_mode, ("archive member mode", relative, mode, expected_mode))


def verify_tar_gz(path: Path) -> dict:
    raw = path.read_bytes()
    require(len(raw) >= 10 and raw[:2] == b"\x1f\x8b", "not a gzip stream")
    require(int.from_bytes(raw[4:8], "little") == 0, "noncanonical gzip mtime")
    names: list[str] = []
    member_data: dict[str, tuple[bytes, int]] = {}
    manifest = None
    root = None
    with tarfile.open(path, mode="r:gz") as archive:
        for info in archive.getmembers():
            require(info.isfile() and not (info.issym() or info.islnk()),
                    ("nonregular TAR member", info.name))
            safe_relative_path(info.name)
            parts = PurePosixPath(info.name).parts
            require(len(parts) >= 2, ("TAR member missing archive root", info.name))
            root = root or parts[0]
            require(parts[0] == root, ("multiple TAR roots", info.name))
            relative = PurePosixPath(*parts[1:]).as_posix()
            safe_relative_path(relative)
            require(relative not in member_data,
                    ("duplicate TAR member", relative))
            if relative == MANIFEST_NAME:
                require(manifest is None, "duplicate TAR manifest")
            require(info.uid == info.gid == 0 and info.uname == info.gname == "",
                    ("noncanonical TAR ownership", relative))
            require(info.mode == canonical_mode(relative),
                    ("noncanonical TAR mode", relative, info.mode))
            data_handle = archive.extractfile(info)
            require(data_handle is not None, ("unreadable TAR member", relative))
            data = data_handle.read()
            if relative == MANIFEST_NAME:
                manifest = json.loads(data.decode("utf-8"))
            else:
                member_data[relative] = (data, info.mode)
            names.append(info.name)
    require(names == sorted(names) and len(names) == len(set(names)),
            "TAR member ordering or duplication")
    require(isinstance(manifest, dict) and isinstance(root, str), "missing TAR manifest")
    epoch = manifest.get("source_date_epoch")
    with tarfile.open(path, mode="r:gz") as archive:
        require(all(info.mtime == epoch for info in archive.getmembers()),
                "noncanonical TAR member mtime")
    validate_manifest(manifest, archive_root=root, observed=member_data)
    return {
        "status": "PASS", "kind": manifest.get("kind"), "archive_root": root,
        "source_commit": manifest.get("source_commit"),
        "source_date_epoch": manifest.get("source_date_epoch"),
        "metadata": manifest.get("metadata"), "member_count": len(names),
        "sha256": sha256_bytes(raw), "manifest_payload_sha256": manifest["payload_sha256"],
    }


def verify_zip(path: Path) -> dict:
    names: list[str] = []
    member_data: dict[str, tuple[bytes, int]] = {}
    manifest = None
    root = None
    with zipfile.ZipFile(path, mode="r") as archive:
        require(archive.testzip() is None, "ZIP CRC failure")
        for info in archive.infolist():
            require(not info.is_dir(), ("directory ZIP member forbidden", info.filename))
            safe_relative_path(info.filename)
            parts = PurePosixPath(info.filename).parts
            require(len(parts) >= 2, ("ZIP member missing archive root", info.filename))
            root = root or parts[0]
            require(parts[0] == root, ("multiple ZIP roots", info.filename))
            relative = PurePosixPath(*parts[1:]).as_posix()
            safe_relative_path(relative)
            require(relative not in member_data,
                    ("duplicate ZIP member", relative))
            if relative == MANIFEST_NAME:
                require(manifest is None, "duplicate ZIP manifest")
            mode = (info.external_attr >> 16) & 0o7777
            require(mode == canonical_mode(relative),
                    ("noncanonical ZIP mode", relative, mode))
            data = archive.read(info)
            if relative == MANIFEST_NAME:
                manifest = json.loads(data.decode("utf-8"))
            else:
                member_data[relative] = (data, mode)
            names.append(info.filename)
    require(names == sorted(names) and len(names) == len(set(names)),
            "ZIP member ordering or duplication")
    require(isinstance(manifest, dict) and isinstance(root, str), "missing ZIP manifest")
    require(isinstance(manifest.get("source_date_epoch"), int),
            "archive source-date epoch")
    expected_time = zip_datetime(manifest["source_date_epoch"])
    with zipfile.ZipFile(path, mode="r") as archive:
        require(all(info.date_time == expected_time for info in archive.infolist()),
                "noncanonical ZIP member mtime")
    validate_manifest(manifest, archive_root=root, observed=member_data)
    return {
        "status": "PASS", "kind": manifest.get("kind"), "archive_root": root,
        "source_commit": manifest.get("source_commit"),
        "source_date_epoch": manifest.get("source_date_epoch"),
        "metadata": manifest.get("metadata"), "member_count": len(names),
        "sha256": sha256_bytes(path.read_bytes()),
        "manifest_payload_sha256": manifest["payload_sha256"],
    }


def safe_extract_zip(path: Path, destination: Path) -> None:
    """Extract validated regular ZIP members without ZipFile.extract()."""
    verify_zip(path)
    destination = destination.resolve()
    with zipfile.ZipFile(path, mode="r") as archive:
        for info in archive.infolist():
            safe_relative_path(info.filename)
            target = (destination / info.filename).resolve()
            try:
                target.relative_to(destination)
            except ValueError as error:
                raise ReleaseFailure(("ZIP extraction traversal", info.filename)) from error
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(info))
            target.chmod((info.external_attr >> 16) & 0o7777)


def safe_extract_tar_gz(path: Path, destination: Path) -> None:
    """Extract validated regular TAR.GZ members without TarFile.extract()."""
    verify_tar_gz(path)
    destination = destination.resolve()
    with tarfile.open(path, mode="r:gz") as archive:
        for info in archive.getmembers():
            safe_relative_path(info.name)
            target = (destination / info.name).resolve()
            try:
                target.relative_to(destination)
            except ValueError as error:
                raise ReleaseFailure(("TAR extraction traversal", info.name)) from error
            handle = archive.extractfile(info)
            require(handle is not None, ("unreadable TAR member", info.name))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(handle.read())
            target.chmod(info.mode)
