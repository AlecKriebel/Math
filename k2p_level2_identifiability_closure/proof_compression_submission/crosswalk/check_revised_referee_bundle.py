#!/usr/bin/env python3
"""Independent fail-closed checker for the revised referee manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any


PROJECT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = Path(__file__).with_name("REVISED_REFEREE_BUNDLE_MANIFEST.json")
LOCK_RELATIVE = "work/final_theorem_release/RELEASE_LOCK.json"
MANIFEST_RELATIVE = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
LOCK_SHA256 = "0c17eeaa3344f0982998ea694c1eb92f72f5ced0841e2acad0d39566e2ec71c3"
LOCK_PAYLOAD_SHA256 = "0e146ccee2352b80a5ceb605ff7aaa612ed28fd3122744b056c891d1e2ed2690"
FROZEN_CONTENT_ROOT = "c79fa2d3cb6431207823e3c66c3440cbeb94226d8a9925960883efca7dca2416"
PENDING_METADATA = [
    "corresponding email address",
    "author-contribution statement",
    "funding declaration",
    "competing-interests declaration",
    "article license",
    "code license",
    "data license",
    "final repository URL and immutable submission tag",
    "whether and when to mint a GitHub/Zenodo DOI release",
    "final clean full-replay wall time and peak memory",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def reject_optimized_mode() -> None:
    if not __debug__:
        fail("optimized Python is forbidden")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return sha256_bytes(data)


def safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        fail(f"unsafe path in manifest: {value!r}")
    return path


def project_path(relative: str) -> Path:
    return PROJECT.joinpath(*safe_relative(relative).parts)


def object_from_path(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing or symbolic {label}: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"{label} is not a JSON object")
    return value


def add_sha_manifest(expected: dict[str, str], relative: str, base: str) -> None:
    for ordinal, line in enumerate(project_path(relative).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            fail(f"invalid SHA manifest line {relative}:{ordinal}")
        digest, child = match.groups()
        child_relative = (PurePosixPath(base) / safe_relative(child)).as_posix()
        previous = expected.get(child_relative)
        if previous is not None and previous != digest:
            fail(f"conflicting nested digest for {child_relative}")
        expected[child_relative] = digest


def reconstruct_frozen_bindings() -> dict[str, dict[str, int | str]]:
    lock_bytes = project_path(LOCK_RELATIVE).read_bytes()
    if sha256_bytes(lock_bytes) != LOCK_SHA256:
        fail("RELEASE_LOCK hash mismatch")
    lock = json.loads(lock_bytes)
    if not isinstance(lock, dict):
        fail("RELEASE_LOCK is not an object")
    if lock.get("schema") != "k2p-principal-d-plus-final-theorem-release-lock-v1":
        fail("RELEASE_LOCK schema mismatch")
    if lock.get("payload_sha256") != LOCK_PAYLOAD_SHA256:
        fail("RELEASE_LOCK payload mismatch")
    if lock.get("promotion_ready") is not True or lock.get("blockers") or lock.get("missing_required_files"):
        fail("RELEASE_LOCK is not promotion-ready")
    files = lock.get("files")
    if not isinstance(files, dict) or len(files) != 194:
        fail("RELEASE_LOCK outer file count mismatch")
    expected: dict[str, str] = {}
    for relative, row in files.items():
        if not isinstance(relative, str) or not isinstance(row, dict) or not isinstance(row.get("sha256"), str):
            fail("malformed outer frozen file binding")
        expected[relative] = row["sha256"]
    add_sha_manifest(expected, "work/rank_upper_certificates/MANIFEST.sha256", "work/rank_upper_certificates")
    add_sha_manifest(expected, "work/cycle_three_port_closure/MANIFEST.sha256", "work/cycle_three_port_closure")
    direct_base = PurePosixPath("package/referee/k2p_offline_sweep_portable")
    for name in ("DIRECT_CLOSURE_LOCK.json", "INPUT_LOCK.json"):
        nested_path = project_path((direct_base / name).as_posix())
        nested = object_from_path(nested_path, name)
        nested_files = nested.get("files")
        if not isinstance(nested_files, dict):
            fail(f"missing files object in {name}")
        for child, digest in nested_files.items():
            if not isinstance(child, str) or not isinstance(digest, str):
                fail(f"malformed nested binding in {name}")
            relative = (direct_base / safe_relative(child)).as_posix()
            previous = expected.get(relative)
            if previous is not None and previous != digest:
                fail(f"conflicting nested direct digest: {relative}")
            expected[relative] = digest
    expected[LOCK_RELATIVE] = LOCK_SHA256
    actual: dict[str, dict[str, int | str]] = {}
    for relative in sorted(expected):
        path = project_path(relative)
        if not path.is_file() or path.is_symlink():
            fail(f"missing or symbolic frozen file: {relative}")
        data = path.read_bytes()
        digest = sha256_bytes(data)
        if digest != expected[relative]:
            fail(f"frozen digest mismatch: {relative}")
        actual[relative] = {"bytes": len(data), "sha256": digest}
    if len(actual) != 370:
        fail(f"reconstructed frozen file count mismatch: {len(actual)}")
    if sum(int(row["bytes"]) for row in actual.values()) != 434_661_763:
        fail("reconstructed frozen byte count mismatch")
    if canonical_hash(actual) != FROZEN_CONTENT_ROOT:
        fail("reconstructed frozen content root mismatch")
    return actual


def include_source(relative: PurePosixPath) -> bool:
    if not relative.parts or relative.parts[0] != "proof_compression_submission":
        return False
    if relative.as_posix() == MANIFEST_RELATIVE:
        return False
    if "output" in relative.parts or "__pycache__" in relative.parts:
        return False
    if relative.name == ".DS_Store" or relative.suffix in {".pyc", ".pyo"}:
        return False
    return True


def reconstruct_submission_bindings() -> dict[str, dict[str, int | str]]:
    base = PROJECT / "proof_compression_submission"
    if not base.is_dir() or base.is_symlink():
        fail("submission source root missing or symbolic")
    actual: dict[str, dict[str, int | str]] = {}
    for path in sorted(base.rglob("*")):
        if path.is_dir():
            continue
        relative = PurePosixPath(path.relative_to(PROJECT).as_posix())
        if not include_source(relative):
            continue
        if not path.is_file() or path.is_symlink():
            fail(f"submission source is not a regular file: {relative.as_posix()}")
        data = path.read_bytes()
        actual[relative.as_posix()] = {"bytes": len(data), "sha256": sha256_bytes(data)}
    return actual


def check_ledger(label: str, declared: Any, actual: dict[str, dict[str, int | str]]) -> None:
    if not isinstance(declared, dict):
        fail(f"missing {label} object")
    files = declared.get("files")
    if not isinstance(files, dict):
        fail(f"missing {label} file map")
    for relative in files:
        if not isinstance(relative, str):
            fail(f"non-string path in {label}")
        safe_relative(relative)
    if files != actual:
        missing = sorted(set(actual) - set(files))
        extra = sorted(set(files) - set(actual))
        fail(f"{label} ledger mismatch; missing={missing[:3]} extra={extra[:3]}")
    if declared.get("file_count") != len(actual):
        fail(f"{label} file count mismatch")
    if declared.get("total_bytes") != sum(int(row["bytes"]) for row in actual.values()):
        fail(f"{label} byte count mismatch")
    if declared.get("content_ledger_root_sha256") != canonical_hash(actual):
        fail(f"{label} content root mismatch")


def declared_json_schema(relative: str) -> str | None:
    if not relative.endswith(".json"):
        return None
    value = json.loads(project_path(relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        return None
    schema = value.get("schema")
    return schema if isinstance(schema, str) else None


def verify_crosswalk(frozen: dict[str, dict[str, int | str]], submission: dict[str, dict[str, int | str]]) -> None:
    relative = "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json"
    if relative not in submission:
        fail("crosswalk JSON omitted from submission ledger")
    crosswalk = object_from_path(project_path(relative), "theorem artifact crosswalk")
    if crosswalk.get("schema") != "k2p-theorem-artifact-reproducibility-crosswalk-v1":
        fail("crosswalk schema mismatch")
    if crosswalk.get("status") != "PASS_PC_PARTIAL":
        fail("crosswalk status mismatch")
    payload = crosswalk.get("payload_sha256")
    unsigned = dict(crosswalk)
    unsigned.pop("payload_sha256", None)
    if not isinstance(payload, str) or payload != canonical_hash(unsigned):
        fail("crosswalk payload mismatch")
    if crosswalk.get("pending_human_metadata") != PENDING_METADATA:
        fail("crosswalk pending metadata drift")
    claims = crosswalk.get("claims")
    if not isinstance(claims, list) or len(claims) != 13:
        fail("crosswalk claim census mismatch")
    required_fields = {
        "claim_id",
        "claim",
        "proof_status",
        "compression_status",
        "authoritative_artifacts",
        "producer_artifacts",
        "replay_artifacts",
        "mutation_artifacts",
        "environment_profile",
        "runtime",
    }
    seen: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict) or not required_fields.issubset(claim):
            fail("crosswalk claim is missing a required field")
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or claim_id in seen:
            fail("duplicate or malformed crosswalk claim ID")
        seen.add(claim_id)
        for field in ("authoritative_artifacts", "producer_artifacts", "replay_artifacts", "mutation_artifacts"):
            rows = claim.get(field)
            if not isinstance(rows, list) or not rows:
                fail(f"empty artifact field {claim_id}:{field}")
            for row in rows:
                if not isinstance(row, dict):
                    fail(f"malformed artifact row {claim_id}:{field}")
                path = row.get("path")
                digest = row.get("sha256")
                frozen_flag = row.get("frozen")
                if not isinstance(path, str) or not isinstance(digest, str) or not isinstance(frozen_flag, bool):
                    fail(f"malformed artifact binding {claim_id}:{field}")
                ledger = frozen if frozen_flag else submission
                bound = ledger.get(path)
                if not isinstance(bound, dict) or bound.get("sha256") != digest or bound.get("bytes") != row.get("bytes"):
                    fail(f"unbound crosswalk artifact {claim_id}:{path}")
                if row.get("declared_schema") != declared_json_schema(path):
                    fail(f"declared schema drift {claim_id}:{path}")
        runtime = claim.get("runtime")
        if not isinstance(runtime, dict) or runtime.get("status") not in {"unknown", "component_observation_only"}:
            fail(f"malformed runtime boundary: {claim_id}")
        if runtime.get("end_to_end_seconds") is not None:
            fail(f"unsupported inferred end-to-end runtime: {claim_id}")


def validate(manifest_path: Path) -> dict[str, Any]:
    reject_optimized_mode()
    manifest = object_from_path(manifest_path, "revised referee manifest")
    if manifest.get("schema") != "k2p-revised-referee-bundle-manifest-v1":
        fail("manifest schema mismatch")
    if manifest.get("status") != "DRAFT_PC_PARTIAL_PENDING_HUMAN_METADATA":
        fail("manifest status mismatch")
    payload = manifest.get("payload_sha256")
    unsigned = dict(manifest)
    unsigned.pop("payload_sha256", None)
    if not isinstance(payload, str) or payload != canonical_hash(unsigned):
        fail("manifest payload mismatch")
    if manifest.get("pending_human_metadata") != PENDING_METADATA:
        fail("manifest pending metadata mismatch")
    runtime = manifest.get("runtime_boundary")
    if runtime != {
        "end_to_end_full_runtime_seconds": None,
        "end_to_end_quick_runtime_seconds": None,
        "status": "unknown_not_byte_bound",
    }:
        fail("manifest runtime boundary mismatch")
    frozen = reconstruct_frozen_bindings()
    submission = reconstruct_submission_bindings()
    check_ledger("frozen evidence", manifest.get("frozen_evidence"), frozen)
    check_ledger("submission sources", manifest.get("submission_sources"), submission)
    frozen_section = manifest["frozen_evidence"]
    if frozen_section.get("release_lock_sha256") != LOCK_SHA256:
        fail("manifest frozen lock hash mismatch")
    if frozen_section.get("release_lock_payload_sha256") != LOCK_PAYLOAD_SHA256:
        fail("manifest frozen lock payload mismatch")
    if manifest.get("combined_file_count_excluding_manifest") != len(frozen) + len(submission):
        fail("combined file count mismatch")
    combined = {"frozen_evidence": frozen, "submission_sources": submission}
    if manifest.get("combined_content_root_sha256") != canonical_hash(combined):
        fail("combined content root mismatch")
    policy = manifest["submission_sources"].get("policy")
    expected_policy = {
        "base": "proof_compression_submission",
        "excluded_components": ["output", "__pycache__"],
        "excluded_names": [".DS_Store", MANIFEST_RELATIVE],
        "excluded_suffixes": [".pyc", ".pyo"],
        "symlinks_allowed": False,
    }
    if policy != expected_policy:
        fail("submission source policy mismatch")
    required_sources = {
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
    }
    missing = sorted(required_sources - set(submission))
    if missing:
        fail(f"required source omitted: {missing}")
    verify_crosswalk(frozen, submission)
    return {
        "combined_content_root_sha256": manifest["combined_content_root_sha256"],
        "frozen_file_count": len(frozen),
        "manifest_payload_sha256": manifest["payload_sha256"],
        "status": "PASS",
        "submission_source_file_count": len(submission),
    }


def main() -> None:
    reject_optimized_mode()
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    print(json.dumps(validate(args.manifest), sort_keys=True))


if __name__ == "__main__":
    main()
