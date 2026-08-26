#!/usr/bin/env python3
"""Independent byte/ledger/archive audit for the 2026-08-25 referee ZIP.

This script imports no submitted module.  It reconstructs the frozen closure
from primitive lock/manifest rows, independently scans the submission policy,
checks every ZIP member, and rebuilds deterministic archives.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


PREFIX = "k2p_principal_d_plus_submission_referee"
MANIFEST_REL = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
LOCK_REL = "work/final_theorem_release/RELEASE_LOCK.json"
PORTABLE_REL = "output/referee/REFEREE_BUNDLE_CONTENTS.json"
OPERATIONAL = {
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json",
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json",
    "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
    "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
    "proof_compression_submission/output/logs/article.log",
    "proof_compression_submission/output/logs/supplement.log",
}


def fail(code: str, detail: object | None = None) -> None:
    raise SystemExit(f"{code}:{detail!r}")


def require(value: bool, code: str, detail: object | None = None) -> None:
    if not value:
        fail(code, detail)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha(raw.encode())


def safe(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    require(
        not path.is_absolute()
        and bool(path.parts)
        and all(part not in {"", ".", ".."} for part in path.parts),
        "UNSAFE_PATH",
        value,
    )
    return path


def disk_path(project: Path, relative: str) -> Path:
    return project.joinpath(*safe(relative).parts)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON_NOT_OBJECT", str(path))
    return value


def verify_payload(value: dict[str, Any], code: str) -> str | None:
    payload = value.get("payload_sha256")
    if payload is None:
        return None
    unsigned = dict(value)
    unsigned.pop("payload_sha256", None)
    require(payload == canonical_hash(unsigned), code)
    return payload


def file_row(path: Path) -> dict[str, int | str]:
    require(path.is_file() and not path.is_symlink(), "NONREGULAR_FILE", str(path))
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha(data)}


def parse_sha_manifest(project: Path, relative: str, base: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for number, line in enumerate(
        disk_path(project, relative).read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "BAD_SHA_MANIFEST_LINE", (relative, number))
        expected, child = match.groups()
        combined = (PurePosixPath(base) / safe(child)).as_posix()
        require(combined not in rows, "DUPLICATE_SHA_PATH", combined)
        require(sha(disk_path(project, combined).read_bytes()) == expected,
                "SHA_MANIFEST_MISMATCH", combined)
        rows[combined] = expected
    return rows


def nested_json_rows(project: Path, relative: str, base: str) -> dict[str, str]:
    value = read_json(disk_path(project, relative))
    verify_payload(value, "NESTED_PAYLOAD_MISMATCH")
    files = value.get("files")
    require(isinstance(files, dict), "NESTED_FILES_MISSING", relative)
    rows: dict[str, str] = {}
    for child, expected in files.items():
        require(isinstance(child, str) and isinstance(expected, str),
                "NESTED_ROW_BAD", child)
        combined = (PurePosixPath(base) / safe(child)).as_posix()
        require(combined not in rows, "NESTED_DUPLICATE_PATH", combined)
        require(sha(disk_path(project, combined).read_bytes()) == expected,
                "NESTED_HASH_MISMATCH", combined)
        rows[combined] = expected
    return rows


def reconstruct_frozen(project: Path) -> tuple[dict[str, dict[str, int | str]], dict[str, Any], dict[str, int]]:
    lock = read_json(disk_path(project, LOCK_REL))
    verify_payload(lock, "LOCK_PAYLOAD_MISMATCH")
    outer = lock.get("files")
    require(isinstance(outer, dict), "OUTER_FILES_MISSING")
    paths = set(outer)

    rank = parse_sha_manifest(
        project,
        "work/rank_upper_certificates/MANIFEST.sha256",
        "work/rank_upper_certificates",
    )
    cycle = parse_sha_manifest(
        project,
        "work/cycle_three_port_closure/MANIFEST.sha256",
        "work/cycle_three_port_closure",
    )
    direct_base = "package/referee/k2p_offline_sweep_portable"
    direct = nested_json_rows(
        project, f"{direct_base}/DIRECT_CLOSURE_LOCK.json", direct_base
    )
    direct_input = nested_json_rows(
        project, f"{direct_base}/INPUT_LOCK.json", direct_base
    )
    paths.update(rank)
    paths.update(cycle)
    paths.update(direct)
    paths.update(direct_input)
    paths.add(LOCK_REL)

    ledger = {
        relative: file_row(disk_path(project, relative))
        for relative in sorted(paths)
    }
    for relative, declared in outer.items():
        require(isinstance(declared, dict), "OUTER_ROW_BAD", relative)
        expected = {"bytes": declared.get("bytes"), "sha256": declared.get("sha256")}
        require(ledger.get(relative) == expected, "OUTER_ROW_MISMATCH", relative)
    counts = {
        "outer_lock_rows": len(outer),
        "rank_manifest_rows": len(rank),
        "cycle_manifest_rows": len(cycle),
        "direct_lock_rows": len(direct),
        "direct_input_lock_rows": len(direct_input),
        "distinct_frozen_paths": len(ledger),
    }
    nested_declared = lock.get("nested_manifests")
    if isinstance(nested_declared, dict):
        require(nested_declared.get("rank_manifest_files") == len(rank),
                "LOCK_NESTED_RANK_COUNT")
        require(nested_declared.get("cycle_manifest_files") == len(cycle),
                "LOCK_NESTED_CYCLE_COUNT")
        require(nested_declared.get("direct_nested_files") == len(direct),
                "LOCK_NESTED_DIRECT_COUNT")
        require(nested_declared.get("direct_input_lock_files") == len(direct_input),
                "LOCK_NESTED_DIRECT_INPUT_COUNT")
    return ledger, lock, counts


def submission_included(relative: PurePosixPath) -> bool:
    if not relative.parts or relative.parts[0] != "proof_compression_submission":
        return False
    value = relative.as_posix()
    if value == MANIFEST_REL:
        return False
    if value in OPERATIONAL:
        return True
    if "output" in relative.parts or "__pycache__" in relative.parts:
        return False
    if any(part.startswith(".") for part in relative.parts[1:-1]):
        return False
    if relative.name == ".DS_Store" or relative.suffix in {".pyc", ".pyo"}:
        return False
    return True


def reconstruct_submission(project: Path, supplemental: list[str]) -> dict[str, dict[str, int | str]]:
    ledger: dict[str, dict[str, int | str]] = {}
    base = project / "proof_compression_submission"
    for path in sorted(base.rglob("*")):
        if path.is_dir():
            continue
        relative = PurePosixPath(path.relative_to(project).as_posix())
        if submission_included(relative):
            ledger[relative.as_posix()] = file_row(path)
    for relative in supplemental:
        require(relative not in ledger, "SUPPLEMENTAL_COLLISION", relative)
        ledger[relative] = file_row(disk_path(project, relative))
    return dict(sorted(ledger.items()))


def parse_timestamp(manifest: dict[str, Any]) -> tuple[int, int, int, int, int, int]:
    policy = manifest.get("archive_policy")
    require(isinstance(policy, dict), "ARCHIVE_POLICY_MISSING")
    stamp = policy.get("fixed_member_timestamp")
    require(isinstance(stamp, str), "ARCHIVE_TIMESTAMP_MISSING")
    value = datetime.fromisoformat(stamp)
    result = (value.year, value.month, value.day, value.hour, value.minute, value.second)
    require(value.second % 2 == 0, "ZIP_TIMESTAMP_NOT_REPRESENTABLE", stamp)
    return result


def rebuild(output: Path, project: Path, paths: list[str], timestamp: tuple[int, ...]) -> dict[str, Any]:
    require(not output.exists() and not output.is_symlink(), "OUTPUT_ALREADY_EXISTS", str(output))
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for relative in paths:
            info = zipfile.ZipInfo(f"{PREFIX}/{relative}", date_time=timestamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            zf.writestr(
                info,
                disk_path(project, relative).read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )
    data = output.read_bytes()
    return {"path": str(output), "bytes": len(data), "sha256": sha(data)}


def audit(project: Path, archive_path: Path, rebuild_paths: list[Path]) -> dict[str, Any]:
    project = project.resolve()
    manifest_path = disk_path(project, MANIFEST_REL)
    manifest_bytes = manifest_path.read_bytes()
    manifest = read_json(manifest_path)
    verify_payload(manifest, "MANIFEST_PAYLOAD_MISMATCH")
    frozen, lock, nested_counts = reconstruct_frozen(project)

    declared_submission = manifest.get("submission_sources")
    declared_frozen = manifest.get("frozen_evidence")
    require(isinstance(declared_submission, dict) and isinstance(declared_frozen, dict),
            "MANIFEST_LEDGER_SECTION_MISSING")
    policy = declared_submission.get("policy")
    require(isinstance(policy, dict), "SUBMISSION_POLICY_MISSING")
    supplemental = policy.get("supplemental_execution_dependencies")
    require(isinstance(supplemental, list)
            and all(isinstance(x, str) for x in supplemental),
            "SUPPLEMENTAL_DEPENDENCIES_BAD")
    submission = reconstruct_submission(project, supplemental)

    require(declared_frozen.get("files") == frozen, "FROZEN_LEDGER_MISMATCH")
    require(declared_submission.get("files") == submission, "SUBMISSION_LEDGER_MISMATCH")
    frozen_bytes = sum(int(row["bytes"]) for row in frozen.values())
    submission_bytes = sum(int(row["bytes"]) for row in submission.values())
    require(declared_frozen.get("file_count") == len(frozen), "FROZEN_COUNT")
    require(declared_frozen.get("total_bytes") == frozen_bytes, "FROZEN_BYTES")
    require(declared_submission.get("file_count") == len(submission), "SUBMISSION_COUNT")
    require(declared_submission.get("total_bytes") == submission_bytes, "SUBMISSION_BYTES")
    require(declared_frozen.get("content_ledger_root_sha256") == canonical_hash(frozen),
            "FROZEN_ROOT")
    require(declared_submission.get("content_ledger_root_sha256") == canonical_hash(submission),
            "SUBMISSION_ROOT")
    combined = {"frozen_evidence": frozen, "submission_sources": submission}
    require(manifest.get("combined_content_root_sha256") == canonical_hash(combined),
            "COMBINED_ROOT")
    require(manifest.get("combined_file_count_excluding_manifest")
            == len(set(frozen).union(submission)), "COMBINED_COUNT")

    portable = read_json(disk_path(project, PORTABLE_REL))
    require(portable.get("files") == frozen, "PORTABLE_LEDGER_MISMATCH")
    require(portable.get("file_count") == len(frozen), "PORTABLE_COUNT")
    require(portable.get("total_bytes") == frozen_bytes, "PORTABLE_BYTES")
    require(portable.get("content_ledger_root_sha256") == canonical_hash(frozen),
            "PORTABLE_ROOT")
    require(portable.get("release_lock_sha256") == sha(disk_path(project, LOCK_REL).read_bytes()),
            "PORTABLE_LOCK_HASH")
    require(portable.get("release_lock_payload_sha256") == lock.get("payload_sha256"),
            "PORTABLE_LOCK_PAYLOAD")

    relative_paths = sorted(set(frozen).union(submission).union({MANIFEST_REL}))
    expected_names = [f"{PREFIX}/{relative}" for relative in relative_paths]
    archive_data = archive_path.read_bytes()
    timestamp = parse_timestamp(manifest)
    with zipfile.ZipFile(archive_path) as zf:
        infos = zf.infolist()
        names = [info.filename for info in infos]
        require(len(names) == len(set(names)), "DUPLICATE_ARCHIVE_MEMBER")
        require(names == expected_names, "ARCHIVE_MEMBER_ORDER_OR_SET")
        require(zf.comment == b"", "ARCHIVE_COMMENT")
        uncompressed = compressed = 0
        for info, relative in zip(infos, relative_paths, strict=True):
            require(info.date_time == timestamp, "ARCHIVE_TIMESTAMP", relative)
            require(info.compress_type == zipfile.ZIP_DEFLATED,
                    "ARCHIVE_COMPRESSION", relative)
            require(info.create_system == 3, "ARCHIVE_CREATE_SYSTEM", relative)
            require((info.external_attr >> 16) == 0o100644, "ARCHIVE_MODE", relative)
            require(not (info.flag_bits & 1), "ARCHIVE_ENCRYPTED", relative)
            payload = zf.read(info)
            require(payload == disk_path(project, relative).read_bytes(),
                    "ARCHIVE_DISK_MISMATCH", relative)
            uncompressed += info.file_size
            compressed += info.compress_size

    tree_files = {
        path.relative_to(project).as_posix()
        for path in project.rglob("*") if path.is_file()
    }
    require(tree_files == set(relative_paths), "TREE_FILE_SET_MISMATCH", {
        "missing": sorted(set(relative_paths) - tree_files),
        "extra": sorted(tree_files - set(relative_paths)),
    })

    rebuilt = [rebuild(path, project, relative_paths, timestamp) for path in rebuild_paths]
    archive_sha = sha(archive_data)
    for row in rebuilt:
        row["byte_identical_to_distributed"] = (
            row["bytes"] == len(archive_data) and row["sha256"] == archive_sha
        )
        require(bool(row["byte_identical_to_distributed"]), "REBUILD_DIFFERS", row)

    return {
        "status": "PASS",
        "archive": {
            "path": str(archive_path),
            "bytes": len(archive_data),
            "sha256": archive_sha,
            "file_count": len(relative_paths),
            "uncompressed_member_bytes": uncompressed,
            "compressed_member_bytes": compressed,
            "fixed_timestamp": list(timestamp),
            "rebuilds": rebuilt,
        },
        "manifest": {
            "path": MANIFEST_REL,
            "bytes": len(manifest_bytes),
            "file_sha256": sha(manifest_bytes),
            "payload_sha256": manifest.get("payload_sha256"),
            "combined_content_root_sha256": canonical_hash(combined),
        },
        "release_lock": {
            "path": LOCK_REL,
            "file_sha256": sha(disk_path(project, LOCK_REL).read_bytes()),
            "payload_sha256": lock.get("payload_sha256"),
        },
        "frozen": {
            "file_count": len(frozen),
            "total_bytes": frozen_bytes,
            "content_root_sha256": canonical_hash(frozen),
            "nested_counts": nested_counts,
        },
        "submission": {
            "file_count": len(submission),
            "total_bytes": submission_bytes,
            "content_root_sha256": canonical_hash(submission),
            "supplemental_execution_dependencies": supplemental,
        },
        "archive_policy_checked": {
            "member_set_and_lexicographic_order": True,
            "prefix": PREFIX,
            "fixed_timestamp": True,
            "mode_100644": True,
            "deflate": True,
            "no_duplicate_or_encrypted_members": True,
            "no_extra_or_missing_extracted_files": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--rebuild", action="append", default=[], type=Path)
    args = parser.parse_args()
    result = audit(args.project, args.archive, args.rebuild)
    result["payload_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
