"""Exact v3 fixtures and hostile tests for the independent aggregate auditor.

The fixture is reconstructed from the published file contracts.  It imports
no production runner, search, synthesis, or shared transition implementation.
"""

from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import replace
from hashlib import sha256
from itertools import product
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import unittest

from verifier_k4_aggregate.checker import (
    AGGREGATE_REPORT_SCHEMA,
    AGGREGATE_REPORT_SCHEMA_VERSION,
    AuditError,
    AuditPolicy,
    FIXTURE_SUCCESS_STATUS,
    FrozenScope,
    PRODUCTION_SCOPE,
    ResourceGateError,
    _CampaignHeavyChildLock,
    _scan_binary_drat,
    _strict_forward_success,
    _strict_lrat_success,
    _strict_normalizer_success,
    _validate_normalization_report,
    _validate_passing_resource_report,
    audit_run,
    static_audit,
)
from verifier_k4_aggregate.parent_reconstruction import reconstruct_parent


CAMPAIGN = Path(__file__).resolve().parents[1]
PARENT = b"p cnf 4 2\n1 0\n-1 0\n"
LRAT = b"7 0 1 2 0\n"
BINARY_EMPTY_ADDITION = b"a\x00"
PIPELINE = "binary-drat-raw-forward-normalize-rup-forward-backward-lrat-v3"
RSS_UNIT = "bytes" if sys.platform == "darwin" else "KiB"


