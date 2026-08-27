#!/usr/bin/env python3
"""Independent byte-ledger audit for the 2026-08-26 K2P referee bundle.

This checker deliberately does not import any submitted package module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


PREFIX = "k2p_principal_d_plus_submission_referee"
MANIFEST = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
PORTABLE = "output/referee/REFEREE_BUNDLE_CONTENTS.json"
LOCK = "work/final_theorem_release/RELEASE_LOCK.json"


class AuditError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    require(isinstance(value, dict), f"JSON top level is not an object: {path}")
    return value


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: Any) -> str:
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def safe(relative: str) -> PurePosixPath:
    path = PurePosixPath(relative)
    require(
        bool(path.parts)
        and not path.is_absolute()
        and path.as_posix() == relative
        and "\\" not in relative
        and all(part not in {"", ".", ".."} for part in path.parts),
        f"unsafe path: {relative!r}",
    )
    return path


def file_row(root: Path, relative: str) -> dict[str, int | str]:
    path = root.joinpath(*safe(relative).parts)
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"not a regular file: {relative}")
    require(not path.is_symlink(), f"symbolic file: {relative}")
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha(data)}


def verify_rows(root: Path, rows: Any, label: str) -> dict[str, dict[str, int | str]]:
    require(isinstance(rows, dict), f"{label} is not a map")
    actual: dict[str, dict[str, int | str]] = {}
    for relative, declared in rows.items():
        require(isinstance(relative, str) and isinstance(declared, dict), f"malformed {label} row")
        row = file_row(root, relative)
        require(row == declared, f"{label} row mismatch: {relative}")
        actual[relative] = row
    return actual


def verify_release_rows(root: Path, rows: Any) -> dict[str, dict[str, int | str]]:
    """Verify byte fields while permitting the lock's additional layer tag."""
    require(isinstance(rows, dict), "release outer is not a map")
    actual: dict[str, dict[str, int | str]] = {}
    for relative, declared in rows.items():
        require(isinstance(relative, str) and isinstance(declared, dict), "malformed release row")
        row = file_row(root, relative)
        require(
            row["bytes"] == declared.get("bytes") and row["sha256"] == declared.get("sha256"),
            f"release outer row mismatch: {relative}",
        )
        require(isinstance(declared.get("layer"), str) and declared["layer"], f"release layer missing: {relative}")
        actual[relative] = row
    return actual


def parse_sha_manifest(root: Path, relative: str, base: str) -> dict[str, str]:
    result: dict[str, str] = {}
    text = root.joinpath(*safe(relative).parts).read_text(encoding="utf-8")
    for ordinal, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, f"bad manifest line {relative}:{ordinal}")
        digest, child = match.groups()
        if child.startswith("./"):
            child = child[2:]
        child_relative = (PurePosixPath(base) / safe(child)).as_posix()
        require(child_relative not in result, f"duplicate manifest path: {child_relative}")
        require(file_row(root, child_relative)["sha256"] == digest, f"manifest hash mismatch: {child_relative}")
        result[child_relative] = digest
    require(bool(result), f"empty manifest: {relative}")
    return result


def unsigned_payload(value: dict[str, Any], field: str = "payload_sha256") -> str:
    expected = value.get(field)
    body = dict(value)
    body.pop(field, None)
    actual = canonical_hash(body)
    require(expected == actual, f"payload mismatch: expected={expected} actual={actual}")
    return actual


