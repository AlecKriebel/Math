#!/usr/bin/env python3
"""Fail-closed qualification of the four-port direct-closure release.

This is an outer verifier, deliberately separate from the immutable sweep
engine.  It validates the release lock with streamed file hashes, reconstructs
the six-source semantic manifest root, binds the 36 published raw records, and
then invokes the independently checkable engine and proof replays.
"""

from __future__ import annotations

if not __debug__:
    raise SystemExit("DIRECT_CLOSURE_OPTIMIZED_MODE_FORBIDDEN: invoke Python without -O")

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parent
LOCK_NAME = "DIRECT_CLOSURE_LOCK.json"
LOCK_SCHEMA = "k2p-four-port-direct-closure-lock-v1"
ENGINE_LOCK_SCHEMA = "k2p-offline-four-port-input-lock-v1"
MANIFEST_SCHEMA = "k2p-four-port-residual-manifest-v2"
RECORD_SCHEMA = "k2p-four-port-record-v3"
MERGED_SCHEMA = "k2p-four-port-six-source-merge-v2"

EXPECTED_SOURCE_CLASS_COUNTS = (536, 747, 276, 276, 64, 32)
EXPECTED_STATUS_COUNTS = {
    "error": 0,
    "isomorphic": 20,
    "restoration_parent": 997,
    "separated": 845,
    "triangle": 35,
    "unresolved": 34,
}
EXPECTED_UNRESOLVED = {
    0: (),
    1: (25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
        39, 40, 41, 42, 43, 44, 45, 46, 47),
    2: (112, 113, 114, 115),
    3: (112, 113, 114, 115),
    4: (8, 9, 10, 11),
    5: (),
}
EXPECTED_CANDIDATES = {
    1: EXPECTED_UNRESOLVED[1],
    2: EXPECTED_UNRESOLVED[2],
    3: EXPECTED_UNRESOLVED[3],
    4: EXPECTED_UNRESOLVED[4],
    5: (9, 10),
}
EXPECTED_FAMILY_COUNTS = {
    "lower_theta_quartic": 12,
    "theta0_quintic_port_orbit": 22,
    "theta3_cubic": 2,
}
VALID_STATUSES = frozenset(EXPECTED_STATUS_COUNTS)
TOP_LEVEL_RELEASE_FILES = (
    "INPUT_LOCK.json",
    "README_DIRECT_CLOSURE.md",
    "build_direct_closure_lock.py",
    "test_direct_closure_release_mutations.py",
    "verify_direct_closure_release.py",
)