def canonical(value: object, *, compact: bool = False) -> bytes:
    options: dict[str, object] = {
        "allow_nan": False,
        "ensure_ascii": True,
        "sort_keys": True,
    }
    if compact:
        options["separators"] = (",", ":")
    else:
        options["indent"] = 2
    return (json.dumps(value, **options) + "\n").encode("utf-8")


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical(value))


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text("utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not an object")
    return value


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def binding(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {
        "path": str(path.resolve()),
        "sha256": sha256(payload).hexdigest(),
        "size_bytes": len(payload),
    }


def command_hash(command: list[str]) -> str:
    return sha256(canonical(command, compact=True)).hexdigest()


def tool_record(
    role: str,
    path: Path,
    archive: Path,
    *,
    commit: str,
    version: str | None,
) -> dict[str, object]:
    return {
        "role": role,
        "path": str(path.resolve()),
        "sha256": digest(path),
        "source_archive_path": str(archive.resolve()),
        "source_archive_sha256": digest(archive),
        "commit": commit,
        "version": version,
    }


def leaf_bytes(literals: list[int]) -> bytes:
    return (
        b"p cnf 4 6\n"
        + PARENT.split(b"\n", 1)[1]
        + b"".join(f"{literal} 0\n".encode("ascii") for literal in literals)
    )


def fixture_scope(parent_manifest: bytes) -> FrozenScope:
    cadical = CAMPAIGN / "tools/cadical_3_0_1/build/cadical"
    drat = CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim"
    lrat = CAMPAIGN / "tools/drat_trim_2023_05_22/lrat-check"
    cadical_archive = CAMPAIGN / "tools/cadical_3_0_1.tar.gz"
    drat_archive = CAMPAIGN / "tools/drat_trim_2023_05_22.tar.gz"
    return FrozenScope(
        scope_id="independent-v3-small-contradiction-fixture",
        production=False,
        campaign_root=CAMPAIGN,
        parent_sha256=sha256(PARENT).hexdigest(),
        parent_manifest_sha256=sha256(parent_manifest).hexdigest(),
        parent_size_bytes=len(PARENT),
        variable_count=4,
        parent_clause_count=2,
        parent_literal_count=2,
        cube_variables=(1, 2, 3, 4),
        cube_labels=("x1", "x2", "x3", "x4"),
        cadical_sha256=digest(cadical),
        drat_trim_sha256=digest(drat),
        lrat_check_sha256=digest(lrat),
        cadical_archive_sha256=digest(cadical_archive),
        drat_archive_sha256=digest(drat_archive),
    )


def child_record(
    command: list[str],
    executable_hash: str,
    exit_code: int,
    stdout: Path,
    stderr: Path,
    *,
    wall_limit: int,
    memory_limit: int,
) -> dict[str, object]:
    return {
        "command": command,
        "command_sha256": command_hash(command),
        "executable_sha256_before": executable_hash,
        "executable_sha256_after": executable_hash,
        "exit_code": exit_code,
        "termination_signal": None,
        "timed_out": False,
        "memory_limit_exceeded": False,
        "started_unix_ns": 10_000,
        "finished_unix_ns": 20_000,
        "wall_seconds": 0.01,
        "user_cpu_seconds": 0.001,
        "system_cpu_seconds": 0.001,
        "maximum_resident_set_size_mib": 1.0,
        "maximum_resident_set_size_raw": 1,
        "maximum_resident_set_size_raw_unit": RSS_UNIT,
        "peak_polled_resident_set_size_mib": 1.0,
        "available_memory_before_bytes": 1 << 30,
        "wall_limit_seconds": wall_limit,
        "memory_limit_mib": memory_limit,
        "file_limit_mib": 16,
        "stdout_path": str(stdout.resolve()),
        "stdout_sha256": digest(stdout),
        "stderr_path": str(stderr.resolve()),
        "stderr_sha256": digest(stderr),
    }


def expected_commands(
    case: dict[str, object],
    attempt: Path,
) -> dict[str, list[str]]:
    cadical = CAMPAIGN / "tools/cadical_3_0_1/build/cadical"
    drat = CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim"
    lrat = CAMPAIGN / "tools/drat_trim_2023_05_22/lrat-check"
    python = Path(sys.executable).resolve()
    instance = (attempt / "instance.cnf").resolve()
    raw = (attempt / "proof.raw.bdrat").resolve()
    normalized = (attempt / "proof.normalized.rup.bdrat").resolve()
    report = (attempt / "normalization-report.json").resolve()
    converted = (attempt / "proof.converted.lrat").resolve()
    return {
        "solver": [
            str(cadical.resolve()),
            f"--seed={case['seed']}",
            "--binary",
            "--no-colors",
            "-q",
            "-t",
            "30",
            "-w",
            str((attempt / "solver.result").resolve()),
            str(instance),
            str(raw),
        ],
        "raw_forward": [
            str(drat.resolve()),
            str(instance),
            str(raw),
            "-i",
            "-f",
            "-W",
            "-t",
            "30",
        ],
        "normalizer": [
            str(python),
            str(
                (
                    CAMPAIGN
                    / "src/search/k4_production/normalize_bdrat.py"
                ).resolve()
            ),
            "--input",
            str(raw),
            "--output",
            str(normalized),
            "--report",
            str(report),
            "--max-variable",
            "4",
        ],
        "normalized_forward": [
            str(drat.resolve()),
            str(instance),
            str(normalized),
            "-i",
            "-f",
            "-W",
            "-U",
            "-t",
            "30",
        ],
        "lrat_conversion": [
            str(drat.resolve()),
            str(instance),
            str(normalized),
            "-i",
            "-W",
            "-U",
            "-L",
            str(converted),
            "-t",
            "30",
        ],
        "lrat_check": [
            str(lrat.resolve()),
            str(instance),
            str(converted),
        ],
    }


def resource_report(phase: str, memory_limit_mib: int) -> dict[str, object]:
    required_memory = (memory_limit_mib + 512) << 20
    required_disk = (4096 + 17 * 16 + 64) << 20
    return {
        "schema": "gamma-theta-k4-resource-gate-v1",
        "phase": phase,
        "checked_unix_ns": 5_000,
        "load_average_one_minute": 0.0,
        "load_ceiling": 1000.0,
        "available_memory_bytes": 8 << 30,
        "required_memory_bytes": required_memory,
        "free_disk_bytes": 16 << 30,
        "required_free_disk_bytes": required_disk,
        "worst_case_live_file_slots": 17,
        "checks": {"load": True, "memory": True, "disk": True},
        "probe_errors": [],
        "passed": True,
    }


def normalization_report(raw: Path, normalized: Path) -> dict[str, object]:
    return {
        "schema": "gamma-theta-order12-k4-binary-drat-normalization-v1",
        "schema_version": 1,
        "policy": "canonical-additions-only-unique-empty-full-stream-v1",
        "claim_status": "TRANSFORMATION_ONLY_NO_PROOF_CLAIM",
        "max_variable_allowed": 4,
        "max_variable_observed": 0,
        "record_counts": {
            "total": 1,
            "additions": 1,
            "deletions": 0,
            "post_empty_deletions": 0,
            "literals": 0,
        },
        "empty_addition_record_index": 1,
        "input": binding(raw),
        "output": binding(normalized),
    }


def make_attempt(
    run: Path,
    case: dict[str, object],
    manifest_hash: str,
    partition_hash: str,
    scope: FrozenScope,
) -> tuple[str, str]:
    case_id = str(case["case_id"])
    attempt = run / "cases" / f"case-{case_id}" / "attempt-000001"
    attempt.mkdir()
    (attempt / "instance.cnf").write_bytes(
        leaf_bytes(list(case["cube_literals"]))
    )
    commands = expected_commands(case, attempt)
    config = {
        "schema": "gamma-theta-order12-k4-attempt-config-v3",
        "schema_version": 3,
        "proof_pipeline": PIPELINE,
        "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
        "construction_status": "ORIGINAL_PRE_RESERVATION",
        "case_id": case_id,
        "attempt_number": 1,
        "seed": case["seed"],
        "cube_literals": case["cube_literals"],
        "case_cnf_sha256": case["cnf_sha256"],
        "run_manifest_sha256": manifest_hash,
        "partition_sha256": partition_hash,
        "solver_command": commands["solver"],
        "raw_forward_command": commands["raw_forward"],
        "normalizer_command": commands["normalizer"],
        "normalized_forward_command": commands["normalized_forward"],
        "lrat_conversion_command": commands["lrat_conversion"],
        "lrat_check_command": commands["lrat_check"],
        "created_unix_ns": 1_000,
    }
    write_json(attempt / "attempt-config.json", config)

    phase_files = {
        "solver": "resource-solver.json",
        "raw-forward": "resource-raw-forward.json",
        "normalizer": "resource-normalizer.json",
        "normalized-forward": "resource-normalized-forward.json",
        "lrat-conversion": "resource-lrat-conversion.json",
        "lrat-check": "resource-lrat-check.json",
    }
    for phase, filename in phase_files.items():
        write_json(attempt / filename, resource_report(phase, 64))

    outputs = {
        "solver.stdout": b"",
        "solver.stderr": b"",
        "solver.result": b"s UNSATISFIABLE\n",
        "proof.raw.bdrat": BINARY_EMPTY_ADDITION,
        "raw-forward.stdout": b"s VERIFIED\n",
        "raw-forward.stderr": b"",
        "normalizer.stdout": b"s NORMALIZED\n",
        "normalizer.stderr": b"",
        "proof.normalized.rup.bdrat": BINARY_EMPTY_ADDITION,
        "normalized-forward.stdout": b"s VERIFIED\n",
        "normalized-forward.stderr": b"",
        "lrat-conversion.stdout": b"s VERIFIED\n",
        "lrat-conversion.stderr": b"",
        "proof.converted.lrat": LRAT,
        "lrat-check.stdout": b"c VERIFIED\n",
        "lrat-check.stderr": b"",
    }
    for filename, payload in outputs.items():
        (attempt / filename).write_bytes(payload)
    write_json(
        attempt / "normalization-report.json",
        normalization_report(
            attempt / "proof.raw.bdrat",
            attempt / "proof.normalized.rup.bdrat",
        ),
    )

    python_hash = digest(Path(sys.executable).resolve())
    children = {
        "solver": child_record(
            commands["solver"],
            scope.cadical_sha256,
            20,
            attempt / "solver.stdout",
            attempt / "solver.stderr",
            wall_limit=30,
            memory_limit=64,
        ),
        "raw_forward": child_record(
            commands["raw_forward"],
            scope.drat_trim_sha256,
            0,
            attempt / "raw-forward.stdout",
            attempt / "raw-forward.stderr",
            wall_limit=30,
            memory_limit=64,
        ),
        "normalizer": child_record(
            commands["normalizer"],
            python_hash,
            0,
            attempt / "normalizer.stdout",
            attempt / "normalizer.stderr",
            wall_limit=30,
            memory_limit=64,
        ),
        "normalized_forward": child_record(
            commands["normalized_forward"],
            scope.drat_trim_sha256,
            0,
            attempt / "normalized-forward.stdout",
            attempt / "normalized-forward.stderr",
            wall_limit=30,
            memory_limit=64,
        ),
        "lrat_conversion": child_record(
            commands["lrat_conversion"],
            scope.drat_trim_sha256,
            0,
            attempt / "lrat-conversion.stdout",
            attempt / "lrat-conversion.stderr",
            wall_limit=30,
            memory_limit=64,
        ),
        "lrat_check": child_record(
            commands["lrat_check"],
            scope.lrat_check_sha256,
            0,
            attempt / "lrat-check.stdout",
            attempt / "lrat-check.stderr",
            wall_limit=30,
            memory_limit=64,
        ),
    }
    certificate = {
        "schema": "gamma-theta-order12-k4-leaf-lrat-certificate-v3",
        "schema_version": 3,
        "proof_pipeline": PIPELINE,
        "leaf_status": "UNSAT_LRAT_VERIFIED",
        "aggregate_status": (
            "NO_AGGREGATE_CLAIM_PENDING_INDEPENDENT_COVERAGE_AUDIT"
        ),
        "case_id": case_id,
        "cube_literals": case["cube_literals"],
        "case_cnf": binding(attempt / "instance.cnf"),
        "raw_solver_result": binding(attempt / "solver.result"),
        "raw_binary_drat": binding(attempt / "proof.raw.bdrat"),
        "normalized_binary_rup": binding(
            attempt / "proof.normalized.rup.bdrat"
        ),
        "normalization_report": binding(
            attempt / "normalization-report.json"
        ),
        "converted_lrat": binding(attempt / "proof.converted.lrat"),
        "solver_resource": binding(attempt / "resource-solver.json"),
        "raw_forward_resource": binding(
            attempt / "resource-raw-forward.json"
        ),
        "normalizer_resource": binding(
            attempt / "resource-normalizer.json"
        ),
        "normalized_forward_resource": binding(
            attempt / "resource-normalized-forward.json"
        ),
        "lrat_conversion_resource": binding(
            attempt / "resource-lrat-conversion.json"
        ),
        "lrat_check_resource": binding(
            attempt / "resource-lrat-check.json"
        ),
        **children,
        "solver_stdout": binding(attempt / "solver.stdout"),
        "solver_stderr": binding(attempt / "solver.stderr"),
        "raw_forward_stdout": binding(attempt / "raw-forward.stdout"),
        "raw_forward_stderr": binding(attempt / "raw-forward.stderr"),
        "normalizer_stdout": binding(attempt / "normalizer.stdout"),
        "normalizer_stderr": binding(attempt / "normalizer.stderr"),
        "normalized_forward_stdout": binding(
            attempt / "normalized-forward.stdout"
        ),
        "normalized_forward_stderr": binding(
            attempt / "normalized-forward.stderr"
        ),
        "lrat_conversion_stdout": binding(
            attempt / "lrat-conversion.stdout"
        ),
        "lrat_conversion_stderr": binding(
            attempt / "lrat-conversion.stderr"
        ),
        "lrat_check_stdout": binding(attempt / "lrat-check.stdout"),
        "lrat_check_stderr": binding(attempt / "lrat-check.stderr"),
    }
    write_json(attempt / "certificate.json", certificate)
    inventory = {
        path.name: binding(path)
        for path in sorted(attempt.iterdir())
        if path.name != "outcome.json"
    }
    outcome = {
        "schema": "gamma-theta-order12-k4-attempt-outcome-v2",
        "schema_version": 2,
        "proof_pipeline": PIPELINE,
        "case_id": case_id,
        "attempt_number": 1,
        "status": "UNSAT_LRAT_VERIFIED",
        "mathematical_claim": "LEAF_UNSAT_AFTER_LRAT_REPLAY",
        "aggregate_claim": "NONE",
        "details": {
            "certificate": binding(attempt / "certificate.json"),
            **children,
        },
        "artifact_inventory": inventory,
        "finished_unix_ns": 30_000,
    }
    write_json(attempt / "outcome.json", outcome)
    return digest(attempt / "attempt-config.json"), digest(attempt / "outcome.json")


def case_states(cases: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "case_id": case["case_id"],
            "status": "PENDING",
            "attempt_count": 0,
            "active_attempt": None,
            "last_completed_outcome_sha256": None,
        }
        for case in cases
    ]


