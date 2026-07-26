"""Fail-closed binary-proof production runner for the derived ``hole5`` CNF.

The runner is intentionally separate from both the frozen coloring-bank
generator and the signature-breaker generator.  It preserves CaDiCaL's raw
binary DRAT proof, invokes the committed clean-room parser as a bounded
subprocess to create and reparse an addition-only proof, and accepts UNSAT
only after strict ``drat-trim -i -f -W -U`` replay.

Importing this module has no side effects.  Production execution requires
both explicit validation and hostile-audit gates, an exact package-manifest
hash, an exact repository HEAD, pinned tools, bounded resources, and a new
output directory.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import shutil
import signal
import stat
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Mapping, Sequence

from .cegar import (
    ChildResult,
    parse_dimacs_bytes,
    parse_solver_result_file,
    run_bounded_child,
    validate_model_satisfies_cnf,
    verify_pinned_tools,
)
from .hole5_signature_breaker import (
    BREAKER_NAME,
    EXPECTED_BREAKER_SHA256,
    EXPECTED_DERIVED_CLAUSE_COUNT,
    EXPECTED_DERIVED_CNF_SHA256,
    EXPECTED_DERIVED_LITERAL_COUNT,
    EXPECTED_DERIVED_VARIABLE_COUNT,
    audit_derived_package,
)
from .template_color_bank import (
    CNF_NAME,
    MANIFEST_NAME,
    _assert_no_symlink_components,
    _assert_regular_single_link,
    _fsync_directory,
    _validate_new_output_directory,
    _write_new_file,
    campaign_root,
    canonical_json_bytes,
    git_source_binding,
    sha256_bytes,
    sha256_file,
    source_set_sha256,
    strict_json_bytes,
)


SCHEMA_VERSION = 1
RUN_CONFIG_NAME = "run_config.json"
OUTCOME_NAME = "outcome.json"
RAW_PROOF_NAME = "proof.raw.bdrat"
ADDITION_PROOF_NAME = "proof.additions.bdrat"
RESULT_NAME = "solver.result"
SAT_CANDIDATE_NAME = "sat_candidate.json"
CERTIFICATE_NAME = "certificate.json"
PARSER_RELATIVE_PATH = "reviews/hole5_binary_drat_hostile_probe.py"
EXPECTED_PARSER_SHA256 = (
    "02c3c00faf7afb91a3217f5b738d0dacf7699875928162d01ce2df97e600007d"
)
EXPECTED_PARSER_LOG_SHA256 = (
    "2674cf53eecd881535c6bc4bc2732d669562d7a86816e7bc9057222aadeb3ca8"
)
EXPECTED_SYMMETRY_PROBE_SHA256 = (
    "3515adc846e961738b86c572a90aa0f42945cfa6794e3700986c392999c4ab66"
)
EXPECTED_SYMMETRY_LOG_SHA256 = (
    "f1d8f6d8d6f85bdffadcf39e5d4c4504b9cf0d1b8a609d8e5fe540523091b9de"
)
EXPECTED_BREAKER_STREAM_SHA256 = (
    "ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6"
)
EXPECTED_PACKAGE_MANIFEST_SHA256 = (
    "da33bc1708f7d21b92ceedc68710d5433a1aacbe6e32b8a7432bbab45d8cc788"
)
EXPECTED_PACKAGE_PROBE_SHA256 = (
    "ddf75d62dda73779cca880d2c3ec60ee00b91d5f1110ffa84426678a8ef32cc9"
)
EXPECTED_PACKAGE_PROBE_LOG_SHA256 = (
    "58edf995b84de703c466e956f47d50443de025fa8b5c5268d781f8962a39d694"
)
EXPECTED_PACKAGE_REVIEW_SHA256 = (
    "b675ed1ba1e83a37069af4f3f526a98b3c627d1133300b1e5764fe933fa7b5ed"
)
EXPECTED_CADICAL_BINARY_SHA256 = (
    "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
)
EXPECTED_CADICAL_ARCHIVE_SHA256 = (
    "2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e"
)
EXPECTED_DRAT_TRIM_BINARY_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
EXPECTED_DRAT_TRIM_ARCHIVE_SHA256 = (
    "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108"
)
MAX_CHILD_MEMORY_MIB = 4_096
MAX_SOLVER_SECONDS = 3_600
MAX_POSTPROCESS_SECONDS = 1_800
MAX_FILE_LIMIT_MIB = 600
MIN_DISK_RESERVE_MIB = 4_096
CHILD_WALL_GRACE_SECONDS = 15
INITIAL_DISK_FILE_SLOTS = 9
PARSER_DISK_FILE_SLOTS = 5
CHECKER_DISK_FILE_SLOTS = 2
DISK_METADATA_ALLOWANCE_MIB = 32
PROOF_STAT_KEYS = {
    "byte_count",
    "record_count",
    "addition_count",
    "deletion_count",
    "addition_literal_count",
    "deletion_literal_count",
    "maximum_variable",
    "maximum_clause_length",
    "empty_addition_count",
    "final_empty_record",
    "first_deletion_record",
    "proof_sha256",
    "addition_stream_sha256",
    "deletion_stream_sha256",
    "addition_stream_size_bytes",
    "deletion_stream_size_bytes",
}
RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/synthesis_k3/__init__.py",
    "src/synthesis_k3/encoding.py",
    "src/synthesis_k3/coloring.py",
    "src/synthesis_k3/generate.py",
    "src/synthesis_k3/cegar.py",
    "src/synthesis_k3/template_color_bank.py",
    "src/synthesis_k3/hole5_signature_breaker.py",
    "src/synthesis_k3/hole5_binary_production.py",
    "math/lemmas/hole5_signature_symmetry.md",
    "reviews/hole5_signature_symmetry_hostile_probe.py",
    "reviews/hole5_signature_symmetry_hostile_probe_log.json",
    "reviews/hole5_signature_symmetry_hostile_review.md",
    "reviews/hole5_signature_package_hostile_probe.py",
    "reviews/hole5_signature_package_hostile_probe_log.json",
    "reviews/hole5_signature_package_hostile_review.md",
    PARSER_RELATIVE_PATH,
    "reviews/hole5_binary_drat_hostile_probe_log.json",
    "reviews/hole5_binary_drat_hostile_review.md",
    "reviews/hole5_binary_production_hostile_probe.py",
    "reviews/hole5_binary_production_hostile_probe_log.json",
    "reviews/hole5_binary_production_hostile_review.md",
    "tests/test_hole5_signature_breaker.py",
    "tests/test_hole5_binary_production.py",
)


def _require_gate(value: object, role: str) -> None:
    if value is not True:
        raise PermissionError(f"explicit {role} gate is required")


def _exact_int(
    value: object,
    role: str,
    *,
    minimum: int,
    maximum: int,
) -> int:
    if (
        type(value) is not int
        or value < minimum
        or value > maximum
    ):
        raise ValueError(
            f"{role} must be an exact integer in {minimum}..{maximum}"
        )
    return value


def _hex_digest(value: object, role: str) -> str:
    if type(value) is not str or len(value) != 64:
        raise ValueError(f"{role} must be a 64-character SHA-256")
    try:
        bytes.fromhex(value)
    except ValueError as error:
        raise ValueError(f"{role} is not hexadecimal") from error
    return value


def _git_object_id(value: object, role: str) -> str:
    if type(value) is not str or len(value) not in (40, 64):
        raise ValueError(f"{role} has an unexpected object-id length")
    try:
        bytes.fromhex(value)
    except ValueError as error:
        raise ValueError(f"{role} is not hexadecimal") from error
    return value


def runtime_source_manifest() -> tuple[tuple[str, str], ...]:
    root = campaign_root()
    result: list[tuple[str, str]] = []
    for relative in RUNTIME_SOURCE_RELATIVE_PATHS:
        path = root / relative
        _assert_regular_single_link(path, f"runtime source {relative}")
        result.append((relative, sha256_file(path)))
    expected = {
        PARSER_RELATIVE_PATH: EXPECTED_PARSER_SHA256,
        "reviews/hole5_binary_drat_hostile_probe_log.json": (
            EXPECTED_PARSER_LOG_SHA256
        ),
        "reviews/hole5_signature_symmetry_hostile_probe.py": (
            EXPECTED_SYMMETRY_PROBE_SHA256
        ),
        "reviews/hole5_signature_symmetry_hostile_probe_log.json": (
            EXPECTED_SYMMETRY_LOG_SHA256
        ),
        "reviews/hole5_signature_package_hostile_probe.py": (
            EXPECTED_PACKAGE_PROBE_SHA256
        ),
        "reviews/hole5_signature_package_hostile_probe_log.json": (
            EXPECTED_PACKAGE_PROBE_LOG_SHA256
        ),
        "reviews/hole5_signature_package_hostile_review.md": (
            EXPECTED_PACKAGE_REVIEW_SHA256
        ),
    }
    observed = dict(result)
    for relative, digest in expected.items():
        if observed.get(relative) != digest:
            raise ValueError(f"hostile artifact hash differs: {relative}")
    return tuple(result)


def _physical_memory_bytes() -> int:
    pages = os.sysconf("SC_PHYS_PAGES")
    page_size = os.sysconf("SC_PAGE_SIZE")
    if (
        type(pages) is not int
        or type(page_size) is not int
        or pages <= 0
        or page_size <= 0
    ):
        raise ValueError("physical-memory report is invalid")
    return pages * page_size


def _disk_gate(
    directory: Path,
    *,
    disk_reserve_mib: int,
    file_limit_mib: int,
    remaining_file_slots: int,
) -> dict[str, int]:
    usage = shutil.disk_usage(directory)
    required_mib = (
        disk_reserve_mib
        + remaining_file_slots * file_limit_mib
        + DISK_METADATA_ALLOWANCE_MIB
    )
    required_bytes = required_mib << 20
    if usage.free < required_bytes:
        raise RuntimeError(
            f"disk gate failed: {usage.free} bytes free, "
            f"{required_bytes} required"
        )
    return {
        "free_bytes": usage.free,
        "required_bytes": required_bytes,
        "remaining_file_slots": remaining_file_slots,
    }


def _resource_preflight(
    *,
    output_parent: Path,
    solver_seconds: int,
    parser_seconds: int,
    checker_seconds: int,
    solver_memory_mib: int,
    parser_memory_mib: int,
    checker_memory_mib: int,
    file_limit_mib: int,
    disk_reserve_mib: int,
) -> dict[str, object]:
    solver_seconds = _exact_int(
        solver_seconds,
        "solver seconds",
        minimum=1,
        maximum=MAX_SOLVER_SECONDS,
    )
    parser_seconds = _exact_int(
        parser_seconds,
        "parser seconds",
        minimum=1,
        maximum=MAX_POSTPROCESS_SECONDS,
    )
    checker_seconds = _exact_int(
        checker_seconds,
        "checker seconds",
        minimum=1,
        maximum=MAX_POSTPROCESS_SECONDS,
    )
    solver_memory_mib = _exact_int(
        solver_memory_mib,
        "solver memory MiB",
        minimum=64,
        maximum=MAX_CHILD_MEMORY_MIB,
    )
    parser_memory_mib = _exact_int(
        parser_memory_mib,
        "parser memory MiB",
        minimum=64,
        maximum=MAX_CHILD_MEMORY_MIB,
    )
    checker_memory_mib = _exact_int(
        checker_memory_mib,
        "checker memory MiB",
        minimum=64,
        maximum=MAX_CHILD_MEMORY_MIB,
    )
    file_limit_mib = _exact_int(
        file_limit_mib,
        "file limit MiB",
        minimum=1,
        maximum=MAX_FILE_LIMIT_MIB,
    )
    disk_reserve_mib = _exact_int(
        disk_reserve_mib,
        "disk reserve MiB",
        minimum=MIN_DISK_RESERVE_MIB,
        maximum=1 << 20,
    )
    physical = _physical_memory_bytes()
    safe_child_mib = math.floor(physical * 0.25 / (1 << 20))
    largest_child = max(
        solver_memory_mib, parser_memory_mib, checker_memory_mib
    )
    if largest_child > safe_child_mib:
        raise ValueError(
            "child memory limit exceeds 25% of physical memory"
        )
    disk = _disk_gate(
        output_parent,
        disk_reserve_mib=disk_reserve_mib,
        file_limit_mib=file_limit_mib,
        remaining_file_slots=INITIAL_DISK_FILE_SLOTS,
    )
    return {
        "physical_memory_bytes": physical,
        "maximum_responsive_child_memory_mib": safe_child_mib,
        "solver_internal_seconds": solver_seconds,
        "solver_supervisor_seconds": (
            solver_seconds + CHILD_WALL_GRACE_SECONDS
        ),
        "parser_supervisor_seconds": (
            parser_seconds + CHILD_WALL_GRACE_SECONDS
        ),
        "checker_internal_seconds": checker_seconds,
        "checker_supervisor_seconds": (
            checker_seconds + CHILD_WALL_GRACE_SECONDS
        ),
        "solver_memory_mib": solver_memory_mib,
        "parser_memory_mib": parser_memory_mib,
        "checker_memory_mib": checker_memory_mib,
        "file_limit_mib": file_limit_mib,
        "disk_reserve_mib": disk_reserve_mib,
        "initial_disk_gate": disk,
    }


def _solver_command(
    cadical: Path,
    *,
    seed: int,
    internal_seconds: int,
    result_path: Path,
    cnf_path: Path,
    proof_path: Path,
) -> tuple[str, ...]:
    return (
        str(cadical.resolve()),
        f"--seed={seed}",
        "--binary",
        "--no-colors",
        "-q",
        "-t",
        str(internal_seconds),
        "-w",
        str(result_path.resolve()),
        str(cnf_path.resolve()),
        str(proof_path.resolve()),
    )


def _parser_command(
    python: Path,
    parser: Path,
    *,
    raw_proof: Path,
    addition_proof: Path,
) -> tuple[str, ...]:
    return (
        str(python.resolve()),
        "-I",
        "-B",
        str(parser.resolve()),
        "strip",
        "--proof",
        str(raw_proof.resolve()),
        "--output",
        str(addition_proof.resolve()),
        "--max-var",
        str(EXPECTED_DERIVED_VARIABLE_COUNT),
    )


def _checker_command(
    checker: Path,
    *,
    cnf_path: Path,
    proof_path: Path,
    internal_seconds: int,
) -> tuple[str, ...]:
    return (
        str(checker.resolve()),
        str(cnf_path.resolve()),
        str(proof_path.resolve()),
        "-i",
        "-f",
        "-W",
        "-U",
        "-t",
        str(internal_seconds),
    )


def _bind_file(path: Path, role: str) -> dict[str, object]:
    _assert_regular_single_link(path, role)
    return {
        "path": str(path.resolve()),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def _verify_binding(record: Mapping[str, object], role: str) -> None:
    if set(record) != {"path", "size_bytes", "sha256"}:
        raise ValueError(f"{role} binding shape is wrong")
    path = Path(str(record["path"]))
    _assert_regular_single_link(path, role)
    if (
        type(record["size_bytes"]) is not int
        or type(record["sha256"]) is not str
        or path.stat().st_size != record["size_bytes"]
        or sha256_file(path) != record["sha256"]
    ):
        raise RuntimeError(f"{role} changed after preflight")


def _immutable_bindings(
    *,
    derived_package: Path,
    source_package: Path,
    cadical_binding: object,
    checker_binding: object,
    parser: Path,
    python: Path,
    sources: Sequence[tuple[str, str]],
) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for prefix, package, names in (
        (
            "derived",
            derived_package,
            (CNF_NAME, BREAKER_NAME, MANIFEST_NAME),
        ),
        (
            "source",
            source_package,
            ("coloring_bank.json", CNF_NAME, MANIFEST_NAME),
        ),
    ):
        for name in names:
            result[f"{prefix}:{name}"] = _bind_file(
                package / name, f"{prefix} package {name}"
            )
    for role, binding in (
        ("cadical", cadical_binding),
        ("drat_trim", checker_binding),
    ):
        path = Path(str(getattr(binding, "path")))
        archive = Path(str(getattr(binding, "source_archive_path")))
        result[f"tool:{role}"] = _bind_file(path, role)
        result[f"tool:{role}:source"] = _bind_file(
            archive, f"{role} source archive"
        )
    result["tool:parser"] = _bind_file(parser, "clean-room parser")
    result["tool:python"] = _bind_file(python, "Python executable")
    for relative, digest in sources:
        path = campaign_root() / relative
        record = _bind_file(path, f"runtime source {relative}")
        if record["sha256"] != digest:
            raise RuntimeError(f"runtime source changed: {relative}")
        result[f"runtime:{relative}"] = record
    return result


def _independent_tool_hash_gate(
    cadical_binding: object,
    checker_binding: object,
) -> None:
    for role, binding, expected_binary, expected_archive in (
        (
            "cadical",
            cadical_binding,
            EXPECTED_CADICAL_BINARY_SHA256,
            EXPECTED_CADICAL_ARCHIVE_SHA256,
        ),
        (
            "drat-trim",
            checker_binding,
            EXPECTED_DRAT_TRIM_BINARY_SHA256,
            EXPECTED_DRAT_TRIM_ARCHIVE_SHA256,
        ),
    ):
        binary = Path(str(getattr(binding, "path")))
        archive = Path(str(getattr(binding, "source_archive_path")))
        if (
            getattr(binding, "sha256") != expected_binary
            or getattr(binding, "source_archive_sha256") != expected_archive
            or sha256_file(binary) != expected_binary
            or sha256_file(archive) != expected_archive
        ):
            raise ValueError(f"independent {role} hash gate failed")


def _verify_all_bindings(
    bindings: Mapping[str, Mapping[str, object]],
) -> None:
    for role, record in bindings.items():
        _verify_binding(record, role)


def _child_record(child: ChildResult | None) -> dict[str, object] | None:
    return None if child is None else asdict(child)


def _child_failure_status(
    child: ChildResult,
    phase: str,
) -> str | None:
    prefix = phase.upper()
    if child.timed_out:
        return f"{prefix}_TIMEOUT_NONCLAIM"
    if child.memory_limit_exceeded:
        return f"{prefix}_MEMORY_LIMIT_NONCLAIM"
    if child.termination_signal == int(signal.SIGXFSZ):
        return f"{prefix}_FILE_LIMIT_NONCLAIM"
    if child.termination_signal is not None:
        return f"{prefix}_SIGNAL_NONCLAIM"
    return None


def _proof_stat_record(value: object, role: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or set(value) != PROOF_STAT_KEYS:
        raise ValueError(f"{role} proof statistics shape is wrong")
    integer_keys = PROOF_STAT_KEYS - {
        "proof_sha256",
        "addition_stream_sha256",
        "deletion_stream_sha256",
        "first_deletion_record",
    }
    for key in integer_keys:
        if type(value[key]) is not int or value[key] < 0:
            raise ValueError(f"{role} statistic {key} is malformed")
    first_deletion = value["first_deletion_record"]
    if first_deletion is not None and (
        type(first_deletion) is not int or first_deletion <= 0
    ):
        raise ValueError(f"{role} first-deletion record is malformed")
    for key in (
        "proof_sha256",
        "addition_stream_sha256",
        "deletion_stream_sha256",
    ):
        _hex_digest(value[key], f"{role} {key}")
    if (
        value["record_count"]
        != value["addition_count"] + value["deletion_count"]
        or value["byte_count"]
        != (
            value["addition_stream_size_bytes"]
            + value["deletion_stream_size_bytes"]
        )
        or value["empty_addition_count"] > value["addition_count"]
        or value["final_empty_record"] > value["record_count"]
        or (
            value["deletion_count"] == 0
            and value["first_deletion_record"] is not None
        )
        or (
            value["deletion_count"] > 0
            and (
                value["first_deletion_record"] is None
                or value["first_deletion_record"] > value["record_count"]
            )
        )
    ):
        raise ValueError(f"{role} proof statistics are inconsistent")
    return value


def _validate_parser_report(
    stdout_path: Path,
    stderr_path: Path,
    *,
    raw_proof: Path,
    addition_proof: Path,
) -> dict[str, object]:
    stderr = stderr_path.read_bytes()
    if stderr:
        raise ValueError("clean-room parser emitted stderr")
    payload = stdout_path.read_bytes()
    parsed = strict_json_bytes(payload)
    if canonical_json_bytes(parsed) != payload:
        raise ValueError("clean-room parser report is not canonical JSON")
    if (
        not isinstance(parsed, Mapping)
        or set(parsed)
        != {
            "source",
            "addition_only",
            "all_addition_bytes_preserved_in_order",
        }
        or parsed["all_addition_bytes_preserved_in_order"] is not True
    ):
        raise ValueError("clean-room parser report shape is wrong")
    source = _proof_stat_record(parsed["source"], "source")
    addition = _proof_stat_record(
        parsed["addition_only"], "addition-only"
    )
    _assert_regular_single_link(raw_proof, "raw binary proof")
    _assert_regular_single_link(
        addition_proof, "addition-only binary proof"
    )
    raw_size = raw_proof.stat().st_size
    raw_hash = sha256_file(raw_proof)
    addition_size = addition_proof.stat().st_size
    addition_hash = sha256_file(addition_proof)
    if (
        source["byte_count"] != raw_size
        or source["proof_sha256"] != raw_hash
        or source["empty_addition_count"] != 1
        or source["final_empty_record"] != source["record_count"]
        or source["maximum_variable"]
        > EXPECTED_DERIVED_VARIABLE_COUNT
        or source["addition_stream_size_bytes"]
        + source["deletion_stream_size_bytes"]
        != raw_size
    ):
        raise ValueError("source proof statistics do not bind the raw proof")
    if (
        addition["byte_count"] != addition_size
        or addition["proof_sha256"] != addition_hash
        or addition["deletion_count"] != 0
        or addition["record_count"] != addition["addition_count"]
        or addition["first_deletion_record"] is not None
        or addition["deletion_literal_count"] != 0
        or addition["deletion_stream_size_bytes"] != 0
        or addition["addition_stream_size_bytes"] != addition_size
        or addition["addition_stream_sha256"] != addition_hash
        or addition["empty_addition_count"] != 1
        or addition["final_empty_record"] != addition["record_count"]
        or addition["maximum_variable"]
        > EXPECTED_DERIVED_VARIABLE_COUNT
    ):
        raise ValueError(
            "addition-only statistics do not bind the stripped proof"
        )
    if (
        source["addition_stream_sha256"] != addition_hash
        or source["addition_stream_size_bytes"] != addition_size
        or source["addition_count"] != addition["addition_count"]
        or source["addition_literal_count"]
        != addition["addition_literal_count"]
    ):
        raise ValueError("addition-only proof differs from source additions")
    return dict(parsed)


def _strict_checker_verified(
    stdout_path: Path,
    stderr_path: Path,
) -> None:
    try:
        stdout = stdout_path.read_text(encoding="ascii")
        stderr = stderr_path.read_text(encoding="ascii")
    except UnicodeDecodeError as error:
        raise ValueError("checker logs are not ASCII") from error
    if stderr:
        raise ValueError("strict checker emitted stderr")
    combined = stdout + "\n" + stderr
    if "warning" in combined.lower():
        raise ValueError("strict checker emitted a warning")
    lines = [line.strip() for line in stdout.splitlines()]
    statuses = [line for line in lines if line.startswith("s ")]
    if statuses != ["s VERIFIED"]:
        raise ValueError("strict checker lacks its unique s VERIFIED status")
    rat_lines = [
        line for line in lines if "RAT lemmas in core" in line
    ]
    if (
        len(rat_lines) != 1
        or combined.count("RAT lemmas in core") != 1
        or not (
            rat_lines[0] == "c 0 RAT lemmas in core"
            or rat_lines[0].startswith("c 0 RAT lemmas in core;")
        )
    ):
        raise ValueError("strict checker did not report zero RAT lemmas")


def _existing_artifact_map(
    directory: Path,
) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for path in sorted(directory.iterdir()):
        if path.name == OUTCOME_NAME:
            continue
        _assert_no_symlink_components(path)
        information = os.lstat(path)
        if not stat.S_ISREG(information.st_mode):
            raise ValueError(f"output artifact is not a regular file: {path}")
        if information.st_nlink != 1:
            raise ValueError(f"output artifact has multiple links: {path}")
        result[path.name] = {
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
    return result


def _write_sat_candidate(
    path: Path,
    *,
    cnf_sha256: str,
    result_path: Path,
) -> bytes:
    payload = canonical_json_bytes(
        {
            "schema": "gamma-theta-hole5-sat-candidate-v1",
            "status": "SAT_MODEL_VERIFIED_CANDIDATE_ONLY",
            "claim_status": "CANDIDATE_ONLY",
            "cnf_sha256": cnf_sha256,
            "solver_result_sha256": sha256_file(result_path),
            "counterexample_claim": False,
            "required_follow_up": (
                "independent graph decoding and full parameter verification"
            ),
        }
    )
    _write_new_file(path, payload)
    return payload


def _verify_exact_payload(path: Path, payload: bytes, role: str) -> None:
    _assert_regular_single_link(path, role)
    if path.read_bytes() != payload:
        raise RuntimeError(f"{role} differs from its frozen canonical bytes")


def _write_certificate(
    path: Path,
    *,
    package_manifest_sha256: str,
    cnf_path: Path,
    raw_proof: Path,
    addition_proof: Path,
    parser_report: Mapping[str, object],
    parser_command: Sequence[str],
    checker_command: Sequence[str],
) -> bytes:
    payload = canonical_json_bytes(
        {
            "schema": "gamma-theta-hole5-binary-certificate-v1",
            "schema_version": SCHEMA_VERSION,
            "status": "UNSAT_REPLAY_ARTIFACT",
            "claim_status": "NO_STANDALONE_MATHEMATICAL_CLAIM",
            "scope": (
                "exact retained hole5 S6 signature-broken full-bank CNF"
            ),
            "package_manifest_sha256": package_manifest_sha256,
            "cnf_sha256": sha256_file(cnf_path),
            "raw_binary_proof": {
                "path": raw_proof.name,
                "size_bytes": raw_proof.stat().st_size,
                "sha256": sha256_file(raw_proof),
                "preserved": True,
            },
            "addition_only_binary_proof": {
                "path": addition_proof.name,
                "size_bytes": addition_proof.stat().st_size,
                "sha256": sha256_file(addition_proof),
            },
            "parser_report": dict(parser_report),
            "parser_command": list(parser_command),
            "checker_command": list(checker_command),
            "strict_checker_requirements": {
                "binary_input": True,
                "forward": True,
                "warning_fatal": True,
                "rup_only": True,
                "exactly_one_verified_line": True,
                "zero_rat_lemmas": True,
            },
            "activation_condition": {
                "required_file": OUTCOME_NAME,
                "required_status": "UNSAT_VERIFIED_FINITE_CERTIFICATE",
                "required_claim_status": "VERIFIED_FINITE_CERTIFICATE",
                "required_self_hash_binding": (
                    f"outcome.artifacts.{CERTIFICATE_NAME}.sha256"
                ),
            },
            "claim_boundary": (
                "This replay artifact is not a standalone claim.  With "
                "its matching final outcome it certifies only the exact "
                "hole5 finite instance, not the universal conjecture."
            ),
        }
    )
    _write_new_file(path, payload)
    return payload


def run_production(
    *,
    package_directory: Path,
    source_package_directory: Path,
    output_directory: Path,
    expected_package_manifest_sha256: str,
    expected_head_commit: str,
    cadical_path: Path,
    drat_trim_path: Path,
    seed: int,
    solver_seconds: int,
    parser_seconds: int,
    checker_seconds: int,
    solver_memory_mib: int,
    parser_memory_mib: int,
    checker_memory_mib: int,
    file_limit_mib: int,
    disk_reserve_mib: int,
    validation_gate: object,
    hostile_audit_gate: object,
) -> dict[str, object]:
    """Run one exact, bounded production attempt in a new directory."""

    _require_gate(validation_gate, "validation")
    _require_gate(hostile_audit_gate, "hostile-audit")
    expected_manifest_hash = _hex_digest(
        expected_package_manifest_sha256,
        "expected package manifest hash",
    )
    if expected_manifest_hash != EXPECTED_PACKAGE_MANIFEST_SHA256:
        raise ValueError("only the exact hostile-audited package is accepted")
    expected_head = _git_object_id(
        expected_head_commit, "expected repository HEAD"
    )
    seed = _exact_int(
        seed, "solver seed", minimum=0, maximum=2_000_000_000
    )
    destination = _validate_new_output_directory(output_directory)
    resources = _resource_preflight(
        output_parent=destination.parent,
        solver_seconds=solver_seconds,
        parser_seconds=parser_seconds,
        checker_seconds=checker_seconds,
        solver_memory_mib=solver_memory_mib,
        parser_memory_mib=parser_memory_mib,
        checker_memory_mib=checker_memory_mib,
        file_limit_mib=file_limit_mib,
        disk_reserve_mib=disk_reserve_mib,
    )
    package = package_directory.resolve(strict=True)
    source_package = source_package_directory.resolve(strict=True)
    if package in destination.parents or source_package in destination.parents:
        raise ValueError("output directory must not lie inside an input package")
    package_report = audit_derived_package(
        package,
        source_package=source_package,
        exhaustive_covariance=True,
    )
    if package_report["manifest_sha256"] != expected_manifest_hash:
        raise ValueError("derived package manifest hash differs from expected")
    if (
        package_report["cnf_sha256"] != EXPECTED_DERIVED_CNF_SHA256
        or package_report["breaker_sha256"] != EXPECTED_BREAKER_SHA256
        or package_report["variable_count"]
        != EXPECTED_DERIVED_VARIABLE_COUNT
        or package_report["clause_count"]
        != EXPECTED_DERIVED_CLAUSE_COUNT
        or package_report["literal_count"]
        != EXPECTED_DERIVED_LITERAL_COUNT
    ):
        raise ValueError("derived package formula binding is wrong")
    cnf_path = package / CNF_NAME
    parsed_cnf = parse_dimacs_bytes(cnf_path.read_bytes())
    cadical, checker = verify_pinned_tools(
        cadical_path, drat_trim_path
    )
    _independent_tool_hash_gate(cadical, checker)
    root = campaign_root()
    parser_path = root / PARSER_RELATIVE_PATH
    _assert_regular_single_link(parser_path, "clean-room parser")
    if sha256_file(parser_path) != EXPECTED_PARSER_SHA256:
        raise ValueError("clean-room parser hash differs")
    python_path = Path(sys.executable).resolve(strict=True)
    _assert_regular_single_link(python_path, "Python executable")
    sources = runtime_source_manifest()
    git_binding = git_source_binding(sources)
    if (
        git_binding.get("runtime_sources_match_head") is not True
        or git_binding.get("head_commit") != expected_head
    ):
        raise RuntimeError(
            "production runtime sources do not match the expected HEAD"
        )
    bindings = _immutable_bindings(
        derived_package=package,
        source_package=source_package,
        cadical_binding=cadical,
        checker_binding=checker,
        parser=parser_path,
        python=python_path,
        sources=sources,
    )
    result_path = destination / RESULT_NAME
    raw_proof = destination / RAW_PROOF_NAME
    addition_proof = destination / ADDITION_PROOF_NAME
    solver_stdout = destination / "solver.stdout"
    solver_stderr = destination / "solver.stderr"
    parser_stdout = destination / "parser.stdout"
    parser_stderr = destination / "parser.stderr"
    checker_stdout = destination / "checker.stdout"
    checker_stderr = destination / "checker.stderr"
    solver_command = _solver_command(
        Path(cadical.path),
        seed=seed,
        internal_seconds=solver_seconds,
        result_path=result_path,
        cnf_path=cnf_path,
        proof_path=raw_proof,
    )
    parser_command = _parser_command(
        python_path,
        parser_path,
        raw_proof=raw_proof,
        addition_proof=addition_proof,
    )
    checker_command = _checker_command(
        Path(checker.path),
        cnf_path=cnf_path,
        proof_path=addition_proof,
        internal_seconds=checker_seconds,
    )
    destination.mkdir(mode=0o700)
    _fsync_directory(destination.parent)
    run_config = {
        "schema": "gamma-theta-hole5-binary-production-config-v1",
        "schema_version": SCHEMA_VERSION,
        "package": {
            "path": str(package),
            "manifest_sha256": expected_manifest_hash,
            "cnf_sha256": EXPECTED_DERIVED_CNF_SHA256,
            "breaker_sha256": EXPECTED_BREAKER_SHA256,
            "variable_count": EXPECTED_DERIVED_VARIABLE_COUNT,
            "clause_count": EXPECTED_DERIVED_CLAUSE_COUNT,
            "literal_count": EXPECTED_DERIVED_LITERAL_COUNT,
            "breaker_clause_stream_sha256": (
                EXPECTED_BREAKER_STREAM_SHA256
            ),
        },
        "source_package_path": str(source_package),
        "expected_head_commit": expected_head,
        "git_source_binding": dict(git_binding),
        "runtime_source_manifest": [
            [relative, digest] for relative, digest in sources
        ],
        "runtime_source_set_sha256": source_set_sha256(sources),
        "immutable_input_bindings": bindings,
        "tools": {
            "cadical": asdict(cadical),
            "drat_trim": asdict(checker),
            "clean_room_parser": {
                "path": str(parser_path.resolve()),
                "sha256": EXPECTED_PARSER_SHA256,
            },
            "python": {
                "path": str(python_path),
                "sha256": sha256_file(python_path),
                "implementation": platform.python_implementation(),
                "version": platform.python_version(),
            },
        },
        "seed": seed,
        "resources": resources,
        "commands": {
            "solver": list(solver_command),
            "parser": list(parser_command),
            "checker": list(checker_command),
        },
        "gates": {
            "validation_gate": True,
            "hostile_audit_gate": True,
            "source_to_head_gate": True,
            "atomic_new_output": True,
            "raw_binary_proof_preserved": True,
        },
        "claim_boundary": (
            "SAT is candidate-only; every incomplete or failed phase is "
            "NO_MATHEMATICAL_CLAIM; verified UNSAT covers only this finite "
            "hole5 instance."
        ),
    }
    run_config_payload = canonical_json_bytes(run_config)
    _write_new_file(destination / RUN_CONFIG_NAME, run_config_payload)
    _fsync_directory(destination)

    solver: ChildResult | None = None
    parser_child: ChildResult | None = None
    checker_child: ChildResult | None = None
    status = "SOLVER_CONTROL_FAILURE_NONCLAIM"
    claim_status = "NO_MATHEMATICAL_CLAIM"
    failures: list[dict[str, str]] = []
    semantic_checks: dict[str, object] = {}
    parser_report: dict[str, object] | None = None
    disk_gates: dict[str, object] = {}
    certificate_ready = False
    sat_candidate_payload: bytes | None = None
    certificate_payload: bytes | None = None

    def record_failure(error: BaseException) -> None:
        failures.append(
            {
                "exception_type": type(error).__name__,
                "message": str(error),
            }
        )

    try:
        solver = run_bounded_child(
            command=solver_command,
            cwd=destination,
            stdout_path=solver_stdout,
            stderr_path=solver_stderr,
            wall_limit_seconds=solver_seconds + CHILD_WALL_GRACE_SECONDS,
            memory_limit_mib=solver_memory_mib,
            file_limit_mib=file_limit_mib,
            readonly_paths={"CNF": cnf_path},
        )
    except Exception as error:
        record_failure(error)
    else:
        resource_status = _child_failure_status(solver, "solver")
        if resource_status is not None:
            status = resource_status
        elif solver.exit_code == 0:
            try:
                result = parse_solver_result_file(
                    result_path, parsed_cnf.variable_count
                )
                if result.status != "UNKNOWN":
                    raise ValueError(
                        "solver exit zero lacks exact UNKNOWN result"
                    )
            except Exception as error:
                status = "INVALID_SOLVER_UNKNOWN_ARTIFACT_NONCLAIM"
                record_failure(error)
            else:
                status = "INCONCLUSIVE_SOLVER_UNKNOWN"
        elif solver.exit_code == 10:
            try:
                result = parse_solver_result_file(
                    result_path, parsed_cnf.variable_count
                )
                if result.status != "SAT" or result.model is None:
                    raise ValueError(
                        "solver exit ten lacks exact SAT model"
                    )
                validate_model_satisfies_cnf(parsed_cnf, result.model)
                sat_candidate_payload = _write_sat_candidate(
                    destination / SAT_CANDIDATE_NAME,
                    cnf_sha256=EXPECTED_DERIVED_CNF_SHA256,
                    result_path=result_path,
                )
            except Exception as error:
                status = "INVALID_SAT_MODEL_NONCLAIM"
                record_failure(error)
            else:
                status = "SAT_MODEL_VERIFIED_CANDIDATE_ONLY"
                claim_status = "CANDIDATE_ONLY"
                semantic_checks = {
                    "complete_model": True,
                    "model_satisfies_exact_cnf": True,
                    "counterexample_claim": False,
                }
        elif solver.exit_code == 20:
            try:
                result = parse_solver_result_file(
                    result_path, parsed_cnf.variable_count
                )
                if result.status != "UNSAT":
                    raise ValueError(
                        "solver exit twenty lacks exact UNSAT result"
                    )
                _assert_regular_single_link(
                    raw_proof, "raw binary DRAT proof"
                )
                if raw_proof.stat().st_size == 0:
                    raise ValueError("raw binary proof is empty")
                raw_hash_before = sha256_file(raw_proof)
                disk_gates["before_parser"] = _disk_gate(
                    destination,
                    disk_reserve_mib=disk_reserve_mib,
                    file_limit_mib=file_limit_mib,
                    remaining_file_slots=PARSER_DISK_FILE_SLOTS,
                )
            except Exception as error:
                status = "INVALID_UNSAT_SOLVER_ARTIFACT_NONCLAIM"
                record_failure(error)
            else:
                try:
                    parser_child = run_bounded_child(
                        command=parser_command,
                        cwd=destination,
                        stdout_path=parser_stdout,
                        stderr_path=parser_stderr,
                        wall_limit_seconds=(
                            parser_seconds + CHILD_WALL_GRACE_SECONDS
                        ),
                        memory_limit_mib=parser_memory_mib,
                        file_limit_mib=file_limit_mib,
                        readonly_paths={
                            "raw proof": raw_proof,
                            "clean-room parser": parser_path,
                        },
                    )
                except Exception as error:
                    status = "PARSER_CONTROL_FAILURE_NONCLAIM"
                    record_failure(error)
                else:
                    parser_status = _child_failure_status(
                        parser_child, "parser"
                    )
                    if parser_status is not None:
                        status = parser_status
                    elif parser_child.exit_code != 0:
                        status = "PARSER_EXIT_NONCLAIM"
                    else:
                        try:
                            if sha256_file(raw_proof) != raw_hash_before:
                                raise RuntimeError(
                                    "raw proof changed during parser phase"
                                )
                            parser_report = _validate_parser_report(
                                parser_stdout,
                                parser_stderr,
                                raw_proof=raw_proof,
                                addition_proof=addition_proof,
                            )
                            addition_hash_before = sha256_file(
                                addition_proof
                            )
                            disk_gates["before_checker"] = _disk_gate(
                                destination,
                                disk_reserve_mib=disk_reserve_mib,
                                file_limit_mib=file_limit_mib,
                                remaining_file_slots=(
                                    CHECKER_DISK_FILE_SLOTS
                                ),
                            )
                        except Exception as error:
                            status = "PARSER_ARTIFACT_INVALID_NONCLAIM"
                            record_failure(error)
                        else:
                            try:
                                checker_child = run_bounded_child(
                                    command=checker_command,
                                    cwd=destination,
                                    stdout_path=checker_stdout,
                                    stderr_path=checker_stderr,
                                    wall_limit_seconds=(
                                        checker_seconds
                                        + CHILD_WALL_GRACE_SECONDS
                                    ),
                                    memory_limit_mib=checker_memory_mib,
                                    file_limit_mib=file_limit_mib,
                                    readonly_paths={
                                        "CNF": cnf_path,
                                        "addition-only proof": (
                                            addition_proof
                                        ),
                                    },
                                )
                            except Exception as error:
                                status = (
                                    "CHECKER_CONTROL_FAILURE_NONCLAIM"
                                )
                                record_failure(error)
                            else:
                                checker_status = _child_failure_status(
                                    checker_child, "checker"
                                )
                                if checker_status is not None:
                                    status = checker_status
                                elif checker_child.exit_code != 0:
                                    status = "CHECKER_EXIT_NONCLAIM"
                                else:
                                    try:
                                        _strict_checker_verified(
                                            checker_stdout,
                                            checker_stderr,
                                        )
                                        if (
                                            sha256_file(raw_proof)
                                            != raw_hash_before
                                            or sha256_file(addition_proof)
                                            != addition_hash_before
                                        ):
                                            raise RuntimeError(
                                                "proof changed during "
                                                "strict replay"
                                            )
                                    except Exception as error:
                                        status = (
                                            "CHECKER_ARTIFACT_INVALID_NONCLAIM"
                                        )
                                        record_failure(error)
                                    else:
                                        status = (
                                            "UNSAT_VERIFIED_FINITE_CERTIFICATE"
                                        )
                                        claim_status = (
                                            "VERIFIED_FINITE_CERTIFICATE"
                                        )
                                        semantic_checks = {
                                            "solver_result_unsat": True,
                                            "raw_binary_proof_preserved": True,
                                            "clean_room_parser_max_var": (
                                                EXPECTED_DERIVED_VARIABLE_COUNT
                                            ),
                                            "addition_only_reparsed": True,
                                            "all_deletions_removed": True,
                                            "strict_binary_forward_rup_replay": (
                                                True
                                            ),
                                            "checker_warning_free": True,
                                            "checker_zero_rat_lemmas": True,
                                        }
                                        certificate_ready = True
        else:
            status = "SOLVER_UNEXPECTED_EXIT_NONCLAIM"

    try:
        _verify_all_bindings(bindings)
    except Exception as error:
        status = "IMMUTABLE_INPUT_MUTATION_NONCLAIM"
        claim_status = "NO_MATHEMATICAL_CLAIM"
        semantic_checks = {}
        record_failure(error)
    if (
        status == "UNSAT_VERIFIED_FINITE_CERTIFICATE"
        and certificate_ready
    ):
        try:
            if parser_report is None:
                raise RuntimeError("verified UNSAT lacks parser report")
            certificate_payload = _write_certificate(
                destination / CERTIFICATE_NAME,
                package_manifest_sha256=expected_manifest_hash,
                cnf_path=cnf_path,
                raw_proof=raw_proof,
                addition_proof=addition_proof,
                parser_report=parser_report,
                parser_command=parser_command,
                checker_command=checker_command,
            )
        except Exception as error:
            status = "CERTIFICATE_WRITE_FAILURE_NONCLAIM"
            claim_status = "NO_MATHEMATICAL_CLAIM"
            semantic_checks = {}
            record_failure(error)
    if (
        status == "UNSAT_VERIFIED_FINITE_CERTIFICATE"
        and (destination / CERTIFICATE_NAME).is_file()
    ):
        try:
            _verify_all_bindings(bindings)
            if parser_report is None:
                raise RuntimeError("final replay lacks parser report")
            final_parser_report = _validate_parser_report(
                parser_stdout,
                parser_stderr,
                raw_proof=raw_proof,
                addition_proof=addition_proof,
            )
            if final_parser_report != parser_report:
                raise RuntimeError("parser report changed after replay")
            _strict_checker_verified(checker_stdout, checker_stderr)
            if certificate_payload is None:
                raise RuntimeError("final replay lacks certificate bytes")
            _verify_exact_payload(
                destination / CERTIFICATE_NAME,
                certificate_payload,
                "canonical replay artifact",
            )
        except Exception as error:
            status = "POST_CERTIFICATE_MUTATION_NONCLAIM"
            claim_status = "NO_MATHEMATICAL_CLAIM"
            semantic_checks = {}
            record_failure(error)
    try:
        first_artifacts = _existing_artifact_map(destination)
        _verify_all_bindings(bindings)
        _verify_exact_payload(
            destination / RUN_CONFIG_NAME,
            run_config_payload,
            "canonical run configuration",
        )
        if sat_candidate_payload is not None:
            _verify_exact_payload(
                destination / SAT_CANDIDATE_NAME,
                sat_candidate_payload,
                "canonical SAT candidate",
            )
        if certificate_payload is not None:
            _verify_exact_payload(
                destination / CERTIFICATE_NAME,
                certificate_payload,
                "canonical replay artifact",
            )
        if status == "SAT_MODEL_VERIFIED_CANDIDATE_ONLY":
            if sat_candidate_payload is None:
                raise RuntimeError("SAT status lacks candidate bytes")
            final_result = parse_solver_result_file(
                result_path, parsed_cnf.variable_count
            )
            if final_result.status != "SAT" or final_result.model is None:
                raise RuntimeError("final SAT result is malformed")
            validate_model_satisfies_cnf(parsed_cnf, final_result.model)
            candidate = strict_json_bytes(sat_candidate_payload)
            if (
                not isinstance(candidate, Mapping)
                or candidate.get("solver_result_sha256")
                != sha256_file(result_path)
            ):
                raise RuntimeError("SAT candidate does not bind final model")
        if status == "UNSAT_VERIFIED_FINITE_CERTIFICATE":
            if parser_report is None or certificate_payload is None:
                raise RuntimeError("UNSAT status lacks replay artifacts")
            final_result = parse_solver_result_file(
                result_path, parsed_cnf.variable_count
            )
            if final_result.status != "UNSAT":
                raise RuntimeError("final UNSAT result is malformed")
            if (
                _validate_parser_report(
                    parser_stdout,
                    parser_stderr,
                    raw_proof=raw_proof,
                    addition_proof=addition_proof,
                )
                != parser_report
            ):
                raise RuntimeError("final parser report changed")
            _strict_checker_verified(checker_stdout, checker_stderr)
        artifacts = _existing_artifact_map(destination)
        if artifacts != first_artifacts:
            raise RuntimeError("output artifact set changed during binding")
    except Exception as error:
        status = "FINAL_OUTPUT_VALIDATION_NONCLAIM"
        claim_status = "NO_MATHEMATICAL_CLAIM"
        semantic_checks = {}
        record_failure(error)
        artifacts = {}
    outcome = {
        "schema": "gamma-theta-hole5-binary-production-outcome-v1",
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "claim_status": claim_status,
        "package_manifest_sha256": expected_manifest_hash,
        "cnf_sha256": EXPECTED_DERIVED_CNF_SHA256,
        "run_config_sha256": sha256_bytes(run_config_payload),
        "solver": _child_record(solver),
        "parser": _child_record(parser_child),
        "checker": _child_record(checker_child),
        "parser_report": parser_report,
        "disk_gates": disk_gates,
        "semantic_checks": semantic_checks,
        "failures": failures,
        "artifacts": artifacts,
    }
    _write_new_file(
        destination / OUTCOME_NAME, canonical_json_bytes(outcome)
    )
    _fsync_directory(destination)
    return outcome


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="bounded binary-proof production for hole5 S6 package"
    )
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--source-package", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--expected-package-manifest-sha256", required=True
    )
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--solver-seconds", type=int, default=600)
    parser.add_argument("--parser-seconds", type=int, default=600)
    parser.add_argument("--checker-seconds", type=int, default=600)
    parser.add_argument("--solver-memory-mib", type=int, default=1_024)
    parser.add_argument("--parser-memory-mib", type=int, default=512)
    parser.add_argument("--checker-memory-mib", type=int, default=4_096)
    parser.add_argument("--file-limit-mib", type=int, default=512)
    parser.add_argument(
        "--disk-reserve-mib",
        type=int,
        default=MIN_DISK_RESERVE_MIB,
    )
    parser.add_argument("--validation-gate", action="store_true")
    parser.add_argument("--hostile-audit-gate", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _build_parser().parse_args(argv)
    outcome = run_production(
        package_directory=arguments.package,
        source_package_directory=arguments.source_package,
        output_directory=arguments.output_dir,
        expected_package_manifest_sha256=(
            arguments.expected_package_manifest_sha256
        ),
        expected_head_commit=arguments.expected_head,
        cadical_path=arguments.cadical,
        drat_trim_path=arguments.drat_trim,
        seed=arguments.seed,
        solver_seconds=arguments.solver_seconds,
        parser_seconds=arguments.parser_seconds,
        checker_seconds=arguments.checker_seconds,
        solver_memory_mib=arguments.solver_memory_mib,
        parser_memory_mib=arguments.parser_memory_mib,
        checker_memory_mib=arguments.checker_memory_mib,
        file_limit_mib=arguments.file_limit_mib,
        disk_reserve_mib=arguments.disk_reserve_mib,
        validation_gate=arguments.validation_gate,
        hostile_audit_gate=arguments.hostile_audit_gate,
    )
    print(json.dumps(outcome, allow_nan=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
