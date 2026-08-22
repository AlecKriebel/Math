#!/usr/bin/env python3
"""Build/check a deterministic manifest and, only on request, a referee ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


PROJECT = Path(__file__).resolve().parents[2]
LOCK_RELATIVE = "work/final_theorem_release/RELEASE_LOCK.json"
MANIFEST_RELATIVE = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
MANIFEST_PATH = PROJECT / MANIFEST_RELATIVE
LOCK_SHA256 = "58e32bd29f7a039e3da4e47398e32ee8277ad46cf62271a7ed80bf41688b18fb"
LOCK_PAYLOAD_SHA256 = "3b7de4c60315a5820a2623de860f493d6b76a645b5c674ffda89f12fc31a5c90"
FROZEN_FILE_COUNT = 374
FROZEN_TOTAL_BYTES = 434_698_345
FROZEN_CONTENT_ROOT = "7004e3e26bf359d0a11c07fd51cb1636859b30b07a97ca6c9cfd0dcd082dfc92"
ARCHIVE_PREFIX = "k2p_principal_d_plus_submission_referee"
ARCHIVE_TIMESTAMP = (2026, 8, 22, 0, 0, 0)
OPERATIONAL_EVIDENCE = {
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json",
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json",
    "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
    "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
    "proof_compression_submission/output/logs/article.log",
    "proof_compression_submission/output/logs/supplement.log",
}
PENDING_METADATA = [
    "corresponding email address",
    "author-contribution statement",
    "funding declaration",
    "competing-interests declaration",
    "article license",
    "code license",
    "data license",
    "immutable submission tag",
    "whether and when to mint a GitHub/Zenodo DOI release",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def reject_optimized_mode() -> None:
    if not __debug__:
        fail("optimized Python is forbidden")


def safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        fail(f"unsafe relative path: {value!r}")
    return path


def project_path(relative: str) -> Path:
    return PROJECT.joinpath(*safe_relative(relative).parts)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def canonical_hash(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def read_json(relative: str) -> dict[str, Any]:
    value = json.loads(project_path(relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"expected JSON object: {relative}")
    return value


def clean_full_replay_boundary() -> dict[str, Any]:
    report_relative = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json"
    telemetry_relative = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"
    report_path = project_path(report_relative)
    telemetry_path = project_path(telemetry_relative)
    report = read_json(report_relative)
    telemetry = read_json(telemetry_relative)
    report_sha = sha256_bytes(report_path.read_bytes())
    telemetry_sha = sha256_bytes(telemetry_path.read_bytes())
    if report.get("schema") != "k2p-principal-d-plus-final-theorem-replay-report-v1":
        fail("clean full replay report schema mismatch")
    if report.get("status") != "PASS" or report.get("promotion_ready") is not True or report.get("blockers"):
        fail("clean full replay report is not promotion-ready PASS")
    if report.get("mode") != "full" or len(report.get("layer_replays", [])) != 35:
        fail("clean full replay mode/layer census mismatch")
    if report.get("lock_payload_sha256") != LOCK_PAYLOAD_SHA256:
        fail("clean full replay lock payload mismatch")
    if telemetry.get("schema") != "k2p-final-clean-full-replay-telemetry-v1" or telemetry.get("status") != "PASS":
        fail("clean full replay telemetry schema/status mismatch")
    if telemetry.get("report", {}).get("sha256") != report_sha:
        fail("clean full replay telemetry report hash mismatch")
    timing = telemetry.get("time_l", {})
    expected_timing = {
        "real_seconds": 5172.89,
        "maximum_resident_set_size_bytes": 1960001536,
        "peak_memory_footprint_bytes": 491504408,
    }
    if any(timing.get(key) != value for key, value in expected_timing.items()):
        fail("clean full replay timing/memory drift")
    return {
        "status": "clean_detached_full_replay_pass",
        "git_commit": telemetry.get("git_commit"),
        "clean_detached_checkout": telemetry.get("clean_detached_checkout"),
        "end_to_end_full_runtime_seconds": timing["real_seconds"],
        "internal_elapsed_seconds": report.get("elapsed_seconds"),
        "layer_count": len(report["layer_replays"]),
        "maximum_resident_set_size_bytes": timing["maximum_resident_set_size_bytes"],
        "peak_memory_footprint_bytes": timing["peak_memory_footprint_bytes"],
        "end_to_end_quick_runtime_seconds": None,
        "report_path": report_relative,
        "report_sha256": report_sha,
        "telemetry_path": telemetry_relative,
        "telemetry_sha256": telemetry_sha,
    }


def add_manifest_paths(paths: set[str], manifest_relative: str, base_relative: str) -> None:
    manifest = project_path(manifest_relative)
    base = PurePosixPath(base_relative)
    for ordinal, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            fail(f"invalid nested manifest line {manifest_relative}:{ordinal}")
        digest, child = match.groups()
        relative = (base / safe_relative(child)).as_posix()
        data = project_path(relative).read_bytes()
        if sha256_bytes(data) != digest:
            fail(f"nested manifest hash mismatch: {relative}")
        paths.add(relative)


def collect_frozen_ledger() -> dict[str, dict[str, int | str]]:
    lock_path = project_path(LOCK_RELATIVE)
    lock_bytes = lock_path.read_bytes()
    if sha256_bytes(lock_bytes) != LOCK_SHA256:
        fail("frozen RELEASE_LOCK byte hash mismatch")
    lock = json.loads(lock_bytes)
    if not isinstance(lock, dict):
        fail("frozen RELEASE_LOCK is not an object")
    if lock.get("schema") != "k2p-principal-d-plus-final-theorem-release-lock-v1":
        fail("frozen RELEASE_LOCK schema mismatch")
    if lock.get("payload_sha256") != LOCK_PAYLOAD_SHA256:
        fail("frozen RELEASE_LOCK payload mismatch")
    if lock.get("promotion_ready") is not True or lock.get("blockers") or lock.get("missing_required_files"):
        fail("frozen theorem release is not promotion-ready")
    outer_files = lock.get("files")
    if not isinstance(outer_files, dict) or len(outer_files) != 198:
        fail("unexpected frozen outer file map")
    paths = set(outer_files)
    add_manifest_paths(paths, "work/rank_upper_certificates/MANIFEST.sha256", "work/rank_upper_certificates")
    add_manifest_paths(paths, "work/cycle_three_port_closure/MANIFEST.sha256", "work/cycle_three_port_closure")
    direct_root = PurePosixPath("package/referee/k2p_offline_sweep_portable")
    for nested_name in ("DIRECT_CLOSURE_LOCK.json", "INPUT_LOCK.json"):
        nested = read_json((direct_root / nested_name).as_posix())
        nested_files = nested.get("files")
        if not isinstance(nested_files, dict):
            fail(f"missing nested direct file map: {nested_name}")
        for child, digest in nested_files.items():
            if not isinstance(child, str) or not isinstance(digest, str):
                fail(f"malformed nested direct file binding: {nested_name}")
            relative = (direct_root / safe_relative(child)).as_posix()
            data = project_path(relative).read_bytes()
            if sha256_bytes(data) != digest:
                fail(f"nested direct lock mismatch: {relative}")
            paths.add(relative)
    paths.add(LOCK_RELATIVE)
    ledger: dict[str, dict[str, int | str]] = {}
    for relative in sorted(paths):
        path = project_path(relative)
        if not path.is_file() or path.is_symlink():
            fail(f"missing or symbolic frozen evidence file: {relative}")
        data = path.read_bytes()
        metadata: dict[str, int | str] = {"bytes": len(data), "sha256": sha256_bytes(data)}
        outer = outer_files.get(relative)
        if isinstance(outer, dict):
            if metadata["bytes"] != outer.get("bytes") or metadata["sha256"] != outer.get("sha256"):
                fail(f"outer frozen lock mismatch: {relative}")
        ledger[relative] = metadata
    if len(ledger) != FROZEN_FILE_COUNT:
        fail(f"frozen file count mismatch: {len(ledger)}")
    if sum(int(row["bytes"]) for row in ledger.values()) != FROZEN_TOTAL_BYTES:
        fail("frozen total byte count mismatch")
    if canonical_hash(ledger) != FROZEN_CONTENT_ROOT:
        fail("frozen content root mismatch")
    return ledger


def include_submission_source(relative: PurePosixPath) -> bool:
    if not relative.parts or relative.parts[0] != "proof_compression_submission":
        return False
    if relative.as_posix() == MANIFEST_RELATIVE:
        return False
    if relative.as_posix() in OPERATIONAL_EVIDENCE:
        return True
    if (
        "output" in relative.parts
        or "__pycache__" in relative.parts
        or any(part.startswith(".") for part in relative.parts[1:-1])
    ):
        return False
    if relative.name in {".DS_Store"} or relative.suffix in {".pyc", ".pyo"}:
        return False
    return True


def collect_submission_ledger() -> dict[str, dict[str, int | str]]:
    base = PROJECT / "proof_compression_submission"
    if not base.is_dir() or base.is_symlink():
        fail("missing or symbolic proof_compression_submission directory")
    ledger: dict[str, dict[str, int | str]] = {}
    for path in sorted(base.rglob("*")):
        if path.is_dir():
            continue
        relative = PurePosixPath(path.relative_to(PROJECT).as_posix())
        if not include_submission_source(relative):
            continue
        if not path.is_file() or path.is_symlink():
            fail(f"non-regular submission source: {relative.as_posix()}")
        data = path.read_bytes()
        ledger[relative.as_posix()] = {"bytes": len(data), "sha256": sha256_bytes(data)}
    required = {
        "proof_compression_submission/article/main.tex",
        "proof_compression_submission/article/references.bib",
        "proof_compression_submission/supplement/supplement.tex",
        "proof_compression_submission/supplement/compression_tables.tex",
        "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json",
        "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.md",
        "proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py",
        "proof_compression_submission/crosswalk/build_revised_referee_bundle.py",
        "proof_compression_submission/crosswalk/check_revised_referee_bundle.py",
        "proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py",
        "proof_compression_submission/analysis/WEAK_SHARPNESS_COLUMN_CROSSWALK.json",
        "proof_compression_submission/analysis/build_weak_sharpness_column_crosswalk.py",
        "proof_compression_submission/analysis/verify_weak_sharpness_column_crosswalk.py",
        "proof_compression_submission/analysis/test_weak_sharpness_column_crosswalk_mutations.py",
        "proof_compression_submission/templates/PRINTED_CERTIFICATE_APPENDIX.json",
        "proof_compression_submission/templates/build_printed_certificate_appendix.py",
        "proof_compression_submission/templates/verify_printed_certificate_appendix.py",
        "proof_compression_submission/templates/test_printed_certificate_appendix_mutations.py",
        "proof_compression_submission/supplement/certificate_appendix.tex",
        "proof_compression_submission/PDF_BUILD_REPORT.json",
        "proof_compression_submission/PDF_BUILD_REPORT.md",
        *OPERATIONAL_EVIDENCE,
    }
    missing = sorted(required - set(ledger))
    if missing:
        fail(f"required submission source missing: {missing}")
    return ledger


def build_manifest() -> dict[str, Any]:
    reject_optimized_mode()
    frozen = collect_frozen_ledger()
    submission = collect_submission_ledger()
    overlap = sorted(set(frozen).intersection(submission))
    if overlap:
        fail(f"frozen/submission ledger overlap: {overlap[:3]}")
    combined_binding = {"frozen_evidence": frozen, "submission_sources": submission}
    value: dict[str, Any] = {
        "schema": "k2p-revised-referee-bundle-manifest-v1",
        "status": "DRAFT_PC_PARTIAL_PENDING_HUMAN_METADATA",
        "archive_policy": {
            "archive_prefix": ARCHIVE_PREFIX,
            "compression": "ZIP_DEFLATED level 9",
            "fixed_member_timestamp": "2026-08-22T00:00:00",
            "member_mode": "100644",
            "member_order": "project-relative path lexicographic",
            "manifest_included": True,
        },
        "frozen_evidence": {
            "content_ledger_root_sha256": FROZEN_CONTENT_ROOT,
            "file_count": len(frozen),
            "files": frozen,
            "release_lock_payload_sha256": LOCK_PAYLOAD_SHA256,
            "release_lock_sha256": LOCK_SHA256,
            "total_bytes": sum(int(row["bytes"]) for row in frozen.values()),
        },
        "submission_sources": {
            "content_ledger_root_sha256": canonical_hash(submission),
            "file_count": len(submission),
            "files": submission,
            "policy": {
                "base": "proof_compression_submission",
                "excluded_components": ["output except named replay/PDF/log artifacts", "__pycache__", "dot-prefixed directories"],
                "excluded_names": [".DS_Store", MANIFEST_RELATIVE],
                "excluded_suffixes": [".pyc", ".pyo"],
                "symlinks_allowed": False,
            },
            "total_bytes": sum(int(row["bytes"]) for row in submission.values()),
        },
        "combined_content_root_sha256": canonical_hash(combined_binding),
        "combined_file_count_excluding_manifest": len(frozen) + len(submission),
        "pending_human_metadata": PENDING_METADATA,
        "runtime_boundary": clean_full_replay_boundary(),
    }
    value["payload_sha256"] = canonical_hash(value)
    return value


def write_archive(path: Path, manifest: dict[str, Any]) -> str:
    if path.exists() and path.is_symlink():
        fail(f"refusing symbolic archive output: {path}")
    frozen = manifest["frozen_evidence"]["files"]
    submission = manifest["submission_sources"]["files"]
    all_paths = sorted(set(frozen).union(submission).union({MANIFEST_RELATIVE}))
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in all_paths:
            data = project_path(relative).read_bytes()
            info = zipfile.ZipInfo(f"{ARCHIVE_PREFIX}/{relative}", date_time=ARCHIVE_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return sha256_bytes(path.read_bytes())


def main() -> None:
    reject_optimized_mode()
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the deterministic manifest")
    parser.add_argument("--check", action="store_true", help="require exact equality with the existing manifest")
    parser.add_argument("--archive", type=Path, help="write the large deterministic ZIP only when explicitly requested")
    args = parser.parse_args()
    if not args.write and not args.check and args.archive is None:
        parser.error("provide --write, --check, or --archive")
    if args.write and args.check:
        parser.error("--write and --check are mutually exclusive")
    if args.archive is not None and not args.check:
        parser.error("--archive requires --check against a sealed manifest")
    manifest = build_manifest()
    encoded = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if args.write:
        MANIFEST_PATH.write_text(encoded, encoding="utf-8")
    if args.check or args.archive is not None:
        if not MANIFEST_PATH.is_file() or MANIFEST_PATH.is_symlink():
            fail("missing or symbolic revised referee manifest")
        if MANIFEST_PATH.read_text(encoding="utf-8") != encoded:
            fail("revised referee manifest is stale")
    result: dict[str, Any] = {
        "combined_content_root_sha256": manifest["combined_content_root_sha256"],
        "frozen_file_count": manifest["frozen_evidence"]["file_count"],
        "manifest_payload_sha256": manifest["payload_sha256"],
        "status": "PASS",
        "submission_source_file_count": manifest["submission_sources"]["file_count"],
    }
    if args.archive is not None:
        result["archive_path"] = str(args.archive)
        result["archive_sha256"] = write_archive(args.archive, manifest)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