def aggregate_status(states: list[dict[str, object]]) -> str:
    statuses = [state["status"] for state in states]
    if all(status == "UNSAT_LRAT_VERIFIED" for status in statuses):
        return "ALL_LEAVES_VERIFIED_PENDING_INDEPENDENT_COVERAGE_AUDIT"
    if "RUNNING_UNFINISHED_NONCLAIM" in statuses:
        return "INCOMPLETE_ACTIVE_NONCLAIM"
    return "INCOMPLETE_NONCLAIM"


def checkpoint(
    run: Path,
    sequence: int,
    previous: str | None,
    manifest_hash: str,
    partition_hash: str,
    states: list[dict[str, object]],
    event: dict[str, object],
) -> str:
    payload = {
        "schema": "gamma-theta-order12-k4-production-checkpoint-v1",
        "schema_version": 1,
        "sequence": sequence,
        "previous_checkpoint_sha256": previous,
        "run_manifest_sha256": manifest_hash,
        "partition_sha256": partition_hash,
        "cases": states,
        "aggregate_status": aggregate_status(states),
        "claim_boundary": (
            "No aggregate SAT/UNSAT claim is made. SAT is candidate-only; "
            "all verified UNSAT leaves still require an independent coverage "
            "and proof replay."
        ),
        "event": event,
        "written_unix_ns": 100_000 + sequence,
    }
    path = run / "checkpoints" / f"checkpoint-{sequence:06d}.json"
    write_json(path, payload)
    return digest(path)


