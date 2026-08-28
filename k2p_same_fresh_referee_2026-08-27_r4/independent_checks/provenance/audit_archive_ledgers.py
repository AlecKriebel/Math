#!/usr/bin/env python3
"""Independent, standard-library audit of the distributed ZIP and its ledgers.

This reviewer-owned checker deliberately does not import submission code.
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_bytes(data: bytes, label: str) -> dict[str, Any]:
    value = json.loads(data, object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        raise ValueError(f"{label}: top level is not an object")
    return value


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return sha256_bytes(encoded)


def validate_relative(relative: str) -> None:
    pure = PurePosixPath(relative)
    if (
        not relative
        or relative.startswith("/")
        or "\\" in relative
        or pure.as_posix() != relative
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        raise ValueError(f"unsafe relative path: {relative!r}")


def parse_sha_manifest(data: bytes, base: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for ordinal, line in enumerate(data.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            raise ValueError(f"manifest line {ordinal} invalid")
        digest, child = match.groups()
        if child.startswith("./"):
            child = child[2:]
        validate_relative(child)
        relative = (PurePosixPath(base) / child).as_posix()
        if relative in result:
            raise ValueError(f"duplicate manifest path: {relative}")
        result[relative] = digest
    return result


def audit(args: argparse.Namespace) -> dict[str, Any]:
    archive = args.archive.resolve()
    project = args.project.resolve()
    result: dict[str, Any] = {
        "archive": {
            "path": str(archive),
            "bytes": archive.stat().st_size,
            "sha256": sha256_file(archive),
        }
    }

    zip_rows: dict[str, dict[str, Any]] = {}
    prefix: str | None = None
    directory_count = 0
    encrypted_count = 0
    symlink_count = 0
    special_count = 0
    unsafe_paths: list[str] = []
    raw_names: list[str] = []
    with zipfile.ZipFile(archive) as handle:
        infos = handle.infolist()
        bad_crc = handle.testzip()
        for info in infos:
            raw_names.append(info.filename)
            pure = PurePosixPath(info.filename)
            try:
                validate_relative(info.filename.rstrip("/"))
            except ValueError:
                unsafe_paths.append(info.filename)
            if not pure.parts:
                unsafe_paths.append(info.filename)
                continue
            if prefix is None:
                prefix = pure.parts[0]
            elif pure.parts[0] != prefix:
                unsafe_paths.append(info.filename)
            mode = (info.external_attr >> 16) & 0o177777
            kind = stat.S_IFMT(mode)
            if info.flag_bits & 1:
                encrypted_count += 1
            if info.is_dir():
                directory_count += 1
                continue
            if kind == stat.S_IFLNK:
                symlink_count += 1
            elif kind not in {0, stat.S_IFREG}:
                special_count += 1
            if len(pure.parts) < 2:
                unsafe_paths.append(info.filename)
                continue
            relative = PurePosixPath(*pure.parts[1:]).as_posix()
            validate_relative(relative)
            data = handle.read(info)
            zip_rows[relative] = {
                "bytes": len(data),
                "sha256": sha256_bytes(data),
                "compress_bytes": info.compress_size,
                "compress_type": info.compress_type,
                "date_time": list(info.date_time),
                "mode": oct(mode),
            }
            extracted = project.joinpath(*PurePosixPath(relative).parts)
            if not extracted.is_file() or extracted.is_symlink():
                raise ValueError(f"missing/nonregular extracted member: {relative}")
            if extracted.stat().st_size != len(data) or sha256_file(extracted) != sha256_bytes(data):
                raise ValueError(f"extracted member mismatch: {relative}")

    duplicate_names = sorted(name for name, count in Counter(raw_names).items() if count > 1)
    casefold_collisions = sorted(
        names
        for names in (
            sorted(name for name in raw_names if name.casefold() == key)
            for key, count in Counter(name.casefold() for name in raw_names).items()
            if count > 1
        )
    )
    result["archive"].update(
        {
            "prefix": prefix,
            "entry_count": len(raw_names),
            "file_count": len(zip_rows),
            "directory_count": directory_count,
            "uncompressed_file_bytes": sum(row["bytes"] for row in zip_rows.values()),
            "testzip_bad_member": bad_crc,
            "unsafe_paths": unsafe_paths,
            "duplicate_names": duplicate_names,
            "casefold_collisions": casefold_collisions,
            "encrypted_members": encrypted_count,
            "symlink_members": symlink_count,
            "special_members": special_count,
            "all_fixed_timestamp": all(row["date_time"] == [2026, 8, 27, 0, 0, 0] for row in zip_rows.values()),
            "all_deflated": all(row["compress_type"] == zipfile.ZIP_DEFLATED for row in zip_rows.values()),
            "all_mode_100644": all(row["mode"] == "0o100644" for row in zip_rows.values()),
            "lexicographic_file_order": [name for name in raw_names if not name.endswith("/")]
            == sorted(name for name in raw_names if not name.endswith("/")),
        }
    )

    manifest_relative = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
    manifest_bytes = project.joinpath(*PurePosixPath(manifest_relative).parts).read_bytes()
    manifest = load_json_bytes(manifest_bytes, manifest_relative)
    payload = manifest.get("payload_sha256")
    unsigned = dict(manifest)
    unsigned.pop("payload_sha256", None)
    if payload != canonical_hash(unsigned):
        raise ValueError("revised manifest payload hash mismatch")
    declared_combined: dict[str, dict[str, Any]] = {}
    for section in ("frozen_evidence", "submission_sources"):
        part = manifest[section]
        files = part["files"]
        if part["file_count"] != len(files):
            raise ValueError(f"{section}: file-count mismatch")
        if part["total_bytes"] != sum(row["bytes"] for row in files.values()):
            raise ValueError(f"{section}: byte-count mismatch")
        if part["content_ledger_root_sha256"] != canonical_hash(files):
            raise ValueError(f"{section}: content-root mismatch")
        for relative, row in files.items():
            validate_relative(relative)
            if relative in declared_combined:
                raise ValueError(f"overlapping manifest path: {relative}")
            declared_combined[relative] = row
    expected_zip_rows = {
        **declared_combined,
        manifest_relative: {
            "bytes": len(manifest_bytes),
            "sha256": sha256_bytes(manifest_bytes),
        },
    }
    actual_compact = {
        relative: {"bytes": row["bytes"], "sha256": row["sha256"]}
        for relative, row in zip_rows.items()
    }
    result["revised_manifest"] = {
        "payload_sha256": payload,
        "combined_content_root_sha256": manifest["combined_content_root_sha256"],
        "combined_content_root_recomputed": canonical_hash(
            {
                "frozen_evidence": manifest["frozen_evidence"]["files"],
                "submission_sources": manifest["submission_sources"]["files"],
            }
        ),
        "declared_file_count_excluding_manifest": manifest["combined_file_count_excluding_manifest"],
        "actual_file_count_excluding_manifest": len(declared_combined),
        "archive_exactly_matches_manifest": actual_compact == expected_zip_rows,
        "archive_missing_paths": sorted(set(expected_zip_rows) - set(actual_compact)),
        "archive_extra_paths": sorted(set(actual_compact) - set(expected_zip_rows)),
        "archive_metadata_mismatches": sorted(
            relative
            for relative in set(expected_zip_rows) & set(actual_compact)
            if expected_zip_rows[relative] != actual_compact[relative]
        ),
    }

    lock_relative = "work/final_theorem_release/RELEASE_LOCK.json"
    lock_bytes = project.joinpath(*PurePosixPath(lock_relative).parts).read_bytes()
    lock = load_json_bytes(lock_bytes, lock_relative)
    lock_payload = lock["payload_sha256"]
    lock_unsigned = dict(lock)
    lock_unsigned.pop("payload_sha256", None)
    if canonical_hash(lock_unsigned) != lock_payload:
        raise ValueError("release lock payload mismatch")
    closure: dict[str, str] = {
        relative: row["sha256"] for relative, row in lock["files"].items()
    }
    sha_manifest_counts: dict[str, int] = {}
    for relative, base in (
        ("work/rank_upper_certificates/MANIFEST.sha256", "work/rank_upper_certificates"),
        ("work/cycle_three_port_closure/MANIFEST.sha256", "work/cycle_three_port_closure"),
    ):
        rows = parse_sha_manifest(
            project.joinpath(*PurePosixPath(relative).parts).read_bytes(), base
        )
        sha_manifest_counts[relative] = len(rows)
        for child, digest in rows.items():
            prior = closure.get(child)
            if prior is not None and prior != digest:
                raise ValueError(f"conflicting closure digest: {child}")
            closure[child] = digest
    direct_base = PurePosixPath("package/referee/k2p_offline_sweep_portable")
    direct_lock_counts: dict[str, int] = {}
    for name in ("DIRECT_CLOSURE_LOCK.json", "INPUT_LOCK.json"):
        nested = load_json_bytes(
            project.joinpath(*(direct_base / name).parts).read_bytes(), name
        )
        direct_lock_counts[name] = len(nested["files"])
        for child, digest in nested["files"].items():
            validate_relative(child)
            relative = (direct_base / child).as_posix()
            prior = closure.get(relative)
            if prior is not None and prior != digest:
                raise ValueError(f"conflicting closure digest: {relative}")
            closure[relative] = digest
    closure[lock_relative] = sha256_bytes(lock_bytes)
    closure_rows: dict[str, dict[str, Any]] = {}
    for relative, digest in sorted(closure.items()):
        path = project.joinpath(*PurePosixPath(relative).parts)
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"missing/nonregular closure file: {relative}")
        actual = sha256_file(path)
        if actual != digest:
            raise ValueError(f"closure digest mismatch: {relative}")
        closure_rows[relative] = {"bytes": path.stat().st_size, "sha256": actual}
        if path.suffix == ".json":
            load_json_bytes(path.read_bytes(), relative)
    declared_frozen = manifest["frozen_evidence"]["files"]
    result["release_closure"] = {
        "release_lock_bytes": len(lock_bytes),
        "release_lock_sha256": sha256_bytes(lock_bytes),
        "release_lock_payload_sha256": lock_payload,
        "outer_lock_file_count": len(lock["files"]),
        "nested_sha_manifest_counts": sha_manifest_counts,
        "nested_direct_lock_counts": direct_lock_counts,
        "closure_file_count": len(closure_rows),
        "closure_total_bytes": sum(row["bytes"] for row in closure_rows.values()),
        "closure_content_root_sha256": canonical_hash(closure_rows),
        "manifest_frozen_exact_match": closure_rows == declared_frozen,
        "promotion_ready": lock.get("promotion_ready"),
        "blockers": lock.get("blockers"),
        "missing_required_files": lock.get("missing_required_files"),
    }

    portable_relative = "output/referee/REFEREE_BUNDLE_CONTENTS.json"
    portable = load_json_bytes(
        project.joinpath(*PurePosixPath(portable_relative).parts).read_bytes(),
        portable_relative,
    )
    portable_files = portable["files"]
    result["portable_content_ledger"] = {
        "file_count": portable.get("file_count"),
        "total_bytes": portable.get("total_bytes"),
        "content_ledger_root_sha256": portable.get("content_ledger_root_sha256"),
        "recomputed_file_count": len(portable_files),
        "recomputed_total_bytes": sum(row["bytes"] for row in portable_files.values()),
        "recomputed_content_ledger_root_sha256": canonical_hash(portable_files),
        "exact_match_to_release_closure": portable_files == closure_rows,
    }

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
