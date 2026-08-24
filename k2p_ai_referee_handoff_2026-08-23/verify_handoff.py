#!/usr/bin/env python3
"""Independent fail-closed verification of the outer and inner handoff ledgers."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_MANIFEST = ROOT / "PACKAGE_MANIFEST.json"
INNER_ROOT = ROOT / "materials" / "k2p_principal_d_plus_submission_referee"
INNER_MANIFEST_RELATIVE = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
IGNORED_TOP_LEVEL = {".referee_venv", "referee_outputs"}
IGNORED_COMPONENTS = {".venv"}


def fail(message: str) -> None:
    raise SystemExit(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def safe(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        fail(f"unsafe manifest path: {value!r}")
    return path


def include(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if relative.as_posix() == "PACKAGE_MANIFEST.json":
        return False
    if relative.parts and relative.parts[0] in IGNORED_TOP_LEVEL:
        return False
    if any(part in IGNORED_COMPONENTS for part in relative.parts):
        return False
    if "__pycache__" in relative.parts or path.name == ".DS_Store":
        return False
    return path.suffix not in {".pyc", ".pyo"}


def actual_outer_files() -> dict[str, dict[str, int | str]]:
    result: dict[str, dict[str, int | str]] = {}
    for path in sorted(ROOT.rglob("*")):
        if path.is_dir() or not include(path):
            continue
        if not path.is_file() or path.is_symlink():
            fail(f"non-regular or symbolic handoff file: {path}")
        relative = path.relative_to(ROOT).as_posix()
        safe(relative)
        data = path.read_bytes()
        result[relative] = {"bytes": len(data), "sha256": digest(data)}
    return result


def verify_inner(inner: dict[str, Any]) -> tuple[int, int]:
    if inner.get("schema") != "k2p-revised-referee-bundle-manifest-v1":
        fail("inner manifest schema mismatch")
    payload = inner.get("payload_sha256")
    unsigned = dict(inner)
    unsigned.pop("payload_sha256", None)
    if payload != digest(canonical(unsigned)):
        fail("inner manifest payload mismatch")
    frozen = inner.get("frozen_evidence", {}).get("files")
    submission = inner.get("submission_sources", {}).get("files")
    if not isinstance(frozen, dict) or not isinstance(submission, dict):
        fail("inner file maps are missing")
    if len(frozen) != 374 or len(submission) != 73:
        fail("inner file census mismatch")
    for relative, row in {**frozen, **submission}.items():
        path = INNER_ROOT.joinpath(*safe(relative).parts)
        if not path.is_file() or path.is_symlink():
            fail(f"missing or symbolic inner file: {relative}")
        data = path.read_bytes()
        if row != {"bytes": len(data), "sha256": digest(data)}:
            fail(f"inner file binding mismatch: {relative}")
    combined = {"frozen_evidence": frozen, "submission_sources": submission}
    if inner.get("combined_content_root_sha256") != digest(canonical(combined)):
        fail("inner combined content root mismatch")
    return len(frozen), len(submission)


def verify(manifest_path: Path) -> dict[str, Any]:
    if not __debug__:
        fail("optimized Python is forbidden")
    if not manifest_path.is_file() or manifest_path.is_symlink():
        fail("outer handoff manifest is missing or symbolic")
    value = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema") != "k2p-post-submission-ai-referee-handoff-v1":
        fail("outer manifest schema mismatch")
    if value.get("status") != "READY_FOR_INDEPENDENT_REVIEW":
        fail("outer manifest status mismatch")
    payload = value.get("payload_sha256")
    unsigned = dict(value)
    unsigned.pop("payload_sha256", None)
    if payload != digest(canonical(unsigned)):
        fail("outer manifest payload mismatch")
    declared = value.get("files")
    if not isinstance(declared, dict):
        fail("outer manifest file map missing")
    for relative in declared:
        safe(relative)
    actual = actual_outer_files()
    if declared != actual:
        fail(f"outer file ledger mismatch: declared={len(declared)} actual={len(actual)}")
    if value.get("file_count_excluding_manifest") != len(actual):
        fail("outer file count mismatch")
    if value.get("total_bytes_excluding_manifest") != sum(int(row["bytes"]) for row in actual.values()):
        fail("outer byte count mismatch")
    if value.get("content_root_sha256") != digest(canonical(actual)):
        fail("outer content root mismatch")
    inner_path = INNER_ROOT / INNER_MANIFEST_RELATIVE
    inner = json.loads(inner_path.read_text(encoding="utf-8"))
    frozen_count, submission_count = verify_inner(inner)
    summary = value.get("inner_manifest")
    expected_summary = {
        "path": inner_path.relative_to(ROOT).as_posix(),
        "payload_sha256": inner.get("payload_sha256"),
        "combined_content_root_sha256": inner.get("combined_content_root_sha256"),
        "frozen_file_count": frozen_count,
        "submission_file_count": submission_count,
    }
    if summary != expected_summary:
        fail("outer-to-inner manifest binding mismatch")
    binding_path = ROOT / "SUBMISSION_BINDING.json"
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    if binding.get("schema") != "k2p-ai-referee-submission-binding-v1":
        fail("submission binding schema mismatch")
    paper_sources = {
        "article": "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
        "supplement": "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
    }
    for label, inner_relative in paper_sources.items():
        row = binding.get("papers", {}).get(label)
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            fail(f"submission paper binding malformed: {label}")
        outer_paper = ROOT.joinpath(*safe(row["path"]).parts)
        inner_paper = INNER_ROOT / inner_relative
        outer_data = outer_paper.read_bytes()
        inner_data = inner_paper.read_bytes()
        if outer_data != inner_data:
            fail(f"top-level and inner paper bytes differ: {label}")
        if row.get("bytes") != len(outer_data) or row.get("sha256") != digest(outer_data):
            fail(f"submission paper hash/byte binding mismatch: {label}")
    source_bindings = binding.get("five_source_set")
    if not isinstance(source_bindings, dict) or len(source_bindings) != 5:
        fail("five-source submission binding malformed")
    for relative, expected_hash in source_bindings.items():
        path = INNER_ROOT.joinpath(*safe(relative).parts)
        if digest(path.read_bytes()) != expected_hash:
            fail(f"five-source hash mismatch: {relative}")
    computational = binding.get("computational_evidence")
    if not isinstance(computational, dict):
        fail("computational submission binding malformed")
    if computational.get("inner_manifest_payload_sha256") != inner.get("payload_sha256"):
        fail("submission binding inner payload mismatch")
    if computational.get("inner_combined_content_root_sha256") != inner.get("combined_content_root_sha256"):
        fail("submission binding inner content root mismatch")
    quick = binding.get("copied_handoff_quick_qualification")
    if not isinstance(quick, dict) or not isinstance(quick.get("path"), str):
        fail("copied quick-qualification binding malformed")
    quick_path = ROOT.joinpath(*safe(quick["path"]).parts)
    quick_value = json.loads(quick_path.read_text(encoding="utf-8"))
    if digest(quick_path.read_bytes()) != quick.get("sha256"):
        fail("copied quick-qualification hash mismatch")
    if quick_value.get("status") != "PASS" or quick_value.get("commands_completed") != quick.get("commands"):
        fail("copied quick qualification is not complete PASS")
    dependencies = binding.get("supplemental_execution_dependencies_added_outside_the_inner_seal")
    if not isinstance(dependencies, dict) or len(dependencies) != 5:
        fail("supplemental execution-dependency binding malformed")
    for relative, row in dependencies.items():
        if not isinstance(row, dict):
            fail(f"supplemental execution-dependency row malformed: {relative}")
        path = INNER_ROOT.joinpath(*safe(relative).parts)
        data = path.read_bytes()
        if digest(data) != row.get("sha256"):
            fail(f"supplemental execution-dependency hash mismatch: {relative}")
        matching = row.get("matching_inner_sealed_copy")
        if matching is not None:
            if not isinstance(matching, str):
                fail(f"matching sealed-copy path malformed: {relative}")
            if data != INNER_ROOT.joinpath(*safe(matching).parts).read_bytes():
                fail(f"declared matching sealed copy differs: {relative}")
    required = [
        "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
        "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
        "work/final_theorem_release/RELEASE_LOCK.json",
        "work/final_theorem_release/verify_final_theorem_release.py",
        "work/final_theorem_release/run_release_mutations.py",
    ]
    for relative in required:
        if not (INNER_ROOT / relative).is_file():
            fail(f"required referee artifact missing: {relative}")
    return {
        "status": "PASS",
        "outer_files": len(actual),
        "outer_payload_sha256": payload,
        "inner_frozen_files": frozen_count,
        "inner_submission_files": submission_count,
        "inner_payload_sha256": inner.get("payload_sha256"),
        "submission_binding": "PASS",
        "supplemental_execution_dependencies": len(dependencies),
        "copied_quick_qualification": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    print(json.dumps(verify(args.manifest), sort_keys=True))


if __name__ == "__main__":
    main()