def make_fixture(
    directory: Path,
    *,
    completed_count: int = 16,
) -> tuple[Path, FrozenScope]:
    run = (directory / "run").resolve()
    run.mkdir()
    (run / "checkpoints").mkdir()
    (run / "cases").mkdir()
    if completed_count:
        (run / "run.lock").write_bytes(b"")
    (run / "parent.cnf").write_bytes(PARENT)
    parent_manifest_value = {
        "claim_status": "NO_MATHEMATICAL_CLAIM",
        "cnf_sha256": sha256(PARENT).hexdigest(),
        "cnf_size_bytes": len(PARENT),
        "variable_count": 4,
        "clause_count": 2,
        "literal_count": 2,
    }
    parent_manifest = canonical(parent_manifest_value)
    (run / "parent-generator-manifest.json").write_bytes(parent_manifest)
    scope = fixture_scope(parent_manifest)

    cases: list[dict[str, object]] = []
    for index, bits in enumerate(product((0, 1), repeat=4)):
        literals = [
            variable if bit else -variable
            for variable, bit in zip((1, 2, 3, 4), bits, strict=True)
        ]
        leaf = leaf_bytes(literals)
        case_id = "".join(map(str, bits))
        cases.append(
            {
                "case_id": case_id,
                "case_index": index,
                "cube_bits": list(bits),
                "cube_literals": literals,
                "seed": 100 + index,
                "cnf_sha256": sha256(leaf).hexdigest(),
                "cnf_size_bytes": len(leaf),
                "variable_count": 4,
                "clause_count": 6,
                "literal_count": 6,
            }
        )
        (run / "cases" / f"case-{case_id}").mkdir()
    partition = {
        "schema": "gamma-theta-order12-k4-boolean-cube-partition-v1",
        "schema_version": 1,
        "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
        "aggregate_terminal_status": (
            "ALL_LEAVES_VERIFIED_PENDING_INDEPENDENT_COVERAGE_AUDIT"
        ),
        "coverage_basis": (
            "All 2^4 total assignments to four distinct Boolean variables; "
            "every total parent assignment belongs to exactly one cube."
        ),
        "parent_cnf_sha256": scope.parent_sha256,
        "cube_variables": [1, 2, 3, 4],
        "cube_variable_labels": ["x1", "x2", "x3", "x4"],
        "case_count": 16,
        "cases": cases,
    }
    write_json(run / "partition.json", partition)

    cadical = CAMPAIGN / "tools/cadical_3_0_1/build/cadical"
    drat = CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim"
    lrat = CAMPAIGN / "tools/drat_trim_2023_05_22/lrat-check"
    cadical_archive = CAMPAIGN / "tools/cadical_3_0_1.tar.gz"
    drat_archive = CAMPAIGN / "tools/drat_trim_2023_05_22.tar.gz"
    python = Path(sys.executable).resolve()
    records: list[object] = []
    manifest = {
        "schema": "gamma-theta-order12-k4-production-run-v1",
        "schema_version": 1,
        "proof_pipeline": PIPELINE,
        "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
        "run_directory": str(run),
        "campaign_root": str(CAMPAIGN.resolve()),
        "original_parent_cnf": binding(run / "parent.cnf"),
        "original_parent_generator_manifest": binding(
            run / "parent-generator-manifest.json"
        ),
        "retained_parent_cnf": binding(run / "parent.cnf"),
        "retained_parent_generator_manifest": binding(
            run / "parent-generator-manifest.json"
        ),
        "partition": binding(run / "partition.json"),
        "base_seed": 100,
        "limits": {
            "solver_wall_seconds": 30,
            "converter_wall_seconds": 30,
            "checker_wall_seconds": 30,
            "solver_memory_mib": 64,
            "postprocess_memory_mib": 64,
            "file_limit_mib": 16,
            "disk_reserve_mib": 4096,
            "memory_reserve_mib": 512,
            "load_max": 1000.0,
            "maximum_responsive_child_memory_mib": 12_288,
            "worst_case_live_file_slots": 17,
        },
        "hardware": {
            "logical_cpu_count": 10,
            "physical_memory_bytes": 16 << 30,
            "machine": "fixture",
            "processor": "fixture",
            "platform": "fixture",
            "python_executable": str(python),
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
        },
        "runtime_sources": {
            "head_at_creation": "0" * 40,
            "global_worktree_cleanliness_required": False,
            "records": records,
            "source_set_sha256": sha256(canonical(records)).hexdigest(),
        },
        "tools": {
            "cadical": tool_record(
                "cadical",
                cadical,
                cadical_archive,
                commit="c60730422e758ef1cebe7aeddf2dda31c996bf04",
                version="3.0.1",
            ),
            "drat_trim": tool_record(
                "drat-trim",
                drat,
                drat_archive,
                commit="2e5e29cb0019d5cfd547d4208dca1b3ec290349f",
                version=None,
            ),
            "lrat_check": tool_record(
                "lrat-check",
                lrat,
                drat_archive,
                commit="2e5e29cb0019d5cfd547d4208dca1b3ec290349f",
                version=None,
            ),
            "normalizer_python": {
                "role": "normalizer-python-runtime",
                "path": str(python),
                "sha256": digest(python),
                "implementation": platform.python_implementation(),
                "version": platform.python_version(),
            },
        },
        "normalized_resume_invocation": [
            "/usr/bin/env",
            f"PYTHONPATH={CAMPAIGN / 'src'}",
            str(python),
            "-m",
            "search.k4_production",
            "run-next",
            "--production-gate-open",
            "--run-dir",
            str(run),
        ],
        "created_unix_ns": 1,
    }
    write_json(run / "run-manifest.json", manifest)
    manifest_hash = digest(run / "run-manifest.json")
    partition_hash = digest(run / "partition.json")
    configurations = [
        make_attempt(
            run,
            case,
            manifest_hash,
            partition_hash,
            scope,
        )
        for case in cases[:completed_count]
    ]

    states = case_states(cases)
    previous = checkpoint(
        run,
        0,
        None,
        manifest_hash,
        partition_hash,
        deepcopy(states),
        {
            "kind": "INITIALIZED_NO_SOLVER_RUN",
            "base_seed": 100,
            "case_count": 16,
        },
    )
    sequence = 1
    for index, (config_hash, outcome_hash) in enumerate(configurations):
        state = states[index]
        state["status"] = "RUNNING_UNFINISHED_NONCLAIM"
        state["attempt_count"] = 1
        state["active_attempt"] = 1
        previous = checkpoint(
            run,
            sequence,
            previous,
            manifest_hash,
            partition_hash,
            deepcopy(states),
            {
                "kind": "ATTEMPT_RESERVED_NO_RESULT",
                "case_id": state["case_id"],
                "attempt_number": 1,
                "attempt_config_sha256": config_hash,
            },
        )
        sequence += 1
        state["status"] = "UNSAT_LRAT_VERIFIED"
        state["active_attempt"] = None
        state["last_completed_outcome_sha256"] = outcome_hash
        previous = checkpoint(
            run,
            sequence,
            previous,
            manifest_hash,
            partition_hash,
            deepcopy(states),
            {
                "kind": "ATTEMPT_COMPLETED",
                "case_id": state["case_id"],
                "attempt_number": 1,
                "outcome_status": "UNSAT_LRAT_VERIFIED",
                "outcome_sha256": outcome_hash,
            },
        )
        sequence += 1
    return run, scope


