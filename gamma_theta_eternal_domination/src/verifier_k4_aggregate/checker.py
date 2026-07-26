"""Independent, fail-closed aggregate auditor for a future ``(12, 4)`` run.

This package deliberately imports no search, synthesis, production-runner, or
existing verifier module.  All parsing, leaf reconstruction, coverage checks,
checkpoint validation, binding checks, and bounded LRAT replay are implemented
here with the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha1, sha256
from itertools import combinations, product
import base64
import binascii
import json
import math
import os
from pathlib import Path
import re
import resource
import signal
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any, BinaryIO, Mapping, Sequence

import fcntl

from .parent_reconstruction import reconstruct_parent


VERIFIER = "independent-k4-aggregate-auditor-v3"
SCHEMA_VERSION = 1
AGGREGATE_REPORT_SCHEMA = "gamma-theta-order12-k4-aggregate-audit-report-v3"
AGGREGATE_REPORT_SCHEMA_VERSION = 3
REPLAY_MANIFEST_SCHEMA = "gamma-theta-order12-k4-aggregate-replay-ledger-v1"
REPLAY_RECORD_SCHEMA = "gamma-theta-order12-k4-aggregate-replay-record-v1"
REPLAY_SCHEMA_VERSION = 1
SUCCESS_STATUS = "CERTIFIED_FINITE_PENDING_MATHEMATICAL_SCOPE_ASSEMBLY"
FIXTURE_SUCCESS_STATUS = "PASS_TEST_FIXTURE_ONLY_NO_MATHEMATICAL_CLAIM"
FAILURE_STATUS = "NO_CERTIFIED_FINITE_RESULT"

RUN_MANIFEST_NAME = "run-manifest.json"
PARTITION_NAME = "partition.json"
PARENT_NAME = "parent.cnf"
PARENT_MANIFEST_NAME = "parent-generator-manifest.json"
CHECKPOINT_DIR_NAME = "checkpoints"
CASE_DIR_NAME = "cases"

RUN_SCHEMA = "gamma-theta-order12-k4-production-run-v1"
PARTITION_SCHEMA = "gamma-theta-order12-k4-boolean-cube-partition-v1"
CHECKPOINT_SCHEMA = "gamma-theta-order12-k4-production-checkpoint-v1"
ATTEMPT_CONFIG_SCHEMA = "gamma-theta-order12-k4-attempt-config-v3"
ATTEMPT_CONFIG_SCHEMA_VERSION = 3
ATTEMPT_OUTCOME_SCHEMA = "gamma-theta-order12-k4-attempt-outcome-v2"
ATTEMPT_OUTCOME_SCHEMA_VERSION = 2
LEAF_CERTIFICATE_SCHEMA = "gamma-theta-order12-k4-leaf-lrat-certificate-v3"
LEAF_CERTIFICATE_SCHEMA_VERSION = 3
PROOF_PIPELINE_ID = (
    "binary-drat-raw-forward-normalize-rup-forward-backward-lrat-v3"
)
NORMALIZATION_SCHEMA = "gamma-theta-order12-k4-binary-drat-normalization-v1"
NORMALIZATION_POLICY = "canonical-additions-only-unique-empty-full-stream-v1"

FROZEN_PRODUCTION_RUNNER_SHA256 = (
    "39d690edc72d852b36b637497ef44463ebd80a51d3b13479d96e31becb939cfb"
)
FROZEN_RUNTIME_SOURCE_SET_SHA256 = (
    "4c8988b1e7967e2e4d59f73e0b6323900266c5b23fc94e0e19fc5a68fbc2921e"
)

RUN_CLAIM = "NO_SAT_OR_UNSAT_CLAIM"
LEAF_UNSAT = "UNSAT_LRAT_VERIFIED"
RUNNER_TERMINAL = "ALL_LEAVES_VERIFIED_PENDING_INDEPENDENT_COVERAGE_AUDIT"

CHECKPOINT_RE = re.compile(r"checkpoint-([0-9]{6})\.json\Z")
CASE_RE = re.compile(r"case-([01]{4})\Z")
ATTEMPT_RE = re.compile(r"attempt-([0-9]{6})\Z")
HEX64_RE = re.compile(r"[0-9a-f]{64}\Z")

MAX_JSON_BYTES = 32 << 20
MAX_REPORT_BYTES = 64 << 20
MAX_REPLAY_OUTPUT_BYTES = 1 << 20
MAX_REPLAY_WALL_SECONDS = 1_800
MAX_REPLAY_MEMORY_MIB = 4_096
MIN_DISK_RESERVE_MIB = 512
MIN_MEMORY_RESERVE_MIB = 512
WORST_CASE_LIVE_FILE_SLOTS = 17
DISK_METADATA_ALLOWANCE_MIB = 64
MAX_UNSIGNED_VARINT_BYTES = 10
HEAVY_CHILD_LOCK_NAME = "gamma-theta-k3-heavy-child"
REPLAY_MANIFEST_NAME = "replay-manifest.json"
REPLAY_LOCK_NAME = "replay.lock"
REPLAY_RECORD_RE = re.compile(r"case-([01]{4})\.json\Z")

RUNTIME_SOURCE_PATHS = (
    "src/search/k4_production/__init__.py",
    "src/search/k4_production/__main__.py",
    "src/search/k4_production/normalize_bdrat.py",
    "src/search/k4_production/runner.py",
    "src/synthesis_k3/cegar.py",
    "src/synthesis_k3/coloring.py",
    "src/synthesis_k3/encoding.py",
    "src/synthesis_k3/generate.py",
    "math/lemmas/order12_k4_partition_plan.md",
)
FROZEN_RUNTIME_SOURCE_RECORDS = (
    (
        "src/search/k4_production/__init__.py",
        "9bee968c763ef704d61bf6259e969cd7cffc4039",
        "d217fa6af4e7273a80cc63ee8ac812e83b6ce8ed64585fef6d2ef8a371dd2c67",
        478,
    ),
    (
        "src/search/k4_production/__main__.py",
        "3dd41c7c854230ceeaa2c0d5e33b6d3e291644c6",
        "a5d3245ca5614aa7b566a1a182d03b48fbc3c40c3ade4d56d9d8114b5dcb432d",
        148,
    ),
    (
        "src/search/k4_production/normalize_bdrat.py",
        "77a987d3c9c6d558b9d7185638cf2b9e6baccc65",
        "07229fce9293a05fed3fa6ef3f96415eb48ea4b0cdd8e9a329620017d2bced99",
        13_157,
    ),
    (
        "src/search/k4_production/runner.py",
        "dd4a7b37c040dd70596d75ce9b51301c8cb0905d",
        FROZEN_PRODUCTION_RUNNER_SHA256,
        180_633,
    ),
    (
        "src/synthesis_k3/cegar.py",
        "d6c4436ba2c3bf2660aebbdcce2ebe0e40973e82",
        "411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c",
        179_763,
    ),
    (
        "src/synthesis_k3/coloring.py",
        "56f40a4e3716c9bd19880b9a507a37865a65e6d7",
        "9791599aaca6b9f7ec5e6fed8cfce41a5c5bec825a350e5e493a0d1aa06d3713",
        3_963,
    ),
    (
        "src/synthesis_k3/encoding.py",
        "f6ed2e25d399c944f1449b299839af23fcd05d06",
        "fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6",
        15_071,
    ),
    (
        "src/synthesis_k3/generate.py",
        "78bc7b85b3f88810f324120fd7cb6b51bcddfaed",
        "456029e08a199e3cc8d4aa6070e3209d6884901fc6c3db8486b80862614430e1",
        10_004,
    ),
    (
        "math/lemmas/order12_k4_partition_plan.md",
        "8680df36ae90c6be335124cebf35a17d59bfbe78",
        "f49a7ddfc3e7845b59fd9aa2f2938e0802f0d100241819b8b24953d8009b9ad4",
        8_897,
    ),
)

VERIFIER_RUNTIME_SOURCE_PATHS = (
    "src/verifier_k4_aggregate/__init__.py",
    "src/verifier_k4_aggregate/__main__.py",
    "src/verifier_k4_aggregate/checker.py",
    "src/verifier_k4_aggregate/cli.py",
    "src/verifier_k4_aggregate/parent_reconstruction.py",
)
ACCEPTED_HISTORICAL_VERIFIER_SOURCE_VECTORS = (
    (
        "66cdb5007d2283add230950720285560b638786b11f27d2c73f71b6331452cae",
        (
            (
                "src/verifier_k4_aggregate/__init__.py",
                "b8d10fd40fdfe27617112354d372446d12a3875d41aed1511f338e2ecd64743f",
                440,
            ),
            (
                "src/verifier_k4_aggregate/__main__.py",
                "0f7d54f3fbb1f79a85eb8110f11793db99da6f3c61ee979de5abe9a1b5f3fdb3",
                49,
            ),
            (
                "src/verifier_k4_aggregate/checker.py",
                "e4b10fbb24e26fc65bba56d4be857c59c008cbcfee1557471b5b5231c2fa168b",
                174_683,
            ),
            (
                "src/verifier_k4_aggregate/cli.py",
                "bc4dabbe9a18f50cd070b40fbaf5fc1f62f63b665f6172ff8f057eeacc3df810",
                3_095,
            ),
            (
                "src/verifier_k4_aggregate/parent_reconstruction.py",
                "d69baa904f92087ae4c8e46515996a03eb81faa440f0e32d15cfd81831b6afb6",
                11_859,
            ),
        ),
    ),
)

RUN_KEYS = {
    "schema",
    "schema_version",
    "proof_pipeline",
    "claim_status",
    "run_directory",
    "campaign_root",
    "original_parent_cnf",
    "original_parent_generator_manifest",
    "retained_parent_cnf",
    "retained_parent_generator_manifest",
    "partition",
    "base_seed",
    "limits",
    "hardware",
    "runtime_sources",
    "tools",
    "normalized_resume_invocation",
    "created_unix_ns",
}
PARTITION_KEYS = {
    "schema",
    "schema_version",
    "claim_status",
    "aggregate_terminal_status",
    "coverage_basis",
    "parent_cnf_sha256",
    "cube_variables",
    "cube_variable_labels",
    "case_count",
    "cases",
}
PARTITION_CASE_KEYS = {
    "case_id",
    "case_index",
    "cube_bits",
    "cube_literals",
    "seed",
    "cnf_sha256",
    "cnf_size_bytes",
    "variable_count",
    "clause_count",
    "literal_count",
}
CHECKPOINT_KEYS = {
    "schema",
    "schema_version",
    "sequence",
    "previous_checkpoint_sha256",
    "run_manifest_sha256",
    "partition_sha256",
    "cases",
    "aggregate_status",
    "claim_boundary",
    "event",
    "written_unix_ns",
}
CASE_STATE_KEYS = {
    "case_id",
    "status",
    "attempt_count",
    "active_attempt",
    "last_completed_outcome_sha256",
}
ATTEMPT_CONFIG_KEYS = {
    "schema",
    "schema_version",
    "proof_pipeline",
    "claim_status",
    "construction_status",
    "case_id",
    "attempt_number",
    "seed",
    "cube_literals",
    "case_cnf_sha256",
    "run_manifest_sha256",
    "partition_sha256",
    "solver_command",
    "raw_forward_command",
    "normalizer_command",
    "normalized_forward_command",
    "lrat_conversion_command",
    "lrat_check_command",
    "created_unix_ns",
}
OUTCOME_KEYS = {
    "schema",
    "schema_version",
    "proof_pipeline",
    "case_id",
    "attempt_number",
    "status",
    "mathematical_claim",
    "aggregate_claim",
    "details",
    "artifact_inventory",
    "finished_unix_ns",
}
BINDING_KEYS = {"path", "sha256", "size_bytes"}
TOOL_KEYS = {
    "role",
    "path",
    "sha256",
    "source_archive_path",
    "source_archive_sha256",
    "commit",
    "version",
}
NORMALIZER_PYTHON_KEYS = {
    "role",
    "path",
    "sha256",
    "implementation",
    "version",
}

ALLOWED_CASE_STATUSES = {
    "PENDING",
    "RUNNING_UNFINISHED_NONCLAIM",
    "RETRYABLE_NONCLAIM",
    "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION",
    LEAF_UNSAT,
}
RETRYABLE_OUTCOMES = {
    "RESOURCE_GATE_FAILED_NONCLAIM",
    "SOLVER_TIMEOUT_NONCLAIM",
    "SOLVER_MEMORY_LIMIT_NONCLAIM",
    "SOLVER_FILE_LIMIT_NONCLAIM",
    "SOLVER_SIGNAL_NONCLAIM",
    "SOLVER_INVALID_OUTPUT_NONCLAIM",
    "SOLVER_UNKNOWN_NONCLAIM",
    "SAT_MODEL_INVALID_NONCLAIM",
    "RAW_FORWARD_TIMEOUT_NONCLAIM",
    "RAW_FORWARD_MEMORY_LIMIT_NONCLAIM",
    "RAW_FORWARD_FILE_LIMIT_NONCLAIM",
    "RAW_FORWARD_SIGNAL_NONCLAIM",
    "RAW_FORWARD_REJECTED_NONCLAIM",
    "NORMALIZER_TIMEOUT_NONCLAIM",
    "NORMALIZER_MEMORY_LIMIT_NONCLAIM",
    "NORMALIZER_FILE_LIMIT_NONCLAIM",
    "NORMALIZER_SIGNAL_NONCLAIM",
    "NORMALIZER_REJECTED_NONCLAIM",
    "NORMALIZED_FORWARD_TIMEOUT_NONCLAIM",
    "NORMALIZED_FORWARD_MEMORY_LIMIT_NONCLAIM",
    "NORMALIZED_FORWARD_FILE_LIMIT_NONCLAIM",
    "NORMALIZED_FORWARD_SIGNAL_NONCLAIM",
    "NORMALIZED_FORWARD_REJECTED_NONCLAIM",
    "LRAT_CONVERSION_TIMEOUT_NONCLAIM",
    "LRAT_CONVERSION_MEMORY_LIMIT_NONCLAIM",
    "LRAT_CONVERSION_FILE_LIMIT_NONCLAIM",
    "LRAT_CONVERSION_SIGNAL_NONCLAIM",
    "LRAT_CONVERSION_REJECTED_NONCLAIM",
    "LRAT_CHECK_TIMEOUT_NONCLAIM",
    "LRAT_CHECK_MEMORY_LIMIT_NONCLAIM",
    "LRAT_CHECK_FILE_LIMIT_NONCLAIM",
    "LRAT_CHECK_SIGNAL_NONCLAIM",
    "LRAT_CHECK_REJECTED_NONCLAIM",
    "ORCHESTRATOR_EXCEPTION_NONCLAIM",
    "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM",
}

CHILD_KEYS = {
    "command",
    "command_sha256",
    "executable_sha256_before",
    "executable_sha256_after",
    "exit_code",
    "termination_signal",
    "timed_out",
    "memory_limit_exceeded",
    "started_unix_ns",
    "finished_unix_ns",
    "wall_seconds",
    "user_cpu_seconds",
    "system_cpu_seconds",
    "maximum_resident_set_size_mib",
    "maximum_resident_set_size_raw",
    "maximum_resident_set_size_raw_unit",
    "peak_polled_resident_set_size_mib",
    "available_memory_before_bytes",
    "wall_limit_seconds",
    "memory_limit_mib",
    "file_limit_mib",
    "stdout_path",
    "stdout_sha256",
    "stderr_path",
    "stderr_sha256",
}
CERTIFICATE_KEYS = {
    "schema",
    "schema_version",
    "proof_pipeline",
    "leaf_status",
    "aggregate_status",
    "case_id",
    "cube_literals",
    "case_cnf",
    "raw_solver_result",
    "raw_binary_drat",
    "normalized_binary_rup",
    "normalization_report",
    "converted_lrat",
    "solver_resource",
    "raw_forward_resource",
    "normalizer_resource",
    "normalized_forward_resource",
    "lrat_conversion_resource",
    "lrat_check_resource",
    "solver",
    "raw_forward",
    "normalizer",
    "normalized_forward",
    "lrat_conversion",
    "lrat_check",
    "solver_stdout",
    "solver_stderr",
    "raw_forward_stdout",
    "raw_forward_stderr",
    "normalizer_stdout",
    "normalizer_stderr",
    "normalized_forward_stdout",
    "normalized_forward_stderr",
    "lrat_conversion_stdout",
    "lrat_conversion_stderr",
    "lrat_check_stdout",
    "lrat_check_stderr",
}
DECISIVE_ARTIFACT_NAMES = {
    "attempt-config.json",
    "instance.cnf",
    "resource-solver.json",
    "solver.stdout",
    "solver.stderr",
    "solver.result",
    "proof.raw.bdrat",
    "resource-raw-forward.json",
    "raw-forward.stdout",
    "raw-forward.stderr",
    "resource-normalizer.json",
    "normalizer.stdout",
    "normalizer.stderr",
    "proof.normalized.rup.bdrat",
    "normalization-report.json",
    "resource-normalized-forward.json",
    "normalized-forward.stdout",
    "normalized-forward.stderr",
    "resource-lrat-conversion.json",
    "lrat-conversion.stdout",
    "lrat-conversion.stderr",
    "proof.converted.lrat",
    "resource-lrat-check.json",
    "lrat-check.stdout",
    "lrat-check.stderr",
    "certificate.json",
}
REPLAY_MANIFEST_KEYS = {
    "schema",
    "schema_version",
    "verifier",
    "scope_id",
    "production_scope",
    "run_directory",
    "run_manifest_sha256",
    "partition_sha256",
    "parent_cnf_sha256",
    "coverage_rows_sha256",
    "lrat_check_sha256",
    "verifier_runtime_sources",
    "verifier_runtime_source_set_sha256",
    "created_unix_ns",
}
REPLAY_SOURCE_KEYS = {"path", "sha256", "size_bytes"}
REPLAY_CONTEXT_KEYS = {
    "replay_manifest_sha256",
    "run_manifest_sha256",
    "partition_sha256",
    "parent_cnf_sha256",
    "coverage_rows_sha256",
    "case_id",
    "cube_literals",
    "certificate_sha256",
    "cnf_sha256",
    "cnf_size_bytes",
    "lrat_sha256",
    "lrat_size_bytes",
    "lrat_check_sha256",
    "policy",
}
REPLAY_POLICY_KEYS = {
    "wall_seconds",
    "memory_mib",
    "file_limit_mib",
    "load_max",
    "memory_reserve_mib",
    "disk_reserve_mib",
    "enforce_live_resource_gates",
}
REPLAY_RECORD_KEYS = {
    "schema",
    "schema_version",
    "verifier",
    "status",
    "context",
    "context_sha256",
    "result",
    "written_unix_ns",
}
REPLAY_RESULT_KEYS = {
    "case_id",
    "logical_command",
    "command_sha256",
    "execution_isolation",
    "checker_sha256_before",
    "checker_sha256_private",
    "checker_sha256_after",
    "cnf_sha256_before",
    "cnf_sha256_reconstructed",
    "cnf_sha256_private",
    "cnf_sha256_after",
    "lrat_sha256_before",
    "lrat_sha256_private",
    "lrat_sha256_after",
    "exit_code",
    "timed_out",
    "memory_limit_exceeded",
    "rss_monitoring_failed",
    "rss_probe_failure_count",
    "peak_polled_resident_set_size_mib",
    "started_unix_ns",
    "finished_unix_ns",
    "wall_seconds",
    "stdout_sha256",
    "stdout_size_bytes",
    "stdout_base64",
    "stderr_sha256",
    "stderr_size_bytes",
    "stderr_base64",
    "resource_gate",
}


class AuditError(ValueError):
    """The run does not support an aggregate finite certificate."""


class ResourceGateError(AuditError):
    """A live resource gate forbids starting the next proof checker."""


class SatLeafPresentError(AuditError):
    """A SAT artifact freezes the aggregate; it is never promoted here."""


@dataclass(frozen=True, slots=True)
class FrozenScope:
    scope_id: str
    production: bool
    campaign_root: Path
    parent_sha256: str
    parent_manifest_sha256: str
    parent_size_bytes: int
    variable_count: int
    parent_clause_count: int
    parent_literal_count: int
    cube_variables: tuple[int, int, int, int]
    cube_labels: tuple[str, str, str, str]
    cadical_sha256: str
    drat_trim_sha256: str
    lrat_check_sha256: str
    cadical_archive_sha256: str
    drat_archive_sha256: str

    @property
    def leaf_clause_count(self) -> int:
        return self.parent_clause_count + len(self.cube_variables)

    @property
    def leaf_literal_count(self) -> int:
        return self.parent_literal_count + len(self.cube_variables)


@dataclass(frozen=True, slots=True)
class AuditPolicy:
    wall_seconds: int = 1_800
    memory_mib: int = 4_096
    file_limit_mib: int = 16
    load_max: float = 7.5
    memory_reserve_mib: int = 2_048
    disk_reserve_mib: int = 512
    enforce_live_resource_gates: bool = True

    def validated(self) -> "AuditPolicy":
        if (
            type(self.wall_seconds) is not int
            or not 1 <= self.wall_seconds <= MAX_REPLAY_WALL_SECONDS
            or type(self.memory_mib) is not int
            or not 16 <= self.memory_mib <= MAX_REPLAY_MEMORY_MIB
            or type(self.file_limit_mib) is not int
            or not 1 <= self.file_limit_mib <= 64
            or type(self.load_max) not in (int, float)
            or not math.isfinite(float(self.load_max))
            or not 0.1 <= float(self.load_max) <= 1_000.0
            or type(self.memory_reserve_mib) is not int
            or self.memory_reserve_mib < MIN_MEMORY_RESERVE_MIB
            or type(self.disk_reserve_mib) is not int
            or self.disk_reserve_mib < MIN_DISK_RESERVE_MIB
            or type(self.enforce_live_resource_gates) is not bool
        ):
            raise AuditError("aggregate replay policy is malformed")
        return self


def campaign_root() -> Path:
    return Path(__file__).resolve().parents[2]


PRODUCTION_SCOPE = FrozenScope(
    scope_id="order12-k4-connected-parent-adbe0c01",
    production=True,
    campaign_root=campaign_root(),
    parent_sha256=(
        "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac"
    ),
    parent_manifest_sha256=(
        "621a0878c117dc8b4d6dbd0ba14c8402a8c24e8339d2f85cb23d61ffd74fbb61"
    ),
    parent_size_bytes=3_992_947,
    variable_count=18_381,
    parent_clause_count=114_742,
    parent_literal_count=1_180_016,
    cube_variables=(4, 14, 23, 31),
    cube_labels=("e_0_4", "e_1_4", "e_2_4", "e_3_4"),
    cadical_sha256=(
        "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
    ),
    drat_trim_sha256=(
        "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
    ),
    lrat_check_sha256=(
        "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2"
    ),
    cadical_archive_sha256=(
        "2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e"
    ),
    drat_archive_sha256=(
        "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108"
    ),
)


def _validate_scope(scope: FrozenScope) -> FrozenScope:
    if not isinstance(scope, FrozenScope):
        raise AuditError("aggregate scope has the wrong type")
    if scope.production and scope != PRODUCTION_SCOPE:
        raise AuditError("custom production scopes are forbidden")
    if (
        not scope.scope_id
        or not scope.campaign_root.is_absolute()
        or type(scope.production) is not bool
        or len(scope.cube_variables) != 4
        or len(set(scope.cube_variables)) != 4
        or len(scope.cube_labels) != 4
        or any(
            type(variable) is not int
            or not 1 <= variable <= scope.variable_count
            for variable in scope.cube_variables
        )
    ):
        raise AuditError("aggregate scope is malformed")
    return scope


@dataclass(frozen=True, slots=True)
class FileStamp:
    device: int
    inode: int
    mode: int
    links: int
    size: int
    modified_ns: int
    changed_ns: int


@dataclass(frozen=True, slots=True)
class DimacsCensus:
    variable_count: int
    clause_count: int
    literal_count: int


@dataclass(frozen=True, slots=True)
class StaticAudit:
    run_directory: Path
    run_manifest: dict[str, Any]
    run_manifest_sha256: str
    partition: dict[str, Any]
    partition_sha256: str
    parent: bytes
    parent_sha256: str
    latest_checkpoint: dict[str, Any]
    latest_checkpoint_sha256: str
    reconstructed_leaves: tuple[dict[str, Any], ...]
    terminal_attempts: tuple[dict[str, Any], ...]
    coverage_rows_sha256: str
    checkpoint_count: int
    historical_attempt_count: int
    lrat_check_path: Path
    lrat_check_sha256: str


def canonical_json_bytes(value: object) -> bytes:
    try:
        text = json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
    except (TypeError, ValueError, RecursionError) as error:
        raise AuditError("object is not canonical finite JSON") from error
    return (text + "\n").encode("utf-8")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AuditError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise AuditError(f"non-finite JSON number {token!r}")


def _stamp(information: os.stat_result) -> FileStamp:
    return FileStamp(
        information.st_dev,
        information.st_ino,
        information.st_mode,
        information.st_nlink,
        information.st_size,
        information.st_mtime_ns,
        information.st_ctime_ns,
    )


def _assert_no_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current /= component
        try:
            information = os.lstat(current)
        except FileNotFoundError:
            raise AuditError(f"path component is missing: {current}") from None
        if stat.S_ISLNK(information.st_mode):
            raise AuditError(f"symlinked path component is forbidden: {current}")


def _open_regular_single_link(path: Path, role: str) -> tuple[int, FileStamp]:
    _assert_no_symlink_components(path)
    try:
        before_open = os.lstat(path)
    except OSError as error:
        raise AuditError(f"{role} cannot be inspected: {path}") from error
    if (
        stat.S_ISLNK(before_open.st_mode)
        or not stat.S_ISREG(before_open.st_mode)
        or before_open.st_nlink != 1
    ):
        raise AuditError(f"{role} is not a single-link regular file: {path}")
    flags = os.O_RDONLY | os.O_NONBLOCK
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise AuditError(f"{role} cannot be opened: {path}") from error
    try:
        information = os.fstat(descriptor)
        if not stat.S_ISREG(information.st_mode):
            raise AuditError(f"{role} is not a regular file: {path}")
        if information.st_nlink != 1:
            raise AuditError(
                f"{role} must have one hard link, found {information.st_nlink}: {path}"
            )
        if (
            information.st_dev != before_open.st_dev
            or information.st_ino != before_open.st_ino
        ):
            raise AuditError(f"{role} changed identity while opening: {path}")
        return descriptor, _stamp(information)
    except BaseException:
        os.close(descriptor)
        raise


def _stable_file_hash(path: Path, role: str) -> tuple[str, int]:
    descriptor, before = _open_regular_single_link(path, role)
    digest = sha256()
    try:
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                break
            digest.update(chunk)
        after = _stamp(os.fstat(descriptor))
    finally:
        os.close(descriptor)
    if before != after:
        raise AuditError(f"{role} changed while hashing: {path}")
    return digest.hexdigest(), before.size


def _stable_file_bytes(
    path: Path,
    role: str,
    *,
    maximum_bytes: int,
) -> bytes:
    descriptor, before = _open_regular_single_link(path, role)
    if before.size > maximum_bytes:
        os.close(descriptor)
        raise AuditError(f"{role} exceeds {maximum_bytes} bytes: {path}")
    chunks: list[bytes] = []
    remaining = before.size
    try:
        while remaining:
            chunk = os.read(descriptor, min(1 << 20, remaining))
            if not chunk:
                raise AuditError(f"{role} was truncated while reading: {path}")
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1):
            raise AuditError(f"{role} grew while reading: {path}")
        after = _stamp(os.fstat(descriptor))
    finally:
        os.close(descriptor)
    if before != after:
        raise AuditError(f"{role} changed while reading: {path}")
    return b"".join(chunks)


def _fsync_directory(directory: Path, role: str) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    try:
        descriptor = os.open(directory, flags)
    except OSError as error:
        raise AuditError(f"{role} directory cannot be opened") from error
    try:
        os.fsync(descriptor)
    except OSError as error:
        raise AuditError(f"{role} directory cannot be synchronized") from error
    finally:
        os.close(descriptor)


def _write_exclusive_bytes(
    path: Path,
    payload: bytes,
    role: str,
    *,
    mode: int = 0o600,
) -> tuple[str, int]:
    if not isinstance(payload, bytes):
        raise AuditError(f"{role} payload is not bytes")
    _assert_no_symlink_components(path.parent)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, mode)
    except OSError as error:
        raise AuditError(f"{role} cannot be created") from error
    written = 0
    try:
        while written < len(payload):
            count = os.write(descriptor, payload[written:])
            if count <= 0:
                raise AuditError(f"{role} write made no progress")
            written += count
        os.fsync(descriptor)
        information = os.fstat(descriptor)
        if (
            not stat.S_ISREG(information.st_mode)
            or information.st_nlink != 1
            or information.st_size != len(payload)
        ):
            raise AuditError(f"{role} created file is malformed")
    except BaseException:
        os.close(descriptor)
        try:
            path.unlink()
        except OSError:
            pass
        raise
    os.close(descriptor)
    _fsync_directory(path.parent, role)
    return sha256(payload).hexdigest(), len(payload)


def _copy_stable_file(
    source: Path,
    destination: Path,
    role: str,
    *,
    executable: bool = False,
) -> tuple[str, int]:
    source_descriptor, source_before = _open_regular_single_link(source, role)
    _assert_no_symlink_components(destination.parent)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        destination_descriptor = os.open(
            destination,
            flags,
            0o700 if executable else 0o600,
        )
    except BaseException:
        os.close(source_descriptor)
        raise
    digest = sha256()
    copied = 0
    try:
        while True:
            chunk = os.read(source_descriptor, 1 << 20)
            if not chunk:
                break
            digest.update(chunk)
            offset = 0
            while offset < len(chunk):
                count = os.write(destination_descriptor, chunk[offset:])
                if count <= 0:
                    raise AuditError(f"{role} private copy made no progress")
                offset += count
            copied += len(chunk)
        source_after = _stamp(os.fstat(source_descriptor))
        if source_after != source_before or copied != source_before.size:
            raise AuditError(f"{role} changed during private copy")
        os.fsync(destination_descriptor)
        destination_information = os.fstat(destination_descriptor)
        if (
            not stat.S_ISREG(destination_information.st_mode)
            or destination_information.st_nlink != 1
            or destination_information.st_size != copied
        ):
            raise AuditError(f"{role} private copy is malformed")
    except BaseException:
        os.close(destination_descriptor)
        os.close(source_descriptor)
        try:
            destination.unlink()
        except OSError:
            pass
        raise
    os.close(destination_descriptor)
    os.close(source_descriptor)
    _fsync_directory(destination.parent, role)
    destination_hash, destination_size = _stable_file_hash(
        destination, f"{role} private copy"
    )
    if destination_hash != digest.hexdigest() or destination_size != copied:
        raise AuditError(f"{role} private copy differs")
    return destination_hash, destination_size


def _load_canonical_json(path: Path, role: str) -> tuple[Any, bytes, str]:
    raw = _stable_file_bytes(path, role, maximum_bytes=MAX_JSON_BYTES)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AuditError(f"{role} is not UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as error:
        raise AuditError(f"{role} is malformed JSON") from error
    except RecursionError as error:
        raise AuditError(f"{role} JSON nesting is too deep") from error
    if canonical_json_bytes(value) != raw:
        raise AuditError(f"{role} is not in canonical JSON serialization")
    return value, raw, sha256(raw).hexdigest()


def _exact_keys(value: object, keys: set[str], role: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        observed = set(value) if isinstance(value, dict) else set()
        raise AuditError(
            f"{role} keys differ; missing={sorted(keys-observed)}, "
            f"extra={sorted(observed-keys)}"
        )
    return value


def _exact_int(
    value: object,
    role: str,
    *,
    minimum: int = 0,
    maximum: int = (1 << 63) - 1,
) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise AuditError(f"{role} must be an integer in {minimum}..{maximum}")
    return value


def _hex_digest(value: object, role: str) -> str:
    if type(value) is not str or HEX64_RE.fullmatch(value) is None:
        raise AuditError(f"{role} must be a lowercase SHA-256 digest")
    return value


def _binding(
    value: object,
    role: str,
    *,
    expected_path: Path | None = None,
    expected_sha256: str | None = None,
    expected_size: int | None = None,
    verify_file: bool = True,
) -> dict[str, Any]:
    record = _exact_keys(value, BINDING_KEYS, f"{role} binding")
    raw_path = record["path"]
    if type(raw_path) is not str or not Path(raw_path).is_absolute():
        raise AuditError(f"{role} binding path must be absolute")
    digest = _hex_digest(record["sha256"], f"{role} binding digest")
    size = _exact_int(record["size_bytes"], f"{role} binding size")
    path = Path(raw_path)
    if expected_path is not None and path != expected_path.resolve():
        raise AuditError(f"{role} binding path differs")
    if expected_sha256 is not None and digest != expected_sha256:
        raise AuditError(f"{role} binding digest differs")
    if expected_size is not None and size != expected_size:
        raise AuditError(f"{role} binding size differs")
    if verify_file:
        observed_digest, observed_size = _stable_file_hash(path, role)
        if observed_digest != digest or observed_size != size:
            raise AuditError(f"{role} binding no longer holds")
    return record


def _inspect_dimacs(payload: bytes, role: str) -> DimacsCensus:
    if not payload.endswith(b"\n"):
        raise AuditError(f"{role} must end with a newline")
    newline = payload.find(b"\n")
    if newline < 0:
        raise AuditError(f"{role} has no DIMACS header")
    try:
        header = payload[:newline].decode("ascii")
    except UnicodeDecodeError as error:
        raise AuditError(f"{role} header is not ASCII") from error
    fields = header.split()
    if (
        len(fields) != 4
        or fields[:2] != ["p", "cnf"]
        or not fields[2].isdigit()
        or not fields[3].isdigit()
    ):
        raise AuditError(f"{role} DIMACS header is malformed")
    variables = int(fields[2])
    declared_clauses = int(fields[3])
    clauses = 0
    literals = 0
    open_clause = False
    for line_number, raw_line in enumerate(
        payload[newline + 1 :].splitlines(), start=2
    ):
        if raw_line.startswith(b"c"):
            if open_clause:
                raise AuditError(f"{role} comment interrupts a clause")
            continue
        try:
            tokens = raw_line.decode("ascii").split()
        except UnicodeDecodeError as error:
            raise AuditError(f"{role} line {line_number} is not ASCII") from error
        for token in tokens:
            try:
                literal = int(token, 10)
            except ValueError as error:
                raise AuditError(
                    f"{role} line {line_number} has a noninteger token"
                ) from error
            if literal == 0:
                clauses += 1
                open_clause = False
            else:
                if abs(literal) > variables:
                    raise AuditError(
                        f"{role} literal {literal} exceeds variable range"
                    )
                literals += 1
                open_clause = True
    if open_clause:
        raise AuditError(f"{role} has an unterminated final clause")
    if clauses != declared_clauses:
        raise AuditError(
            f"{role} declares {declared_clauses} clauses but contains {clauses}"
        )
    return DimacsCensus(variables, clauses, literals)


def _leaf_bytes(
    parent: bytes,
    literals: Sequence[int],
    scope: FrozenScope,
) -> bytes:
    if (
        len(literals) != len(scope.cube_variables)
        or tuple(abs(item) for item in literals) != scope.cube_variables
        or any(type(item) is not int or item == 0 for item in literals)
    ):
        raise AuditError("cube literals do not match the four frozen variables")
    newline = parent.find(b"\n")
    expected_header = (
        f"p cnf {scope.variable_count} {scope.parent_clause_count}\n"
    ).encode("ascii")
    if newline < 0 or parent[: newline + 1] != expected_header:
        raise AuditError("frozen parent header differs")
    header = (
        f"p cnf {scope.variable_count} {scope.leaf_clause_count}\n"
    ).encode("ascii")
    units = b"".join(f"{literal} 0\n".encode("ascii") for literal in literals)
    return header + parent[newline + 1 :] + units


def _summary_for_cases(cases: Sequence[Mapping[str, Any]]) -> str:
    statuses = [record["status"] for record in cases]
    if any(
        status == "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION"
        for status in statuses
    ):
        return "SAT_CANDIDATE_HOLD_NONCLAIM"
    if statuses and all(status == LEAF_UNSAT for status in statuses):
        return RUNNER_TERMINAL
    if any(status == "RUNNING_UNFINISHED_NONCLAIM" for status in statuses):
        return "INCOMPLETE_ACTIVE_NONCLAIM"
    return "INCOMPLETE_NONCLAIM"


def _source_set_digest(records: object) -> str:
    return sha256(canonical_json_bytes(records)).hexdigest()


def _validate_parent(
    run_directory: Path,
    run_manifest: Mapping[str, Any],
    scope: FrozenScope,
) -> tuple[bytes, str]:
    retained_parent_path = run_directory / PARENT_NAME
    retained_manifest_path = run_directory / PARENT_MANIFEST_NAME
    _binding(
        run_manifest["retained_parent_cnf"],
        "retained parent CNF",
        expected_path=retained_parent_path,
        expected_sha256=scope.parent_sha256,
        expected_size=scope.parent_size_bytes,
    )
    _binding(
        run_manifest["retained_parent_generator_manifest"],
        "retained parent generator manifest",
        expected_path=retained_manifest_path,
        expected_sha256=scope.parent_manifest_sha256,
    )
    original_parent = _binding(
        run_manifest["original_parent_cnf"],
        "original parent CNF",
        expected_sha256=scope.parent_sha256,
        expected_size=scope.parent_size_bytes,
        verify_file=False,
    )
    original_manifest = _binding(
        run_manifest["original_parent_generator_manifest"],
        "original parent generator manifest",
        expected_sha256=scope.parent_manifest_sha256,
        verify_file=False,
    )
    if original_parent["sha256"] != scope.parent_sha256:
        raise AuditError("historical original parent binding differs")
    if original_manifest["sha256"] != scope.parent_manifest_sha256:
        raise AuditError("historical original parent-manifest binding differs")

    parent = _stable_file_bytes(
        retained_parent_path,
        "retained parent CNF",
        maximum_bytes=max(scope.parent_size_bytes, 1),
    )
    if (
        len(parent) != scope.parent_size_bytes
        or sha256(parent).hexdigest() != scope.parent_sha256
    ):
        raise AuditError("retained parent bytes differ from the frozen scope")
    census = _inspect_dimacs(parent, "retained parent CNF")
    if census != DimacsCensus(
        scope.variable_count,
        scope.parent_clause_count,
        scope.parent_literal_count,
    ):
        raise AuditError("retained parent DIMACS census differs")

    parent_manifest, raw_manifest, manifest_hash = _load_canonical_json(
        retained_manifest_path,
        "retained parent generator manifest",
    )
    if manifest_hash != scope.parent_manifest_sha256:
        raise AuditError("retained parent-generator manifest hash differs")
    if not isinstance(parent_manifest, dict):
        raise AuditError("retained parent-generator manifest is not an object")
    required = {
        "cnf_sha256": scope.parent_sha256,
        "cnf_size_bytes": scope.parent_size_bytes,
        "variable_count": scope.variable_count,
        "clause_count": scope.parent_clause_count,
        "literal_count": scope.parent_literal_count,
        "claim_status": "NO_MATHEMATICAL_CLAIM",
    }
    for key in (
        "cnf_size_bytes",
        "variable_count",
        "clause_count",
        "literal_count",
    ):
        _exact_int(
            parent_manifest.get(key),
            f"retained parent-generator manifest {key}",
            minimum=required[key],
            maximum=required[key],
        )
    if any(parent_manifest.get(key) != expected for key, expected in required.items()):
        raise AuditError("retained parent-generator manifest disagrees with scope")
    if sha256(raw_manifest).hexdigest() != scope.parent_manifest_sha256:
        raise AssertionError("parent-manifest read/hash invariant failed")
    if scope.production:
        reconstructed = reconstruct_parent()
        reconstructed_hash = sha256(reconstructed.payload).hexdigest()
        if (
            reconstructed.payload != parent
            or reconstructed_hash != scope.parent_sha256
            or reconstructed.variable_count != scope.variable_count
            or reconstructed.clause_count != scope.parent_clause_count
            or reconstructed.literal_count != scope.parent_literal_count
            or reconstructed.cube_variables != scope.cube_variables
            or reconstructed.cube_labels != scope.cube_labels
        ):
            raise AuditError(
                "clean-room parent/cube reconstruction differs from the run"
            )
    return parent, scope.parent_sha256


def _validate_limits(
    value: object,
    hardware: Mapping[str, Any],
) -> dict[str, Any]:
    expected = {
        "solver_wall_seconds",
        "converter_wall_seconds",
        "checker_wall_seconds",
        "solver_memory_mib",
        "postprocess_memory_mib",
        "file_limit_mib",
        "disk_reserve_mib",
        "memory_reserve_mib",
        "load_max",
        "maximum_responsive_child_memory_mib",
        "worst_case_live_file_slots",
    }
    limits = _exact_keys(value, expected, "run limits")
    for name in (
        "solver_wall_seconds",
        "converter_wall_seconds",
        "checker_wall_seconds",
    ):
        _exact_int(
            limits[name], f"run limit {name}", minimum=1, maximum=21_600
        )
    for name in ("solver_memory_mib", "postprocess_memory_mib"):
        _exact_int(
            limits[name], f"run limit {name}", minimum=64, maximum=1 << 20
        )
    _exact_int(
        limits["file_limit_mib"],
        "run file limit",
        minimum=16,
        maximum=4_096,
    )
    _exact_int(
        limits["disk_reserve_mib"],
        "run disk reserve",
        minimum=4_096,
        maximum=1 << 20,
    )
    _exact_int(
        limits["memory_reserve_mib"],
        "run memory reserve",
        minimum=512,
        maximum=1 << 20,
    )
    load = limits["load_max"]
    if (
        type(load) not in (int, float)
        or not math.isfinite(float(load))
        or not 0.1 <= float(load) <= 1_000.0
    ):
        raise AuditError("run load ceiling is malformed")
    physical = _exact_int(
        hardware["physical_memory_bytes"],
        "hardware physical memory",
        minimum=1,
    )
    maximum_responsive = math.floor(physical * 0.75 / (1 << 20))
    if (
        limits["maximum_responsive_child_memory_mib"] != maximum_responsive
        or limits["worst_case_live_file_slots"]
        != WORST_CASE_LIVE_FILE_SLOTS
        or max(
            limits["solver_memory_mib"],
            limits["postprocess_memory_mib"],
        )
        > maximum_responsive
    ):
        raise AuditError("run responsive-resource limits differ")
    return limits


def _validate_hardware(value: object) -> dict[str, Any]:
    keys = {
        "logical_cpu_count",
        "physical_memory_bytes",
        "machine",
        "processor",
        "platform",
        "python_executable",
        "python_implementation",
        "python_version",
    }
    hardware = _exact_keys(value, keys, "hardware report")
    _exact_int(hardware["logical_cpu_count"], "logical CPU count", minimum=1)
    _exact_int(hardware["physical_memory_bytes"], "physical memory", minimum=1)
    for key in keys - {"logical_cpu_count", "physical_memory_bytes"}:
        if type(hardware[key]) is not str:
            raise AuditError(f"hardware field {key} is not a string")
    return hardware


def _git_blob_sha1(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return sha1(header + payload).hexdigest()


def _git_read(
    root: Path,
    arguments: Sequence[str],
    role: str,
    *,
    maximum_bytes: int = MAX_JSON_BYTES,
) -> bytes:
    try:
        completed = subprocess.run(
            ("/usr/bin/git", *arguments),
            cwd=root,
            env={},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise AuditError(f"{role} could not be read from git") from error
    if (
        completed.returncode != 0
        or completed.stderr
        or len(completed.stdout) > maximum_bytes
    ):
        raise AuditError(f"{role} git lookup failed")
    return completed.stdout


def _validate_runtime_sources(
    value: object,
    scope: FrozenScope,
) -> dict[str, Any]:
    binding = _exact_keys(
        value,
        {
            "head_at_creation",
            "global_worktree_cleanliness_required",
            "records",
            "source_set_sha256",
        },
        "runtime source binding",
    )
    if (
        type(binding["head_at_creation"]) is not str
        or re.fullmatch(r"[0-9a-f]{40}", binding["head_at_creation"]) is None
        or binding["global_worktree_cleanliness_required"] is not False
        or not isinstance(binding["records"], list)
    ):
        raise AuditError("runtime source binding header is malformed")
    records = binding["records"]
    observed_paths = [
        record.get("path") for record in records if isinstance(record, dict)
    ]
    if records and observed_paths != list(RUNTIME_SOURCE_PATHS):
        raise AuditError("runtime source path order differs")
    if scope.production and observed_paths != list(RUNTIME_SOURCE_PATHS):
        raise AuditError("production run does not bind every runtime source")
    for index, record in enumerate(records):
        source = _exact_keys(
            record,
            {"path", "git_blob", "sha256", "size_bytes"},
            f"runtime source {index}",
        )
        if (
            type(source["path"]) is not str
            or type(source["git_blob"]) is not str
            or re.fullmatch(r"[0-9a-f]{40}", source["git_blob"]) is None
        ):
            raise AuditError(f"runtime source {index} is malformed")
        _hex_digest(source["sha256"], f"runtime source {index} digest")
        size = _exact_int(
            source["size_bytes"], f"runtime source {index} size"
        )
        relative = Path(source["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise AuditError(f"runtime source {index} path escapes the campaign")
        historic_blob = _git_read(
            scope.campaign_root,
            ("show", f"{binding['head_at_creation']}:./{source['path']}"),
            f"historic runtime source {source['path']}",
        )
        if (
            len(historic_blob) != size
            or sha256(historic_blob).hexdigest() != source["sha256"]
            or _git_blob_sha1(historic_blob) != source["git_blob"]
        ):
            raise AuditError(
                f"runtime source {source['path']} differs at creation commit"
            )
    digest = _hex_digest(
        binding["source_set_sha256"],
        "runtime source-set digest",
    )
    if digest != _source_set_digest(records):
        raise AuditError("runtime source-set digest differs")
    if scope.production:
        expected_records = [
            {
                "path": path,
                "git_blob": blob,
                "sha256": digest,
                "size_bytes": size,
            }
            for path, blob, digest, size in FROZEN_RUNTIME_SOURCE_RECORDS
        ]
        if records != expected_records:
            raise AuditError(
                "production runtime source vector differs from f4ccb167"
            )
        if digest != FROZEN_RUNTIME_SOURCE_SET_SHA256:
            raise AuditError("production runtime source-set pin differs")
    return binding


def _validate_tool_record(
    value: object,
    role: str,
    *,
    expected_binary_hash: str,
    expected_archive_hash: str,
    expected_path: Path,
    expected_archive_path: Path,
    expected_commit: str,
    expected_version: str | None,
) -> dict[str, Any]:
    record = _exact_keys(value, TOOL_KEYS, f"{role} tool record")
    if record["role"] != role:
        raise AuditError(f"{role} tool role differs")
    if (
        record["commit"] != expected_commit
        or record["version"] != expected_version
        or record["path"] != str(expected_path.resolve())
        or record["sha256"] != expected_binary_hash
        or record["source_archive_path"] != str(expected_archive_path.resolve())
        or record["source_archive_sha256"] != expected_archive_hash
    ):
        raise AuditError(f"{role} frozen path or digest differs")
    observed_hash, _ = _stable_file_hash(expected_path, role)
    archive_hash, _ = _stable_file_hash(
        expected_archive_path,
        f"{role} source archive",
    )
    if observed_hash != expected_binary_hash or archive_hash != expected_archive_hash:
        raise AuditError(f"{role} current binary/archive binding differs")
    if not os.access(expected_path, os.X_OK):
        raise AuditError(f"{role} is not executable")
    return record


def _validate_tools(
    value: object,
    scope: FrozenScope,
) -> tuple[dict[str, Any], Path]:
    tools = _exact_keys(
        value,
        {"cadical", "drat_trim", "lrat_check", "normalizer_python"},
        "tools",
    )
    root = scope.campaign_root
    cadical = root / "tools/cadical_3_0_1/build/cadical"
    drat_trim = root / "tools/drat_trim_2023_05_22/drat-trim"
    lrat_check = root / "tools/drat_trim_2023_05_22/lrat-check"
    cadical_archive = root / "tools/cadical_3_0_1.tar.gz"
    drat_archive = root / "tools/drat_trim_2023_05_22.tar.gz"
    cadical_record = _exact_keys(tools["cadical"], TOOL_KEYS, "cadical tool record")
    drat_record = _exact_keys(
        tools["drat_trim"], TOOL_KEYS, "drat_trim tool record"
    )
    lrat_record = _exact_keys(
        tools["lrat_check"], TOOL_KEYS, "lrat_check tool record"
    )
    if lrat_record["source_archive_path"] != str(drat_archive.resolve()):
        raise AuditError("lrat-check and drat-trim source archive paths differ")
    _validate_tool_record(
        cadical_record,
        "cadical",
        expected_binary_hash=scope.cadical_sha256,
        expected_archive_hash=scope.cadical_archive_sha256,
        expected_path=cadical,
        expected_archive_path=cadical_archive,
        expected_commit="c60730422e758ef1cebe7aeddf2dda31c996bf04",
        expected_version="3.0.1",
    )
    _validate_tool_record(
        drat_record,
        "drat-trim",
        expected_binary_hash=scope.drat_trim_sha256,
        expected_archive_hash=scope.drat_archive_sha256,
        expected_path=drat_trim,
        expected_archive_path=drat_archive,
        expected_commit="2e5e29cb0019d5cfd547d4208dca1b3ec290349f",
        expected_version=None,
    )
    _validate_tool_record(
        lrat_record,
        "lrat-check",
        expected_binary_hash=scope.lrat_check_sha256,
        expected_archive_hash=scope.drat_archive_sha256,
        expected_path=lrat_check,
        expected_archive_path=drat_archive,
        expected_commit="2e5e29cb0019d5cfd547d4208dca1b3ec290349f",
        expected_version=None,
    )
    python_record = _exact_keys(
        tools["normalizer_python"],
        NORMALIZER_PYTHON_KEYS,
        "normalizer Python tool record",
    )
    python_path_raw = python_record["path"]
    if (
        python_record["role"] != "normalizer-python-runtime"
        or type(python_path_raw) is not str
        or not Path(python_path_raw).is_absolute()
        or type(python_record["implementation"]) is not str
        or not python_record["implementation"]
        or type(python_record["version"]) is not str
        or not python_record["version"]
    ):
        raise AuditError("normalizer Python tool record is malformed")
    python_digest = _hex_digest(
        python_record["sha256"], "normalizer Python digest"
    )
    python_path = Path(python_path_raw)
    observed_python_digest, _ = _stable_file_hash(
        python_path, "normalizer Python runtime"
    )
    if (
        observed_python_digest != python_digest
        or not os.access(python_path, os.X_OK)
    ):
        raise AuditError("normalizer Python runtime binding differs")
    return tools, lrat_check


def _validate_run_manifest(
    run_directory: Path,
    scope: FrozenScope,
) -> tuple[dict[str, Any], str, Path]:
    path = run_directory / RUN_MANIFEST_NAME
    value, _, digest = _load_canonical_json(path, "run manifest")
    manifest = _exact_keys(value, RUN_KEYS, "run manifest")
    _exact_int(
        manifest["schema_version"],
        "run-manifest schema version",
        minimum=SCHEMA_VERSION,
        maximum=SCHEMA_VERSION,
    )
    if (
        manifest["schema"] != RUN_SCHEMA
        or manifest["schema_version"] != SCHEMA_VERSION
        or manifest["proof_pipeline"] != PROOF_PIPELINE_ID
        or manifest["claim_status"] != RUN_CLAIM
        or manifest["run_directory"] != str(run_directory)
        or manifest["campaign_root"] != str(scope.campaign_root.resolve())
    ):
        raise AuditError("run manifest header differs")
    _exact_int(
        manifest["base_seed"],
        "base seed",
        maximum=2_000_000_000 - 15,
    )
    _exact_int(manifest["created_unix_ns"], "run creation time", minimum=1)
    hardware = _validate_hardware(manifest["hardware"])
    _validate_limits(manifest["limits"], hardware)
    _validate_runtime_sources(manifest["runtime_sources"], scope)
    _, lrat_check = _validate_tools(manifest["tools"], scope)
    invocation = manifest["normalized_resume_invocation"]
    expected_invocation = [
        "/usr/bin/env",
        f"PYTHONPATH={scope.campaign_root / 'src'}",
        str(Path(manifest["tools"]["normalizer_python"]["path"])),
        "-m",
        "search.k4_production",
        "run-next",
        "--production-gate-open",
        "--run-dir",
        str(run_directory),
    ]
    if (
        not isinstance(invocation, list)
        or any(type(item) is not str for item in invocation)
        or invocation != expected_invocation
    ):
        raise AuditError("normalized resume invocation is malformed")
    return manifest, digest, lrat_check


def _validate_partition(
    run_directory: Path,
    run_manifest: Mapping[str, Any],
    parent: bytes,
    scope: FrozenScope,
) -> tuple[dict[str, Any], str, tuple[dict[str, Any], ...], str]:
    path = run_directory / PARTITION_NAME
    partition_binding = _binding(
        run_manifest["partition"],
        "partition",
        expected_path=path,
    )
    value, _, digest = _load_canonical_json(path, "partition")
    if digest != partition_binding["sha256"]:
        raise AuditError("partition hash differs from run-manifest binding")
    partition = _exact_keys(value, PARTITION_KEYS, "partition")
    _exact_int(
        partition["schema_version"],
        "partition schema version",
        minimum=SCHEMA_VERSION,
        maximum=SCHEMA_VERSION,
    )
    _exact_int(
        partition["case_count"],
        "partition case count",
        minimum=16,
        maximum=16,
    )
    if (
        not isinstance(partition["cube_variables"], list)
        or any(
            type(variable) is not int
            for variable in partition["cube_variables"]
        )
        or not isinstance(partition["cube_variable_labels"], list)
        or any(
            type(label) is not str
            for label in partition["cube_variable_labels"]
        )
    ):
        raise AuditError("partition cube-variable data is malformed")
    if (
        partition["schema"] != PARTITION_SCHEMA
        or partition["schema_version"] != SCHEMA_VERSION
        or partition["claim_status"] != RUN_CLAIM
        or partition["aggregate_terminal_status"] != RUNNER_TERMINAL
        or partition["parent_cnf_sha256"] != scope.parent_sha256
        or partition["cube_variables"] != list(scope.cube_variables)
        or partition["cube_variable_labels"] != list(scope.cube_labels)
        or partition["case_count"] != 16
    ):
        raise AuditError("partition header differs")
    expected_basis = (
        "All 2^4 total assignments to four distinct Boolean variables; "
        "every total parent assignment belongs to exactly one cube."
    )
    if partition["coverage_basis"] != expected_basis:
        raise AuditError("partition coverage-basis statement differs")
    raw_cases = partition["cases"]
    if not isinstance(raw_cases, list) or len(raw_cases) != 16:
        raise AuditError("partition must contain exactly 16 cases")

    base_seed = run_manifest["base_seed"]
    reconstructed: list[dict[str, Any]] = []
    expected_bit_rows = tuple(product((0, 1), repeat=4))
    for index, (raw_case, bits) in enumerate(
        zip(raw_cases, expected_bit_rows, strict=True)
    ):
        case = _exact_keys(raw_case, PARTITION_CASE_KEYS, f"partition case {index}")
        expected_id = "".join(map(str, bits))
        literals = tuple(
            variable if bit else -variable
            for variable, bit in zip(scope.cube_variables, bits, strict=True)
        )
        leaf = _leaf_bytes(parent, literals, scope)
        for key, expected_number in (
            ("case_index", index),
            ("seed", base_seed + index),
            ("cnf_size_bytes", len(leaf)),
            ("variable_count", scope.variable_count),
            ("clause_count", scope.leaf_clause_count),
            ("literal_count", scope.leaf_literal_count),
        ):
            _exact_int(
                case[key],
                f"partition case {expected_id} {key}",
                minimum=expected_number,
                maximum=expected_number,
            )
        if (
            not isinstance(case["cube_bits"], list)
            or any(
                type(bit) is not int or bit not in (0, 1)
                for bit in case["cube_bits"]
            )
            or not isinstance(case["cube_literals"], list)
            or any(
                type(literal) is not int
                for literal in case["cube_literals"]
            )
        ):
            raise AuditError(
                f"partition case {expected_id} cube data is malformed"
            )
        census = _inspect_dimacs(leaf, f"reconstructed leaf {expected_id}")
        leaf_hash = sha256(leaf).hexdigest()
        if (
            case["case_id"] != expected_id
            or case["case_index"] != index
            or case["cube_bits"] != list(bits)
            or case["cube_literals"] != list(literals)
            or case["seed"] != base_seed + index
            or case["cnf_sha256"] != leaf_hash
            or case["cnf_size_bytes"] != len(leaf)
            or case["variable_count"] != scope.variable_count
            or case["clause_count"] != scope.leaf_clause_count
            or case["literal_count"] != scope.leaf_literal_count
            or census
            != DimacsCensus(
                scope.variable_count,
                scope.leaf_clause_count,
                scope.leaf_literal_count,
            )
        ):
            raise AuditError(f"partition case {expected_id} differs")
        reconstructed.append(
            {
                "case_id": expected_id,
                "case_index": index,
                "cube_bits": list(bits),
                "cube_literals": list(literals),
                "cnf_sha256": leaf_hash,
                "cnf_size_bytes": len(leaf),
                "seed": base_seed + index,
            }
        )

    coverage_rows: list[dict[str, Any]] = []
    cubes = [tuple(record["cube_literals"]) for record in reconstructed]
    for assignment in expected_bit_rows:
        truth = dict(zip(scope.cube_variables, assignment, strict=True))
        hits: list[int] = []
        for index, cube in enumerate(cubes):
            if all(
                truth[abs(literal)] == int(literal > 0)
                for literal in cube
            ):
                hits.append(index)
        if len(hits) != 1:
            raise AuditError(
                f"assignment {assignment} belongs to {len(hits)} cubes"
            )
        coverage_rows.append(
            {
                "assignment_bits": list(assignment),
                "unique_case_id": reconstructed[hits[0]]["case_id"],
            }
        )
    for left, right in combinations(cubes, 2):
        if not any(-literal in right for literal in left):
            raise AuditError("two distinct cubes are not concretely disjoint")
    coverage_hash = sha256(canonical_json_bytes(coverage_rows)).hexdigest()
    return partition, digest, tuple(reconstructed), coverage_hash


def _case_state(value: object, expected_id: str, role: str) -> dict[str, Any]:
    state = _exact_keys(value, CASE_STATE_KEYS, role)
    if (
        state["case_id"] != expected_id
        or state["status"] not in ALLOWED_CASE_STATUSES
    ):
        raise AuditError(f"{role} identity/status differs")
    attempts = _exact_int(state["attempt_count"], f"{role} attempt count")
    active = state["active_attempt"]
    if active is not None:
        active = _exact_int(active, f"{role} active attempt", minimum=1)
    last = state["last_completed_outcome_sha256"]
    if last is not None:
        _hex_digest(last, f"{role} last outcome digest")
    status = state["status"]
    if (status == "RUNNING_UNFINISHED_NONCLAIM") != (active is not None):
        raise AuditError(f"{role} active marker differs")
    if active is not None and active != attempts:
        raise AuditError(f"{role} active attempt number differs")
    if status == "PENDING":
        if attempts != 0 or active is not None or last is not None:
            raise AuditError(f"{role} pending state is not pristine")
    elif status == "RUNNING_UNFINISHED_NONCLAIM":
        if attempts < 1:
            raise AuditError(f"{role} active state has no attempt")
    elif attempts < 1 or active is not None or last is None:
        raise AuditError(f"{role} completed state lacks an outcome")
    return state


def _checkpoint_paths(run_directory: Path) -> tuple[Path, ...]:
    directory = run_directory / CHECKPOINT_DIR_NAME
    _assert_no_symlink_components(directory)
    if not directory.is_dir():
        raise AuditError("checkpoint directory is missing")
    paths = tuple(sorted(directory.iterdir()))
    if not paths:
        raise AuditError("checkpoint chain is empty")
    for sequence, path in enumerate(paths):
        match = CHECKPOINT_RE.fullmatch(path.name)
        if match is None or int(match.group(1)) != sequence:
            raise AuditError("checkpoint filenames are not exactly consecutive")
        _open_descriptor, _ = _open_regular_single_link(path, "checkpoint")
        os.close(_open_descriptor)
    return paths


def _validate_checkpoints(
    run_directory: Path,
    *,
    run_manifest_sha256: str,
    partition_sha256: str,
    case_ids: Sequence[str],
    base_seed: int,
) -> tuple[
    dict[str, Any],
    str,
    dict[tuple[str, int], str],
    dict[tuple[str, int], str],
    int,
]:
    previous_hash: str | None = None
    previous_cases: list[dict[str, Any]] | None = None
    previous_time: int | None = None
    config_hashes: dict[tuple[str, int], str] = {}
    outcome_hashes: dict[tuple[str, int], str] = {}
    latest: dict[str, Any] | None = None
    paths = _checkpoint_paths(run_directory)
    exact_claim_boundary = (
        "No aggregate SAT/UNSAT claim is made. SAT is candidate-only; "
        "all verified UNSAT leaves still require an independent coverage "
        "and proof replay."
    )
    for sequence, path in enumerate(paths):
        value, _, checkpoint_hash = _load_canonical_json(
            path, f"checkpoint {sequence}"
        )
        checkpoint = _exact_keys(value, CHECKPOINT_KEYS, f"checkpoint {sequence}")
        _exact_int(
            checkpoint["schema_version"],
            f"checkpoint {sequence} schema version",
            minimum=SCHEMA_VERSION,
            maximum=SCHEMA_VERSION,
        )
        _exact_int(
            checkpoint["sequence"],
            f"checkpoint {sequence} sequence",
            minimum=sequence,
            maximum=sequence,
        )
        if (
            checkpoint["schema"] != CHECKPOINT_SCHEMA
            or checkpoint["schema_version"] != SCHEMA_VERSION
            or checkpoint["sequence"] != sequence
            or checkpoint["previous_checkpoint_sha256"] != previous_hash
            or checkpoint["run_manifest_sha256"] != run_manifest_sha256
            or checkpoint["partition_sha256"] != partition_sha256
            or checkpoint["claim_boundary"] != exact_claim_boundary
        ):
            raise AuditError(f"checkpoint {sequence} header/link differs")
        written = _exact_int(
            checkpoint["written_unix_ns"],
            f"checkpoint {sequence} time",
        )
        if previous_time is not None and written < previous_time:
            raise AuditError(f"checkpoint {sequence} time moves backward")
        raw_cases = checkpoint["cases"]
        if not isinstance(raw_cases, list) or len(raw_cases) != len(case_ids):
            raise AuditError(f"checkpoint {sequence} case list differs")
        cases = [
            _case_state(
                raw_state,
                expected_id,
                f"checkpoint {sequence} case {expected_id}",
            )
            for raw_state, expected_id in zip(
                raw_cases, case_ids, strict=True
            )
        ]
        if checkpoint["aggregate_status"] != _summary_for_cases(cases):
            raise AuditError(f"checkpoint {sequence} aggregate status differs")
        event = checkpoint["event"]
        if not isinstance(event, dict):
            raise AuditError(f"checkpoint {sequence} event is not an object")
        if sequence == 0:
            _exact_keys(
                event,
                {"kind", "base_seed", "case_count"},
                "initial checkpoint event",
            )
            if (
                event["kind"] != "INITIALIZED_NO_SOLVER_RUN"
                or event["base_seed"] != base_seed
                or event["case_count"] != len(case_ids)
                or any(state["status"] != "PENDING" for state in cases)
            ):
                raise AuditError("initial checkpoint is not a pristine plan")
            _exact_int(
                event["base_seed"],
                "initial checkpoint base seed",
                minimum=base_seed,
                maximum=base_seed,
            )
            _exact_int(
                event["case_count"],
                "initial checkpoint case count",
                minimum=len(case_ids),
                maximum=len(case_ids),
            )
        else:
            if previous_cases is None:
                raise AssertionError("checkpoint predecessor invariant failed")
            changed = [
                index
                for index, (before, after) in enumerate(
                    zip(previous_cases, cases, strict=True)
                )
                if before != after
            ]
            if len(changed) != 1:
                raise AuditError(
                    f"checkpoint {sequence} must change exactly one case"
                )
            before = previous_cases[changed[0]]
            after = cases[changed[0]]
            kind = event.get("kind")
            if (
                event.get("case_id") != after["case_id"]
                or before["case_id"] != after["case_id"]
            ):
                raise AuditError(f"checkpoint {sequence} event case differs")
            case_id = after["case_id"]
            if kind == "ATTEMPT_RESERVED_NO_RESULT":
                _exact_keys(
                    event,
                    {
                        "kind",
                        "case_id",
                        "attempt_number",
                        "attempt_config_sha256",
                    },
                    f"checkpoint {sequence} reservation event",
                )
                attempt = _exact_int(
                    event["attempt_number"],
                    f"checkpoint {sequence} attempt",
                    minimum=1,
                )
                config_hash = _hex_digest(
                    event["attempt_config_sha256"],
                    f"checkpoint {sequence} attempt-config digest",
                )
                valid = (
                    before["status"] in {"PENDING", "RETRYABLE_NONCLAIM"}
                    and after["status"] == "RUNNING_UNFINISHED_NONCLAIM"
                    and after["attempt_count"] == before["attempt_count"] + 1
                    and after["active_attempt"] == after["attempt_count"] == attempt
                    and after["last_completed_outcome_sha256"]
                    == before["last_completed_outcome_sha256"]
                    and (case_id, attempt) not in config_hashes
                )
                if not valid:
                    raise AuditError(
                        f"checkpoint {sequence} reservation transition differs"
                    )
                config_hashes[(case_id, attempt)] = config_hash
            elif kind == "ATTEMPT_COMPLETED":
                _exact_keys(
                    event,
                    {
                        "kind",
                        "case_id",
                        "attempt_number",
                        "outcome_status",
                        "outcome_sha256",
                    },
                    f"checkpoint {sequence} completion event",
                )
                attempt = _exact_int(
                    event["attempt_number"],
                    f"checkpoint {sequence} attempt",
                    minimum=1,
                )
                outcome_hash = _hex_digest(
                    event["outcome_sha256"],
                    f"checkpoint {sequence} outcome digest",
                )
                status = event["outcome_status"]
                if status == "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION":
                    raise SatLeafPresentError(
                        f"SAT leaf {case_id} attempt {attempt} is never aggregated"
                    )
                expected_after = (
                    status
                    if status == LEAF_UNSAT
                    else (
                        "RETRYABLE_NONCLAIM"
                        if status in RETRYABLE_OUTCOMES
                        else None
                    )
                )
                valid = (
                    before["status"] == "RUNNING_UNFINISHED_NONCLAIM"
                    and after["status"] == expected_after
                    and after["attempt_count"] == before["attempt_count"] == attempt
                    and after["active_attempt"] is None
                    and after["last_completed_outcome_sha256"] == outcome_hash
                    and (case_id, attempt) in config_hashes
                    and (case_id, attempt) not in outcome_hashes
                )
                if not valid:
                    raise AuditError(
                        f"checkpoint {sequence} completion transition differs"
                    )
                outcome_hashes[(case_id, attempt)] = outcome_hash
            elif kind == "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM":
                _exact_keys(
                    event,
                    {
                        "kind",
                        "case_id",
                        "attempt_number",
                        "outcome_sha256",
                    },
                    f"checkpoint {sequence} recovery event",
                )
                attempt = _exact_int(
                    event["attempt_number"],
                    f"checkpoint {sequence} recovered attempt",
                    minimum=1,
                )
                outcome_hash = _hex_digest(
                    event["outcome_sha256"],
                    f"checkpoint {sequence} recovery digest",
                )
                valid = (
                    before["status"] == "RUNNING_UNFINISHED_NONCLAIM"
                    and after["status"] == "RETRYABLE_NONCLAIM"
                    and after["attempt_count"] == before["attempt_count"] == attempt
                    and after["active_attempt"] is None
                    and after["last_completed_outcome_sha256"] == outcome_hash
                    and (case_id, attempt) in config_hashes
                    and (case_id, attempt) not in outcome_hashes
                )
                if not valid:
                    raise AuditError(
                        f"checkpoint {sequence} recovery transition differs"
                    )
                outcome_hashes[(case_id, attempt)] = outcome_hash
            elif kind == "ORPHAN_ATTEMPT_RECONCILED_NONCLAIM":
                _exact_keys(
                    event,
                    {
                        "kind",
                        "case_id",
                        "attempt_number",
                        "attempt_config_sha256",
                        "outcome_status",
                        "outcome_sha256",
                    },
                    f"checkpoint {sequence} orphan reconciliation event",
                )
                attempt = _exact_int(
                    event["attempt_number"],
                    f"checkpoint {sequence} reconciled attempt",
                    minimum=1,
                )
                config_hash = _hex_digest(
                    event["attempt_config_sha256"],
                    f"checkpoint {sequence} attempt-config digest",
                )
                outcome_hash = _hex_digest(
                    event["outcome_sha256"],
                    f"checkpoint {sequence} outcome digest",
                )
                valid = (
                    before["status"] in {"PENDING", "RETRYABLE_NONCLAIM"}
                    and after["status"] == "RETRYABLE_NONCLAIM"
                    and after["attempt_count"] == before["attempt_count"] + 1
                    and after["attempt_count"] == attempt
                    and after["active_attempt"] is None
                    and after["last_completed_outcome_sha256"] == outcome_hash
                    and event["outcome_status"]
                    == "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM"
                    and (case_id, attempt) not in config_hashes
                    and (case_id, attempt) not in outcome_hashes
                )
                if not valid:
                    raise AuditError(
                        f"checkpoint {sequence} orphan transition differs"
                    )
                config_hashes[(case_id, attempt)] = config_hash
                outcome_hashes[(case_id, attempt)] = outcome_hash
            elif kind == "OUTCOME_CHECKPOINT_RECONCILED_NONCLAIM":
                _exact_keys(
                    event,
                    {
                        "kind",
                        "case_id",
                        "attempt_number",
                        "original_outcome_status",
                        "outcome_sha256",
                    },
                    f"checkpoint {sequence} outcome reconciliation event",
                )
                attempt = _exact_int(
                    event["attempt_number"],
                    f"checkpoint {sequence} reconciled attempt",
                    minimum=1,
                )
                original = event["original_outcome_status"]
                if original == "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION":
                    raise SatLeafPresentError(
                        f"SAT leaf {case_id} attempt {attempt} is never aggregated"
                    )
                if original not in RETRYABLE_OUTCOMES | {LEAF_UNSAT}:
                    raise AuditError(
                        f"checkpoint {sequence} reconciled status is unknown"
                    )
                outcome_hash = _hex_digest(
                    event["outcome_sha256"],
                    f"checkpoint {sequence} reconciled outcome digest",
                )
                valid = (
                    before["status"] == "RUNNING_UNFINISHED_NONCLAIM"
                    and after["status"] == "RETRYABLE_NONCLAIM"
                    and after["attempt_count"] == before["attempt_count"] == attempt
                    and after["active_attempt"] is None
                    and after["last_completed_outcome_sha256"] == outcome_hash
                    and (case_id, attempt) in config_hashes
                    and (case_id, attempt) not in outcome_hashes
                )
                if not valid:
                    raise AuditError(
                        f"checkpoint {sequence} outcome reconciliation differs"
                    )
                outcome_hashes[(case_id, attempt)] = outcome_hash
            else:
                raise AuditError(f"checkpoint {sequence} event kind is unknown")
        previous_hash = checkpoint_hash
        previous_cases = cases
        previous_time = written
        latest = checkpoint
    if latest is None or previous_hash is None:
        raise AssertionError("checkpoint audit returned no latest state")
    latest_cases = latest["cases"]
    if not isinstance(latest_cases, list):
        raise AuditError("latest checkpoint cases are malformed")
    active_keys = {
        (state["case_id"], state["active_attempt"])
        for state in latest_cases
        if isinstance(state, dict) and state["active_attempt"] is not None
    }
    if len(active_keys) > 1:
        raise AuditError("latest checkpoint has multiple active attempts")
    if (
        set(outcome_hashes) - set(config_hashes)
        or set(config_hashes) - set(outcome_hashes) != active_keys
    ):
        raise AuditError("checkpoint chain has an unbound attempt")
    return latest, previous_hash, config_hashes, outcome_hashes, len(paths)


def _compact_json_bytes(value: object) -> bytes:
    try:
        encoded = json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError, RecursionError) as error:
        raise AuditError("command is not finite canonical JSON") from error
    return (encoded + "\n").encode("utf-8")


def _command_sha256(command: Sequence[str]) -> str:
    return sha256(_compact_json_bytes(list(command))).hexdigest()


def _expected_commands(
    manifest: Mapping[str, Any],
    case: Mapping[str, Any],
    attempt_directory: Path,
    scope: FrozenScope,
) -> dict[str, list[str]]:
    tools = manifest["tools"]
    limits = manifest["limits"]
    if not isinstance(tools, dict) or not isinstance(limits, dict):
        raise AuditError("run command inputs are malformed")
    cadical = tools["cadical"]
    drat_trim = tools["drat_trim"]
    lrat_check = tools["lrat_check"]
    normalizer_python = tools["normalizer_python"]
    if not all(
        isinstance(item, dict)
        for item in (cadical, drat_trim, lrat_check, normalizer_python)
    ):
        raise AuditError("run command tool records are malformed")
    instance = (attempt_directory / "instance.cnf").resolve()
    result = (attempt_directory / "solver.result").resolve()
    raw_proof = (attempt_directory / "proof.raw.bdrat").resolve()
    normalized = (
        attempt_directory / "proof.normalized.rup.bdrat"
    ).resolve()
    normalization_report = (
        attempt_directory / "normalization-report.json"
    ).resolve()
    converted = (attempt_directory / "proof.converted.lrat").resolve()
    return {
        "solver": [
            str(cadical["path"]),
            f"--seed={case['seed']}",
            "--binary",
            "--no-colors",
            "-q",
            "-t",
            str(limits["solver_wall_seconds"]),
            "-w",
            str(result),
            str(instance),
            str(raw_proof),
        ],
        "raw_forward": [
            str(drat_trim["path"]),
            str(instance),
            str(raw_proof),
            "-i",
            "-f",
            "-W",
            "-t",
            str(limits["converter_wall_seconds"]),
        ],
        "normalizer": [
            str(normalizer_python["path"]),
            str(
                (
                    scope.campaign_root
                    / "src/search/k4_production/normalize_bdrat.py"
                ).resolve()
            ),
            "--input",
            str(raw_proof),
            "--output",
            str(normalized),
            "--report",
            str(normalization_report),
            "--max-variable",
            str(scope.variable_count),
        ],
        "normalized_forward": [
            str(drat_trim["path"]),
            str(instance),
            str(normalized),
            "-i",
            "-f",
            "-W",
            "-U",
            "-t",
            str(limits["converter_wall_seconds"]),
        ],
        "lrat_conversion": [
            str(drat_trim["path"]),
            str(instance),
            str(normalized),
            "-i",
            "-W",
            "-U",
            "-L",
            str(converted),
            "-t",
            str(limits["converter_wall_seconds"]),
        ],
        "lrat_check": [
            str(lrat_check["path"]),
            str(instance),
            str(converted),
        ],
    }


def _strict_forward_success(stdout: bytes, stderr: bytes, role: str) -> None:
    if stderr:
        raise AuditError(f"{role} wrote to stderr")
    try:
        text = stdout.decode("ascii")
    except UnicodeDecodeError as error:
        raise AuditError(f"{role} stdout is not ASCII") from error
    lines = [
        line.strip()
        for line in text.replace("\r", "\n").splitlines()
        if line.strip()
    ]
    lowered = "\n".join(lines).lower()
    if (
        lines.count("s VERIFIED") != 1
        or "warning" in lowered
        or "error" in lowered
        or "not verified" in lowered
    ):
        raise AuditError(f"{role} lacks one clean VERIFIED status")


def _strict_lrat_success(stdout: bytes, stderr: bytes, role: str) -> None:
    if stderr:
        raise AuditError(f"{role} wrote to stderr")
    try:
        text = stdout.decode("ascii")
    except UnicodeDecodeError as error:
        raise AuditError(f"{role} stdout is not ASCII") from error
    lines = [
        line.strip()
        for line in text.replace("\r", "\n").splitlines()
        if line.strip()
    ]
    lowered = "\n".join(lines).lower()
    if (
        lines.count("c VERIFIED") != 1
        or "warning" in lowered
        or "error" in lowered
        or "not verified" in lowered
    ):
        raise AuditError(f"{role} lacks one clean VERIFIED status")


def _strict_solver_unsat(payload: bytes, role: str) -> None:
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise AuditError(f"{role} is not ASCII") from error
    if text != "s UNSATISFIABLE\n":
        raise AuditError(f"{role} is not the exact one-line UNSAT result")


def _strict_normalizer_success(
    stdout: bytes,
    stderr: bytes,
    role: str,
) -> None:
    if stderr or stdout != b"s NORMALIZED\n":
        raise AuditError(f"{role} lacks the exact NORMALIZED status")


def _encode_unsigned(value: int) -> bytes:
    encoded = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            encoded.append(byte | 0x80)
        else:
            encoded.append(byte)
            return bytes(encoded)


def _decode_unsigned(
    source: BinaryIO,
    *,
    record_index: int,
    maximum_code: int,
) -> tuple[int, bytes]:
    encoded = bytearray()
    value = 0
    shift = 0
    while True:
        byte = source.read(1)
        if not byte:
            raise AuditError(
                f"binary DRAT record {record_index} has an unterminated varint"
            )
        encoded.append(byte[0])
        if len(encoded) > MAX_UNSIGNED_VARINT_BYTES:
            raise AuditError(
                f"binary DRAT record {record_index} has an oversized varint"
            )
        value |= (byte[0] & 0x7F) << shift
        if byte[0] < 0x80:
            break
        shift += 7
    if bytes(encoded) != _encode_unsigned(value):
        raise AuditError(
            f"binary DRAT record {record_index} has a noncanonical varint"
        )
    if value > maximum_code:
        raise AuditError(
            f"binary DRAT record {record_index} exceeds the variable bound"
        )
    return value, bytes(encoded)


def _scan_binary_drat(
    path: Path,
    *,
    maximum_variable: int,
    role: str,
) -> dict[str, Any]:
    descriptor, before = _open_regular_single_link(path, role)
    maximum_code = 2 * maximum_variable + 1
    total = additions = deletions = post_empty_deletions = literals = 0
    addition_literals = 0
    maximum_observed = addition_maximum_observed = 0
    empty_record: int | None = None
    addition_digest = sha256()
    addition_size = 0
    try:
        with os.fdopen(descriptor, "rb", buffering=1 << 20) as source:
            descriptor = -1
            while True:
                prefix = source.read(1)
                if not prefix:
                    break
                total += 1
                if prefix not in {b"a", b"d"}:
                    raise AuditError(
                        f"{role} record {total} has an invalid prefix"
                    )
                is_addition = prefix == b"a"
                encoded_clause = bytearray()
                clause_length = 0
                while True:
                    value, encoded = _decode_unsigned(
                        source,
                        record_index=total,
                        maximum_code=maximum_code,
                    )
                    encoded_clause.extend(encoded)
                    if value == 0:
                        break
                    if value == 1:
                        raise AuditError(
                            f"{role} record {total} contains negative zero"
                        )
                    variable = value >> 1
                    maximum_observed = max(maximum_observed, variable)
                    literals += 1
                    clause_length += 1
                    if is_addition:
                        addition_literals += 1
                        addition_maximum_observed = max(
                            addition_maximum_observed, variable
                        )
                if is_addition:
                    additions += 1
                    if empty_record is not None:
                        raise AuditError(
                            f"{role} contains an addition after its empty addition"
                        )
                    payload = prefix + bytes(encoded_clause)
                    addition_digest.update(payload)
                    addition_size += len(payload)
                    if clause_length == 0:
                        empty_record = total
                else:
                    deletions += 1
                    if clause_length == 0:
                        raise AuditError(f"{role} contains an empty deletion")
                    if empty_record is not None:
                        post_empty_deletions += 1
            after = _stamp(os.fstat(source.fileno()))
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if before != after:
        raise AuditError(f"{role} changed while scanning")
    if total == 0 or empty_record is None:
        raise AuditError(f"{role} is empty or has no empty addition")
    return {
        "record_counts": {
            "total": total,
            "additions": additions,
            "deletions": deletions,
            "post_empty_deletions": post_empty_deletions,
            "literals": literals,
        },
        "addition_literal_count": addition_literals,
        "max_variable_observed": maximum_observed,
        "addition_max_variable_observed": addition_maximum_observed,
        "empty_addition_record_index": empty_record,
        "addition_stream_sha256": addition_digest.hexdigest(),
        "addition_stream_size_bytes": addition_size,
    }


def _validate_normalization_report(
    report_path: Path,
    raw_proof_path: Path,
    normalized_proof_path: Path,
    scope: FrozenScope,
) -> dict[str, Any]:
    value, _, _ = _load_canonical_json(report_path, "normalization report")
    report = _exact_keys(
        value,
        {
            "schema",
            "schema_version",
            "policy",
            "claim_status",
            "max_variable_allowed",
            "max_variable_observed",
            "record_counts",
            "empty_addition_record_index",
            "input",
            "output",
        },
        "normalization report",
    )
    _exact_int(
        report["schema_version"],
        "normalization-report schema version",
        minimum=1,
        maximum=1,
    )
    counts = _exact_keys(
        report["record_counts"],
        {
            "total",
            "additions",
            "deletions",
            "post_empty_deletions",
            "literals",
        },
        "normalization record counts",
    )
    for name in counts:
        _exact_int(counts[name], f"normalization count {name}")
    maximum_observed = _exact_int(
        report["max_variable_observed"],
        "normalization maximum variable",
        maximum=scope.variable_count,
    )
    empty_index = _exact_int(
        report["empty_addition_record_index"],
        "normalization empty-addition index",
        minimum=1,
    )
    if (
        report["schema"] != NORMALIZATION_SCHEMA
        or report["schema_version"] != 1
        or report["policy"] != NORMALIZATION_POLICY
        or report["claim_status"]
        != "TRANSFORMATION_ONLY_NO_PROOF_CLAIM"
        or report["max_variable_allowed"] != scope.variable_count
        or counts["total"] != counts["additions"] + counts["deletions"]
        or counts["additions"] < 1
        or counts["post_empty_deletions"] > counts["deletions"]
        or counts["additions"] > empty_index
        or empty_index + counts["post_empty_deletions"] != counts["total"]
        or counts["literals"] < counts["total"] - 1
        or maximum_observed > scope.variable_count
        or ((counts["literals"] == 0) != (maximum_observed == 0))
    ):
        raise AuditError("normalization report semantics differ")
    input_binding = _binding(
        report["input"],
        "normalization input",
        expected_path=raw_proof_path,
    )
    output_binding = _binding(
        report["output"],
        "normalization output",
        expected_path=normalized_proof_path,
    )
    if output_binding["size_bytes"] == 0:
        raise AuditError("normalized binary proof is empty")
    raw_scan = _scan_binary_drat(
        raw_proof_path,
        maximum_variable=scope.variable_count,
        role="raw binary DRAT proof",
    )
    normalized_scan = _scan_binary_drat(
        normalized_proof_path,
        maximum_variable=scope.variable_count,
        role="normalized binary RUP proof",
    )
    if (
        raw_scan["record_counts"] != counts
        or raw_scan["max_variable_observed"] != maximum_observed
        or raw_scan["empty_addition_record_index"] != empty_index
        or raw_scan["addition_stream_sha256"] != output_binding["sha256"]
        or raw_scan["addition_stream_size_bytes"]
        != output_binding["size_bytes"]
        or input_binding["sha256"]
        != _stable_file_hash(raw_proof_path, "normalization raw input")[0]
    ):
        raise AuditError("normalization report differs from the raw stream")
    normalized_counts = normalized_scan["record_counts"]
    raw_counts = raw_scan["record_counts"]
    if (
        normalized_counts["total"] != raw_counts["additions"]
        or normalized_counts["additions"] != raw_counts["additions"]
        or normalized_counts["deletions"] != 0
        or normalized_counts["post_empty_deletions"] != 0
        or normalized_counts["literals"]
        != raw_scan["addition_literal_count"]
        or normalized_scan["max_variable_observed"]
        != raw_scan["addition_max_variable_observed"]
        or normalized_scan["empty_addition_record_index"]
        != raw_counts["additions"]
    ):
        raise AuditError(
            "normalized proof is not exactly the raw addition stream"
        )
    return report


def _validate_passing_resource_report(
    path: Path,
    *,
    phase: str,
    memory_limit_mib: int,
    limits: Mapping[str, Any],
) -> dict[str, Any]:
    value, _, _ = _load_canonical_json(path, f"{phase} resource report")
    report = _exact_keys(
        value,
        {
            "schema",
            "phase",
            "checked_unix_ns",
            "load_average_one_minute",
            "load_ceiling",
            "available_memory_bytes",
            "required_memory_bytes",
            "free_disk_bytes",
            "required_free_disk_bytes",
            "worst_case_live_file_slots",
            "checks",
            "probe_errors",
            "passed",
        },
        f"{phase} resource report",
    )
    checked = _exact_int(
        report["checked_unix_ns"], f"{phase} resource time", minimum=1
    )
    del checked
    observed_load = report["load_average_one_minute"]
    if (
        type(observed_load) not in (int, float)
        or not math.isfinite(float(observed_load))
        or float(observed_load) < 0
    ):
        raise AuditError(f"{phase} resource load is malformed")
    available = _exact_int(
        report["available_memory_bytes"],
        f"{phase} available memory",
        minimum=1,
    )
    free_disk = _exact_int(
        report["free_disk_bytes"], f"{phase} free disk", minimum=1
    )
    expected_memory = (
        memory_limit_mib + int(limits["memory_reserve_mib"])
    ) << 20
    expected_disk = (
        int(limits["disk_reserve_mib"])
        + WORST_CASE_LIVE_FILE_SLOTS * int(limits["file_limit_mib"])
        + DISK_METADATA_ALLOWANCE_MIB
    ) << 20
    if (
        report["schema"] != "gamma-theta-k4-resource-gate-v1"
        or report["phase"] != phase
        or report["load_ceiling"] != limits["load_max"]
        or float(observed_load) > float(limits["load_max"])
        or report["required_memory_bytes"] != expected_memory
        or available < expected_memory
        or report["required_free_disk_bytes"] != expected_disk
        or free_disk < expected_disk
        or report["worst_case_live_file_slots"]
        != WORST_CASE_LIVE_FILE_SLOTS
        or report["checks"] != {
            "load": True,
            "memory": True,
            "disk": True,
        }
        or report["probe_errors"] != []
        or report["passed"] is not True
    ):
        raise AuditError(f"{phase} resource report was not a clean pass")
    return report


def _validate_inventory(
    value: object,
    attempt_directory: Path,
) -> dict[str, dict[str, Any]]:
    if not isinstance(value, dict):
        raise AuditError("attempt artifact inventory is not an object")
    observed: dict[str, tuple[str, int]] = {}
    for path in sorted(attempt_directory.iterdir()):
        if path.name == "outcome.json":
            continue
        if "/" in path.name or path.name in {"", ".", ".."}:
            raise AuditError("attempt artifact name is malformed")
        digest, size = _stable_file_hash(path, f"attempt artifact {path.name}")
        observed[path.name] = (digest, size)
    if set(value) != set(observed):
        raise AuditError("attempt artifact inventory filenames differ")
    result: dict[str, dict[str, Any]] = {}
    for name, raw_binding in value.items():
        if type(name) is not str:
            raise AuditError("attempt artifact inventory name is not a string")
        digest, size = observed[name]
        binding = _binding(
            raw_binding,
            f"attempt artifact {name}",
            expected_path=attempt_directory / name,
            expected_sha256=digest,
            expected_size=size,
        )
        result[name] = binding
    return result


def _finite_nonnegative(value: object, role: str) -> float:
    if (
        type(value) is not float
        or not math.isfinite(value)
        or value < 0
    ):
        raise AuditError(f"{role} must be a finite nonnegative number")
    return float(value)


def _validate_child_record(
    value: object,
    *,
    role: str,
    expected_command: Sequence[str],
    expected_executable_sha256: str,
    expected_exit_code: int,
    expected_stdout: Path,
    expected_stderr: Path,
    expected_wall_limit: int,
    expected_memory_limit: int,
    expected_file_limit: int,
) -> dict[str, Any]:
    child = _exact_keys(value, CHILD_KEYS, f"{role} child record")
    _exact_int(
        child["exit_code"],
        f"{role} exit code",
        minimum=expected_exit_code,
        maximum=expected_exit_code,
    )
    if (
        child["command"] != list(expected_command)
        or child["command_sha256"] != _command_sha256(expected_command)
        or child["executable_sha256_before"] != expected_executable_sha256
        or child["executable_sha256_after"] != expected_executable_sha256
        or child["exit_code"] != expected_exit_code
        or child["termination_signal"] is not None
        or child["timed_out"] is not False
        or child["memory_limit_exceeded"] is not False
    ):
        raise AuditError(f"{role} decisive child status differs")
    started = _exact_int(child["started_unix_ns"], f"{role} start time", minimum=1)
    finished = _exact_int(
        child["finished_unix_ns"], f"{role} finish time", minimum=started
    )
    if finished < started:
        raise AuditError(f"{role} finish time precedes start time")
    for key in (
        "wall_seconds",
        "user_cpu_seconds",
        "system_cpu_seconds",
        "maximum_resident_set_size_mib",
        "peak_polled_resident_set_size_mib",
    ):
        _finite_nonnegative(child[key], f"{role} {key}")
    _exact_int(
        child["maximum_resident_set_size_raw"],
        f"{role} raw maximum resident size",
    )
    _exact_int(
        child["available_memory_before_bytes"],
        f"{role} available memory",
        minimum=1,
    )
    expected_rss_unit = "bytes" if sys.platform == "darwin" else "KiB"
    if (
        child["maximum_resident_set_size_raw_unit"] != expected_rss_unit
        or child["wall_limit_seconds"] != expected_wall_limit
        or child["memory_limit_mib"] != expected_memory_limit
        or child["file_limit_mib"] != expected_file_limit
    ):
        raise AuditError(f"{role} resource record differs")
    for key, expected in (
        ("wall_limit_seconds", expected_wall_limit),
        ("memory_limit_mib", expected_memory_limit),
        ("file_limit_mib", expected_file_limit),
    ):
        _exact_int(
            child[key],
            f"{role} {key}",
            minimum=expected,
            maximum=expected,
        )
    stdout_hash, _ = _stable_file_hash(expected_stdout, f"{role} stdout")
    stderr_hash, _ = _stable_file_hash(expected_stderr, f"{role} stderr")
    if (
        child["stdout_path"] != str(expected_stdout.resolve())
        or child["stdout_sha256"] != stdout_hash
        or child["stderr_path"] != str(expected_stderr.resolve())
        or child["stderr_sha256"] != stderr_hash
    ):
        raise AuditError(f"{role} child output binding differs")
    return child


def _certificate_binding(
    certificate: Mapping[str, Any],
    key: str,
    attempt_directory: Path,
    filename: str,
    role: str,
) -> dict[str, Any]:
    return _binding(
        certificate[key],
        role,
        expected_path=attempt_directory / filename,
    )


def _validate_leaf_certificate(
    *,
    certificate_path: Path,
    outcome: Mapping[str, Any],
    inventory: Mapping[str, Mapping[str, Any]],
    config: Mapping[str, Any],
    manifest: Mapping[str, Any],
    case: Mapping[str, Any],
    attempt_directory: Path,
    scope: FrozenScope,
) -> dict[str, Any]:
    if set(inventory) != DECISIVE_ARTIFACT_NAMES:
        raise AuditError(
            f"case {case['case_id']} decisive artifact filename set differs"
        )
    value, raw, certificate_hash = _load_canonical_json(
        certificate_path, f"leaf certificate {case['case_id']}"
    )
    certificate = _exact_keys(value, CERTIFICATE_KEYS, "leaf certificate")
    _exact_int(
        certificate["schema_version"],
        f"leaf certificate {case['case_id']} schema version",
        minimum=LEAF_CERTIFICATE_SCHEMA_VERSION,
        maximum=LEAF_CERTIFICATE_SCHEMA_VERSION,
    )
    if (
        not isinstance(certificate["cube_literals"], list)
        or any(
            type(literal) is not int
            for literal in certificate["cube_literals"]
        )
    ):
        raise AuditError(
            f"leaf certificate {case['case_id']} cube literals are malformed"
        )
    if (
        certificate["schema"] != LEAF_CERTIFICATE_SCHEMA
        or certificate["schema_version"] != LEAF_CERTIFICATE_SCHEMA_VERSION
        or certificate["proof_pipeline"] != PROOF_PIPELINE_ID
        or certificate["leaf_status"] != LEAF_UNSAT
        or certificate["aggregate_status"]
        != "NO_AGGREGATE_CLAIM_PENDING_INDEPENDENT_COVERAGE_AUDIT"
        or certificate["case_id"] != case["case_id"]
        or certificate["cube_literals"] != case["cube_literals"]
    ):
        raise AuditError(f"leaf certificate {case['case_id']} header differs")

    bindings = {
        "case_cnf": ("instance.cnf", "certificate case CNF"),
        "raw_solver_result": ("solver.result", "certificate raw solver result"),
        "raw_binary_drat": ("proof.raw.bdrat", "certificate raw binary DRAT"),
        "normalized_binary_rup": (
            "proof.normalized.rup.bdrat",
            "certificate normalized binary RUP proof",
        ),
        "normalization_report": (
            "normalization-report.json",
            "certificate normalization report",
        ),
        "converted_lrat": ("proof.converted.lrat", "certificate converted LRAT"),
        "solver_resource": (
            "resource-solver.json",
            "certificate solver resource report",
        ),
        "raw_forward_resource": (
            "resource-raw-forward.json",
            "certificate raw-forward resource report",
        ),
        "normalizer_resource": (
            "resource-normalizer.json",
            "certificate normalizer resource report",
        ),
        "normalized_forward_resource": (
            "resource-normalized-forward.json",
            "certificate normalized-forward resource report",
        ),
        "lrat_conversion_resource": (
            "resource-lrat-conversion.json",
            "certificate LRAT-conversion resource report",
        ),
        "lrat_check_resource": (
            "resource-lrat-check.json",
            "certificate lrat-check resource report",
        ),
        "solver_stdout": ("solver.stdout", "certificate solver stdout"),
        "solver_stderr": ("solver.stderr", "certificate solver stderr"),
        "raw_forward_stdout": (
            "raw-forward.stdout",
            "certificate raw-forward stdout",
        ),
        "raw_forward_stderr": (
            "raw-forward.stderr",
            "certificate raw-forward stderr",
        ),
        "normalizer_stdout": (
            "normalizer.stdout",
            "certificate normalizer stdout",
        ),
        "normalizer_stderr": (
            "normalizer.stderr",
            "certificate normalizer stderr",
        ),
        "normalized_forward_stdout": (
            "normalized-forward.stdout",
            "certificate normalized-forward stdout",
        ),
        "normalized_forward_stderr": (
            "normalized-forward.stderr",
            "certificate normalized-forward stderr",
        ),
        "lrat_conversion_stdout": (
            "lrat-conversion.stdout",
            "certificate LRAT-conversion stdout",
        ),
        "lrat_conversion_stderr": (
            "lrat-conversion.stderr",
            "certificate LRAT-conversion stderr",
        ),
        "lrat_check_stdout": (
            "lrat-check.stdout",
            "certificate lrat-check stdout",
        ),
        "lrat_check_stderr": (
            "lrat-check.stderr",
            "certificate lrat-check stderr",
        ),
    }
    checked_bindings = {
        key: _certificate_binding(
            certificate,
            key,
            attempt_directory,
            filename,
            role,
        )
        for key, (filename, role) in bindings.items()
    }
    if (
        checked_bindings["case_cnf"]["sha256"] != case["cnf_sha256"]
        or checked_bindings["case_cnf"]["size_bytes"] != case["cnf_size_bytes"]
        or checked_bindings["raw_binary_drat"]["size_bytes"] == 0
        or checked_bindings["normalized_binary_rup"]["size_bytes"] == 0
        or checked_bindings["converted_lrat"]["size_bytes"] == 0
    ):
        raise AuditError(f"leaf certificate {case['case_id']} proof inputs differ")
    for key, (filename, _) in bindings.items():
        if filename not in inventory or inventory[filename] != checked_bindings[key]:
            raise AuditError(
                f"leaf certificate {case['case_id']} escapes its inventory"
            )

    raw_result = _stable_file_bytes(
        attempt_directory / "solver.result",
        f"case {case['case_id']} solver result",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    _strict_solver_unsat(raw_result, f"case {case['case_id']} solver result")
    raw_forward_stdout = _stable_file_bytes(
        attempt_directory / "raw-forward.stdout",
        f"case {case['case_id']} raw-forward stdout",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    raw_forward_stderr = _stable_file_bytes(
        attempt_directory / "raw-forward.stderr",
        f"case {case['case_id']} raw-forward stderr",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    normalizer_stdout = _stable_file_bytes(
        attempt_directory / "normalizer.stdout",
        f"case {case['case_id']} normalizer stdout",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    normalizer_stderr = _stable_file_bytes(
        attempt_directory / "normalizer.stderr",
        f"case {case['case_id']} normalizer stderr",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    normalized_stdout = _stable_file_bytes(
        attempt_directory / "normalized-forward.stdout",
        f"case {case['case_id']} normalized-forward stdout",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    normalized_stderr = _stable_file_bytes(
        attempt_directory / "normalized-forward.stderr",
        f"case {case['case_id']} normalized-forward stderr",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    conversion_stdout = _stable_file_bytes(
        attempt_directory / "lrat-conversion.stdout",
        f"case {case['case_id']} LRAT-conversion stdout",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    conversion_stderr = _stable_file_bytes(
        attempt_directory / "lrat-conversion.stderr",
        f"case {case['case_id']} LRAT-conversion stderr",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    historic_stdout = _stable_file_bytes(
        attempt_directory / "lrat-check.stdout",
        f"case {case['case_id']} historic lrat-check stdout",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    historic_stderr = _stable_file_bytes(
        attempt_directory / "lrat-check.stderr",
        f"case {case['case_id']} historic lrat-check stderr",
        maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
    )
    _strict_forward_success(
        raw_forward_stdout,
        raw_forward_stderr,
        f"case {case['case_id']} raw-forward check",
    )
    _strict_normalizer_success(
        normalizer_stdout,
        normalizer_stderr,
        f"case {case['case_id']} normalizer",
    )
    _validate_normalization_report(
        attempt_directory / "normalization-report.json",
        attempt_directory / "proof.raw.bdrat",
        attempt_directory / "proof.normalized.rup.bdrat",
        scope,
    )
    _strict_forward_success(
        normalized_stdout,
        normalized_stderr,
        f"case {case['case_id']} normalized-forward check",
    )
    _strict_forward_success(
        conversion_stdout,
        conversion_stderr,
        f"case {case['case_id']} LRAT conversion",
    )
    _strict_lrat_success(
        historic_stdout,
        historic_stderr,
        f"case {case['case_id']} historic lrat-check",
    )

    if config["construction_status"] != "ORIGINAL_PRE_RESERVATION":
        raise AuditError(
            f"case {case['case_id']} decisive config was reconstructed"
        )
    commands = _expected_commands(manifest, case, attempt_directory, scope)
    limits = manifest["limits"]
    normalizer_python = manifest["tools"]["normalizer_python"]
    if not isinstance(normalizer_python, dict):
        raise AuditError("normalizer Python binding is malformed")
    child_parameters = {
        "solver": (
            scope.cadical_sha256,
            20,
            "solver.stdout",
            "solver.stderr",
            limits["solver_wall_seconds"],
            limits["solver_memory_mib"],
        ),
        "raw_forward": (
            scope.drat_trim_sha256,
            0,
            "raw-forward.stdout",
            "raw-forward.stderr",
            limits["converter_wall_seconds"],
            limits["postprocess_memory_mib"],
        ),
        "normalizer": (
            normalizer_python["sha256"],
            0,
            "normalizer.stdout",
            "normalizer.stderr",
            limits["converter_wall_seconds"],
            limits["postprocess_memory_mib"],
        ),
        "normalized_forward": (
            scope.drat_trim_sha256,
            0,
            "normalized-forward.stdout",
            "normalized-forward.stderr",
            limits["converter_wall_seconds"],
            limits["postprocess_memory_mib"],
        ),
        "lrat_conversion": (
            scope.drat_trim_sha256,
            0,
            "lrat-conversion.stdout",
            "lrat-conversion.stderr",
            limits["converter_wall_seconds"],
            limits["postprocess_memory_mib"],
        ),
        "lrat_check": (
            scope.lrat_check_sha256,
            0,
            "lrat-check.stdout",
            "lrat-check.stderr",
            limits["checker_wall_seconds"],
            limits["postprocess_memory_mib"],
        ),
    }
    children: dict[str, dict[str, Any]] = {}
    for key, (
        executable_hash,
        exit_code,
        stdout_name,
        stderr_name,
        wall_limit,
        memory_limit,
    ) in child_parameters.items():
        children[key] = _validate_child_record(
            certificate[key],
            role=f"case {case['case_id']} {key}",
            expected_command=commands[key],
            expected_executable_sha256=executable_hash,
            expected_exit_code=exit_code,
            expected_stdout=attempt_directory / stdout_name,
            expected_stderr=attempt_directory / stderr_name,
            expected_wall_limit=wall_limit,
            expected_memory_limit=memory_limit,
            expected_file_limit=limits["file_limit_mib"],
        )

    resource_expectations = {
        "solver_resource": ("solver", limits["solver_memory_mib"]),
        "raw_forward_resource": (
            "raw-forward",
            limits["postprocess_memory_mib"],
        ),
        "normalizer_resource": (
            "normalizer",
            limits["postprocess_memory_mib"],
        ),
        "normalized_forward_resource": (
            "normalized-forward",
            limits["postprocess_memory_mib"],
        ),
        "lrat_conversion_resource": (
            "lrat-conversion",
            limits["postprocess_memory_mib"],
        ),
        "lrat_check_resource": (
            "lrat-check",
            limits["postprocess_memory_mib"],
        ),
    }
    for certificate_key, (phase, memory_limit) in resource_expectations.items():
        filename = bindings[certificate_key][0]
        report = _validate_passing_resource_report(
            attempt_directory / filename,
            phase=phase,
            memory_limit_mib=memory_limit,
            limits=limits,
        )
        del report

    details = _exact_keys(
        outcome["details"],
        {
            "certificate",
            "solver",
            "raw_forward",
            "normalizer",
            "normalized_forward",
            "lrat_conversion",
            "lrat_check",
        },
        f"case {case['case_id']} terminal outcome details",
    )
    certificate_binding = _binding(
        details["certificate"],
        f"case {case['case_id']} certificate",
        expected_path=certificate_path,
        expected_sha256=certificate_hash,
        expected_size=len(raw),
    )
    if (
        "certificate.json" not in inventory
        or inventory["certificate.json"] != certificate_binding
        or any(details[key] != children[key] for key in children)
    ):
        raise AuditError(
            f"case {case['case_id']} outcome/certificate binding differs"
        )
    return {
        "case_id": case["case_id"],
        "certificate_path": certificate_path,
        "certificate_sha256": certificate_hash,
        "cnf_path": attempt_directory / "instance.cnf",
        "cnf_sha256": checked_bindings["case_cnf"]["sha256"],
        "cube_literals": list(case["cube_literals"]),
        "lrat_path": attempt_directory / "proof.converted.lrat",
        "lrat_sha256": checked_bindings["converted_lrat"]["sha256"],
        "lrat_size_bytes": checked_bindings["converted_lrat"]["size_bytes"],
    }


def _validate_attempts(
    run_directory: Path,
    *,
    manifest: Mapping[str, Any],
    manifest_sha256: str,
    partition_sha256: str,
    parent: bytes,
    cases: Sequence[Mapping[str, Any]],
    latest: Mapping[str, Any],
    config_hashes: Mapping[tuple[str, int], str],
    outcome_hashes: Mapping[tuple[str, int], str],
    scope: FrozenScope,
) -> tuple[tuple[dict[str, Any], ...], int]:
    case_root = run_directory / CASE_DIR_NAME
    _assert_no_symlink_components(case_root)
    if not case_root.is_dir():
        raise AuditError("case directory is missing")
    expected_names = {f"case-{case['case_id']}" for case in cases}
    observed_names = {path.name for path in case_root.iterdir()}
    if observed_names != expected_names:
        raise AuditError("case directory set differs from the partition")
    raw_states = latest["cases"]
    if not isinstance(raw_states, list) or len(raw_states) != len(cases):
        raise AuditError("latest checkpoint case state list differs")

    terminals: list[dict[str, Any]] = []
    seen_attempts: set[tuple[str, int]] = set()
    seen_outcomes: set[tuple[str, int]] = set()
    historical_count = 0
    for case, state in zip(cases, raw_states, strict=True):
        case_id = case["case_id"]
        case_directory = case_root / f"case-{case_id}"
        _assert_no_symlink_components(case_directory)
        if case_directory.is_symlink() or not case_directory.is_dir():
            raise AuditError(f"case {case_id} directory is malformed")
        attempts = tuple(sorted(case_directory.iterdir()))
        attempt_count = state["attempt_count"]
        if len(attempts) != attempt_count:
            raise AuditError(f"case {case_id} attempt count differs")
        last_status: str | None = None
        last_hash: str | None = None
        expected_leaf = _leaf_bytes(parent, case["cube_literals"], scope)
        for attempt_number, attempt_directory in enumerate(attempts, start=1):
            historical_count += 1
            key = (case_id, attempt_number)
            seen_attempts.add(key)
            match = ATTEMPT_RE.fullmatch(attempt_directory.name)
            if (
                match is None
                or int(match.group(1)) != attempt_number
                or attempt_directory.is_symlink()
                or not attempt_directory.is_dir()
            ):
                raise AuditError(f"case {case_id} attempt layout differs")
            _assert_no_symlink_components(attempt_directory)
            config_path = attempt_directory / "attempt-config.json"
            config_value, _, config_hash = _load_canonical_json(
                config_path,
                f"case {case_id} attempt {attempt_number} configuration",
            )
            config = _exact_keys(
                config_value,
                ATTEMPT_CONFIG_KEYS,
                f"case {case_id} attempt configuration",
            )
            _exact_int(
                config["schema_version"],
                f"case {case_id} attempt schema version",
                minimum=ATTEMPT_CONFIG_SCHEMA_VERSION,
                maximum=ATTEMPT_CONFIG_SCHEMA_VERSION,
            )
            _exact_int(
                config["attempt_number"],
                f"case {case_id} attempt number",
                minimum=attempt_number,
                maximum=attempt_number,
            )
            _exact_int(
                config["seed"],
                f"case {case_id} attempt seed",
                minimum=case["seed"],
                maximum=case["seed"],
            )
            if (
                not isinstance(config["cube_literals"], list)
                or any(
                    type(literal) is not int
                    for literal in config["cube_literals"]
                )
            ):
                raise AuditError(
                    f"case {case_id} attempt cube literals are malformed"
                )
            commands = _expected_commands(
                manifest, case, attempt_directory, scope
            )
            if (
                config["schema"] != ATTEMPT_CONFIG_SCHEMA
                or config["schema_version"] != ATTEMPT_CONFIG_SCHEMA_VERSION
                or config["proof_pipeline"] != PROOF_PIPELINE_ID
                or config["claim_status"] != RUN_CLAIM
                or config["construction_status"]
                not in {
                    "ORIGINAL_PRE_RESERVATION",
                    "RECOVERED_AFTER_ATOMIC_CONFIG_ABSENCE",
                }
                or config["case_id"] != case_id
                or config["attempt_number"] != attempt_number
                or config["seed"] != case["seed"]
                or config["cube_literals"] != case["cube_literals"]
                or config["case_cnf_sha256"] != case["cnf_sha256"]
                or config["run_manifest_sha256"] != manifest_sha256
                or config["partition_sha256"] != partition_sha256
                or config["solver_command"] != commands["solver"]
                or config["raw_forward_command"] != commands["raw_forward"]
                or config["normalizer_command"] != commands["normalizer"]
                or config["normalized_forward_command"]
                != commands["normalized_forward"]
                or config["lrat_conversion_command"] != commands["lrat_conversion"]
                or config["lrat_check_command"] != commands["lrat_check"]
                or config_hashes.get(key) != config_hash
            ):
                raise AuditError(
                    f"case {case_id} attempt {attempt_number} configuration differs"
                )
            created = _exact_int(
                config["created_unix_ns"],
                f"case {case_id} attempt creation time",
                minimum=1,
            )
            instance = _stable_file_bytes(
                attempt_directory / "instance.cnf",
                f"case {case_id} materialized CNF",
                maximum_bytes=max(len(expected_leaf), 1),
            )
            if instance != expected_leaf:
                raise AuditError(
                    f"case {case_id} materialized CNF is not its reconstructed leaf"
                )

            outcome_path = attempt_directory / "outcome.json"
            is_active = state["active_attempt"] == attempt_number
            if is_active:
                if attempt_number != attempt_count:
                    raise AuditError(f"case {case_id} nonlatest attempt is active")
                if outcome_path.exists() or outcome_path.is_symlink():
                    raise AuditError(
                        f"case {case_id} active attempt already has an outcome"
                    )
                continue
            outcome_value, _, outcome_hash = _load_canonical_json(
                outcome_path,
                f"case {case_id} attempt {attempt_number} outcome",
            )
            seen_outcomes.add(key)
            outcome = _exact_keys(
                outcome_value,
                OUTCOME_KEYS,
                f"case {case_id} attempt outcome",
            )
            _exact_int(
                outcome["schema_version"],
                f"case {case_id} outcome schema version",
                minimum=ATTEMPT_OUTCOME_SCHEMA_VERSION,
                maximum=ATTEMPT_OUTCOME_SCHEMA_VERSION,
            )
            _exact_int(
                outcome["attempt_number"],
                f"case {case_id} outcome attempt number",
                minimum=attempt_number,
                maximum=attempt_number,
            )
            status = outcome["status"]
            if status == "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION":
                raise SatLeafPresentError(
                    f"SAT leaf {case_id} attempt {attempt_number} is never aggregated"
                )
            if status not in RETRYABLE_OUTCOMES | {LEAF_UNSAT}:
                raise AuditError(f"case {case_id} outcome status is unknown")
            if (
                config["construction_status"]
                == "RECOVERED_AFTER_ATOMIC_CONFIG_ABSENCE"
                and status != "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM"
            ):
                raise AuditError(
                    f"case {case_id} recovered config has a decisive outcome"
                )
            expected_math_claim = (
                "LEAF_UNSAT_AFTER_LRAT_REPLAY" if status == LEAF_UNSAT else "NONE"
            )
            finished = _exact_int(
                outcome["finished_unix_ns"],
                f"case {case_id} attempt finish time",
                minimum=created,
            )
            if (
                outcome["schema"] != ATTEMPT_OUTCOME_SCHEMA
                or outcome["schema_version"] != ATTEMPT_OUTCOME_SCHEMA_VERSION
                or outcome["proof_pipeline"] != PROOF_PIPELINE_ID
                or outcome["case_id"] != case_id
                or outcome["attempt_number"] != attempt_number
                or outcome["mathematical_claim"] != expected_math_claim
                or outcome["aggregate_claim"] != "NONE"
                or not isinstance(outcome["details"], dict)
                or outcome_hashes.get(key) != outcome_hash
                or finished < created
            ):
                raise AuditError(
                    f"case {case_id} attempt {attempt_number} outcome differs"
                )
            inventory = _validate_inventory(
                outcome["artifact_inventory"], attempt_directory
            )
            if status == LEAF_UNSAT:
                terminal = _validate_leaf_certificate(
                    certificate_path=attempt_directory / "certificate.json",
                    outcome=outcome,
                    inventory=inventory,
                    config=config,
                    manifest=manifest,
                    case=case,
                    attempt_directory=attempt_directory,
                    scope=scope,
                )
                if (
                    attempt_number == attempt_count
                    and state["status"] == LEAF_UNSAT
                ):
                    terminals.append(terminal)
            last_status = status
            last_hash = outcome_hash
        state_status = state["status"]
        if state_status == "PENDING":
            valid_state = (
                attempt_count == 0
                and last_status is None
                and last_hash is None
                and state["last_completed_outcome_sha256"] is None
            )
        elif state_status == "RUNNING_UNFINISHED_NONCLAIM":
            valid_state = (
                state["active_attempt"] == attempt_count
                and last_hash == state["last_completed_outcome_sha256"]
            )
        elif state_status == "RETRYABLE_NONCLAIM":
            valid_state = (
                attempt_count >= 1
                and state["active_attempt"] is None
                and last_hash == state["last_completed_outcome_sha256"]
            )
        elif state_status == LEAF_UNSAT:
            valid_state = (
                attempt_count >= 1
                and state["active_attempt"] is None
                and last_status == LEAF_UNSAT
                and last_hash == state["last_completed_outcome_sha256"]
            )
        else:
            valid_state = False
        if not valid_state:
            raise AuditError(f"case {case_id} latest outcome/state differs")

    if seen_attempts != set(config_hashes) or seen_outcomes != set(outcome_hashes):
        raise AuditError("checkpoint bindings and attempt directory set differ")
    return tuple(terminals), historical_count


class _ReadLock:
    def __init__(self, run_directory: Path) -> None:
        self.path = run_directory / "run.lock"
        self.descriptor: int | None = None

    def __enter__(self) -> "_ReadLock":
        descriptor, _ = _open_regular_single_link(self.path, "run lock")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except (OSError, BlockingIOError) as error:
            os.close(descriptor)
            raise AuditError("production run is currently being mutated") from error
        self.descriptor = descriptor
        return self

    def __exit__(self, *_: object) -> None:
        if self.descriptor is None:
            raise AssertionError("read lock exited without a descriptor")
        fcntl.flock(self.descriptor, fcntl.LOCK_UN)
        os.close(self.descriptor)
        self.descriptor = None


class _CampaignHeavyChildLock:
    """Independent implementation of the campaign-wide heavy-job lock."""

    def __init__(self, root: Path) -> None:
        root_digest = sha256(str(root.resolve()).encode("utf-8")).hexdigest()[:20]
        self.path = (
            Path(tempfile.gettempdir()).resolve()
            / f"{HEAVY_CHILD_LOCK_NAME}-{root_digest}.lock"
        )
        self.descriptor: int | None = None

    def __enter__(self) -> "_CampaignHeavyChildLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        _assert_no_symlink_components(self.path.parent)
        if os.path.lexists(self.path):
            information = os.lstat(self.path)
            if (
                stat.S_ISLNK(information.st_mode)
                or not stat.S_ISREG(information.st_mode)
                or information.st_nlink != 1
            ):
                raise AuditError("campaign heavy-child lock is malformed")
        flags = os.O_CREAT | os.O_RDWR
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(self.path, flags, 0o600)
        except OSError as error:
            raise AuditError("campaign heavy-child lock cannot be opened") from error
        information = os.fstat(descriptor)
        if (
            not stat.S_ISREG(information.st_mode)
            or information.st_nlink != 1
        ):
            os.close(descriptor)
            raise AuditError("campaign heavy-child lock is not a regular file")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(descriptor)
            raise ResourceGateError(
                "another campaign solver/checker child is active"
            ) from error
        self.descriptor = descriptor
        return self

    def __exit__(self, *_: object) -> None:
        if self.descriptor is None:
            raise AssertionError("heavy-child lock exited without acquisition")
        fcntl.flock(self.descriptor, fcntl.LOCK_UN)
        os.close(self.descriptor)
        self.descriptor = None


class _ReplayDirectoryLock:
    """Serialize writers to one external resumable replay ledger."""

    def __init__(self, replay_directory: Path) -> None:
        self.path = replay_directory / REPLAY_LOCK_NAME
        self.descriptor: int | None = None

    def __enter__(self) -> "_ReplayDirectoryLock":
        _assert_no_symlink_components(self.path.parent)
        if os.path.lexists(self.path):
            information = os.lstat(self.path)
            if (
                stat.S_ISLNK(information.st_mode)
                or not stat.S_ISREG(information.st_mode)
                or information.st_nlink != 1
            ):
                raise AuditError("replay-directory lock is malformed")
        flags = os.O_CREAT | os.O_RDWR
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(self.path, flags, 0o600)
        except OSError as error:
            raise AuditError("replay-directory lock cannot be opened") from error
        information = os.fstat(descriptor)
        if (
            not stat.S_ISREG(information.st_mode)
            or information.st_nlink != 1
        ):
            os.close(descriptor)
            raise AuditError("replay-directory lock is not a regular file")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(descriptor)
            raise ResourceGateError(
                "another aggregate auditor owns the replay ledger"
            ) from error
        self.descriptor = descriptor
        return self

    def __exit__(self, *_: object) -> None:
        if self.descriptor is None:
            raise AssertionError("replay-directory lock exited without acquisition")
        fcntl.flock(self.descriptor, fcntl.LOCK_UN)
        os.close(self.descriptor)
        self.descriptor = None


def _validate_run_root_layout(run_directory: Path) -> None:
    expected = {
        RUN_MANIFEST_NAME,
        PARTITION_NAME,
        PARENT_NAME,
        PARENT_MANIFEST_NAME,
        CHECKPOINT_DIR_NAME,
        CASE_DIR_NAME,
    }
    observed = {path.name for path in run_directory.iterdir()}
    if "run.lock" in observed:
        expected.add("run.lock")
    if observed != expected:
        raise AuditError("frozen run-root entry set differs")
    for name in (CHECKPOINT_DIR_NAME, CASE_DIR_NAME):
        path = run_directory / name
        information = os.lstat(path)
        if stat.S_ISLNK(information.st_mode) or not stat.S_ISDIR(
            information.st_mode
        ):
            raise AuditError(f"frozen run-root directory {name!r} is malformed")


def _static_audit_unlocked(
    run_directory: Path,
    scope: FrozenScope,
) -> StaticAudit:
    _validate_run_root_layout(run_directory)
    manifest, manifest_hash, lrat_check = _validate_run_manifest(
        run_directory, scope
    )
    parent, parent_hash = _validate_parent(run_directory, manifest, scope)
    partition, partition_hash, leaves, coverage_hash = _validate_partition(
        run_directory,
        manifest,
        parent,
        scope,
    )
    latest, latest_hash, config_hashes, outcome_hashes, checkpoint_count = (
        _validate_checkpoints(
            run_directory,
            run_manifest_sha256=manifest_hash,
            partition_sha256=partition_hash,
            case_ids=[case["case_id"] for case in leaves],
            base_seed=manifest["base_seed"],
        )
    )
    terminals, historic_count = _validate_attempts(
        run_directory,
        manifest=manifest,
        manifest_sha256=manifest_hash,
        partition_sha256=partition_hash,
        parent=parent,
        cases=leaves,
        latest=latest,
        config_hashes=config_hashes,
        outcome_hashes=outcome_hashes,
        scope=scope,
    )
    return StaticAudit(
        run_directory=run_directory,
        run_manifest=manifest,
        run_manifest_sha256=manifest_hash,
        partition=partition,
        partition_sha256=partition_hash,
        parent=parent,
        parent_sha256=parent_hash,
        latest_checkpoint=latest,
        latest_checkpoint_sha256=latest_hash,
        reconstructed_leaves=leaves,
        terminal_attempts=terminals,
        coverage_rows_sha256=coverage_hash,
        checkpoint_count=checkpoint_count,
        historical_attempt_count=historic_count,
        lrat_check_path=lrat_check,
        lrat_check_sha256=scope.lrat_check_sha256,
    )


def static_audit(
    run_directory: Path,
    *,
    scope: FrozenScope = PRODUCTION_SCOPE,
) -> StaticAudit:
    """Perform the complete immutable audit without starting ``lrat-check``."""

    scope = _validate_scope(scope)
    _assert_no_symlink_components(run_directory)
    resolved = run_directory.resolve(strict=True)
    if not resolved.is_dir():
        raise AuditError("run directory is not a directory")
    lock_path = resolved / "run.lock"
    if os.path.lexists(lock_path):
        with _ReadLock(resolved):
            return _static_audit_unlocked(resolved, scope)
    static = _static_audit_unlocked(resolved, scope)
    if (
        os.path.lexists(lock_path)
        or static.latest_checkpoint["sequence"] != 0
        or static.historical_attempt_count != 0
    ):
        raise AuditError("lock-free pristine run changed during audit")
    return static


def _available_memory_bytes() -> int:
    if Path("/proc/meminfo").is_file():
        try:
            for line in Path("/proc/meminfo").read_text("ascii").splitlines():
                if line.startswith("MemAvailable:"):
                    fields = line.split()
                    if len(fields) == 3 and fields[1].isdigit() and fields[2] == "kB":
                        return int(fields[1]) << 10
        except (OSError, UnicodeError):
            pass
    try:
        completed = subprocess.run(
            ("/usr/bin/vm_stat",),
            env={},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
            timeout=5,
        )
        text = completed.stdout.decode("ascii", "strict")
        page_match = re.search(r"page size of ([0-9]+) bytes", text)
        if completed.returncode == 0 and not completed.stderr and page_match:
            page_size = int(page_match.group(1))
            counts: dict[str, int] = {}
            for line in text.splitlines():
                match = re.fullmatch(r"([^:]+):\s*([0-9]+)\.", line.strip())
                if match:
                    counts[match.group(1)] = int(match.group(2))
            pages = sum(
                counts.get(name, 0)
                for name in (
                    "Pages free",
                    "Pages inactive",
                    "Pages speculative",
                    "Pages purgeable",
                )
            )
            if pages > 0:
                return pages * page_size
    except (OSError, subprocess.TimeoutExpired, UnicodeError):
        pass
    raise ResourceGateError("available memory cannot be measured")


def _physical_memory_bytes() -> int:
    if Path("/proc/meminfo").is_file():
        try:
            for line in Path("/proc/meminfo").read_text("ascii").splitlines():
                if line.startswith("MemTotal:"):
                    fields = line.split()
                    if (
                        len(fields) == 3
                        and fields[1].isdigit()
                        and fields[2] == "kB"
                    ):
                        return int(fields[1]) << 10
        except (OSError, UnicodeError):
            pass
    try:
        completed = subprocess.run(
            ("/usr/sbin/sysctl", "-n", "hw.memsize"),
            env={},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
            timeout=5,
        )
        stripped = completed.stdout.strip()
        if (
            completed.returncode == 0
            and not completed.stderr
            and stripped.isdigit()
            and int(stripped) > 0
        ):
            return int(stripped)
    except (OSError, subprocess.TimeoutExpired):
        pass
    raise ResourceGateError("physical memory cannot be measured")


def _resource_gate(
    run_directory: Path,
    policy: AuditPolicy,
    *,
    additional_disk_bytes: int = 0,
) -> dict[str, Any]:
    if type(additional_disk_bytes) is not int or additional_disk_bytes < 0:
        raise AuditError("additional replay disk requirement is malformed")
    load_one = os.getloadavg()[0]
    available = _available_memory_bytes()
    physical = _physical_memory_bytes()
    free_disk = os.statvfs(run_directory)
    free_disk_bytes = free_disk.f_bavail * free_disk.f_frsize
    required_memory = (policy.memory_mib + policy.memory_reserve_mib) << 20
    required_disk = (
        (policy.file_limit_mib + policy.disk_reserve_mib) << 20
    ) + additional_disk_bytes
    checks = {
        "load": load_one <= float(policy.load_max),
        "memory": available >= required_memory,
        "responsive_memory": (policy.memory_mib << 20) <= physical * 0.75,
        "disk": free_disk_bytes >= required_disk,
    }
    if not all(checks.values()):
        raise ResourceGateError(
            "fresh LRAT replay resource gate failed: "
            + ", ".join(name for name, passed in checks.items() if not passed)
        )
    return {
        "load_average_one_minute": load_one,
        "available_memory_bytes": available,
        "physical_memory_bytes": physical,
        "free_disk_bytes": free_disk_bytes,
        "required_memory_bytes": required_memory,
        "required_free_disk_bytes": required_disk,
        "checks": checks,
    }


def _resident_bytes(pid: int) -> int | None:
    try:
        completed = subprocess.run(
            ("/bin/ps", "-o", "rss=", "-p", str(pid)),
            env={},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
            timeout=2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0 or completed.stderr:
        return None
    stripped = completed.stdout.strip()
    return int(stripped) << 10 if stripped.isdigit() else None


def _kill_process_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def _checker_child_setup(wall_seconds: int, file_bytes: int) -> None:
    os.setsid()
    resource.setrlimit(resource.RLIMIT_CPU, (wall_seconds + 1, wall_seconds + 1))
    resource.setrlimit(resource.RLIMIT_FSIZE, (file_bytes, file_bytes))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def _policy_record(policy: AuditPolicy) -> dict[str, Any]:
    return {
        "wall_seconds": policy.wall_seconds,
        "memory_mib": policy.memory_mib,
        "file_limit_mib": policy.file_limit_mib,
        "load_max": float(policy.load_max),
        "memory_reserve_mib": policy.memory_reserve_mib,
        "disk_reserve_mib": policy.disk_reserve_mib,
        "enforce_live_resource_gates": policy.enforce_live_resource_gates,
    }


def _verifier_runtime_sources() -> tuple[list[dict[str, Any]], str]:
    root = campaign_root()
    records: list[dict[str, Any]] = []
    for relative in VERIFIER_RUNTIME_SOURCE_PATHS:
        path = root / relative
        digest, size = _stable_file_hash(
            path, f"aggregate verifier runtime source {relative}"
        )
        records.append(
            {
                "path": relative,
                "sha256": digest,
                "size_bytes": size,
            }
        )
    return records, _source_set_digest(records)


def _prepare_replay_directory(
    requested: Path,
    run_directory: Path,
    *,
    production: bool,
) -> Path:
    absolute = requested if requested.is_absolute() else Path.cwd() / requested
    absolute = absolute.absolute()
    if os.path.lexists(absolute):
        _assert_no_symlink_components(absolute)
        information = os.lstat(absolute)
        if not stat.S_ISDIR(information.st_mode):
            raise AuditError("replay path is not a directory")
    else:
        _assert_no_symlink_components(absolute.parent)
        try:
            absolute.mkdir(mode=0o700)
        except OSError as error:
            raise AuditError("external replay directory cannot be created") from error
        _fsync_directory(absolute.parent, "external replay directory")
    resolved = absolute.resolve(strict=True)
    information = os.lstat(resolved)
    if (
        not stat.S_ISDIR(information.st_mode)
        or (production and stat.S_IMODE(information.st_mode) & 0o077)
    ):
        raise AuditError(
            "production replay directory must be a private real directory"
        )
    if resolved == run_directory or run_directory in resolved.parents:
        raise AuditError("replay ledger must be external to the frozen run")
    return resolved


def _remove_abandoned_pending(path: Path, role: str) -> None:
    if not os.path.lexists(path):
        return
    information = os.lstat(path)
    if (
        stat.S_ISLNK(information.st_mode)
        or not stat.S_ISREG(information.st_mode)
        or information.st_nlink != 1
    ):
        raise AuditError(f"{role} pending file is malformed")
    try:
        path.unlink()
    except OSError as error:
        raise AuditError(f"{role} pending file cannot be removed") from error
    _fsync_directory(path.parent, role)


def _publish_canonical_json_once(
    path: Path,
    value: object,
    role: str,
) -> tuple[str, int]:
    if os.path.lexists(path):
        raise AuditError(f"{role} already exists")
    pending = path.parent / f".{path.name}.pending"
    _remove_abandoned_pending(pending, role)
    raw = canonical_json_bytes(value)
    _write_exclusive_bytes(pending, raw, f"{role} pending record")
    if os.path.lexists(path):
        raise AuditError(f"{role} appeared during publication")
    try:
        os.replace(pending, path)
    except OSError as error:
        raise AuditError(f"{role} cannot be published atomically") from error
    _fsync_directory(path.parent, role)
    digest, size = _stable_file_hash(path, role)
    if digest != sha256(raw).hexdigest() or size != len(raw):
        raise AuditError(f"{role} differs after publication")
    return digest, size


def _replay_manifest_fields(
    static: StaticAudit,
    scope: FrozenScope,
    sources: Sequence[Mapping[str, Any]],
    source_set_sha256: str,
) -> dict[str, Any]:
    return {
        "schema": REPLAY_MANIFEST_SCHEMA,
        "schema_version": REPLAY_SCHEMA_VERSION,
        "verifier": VERIFIER,
        "scope_id": scope.scope_id,
        "production_scope": scope.production,
        "run_directory": str(static.run_directory),
        "run_manifest_sha256": static.run_manifest_sha256,
        "partition_sha256": static.partition_sha256,
        "parent_cnf_sha256": static.parent_sha256,
        "coverage_rows_sha256": static.coverage_rows_sha256,
        "lrat_check_sha256": static.lrat_check_sha256,
        "verifier_runtime_sources": list(sources),
        "verifier_runtime_source_set_sha256": source_set_sha256,
    }


def _load_or_create_replay_manifest(
    replay_directory: Path,
    static: StaticAudit,
    scope: FrozenScope,
) -> tuple[dict[str, Any], str, list[dict[str, Any]], str]:
    sources, source_set_sha256 = _verifier_runtime_sources()
    expected = _replay_manifest_fields(
        static, scope, sources, source_set_sha256
    )
    path = replay_directory / REPLAY_MANIFEST_NAME
    pending = replay_directory / f".{REPLAY_MANIFEST_NAME}.pending"
    if os.path.lexists(path):
        if os.path.lexists(pending):
            _remove_abandoned_pending(pending, "replay manifest")
        value, _, digest = _load_canonical_json(path, "replay manifest")
        manifest = _exact_keys(value, REPLAY_MANIFEST_KEYS, "replay manifest")
        _exact_int(
            manifest["schema_version"],
            "replay-manifest schema version",
            minimum=REPLAY_SCHEMA_VERSION,
            maximum=REPLAY_SCHEMA_VERSION,
        )
        created = _exact_int(
            manifest["created_unix_ns"],
            "replay manifest creation time",
            minimum=1,
        )
        del created
        if manifest["production_scope"] is not scope.production:
            raise AuditError("replay manifest production-scope flag differs")
        raw_sources = manifest["verifier_runtime_sources"]
        if not isinstance(raw_sources, list):
            raise AuditError("replay manifest source vector is malformed")
        for index, raw_source in enumerate(raw_sources):
            source = _exact_keys(
                raw_source,
                REPLAY_SOURCE_KEYS,
                f"replay manifest source {index}",
            )
            _exact_int(
                source["size_bytes"],
                f"replay manifest source {index} size",
            )
            _hex_digest(
                source["sha256"],
                f"replay manifest source {index} digest",
            )
        recorded_source_set = _hex_digest(
            manifest["verifier_runtime_source_set_sha256"],
            "replay manifest verifier source-set digest",
        )
        if recorded_source_set != _source_set_digest(raw_sources):
            raise AuditError("replay manifest verifier source set is inconsistent")
        observed = dict(manifest)
        del observed["created_unix_ns"]
        observed_sources = observed.pop("verifier_runtime_sources")
        observed_source_set = observed.pop(
            "verifier_runtime_source_set_sha256"
        )
        expected_context = dict(expected)
        del expected_context["verifier_runtime_sources"]
        del expected_context["verifier_runtime_source_set_sha256"]
        accepted_historical = {
            historical_digest: [
                {
                    "path": relative,
                    "sha256": digest_value,
                    "size_bytes": size,
                }
                for relative, digest_value, size in vector
            ]
            for historical_digest, vector in (
                ACCEPTED_HISTORICAL_VERIFIER_SOURCE_VECTORS
            )
        }
        source_vector_is_current = (
            observed_source_set == source_set_sha256
            and observed_sources == sources
        )
        source_vector_is_accepted_historical = (
            observed_source_set in accepted_historical
            and observed_sources == accepted_historical[observed_source_set]
        )
        if (
            observed != expected_context
            or not (
                source_vector_is_current
                or source_vector_is_accepted_historical
            )
        ):
            raise AuditError(
                "replay manifest context or verifier source binding differs"
            )
    else:
        manifest = {**expected, "created_unix_ns": time.time_ns()}
        digest, _ = _publish_canonical_json_once(
            path, manifest, "replay manifest"
        )
    return manifest, digest, sources, source_set_sha256


def _validate_replay_directory_entries(
    replay_directory: Path,
    terminal_case_ids: set[str],
) -> None:
    allowed_fixed = {REPLAY_MANIFEST_NAME, REPLAY_LOCK_NAME}
    for path in replay_directory.iterdir():
        if path.name in allowed_fixed:
            continue
        match = REPLAY_RECORD_RE.fullmatch(path.name)
        if match is None or match.group(1) not in terminal_case_ids:
            raise AuditError(f"unexpected replay-ledger entry {path.name!r}")
        descriptor, _ = _open_regular_single_link(path, "replay record")
        os.close(descriptor)


def _replay_context(
    static: StaticAudit,
    terminal: Mapping[str, Any],
    policy: AuditPolicy,
    replay_manifest_sha256: str,
) -> dict[str, Any]:
    return {
        "replay_manifest_sha256": replay_manifest_sha256,
        "run_manifest_sha256": static.run_manifest_sha256,
        "partition_sha256": static.partition_sha256,
        "parent_cnf_sha256": static.parent_sha256,
        "coverage_rows_sha256": static.coverage_rows_sha256,
        "case_id": terminal["case_id"],
        "cube_literals": list(terminal["cube_literals"]),
        "certificate_sha256": terminal["certificate_sha256"],
        "cnf_sha256": terminal["cnf_sha256"],
        "cnf_size_bytes": next(
            case["cnf_size_bytes"]
            for case in static.reconstructed_leaves
            if case["case_id"] == terminal["case_id"]
        ),
        "lrat_sha256": terminal["lrat_sha256"],
        "lrat_size_bytes": terminal["lrat_size_bytes"],
        "lrat_check_sha256": static.lrat_check_sha256,
        "policy": _policy_record(policy),
    }


def _validate_recorded_replay_context(
    value: object,
    expected: Mapping[str, Any],
    role: str,
) -> dict[str, Any]:
    context = _exact_keys(value, REPLAY_CONTEXT_KEYS, role)
    for key in ("cnf_size_bytes", "lrat_size_bytes"):
        _exact_int(
            context[key],
            f"{role} {key}",
            minimum=expected[key],
            maximum=expected[key],
        )
    if (
        not isinstance(context["cube_literals"], list)
        or any(type(literal) is not int for literal in context["cube_literals"])
    ):
        raise AuditError(f"{role} cube literals are malformed")
    recorded_policy = _exact_keys(
        context["policy"], REPLAY_POLICY_KEYS, f"{role} policy"
    )
    expected_policy = expected["policy"]
    if not isinstance(expected_policy, dict):
        raise AssertionError("expected replay policy invariant failed")
    for key in (
        "wall_seconds",
        "memory_mib",
        "file_limit_mib",
        "memory_reserve_mib",
        "disk_reserve_mib",
    ):
        _exact_int(
            recorded_policy[key],
            f"{role} policy {key}",
            minimum=expected_policy[key],
            maximum=expected_policy[key],
        )
    if (
        type(recorded_policy["load_max"]) not in (int, float)
        or not math.isfinite(float(recorded_policy["load_max"]))
        or type(recorded_policy["enforce_live_resource_gates"]) is not bool
        or context != expected
    ):
        raise AuditError(f"{role} differs")
    return context


def _decode_recorded_output(
    encoded: object,
    expected_hash: object,
    expected_size: object,
    role: str,
) -> bytes:
    if not isinstance(encoded, str):
        raise AuditError(f"{role} base64 is not a string")
    size = _exact_int(
        expected_size,
        f"{role} recorded size",
        maximum=MAX_REPLAY_OUTPUT_BYTES,
    )
    _hex_digest(expected_hash, f"{role} recorded digest")
    try:
        raw = base64.b64decode(encoded.encode("ascii"), validate=True)
    except (UnicodeEncodeError, binascii.Error) as error:
        raise AuditError(f"{role} base64 is malformed") from error
    if (
        base64.b64encode(raw).decode("ascii") != encoded
        or expected_hash != sha256(raw).hexdigest()
        or size != len(raw)
        or len(raw) > MAX_REPLAY_OUTPUT_BYTES
    ):
        raise AuditError(f"{role} recorded output binding differs")
    return raw


def _validate_replay_resource_gate(
    value: object,
    policy: AuditPolicy,
    role: str,
) -> dict[str, Any]:
    if not policy.enforce_live_resource_gates:
        if value != {"checks": {"live_resource_gates_disabled_for_test": True}}:
            raise AuditError(f"{role} disabled resource-gate record differs")
        return dict(value)
    gate = _exact_keys(
        value,
        {
            "load_average_one_minute",
            "available_memory_bytes",
            "physical_memory_bytes",
            "free_disk_bytes",
            "required_memory_bytes",
            "required_free_disk_bytes",
            "checks",
        },
        role,
    )
    for key in (
        "load_average_one_minute",
        "available_memory_bytes",
        "physical_memory_bytes",
        "free_disk_bytes",
        "required_memory_bytes",
        "required_free_disk_bytes",
    ):
        number = gate[key]
        if (
            type(number) not in (int, float)
            or not math.isfinite(float(number))
            or number < 0
        ):
            raise AuditError(f"{role} numeric field {key!r} differs")
    checks = _exact_keys(
        gate["checks"],
        {"load", "memory", "responsive_memory", "disk"},
        f"{role} checks",
    )
    if any(value is not True for value in checks.values()):
        raise AuditError(f"{role} did not record a clean resource-gate pass")
    if (
        gate["load_average_one_minute"] > float(policy.load_max)
        or gate["available_memory_bytes"] < gate["required_memory_bytes"]
        or (policy.memory_mib << 20)
        > gate["physical_memory_bytes"] * 0.75
        or gate["free_disk_bytes"] < gate["required_free_disk_bytes"]
        or gate["required_memory_bytes"]
        != (policy.memory_mib + policy.memory_reserve_mib) << 20
    ):
        raise AuditError(f"{role} resource-gate arithmetic differs")
    return gate


def _validate_replay_result(
    value: object,
    context: Mapping[str, Any],
    policy: AuditPolicy,
    role: str,
) -> dict[str, Any]:
    result = _exact_keys(value, REPLAY_RESULT_KEYS, role)
    _exact_int(
        result["exit_code"],
        f"{role} exit code",
        minimum=0,
        maximum=0,
    )
    logical_command = [
        "PRIVATE_COPY_OF_PINNED_LRAT_CHECK",
        "INDEPENDENTLY_RECONSTRUCTED_LEAF_CNF",
        "PRIVATE_COPY_OF_BOUND_LRAT",
    ]
    expected_hashes = {
        "checker_sha256_before": context["lrat_check_sha256"],
        "checker_sha256_private": context["lrat_check_sha256"],
        "checker_sha256_after": context["lrat_check_sha256"],
        "cnf_sha256_before": context["cnf_sha256"],
        "cnf_sha256_reconstructed": context["cnf_sha256"],
        "cnf_sha256_private": context["cnf_sha256"],
        "cnf_sha256_after": context["cnf_sha256"],
        "lrat_sha256_before": context["lrat_sha256"],
        "lrat_sha256_private": context["lrat_sha256"],
        "lrat_sha256_after": context["lrat_sha256"],
    }
    if (
        result["case_id"] != context["case_id"]
        or result["logical_command"] != logical_command
        or result["command_sha256"] != _command_sha256(logical_command)
        or result["execution_isolation"]
        != (
            "private-checker-copy+independent-leaf-reconstruction+"
            "private-lrat-copy+empty-environment"
        )
        or any(result[key] != digest for key, digest in expected_hashes.items())
        or result["exit_code"] != 0
        or result["timed_out"] is not False
        or result["memory_limit_exceeded"] is not False
        or result["rss_monitoring_failed"] is not False
    ):
        raise AuditError(f"{role} decisive replay fields differ")
    _exact_int(
        result["rss_probe_failure_count"],
        f"{role} RSS probe failure count",
    )
    for key in ("peak_polled_resident_set_size_mib", "wall_seconds"):
        number = result[key]
        if (
            type(number) not in (int, float)
            or not math.isfinite(float(number))
            or number < 0
        ):
            raise AuditError(f"{role} metric {key!r} differs")
    started = _exact_int(
        result["started_unix_ns"], f"{role} start time", minimum=1
    )
    finished = _exact_int(
        result["finished_unix_ns"],
        f"{role} finish time",
        minimum=started,
    )
    del finished
    if result["wall_seconds"] > policy.wall_seconds + 5:
        raise AuditError(f"{role} exceeds its replay wall-time envelope")
    stdout = _decode_recorded_output(
        result["stdout_base64"],
        result["stdout_sha256"],
        result["stdout_size_bytes"],
        f"{role} stdout",
    )
    stderr = _decode_recorded_output(
        result["stderr_base64"],
        result["stderr_sha256"],
        result["stderr_size_bytes"],
        f"{role} stderr",
    )
    _strict_lrat_success(stdout, stderr, role)
    _validate_replay_resource_gate(result["resource_gate"], policy, role)
    return result


def _fresh_replay_one(
    static: StaticAudit,
    terminal: Mapping[str, Any],
    policy: AuditPolicy,
    scope: FrozenScope,
) -> dict[str, Any]:
    checker_hash_before, checker_size = _stable_file_hash(
        static.lrat_check_path, "fresh lrat-check executable"
    )
    cnf_path = Path(terminal["cnf_path"])
    lrat_path = Path(terminal["lrat_path"])
    cnf_hash_before, cnf_size = _stable_file_hash(cnf_path, "fresh replay CNF")
    lrat_hash_before, lrat_size = _stable_file_hash(
        lrat_path, "fresh replay LRAT"
    )
    reconstructed = _leaf_bytes(
        static.parent,
        terminal["cube_literals"],
        scope,
    )
    reconstructed_hash = sha256(reconstructed).hexdigest()
    if (
        checker_hash_before != static.lrat_check_sha256
        or cnf_hash_before != terminal["cnf_sha256"]
        or cnf_size != len(reconstructed)
        or cnf_hash_before != reconstructed_hash
        or lrat_hash_before != terminal["lrat_sha256"]
        or lrat_size != terminal["lrat_size_bytes"]
    ):
        raise AuditError(f"case {terminal['case_id']} changed before fresh replay")

    logical_command = [
        "PRIVATE_COPY_OF_PINNED_LRAT_CHECK",
        "INDEPENDENTLY_RECONSTRUCTED_LEAF_CNF",
        "PRIVATE_COPY_OF_BOUND_LRAT",
    ]
    file_bytes = min(policy.file_limit_mib << 20, MAX_REPLAY_OUTPUT_BYTES)
    additional_disk = (
        checker_size + len(reconstructed) + lrat_size + 2 * file_bytes
    )
    with _CampaignHeavyChildLock(Path(static.run_manifest["campaign_root"])):
        resource_report = (
            _resource_gate(
                static.run_directory,
                policy,
                additional_disk_bytes=additional_disk,
            )
            if policy.enforce_live_resource_gates
            else {"checks": {"live_resource_gates_disabled_for_test": True}}
        )
        with tempfile.TemporaryDirectory(
            prefix="gamma-theta-k4-aggregate-"
        ) as raw_tmp:
            temporary = Path(raw_tmp).resolve()
            checker_private = temporary / "lrat-check"
            cnf_private = temporary / "leaf.cnf"
            lrat_private = temporary / "proof.lrat"
            checker_private_hash, checker_private_size = _copy_stable_file(
                static.lrat_check_path,
                checker_private,
                "fresh lrat-check executable",
                executable=True,
            )
            cnf_private_hash, cnf_private_size = _write_exclusive_bytes(
                cnf_private,
                reconstructed,
                "independently reconstructed replay CNF",
            )
            lrat_private_hash, lrat_private_size = _copy_stable_file(
                lrat_path,
                lrat_private,
                "fresh replay LRAT",
            )
            if (
                checker_private_hash != checker_hash_before
                or checker_private_size != checker_size
                or cnf_private_hash != reconstructed_hash
                or cnf_private_size != len(reconstructed)
                or lrat_private_hash != lrat_hash_before
                or lrat_private_size != lrat_size
            ):
                raise AuditError(
                    f"case {terminal['case_id']} private replay copy differs"
                )
            command = [
                str(checker_private),
                str(cnf_private),
                str(lrat_private),
            ]
            started_ns = time.time_ns()
            started = time.monotonic()
            timed_out = False
            memory_exceeded = False
            rss_monitoring_failed = False
            rss_probe_failures = 0
            consecutive_rss_probe_failures = 0
            peak_rss = 0
            stdout_path = temporary / "stdout"
            stderr_path = temporary / "stderr"
            with stdout_path.open("xb") as stdout_handle, stderr_path.open(
                "xb"
            ) as stderr_handle:
                try:
                    process = subprocess.Popen(
                        command,
                        cwd=temporary,
                        env={},
                        stdin=subprocess.DEVNULL,
                        stdout=stdout_handle,
                        stderr=stderr_handle,
                        close_fds=True,
                        preexec_fn=lambda: _checker_child_setup(
                            policy.wall_seconds, file_bytes
                        ),
                    )
                except OSError as error:
                    raise AuditError("fresh lrat-check could not start") from error
                deadline = started + policy.wall_seconds
                while process.poll() is None:
                    resident = _resident_bytes(process.pid)
                    if resident is None:
                        rss_probe_failures += 1
                        consecutive_rss_probe_failures += 1
                        if consecutive_rss_probe_failures >= 3:
                            rss_monitoring_failed = True
                            _kill_process_group(process)
                            break
                    else:
                        consecutive_rss_probe_failures = 0
                        peak_rss = max(peak_rss, resident)
                        if resident > (policy.memory_mib << 20):
                            memory_exceeded = True
                            _kill_process_group(process)
                            break
                    if time.monotonic() >= deadline:
                        timed_out = True
                        _kill_process_group(process)
                        break
                    time.sleep(0.05)
                try:
                    exit_code = process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    _kill_process_group(process)
                    exit_code = process.wait(timeout=5)
                stdout_handle.flush()
                stderr_handle.flush()
            stdout = _stable_file_bytes(
                stdout_path,
                "fresh lrat-check stdout",
                maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
            )
            stderr = _stable_file_bytes(
                stderr_path,
                "fresh lrat-check stderr",
                maximum_bytes=MAX_REPLAY_OUTPUT_BYTES,
            )
            finished_ns = time.time_ns()
            elapsed = time.monotonic() - started
            if timed_out:
                raise AuditError(
                    f"case {terminal['case_id']} fresh LRAT replay timed out"
                )
            if memory_exceeded:
                raise AuditError(
                    f"case {terminal['case_id']} fresh LRAT replay exceeded memory"
                )
            if rss_monitoring_failed:
                raise AuditError(
                    f"case {terminal['case_id']} fresh LRAT RSS monitoring failed"
                )
            if exit_code != 0:
                raise AuditError(
                    f"case {terminal['case_id']} fresh lrat-check exited {exit_code}"
                )
            _strict_lrat_success(
                stdout,
                stderr,
                f"case {terminal['case_id']} fresh lrat-check",
            )
        checker_hash_after, checker_size_after = _stable_file_hash(
            static.lrat_check_path, "fresh lrat-check executable"
        )
        cnf_hash_after, cnf_size_after = _stable_file_hash(
            cnf_path, "fresh replay CNF"
        )
        lrat_hash_after, lrat_size_after = _stable_file_hash(
            lrat_path, "fresh replay LRAT"
        )
        if (
            checker_hash_after != checker_hash_before
            or checker_size_after != checker_size
            or cnf_hash_after != cnf_hash_before
            or cnf_size_after != cnf_size
            or lrat_hash_after != lrat_hash_before
            or lrat_size_after != lrat_size
        ):
            raise AuditError(
                f"case {terminal['case_id']} changed during fresh replay"
            )
    return {
        "case_id": terminal["case_id"],
        "logical_command": logical_command,
        "command_sha256": _command_sha256(logical_command),
        "execution_isolation": (
            "private-checker-copy+independent-leaf-reconstruction+"
            "private-lrat-copy+empty-environment"
        ),
        "checker_sha256_before": checker_hash_before,
        "checker_sha256_private": checker_private_hash,
        "checker_sha256_after": checker_hash_after,
        "cnf_sha256_before": cnf_hash_before,
        "cnf_sha256_reconstructed": reconstructed_hash,
        "cnf_sha256_private": cnf_private_hash,
        "cnf_sha256_after": cnf_hash_after,
        "lrat_sha256_before": lrat_hash_before,
        "lrat_sha256_private": lrat_private_hash,
        "lrat_sha256_after": lrat_hash_after,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "memory_limit_exceeded": memory_exceeded,
        "rss_monitoring_failed": rss_monitoring_failed,
        "rss_probe_failure_count": rss_probe_failures,
        "peak_polled_resident_set_size_mib": peak_rss / (1 << 20),
        "started_unix_ns": started_ns,
        "finished_unix_ns": finished_ns,
        "wall_seconds": elapsed,
        "stdout_sha256": sha256(stdout).hexdigest(),
        "stdout_size_bytes": len(stdout),
        "stdout_base64": base64.b64encode(stdout).decode("ascii"),
        "stderr_sha256": sha256(stderr).hexdigest(),
        "stderr_size_bytes": len(stderr),
        "stderr_base64": base64.b64encode(stderr).decode("ascii"),
        "resource_gate": resource_report,
    }


def _load_or_run_replay_record(
    replay_directory: Path,
    static: StaticAudit,
    terminal: Mapping[str, Any],
    policy: AuditPolicy,
    scope: FrozenScope,
    replay_manifest_sha256: str,
) -> dict[str, Any]:
    case_id = terminal["case_id"]
    path = replay_directory / f"case-{case_id}.json"
    pending = replay_directory / f".case-{case_id}.json.pending"
    context = _replay_context(
        static, terminal, policy, replay_manifest_sha256
    )
    context = _exact_keys(
        context, REPLAY_CONTEXT_KEYS, f"case {case_id} replay context"
    )
    context_sha256 = sha256(canonical_json_bytes(context)).hexdigest()
    resumed = os.path.lexists(path)
    if resumed:
        _remove_abandoned_pending(pending, f"case {case_id} replay record")
    else:
        _remove_abandoned_pending(pending, f"case {case_id} replay record")
        result = _fresh_replay_one(static, terminal, policy, scope)
        _validate_replay_result(
            result, context, policy, f"case {case_id} fresh replay"
        )
        record = {
            "schema": REPLAY_RECORD_SCHEMA,
            "schema_version": REPLAY_SCHEMA_VERSION,
            "verifier": VERIFIER,
            "status": "FRESH_LRAT_REPLAY_PASSED",
            "context": context,
            "context_sha256": context_sha256,
            "result": result,
            "written_unix_ns": time.time_ns(),
        }
        _publish_canonical_json_once(
            path, record, f"case {case_id} replay record"
        )
    value, raw, digest = _load_canonical_json(
        path, f"case {case_id} replay record"
    )
    record = _exact_keys(
        value, REPLAY_RECORD_KEYS, f"case {case_id} replay record"
    )
    _exact_int(
        record["schema_version"],
        f"case {case_id} replay-record schema version",
        minimum=REPLAY_SCHEMA_VERSION,
        maximum=REPLAY_SCHEMA_VERSION,
    )
    if (
        record["schema"] != REPLAY_RECORD_SCHEMA
        or record["schema_version"] != REPLAY_SCHEMA_VERSION
        or record["verifier"] != VERIFIER
        or record["status"] != "FRESH_LRAT_REPLAY_PASSED"
        or record["context_sha256"] != context_sha256
    ):
        raise AuditError(f"case {case_id} replay record context differs")
    _validate_recorded_replay_context(
        record["context"],
        context,
        f"case {case_id} replay record context",
    )
    result = _validate_replay_result(
        record["result"], context, policy, f"case {case_id} replay record"
    )
    written = _exact_int(
        record["written_unix_ns"],
        f"case {case_id} replay record time",
        minimum=result["finished_unix_ns"],
    )
    del written
    return {
        "case_id": case_id,
        "record_path": str(path),
        "record_sha256": digest,
        "record_size_bytes": len(raw),
        "resumed_from_external_ledger": resumed,
        "result": result,
    }


def _audit_replays_with_ledger(
    static: StaticAudit,
    scope: FrozenScope,
    policy: AuditPolicy,
    replay_directory: Path,
) -> tuple[
    tuple[dict[str, Any], ...],
    dict[str, Any],
    list[dict[str, Any]],
    str,
]:
    resolved = _prepare_replay_directory(
        replay_directory,
        static.run_directory,
        production=scope.production,
    )
    terminal_ids = {
        terminal["case_id"] for terminal in static.terminal_attempts
    }
    with _ReplayDirectoryLock(resolved):
        _remove_abandoned_pending(
            resolved / f".{REPLAY_MANIFEST_NAME}.pending",
            "replay manifest",
        )
        for case_id in terminal_ids:
            _remove_abandoned_pending(
                resolved / f".case-{case_id}.json.pending",
                f"case {case_id} replay record",
            )
        _validate_replay_directory_entries(resolved, terminal_ids)
        manifest, manifest_hash, sources, source_set_sha256 = (
            _load_or_create_replay_manifest(resolved, static, scope)
        )
        _validate_replay_directory_entries(resolved, terminal_ids)
        records = tuple(
            _load_or_run_replay_record(
                resolved,
                static,
                terminal,
                policy,
                scope,
                manifest_hash,
            )
            for terminal in static.terminal_attempts
        )
        _validate_replay_directory_entries(resolved, terminal_ids)
        sources_after, source_set_after = _verifier_runtime_sources()
        if (
            sources_after != sources
            or source_set_after != source_set_sha256
        ):
            raise AuditError("aggregate verifier sources changed during replay")
    ledger = {
        "directory": str(resolved),
        "manifest_path": str(resolved / REPLAY_MANIFEST_NAME),
        "manifest_sha256": manifest_hash,
        "manifest": manifest,
        "producer_source_set_is_current": (
            manifest["verifier_runtime_source_set_sha256"]
            == source_set_sha256
        ),
        "historical_producer_revalidated_by_current_verifier": (
            manifest["verifier_runtime_source_set_sha256"]
            != source_set_sha256
        ),
    }
    return records, ledger, sources, source_set_sha256


def audit_run(
    run_directory: Path,
    *,
    scope: FrozenScope = PRODUCTION_SCOPE,
    policy: AuditPolicy = AuditPolicy(),
    replay_directory: Path | None = None,
) -> dict[str, Any]:
    """Audit one frozen run and replay every currently verified LRAT proof.

    The function writes nothing beneath ``run_directory``.  It holds a shared
    lock for the full static audit and replay, runs one bounded checker at a
    time, and checkpoints production replays in an external append-only
    ledger.  It raises :class:`AuditError` on every non-success condition.
    """

    scope = _validate_scope(scope)
    policy = policy.validated()
    if scope.production and not policy.enforce_live_resource_gates:
        raise AuditError("production replay resource gates cannot be disabled")
    _assert_no_symlink_components(run_directory)
    resolved = run_directory.resolve(strict=True)
    if not resolved.is_dir():
        raise AuditError("run directory is not a directory")
    lock_path = resolved / "run.lock"
    if os.path.lexists(lock_path):
        with _ReadLock(resolved):
            static = _static_audit_unlocked(resolved, scope)
            if (
                scope.production
                and static.terminal_attempts
                and replay_directory is None
            ):
                raise AuditError(
                    "production proof replay requires an external replay directory"
                )
            if replay_directory is not None:
                replays, ledger, verifier_sources, verifier_source_set = (
                    _audit_replays_with_ledger(
                        static,
                        scope,
                        policy,
                        replay_directory,
                    )
                )
            else:
                verifier_sources, verifier_source_set = (
                    _verifier_runtime_sources()
                )
                direct_results = tuple(
                    _fresh_replay_one(static, terminal, policy, scope)
                    for terminal in static.terminal_attempts
                )
                sources_after, source_set_after = _verifier_runtime_sources()
                if (
                    sources_after != verifier_sources
                    or source_set_after != verifier_source_set
                ):
                    raise AuditError(
                        "aggregate verifier sources changed during replay"
                    )
                replays = tuple(
                    {
                        "case_id": result["case_id"],
                        "record_path": None,
                        "record_sha256": None,
                        "record_size_bytes": None,
                        "resumed_from_external_ledger": False,
                        "result": result,
                    }
                    for result in direct_results
                )
                ledger = None
    else:
        static = _static_audit_unlocked(resolved, scope)
        if (
            os.path.lexists(lock_path)
            or static.latest_checkpoint["sequence"] != 0
            or static.historical_attempt_count != 0
            or static.terminal_attempts
        ):
            raise AuditError("lock-free pristine run changed during audit")
        replays = ()
        ledger = None
        verifier_sources, verifier_source_set = _verifier_runtime_sources()
    case_ids = [record["case_id"] for record in replays]
    terminal_case_ids = [
        record["case_id"] for record in static.terminal_attempts
    ]
    expected_ids = [
        "".join(map(str, bits)) for bits in product((0, 1), repeat=4)
    ]
    terminal = static.latest_checkpoint["aggregate_status"] == RUNNER_TERMINAL
    if case_ids != terminal_case_ids:
        raise AuditError("replay records and verified terminal leaves differ")
    if terminal and (
        len(replays) != 16
        or terminal_case_ids != expected_ids
        or case_ids != expected_ids
    ):
        raise AuditError("terminal run lacks exactly one fresh replay per leaf")
    if not terminal:
        status = (
            f"INCOMPLETE_{len(static.terminal_attempts)}_OF_16_"
            "VERIFIED_NONCLAIM"
        )
    else:
        status = SUCCESS_STATUS if scope.production else FIXTURE_SUCCESS_STATUS
    replayed_freshly = sum(
        not record["resumed_from_external_ledger"] for record in replays
    )
    replayed_from_ledger = len(replays) - replayed_freshly
    return {
        "schema": AGGREGATE_REPORT_SCHEMA,
        "schema_version": AGGREGATE_REPORT_SCHEMA_VERSION,
        "verifier": VERIFIER,
        "status": status,
        "runner_aggregate_status": static.latest_checkpoint["aggregate_status"],
        "scope_id": scope.scope_id,
        "production_scope": scope.production,
        "claim_boundary": (
            (
                "No aggregate SAT/UNSAT claim is made. This report validates "
                f"exactly {len(static.terminal_attempts)} of 16 frozen leaves; "
                f"{16 - len(static.terminal_attempts)} remain pending."
            )
            if not terminal
            else (
                "This certifies UNSAT of the exact frozen 16-leaf partition "
                "only. Promotion to a mathematical n=12,k=4 theorem "
                "additionally requires the independent mathematical "
                "scope/encoding assembly."
            )
        ),
        "run_directory": str(resolved),
        "run_manifest_sha256": static.run_manifest_sha256,
        "partition_sha256": static.partition_sha256,
        "parent_cnf_sha256": static.parent_sha256,
        "latest_checkpoint_sha256": static.latest_checkpoint_sha256,
        "latest_checkpoint_sequence": static.latest_checkpoint["sequence"],
        "checkpoint_count": static.checkpoint_count,
        "historical_attempt_count": static.historical_attempt_count,
        "coverage_rows_sha256": static.coverage_rows_sha256,
        "coverage_assignment_count": 16,
        "pairwise_disjoint_pair_count": 120,
        "independent_parent_reconstruction_performed": scope.production,
        "independent_leaf_reconstruction_per_replay": True,
        "fresh_normalized_rup_replay_required": False,
        "fresh_normalized_rup_replay_performed": False,
        "normalized_rup_assurance": (
            "The auditor independently scans raw and normalized binary DRAT, "
            "checks the canonical additions-only normalization report, and "
            "freshly replays the resulting LRAT. A second fresh forward-RUP "
            "run is supplemental rather than necessary for the finite claim."
        ),
        "verified_leaf_count": len(static.terminal_attempts),
        "pending_leaf_count": 16 - len(static.terminal_attempts),
        "fresh_lrat_success_count": len(replays),
        "fresh_lrat_executed_this_invocation": replayed_freshly,
        "fresh_lrat_resumed_from_ledger": replayed_from_ledger,
        "replay_policy": _policy_record(policy),
        "external_replay_ledger": ledger,
        "verifier_runtime_sources": verifier_sources,
        "verifier_runtime_source_set_sha256": verifier_source_set,
        "fresh_lrat_replays": list(replays),
        "completed_unix_ns": time.time_ns(),
    }
