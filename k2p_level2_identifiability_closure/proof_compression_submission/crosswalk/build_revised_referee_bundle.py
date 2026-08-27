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
TELEMETRY_SUBMISSION_SOURCES = (
    "proof_compression_submission/article/main.tex",
    "proof_compression_submission/article/references.bib",
    "proof_compression_submission/supplement/supplement.tex",
    "proof_compression_submission/supplement/compression_tables.tex",
    "proof_compression_submission/supplement/certificate_appendix.tex",
)
ARCHIVE_PREFIX = "k2p_principal_d_plus_submission_referee"
ARCHIVE_TIMESTAMP = (2026, 8, 27, 0, 0, 0)
OPERATIONAL_EVIDENCE = {
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json",
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json",
    "proof_compression_submission/output/FINAL_RELEASE_MUTATIONS.json",
    "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
    "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
    "proof_compression_submission/output/logs/article.log",
    "proof_compression_submission/output/logs/supplement.log",
}
SUPPLEMENTAL_EXECUTION_DEPENDENCIES = {
    "output/referee/README.md",
    "output/referee/REFEREE_BUNDLE_CONTENTS.json",
    "output/referee/build_referee_bundle.py",
}
SUBMISSION_METADATA = {
    "author_contributions": "approved sole-author contribution statement",
    "code_license": "MIT",
    "competing_interests": "The author declares no competing interests.",
    "corresponding_email": "me@aleckriebel.com",
    "data_license": "CC BY 4.0",
    "doi": None,
    "funding": "No specific funding supported this work.",
    "versioned_annotated_source_tag": "k2p-same-biorxiv-v1.0.3",
    "paper_license": "CC BY 4.0",
    "release_boundary": (
        "No GitHub Release, Zenodo deposit, or DOI is created or claimed by "
        "this package; the author will perform any such release actions."
    ),
}


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


def unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build one JSON object while rejecting every repeated member name."""

    value: dict[str, Any] = {}
    for name, child in pairs:
        if name in value:
            fail(f"duplicate JSON object name: {name!r}")
        value[name] = child
    return value


def parse_json_document(data: str | bytes, label: str) -> Any:
    try:
        return json.loads(data, object_pairs_hook=unique_json_object)
    except json.JSONDecodeError as error:
        fail(f"invalid JSON in {label}: {error.msg}")


def validate_json_member(relative: str, data: bytes) -> None:
    if PurePosixPath(relative).suffix == ".json":
        parse_json_document(data, relative)


def read_json(relative: str) -> dict[str, Any]:
    value = parse_json_document(project_path(relative).read_bytes(), relative)
    if not isinstance(value, dict):
        fail(f"expected JSON object: {relative}")
    return value


def release_context() -> tuple[dict[str, Any], str, str]:
    lock_path = project_path(LOCK_RELATIVE)
    if not lock_path.is_file() or lock_path.is_symlink():
        fail("missing or symbolic RELEASE_LOCK")
    lock_bytes = lock_path.read_bytes()
    lock_sha256 = sha256_bytes(lock_bytes)
    lock = parse_json_document(lock_bytes, LOCK_RELATIVE)
    if not isinstance(lock, dict):
        fail("RELEASE_LOCK is not an object")
    if lock.get("schema") != "k2p-principal-d-plus-final-theorem-release-lock-v1":
        fail("RELEASE_LOCK schema mismatch")
    payload_sha256 = lock.get("payload_sha256")
    unsigned = dict(lock)
    unsigned.pop("payload_sha256", None)
    if not isinstance(payload_sha256, str) or payload_sha256 != canonical_hash(unsigned):
        fail("RELEASE_LOCK payload mismatch")
    if lock.get("promotion_ready") is not True or lock.get("blockers") or lock.get("missing_required_files"):
        fail("RELEASE_LOCK is not promotion-ready")
    return lock, lock_sha256, payload_sha256


def current_file_row(relative: str) -> dict[str, int | str]:
    path = project_path(relative)
    if not path.is_file() or path.is_symlink():
        fail(f"missing or symbolic telemetry-bound file: {relative}")
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256_bytes(data)}


def expected_telemetry_submission_sources() -> dict[str, dict[str, int | str]]:
    return {
        relative: current_file_row(relative)
        for relative in TELEMETRY_SUBMISSION_SOURCES
    }


def expected_telemetry_release_lock(
    lock_sha256: str, lock_payload_sha256: str
) -> dict[str, int | str]:
    lock_row = current_file_row(LOCK_RELATIVE)
    if lock_row["sha256"] != lock_sha256:
        fail("telemetry release-lock current hash mismatch")
    return {
        "bytes": lock_row["bytes"],
        "path": LOCK_RELATIVE,
        "payload_sha256": lock_payload_sha256,
        "sha256": lock_sha256,
    }


def validate_telemetry_checkout_bindings(
    telemetry: dict[str, Any], lock_sha256: str, lock_payload_sha256: str
) -> None:
    if telemetry.get("submission_sources") != expected_telemetry_submission_sources():
        fail("clean full replay telemetry submission-source binding mismatch")
    if telemetry.get("release_lock") != expected_telemetry_release_lock(
        lock_sha256, lock_payload_sha256
    ):
        fail("clean full replay telemetry release-lock binding mismatch")


def clean_full_replay_boundary(
    lock_sha256: str, lock_payload_sha256: str
) -> dict[str, Any]:
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
    layers = report.get("layer_replays")
    if report.get("mode") != "full" or not isinstance(layers, list) or not layers:
        fail("clean full replay mode/layer census mismatch")
    if report.get("lock_payload_sha256") != lock_payload_sha256:
        fail("clean full replay lock payload mismatch")
    if telemetry.get("schema") != "k2p-final-clean-full-replay-telemetry-v1" or telemetry.get("status") != "PASS":
        fail("clean full replay telemetry schema/status mismatch")
    if telemetry.get("report", {}).get("sha256") != report_sha:
        fail("clean full replay telemetry report hash mismatch")
    if telemetry.get("report", {}).get("lock_payload_sha256") != lock_payload_sha256:
        fail("clean full replay telemetry lock payload mismatch")
    validate_telemetry_checkout_bindings(
        telemetry, lock_sha256, lock_payload_sha256
    )
    if telemetry.get("clean_detached_checkout") is not True:
        fail("clean full replay was not run from a detached clean checkout")
    timing = telemetry.get("time_l", {})
    for key in ("real_seconds", "maximum_resident_set_size_bytes", "peak_memory_footprint_bytes"):
        value = timing.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            fail(f"clean full replay telemetry missing positive field: {key}")
    internal_elapsed = report.get("elapsed_seconds")
    if not isinstance(internal_elapsed, (int, float)) or isinstance(internal_elapsed, bool) or internal_elapsed <= 0:
        fail("clean full replay internal elapsed time missing")
    if timing["real_seconds"] < internal_elapsed:
        fail("clean full replay wall time is below internal elapsed time")
    if (
        telemetry.get("report", {}).get("layer_count") != len(layers)
        or telemetry.get("report", {}).get("internal_elapsed_seconds") != internal_elapsed
        or telemetry.get("report", {}).get("promotion_ready") is not True
        or telemetry.get("report", {}).get("blocker_count") != 0
    ):
        fail("clean full replay telemetry summary mismatch")
    git_commit = telemetry.get("git_commit")
    if not isinstance(git_commit, str) or not git_commit:
        fail("clean full replay git commit missing")
    return {
        "status": "clean_detached_full_replay_pass",
        "git_commit": git_commit,
        "clean_detached_checkout": True,
        "end_to_end_full_runtime_seconds": timing["real_seconds"],
        "internal_elapsed_seconds": internal_elapsed,
        "layer_count": len(layers),
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


def collect_frozen_ledger(
    lock: dict[str, Any], lock_sha256: str
) -> dict[str, dict[str, int | str]]:
    outer_files = lock.get("files")
    if not isinstance(outer_files, dict) or not outer_files:
        fail("missing frozen outer file map")
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
        validate_json_member(relative, data)
        metadata: dict[str, int | str] = {"bytes": len(data), "sha256": sha256_bytes(data)}
        outer = outer_files.get(relative)
        if isinstance(outer, dict):
            if metadata["bytes"] != outer.get("bytes") or metadata["sha256"] != outer.get("sha256"):
                fail(f"outer frozen lock mismatch: {relative}")
        ledger[relative] = metadata
    if ledger[LOCK_RELATIVE]["sha256"] != lock_sha256:
        fail("frozen RELEASE_LOCK binding mismatch")
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
        validate_json_member(relative.as_posix(), data)
        ledger[relative.as_posix()] = {"bytes": len(data), "sha256": sha256_bytes(data)}
    for relative in sorted(SUPPLEMENTAL_EXECUTION_DEPENDENCIES):
        path = project_path(relative)
        if not path.is_file() or path.is_symlink():
            fail(f"missing or symbolic supplemental execution dependency: {relative}")
        data = path.read_bytes()
        validate_json_member(relative, data)
        ledger[relative] = {"bytes": len(data), "sha256": sha256_bytes(data)}
    required = {
        "proof_compression_submission/AI_REFEREE_PROMPT.md",
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
        "proof_compression_submission/adversarial_review/STATIC_AUDIT_RESULT.json",
        "proof_compression_submission/adversarial_review/audit_article_sources.py",
        *OPERATIONAL_EVIDENCE,
        *SUPPLEMENTAL_EXECUTION_DEPENDENCIES,
    }
    missing = sorted(required - set(ledger))
    if missing:
        fail(f"required submission source missing: {missing}")
    return ledger


def build_manifest() -> dict[str, Any]:
    reject_optimized_mode()
    lock, lock_sha256, lock_payload_sha256 = release_context()
    frozen = collect_frozen_ledger(lock, lock_sha256)
    frozen_content_root = canonical_hash(frozen)
    submission = collect_submission_ledger()
    overlap = sorted(set(frozen).intersection(submission))
    if overlap:
        fail(f"frozen/submission ledger overlap: {overlap[:3]}")
    combined_binding = {"frozen_evidence": frozen, "submission_sources": submission}
    value: dict[str, Any] = {
        "schema": "k2p-revised-referee-bundle-manifest-v2",
        "status": "SUBMISSION_READY_PC_PARTIAL",
        "archive_policy": {
            "archive_prefix": ARCHIVE_PREFIX,
            "compression": "ZIP_DEFLATED level 9",
            "fixed_member_timestamp": "2026-08-26T00:00:00",
            "member_mode": "100644",
            "member_order": "project-relative path lexicographic",
            "manifest_included": True,
        },
        "frozen_evidence": {
            "content_ledger_root_sha256": frozen_content_root,
            "file_count": len(frozen),
            "files": frozen,
            "release_lock_payload_sha256": lock_payload_sha256,
            "release_lock_sha256": lock_sha256,
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
                "supplemental_execution_dependencies": sorted(
                    SUPPLEMENTAL_EXECUTION_DEPENDENCIES
                ),
                "symlinks_allowed": False,
            },
            "total_bytes": sum(int(row["bytes"]) for row in submission.values()),
        },
        "combined_content_root_sha256": canonical_hash(combined_binding),
        "combined_file_count_excluding_manifest": len(frozen) + len(submission),
        "submission_metadata": SUBMISSION_METADATA,
        "runtime_boundary": clean_full_replay_boundary(
            lock_sha256, lock_payload_sha256
        ),
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