def fail(code: str, detail: Any = None) -> "None":
    message = code if detail is None else f"{code}: {detail}"
    raise SystemExit(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        fail("RELEASE_HASH_READ_FAIL", f"{path}: {exc}")
    return digest.hexdigest()


def sha_object(value: Any) -> str:
    raw = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=str
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail("RELEASE_JSON_DUPLICATE_KEY", key)
        result[key] = value
    return result


def load_json(path: Path, code: str) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle, object_pairs_hook=no_duplicate_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(code, f"{path}: {exc}")
    if not isinstance(value, dict):
        fail(code, f"top-level JSON value is not an object: {path}")
    return value


def independent_release_files(root: Path) -> tuple[Path, ...]:
    paths = [root / relative for relative in TOP_LEVEL_RELEASE_FILES]
    for directory in (root / "proofs", root / "results/four_port_release_v4"):
        if not directory.is_dir():
            fail("RELEASE_DIRECTORY_MISSING", directory)
        paths.extend(
            path
            for path in directory.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.name != ".DS_Store"
            and not path.name.endswith((".pyc", ".pyo"))
        )
    return tuple(sorted(set(paths), key=lambda path: path.relative_to(root).as_posix()))


def validate_safe_regular_file(root: Path, relative: str) -> Path:
    pure = PurePosixPath(relative)
    if (
        not relative
        or pure.is_absolute()
        or ".." in pure.parts
        or "." in pure.parts
        or "\\" in relative
        or pure.as_posix() != relative
    ):
        fail("DIRECT_CLOSURE_LOCK_UNSAFE_PATH", relative)
    path = root.joinpath(*pure.parts)
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        fail("DIRECT_CLOSURE_LOCK_FILE_MISSING", f"{relative}: {exc}")
    if not stat.S_ISREG(mode):
        fail("DIRECT_CLOSURE_LOCK_NONREGULAR_FILE", relative)
    try:
        path.resolve().relative_to(root.resolve())
    except (OSError, ValueError):
        fail("DIRECT_CLOSURE_LOCK_PATH_ESCAPE", relative)
    return path


def validate_release_lock(root: Path, allow_missing: bool) -> dict[str, Any] | None:
    lock_path = root / LOCK_NAME
    if not lock_path.is_file():
        if allow_missing:
            print("DIRECT_CLOSURE_LOCK_PRELOCK_MODE")
            return None
        fail("DIRECT_CLOSURE_LOCK_MISSING", lock_path)
    lock = load_json(lock_path, "DIRECT_CLOSURE_LOCK_JSON_FAIL")
    expected_keys = {
        "schema", "engine_input_lock_sha256", "expected_candidate_record_count",
        "expected_manifest_summary_count", "expected_proof_family_counts",
        "file_count", "total_bytes", "files",
    }
    if set(lock) != expected_keys:
        fail("DIRECT_CLOSURE_LOCK_FIELD_SET_FAIL", sorted(set(lock) ^ expected_keys))
    if lock.get("schema") != LOCK_SCHEMA:
        fail("DIRECT_CLOSURE_LOCK_SCHEMA_FAIL", lock.get("schema"))
    if lock.get("expected_candidate_record_count") != 36:
        fail("DIRECT_CLOSURE_LOCK_CANDIDATE_COUNT_FAIL")
    if lock.get("expected_manifest_summary_count") != 1931:
        fail("DIRECT_CLOSURE_LOCK_SUMMARY_COUNT_FAIL")
    if lock.get("expected_proof_family_counts") != EXPECTED_FAMILY_COUNTS:
        fail("DIRECT_CLOSURE_LOCK_FAMILY_COUNT_FAIL")
    files = lock.get("files")
    if not isinstance(files, dict):
        fail("DIRECT_CLOSURE_LOCK_FILES_FAIL", "files is not an object")
    observed_paths = independent_release_files(root)
    observed_relatives = tuple(path.relative_to(root).as_posix() for path in observed_paths)
    locked_relatives = tuple(sorted(files))
    if locked_relatives != observed_relatives:
        fail(
            "DIRECT_CLOSURE_LOCK_FILE_SET_FAIL",
            {"missing_from_lock": sorted(set(observed_relatives) - set(files)),
             "missing_from_release": sorted(set(files) - set(observed_relatives))},
        )
    if lock.get("file_count") != len(observed_paths):
        fail("DIRECT_CLOSURE_LOCK_FILE_COUNT_FAIL")
    total_bytes = 0
    for relative in locked_relatives:
        expected = files[relative]
        if (
            not isinstance(expected, str)
            or len(expected) != 64
            or any(character not in "0123456789abcdef" for character in expected)
        ):
            fail("DIRECT_CLOSURE_LOCK_HASH_FORMAT_FAIL", relative)
        path = validate_safe_regular_file(root, relative)
        total_bytes += path.stat().st_size
        observed = sha256_file(path)
        if observed != expected:
            fail("DIRECT_CLOSURE_LOCK_HASH_FAIL", relative)
    if lock.get("total_bytes") != total_bytes:
        fail("DIRECT_CLOSURE_LOCK_BYTE_COUNT_FAIL")
    if lock.get("engine_input_lock_sha256") != files.get("INPUT_LOCK.json"):
        fail("DIRECT_CLOSURE_LOCK_ENGINE_BINDING_FAIL")
    print(f"DIRECT_CLOSURE_LOCK_PASS files={len(files)} bytes={total_bytes}")
    return lock


def semantic_record_hash(record: dict[str, Any]) -> str:
    diagnostic_fields = {
        "runtime_seconds", "peak_rss_bytes", "runtime_platform", "generated_at_utc",
        "record_payload_sha256", "semantic_record_sha256",
    }
    return sha_object({key: value for key, value in record.items() if key not in diagnostic_fields})


def record_payload_hash(record: dict[str, Any]) -> str:
    return sha_object({key: value for key, value in record.items() if key != "record_payload_sha256"})


def semantic_manifest_hash(
    source_index: int,
    class_count: int,
    bindings: dict[str, Any],
    summaries: list[dict[str, Any]],
) -> str:
    semantic_summaries = [
        {key: value for key, value in summary.items() if key != "record_sha256"}
        for summary in summaries
    ]
    return sha_object({
        "source_index": source_index,
        "canonical_class_count": class_count,
        "immutable": {"schema": RECORD_SCHEMA, **bindings},
        "records": semantic_summaries,
    })


def package_bindings(root: Path, engine_lock: dict[str, Any]) -> dict[str, Any]:
    files = engine_lock.get("files")
    if not isinstance(files, dict):
        fail("ENGINE_INPUT_LOCK_FILES_FAIL")
    required = (
        "atlas/descriptors_4.pkl", "atlas/k2p_atlas_core.py",
        "atlas/rank_certs_4.pkl", "certificates/direct_hard_cases.json",
        "schemas/four_port_record_v3.schema.json",
    )
    if any(relative not in files for relative in required):
        fail("ENGINE_INPUT_LOCK_REQUIRED_FILE_FAIL")
    return {
        "compiler_sha256": engine_lock.get("compiler_sha256"),
        "canonicalizer_sha256": engine_lock.get("canonicalizer_sha256"),
        "descriptor_pickle_sha256": files["atlas/descriptors_4.pkl"],
        "rank_pickle_sha256": files["atlas/rank_certs_4.pkl"],
        "output_schema_sha256": files["schemas/four_port_record_v3.schema.json"],
        "input_lock_sha256": sha256_file(root / "INPUT_LOCK.json"),
        "hard_certificate_sha256": files["certificates/direct_hard_cases.json"],
    }


def validate_candidate_record(
    path: Path,
    source_index: int,
    class_id: int,
    summary: dict[str, Any],
    bindings: dict[str, Any],
) -> dict[str, Any]:
    record = load_json(path, "RELEASE_RECORD_JSON_FAIL")
    if record.get("source_index") != source_index or record.get("canonical_class_id") != class_id:
        fail("RELEASE_RECORD_IDENTITY_MISMATCH", path)
    if record.get("schema") != RECORD_SCHEMA:
        fail("RELEASE_RECORD_SCHEMA_MISMATCH", path)
    expected_status = "separated" if source_index == 5 else "unresolved"
    if record.get("status") != expected_status or summary.get("status") != expected_status:
        fail("RELEASE_RECORD_STATUS_MISMATCH", path)
    if record.get("stratum") != "direct_no_dummy":
        fail("RELEASE_RECORD_STRATUM_MISMATCH", path)
    if record.get("direction") != "source_to_target":
        fail("RELEASE_RECORD_DIRECTION_MISMATCH", path)
    members = record.get("members")
    port = record.get("port_match")
    if (
        not isinstance(members, list) or len(members) != 1
        or not isinstance(port, list) or sorted(port) != [0, 1, 2, 3]
        or members[0].get("port_match") != port
        or record.get("port_matches") != [port]
    ):
        fail("RELEASE_RECORD_PORT_MISMATCH", path)
    if record.get("omitted_roles") != [] or record.get("child_requests") != []:
        fail("RELEASE_RECORD_DIRECT_SCOPE_MISMATCH", path)
    if any(record.get(key) != value for key, value in bindings.items()):
        fail("RELEASE_RECORD_ENGINE_BINDING_MISMATCH", path)
    observed_semantic = semantic_record_hash(record)
    if record.get("semantic_record_sha256") != observed_semantic:
        fail("RELEASE_RECORD_SEMANTIC_HASH_MISMATCH", path)
    if record.get("record_payload_sha256") != record_payload_hash(record):
        fail("RELEASE_RECORD_PAYLOAD_HASH_MISMATCH", path)
    expected_summary = {
        "canonical_class_id": class_id,
        "status": record["status"],
        "stratum": record["stratum"],
        "descriptor_sha256": record["descriptor_sha256"],
        "record_sha256": sha256_file(path),
        "semantic_record_sha256": observed_semantic,
        "omitted_roles": record["omitted_roles"],
        "child_requests": record["child_requests"],
    }
    if summary != expected_summary:
        fail("RELEASE_RECORD_SUMMARY_MISMATCH", path)
    if source_index == 5 and not isinstance(record.get("certificate"), dict):
        fail("RELEASE_RECORD_CUBIC_CERTIFICATE_MISSING", path)
    if source_index != 5 and record.get("certificate") is not None:
        fail("RELEASE_RECORD_UNEXPECTED_CERTIFICATE", path)
    return record


def validate_release_semantics(root: Path, direct_lock: dict[str, Any] | None) -> dict[str, Any]:
    engine_lock = load_json(root / "INPUT_LOCK.json", "ENGINE_INPUT_LOCK_JSON_FAIL")
    if engine_lock.get("schema") != ENGINE_LOCK_SCHEMA:
        fail("ENGINE_INPUT_LOCK_SCHEMA_FAIL")
    if tuple(engine_lock.get("expected_source_class_counts", ())) != EXPECTED_SOURCE_CLASS_COUNTS:
        fail("ENGINE_SOURCE_COUNTS_FAIL")
    engine_lock_sha = sha256_file(root / "INPUT_LOCK.json")
    if direct_lock is not None and direct_lock.get("engine_input_lock_sha256") != engine_lock_sha:
        fail("DIRECT_CLOSURE_LOCK_ENGINE_HASH_MISMATCH")
    bindings = package_bindings(root, engine_lock)
    run_root = root / "results/four_port_release_v4"
    summaries_by_key: dict[tuple[int, int], dict[str, Any]] = {}
    merge_rows: list[dict[str, Any]] = []
    totals = {status: 0 for status in sorted(VALID_STATUSES)}
    summary_count = 0

    for source_index, class_count in enumerate(EXPECTED_SOURCE_CLASS_COUNTS):
        path = run_root / f"source_{source_index}/residual_manifest.json"
        manifest = load_json(path, "RELEASE_MANIFEST_JSON_FAIL")
        if (
            manifest.get("schema") != MANIFEST_SCHEMA
            or manifest.get("record_schema") != RECORD_SCHEMA
            or manifest.get("source_index") != source_index
            or manifest.get("canonical_class_count") != class_count
            or manifest.get("record_count") != class_count
            or manifest.get("complete") is not True
        ):
            fail("RELEASE_MANIFEST_HEADER_MISMATCH", path)
        if {key: manifest.get(key) for key in bindings} != bindings:
            fail("RELEASE_MANIFEST_ENGINE_BINDING_MISMATCH", path)
        summaries = manifest.get("records")
        if not isinstance(summaries, list):
            fail("RELEASE_MANIFEST_RECORDS_TYPE_FAIL", path)
        ids = [row.get("canonical_class_id") if isinstance(row, dict) else None for row in summaries]
        if ids != list(range(class_count)):
            fail("RELEASE_MANIFEST_CLASS_CENSUS_MISMATCH", path)
        for summary in summaries:
            status = summary.get("status")
            if status not in VALID_STATUSES:
                fail("RELEASE_MANIFEST_STATUS_INVALID", f"{path}: {status}")
            key = (source_index, summary["canonical_class_id"])
            if key in summaries_by_key:
                fail("RELEASE_MANIFEST_DUPLICATE_SUMMARY", key)
            summaries_by_key[key] = summary
            totals[status] += 1
        summary_count += len(summaries)
        unresolved = sorted(row["canonical_class_id"] for row in summaries if row["status"] == "unresolved")
        restoration = sorted(row["canonical_class_id"] for row in summaries if row["status"] == "restoration_parent")
        if tuple(unresolved) != EXPECTED_UNRESOLVED[source_index]:
            fail("RELEASE_MANIFEST_STATUS_CENSUS_MISMATCH", path)
        if manifest.get("unresolved") != unresolved:
            fail("RELEASE_MANIFEST_UNRESOLVED_MISMATCH", path)
        if manifest.get("restoration_candidates") != restoration:
            fail("RELEASE_MANIFEST_RESTORATION_MISMATCH", path)
        semantic_hash = semantic_manifest_hash(source_index, class_count, bindings, summaries)
        if manifest.get("semantic_manifest_sha256") != semantic_hash:
            fail("RELEASE_MANIFEST_SEMANTIC_ROOT_MISMATCH", path)
        merge_rows.append({
            "source_index": source_index,
            "manifest_sha256": sha256_file(path),
            "semantic_manifest_sha256": semantic_hash,
            "complete": True,
            "canonical_class_count": class_count,
            "record_count": class_count,
            "unresolved": unresolved,
            "restoration_candidates": restoration,
        })

    if summary_count != 1931:
        fail("RELEASE_MANIFEST_SUMMARY_TOTAL_MISMATCH", summary_count)
    if totals != EXPECTED_STATUS_COUNTS:
        fail("RELEASE_MANIFEST_TOTAL_STATUS_MISMATCH", totals)

    expected_record_relatives = {
        f"source_{source}/records/class_{class_id:06d}.json"
        for source, classes in EXPECTED_CANDIDATES.items()
        for class_id in classes
    }
    observed_record_relatives = {
        path.relative_to(run_root).as_posix()
        for path in run_root.glob("source_*/records/*.json")
        if path.is_file()
    }
    if observed_record_relatives != expected_record_relatives:
        fail("RELEASE_RECORD_SET_MISMATCH", {
            "missing": sorted(expected_record_relatives - observed_record_relatives),
            "extra": sorted(observed_record_relatives - expected_record_relatives),
        })
    for source_index, classes in EXPECTED_CANDIDATES.items():
        for class_id in classes:
            path = run_root / f"source_{source_index}/records/class_{class_id:06d}.json"
            validate_candidate_record(path, source_index, class_id, summaries_by_key[(source_index, class_id)], bindings)

    merged_base = {
        "schema": MERGED_SCHEMA,
        "bindings": bindings,
        "sources": merge_rows,
        "all_six_sources_present": True,
        "all_manifests_complete": True,
        "total_status_counts": totals,
        "unresolved_by_source": {
            str(row["source_index"]): row["unresolved"] for row in merge_rows if row["unresolved"]
        },
        "restoration_candidate_counts": {
            str(row["source_index"]): len(row["restoration_candidates"]) for row in merge_rows
        },
    }
    merged_expected = dict(merged_base)
    merged_expected["payload_sha256_without_hash"] = sha_object(merged_base)
    merged_expected["semantic_sweep_sha256"] = sha_object({
        "schema": MERGED_SCHEMA,
        "bindings": bindings,
        "sources": [{
            "source_index": row["source_index"],
            "canonical_class_count": row["canonical_class_count"],
            "semantic_manifest_sha256": row["semantic_manifest_sha256"],
        } for row in merge_rows],
    })
    merged_path = run_root / "FOUR_PORT_SWEEP_MERGED_STATUS.json"
    merged = load_json(merged_path, "RELEASE_MERGED_JSON_FAIL")
    if merged != merged_expected:
        fail("RELEASE_MERGED_MISMATCH", merged_path)

    provenance = load_json(run_root / "PROVENANCE.json", "RELEASE_PROVENANCE_JSON_FAIL")
    expected_candidate_json = {str(source): list(classes) for source, classes in EXPECTED_CANDIDATES.items()}
    expected_unresolved_json = {
        str(source): list(classes) for source, classes in EXPECTED_UNRESOLVED.items() if classes
    }
    if (
        provenance.get("schema") != "k2p-four-port-release-provenance-v1"
        or provenance.get("candidate_direct_classes") != expected_candidate_json
        or provenance.get("unresolved_by_source") != expected_unresolved_json
        or provenance.get("status_counts") != EXPECTED_STATUS_COUNTS
        or provenance.get("bindings", {}).get("semantic_sweep_sha256") != merged["semantic_sweep_sha256"]
        or provenance.get("published_payload", {}).get("direct_candidate_records") != 36
        or provenance.get("published_payload", {}).get("record_summaries_in_manifests") != 1931
    ):
        fail("RELEASE_PROVENANCE_MISMATCH")
    print(
        "DIRECT_CLOSURE_RELEASE_SEMANTICS_PASS "
        f"summaries={summary_count} candidates={len(expected_record_relatives)} "
        f"semantic_sweep_sha256={merged['semantic_sweep_sha256']}"
    )
    return merged


def child_environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment.setdefault("PYTHONHASHSEED", "0")
    return environment


def run_child(
    label: str,
    command: list[str],
    root: Path,
    timeout_seconds: float,
) -> bytes:
    try:
        result = subprocess.run(
            command,
            cwd=root,
            env=child_environment(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        fail(f"{label}_TIMEOUT", f"{timeout_seconds:g}s")
    if result.returncode != 0:
        output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
        fail(f"{label}_FAIL", output[-4000:])
    if result.stderr:
        fail(f"{label}_STDERR", result.stderr.decode("utf-8", errors="replace")[-4000:])
    return result.stdout


def require_byte_identity(label: str, observed: bytes, golden: Path) -> None:
    expected = golden.read_bytes()
    if observed != expected:
        fail(label, {
            "observed_sha256": hashlib.sha256(observed).hexdigest(),
            "expected_sha256": hashlib.sha256(expected).hexdigest(),
        })


def run_qualification(root: Path, quick: bool, timeout_seconds: float) -> dict[str, str]:
    python = sys.executable
    engine_command = [python, "-B", str(root / "verify_package.py")]
    if quick:
        engine_command.extend(("--skip-smoke", "--skip-mutations", "--skip-prepared-audit"))
    engine_output = run_child("ENGINE_QUALIFICATION", engine_command, root, timeout_seconds)
    if b"K2P_OFFLINE_SWEEP_PACKAGE_PASS" not in engine_output.splitlines():
        fail("ENGINE_QUALIFICATION_TERMINAL_FAIL")
    print("DIRECT_CLOSURE_ENGINE_PASS" + (" mode=quick" if quick else " mode=full"))

    proof_root = root / "proofs"
    run_root = root / "results/four_port_release_v4"
    golden_overlay = proof_root / "four_port_direct_residual_closure_certificate.json"
    with tempfile.TemporaryDirectory(prefix="k2p_direct_closure_replay_") as temporary:
        replay_certificate = Path(temporary) / "replay.json"
        overlay_output = run_child(
            "DIRECT_OVERLAY_REPLAY",
            [python, "-B", str(proof_root / "verify_four_port_direct_residual_closure.py"),
             "--package-root", str(root), "--run-root", str(run_root),
             "--certificate", str(replay_certificate)],
            root, timeout_seconds,
        )
        if b"FOUR_PORT_DIRECT_CANDIDATE_OVERLAY_PASS" not in overlay_output.splitlines():
            fail("DIRECT_OVERLAY_REPLAY_TERMINAL_FAIL")
        require_byte_identity(
            "DIRECT_OVERLAY_CERTIFICATE_BYTE_MISMATCH",
            replay_certificate.read_bytes(), golden_overlay,
        )
    print("DIRECT_CLOSURE_OVERLAY_REPLAY_PASS byte_identical=true")

    theta0_output = run_child(
        "THETA0_QUINTIC_REPLAY",
        [python, "-B", str(proof_root / "verify_theta0_quintic_orbit.py")],
        root, timeout_seconds,
    )
    require_byte_identity(
        "THETA0_QUINTIC_STDOUT_BYTE_MISMATCH",
        theta0_output, proof_root / "theta0_quintic_orbit_certificate.json",
    )
    print("THETA0_QUINTIC_STDOUT_PASS byte_identical=true")

    independent_output = run_child(
        "THETA_QUARTIC_INDEPENDENT_REPLAY",
        [python, "-B", str(proof_root / "verify_theta_quartic_obstructions_independent.py")],
        root, timeout_seconds,
    )
    require_byte_identity(
        "THETA_QUARTIC_INDEPENDENT_STDOUT_BYTE_MISMATCH",
        independent_output,
        proof_root / "theta_quartic_obstructions_independent_certificate.json",
    )
    print("THETA_QUARTIC_INDEPENDENT_STDOUT_PASS byte_identical=true")

    primary_output = run_child(
        "THETA_QUARTIC_PRIMARY_REPLAY",
        [python, "-B", str(proof_root / "verify_theta_quartic_obstructions.py"),
         "--run-root", str(run_root)],
        root, timeout_seconds,
    )
    lines = [line for line in primary_output.splitlines() if line.strip()]
    if not lines or lines[-1] != b"THETA_QUARTIC_OBSTRUCTIONS_INDEPENDENT_REPLAY_PASS":
        fail("THETA_QUARTIC_PRIMARY_TERMINAL_FAIL")
    print("THETA_QUARTIC_PRIMARY_REPLAY_PASS")
    return {
        "engine_stdout_sha256": hashlib.sha256(engine_output).hexdigest(),
        "overlay_certificate_sha256": sha256_file(golden_overlay),
        "theta0_stdout_sha256": hashlib.sha256(theta0_output).hexdigest(),
        "quartic_independent_stdout_sha256": hashlib.sha256(independent_output).hexdigest(),
        "quartic_primary_stdout_sha256": hashlib.sha256(primary_output).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--package-root", type=Path, default=ROOT,
        help="direct-closure portable package root (default: directory containing this script)",
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="retain every release/proof check but use the engine's quick qualification path",
    )
    parser.add_argument(
        "--allow-missing-lock", action="store_true",
        help="developer pre-lock mode; never use to qualify a distributed release",
    )
    parser.add_argument("--timeout-seconds", type=float, default=900.0)
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        fail("DIRECT_CLOSURE_TIMEOUT_INVALID")
    root = args.package_root.resolve()
    direct_lock = validate_release_lock(root, args.allow_missing_lock)
    merged = validate_release_semantics(root, direct_lock)
    replay_hashes = run_qualification(root, args.quick, args.timeout_seconds)
    payload = {
        "lock_sha256": sha256_file(root / LOCK_NAME) if direct_lock is not None else None,
        "semantic_sweep_sha256": merged["semantic_sweep_sha256"],
        "proof_family_counts": EXPECTED_FAMILY_COUNTS,
        "remaining_unproved_among_36": 0,
        "replay_hashes": replay_hashes,
    }
    print("K2P_FOUR_PORT_DIRECT_CLOSURE_RELEASE_PASS")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