def policy() -> AuditPolicy:
    return AuditPolicy(
        wall_seconds=30,
        memory_mib=64,
        file_limit_mib=4,
        load_max=1000.0,
        memory_reserve_mib=512,
        disk_reserve_mib=512,
        enforce_live_resource_gates=False,
    )


class AggregateVerifierV3Tests(unittest.TestCase):
    def test_complete_fixture_checkpoints_and_resumes_sixteen(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run, scope = make_fixture(root)
            ledger = root / "external-replays"
            first = audit_run(
                run,
                scope=scope,
                policy=policy(),
                replay_directory=ledger,
            )
            hashes_before = {
                path.name: digest(path)
                for path in ledger.glob("case-*.json")
            }
            second = audit_run(
                run,
                scope=scope,
                policy=policy(),
                replay_directory=ledger,
            )
            hashes_after = {
                path.name: digest(path)
                for path in ledger.glob("case-*.json")
            }
        self.assertEqual(first["schema"], AGGREGATE_REPORT_SCHEMA)
        self.assertEqual(
            first["schema_version"], AGGREGATE_REPORT_SCHEMA_VERSION
        )
        self.assertEqual(first["status"], FIXTURE_SUCCESS_STATUS)
        self.assertIn(
            "certifies UNSAT of the exact frozen 16-leaf partition",
            first["claim_boundary"],
        )
        self.assertEqual(first["fresh_lrat_executed_this_invocation"], 16)
        self.assertEqual(first["fresh_lrat_resumed_from_ledger"], 0)
        self.assertEqual(second["fresh_lrat_executed_this_invocation"], 0)
        self.assertEqual(second["fresh_lrat_resumed_from_ledger"], 16)
        self.assertEqual(hashes_before, hashes_after)
        self.assertEqual(first["pairwise_disjoint_pair_count"], 120)
        self.assertEqual(
            [row["case_id"] for row in first["fresh_lrat_replays"]],
            ["".join(map(str, bits)) for bits in product((0, 1), repeat=4)],
        )

    def test_exact_incomplete_one_of_sixteen_status(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run, scope = make_fixture(root, completed_count=1)
            report = audit_run(
                run,
                scope=scope,
                policy=policy(),
                replay_directory=root / "external-replays",
            )
        self.assertEqual(
            report["status"], "INCOMPLETE_1_OF_16_VERIFIED_NONCLAIM"
        )
        self.assertEqual(
            report["claim_boundary"],
            (
                "No aggregate SAT/UNSAT claim is made. This report validates "
                "exactly 1 of 16 frozen leaves; 15 remain pending."
            ),
        )
        self.assertEqual(report["verified_leaf_count"], 1)
        self.assertEqual(report["pending_leaf_count"], 15)
        self.assertEqual(report["fresh_lrat_success_count"], 1)

    def test_zero_leaf_run_is_exactly_incomplete_without_checker(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run, scope = make_fixture(
                Path(temporary).resolve(), completed_count=0
            )
            report = audit_run(run, scope=scope, policy=policy())
        self.assertEqual(
            report["status"], "INCOMPLETE_0_OF_16_VERIFIED_NONCLAIM"
        )
        self.assertEqual(report["fresh_lrat_success_count"], 0)

    def test_external_record_tampering_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run, scope = make_fixture(root, completed_count=1)
            ledger = root / "external-replays"
            audit_run(
                run,
                scope=scope,
                policy=policy(),
                replay_directory=ledger,
            )
            path = ledger / "case-0000.json"
            record = read_json(path)
            result = record["result"]
            if not isinstance(result, dict):
                raise AssertionError("fixture replay result changed shape")
            result["stdout_base64"] = "YyBWRVJJRklFRAo=A"
            write_json(path, record)
            with self.assertRaises(AuditError):
                audit_run(
                    run,
                    scope=scope,
                    policy=policy(),
                    replay_directory=ledger,
                )

    def test_replay_policy_change_cannot_reuse_old_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run, scope = make_fixture(root, completed_count=1)
            ledger = root / "external-replays"
            audit_run(
                run,
                scope=scope,
                policy=policy(),
                replay_directory=ledger,
            )
            with self.assertRaises(AuditError):
                audit_run(
                    run,
                    scope=scope,
                    policy=replace(policy(), wall_seconds=29),
                    replay_directory=ledger,
                )

    def test_missing_decisive_artifact_is_rejected_statically(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run, scope = make_fixture(
                Path(temporary).resolve(), completed_count=1
            )
            (
                run / "cases/case-0000/attempt-000001/proof.converted.lrat"
            ).unlink()
            with self.assertRaises(AuditError):
                static_audit(run, scope=scope)

    def test_v2_attempt_schema_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run, scope = make_fixture(
                Path(temporary).resolve(), completed_count=1
            )
            path = run / "cases/case-0000/attempt-000001/attempt-config.json"
            config = read_json(path)
            config["schema"] = "gamma-theta-order12-k4-attempt-config-v2"
            write_json(path, config)
            with self.assertRaises(AuditError):
                static_audit(run, scope=scope)

    def test_boolean_schema_version_is_not_integer_one(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run, scope = make_fixture(
                Path(temporary).resolve(), completed_count=0
            )
            path = run / "run-manifest.json"
            manifest = read_json(path)
            manifest["schema_version"] = True
            write_json(path, manifest)
            with self.assertRaises(AuditError):
                static_audit(run, scope=scope)

    def test_unexpected_root_fifo_is_rejected_without_opening(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run, scope = make_fixture(
                Path(temporary).resolve(), completed_count=0
            )
            os.mkfifo(run / "hostile-fifo")
            with self.assertRaises(AuditError):
                static_audit(run, scope=scope)

    def test_child_record_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run, scope = make_fixture(
                Path(temporary).resolve(), completed_count=1
            )
            path = run / "cases/case-0000/attempt-000001/certificate.json"
            certificate = read_json(path)
            child = certificate["normalizer"]
            if not isinstance(child, dict):
                raise AssertionError("fixture normalizer child changed shape")
            child["memory_limit_exceeded"] = True
            write_json(path, certificate)
            with self.assertRaises(AuditError):
                static_audit(run, scope=scope)

    def test_resource_report_semantics_are_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary).resolve() / "resource.json"
            report = resource_report("normalizer", 64)
            write_json(path, report)
            limits = {
                "memory_reserve_mib": 512,
                "disk_reserve_mib": 4096,
                "file_limit_mib": 16,
                "load_max": 1000.0,
            }
            _validate_passing_resource_report(
                path,
                phase="normalizer",
                memory_limit_mib=64,
                limits=limits,
            )
            report["probe_errors"] = ["probe failed"]
            write_json(path, report)
            with self.assertRaises(AuditError):
                _validate_passing_resource_report(
                    path,
                    phase="normalizer",
                    memory_limit_mib=64,
                    limits=limits,
                )

    def test_binary_drat_scanner_rejects_noncanonical_varint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary).resolve() / "proof.bdrat"
            path.write_bytes(b"a\x80\x00")
            with self.assertRaises(AuditError):
                _scan_binary_drat(
                    path,
                    maximum_variable=4,
                    role="hostile binary proof",
                )

    def test_normalization_report_binds_exact_addition_stream(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            raw = root / "raw.bdrat"
            normalized = root / "normalized.bdrat"
            report = root / "report.json"
            raw.write_bytes(BINARY_EMPTY_ADDITION)
            normalized.write_bytes(BINARY_EMPTY_ADDITION)
            parent_manifest = canonical(
                {
                    "claim_status": "NO_MATHEMATICAL_CLAIM",
                    "cnf_sha256": sha256(PARENT).hexdigest(),
                    "cnf_size_bytes": len(PARENT),
                    "variable_count": 4,
                    "clause_count": 2,
                    "literal_count": 2,
                }
            )
            scope = fixture_scope(parent_manifest)
            write_json(report, normalization_report(raw, normalized))
            _validate_normalization_report(report, raw, normalized, scope)
            normalized.write_bytes(b"a\x04\x00a\x00")
            with self.assertRaises(AuditError):
                _validate_normalization_report(report, raw, normalized, scope)

    def test_strict_output_parsers_reject_warnings(self) -> None:
        _strict_forward_success(b"s VERIFIED\n", b"", "forward")
        _strict_lrat_success(b"c VERIFIED\n", b"", "lrat")
        _strict_normalizer_success(b"s NORMALIZED\n", b"", "normalizer")
        with self.assertRaises(AuditError):
            _strict_forward_success(
                b"warning: tolerated\ns VERIFIED\n", b"", "forward"
            )
        with self.assertRaises(AuditError):
            _strict_lrat_success(
                b"warning: tolerated\nc VERIFIED\n", b"", "lrat"
            )
        with self.assertRaises(AuditError):
            _strict_normalizer_success(
                b"s NORMALIZED\nwarning\n", b"", "normalizer"
            )

    def test_custom_production_scope_is_sealed_out(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run, _ = make_fixture(
                Path(temporary).resolve(), completed_count=0
            )
            hostile = replace(PRODUCTION_SCOPE, scope_id="hostile-substitute")
            with self.assertRaises(AuditError):
                static_audit(run, scope=hostile)

    def test_campaign_heavy_child_lock_refuses_nested_owner(self) -> None:
        with _CampaignHeavyChildLock(CAMPAIGN):
            with self.assertRaises(ResourceGateError):
                with _CampaignHeavyChildLock(CAMPAIGN):
                    self.fail("nested heavy-child lock unexpectedly succeeded")

    def test_clean_room_parent_reconstruction_matches_frozen_scope(self) -> None:
        reconstructed = reconstruct_parent()
        self.assertEqual(
            sha256(reconstructed.payload).hexdigest(),
            PRODUCTION_SCOPE.parent_sha256,
        )
        self.assertEqual(
            (
                reconstructed.variable_count,
                reconstructed.clause_count,
                reconstructed.literal_count,
                reconstructed.cube_variables,
                reconstructed.cube_labels,
            ),
            (
                PRODUCTION_SCOPE.variable_count,
                PRODUCTION_SCOPE.parent_clause_count,
                PRODUCTION_SCOPE.parent_literal_count,
                PRODUCTION_SCOPE.cube_variables,
                PRODUCTION_SCOPE.cube_labels,
            ),
        )

    def test_runtime_imports_are_independent_by_ast(self) -> None:
        root = CAMPAIGN / "src/verifier_k4_aggregate"
        for path in sorted(root.glob("*.py")):
            tree = ast.parse(path.read_text("utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertFalse(
                            alias.name.startswith(("search", "synthesis")),
                            f"{path} imports {alias.name}",
                        )
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    self.assertFalse(
                        module.startswith(("search", "synthesis")),
                        f"{path} imports {module}",
                    )


if __name__ == "__main__":
    unittest.main()
