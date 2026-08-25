#!/usr/bin/env python3
"""Independent byte-level audit and deterministic rebuild of the referee ZIP.

This implementation deliberately does not import any submitted builder or
checker module.  It reconstructs both declared path closures from primitive
JSON/manifests and checks every archive member against the isolated tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


PREFIX = "k2p_principal_d_plus_submission_referee"
MANIFEST_REL = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
LOCK_REL = "work/final_theorem_release/RELEASE_LOCK.json"
OPERATIONAL = {
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json",
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json",
    "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
    "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
    "proof_compression_submission/output/logs/article.log",
    "proof_compression_submission/output/logs/supplement.log",
}
SUPPLEMENTAL = {
    "output/referee/README.md",
    "output/referee/REFEREE_BUNDLE_CONTENTS.json",
    "output/referee/build_referee_bundle.py",
}


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise SystemExit(f"{code}: {detail!r}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return digest(encoded)


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


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON_NOT_OBJECT", path)
    return value


def file_row(path: Path) -> dict[str, int | str]:
    require(path.is_file() and not path.is_symlink(), "NONREGULAR_FILE", path)
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": digest(data)}


def parse_sha_manifest(
    project: Path, relative: str, base: str
) -> dict[str, str]:
    rows: dict[str, str] = {}
    manifest = project.joinpath(*safe(relative).parts)
    for line_number, line in enumerate(
        manifest.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "BAD_SHA_MANIFEST_LINE", (relative, line_number))
        expected, child = match.groups()
        combined = (PurePosixPath(base) / safe(child)).as_posix()
        require(combined not in rows, "DUPLICATE_SHA_MANIFEST_PATH", combined)
        actual = digest(project.joinpath(*safe(combined).parts).read_bytes())
        require(actual == expected, "SHA_MANIFEST_HASH_MISMATCH", combined)
        rows[combined] = expected
    return rows


def reconstruct_frozen(project: Path) -> tuple[dict[str, dict[str, int | str]], dict[str, Any]]:
    lock_path = project / LOCK_REL
    lock = read_json(lock_path)
    payload = lock.get("payload_sha256")
    unsigned = dict(lock)
    unsigned.pop("payload_sha256", None)
    require(payload == canonical_hash(unsigned), "LOCK_PAYLOAD_MISMATCH")
    outer = lock.get("files")
    require(isinstance(outer, dict) and len(outer) == 223, "OUTER_LOCK_CENSUS")
    paths = set(outer)
    paths.update(
        parse_sha_manifest(
            project,
            "work/rank_upper_certificates/MANIFEST.sha256",
            "work/rank_upper_certificates",
        )
    )
    paths.update(
        parse_sha_manifest(
            project,
            "work/cycle_three_port_closure/MANIFEST.sha256",
            "work/cycle_three_port_closure",
        )
    )
    direct_root = PurePosixPath("package/referee/k2p_offline_sweep_portable")
    for lock_name in ("DIRECT_CLOSURE_LOCK.json", "INPUT_LOCK.json"):
        nested_rel = (direct_root / lock_name).as_posix()
        nested = read_json(project.joinpath(*safe(nested_rel).parts))
        files = nested.get("files")
        require(isinstance(files, dict), "NESTED_FILES_MISSING", lock_name)
        for child, expected in files.items():
            require(isinstance(child, str) and isinstance(expected, str), "NESTED_ROW_BAD")
            relative = (direct_root / safe(child)).as_posix()
            actual = digest(project.joinpath(*safe(relative).parts).read_bytes())
            require(actual == expected, "NESTED_HASH_MISMATCH", relative)
            paths.add(relative)
    paths.add(LOCK_REL)
    ledger = {relative: file_row(project.joinpath(*safe(relative).parts)) for relative in sorted(paths)}
    for relative, declared in outer.items():
        require(isinstance(declared, dict), "OUTER_FILE_BINDING_BAD", relative)
        require(
            ledger.get(relative)
            == {"bytes": declared.get("bytes"), "sha256": declared.get("sha256")},
            "OUTER_FILE_BINDING_MISMATCH",
            relative,
        )
    return ledger, lock


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


def reconstruct_submission(project: Path) -> dict[str, dict[str, int | str]]:
    base = project / "proof_compression_submission"
    ledger: dict[str, dict[str, int | str]] = {}
    for path in sorted(base.rglob("*")):
        if path.is_dir():
            continue
        relative = PurePosixPath(path.relative_to(project).as_posix())
        if submission_included(relative):
            ledger[relative.as_posix()] = file_row(path)
    for relative in sorted(SUPPLEMENTAL):
        ledger[relative] = file_row(project.joinpath(*safe(relative).parts))
    return dict(sorted(ledger.items()))


def write_deterministic_zip(
    output: Path, project: Path, relative_paths: list[str]
) -> str:
    require(not output.is_symlink(), "SYMBOLIC_OUTPUT", output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for relative in relative_paths:
            data = project.joinpath(*safe(relative).parts).read_bytes()
            info = zipfile.ZipInfo(
                f"{PREFIX}/{relative}", date_time=(2026, 8, 24, 0, 0, 0)
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(
                info,
                data,
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )
    return digest(output.read_bytes())


def audit(project: Path, archive_path: Path, checksum_path: Path) -> tuple[dict[str, Any], list[str]]:
    project = project.resolve()
    manifest_path = project / MANIFEST_REL
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    require(isinstance(manifest, dict), "MANIFEST_NOT_OBJECT")
    manifest_payload = manifest.get("payload_sha256")
    unsigned = dict(manifest)
    unsigned.pop("payload_sha256", None)
    require(manifest_payload == canonical_hash(unsigned), "MANIFEST_PAYLOAD_MISMATCH")

    frozen, lock = reconstruct_frozen(project)
    submission = reconstruct_submission(project)
    declared_frozen = manifest.get("frozen_evidence", {})
    declared_submission = manifest.get("submission_sources", {})
    require(declared_frozen.get("files") == frozen, "FROZEN_LEDGER_MISMATCH")
    require(declared_submission.get("files") == submission, "SUBMISSION_LEDGER_MISMATCH")
    require(len(frozen) == 399, "FROZEN_COUNT", len(frozen))
    require(len(submission) == 80, "SUBMISSION_COUNT", len(submission))
    frozen_bytes = sum(int(row["bytes"]) for row in frozen.values())
    submission_bytes = sum(int(row["bytes"]) for row in submission.values())
    require(frozen_bytes == 478_755_815, "FROZEN_BYTES", frozen_bytes)
    require(submission_bytes == 4_065_606, "SUBMISSION_BYTES", submission_bytes)
    require(canonical_hash(frozen) == declared_frozen.get("content_ledger_root_sha256"), "FROZEN_ROOT")
    require(canonical_hash(submission) == declared_submission.get("content_ledger_root_sha256"), "SUBMISSION_ROOT")
    combined = {"frozen_evidence": frozen, "submission_sources": submission}
    require(canonical_hash(combined) == manifest.get("combined_content_root_sha256"), "COMBINED_ROOT")

    portable = read_json(project / "output/referee/REFEREE_BUNDLE_CONTENTS.json")
    require(portable.get("files") == frozen, "PORTABLE_LEDGER_DIFFERS_FROM_FROZEN")
    for key in ("file_count", "total_bytes", "content_ledger_root_sha256"):
        require(portable.get(key) == declared_frozen.get(key), "PORTABLE_SUMMARY_MISMATCH", key)

    archive_sha = digest(archive_path.read_bytes())
    checksum_text = checksum_path.read_text(encoding="utf-8")
    checksum_match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)\n?", checksum_text)
    require(checksum_match is not None, "MALFORMED_ADJACENT_CHECKSUM")
    require(checksum_match.group(1) == archive_sha, "ADJACENT_CHECKSUM_MISMATCH")
    require(checksum_match.group(2) == archive_path.name, "ADJACENT_CHECKSUM_FILENAME_MISMATCH")

    relative_paths = sorted(set(frozen).union(submission).union({MANIFEST_REL}))
    expected_names = [f"{PREFIX}/{relative}" for relative in relative_paths]
    with zipfile.ZipFile(archive_path, "r") as archive:
        infos = archive.infolist()
        names = [row.filename for row in infos]
        require(len(names) == len(set(names)), "DUPLICATE_ARCHIVE_MEMBER")
        require(names == expected_names, "ARCHIVE_MEMBER_SET_OR_ORDER")
        require(archive.comment == b"", "ARCHIVE_COMMENT_PRESENT")
        uncompressed_total = 0
        compressed_total = 0
        for info, relative in zip(infos, relative_paths, strict=True):
            require(info.date_time == (2026, 8, 24, 0, 0, 0), "ARCHIVE_TIMESTAMP", relative)
            require(info.compress_type == zipfile.ZIP_DEFLATED, "ARCHIVE_COMPRESSION", relative)
            require(info.create_system == 3, "ARCHIVE_CREATE_SYSTEM", relative)
            require((info.external_attr >> 16) == 0o100644, "ARCHIVE_MODE", relative)
            require(not (info.flag_bits & 0x1), "ARCHIVE_MEMBER_ENCRYPTED", relative)
            data = archive.read(info)
            disk = project.joinpath(*safe(relative).parts).read_bytes()
            require(data == disk, "ARCHIVE_DISK_BYTE_MISMATCH", relative)
            if relative == MANIFEST_REL:
                require(data == manifest_bytes, "ARCHIVE_MANIFEST_BYTE_MISMATCH")
            else:
                row = frozen.get(relative, submission.get(relative))
                require(row is not None, "UNBOUND_ARCHIVE_MEMBER", relative)
                require(len(data) == row["bytes"] and digest(data) == row["sha256"], "ARCHIVE_LEDGER_MISMATCH", relative)
            uncompressed_total += info.file_size
            compressed_total += info.compress_size
    require(uncompressed_total == frozen_bytes + submission_bytes + len(manifest_bytes), "ARCHIVE_UNCOMPRESSED_TOTAL")

    tree_files = {
        path.relative_to(project).as_posix()
        for path in project.rglob("*")
        if path.is_file()
    }
    require(tree_files == set(relative_paths), "EXTRACTED_TREE_FILE_SET_MISMATCH", {
        "missing": sorted(set(relative_paths) - tree_files),
        "extra": sorted(tree_files - set(relative_paths)),
    })
    result = {
        "status": "PASS",
        "archive_sha256": archive_sha,
        "archive_bytes": archive_path.stat().st_size,
        "archive_file_count": len(expected_names),
        "archive_uncompressed_bytes": uncompressed_total,
        "archive_compressed_member_bytes": compressed_total,
        "manifest_file_sha256": digest(manifest_bytes),
        "manifest_payload_sha256": manifest_payload,
        "manifest_bytes": len(manifest_bytes),
        "release_lock_file_sha256": digest((project / LOCK_REL).read_bytes()),
        "release_lock_payload_sha256": lock.get("payload_sha256"),
        "frozen_file_count": len(frozen),
        "frozen_total_bytes": frozen_bytes,
        "frozen_content_root_sha256": canonical_hash(frozen),
        "submission_file_count": len(submission),
        "submission_total_bytes": submission_bytes,
        "submission_content_root_sha256": canonical_hash(submission),
        "combined_content_root_sha256": canonical_hash(combined),
        "archive_policy_checked": {
            "fixed_timestamp": True,
            "member_mode_100644": True,
            "lexicographic_order": True,
            "prefix": PREFIX,
            "compression_deflated": True,
            "no_duplicates": True,
            "no_encryption": True,
            "no_extra_tree_files": True,
        },
    }
    return result, relative_paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--checksum", required=True, type=Path)
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--rebuild", action="append", default=[], type=Path)
    args = parser.parse_args()
    result, relative_paths = audit(args.project, args.archive, args.checksum)
    rebuilt: list[dict[str, Any]] = []
    for output in args.rebuild:
        rebuilt_sha = write_deterministic_zip(output, args.project.resolve(), relative_paths)
        rebuilt.append(
            {
                "path": str(output),
                "bytes": output.stat().st_size,
                "sha256": rebuilt_sha,
                "byte_identical_to_distributed": rebuilt_sha == result["archive_sha256"]
                and output.stat().st_size == result["archive_bytes"],
            }
        )
    result["rebuilt_archives"] = rebuilt
    require(all(row["byte_identical_to_distributed"] for row in rebuilt), "REBUILD_NOT_IDENTICAL")
    args.result.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.result.write_text(encoded, encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