def audit(root: Path, archive_path: Path) -> dict[str, Any]:
    root = root.resolve()
    require(root.is_dir() and not root.is_symlink(), f"invalid root: {root}")

    manifest = load_json(root / MANIFEST)
    manifest_payload = unsigned_payload(manifest)
    require(manifest.get("schema") == "k2p-revised-referee-bundle-manifest-v2", "manifest schema")

    frozen_declared = manifest.get("frozen_evidence")
    source_declared = manifest.get("submission_sources")
    require(isinstance(frozen_declared, dict) and isinstance(source_declared, dict), "missing ledger")
    frozen = verify_rows(root, frozen_declared.get("files"), "frozen")
    sources = verify_rows(root, source_declared.get("files"), "submission")
    require(not set(frozen) & set(sources), "frozen/submission overlap")

    def check_summary(declared: dict[str, Any], rows: dict[str, dict[str, int | str]], label: str) -> None:
        require(declared.get("file_count") == len(rows), f"{label} count")
        require(declared.get("total_bytes") == sum(int(row["bytes"]) for row in rows.values()), f"{label} bytes")
        require(declared.get("content_ledger_root_sha256") == canonical_hash(rows), f"{label} root")

    check_summary(frozen_declared, frozen, "frozen")
    check_summary(source_declared, sources, "submission")
    combined = {"frozen_evidence": frozen, "submission_sources": sources}
    require(manifest.get("combined_content_root_sha256") == canonical_hash(combined), "combined root")
    require(manifest.get("combined_file_count_excluding_manifest") == len(frozen) + len(sources), "combined count")

    expected_disk = set(frozen) | set(sources) | {MANIFEST}
    actual_disk = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    require(actual_disk == expected_disk, f"extraction set mismatch extra={sorted(actual_disk-expected_disk)} missing={sorted(expected_disk-actual_disk)}")

    lock_path = root / LOCK
    lock = load_json(lock_path)
    lock_payload = unsigned_payload(lock)
    lock_sha = sha(lock_path.read_bytes())
    require(frozen_declared.get("release_lock_sha256") == lock_sha, "manifest lock byte hash")
    require(frozen_declared.get("release_lock_payload_sha256") == lock_payload, "manifest lock payload")
    outer = verify_release_rows(root, lock.get("files"))
    require(len(outer) == 230, "release outer count")

    rank = parse_sha_manifest(root, "work/rank_upper_certificates/MANIFEST.sha256", "work/rank_upper_certificates")
    cycle = parse_sha_manifest(root, "work/cycle_three_port_closure/MANIFEST.sha256", "work/cycle_three_port_closure")
    direct_base = PurePosixPath("package/referee/k2p_offline_sweep_portable")
    nested_maps: dict[str, dict[str, str]] = {}
    for name in ("DIRECT_CLOSURE_LOCK.json", "INPUT_LOCK.json"):
        nested = load_json(root / direct_base.as_posix() / name)
        files = nested.get("files")
        require(isinstance(files, dict), f"nested map missing: {name}")
        nested_map: dict[str, str] = {}
        for child, digest in files.items():
            require(isinstance(child, str) and isinstance(digest, str), f"nested malformed: {name}")
            relative = (direct_base / safe(child)).as_posix()
            require(file_row(root, relative)["sha256"] == digest, f"nested hash: {relative}")
            nested_map[relative] = digest
        nested_maps[name] = nested_map

    reconstructed = set(outer) | set(rank) | set(cycle)
    for rows in nested_maps.values():
        reconstructed.update(rows)
    reconstructed.add(LOCK)
    require(reconstructed == set(frozen), f"transitive frozen set mismatch extra={sorted(reconstructed-set(frozen))[:5]} missing={sorted(set(frozen)-reconstructed)[:5]}")

    portable = load_json(root / PORTABLE)
    portable_files = verify_rows(root, portable.get("files"), "portable")
    require(portable_files == frozen, "portable/frozen map mismatch")
    require(portable.get("file_count") == len(frozen), "portable count")
    require(portable.get("total_bytes") == sum(int(row["bytes"]) for row in frozen.values()), "portable bytes")
    require(portable.get("content_ledger_root_sha256") == canonical_hash(frozen), "portable root")
    require(portable.get("release_lock_sha256") == lock_sha, "portable lock byte hash")
    require(portable.get("release_lock_payload_sha256") == lock_payload, "portable lock payload")

    archive_sha = sha(archive_path.read_bytes())
    with zipfile.ZipFile(archive_path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        require(len(names) == len(set(names)), "duplicate ZIP names")
        archive_relatives: list[str] = []
        for info in infos:
            require(not info.is_dir(), f"directory member: {info.filename}")
            member = safe(info.filename)
            require(member.parts[0] == PREFIX, f"wrong ZIP prefix: {info.filename}")
            relative = PurePosixPath(*member.parts[1:]).as_posix()
            safe(relative)
            archive_relatives.append(relative)
            require(info.date_time == (2026, 8, 26, 0, 0, 0), f"ZIP timestamp: {relative}")
            require(info.create_system == 3, f"ZIP creator: {relative}")
            require((info.external_attr >> 16) & 0xFFFF == 0o100644, f"ZIP mode: {relative}")
            require(info.compress_type == zipfile.ZIP_DEFLATED, f"ZIP compression: {relative}")
            data = archive.read(info)
            require(data == root.joinpath(*safe(relative).parts).read_bytes(), f"ZIP bytes: {relative}")
        require(archive_relatives == sorted(expected_disk), "ZIP member order/set")

    overlap_rank_outer = len(set(rank) & set(outer))
    overlap_cycle_outer = len(set(cycle) & set(outer))
    direct_union = set().union(*(set(rows) for rows in nested_maps.values()))
    return {
        "status": "PASS",
        "archive": {
            "sha256": archive_sha,
            "bytes": archive_path.stat().st_size,
            "members": len(expected_disk),
            "uncompressed_bytes": sum(path.stat().st_size for path in root.rglob("*") if path.is_file()),
        },
        "manifest": {
            "sha256": sha((root / MANIFEST).read_bytes()),
            "payload_sha256": manifest_payload,
            "combined_root_sha256": canonical_hash(combined),
            "combined_count_excluding_manifest": len(frozen) + len(sources),
        },
        "frozen": {
            "count": len(frozen),
            "bytes": sum(int(row["bytes"]) for row in frozen.values()),
            "root_sha256": canonical_hash(frozen),
        },
        "submission": {
            "count": len(sources),
            "bytes": sum(int(row["bytes"]) for row in sources.values()),
            "root_sha256": canonical_hash(sources),
        },
        "release": {
            "lock_sha256": lock_sha,
            "lock_payload_sha256": lock_payload,
            "outer_count": len(outer),
            "outer_bytes": sum(int(row["bytes"]) for row in outer.values()),
            "rank_manifest_count": len(rank),
            "rank_overlap_outer": overlap_rank_outer,
            "cycle_manifest_count": len(cycle),
            "cycle_overlap_outer": overlap_cycle_outer,
            "direct_closure_count": len(nested_maps["DIRECT_CLOSURE_LOCK.json"]),
            "direct_input_count": len(nested_maps["INPUT_LOCK.json"]),
            "direct_union_count": len(direct_union),
            "direct_union_overlap_outer": len(direct_union & set(outer)),
        },
        "portable_ledger": {
            "sha256": sha((root / PORTABLE).read_bytes()),
            "count": len(portable_files),
            "bytes": sum(int(row["bytes"]) for row in portable_files.values()),
            "root_sha256": canonical_hash(portable_files),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.root, args.archive), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
