#!/usr/bin/env python3
"""Independent fail-closed checker for the revised referee manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any


PROJECT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = Path(__file__).with_name("REVISED_REFEREE_BUNDLE_MANIFEST.json")
LOCK_RELATIVE = "work/final_theorem_release/RELEASE_LOCK.json"
MANIFEST_RELATIVE = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
TELEMETRY_SUBMISSION_SOURCES = (
    "proof_compression_submission/article/main.tex",
    "proof_compression_submission/article/references.bib",
    "proof_compression_submission/supplement/supplement.tex",
    "proof_compression_submission/supplement/compression_tables.tex",
    "proof_compression_submission/supplement/certificate_appendix.tex",
)
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


def verify_portable_builder_optimized_mode_contract() -> None:
    relative = "output/referee/build_referee_bundle.py"
    builder = project_path(relative)
    if not builder.is_file() or builder.is_symlink():
        fail("missing or symbolic portable referee-bundle builder")
    try:
        result = subprocess.run(
            [sys.executable, "-O", "-B", str(builder), "--check-only"],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired:
        fail("portable referee-bundle builder optimized-mode probe timed out")
    diagnostic = (result.stdout + result.stderr).strip()
    if result.returncode != 1 or diagnostic != "optimized Python is forbidden":
        fail("portable referee-bundle builder does not reject optimized Python exactly")


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


def decode_json_without_repeated_names(data: str | bytes, label: str) -> Any:
    """Decode independently of the producer and reject ambiguous objects."""

    def checked_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        names = [name for name, _ in pairs]
        if len(names) != len(set(names)):
            seen: set[str] = set()
            for name in names:
                if name in seen:
                    fail(f"{label} contains duplicate JSON name: {name!r}")
                seen.add(name)
        return dict(pairs)

    try:
        return json.loads(data, object_pairs_hook=checked_pairs)
    except json.JSONDecodeError as error:
        fail(f"invalid JSON in {label}: {error.msg}")


def verify_json_member(relative: str, data: bytes) -> None:
    if PurePosixPath(relative).suffix == ".json":
        decode_json_without_repeated_names(data, relative)


def object_from_path(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing or symbolic {label}: {path}")
    value = decode_json_without_repeated_names(path.read_bytes(), label)
    if not isinstance(value, dict):
        fail(f"{label} is not a JSON object")
    return value


def release_context() -> tuple[dict[str, Any], str, str]:
    lock_path = project_path(LOCK_RELATIVE)
    lock = object_from_path(lock_path, "RELEASE_LOCK")
    lock_sha256 = sha256_bytes(lock_path.read_bytes())
    if lock.get("schema") != "k2p-principal-d-plus-final-theorem-release-lock-v1":
        fail("RELEASE_LOCK schema mismatch")
    lock_payload_sha256 = lock.get("payload_sha256")
    unsigned = dict(lock)
    unsigned.pop("payload_sha256", None)
    if not isinstance(lock_payload_sha256, str) or lock_payload_sha256 != canonical_hash(unsigned):
        fail("RELEASE_LOCK payload mismatch")
    if lock.get("promotion_ready") is not True or lock.get("blockers") or lock.get("missing_required_files"):
        fail("RELEASE_LOCK is not promotion-ready")
    return lock, lock_sha256, lock_payload_sha256


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


def reconstruct_frozen_bindings(
    lock: dict[str, Any], lock_sha256: str
) -> dict[str, dict[str, int | str]]:
    files = lock.get("files")
    if not isinstance(files, dict) or not files:
        fail("RELEASE_LOCK outer file map missing")
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
    expected[LOCK_RELATIVE] = lock_sha256
    actual: dict[str, dict[str, int | str]] = {}
    for relative in sorted(expected):
        path = project_path(relative)
        if not path.is_file() or path.is_symlink():
            fail(f"missing or symbolic frozen file: {relative}")
        data = path.read_bytes()
        digest = sha256_bytes(data)
        if digest != expected[relative]:
            fail(f"frozen digest mismatch: {relative}")
        verify_json_member(relative, data)
        actual[relative] = {"bytes": len(data), "sha256": digest}
    return actual


def include_source(relative: PurePosixPath) -> bool:
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
        verify_json_member(relative.as_posix(), data)
        actual[relative.as_posix()] = {"bytes": len(data), "sha256": sha256_bytes(data)}
    for relative in sorted(SUPPLEMENTAL_EXECUTION_DEPENDENCIES):
        path = project_path(relative)
        if not path.is_file() or path.is_symlink():
            fail(f"missing or symbolic supplemental execution dependency: {relative}")
        data = path.read_bytes()
        verify_json_member(relative, data)
        actual[relative] = {"bytes": len(data), "sha256": sha256_bytes(data)}
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
    value = decode_json_without_repeated_names(
        project_path(relative).read_bytes(), relative
    )
    if not isinstance(value, dict):
        return None
    schema = value.get("schema")
    return schema if isinstance(schema, str) else None


def verify_c02_scope(claim: dict[str, Any]) -> None:
    """Fail closed on the corrected, deliberately narrow C02 authority."""

    expected_claim = (
        "Pointwise displayed-quartet signs, labelled tree-of-blobs recovery, "
        "and raw four-port displayed-quartet direction."
    )
    if claim.get("claim_id") != "C02-quartet-tree-of-blobs":
        fail("C02 claim record missing")
    if claim.get("claim") != expected_claim:
        fail("C02 claim scope drift")

    topology_path = (
        "work/adversarial_proof_review/topology_direction_certificate.json"
    )
    verifier_path = "work/adversarial_proof_review/verify_topology_direction.py"
    expected_bindings = {
        "authoritative_artifacts": {
            topology_path: (
                "raw displayed-quartet graph-direction certificate; no "
                "restoration or whole-map T_i authority"
            )
        },
        "producer_artifacts": {
            verifier_path: "raw displayed-quartet graph-direction producer"
        },
        "replay_artifacts": {
            verifier_path: "independent raw displayed-quartet replay"
        },
    }
    for field, expected in expected_bindings.items():
        rows = claim.get(field)
        if not isinstance(rows, list):
            fail(f"C02 artifact field missing: {field}")
        for path, role in expected.items():
            matches = [
                row
                for row in rows
                if isinstance(row, dict) and row.get("path") == path
            ]
            if len(matches) != 1 or matches[0].get("role") != role:
                fail(f"C02 narrowed artifact role drift: {field}:{path}")

    certificate = object_from_path(
        project_path(topology_path), "raw displayed-quartet direction certificate"
    )
    certificate_payload = certificate.get("payload_sha256")
    unsigned_certificate = dict(certificate)
    unsigned_certificate.pop("payload_sha256", None)
    if (
        not isinstance(certificate_payload, str)
        or certificate_payload != canonical_hash(unsigned_certificate)
    ):
        fail("C02 direction certificate payload mismatch")
    expected_scope = (
        "principal D_plus; raw four-port displayed-quartet direction and "
        "tree-of-blobs predicate only; no restoration or whole-map T_i classifier"
    )
    if (
        certificate.get("schema") != "k2p-displayed-quartet-direction-audit-v2"
        or certificate.get("status") != "PASS"
        or certificate.get("scope") != expected_scope
        or certificate.get("excluded_claims")
        != [
            "rooted tree/sunlet classification",
            "restoration-child classification",
            "whole-map T_i classification",
        ]
    ):
        fail("C02 direction certificate scope drift")
    raw = certificate.get("raw_four_port_quartets")
    current = certificate.get("current_raw4_summary")
    summary_relative = (
        "work/corrected_composite_ledgers/artifacts/"
        "raw4_corrected_composite_summary.json"
    )
    if (
        not isinstance(raw, dict)
        or raw.get("raw_directions") != 405_216
        or raw.get("quartet_exclusions") != 360_408
        or not isinstance(current, dict)
        or current.get("summary_path") != summary_relative
        or current.get("total_rows") != 405_216
        or current.get("displayed_quartet_exclusions") != 360_408
        or current.get("forbidden_rooted_fields") != 0
        or current.get("forbidden_rooted_reasons") != 0
    ):
        fail("C02 direction certificate census or authority drift")
    summary_path = project_path(summary_relative)
    summary = object_from_path(summary_path, "current raw-four composite summary")
    if (
        current.get("summary_sha256") != sha256_bytes(summary_path.read_bytes())
        or current.get("summary_payload_sha256") != summary.get("payload_sha256")
    ):
        fail("C02 current raw-four summary binding drift")


def verify_crosswalk(
    frozen: dict[str, dict[str, int | str]],
    submission: dict[str, dict[str, int | str]],
    expected_runtime: dict[str, Any],
    lock_sha256: str,
    lock_payload_sha256: str,
) -> None:
    relative = "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json"
    if relative not in submission:
        fail("crosswalk JSON omitted from submission ledger")
    crosswalk = object_from_path(project_path(relative), "theorem artifact crosswalk")
    if crosswalk.get("schema") != "k2p-theorem-artifact-reproducibility-crosswalk-v2":
        fail("crosswalk schema mismatch")
    if crosswalk.get("status") != "PASS_PC_PARTIAL":
        fail("crosswalk status mismatch")
    payload = crosswalk.get("payload_sha256")
    unsigned = dict(crosswalk)
    unsigned.pop("payload_sha256", None)
    if not isinstance(payload, str) or payload != canonical_hash(unsigned):
        fail("crosswalk payload mismatch")
    if crosswalk.get("submission_metadata") != SUBMISSION_METADATA:
        fail("crosswalk submission metadata drift")
    if "pending_human_metadata" in crosswalk:
        fail("crosswalk retains a stale pending-human field")
    expected_frozen_release = {
        "candidate_outcome": "K2P-SAME",
        "content_ledger_root_sha256": canonical_hash(frozen),
        "file_count_including_release_lock": len(frozen),
        "release_lock_path": LOCK_RELATIVE,
        "release_lock_payload_sha256": lock_payload_sha256,
        "release_lock_sha256": lock_sha256,
        "total_bytes_including_release_lock": sum(
            int(row["bytes"]) for row in frozen.values()
        ),
    }
    if crosswalk.get("frozen_release") != expected_frozen_release:
        fail("crosswalk frozen release boundary mismatch")
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
    claims_by_id: dict[str, dict[str, Any]] = {}
    claim_paths: dict[str, set[str]] = {}
    for claim in claims:
        if not isinstance(claim, dict) or not required_fields.issubset(claim):
            fail("crosswalk claim is missing a required field")
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or claim_id in seen:
            fail("duplicate or malformed crosswalk claim ID")
        seen.add(claim_id)
        claims_by_id[claim_id] = claim
        claim_paths[claim_id] = set()
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
                claim_paths[claim_id].add(path)
        runtime = claim.get("runtime")
        if not isinstance(runtime, dict) or runtime.get("status") not in {"unknown", "component_observation_only", "clean_full_replay"}:
            fail(f"malformed runtime boundary: {claim_id}")
        if runtime.get("status") == "clean_full_replay":
            expected_claim_runtime = {
                "end_to_end_seconds": expected_runtime["end_to_end_full_runtime_seconds"],
                "status": "clean_full_replay",
                "clean_detached_checkout": True,
                "git_commit": expected_runtime["git_commit"],
                "internal_elapsed_seconds": expected_runtime["internal_elapsed_seconds"],
                "layer_count": expected_runtime["layer_count"],
                "maximum_resident_set_size_bytes": expected_runtime["maximum_resident_set_size_bytes"],
                "peak_memory_footprint_bytes": expected_runtime["peak_memory_footprint_bytes"],
                "report_path": expected_runtime["report_path"],
                "report_sha256": expected_runtime["report_sha256"],
                "telemetry_path": expected_runtime["telemetry_path"],
                "telemetry_sha256": expected_runtime["telemetry_sha256"],
            }
            if claim_id != "C11-global-K2P-SAME-and-reconstruction" or runtime != expected_claim_runtime:
                fail(f"malformed clean full runtime: {claim_id}")
            for path_key, sha_key in (("report_path", "report_sha256"), ("telemetry_path", "telemetry_sha256")):
                path = runtime.get(path_key)
                if path not in OPERATIONAL_EVIDENCE or submission.get(path, {}).get("sha256") != runtime.get(sha_key):
                    fail(f"unbound clean full runtime artifact: {claim_id}:{path_key}")
        elif runtime.get("end_to_end_seconds") is not None:
            fail(f"unsupported inferred end-to-end runtime: {claim_id}")

    required_claim_paths = {
        "C02-quartet-tree-of-blobs": {
            "work/adversarial_proof_review/topology_direction_certificate.json",
            "work/adversarial_proof_review/verify_topology_direction.py",
            "work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json",
            "work/quartet_separation_closure/quartet_logic_certificate.json",
            "work/quartet_separation_closure/quartet_semantics_mutation_certificate.json",
            "work/quartet_separation_closure/quartet_terminal_binding_certificate.json",
            "work/quartet_separation_closure/quartet_terminal_binding_mutation_certificate.json",
            "work/quartet_separation_closure/verify_quartet_terminal_bindings.py",
        },
        "C03-bridge-marginal-local-product": {
            "work/canonicalizer_completeness/inheritance_transport/parameter_transport_certificate.json",
            "work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py",
            "work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py",
            "work/canonicalizer_completeness/inheritance_transport/parameter_transport_mutation_report.json",
        },
        "C04-primitive-grammar-and-completion-count": {
            "work/canonicalizer_completeness/PROOF.md",
            "work/canonicalizer_completeness/canonicalizer_completeness_certificate.json",
            "work/canonicalizer_completeness/canonicalizer_completeness_mutation_certificate.json",
            "work/canonicalizer_completeness/verify_canonicalizer_completeness.py",
        },
        "C05-raw-four-rank-filter": {
            "work/rank_upper_certificates/verify_rank_upper_certificates.py",
            "work/rank_upper_certificates/syzygy_upper.py",
            "work/rank_upper_certificates/mutation_tests.py",
            "work/rank_upper_certificates/mutation_report.json",
        },
        "C06-direct-separator-families": {
            "package/referee/k2p_offline_sweep_portable/test_direct_closure_release_mutations.py",
            "package/referee/k2p_offline_sweep_portable/direct_closure_mutation_report.json",
        },
        "C08-restoration-forest": {
            "work/canonicalizer_completeness/inheritance_transport/parameter_transport_certificate.json",
            "work/canonicalizer_completeness/inheritance_transport/restoration_restriction_parameter_transports.jsonl.gz",
        },
        "C09-coherent-probe-word-reconstruction": {
            "work/canonicalizer_completeness/inheritance_transport/parameter_transport_certificate.json",
            "work/canonicalizer_completeness/inheritance_transport/probe_relation_parameter_transports.jsonl.gz",
            "work/canonicalizer_completeness/inheritance_transport/probe_restriction_parameter_transports.jsonl.gz",
        },
        "C11-global-K2P-SAME-and-reconstruction": {"LICENSES.md"},
        "C13-weak-class-sharpness": {
            "work/weak_sharpness_audit/test_mutations.py",
            "work/weak_sharpness_audit/mutation_report.json",
        },
    }
    for claim_id, required in required_claim_paths.items():
        missing = sorted(required - claim_paths.get(claim_id, set()))
        if missing:
            fail(f"crosswalk omits new exact evidence {claim_id}:{missing}")

    verify_c02_scope(claims_by_id["C02-quartet-tree-of-blobs"])

    profile = crosswalk.get("environment_profiles", {}).get("frozen-python-k2p-v1")
    if (
        not isinstance(profile, dict)
        or profile.get("optimized_python") != "forbidden"
        or profile.get("end_to_end_quick_runtime_seconds") is not None
        or profile.get("end_to_end_full_runtime_seconds")
        != expected_runtime["end_to_end_full_runtime_seconds"]
        or profile.get("full_replay_internal_elapsed_seconds")
        != expected_runtime["internal_elapsed_seconds"]
        or profile.get("full_replay_layer_count") != expected_runtime["layer_count"]
        or profile.get("full_replay_maximum_resident_set_size_bytes")
        != expected_runtime["maximum_resident_set_size_bytes"]
        or profile.get("full_replay_peak_memory_footprint_bytes")
        != expected_runtime["peak_memory_footprint_bytes"]
    ):
        fail("crosswalk environment/runtime profile mismatch")
    requirements = profile.get("requirements")
    if (
        not isinstance(requirements, dict)
        or requirements.get("path") != "work/final_theorem_release/requirements.txt"
        or frozen.get(requirements.get("path"), {}).get("sha256")
        != requirements.get("sha256")
        or frozen.get(requirements.get("path"), {}).get("bytes")
        != requirements.get("bytes")
    ):
        fail("crosswalk environment requirements binding mismatch")

    quartet_path = project_path(
        "work/quartet_separation_closure/quartet_logic_certificate.json"
    )
    quartet = object_from_path(quartet_path, "quartet semantics certificate")
    if (
        quartet.get("schema") != "k2p-displayed-quartet-semantics-v2"
        or quartet.get("status") != "PASS"
        or quartet.get("character_order") != ["0", "C", "G", "T"]
        or quartet.get("edge_spectrum") != ["1", "s", "g", "s"]
        or quartet.get("canonical_formula_count") != 6
        or quartet.get("formula_transport_count") != 288
        or quartet.get("unequal_pair_count") != 21
    ):
        fail("quartet semantics certificate census/convention mismatch")
    spec_path = project_path("work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json")
    if quartet.get("spec_sha256") != sha256_bytes(spec_path.read_bytes()):
        fail("quartet semantics spec binding mismatch")
    quartet_mutation = object_from_path(
        project_path("work/quartet_separation_closure/quartet_semantics_mutation_certificate.json"),
        "quartet semantics mutation certificate",
    )
    if (
        quartet_mutation.get("schema") != "k2p-quartet-semantics-mutations-v4"
        or quartet_mutation.get("status") != "PASS"
        or quartet_mutation.get("case_count") != 8
        or quartet_mutation.get("survived") != 0
        or quartet_mutation.get("spec_sha256") != sha256_bytes(spec_path.read_bytes())
        or quartet_mutation.get("mutation_runner_sha256")
        != sha256_bytes(
            project_path(
                "work/quartet_separation_closure/test_quartet_semantics_mutations.py"
            ).read_bytes()
        )
        or quartet_mutation.get("production_verifier_sha256")
        != sha256_bytes(
            project_path(
                "work/quartet_separation_closure/verify_quartet_logic.py"
            ).read_bytes()
        )
        or quartet_mutation.get("source_certificate_sha256")
        != sha256_bytes(quartet_path.read_bytes())
        or quartet_mutation.get("clean_baseline", {}).get("verifier_exit_code")
        != 0
        or quartet_mutation.get("clean_baseline", {}).get(
            "success_artifact_byte_identical_to_stored"
        ) is not True
        or quartet_mutation.get("source_fingerprints_unchanged") is not True
        or quartet_mutation.get("qualification_negative_controls")
        != {
            "import_error_not_qualified": True,
            "import_failure_stale_pass_removed_before_failure": True,
            "non_one_exit_not_qualified": True,
            "optimized_mode_stale_pass_removed_before_rejection": True,
            "pass_token_not_qualified": True,
            "preexisting_pass_artifact_not_qualified": True,
            "signal_not_qualified": True,
            "timeout_not_qualified": True,
            "traceback_not_qualified": True,
            "wrong_diagnostic_not_qualified": True,
        }
        or quartet_mutation.get("execution_contract")
        != {
            "absolute_paths_recorded": False,
            "atomic_output_publication": True,
            "authoritative_output_requires_exact_override": True,
            "clean_baseline_required": True,
            "exact_full_diagnostic_and_exception_type_required": True,
            "return_code_one_required": True,
            "routine_output_caller_owned_external": True,
            "runtime_fields_recorded": False,
            "stale_output_removed_before_optimized_and_import_work": True,
            "success_tokens_and_artifacts_rejected": True,
            "traceback_import_timeout_signal_non_one_rejected": True,
        }
        or not isinstance(quartet_mutation.get("cases"), list)
        or len(quartet_mutation["cases"]) != 8
        or any(
            not isinstance(row, dict)
            or row.get("observed_semantic_diagnostic")
            != row.get("expected_semantic_diagnostic")
            or row.get("semantic_diagnostic_matched") is not True
            or row.get("verifier_exit_code") != 1
            or row.get("success_artifact_created") is not False
            or row.get("traceback_observed") is not False
            or row.get("import_failure_observed") is not False
            or row.get("success_token_observed") is not False
            or row.get("rejected") is not True
            or row.get("status") != "REJECTED"
            for row in quartet_mutation["cases"]
        )
    ):
        fail("quartet semantics mutation binding mismatch")
    terminal = object_from_path(
        project_path("work/quartet_separation_closure/quartet_terminal_binding_certificate.json"),
        "quartet terminal binding certificate",
    )
    if (
        terminal.get("schema") != "k2p-quartet-terminal-binding-v1"
        or terminal.get("status") != "PASS"
        or terminal.get("aggregate", {}).get("quartet_terminal_rows") != 4_414_710
        or terminal.get("aggregate", {}).get("per_layer_certificate_ids") != 888
        or terminal.get("aggregate", {}).get("missing_references") != 0
        or terminal.get("aggregate", {}).get("dangling_certificates") != 0
    ):
        fail("quartet terminal binding census mismatch")
    quartet_path = project_path("work/quartet_separation_closure/quartet_logic_certificate.json")
    if terminal.get("semantics_certificate", {}).get("sha256") != sha256_bytes(quartet_path.read_bytes()):
        fail("quartet terminal semantics binding mismatch")
    terminal_mutation = object_from_path(
        project_path("work/quartet_separation_closure/quartet_terminal_binding_mutation_certificate.json"),
        "quartet terminal mutation certificate",
    )
    if (
        terminal_mutation.get("schema") != "k2p-quartet-terminal-binding-mutations-v2"
        or terminal_mutation.get("status") != "PASS"
        or terminal_mutation.get("case_count") != 12
        or terminal_mutation.get("survived") != 0
        or terminal_mutation.get("semantics_certificate_sha256")
        != sha256_bytes(quartet_path.read_bytes())
        or terminal_mutation.get("mutation_runner_sha256")
        != sha256_bytes(
            project_path(
                "work/quartet_separation_closure/"
                "test_quartet_terminal_binding_mutations.py"
            ).read_bytes()
        )
        or terminal_mutation.get("binder_sha256")
        != sha256_bytes(
            project_path(
                "work/quartet_separation_closure/verify_quartet_terminal_bindings.py"
            ).read_bytes()
        )
        or terminal_mutation.get("source_certificate_sha256")
        != sha256_bytes(
            project_path(
                "work/quartet_separation_closure/"
                "quartet_terminal_binding_certificate.json"
            ).read_bytes()
        )
        or terminal_mutation.get("clean_baseline", {}).get(
            "quartet_terminal_rows"
        ) != 4_414_710
        or terminal_mutation.get("clean_baseline", {}).get(
            "success_artifact_byte_identical_to_stored"
        ) is not True
        or terminal_mutation.get("source_fingerprints_unchanged") is not True
        or terminal_mutation.get("qualification_negative_controls")
        != {
            "helper_stale_pass_removed_before_import": True,
            "import_error_not_qualified": True,
            "missing_binder_stale_pass_removed_before_failure": True,
            "non_one_exit_not_qualified": True,
            "optimized_mode_stale_pass_removed_before_rejection": True,
            "pass_token_not_qualified": True,
            "preexisting_pass_artifact_not_qualified": True,
            "signal_not_qualified": True,
            "timeout_not_qualified": True,
            "traceback_not_qualified": True,
            "wrong_diagnostic_not_qualified": True,
        }
        or terminal_mutation.get("execution_contract")
        != {
            "absolute_paths_recorded": False,
            "atomic_output_publication": True,
            "authoritative_output_requires_exact_override": True,
            "clean_baseline_required": True,
            "exact_full_diagnostic_and_exception_type_required": True,
            "return_code_one_required": True,
            "routine_output_caller_owned_external": True,
            "runtime_fields_recorded": False,
            "stale_output_removed_before_optimized_and_import_work": True,
            "success_tokens_and_artifacts_rejected": True,
            "traceback_import_timeout_signal_non_one_rejected": True,
        }
        or any(
            row.get("status") != "REJECTED" or row.get("rejected") is not True
            for row in terminal_mutation.get("cases", [])
        )
    ):
        fail("quartet terminal mutation binding mismatch")
    canonicalizer = object_from_path(
        project_path("work/canonicalizer_completeness/canonicalizer_completeness_certificate.json"),
        "canonicalizer completeness certificate",
    )
    if (
        canonicalizer.get("schema") != "k2p-canonicalizer-completeness-v1"
        or canonicalizer.get("status") != "PASS"
        or canonicalizer.get("descriptor_audit", {}).get("primitive_archetypes_compared") != 10_084
        or canonicalizer.get("descriptor_audit", {}).get("slow_fast_disagreements") != 0
        or canonicalizer.get("relation_audit", {}).get("rank_and_topology_eligible_presentations") != 4_012
        or canonicalizer.get("relation_audit", {}).get("disagreements") != 0
    ):
        fail("canonicalizer completeness census mismatch")
    canonicalizer_mutation = object_from_path(
        project_path("work/canonicalizer_completeness/canonicalizer_completeness_mutation_certificate.json"),
        "canonicalizer completeness mutation certificate",
    )
    canonicalizer_mutation_runner = project_path(
        "work/canonicalizer_completeness/test_canonicalizer_mutations.py"
    )
    canonicalizer_diagnostics = {
        "accept_nonordinary_split_heads": "CANONICALIZER_COMPLETENESS_FAIL:NONORDINARY_ATLAS_ACCEPTED",
        "erase_without_marking_selected_triangle": "CANONICALIZER_COMPLETENESS_FAIL:SELECTED_TRIANGLE_ATLAS_ACCEPTED: triangle",
    }
    canonicalizer_baseline = canonicalizer_mutation.get("clean_baseline", {})
    canonicalizer_rows = canonicalizer_mutation.get("mutations", [])
    if (
        canonicalizer_mutation.get("schema") != "k2p-canonicalizer-completeness-mutations-v2"
        or canonicalizer_mutation.get("status") != "PASS"
        or canonicalizer_mutation.get("rejected") != 2
        or canonicalizer_mutation.get("survived") != 0
        or canonicalizer_mutation.get("atlas_sha256")
        != canonicalizer.get("inputs", {}).get("atlas_sha256")
        or canonicalizer_mutation.get("mutation_runner_sha256")
        != sha256_bytes(canonicalizer_mutation_runner.read_bytes())
        or canonicalizer_mutation.get("diagnostic_contract")
        != canonicalizer_diagnostics
        or canonicalizer_baseline.get("returncode") != 0
        or canonicalizer_baseline.get("status") != "PASS"
        or canonicalizer_baseline.get("mode") != "semantic-only"
        or canonicalizer_baseline.get("artifact_contract")
        != (
            "The semantic-only auditor reports PASS on stdout and intentionally "
            "must not create the supplied --output success artifact."
        )
        or canonicalizer_baseline.get("success_artifact_absent") is not True
        or canonicalizer_baseline.get("timeout") is not False
        or canonicalizer_baseline.get("signal") is not False
        or canonicalizer_baseline.get("semantic_mutation_contract")
        != canonicalizer.get("semantic_mutation_contract")
        or [row.get("name") for row in canonicalizer_rows]
        != list(canonicalizer_diagnostics)
    ):
        fail("canonicalizer completeness mutation binding mismatch")
    mutated_atlas_hashes = [row.get("mutated_atlas_sha256") for row in canonicalizer_rows]
    if (
        not all(
            isinstance(value, str)
            and re.fullmatch(r"[0-9a-f]{64}", value)
            and value != canonicalizer_mutation.get("atlas_sha256")
            for value in mutated_atlas_hashes
        )
        or len(set(mutated_atlas_hashes)) != 2
        or not all(
            row.get("rejected") is True
            and row.get("exit_code") == 1
            and row.get("expected_diagnostic") == canonicalizer_diagnostics[row["name"]]
            and row.get("observed_diagnostic") == canonicalizer_diagnostics[row["name"]]
            and row.get("success_artifact_absent") is True
            and row.get("timeout") is False
            and row.get("signal") is False
            for row in canonicalizer_rows
        )
    ):
        fail("canonicalizer mutation semantic diagnostic binding mismatch")
    parameter = object_from_path(
        project_path("work/canonicalizer_completeness/inheritance_transport/parameter_transport_certificate.json"),
        "parameter transport certificate",
    )
    if (
        parameter.get("schema") != "k2p_graph_derived_parameter_transport_certificate_v1"
        or parameter.get("status") != "PASS"
        or parameter.get("closure", {}).get("all_exact_transport_records_used") != 67_741
        or parameter.get("closure", {}).get("all_frozen_parent_restriction_records_used") != 4_379
        or parameter.get("closure", {}).get("restoration_canonical_parents") != 997
        or parameter.get("closure", {}).get("unresolved_parameter_transports") != 0
        or parameter.get("ledgers", {}).get("probe_relations", {}).get("rows") != 67_741
        or parameter.get("ledgers", {}).get("probe_restrictions", {}).get("rows") != 71_022
        or parameter.get("ledgers", {}).get("restoration_restrictions", {}).get("rows") != 5_540
    ):
        fail("graph-derived parameter transport census mismatch")
    parameter_base = PurePosixPath(
        "work/canonicalizer_completeness/inheritance_transport"
    )
    for ledger_name, row in parameter.get("ledgers", {}).items():
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            fail(f"graph-derived parameter ledger row malformed: {ledger_name}")
        relative = (parameter_base / safe_relative(row["path"])).as_posix()
        if (
            frozen.get(relative, {}).get("sha256") != row.get("sha256")
            or frozen.get(relative, {}).get("bytes") != row.get("bytes")
        ):
            fail(f"graph-derived parameter ledger binding mismatch: {ledger_name}")
    parameter_mutation = object_from_path(
        project_path("work/canonicalizer_completeness/inheritance_transport/parameter_transport_mutation_report.json"),
        "parameter transport mutation report",
    )
    parameter_mutation_runner = project_path(
        "work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py"
    )
    parameter_verifier = project_path(
        "work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py"
    )
    parameter_mutation_unsigned = dict(parameter_mutation)
    parameter_mutation_payload = parameter_mutation_unsigned.pop("payload_sha256", None)
    parameter_cases = parameter_mutation.get("cases")
    parameter_names = [
        "required_complement_removed",
        "illicit_complement_injected",
        "parent_order_reversal_unpaired",
        "triangle_reticulation_false_affine_map",
        "triangle_edge_false_product_map",
        "restriction_complement_removed",
        "serial_product_factor_omitted",
        "paired_s_g_action_broken",
        "root_suppressed_incoming_incidence_hidden",
        "source_target_reversal_without_inverse_transport",
    ]
    parameter_full_diagnostics = {
        name: (
            "PARAMETER_TRANSPORT_REPLAY_FAIL:rederived bytes:"
            "parameter_transport_certificate.json"
        )
        for name in (
            "triangle_edge_false_product_map",
            "serial_product_factor_omitted",
            "root_suppressed_incoming_incidence_hidden",
            "source_target_reversal_without_inverse_transport",
        )
    }
    parameter_local_diagnostics = {
        "required_complement_removed": "required_complement_removed:flip flag",
        "illicit_complement_injected": "illicit_complement_injected:flip flag",
        "parent_order_reversal_unpaired": "parent_order_reversal_unpaired:flip flag",
        "triangle_reticulation_false_affine_map": (
            "triangle_reticulation_false_affine_map:triangle-local census"
        ),
        "restriction_complement_removed": "restriction_complement_removed:flip flag",
        "paired_s_g_action_broken": "paired_s_g_action_broken:paired products",
    }
    if (
        parameter_mutation.get("schema") != "k2p_parameter_transport_mutations_v2"
        or parameter_mutation.get("status") != "PASS"
        or parameter_mutation_payload != canonical_hash(parameter_mutation_unsigned)
        or parameter_mutation.get("rejected") != 10
        or parameter_mutation.get("survived") != 0
        or parameter_mutation.get("complete_production_verifier_attacks") != 4
        or parameter_mutation.get("exact_local_semantic_attacks") != 6
        or parameter_mutation.get("certificate_payload_sha256") != parameter.get("payload_sha256")
        or parameter_mutation.get("mutation_runner_sha256")
        != sha256_bytes(parameter_mutation_runner.read_bytes())
        or parameter_mutation.get("production_verifier_sha256")
        != sha256_bytes(parameter_verifier.read_bytes())
        or parameter_mutation.get("source_fingerprints_unchanged") is not True
        or parameter_mutation.get("qualification_negative_controls")
        != {
            "failure_output_with_pass_token_not_qualified": True,
            "optimized_mode_stale_pass_removed_before_rejection": True,
            "signal_or_non_one_exit_not_qualified": True,
            "stale_pass_output_removed_before_work": True,
            "timeout_not_qualified": True,
            "unrelated_traceback_not_qualified": True,
            "wrong_diagnostic_not_qualified": True,
        }
        or parameter_mutation.get("clean_baseline")
        != {
            "authoritative_certificate_file_sha256": sha256_bytes(
                project_path(
                    "work/canonicalizer_completeness/inheritance_transport/parameter_transport_certificate.json"
                ).read_bytes()
            ),
            "authoritative_certificate_payload_sha256": parameter.get(
                "payload_sha256"
            ),
            "authoritative_certificate_unmodified": True,
            "authoritative_certificate_verified_in_place": True,
            "authoritative_input_binding_count": 16,
            "authoritative_input_bindings_current": True,
            "authoritative_ledger_count": 3,
            "full_primitive_regeneration": True,
            "pass_token_count": 1,
            "production_verifier_invoked": True,
            "status": "PASS",
            "verifier_exit_code": 0,
        }
        or not isinstance(parameter_cases, list)
        or [row.get("name") for row in parameter_cases] != parameter_names
    ):
        fail("graph-derived parameter transport mutation binding mismatch")
    for row in parameter_cases:
        name = row["name"]
        if name in parameter_full_diagnostics:
            if (
                row.get("test_type") != "complete_disposable_ledger_and_certificate_attack"
                or row.get("complete_mutant_ledger_created") is not True
                or row.get("complete_mutant_certificate_created") is not True
                or row.get("complete_mutant_ledger_coherently_resealed") is not True
                or row.get("mutant_structural_validation_passed") is not True
                or row.get("full_primitive_regeneration_invoked") is not True
                or row.get("production_verifier_invoked") is not True
                or row.get("production_verifier_sha256")
                != sha256_bytes(parameter_verifier.read_bytes())
                or row.get("verifier_exit_code") != 1
                or row.get("expected_semantic_diagnostic") != parameter_full_diagnostics[name]
                or row.get("observed_semantic_diagnostic") != parameter_full_diagnostics[name]
                or row.get("semantic_diagnostic_matched") is not True
                or row.get("success_token_observed") is not False
                or row.get("traceback_observed") is not False
                or row.get("rejected") is not True
                or row.get("status") != "REJECTED"
                or not isinstance(row.get("mutated_ledger_bytes"), int)
                or row["mutated_ledger_bytes"] <= 0
                or not re.fullmatch(r"[0-9a-f]{64}", str(row.get("mutated_ledger_sha256")))
                or not re.fullmatch(
                    r"[0-9a-f]{64}", str(row.get("mutated_certificate_payload_sha256"))
                )
            ):
                fail(f"parameter transport complete mutation evidence mismatch:{name}")
        elif name in parameter_local_diagnostics:
            if (
                row.get("test_type") != "exact_local_semantic_validator_attack"
                or row.get("complete_mutant_ledger_created") is not False
                or row.get("production_verifier_invoked") is not False
                or row.get("expected_semantic_diagnostic") != parameter_local_diagnostics[name]
                or row.get("observed_semantic_diagnostic") != parameter_local_diagnostics[name]
                or row.get("semantic_diagnostic_matched") is not True
                or row.get("rejected") is not True
                or row.get("status") != "REJECTED"
            ):
                fail(f"parameter transport local mutation evidence mismatch:{name}")
        else:
            fail(f"unexpected parameter transport mutation:{name}")
    rank_mutation = object_from_path(
        project_path("work/rank_upper_certificates/mutation_report.json"),
        "rank-upper mutation report",
    )
    rank_results = rank_mutation.get("results")
    rank_runner = project_path("work/rank_upper_certificates/mutation_tests.py")
    rank_verifier = project_path(
        "work/rank_upper_certificates/verify_rank_upper_certificates.py"
    )
    rank_unsigned = dict(rank_mutation)
    rank_payload = rank_unsigned.pop("payload_sha256", None)
    rank_expected = (
        "K2P_RANK_UPPER_REPLAY_FAIL:"
        "RANK_UPPER_SYMBOLIC_FIELD_DIMENSION_FAIL:orbit=0:observed=4:required=6"
    )
    rank_names = [
        "omitted_descriptor_coverage",
        "duplicated_descriptor_coverage",
        "altered_syzygy_coefficient",
        "reassigned_representative_certificate",
        "broken_port_transport",
        "false_rank_upper_claim",
        "sampled_rank_substituted_for_symbolic_upper",
    ]
    rank_helper_expected = {
        "omitted_descriptor_coverage": {
            "error_type": "AssertionError",
            "diagnostic": "coverage count mismatch",
        },
        "duplicated_descriptor_coverage": {
            "error_type": "AssertionError",
            "diagnostic": "descriptor index mismatch",
        },
        "altered_syzygy_coefficient": {
            "error_type": "AssertionError",
            "diagnostic": "(1, 2, ((0, 0, 1, 0, 1, 0, 1, 0, 2, 0, 2, 0, 0, 1), 1))",
        },
        "reassigned_representative_certificate": {
            "error_type": "AssertionError",
            "diagnostic": "representative digest mismatch",
        },
        "broken_port_transport": {
            "error_type": "AssertionError",
            "diagnostic": "broken port transport",
        },
        "false_rank_upper_claim": {
            "error_type": "AssertionError",
            "diagnostic": "claimed 7, exact certificate 8",
        },
    }
    sampled_rows = [
        row for row in rank_results or []
        if isinstance(row, dict)
        and row.get("mutation") == "sampled_rank_substituted_for_symbolic_upper"
    ]
    if (
        rank_mutation.get("schema") != "k2p-rank-upper-adversarial-mutations-v2"
        or rank_mutation.get("status") != "pass"
        or rank_payload != canonical_hash(rank_unsigned)
        or rank_mutation.get("mutation_count") != 7
        or rank_mutation.get("complete_production_verifier_attacks") != 1
        or rank_mutation.get("survivors") != 0
        or rank_mutation.get("helper_expected_diagnostics")
        != rank_helper_expected
        or rank_mutation.get("mutation_runner_sha256")
        != sha256_bytes(rank_runner.read_bytes())
        or rank_mutation.get("production_verifier_sha256")
        != sha256_bytes(rank_verifier.read_bytes())
        or rank_mutation.get("source_fingerprints_unchanged") is not True
        or rank_mutation.get("qualification_negative_controls")
        != {
            "failure_output_with_pass_token_not_qualified": True,
            "optimized_mode_stale_pass_removed_before_rejection": True,
            "runner_missing_dependency_stale_pass_removed_before_import_failure": True,
            "signal_or_non_one_exit_not_qualified": True,
            "stale_pass_output_removed_before_work": True,
            "timeout_not_qualified": True,
            "unrelated_traceback_not_qualified": True,
            "wrong_diagnostic_not_qualified": True,
            "wrong_helper_diagnostic_not_qualified": True,
            "wrong_helper_exception_type_not_qualified": True,
        }
        or rank_mutation.get("production_output_policy_negative_controls")
        != {
            "certificate_input_collision_rejected": True,
            "hardlink_output_rejected": True,
            "symlink_output_rejected": True,
            "verifier_optimized_mode_stale_pass_removed_before_rejection": True,
            "verifier_missing_dependency_stale_pass_removed_before_import_failure": True,
        }
        or rank_mutation.get("clean_baseline", {}).get("authoritative_package_verified_in_place") is not True
        or rank_mutation.get("clean_baseline", {}).get("authoritative_package_unmodified") is not True
        or rank_mutation.get("clean_baseline", {}).get("authoritative_manifest_verified") is not True
        or rank_mutation.get("clean_baseline", {}).get("authoritative_manifest_file_count") != 94
        or not re.fullmatch(
            r"[0-9a-f]{64}",
            str(rank_mutation.get("clean_baseline", {}).get("authoritative_manifest_aggregate_sha256")),
        )
        or rank_mutation.get("clean_baseline", {}).get("authoritative_sha256_manifest_sha256")
        != sha256_bytes(project_path("work/rank_upper_certificates/MANIFEST.sha256").read_bytes())
        or rank_mutation.get("clean_baseline", {}).get("authoritative_json_manifest_sha256")
        != sha256_bytes(project_path("work/rank_upper_certificates/manifest.json").read_bytes())
        or rank_mutation.get("clean_baseline", {}).get("production_verifier_invoked") is not True
        or rank_mutation.get("clean_baseline", {}).get("full_symbolic_base_recompute") is not True
        or rank_mutation.get("clean_baseline", {}).get("descriptor_count") != 4_379
        or rank_mutation.get("clean_baseline", {}).get("zero_unresolved") is not True
        or rank_mutation.get("clean_baseline", {}).get("base_recomputed") is not True
        or rank_mutation.get("clean_baseline", {}).get("stored_authoritative_replay_byte_identical") is not True
        or rank_mutation.get("clean_baseline", {}).get("stored_authoritative_replay_sha256")
        != sha256_bytes(project_path("work/rank_upper_certificates/rank_upper_replay.json").read_bytes())
        or rank_mutation.get("clean_baseline", {}).get("verifier_exit_code") != 0
        or rank_mutation.get("clean_baseline", {}).get("success_artifact_created") is not True
        or rank_mutation.get("clean_baseline", {}).get("pass_token_count") != 1
        or rank_mutation.get("clean_baseline", {}).get("status") != "pass"
        or not isinstance(rank_results, list)
        or not all(isinstance(row, dict) for row in rank_results)
        or [row.get("mutation") for row in rank_results] != rank_names
        or len(sampled_rows) != 1
    ):
        fail("rank-upper sampled-substitution mutation was not rejected")
    sampled = sampled_rows[0]
    if not all(
        row.get("test_type") == "focused_exact_helper_attack"
        and row.get("production_verifier_invoked") is False
        and row.get("status") == "rejected"
        and row.get("rejected") is True
        and row.get("error")
        == rank_helper_expected[row["mutation"]]["diagnostic"]
        and row.get("expected_error_type")
        == rank_helper_expected[row["mutation"]]["error_type"]
        and row.get("observed_error_type")
        == rank_helper_expected[row["mutation"]]["error_type"]
        and row.get("expected_diagnostic")
        == rank_helper_expected[row["mutation"]]["diagnostic"]
        and row.get("observed_diagnostic")
        == rank_helper_expected[row["mutation"]]["diagnostic"]
        and row.get("diagnostic_matched") is True
        for row in rank_results[:-1]
    ):
        fail("rank-upper focused helper mutation evidence mismatch")
    if (
        sampled.get("test_type") != "complete_disposable_rank_certificate_package_attack"
        or sampled.get("complete_mutant_package_created") is not True
        or sampled.get("mutated_certificate") != "exception_syzygies/orbit_000.json"
        or sampled.get("mutant_manifest_file_count") != 94
        or sampled.get("sampled_evidence_cannot_prove_global_upper_bound") is not True
        or sampled.get("production_verifier_invoked") is not True
        or sampled.get("production_verifier_sha256")
        != sha256_bytes(rank_verifier.read_bytes())
        or sampled.get("verifier_exit_code") != 1
        or sampled.get("expected_semantic_diagnostic") != rank_expected
        or sampled.get("observed_semantic_diagnostic") != rank_expected
        or sampled.get("semantic_diagnostic_matched") is not True
        or sampled.get("preexisting_canonical_success_artifact_present") is not True
        or sampled.get("preexisting_canonical_success_artifact_sha256")
        != sha256_bytes(project_path("work/rank_upper_certificates/rank_upper_replay.json").read_bytes())
        or sampled.get("canonical_success_artifact_removed_before_mutant_work") is not True
        or sampled.get("success_artifact_created") is not False
        or sampled.get("traceback_observed") is not False
        or sampled.get("status") != "rejected"
        or sampled.get("rejected") is not True
        or not re.fullmatch(
            r"[0-9a-f]{64}", str(sampled.get("original_certificate_sha256"))
        )
        or not re.fullmatch(
            r"[0-9a-f]{64}", str(sampled.get("mutated_certificate_sha256"))
        )
        or sampled.get("original_certificate_sha256")
        == sampled.get("mutated_certificate_sha256")
    ):
        fail("rank-upper complete sampled-substitution evidence mismatch")


def verify_final_release_mutations() -> None:
    report = object_from_path(
        project_path(
            "proof_compression_submission/output/FINAL_RELEASE_MUTATIONS.json"
        ),
        "final release mutation report",
    )
    payload = report.get("payload_sha256")
    unsigned = dict(report)
    unsigned.pop("payload_sha256", None)
    rows = report.get("mutations")
    if (
        report.get("schema") != "k2p-principal-d-plus-final-release-mutations-v2"
        or report.get("status") != "PASS"
        or report.get("blockers") != []
        or report.get("required_mutation_count") != 25
        or report.get("observed_mutation_count") != 25
        or report.get("survivors") != 0
        or report.get("output_contract_preflight") != "PASS"
        or not isinstance(rows, list)
        or len(rows) != 25
        or any(row.get("status") != "REJECTED" for row in rows)
        or len({row.get("name") for row in rows}) != 25
        or not isinstance(payload, str)
        or payload != canonical_hash(unsigned)
    ):
        fail("final release mutation report mismatch")


def verify_pdf_build_report(submission: dict[str, dict[str, int | str]]) -> None:
    report = object_from_path(
        project_path("proof_compression_submission/PDF_BUILD_REPORT.json"),
        "PDF build report",
    )
    payload = report.get("payload_sha256")
    unsigned = dict(report)
    unsigned.pop("payload_sha256", None)
    if not isinstance(payload, str) or payload != canonical_hash(unsigned):
        fail("PDF build report payload mismatch")
    if (
        report.get("schema") != "k2p-submission-pdf-build-report-v3"
        or report.get("status") != "PASS"
        or report.get("visual_verdict") != "PASS"
        or report.get("source_date_epoch") != 1787702400
        or report.get("source_date_epoch_utc") != "2026-08-26T00:00:00Z"
        or report.get("engine") != {"name": "Tectonic", "version": "0.16.9"}
        or report.get("byte_identical_double_build") is not True
    ):
        fail("PDF build report schema/verdict mismatch")
    if report.get("source_set") != [
        "article/main.tex",
        "article/references.bib",
        "supplement/supplement.tex",
        "supplement/compression_tables.tex",
        "supplement/certificate_appendix.tex",
    ]:
        fail("PDF build source-set mismatch")
    checks = report.get("checks")
    if not isinstance(checks, dict) or checks.get("all_pages_visually_inspected") is not True or checks.get("all_fonts_embedded") is not True:
        fail("PDF visual/font checks are incomplete")
    for field in (
        "five_source_clean_build_passed",
        "missing_bibliography_manifest_mutation_rejected",
        "missing_certificate_appendix_build_rejected",
        "missing_compression_table_build_rejected",
    ):
        if checks.get(field) is not True:
            fail(f"PDF/source omission check did not pass: {field}")
    for field in ("fatal_latex_errors", "hyperref_pdf_string_warnings", "overfull_boxes", "undefined_citations", "undefined_references"):
        if checks.get(field) != 0:
            fail(f"nonzero PDF build defect count: {field}")
    for name in ("article", "supplement"):
        row = report.get(name)
        if not isinstance(row, dict):
            fail(f"missing PDF report row: {name}")
        pdf_path = row.get("pdf_path")
        source_path = row.get("source_path")
        if not isinstance(pdf_path, str) or not isinstance(source_path, str):
            fail(f"malformed PDF report paths: {name}")
        pdf_binding = submission.get(pdf_path)
        source_binding = submission.get(source_path)
        if not isinstance(pdf_binding, dict) or not isinstance(source_binding, dict):
            fail(f"unbundled PDF/source report path: {name}")
        if pdf_binding.get("sha256") != row.get("pdf_sha256") or pdf_binding.get("bytes") != row.get("bytes"):
            fail(f"PDF hash/byte report mismatch: {name}")
        if source_binding.get("sha256") != row.get("source_sha256"):
            fail(f"PDF source hash report mismatch: {name}")
        log_path = f"proof_compression_submission/output/logs/{'article' if name == 'article' else 'supplement'}.log"
        if submission.get(log_path, {}).get("sha256") != row.get("log_sha256"):
            fail(f"PDF log hash report mismatch: {name}")
        if checks.get(f"{name}_pages_inspected") != row.get("pages"):
            fail(f"PDF visual page census mismatch: {name}")


def verify_static_article_audit(
    submission: dict[str, dict[str, int | str]],
    expected_runtime: dict[str, Any],
    lock_sha256: str,
) -> None:
    relative = "proof_compression_submission/adversarial_review/STATIC_AUDIT_RESULT.json"
    if relative not in submission:
        fail("static article audit omitted from submission ledger")
    audit = object_from_path(project_path(relative), "static article audit")
    payload = audit.get("payload_sha256")
    unsigned = dict(audit)
    unsigned.pop("payload_sha256", None)
    if not isinstance(payload, str) or payload != canonical_hash(unsigned):
        fail("static article audit payload mismatch")
    expected_audit_metadata = {
        "corresponding_email": "me@aleckriebel.com",
        "author_contributions": "approved sole-author contribution statement",
        "funding": "No specific funding supported this work.",
        "competing_interests": "The author declares no competing interests.",
        "paper_and_data_license": "CC BY 4.0",
        "code_license": "MIT",
        "versioned_annotated_source_tag": "k2p-same-biorxiv-v1.0.3",
        "doi": None,
        "external_release_actions_performed": False,
    }
    if (
        audit.get("schema") != "k2p-submission-article-static-audit-v3"
        or audit.get("status") != "PASS"
        or audit.get("findings") != []
        or audit.get("submission_metadata") != expected_audit_metadata
        or audit.get("frozen_release_sha256") != lock_sha256
    ):
        fail("static article audit status/metadata mismatch")
    replay = audit.get("clean_full_replay", {})
    if (
        replay.get("layers") != expected_runtime["layer_count"]
        or replay.get("wall_seconds")
        != expected_runtime["end_to_end_full_runtime_seconds"]
        or replay.get("report_sha256") != expected_runtime["report_sha256"]
        or replay.get("telemetry_sha256") != expected_runtime["telemetry_sha256"]
    ):
        fail("static article audit replay binding mismatch")
    source_hashes = audit.get("source_sha256")
    expected_audit_sources = {
        "article/main.tex",
        "article/references.bib",
        "supplement/supplement.tex",
        "supplement/compression_tables.tex",
        "supplement/certificate_appendix.tex",
        "templates/PRINTED_CERTIFICATE_APPENDIX.json",
        "analysis/WEAK_SHARPNESS_COLUMN_CROSSWALK.json",
    }
    if not isinstance(source_hashes, dict) or set(source_hashes) != expected_audit_sources:
        fail("static article audit source map missing")
    for child, digest in source_hashes.items():
        path = f"proof_compression_submission/{child}"
        if submission.get(path, {}).get("sha256") != digest:
            fail(f"static article audit source binding mismatch: {child}")


def expected_runtime_boundary(
    lock_sha256: str, lock_payload_sha256: str
) -> dict[str, Any]:
    report_relative = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json"
    telemetry_relative = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"
    report_path = project_path(report_relative)
    telemetry_path = project_path(telemetry_relative)
    report = object_from_path(report_path, "clean full replay report")
    telemetry = object_from_path(telemetry_path, "clean full replay telemetry")
    report_sha256 = sha256_bytes(report_path.read_bytes())
    telemetry_sha256 = sha256_bytes(telemetry_path.read_bytes())
    layers = report.get("layer_replays")
    if (
        report.get("schema") != "k2p-principal-d-plus-final-theorem-replay-report-v1"
        or report.get("status") != "PASS"
        or report.get("promotion_ready") is not True
        or report.get("blockers")
        or report.get("mode") != "full"
        or not isinstance(layers, list)
        or not layers
        or report.get("lock_payload_sha256") != lock_payload_sha256
    ):
        fail("clean full replay report is not a bound promotion-ready PASS")
    if (
        telemetry.get("schema") != "k2p-final-clean-full-replay-telemetry-v1"
        or telemetry.get("status") != "PASS"
        or telemetry.get("clean_detached_checkout") is not True
        or telemetry.get("report", {}).get("sha256") != report_sha256
        or telemetry.get("report", {}).get("lock_payload_sha256") != lock_payload_sha256
    ):
        fail("clean full replay telemetry is incoherent")
    validate_telemetry_checkout_bindings(
        telemetry, lock_sha256, lock_payload_sha256
    )
    timing = telemetry.get("time_l")
    if not isinstance(timing, dict):
        fail("clean full replay timing object missing")
    for key in ("real_seconds", "maximum_resident_set_size_bytes", "peak_memory_footprint_bytes"):
        value = timing.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            fail(f"clean full replay timing field missing: {key}")
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
        "report_sha256": report_sha256,
        "telemetry_path": telemetry_relative,
        "telemetry_sha256": telemetry_sha256,
    }


def validate(manifest_path: Path) -> dict[str, Any]:
    reject_optimized_mode()
    verify_portable_builder_optimized_mode_contract()
    manifest = object_from_path(manifest_path, "revised referee manifest")
    if manifest.get("schema") != "k2p-revised-referee-bundle-manifest-v2":
        fail("manifest schema mismatch")
    if manifest.get("status") != "SUBMISSION_READY_PC_PARTIAL":
        fail("manifest status mismatch")
    payload = manifest.get("payload_sha256")
    unsigned = dict(manifest)
    unsigned.pop("payload_sha256", None)
    if not isinstance(payload, str) or payload != canonical_hash(unsigned):
        fail("manifest payload mismatch")
    if manifest.get("submission_metadata") != SUBMISSION_METADATA:
        fail("manifest submission metadata mismatch")
    if "pending_human_metadata" in manifest:
        fail("manifest retains a stale pending-human field")
    lock, lock_sha256, lock_payload_sha256 = release_context()
    frozen = reconstruct_frozen_bindings(lock, lock_sha256)
    submission = reconstruct_submission_bindings()
    expected_runtime = expected_runtime_boundary(
        lock_sha256, lock_payload_sha256
    )
    runtime = manifest.get("runtime_boundary")
    if runtime != expected_runtime:
        fail("manifest runtime boundary mismatch")
    check_ledger("frozen evidence", manifest.get("frozen_evidence"), frozen)
    check_ledger("submission sources", manifest.get("submission_sources"), submission)
    frozen_section = manifest["frozen_evidence"]
    if frozen_section.get("release_lock_sha256") != lock_sha256:
        fail("manifest frozen lock hash mismatch")
    if frozen_section.get("release_lock_payload_sha256") != lock_payload_sha256:
        fail("manifest frozen lock payload mismatch")
    if manifest.get("combined_file_count_excluding_manifest") != len(frozen) + len(submission):
        fail("combined file count mismatch")
    combined = {"frozen_evidence": frozen, "submission_sources": submission}
    if manifest.get("combined_content_root_sha256") != canonical_hash(combined):
        fail("combined content root mismatch")
    policy = manifest["submission_sources"].get("policy")
    expected_policy = {
        "base": "proof_compression_submission",
        "excluded_components": ["output except named replay/PDF/log artifacts", "__pycache__", "dot-prefixed directories"],
        "excluded_names": [".DS_Store", MANIFEST_RELATIVE],
        "excluded_suffixes": [".pyc", ".pyo"],
        "supplemental_execution_dependencies": sorted(
            SUPPLEMENTAL_EXECUTION_DEPENDENCIES
        ),
        "symlinks_allowed": False,
    }
    if policy != expected_policy:
        fail("submission source policy mismatch")
    archive_policy = manifest.get("archive_policy")
    if not isinstance(archive_policy, dict) or archive_policy.get("fixed_member_timestamp") != "2026-08-26T00:00:00":
        fail("archive timestamp policy mismatch")
    required_sources = {
        "proof_compression_submission/AI_REFEREE_PROMPT.md",
        "proof_compression_submission/article/main.tex",
        "proof_compression_submission/article/references.bib",
        "proof_compression_submission/supplement/supplement.tex",
        "proof_compression_submission/supplement/compression_tables.tex",
        "proof_compression_submission/supplement/certificate_appendix.tex",
        "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json",
        "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.md",
        "proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py",
        "proof_compression_submission/crosswalk/build_revised_referee_bundle.py",
        "proof_compression_submission/crosswalk/check_revised_referee_bundle.py",
        "proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py",
        "proof_compression_submission/PDF_BUILD_REPORT.json",
        "proof_compression_submission/PDF_BUILD_REPORT.md",
        "proof_compression_submission/adversarial_review/STATIC_AUDIT_RESULT.json",
        "proof_compression_submission/adversarial_review/audit_article_sources.py",
        *OPERATIONAL_EVIDENCE,
        *SUPPLEMENTAL_EXECUTION_DEPENDENCIES,
    }
    missing = sorted(required_sources - set(submission))
    if missing:
        fail(f"required source omitted: {missing}")
    verify_crosswalk(
        frozen,
        submission,
        expected_runtime,
        lock_sha256,
        lock_payload_sha256,
    )
    verify_final_release_mutations()
    verify_pdf_build_report(submission)
    verify_static_article_audit(submission, expected_runtime, lock_sha256)
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
