"""Fail-closed proof production for one exact order-13 k=3 template.

Operations are deliberately separate:

``initialize``
    Freeze formula, constructor, runtime-source, tool, and resource bindings in
    a new exclusive run directory.  No child process is launched.

``run``
    Execute at most one attempt, with a checkpoint before the first child and
    another after a durable outcome.  The six sequential phases are solver,
    raw forward DRAT check, strict normalization, RUP-only forward check,
    backward LRAT conversion, and independently pinned LRAT replay.

``audit``
    Read-only structural and cryptographic audit.  It never launches a child.

Timeouts, resource failures, malformed output, and solver UNSAT without the
complete checked chain are all explicit nonclaims.  SAT is candidate-only even
after direct semantic validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import re
import shutil
import signal
import stat
import sys
import tempfile
import time
from dataclasses import asdict
from pathlib import Path
from typing import Mapping, Sequence

from synthesis_k3.cegar import (
    ChildResult,
    RunLock,
    _available_memory_bytes,
    _command_sha256,
    parse_dimacs_bytes,
    parse_solver_result_bytes,
    run_bounded_child,
    validate_model_satisfies_cnf,
)

from .encoding import (
    EXPECTED_FORMULAS,
    TEMPLATES,
    build_full_encoding,
    validate_decoded_candidate,
)
from .generate import (
    BANK_NAME,
    INSTANCE_NAME,
    MANIFEST_NAME as CONSTRUCTOR_MANIFEST_NAME,
    audit_package,
    campaign_root,
    canonical_json_bytes,
    sha256_file,
)
from .normalize_bdrat import POLICY as NORMALIZATION_POLICY
from .normalize_bdrat import SCHEMA as NORMALIZATION_SCHEMA


SCHEMA_VERSION = 1
PIPELINE = (
    "raw-binary-drat-forward-normalize-rup-forward-backward-lrat-replay-v1"
)
RUN_MANIFEST_NAME = "run-manifest.json"
LOCK_NAME = "run.lock"
CHECKPOINTS_NAME = "checkpoints"
ATTEMPTS_NAME = "attempts"
CHECKPOINT_RE = re.compile(r"checkpoint-([0-9]{6})\.json\Z")
ATTEMPT_RE = re.compile(r"attempt-([0-9]{6})\Z")

DEFAULT_SOLVER_WALL_SECONDS = 1800
DEFAULT_POSTPROCESS_WALL_SECONDS = 1800
DEFAULT_MEMORY_MIB = 2048
DEFAULT_FILE_MIB = 2048
DEFAULT_DISK_RESERVE_MIB = 8192
DEFAULT_MEMORY_RESERVE_MIB = 2048
DEFAULT_LOAD_MAX = 7.5
MAX_CHILD_MEMORY_MIB = 2048
MAX_CHILD_FILE_MIB = 2048
MIN_DISK_RESERVE_MIB = 8192
LIVE_FILE_SLOTS = 5
DISK_METADATA_MIB = 64
ACCEPTED_TOOL_SHA256 = {
    "cadical": "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6",
    "drat_trim": "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb",
    "lrat_check": "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2",
}
FROZEN_TOOL_IDENTITY = {
    "cadical": {
        "name": "CaDiCaL",
        "version": "3.0.1",
        "commit": "c60730422e758ef1cebe7aeddf2dda31c996bf04",
    },
    "drat_trim": {
        "name": "drat-trim",
        "version": "2023-05-22 campaign build",
        "commit": "2e5e29cb0019d5cfd547d4208dca1b3ec290349f",
    },
    "lrat_check": {
        "name": "lrat-check",
        "version": "2023-05-22 campaign build",
        "commit": "2e5e29cb0019d5cfd547d4208dca1b3ec290349f",
    },
}

RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/search/order13_k3/__init__.py",
    "src/search/order13_k3/encoding.py",
    "src/search/order13_k3/generate.py",
    "src/search/order13_k3/normalize_bdrat.py",
    "src/search/order13_k3/PRODUCTION_PROTOCOL.md",
    "src/search/order13_k3/production.py",
    "src/synthesis_k3/__init__.py",
    "src/synthesis_k3/encoding.py",
    "src/synthesis_k3/coloring.py",
    "src/synthesis_k3/generate.py",
    "src/synthesis_k3/cegar.py",
)

FINAL_SUCCESS = "UNSAT_LRAT_VERIFIED_PENDING_HOSTILE_AUDIT"
SAT_CANDIDATE = (
    "SAT_CANDIDATE_SEMANTICALLY_VALIDATED_PENDING_INDEPENDENT_VERIFICATION"
)
RUNNABLE = {"PENDING", "RETRYABLE_NONCLAIM"}
FROZEN = {FINAL_SUCCESS, SAT_CANDIDATE}
RECOVERED_OUTCOME_STATUS = "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM"
OUTCOME_CLAIM_STATUS = {
    FINAL_SUCCESS: "FORMULA_UNSAT_AFTER_COMPLETE_LRAT_REPLAY",
    SAT_CANDIDATE: "SAT_CANDIDATE_ONLY",
    "RETRYABLE_NONCLAIM": "NO_SAT_OR_UNSAT_CLAIM",
    RECOVERED_OUTCOME_STATUS: "NO_SAT_OR_UNSAT_CLAIM",
}
RECOVERY_REASON = (
    "The previous orchestrator ended before a terminal outcome was "
    "checkpointed. The operator explicitly requested recovery after checking "
    "no child from the attempt remained active. Any uncheckpointed outcome "
    "bytes were moved intact to an external recovery quarantine."
)
CERTIFICATE_CLAIM_BOUNDARY = (
    "One exact template formula has a locally replayed LRAT proof. "
    "Template coverage and hostile independent replay remain separate."
)


class PhaseFailure(RuntimeError):
    def __init__(self, status: str, details: Mapping[str, object]) -> None:
        super().__init__(status)
        self.status = status
        self.details = dict(details)


def _strict_json_bytes(payload: bytes) -> object:
    def reject_constant(value: str) -> object:
        raise ValueError(f"non-finite JSON constant {value!r}")

    def reject_duplicates(
        pairs: list[tuple[str, object]],
    ) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("JSON is not UTF-8") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("malformed JSON") from error


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _quarantine_entry(
    run_directory: Path,
    source: Path,
    *,
    reason: str,
) -> dict[str, object]:
    """Move an interrupted, untracked entry intact outside the run tree."""

    if not source.exists() and not source.is_symlink():
        raise FileNotFoundError(f"quarantine source is absent: {source}")
    parent = run_directory.parent
    if not parent.is_dir() or parent.is_symlink():
        raise ValueError("run parent is malformed")
    stem = (
        f"{run_directory.name}.recovery-quarantine-"
        f"{time.time_ns()}-{os.getpid()}"
    )
    container: Path | None = None
    for suffix in range(1000):
        candidate = parent / f"{stem}-{suffix:03d}"
        try:
            os.mkdir(candidate, 0o700)
        except FileExistsError:
            continue
        container = candidate
        break
    if container is None:
        raise RuntimeError("could not allocate an exclusive quarantine directory")
    destination = container / source.name
    try:
        os.replace(source, destination)
        _fsync_directory(source.parent)
        _fsync_directory(container)
        _fsync_directory(parent)
        moved_kind = (
            "symlink"
            if destination.is_symlink()
            else "directory"
            if destination.is_dir()
            else "regular_file"
            if destination.is_file()
            else "other"
        )
        moved_binding = (
            _binding(destination, "quarantined entry")
            if moved_kind == "regular_file"
            else None
        )
        record = {
            "schema": "gamma-theta-order13-k3-recovery-quarantine-v1",
            "schema_version": 1,
            "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
            "reason": reason,
            "original_path": str(source.absolute()),
            "quarantined_path": str(destination.absolute()),
            "moved_kind": moved_kind,
            "moved_binding": moved_binding,
            "moved_unix_ns": time.time_ns(),
        }
        _write_exclusive(
            container / "quarantine-record.json",
            canonical_json_bytes(record),
        )
        _fsync_directory(container)
        _fsync_directory(parent)
    except BaseException:
        # Never erase interrupted bytes.  If the move happened, leave the
        # exclusive quarantine directory in place for manual inspection.
        if source.exists() or source.is_symlink():
            try:
                container.rmdir()
            except OSError:
                pass
        raise
    return {
        "quarantine_directory": str(container.absolute()),
        "quarantined_path": str(destination.absolute()),
        "record": _binding(
            container / "quarantine-record.json", "quarantine record"
        ),
        "moved_binding": moved_binding,
    }


def _assert_no_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current /= component
        try:
            information = os.lstat(current)
        except FileNotFoundError:
            break
        if stat.S_ISLNK(information.st_mode):
            raise ValueError(f"symlinked path component is forbidden: {current}")


def _regular(path: Path, role: str, *, executable: bool = False) -> os.stat_result:
    _assert_no_symlink_components(path)
    try:
        information = os.lstat(path)
    except FileNotFoundError as error:
        raise ValueError(f"{role} is absent: {path}") from error
    if (
        not stat.S_ISREG(information.st_mode)
        or information.st_nlink != 1
        or stat.S_ISLNK(information.st_mode)
    ):
        raise ValueError(f"{role} is not a single-link regular file")
    if executable and not os.access(path, os.X_OK):
        raise ValueError(f"{role} is not executable")
    return information


def _write_exclusive(path: Path, payload: bytes) -> None:
    _assert_no_symlink_components(path.parent)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        _fsync_directory(path.parent)
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _binding(path: Path, role: str) -> dict[str, object]:
    information = _regular(path, role)
    return {
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "size_bytes": information.st_size,
    }


def _verify_binding(binding: object, role: str) -> Path:
    if (
        not isinstance(binding, dict)
        or set(binding) != {"path", "sha256", "size_bytes"}
        or not isinstance(binding.get("path"), str)
        or not isinstance(binding.get("sha256"), str)
        or type(binding.get("size_bytes")) is not int
    ):
        raise ValueError(f"{role} binding is malformed")
    path = Path(binding["path"])
    actual = _binding(path, role)
    if actual != binding:
        raise ValueError(f"{role} binding differs")
    return path


def _same_bound_contents(first: object, second: object) -> bool:
    return (
        isinstance(first, dict)
        and isinstance(second, dict)
        and first.get("sha256") == second.get("sha256")
        and first.get("size_bytes") == second.get("size_bytes")
    )


def _source_bindings() -> dict[str, dict[str, object]]:
    root = campaign_root()
    return {
        relative: _binding(root / relative, f"runtime source {relative}")
        for relative in RUNTIME_SOURCE_RELATIVE_PATHS
    }


def _source_set_hash(bindings: Mapping[str, Mapping[str, object]]) -> str:
    payload = "".join(
        f"{relative} {record['sha256']} {record['size_bytes']}\n"
        for relative, record in sorted(bindings.items())
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def _verify_sources(observed: object) -> None:
    if not isinstance(observed, dict):
        raise ValueError("runtime source bindings are malformed")
    expected = _source_bindings()
    if observed != expected:
        raise ValueError("runtime source bindings differ from initialized bytes")


def _tool_binding(path: Path, role: str) -> dict[str, object]:
    resolved = path.resolve(strict=True)
    _regular(resolved, role, executable=True)
    return _binding(resolved, role)


def _verify_tools(tools: object) -> Mapping[str, Mapping[str, object]]:
    if not isinstance(tools, dict) or set(tools) != {
        "cadical",
        "drat_trim",
        "lrat_check",
        "normalizer_python",
    }:
        raise ValueError("tool bindings have the wrong shape")
    paths: list[Path] = []
    for role, binding in tools.items():
        path = _verify_binding(binding, f"tool {role}")
        _regular(path, f"tool {role}", executable=True)
        paths.append(path.resolve())
    if len(set(paths)) != len(paths):
        raise ValueError("production tool roles must use distinct executables")
    return tools


def _tool_identity(
    tools: Mapping[str, Mapping[str, object]],
) -> dict[str, object]:
    python = tools.get("normalizer_python")
    if not isinstance(python, dict):
        raise ValueError("normalizer Python binding is absent")
    return {
        **{
            role: dict(identity)
            for role, identity in FROZEN_TOOL_IDENTITY.items()
        },
        "normalizer_python": {
            "name": "Python",
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "platform": platform.platform(),
            "executable_path": python["path"],
            "executable_sha256": python["sha256"],
        },
    }


def _verify_production_toolchain(
    tools_raw: object,
    accepted_raw: object,
    identity_raw: object,
) -> Mapping[str, Mapping[str, object]]:
    tools = _verify_tools(tools_raw)
    if accepted_raw != dict(ACCEPTED_TOOL_SHA256):
        raise ValueError("accepted production tool policy differs")
    for role, expected_hash in ACCEPTED_TOOL_SHA256.items():
        if tools[role]["sha256"] != expected_hash:
            raise ValueError(
                f"{role} binding is not linked to its accepted hash"
            )
    python = tools["normalizer_python"]
    current_python = Path(sys.executable).resolve(strict=True)
    if (
        Path(str(python["path"])).resolve(strict=True) != current_python
        or python["sha256"] != sha256_file(current_python)
    ):
        raise ValueError(
            "normalizer Python is not the current bound interpreter"
        )
    if identity_raw != _tool_identity(tools):
        raise ValueError("human-readable tool identity differs")
    return tools


def _validate_limits(limits: Mapping[str, object]) -> dict[str, object]:
    integer_fields = (
        "solver_wall_seconds",
        "postprocess_wall_seconds",
        "solver_memory_mib",
        "postprocess_memory_mib",
        "file_limit_mib",
        "disk_reserve_mib",
        "memory_reserve_mib",
    )
    if any(type(limits.get(name)) is not int for name in integer_fields):
        raise ValueError("resource limits must be exact integers")
    if (
        not 1 <= int(limits["solver_wall_seconds"]) <= 21600
        or not 1 <= int(limits["postprocess_wall_seconds"]) <= 21600
        or not 1 <= int(limits["solver_memory_mib"]) <= MAX_CHILD_MEMORY_MIB
        or not 1 <= int(limits["postprocess_memory_mib"]) <= MAX_CHILD_MEMORY_MIB
        or not 1 <= int(limits["file_limit_mib"]) <= MAX_CHILD_FILE_MIB
        or int(limits["disk_reserve_mib"]) < MIN_DISK_RESERVE_MIB
        or int(limits["memory_reserve_mib"]) < 512
        or type(limits.get("load_max")) not in (int, float)
        or not math.isfinite(float(limits["load_max"]))
        or float(limits["load_max"]) <= 0
        or limits.get("parallel_children") != 1
    ):
        raise ValueError("resource limits violate production ceilings")
    return dict(limits)


def _validate_new_run(path: Path) -> Path:
    _assert_no_symlink_components(path)
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"run directory already exists: {path}")
    if not path.parent.is_dir():
        raise ValueError("run parent is absent")
    resolved = path.resolve(strict=False)
    root = campaign_root().resolve()
    if resolved in {root, Path.home().resolve(), Path(resolved.anchor)}:
        raise ValueError("unsafe run directory")
    for protected in (root / "src", root / "math", root / "tests"):
        try:
            resolved.relative_to(protected)
        except ValueError:
            continue
        raise ValueError(f"run directory lies in protected tree {protected}")
    return resolved


def initialize(
    *,
    package_directory: Path,
    run_directory: Path,
    cadical_path: Path,
    drat_trim_path: Path,
    lrat_check_path: Path,
    normalizer_python_path: Path,
    seed: int,
    limits: Mapping[str, object],
    validation_gate: object,
) -> dict[str, object]:
    if validation_gate is not True:
        raise PermissionError("explicit production initialization gate is required")
    if type(seed) is not int or seed < 0:
        raise ValueError("seed must be a nonnegative exact integer")
    constructor_report = audit_package(package_directory, exhaustive=True)
    template = constructor_report["template"]
    if template not in TEMPLATES:
        raise ValueError("constructor template differs")
    limits = _validate_limits(limits)
    destination = _validate_new_run(run_directory)
    sources = _source_bindings()
    if normalizer_python_path.resolve(strict=True) != Path(
        sys.executable
    ).resolve(strict=True):
        raise ValueError(
            "normalizer Python must be the interpreter running initialization"
        )
    tools = {
        "cadical": _tool_binding(cadical_path, "CaDiCaL"),
        "drat_trim": _tool_binding(drat_trim_path, "drat-trim"),
        "lrat_check": _tool_binding(lrat_check_path, "lrat-check"),
        "normalizer_python": _tool_binding(
            normalizer_python_path, "normalizer Python"
        ),
    }
    _verify_tools(tools)
    for role, expected_hash in ACCEPTED_TOOL_SHA256.items():
        if tools[role]["sha256"] != expected_hash:
            raise ValueError(
                f"{role} is not the campaign-pinned production executable"
            )
    identity = _tool_identity(tools)
    _verify_production_toolchain(
        tools, dict(ACCEPTED_TOOL_SHA256), identity
    )

    staging = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.partial-", dir=destination.parent)
    )
    try:
        (staging / CHECKPOINTS_NAME).mkdir()
        (staging / ATTEMPTS_NAME).mkdir()
        for name in (INSTANCE_NAME, BANK_NAME, CONSTRUCTOR_MANIFEST_NAME):
            source = package_directory.resolve() / name
            _regular(source, f"constructor artifact {name}")
            shutil.copyfile(source, staging / name)
            with (staging / name).open("rb") as handle:
                os.fsync(handle.fileno())
        (staging / LOCK_NAME).touch(mode=0o600, exist_ok=False)
        copied = {
            name: _binding(staging / name, f"copied constructor artifact {name}")
            for name in (INSTANCE_NAME, BANK_NAME, CONSTRUCTOR_MANIFEST_NAME)
        }
        # Paths in copied bindings must name their final locations.
        for name, record in copied.items():
            record["path"] = str((destination / name).resolve())
        manifest: dict[str, object] = {
            "schema": "gamma-theta-order13-k3-production-run-v1",
            "schema_version": SCHEMA_VERSION,
            "proof_pipeline": PIPELINE,
            "claim_status": "NO_SAT_OR_UNSAT_CLAIM_AT_INITIALIZATION",
            "template": template,
            "order": 13,
            "parameter": 3,
            "seed": seed,
            "constructor_artifacts": copied,
            "expected_formula": dict(EXPECTED_FORMULAS[template]),
            "runtime_sources": sources,
            "runtime_source_set_sha256": _source_set_hash(sources),
            "tools": tools,
            "accepted_production_tool_sha256": dict(ACCEPTED_TOOL_SHA256),
            "tool_identity": identity,
            "limits": limits,
            "hardware": {
                "machine": platform.machine(),
                "logical_cpus": os.cpu_count(),
                "physical_memory_bytes": (
                    os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
                ),
            },
            "normalized_resume_invocation": [
                "/usr/bin/env",
                "PYTHONPATH=src",
                sys.executable,
                "-m",
                "search.order13_k3.production",
                "run",
                "--run-directory",
                str(destination),
                "--production-gate",
            ],
            "normalized_audit_invocation": [
                "/usr/bin/env",
                "PYTHONPATH=src",
                sys.executable,
                "-m",
                "search.order13_k3.production",
                "audit",
                "--run-directory",
                str(destination),
            ],
            "created_unix_ns": time.time_ns(),
        }
        manifest_bytes = canonical_json_bytes(manifest)
        _write_exclusive(staging / RUN_MANIFEST_NAME, manifest_bytes)
        manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
        checkpoint = {
            "schema": "gamma-theta-order13-k3-production-checkpoint-v1",
            "schema_version": SCHEMA_VERSION,
            "sequence": 0,
            "previous_checkpoint_sha256": None,
            "run_manifest_sha256": manifest_hash,
            "status": "PENDING",
            "attempt_count": 0,
            "attempt": None,
            "outcome": None,
            "event": "INITIALIZED",
            "written_unix_ns": time.time_ns(),
        }
        _write_exclusive(
            staging / CHECKPOINTS_NAME / "checkpoint-000000.json",
            canonical_json_bytes(checkpoint),
        )
        os.replace(staging, destination)
        _fsync_directory(destination.parent)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return {
        "initialized": True,
        "template": template,
        "run_directory": str(destination),
        "run_manifest_sha256": manifest_hash,
        "status": "PENDING",
        "child_launched": False,
    }


def _read_canonical_json(path: Path, role: str) -> dict[str, object]:
    _regular(path, role)
    payload = path.read_bytes()
    parsed = _strict_json_bytes(payload)
    if not isinstance(parsed, dict) or canonical_json_bytes(parsed) != payload:
        raise ValueError(f"{role} is not a canonical JSON object")
    return parsed


def _checkpoint_files(run_directory: Path) -> list[Path]:
    directory = run_directory / CHECKPOINTS_NAME
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("checkpoint directory is malformed")
    result = sorted(directory.iterdir())
    for index, path in enumerate(result):
        match = CHECKPOINT_RE.fullmatch(path.name)
        if match is None or int(match.group(1)) != index:
            raise ValueError("checkpoint sequence is not consecutive")
        _regular(path, "checkpoint")
    if not result:
        raise ValueError("run has no checkpoint")
    return result


def _attempt_directory(run_directory: Path, number: int) -> Path:
    if type(number) is not int or number < 1:
        raise ValueError("attempt number is invalid")
    return run_directory / ATTEMPTS_NAME / f"attempt-{number:06d}"


def _verify_exact_binding_path(
    binding: object,
    expected_path: Path,
    role: str,
) -> Path:
    expected = expected_path.resolve()
    if (
        not isinstance(binding, dict)
        or binding.get("path") != str(expected)
    ):
        raise ValueError(f"{role} path is not the canonical run-local path")
    observed = _verify_binding(binding, role)
    if observed.resolve() != expected:
        raise ValueError(f"{role} resolved path differs")
    return observed


def _audit_checkpoints(
    run_directory: Path,
    manifest_hash: str,
) -> tuple[dict[str, object], str]:
    files = _checkpoint_files(run_directory)
    previous_hash: str | None = None
    previous: dict[str, object] | None = None
    expected_keys = {
        "schema",
        "schema_version",
        "sequence",
        "previous_checkpoint_sha256",
        "run_manifest_sha256",
        "status",
        "attempt_count",
        "attempt",
        "outcome",
        "event",
        "written_unix_ns",
    }
    for sequence, path in enumerate(files):
        checkpoint = _read_canonical_json(path, f"checkpoint {sequence}")
        if (
            set(checkpoint) != expected_keys
            or
            checkpoint.get("schema")
            != "gamma-theta-order13-k3-production-checkpoint-v1"
            or checkpoint.get("schema_version") != SCHEMA_VERSION
            or checkpoint.get("sequence") != sequence
            or checkpoint.get("previous_checkpoint_sha256") != previous_hash
            or checkpoint.get("run_manifest_sha256") != manifest_hash
            or type(checkpoint.get("written_unix_ns")) is not int
            or int(checkpoint["written_unix_ns"]) <= 0
            or type(checkpoint.get("attempt_count")) is not int
            or int(checkpoint["attempt_count"]) < 0
        ):
            raise ValueError(f"checkpoint {sequence} header differs")
        if (
            previous is not None
            and int(checkpoint["written_unix_ns"])
            < int(previous["written_unix_ns"])
        ):
            raise ValueError("checkpoint timestamps decrease")
        status = checkpoint.get("status")
        event = checkpoint.get("event")
        if sequence == 0:
            if (
                status != "PENDING"
                or event != "INITIALIZED"
                or checkpoint.get("attempt_count") != 0
                or checkpoint.get("attempt") is not None
                or checkpoint.get("outcome") is not None
            ):
                raise ValueError("initial checkpoint differs")
        else:
            if previous is None:
                raise AssertionError("checkpoint predecessor vanished")
            previous_status = previous["status"]
            previous_count = previous["attempt_count"]
            if event == "RUN_STARTED":
                if (
                    previous_status not in RUNNABLE
                    or status != "RUNNING_UNFINISHED_NONCLAIM"
                    or checkpoint["attempt_count"] != previous_count + 1
                    or sequence != 2 * int(checkpoint["attempt_count"]) - 1
                    or checkpoint.get("attempt") is None
                    or checkpoint.get("outcome") is not None
                ):
                    raise ValueError("RUN_STARTED checkpoint transition differs")
            elif event == "RUN_FINISHED":
                if (
                    previous_status != "RUNNING_UNFINISHED_NONCLAIM"
                    or checkpoint["attempt_count"] != previous_count
                    or sequence != 2 * int(checkpoint["attempt_count"])
                    or status
                    not in {
                        "RETRYABLE_NONCLAIM",
                        FINAL_SUCCESS,
                        SAT_CANDIDATE,
                    }
                    or checkpoint.get("attempt") != previous.get("attempt")
                    or checkpoint.get("outcome") is None
                ):
                    raise ValueError("terminal checkpoint transition differs")
            elif event == "INTERRUPTED_RECOVERED":
                if (
                    previous_status != "RUNNING_UNFINISHED_NONCLAIM"
                    or checkpoint["attempt_count"] != previous_count
                    or sequence != 2 * int(checkpoint["attempt_count"])
                    or status != "RETRYABLE_NONCLAIM"
                    or checkpoint.get("attempt") != previous.get("attempt")
                    or checkpoint.get("outcome") is None
                ):
                    raise ValueError(
                        "recovery checkpoint transition differs"
                    )
            elif event == "UNTRACKED_OUTCOME_QUARANTINED":
                if (
                    previous_status != "RUNNING_UNFINISHED_NONCLAIM"
                    or checkpoint["attempt_count"] != previous_count
                    or sequence != 2 * int(checkpoint["attempt_count"])
                    or status != "RETRYABLE_NONCLAIM"
                    or checkpoint.get("attempt") != previous.get("attempt")
                    or checkpoint.get("outcome") is None
                ):
                    raise ValueError(
                        "untracked-outcome quarantine transition differs"
                    )
            else:
                raise ValueError("checkpoint event differs")
        attempt_binding = checkpoint.get("attempt")
        outcome_binding = checkpoint.get("outcome")
        if attempt_binding is not None:
            attempt = _attempt_directory(
                run_directory, int(checkpoint["attempt_count"])
            )
            _verify_exact_binding_path(
                attempt_binding,
                attempt / "attempt-config.json",
                "attempt configuration",
            )
        if outcome_binding is not None:
            attempt = _attempt_directory(
                run_directory, int(checkpoint["attempt_count"])
            )
            outcome_path = _verify_exact_binding_path(
                outcome_binding,
                attempt / "outcome.json",
                "attempt outcome",
            )
            outcome = _read_canonical_json(outcome_path, "attempt outcome")
            expected_outcome_status = (
                RECOVERED_OUTCOME_STATUS
                if event == "INTERRUPTED_RECOVERED"
                else status
            )
            if event == "UNTRACKED_OUTCOME_QUARANTINED":
                if outcome.get("status") not in OUTCOME_CLAIM_STATUS:
                    raise ValueError(
                        "quarantined outcome status is unrecognized"
                    )
            elif outcome.get("status") != expected_outcome_status:
                raise ValueError("checkpoint and outcome statuses differ")
        previous = checkpoint
        previous_hash = sha256_file(path)
    if previous is None or previous_hash is None:
        raise AssertionError("checkpoint audit returned nothing")
    expected_checkpoint_count = (
        2 * int(previous["attempt_count"])
        if previous["status"] == "RUNNING_UNFINISHED_NONCLAIM"
        else 2 * int(previous["attempt_count"]) + 1
    )
    if len(files) != expected_checkpoint_count:
        raise ValueError("checkpoint count and latest attempt count differ")
    return previous, previous_hash


def _audit_attempts(
    run_directory: Path,
    manifest: Mapping[str, object],
    manifest_hash: str,
    latest: Mapping[str, object],
    *,
    allow_uncheckpointed_outcome: bool = False,
    allow_precheckpoint_orphan: bool = False,
) -> int:
    directory = run_directory / ATTEMPTS_NAME
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("attempt directory is malformed")
    attempts = sorted(directory.iterdir())
    expected_count = latest.get("attempt_count")
    if type(expected_count) is not int:
        raise ValueError("attempt directory count differs from checkpoint")
    has_precheckpoint_orphan = (
        allow_precheckpoint_orphan
        and latest.get("status") in RUNNABLE
        and len(attempts) == expected_count + 1
    )
    if len(attempts) != expected_count and not has_precheckpoint_orphan:
        raise ValueError("attempt directory count differs from checkpoint")
    if has_precheckpoint_orphan:
        orphan = attempts[-1]
        orphan_match = ATTEMPT_RE.fullmatch(orphan.name)
        if (
            orphan_match is None
            or int(orphan_match.group(1)) != expected_count + 1
            or orphan
            != _attempt_directory(run_directory, expected_count + 1)
            or not orphan.is_dir()
            or orphan.is_symlink()
        ):
            raise ValueError("precheckpoint orphan attempt differs")
    for index, attempt in enumerate(attempts[:expected_count], start=1):
        match = ATTEMPT_RE.fullmatch(attempt.name)
        if (
            match is None
            or int(match.group(1)) != index
            or attempt != _attempt_directory(run_directory, index)
            or not attempt.is_dir()
            or attempt.is_symlink()
        ):
            raise ValueError("attempt sequence differs")
        config = _read_canonical_json(attempt / "attempt-config.json", "attempt config")
        expected_instance = _binding(attempt / INSTANCE_NAME, "attempt instance")
        constructor_artifacts = manifest.get("constructor_artifacts")
        frozen_instance = (
            constructor_artifacts.get(INSTANCE_NAME)
            if isinstance(constructor_artifacts, dict)
            else None
        )
        if (
            set(config)
            != {
                "schema",
                "schema_version",
                "claim_status",
                "proof_pipeline",
                "attempt_number",
                "template",
                "seed",
                "run_manifest_sha256",
                "instance",
                "runtime_source_set_sha256",
                "tools",
                "limits",
                "commands",
                "created_unix_ns",
            }
            or config.get("schema")
            != "gamma-theta-order13-k3-attempt-config-v1"
            or config.get("schema_version") != 1
            or config.get("claim_status")
            != "NO_SAT_OR_UNSAT_CLAIM_BEFORE_EXECUTION"
            or config.get("proof_pipeline") != PIPELINE
            or config.get("attempt_number") != index
            or config.get("template") != manifest.get("template")
            or config.get("seed") != manifest.get("seed")
            or config.get("run_manifest_sha256") != manifest_hash
            or config.get("instance") != expected_instance
            or not _same_bound_contents(expected_instance, frozen_instance)
            or config.get("runtime_source_set_sha256")
            != manifest.get("runtime_source_set_sha256")
            or config.get("tools") != manifest.get("tools")
            or config.get("limits") != manifest.get("limits")
            or config.get("commands") != _commands(manifest, attempt)
            or type(config.get("created_unix_ns")) is not int
            or int(config["created_unix_ns"]) <= 0
        ):
            raise ValueError("attempt configuration differs from frozen inputs")
        outcome_path = attempt / "outcome.json"
        running_without_outcome = (
            latest.get("status") == "RUNNING_UNFINISHED_NONCLAIM"
            and index == expected_count
        )
        outcome_exists = outcome_path.exists() or outcome_path.is_symlink()
        if running_without_outcome:
            if outcome_exists and not allow_uncheckpointed_outcome:
                raise ValueError("running attempt unexpectedly has an outcome")
            # Explicit recovery treats every uncheckpointed outcome, including
            # partial or malformed bytes, as opaque nonclaim data.  It is moved
            # intact outside the run tree before a canonical recovery outcome
            # is written.  Ordinary audit still rejects this state.
            continue
        if not outcome_exists:
            raise ValueError("completed attempt has no outcome")
        outcome = _read_canonical_json(outcome_path, "attempt outcome")
        outcome_status = outcome.get("status")
        if (
            outcome.get("schema") != "gamma-theta-order13-k3-attempt-outcome-v1"
            or outcome.get("schema_version") != 1
            or outcome_status not in OUTCOME_CLAIM_STATUS
            or outcome.get("claim_status")
            != OUTCOME_CLAIM_STATUS[outcome_status]
            or type(outcome.get("finished_unix_ns")) is not int
            or int(outcome["finished_unix_ns"]) < int(config["created_unix_ns"])
        ):
            raise ValueError("attempt outcome semantics differ")
        if outcome_status == RECOVERED_OUTCOME_STATUS:
            if (
                set(outcome)
                != {
                    "schema",
                    "schema_version",
                    "status",
                    "claim_status",
                    "reason",
                    "artifacts",
                    "finished_unix_ns",
                }
                or outcome.get("reason") != RECOVERY_REASON
            ):
                raise ValueError("recovered attempt outcome differs")
        else:
            if set(outcome) != {
                "schema",
                "schema_version",
                "status",
                "claim_status",
                "details",
                "artifacts",
                "finished_unix_ns",
            }:
                raise ValueError("ordinary attempt outcome shape differs")
        artifacts = outcome.get("artifacts")
        if not isinstance(artifacts, dict):
            raise ValueError("attempt artifact map is absent")
        actual_artifacts = {
            path.name for path in attempt.iterdir() if path.name != "outcome.json"
        }
        if set(artifacts) != actual_artifacts:
            raise ValueError("attempt artifact set differs from outcome")
        for name, binding in artifacts.items():
            if not isinstance(name, str) or Path(name).name != name:
                raise ValueError("attempt artifact name is unsafe")
            expected_path = attempt / name
            if (
                not isinstance(binding, dict)
                or binding.get("path") != str(expected_path.resolve())
            ):
                raise ValueError("attempt artifact path differs")
            _verify_binding(binding, f"attempt artifact {name}")
        if outcome_status == FINAL_SUCCESS:
            _audit_success_attempt(attempt, manifest, config, outcome)
        elif outcome_status == SAT_CANDIDATE:
            _audit_sat_candidate(attempt, manifest, config, outcome)
        elif outcome_status == "RETRYABLE_NONCLAIM":
            details = outcome.get("details")
            if (
                not isinstance(details, dict)
                or not isinstance(details.get("phase_status"), str)
                or not str(details["phase_status"]).endswith("_NONCLAIM")
            ):
                raise ValueError("retryable outcome details differ")
    return expected_count


def _audit_sat_candidate(
    attempt: Path,
    manifest: Mapping[str, object],
    config: Mapping[str, object],
    outcome: Mapping[str, object],
) -> None:
    candidate = _read_canonical_json(
        attempt / "candidate.json", "SAT candidate"
    )
    expected_keys = {
        "schema",
        "schema_version",
        "status",
        "template",
        "instance",
        "solver_result",
        "assignment_sha256",
        "h_edges",
        "eternal_family",
        "required_next_action",
    }
    if (
        set(candidate) != expected_keys
        or candidate.get("schema")
        != "gamma-theta-order13-k3-sat-candidate-v1"
        or candidate.get("schema_version") != 1
        or candidate.get("status") != SAT_CANDIDATE
        or candidate.get("template") != manifest.get("template")
        or candidate.get("instance")
        != _binding(attempt / INSTANCE_NAME, "SAT candidate instance")
        or candidate.get("solver_result")
        != _binding(attempt / "solver.result", "SAT solver result")
        or candidate.get("required_next_action")
        != (
            "Freeze and run a standalone candidate verifier independent "
            "of this search and decoding core."
        )
    ):
        raise ValueError("SAT candidate bindings or header differ")
    details = outcome.get("details")
    if details != {"candidate": candidate}:
        raise ValueError("SAT outcome does not bind exactly its candidate")

    commands = config.get("commands")
    limits = manifest.get("limits")
    if not isinstance(commands, dict) or not isinstance(limits, dict):
        raise ValueError("SAT candidate command bindings differ")
    _audit_resource_gate(attempt, "solver", limits)
    solver_command = commands.get("solver")
    if not isinstance(solver_command, list):
        raise ValueError("SAT solver command is absent")
    child = _read_phase_record(
        attempt,
        "solver",
        readonly={"instance": attempt / INSTANCE_NAME},
        produced={
            "solver_result": attempt / "solver.result",
            "raw_binary_drat": attempt / "proof.raw.bdrat",
        },
    )
    _verify_child(
        child,
        solver_command,
        stdout_path=attempt / "solver.stdout",
        stderr_path=attempt / "solver.stderr",
        wall_seconds=int(limits["solver_wall_seconds"]),
        memory_mib=int(limits["solver_memory_mib"]),
        file_mib=int(limits["file_limit_mib"]),
    )
    if child.exit_code != 10 or _child_failure(child, "solver") is not None:
        raise ValueError("SAT solver child did not complete as SAT")

    cnf = parse_dimacs_bytes((attempt / INSTANCE_NAME).read_bytes())
    parsed = parse_solver_result_bytes(
        (attempt / "solver.result").read_bytes(), cnf.variable_count
    )
    if parsed.status != "SAT" or parsed.model is None:
        raise ValueError("SAT candidate has no complete SAT model")
    validate_model_satisfies_cnf(cnf, parsed.model)
    encoding = build_full_encoding(str(manifest["template"]))
    edges = encoding.decode_edges(parsed.model)
    family = encoding.decode_family(parsed.model)
    validate_decoded_candidate(str(manifest["template"]), edges, family)
    assignment = canonical_json_bytes(
        [
            variable if parsed.model[variable] else -variable
            for variable in range(1, cnf.variable_count + 1)
        ]
    )
    if (
        candidate.get("assignment_sha256")
        != hashlib.sha256(assignment).hexdigest()
        or candidate.get("h_edges") != [list(pair) for pair in edges]
        or candidate.get("eternal_family")
        != [list(state) for state in family]
    ):
        raise ValueError("SAT candidate decoding differs from its model")


def _audit_resource_gate(
    attempt: Path,
    phase: str,
    limits: Mapping[str, object],
) -> dict[str, object]:
    resource = _read_canonical_json(
        attempt / f"resource-{phase}.json",
        f"{phase} resource report",
    )
    expected_memory = int(
        limits[
            "solver_memory_mib"
            if phase == "solver"
            else "postprocess_memory_mib"
        ]
    )
    required_memory = (
        expected_memory + int(limits["memory_reserve_mib"])
    ) << 20
    required_disk = (
        int(limits["disk_reserve_mib"])
        + LIVE_FILE_SLOTS * int(limits["file_limit_mib"])
        + DISK_METADATA_MIB
    ) << 20
    expected_keys = {
        "schema",
        "phase",
        "checked_unix_ns",
        "load_average_one_minute",
        "load_ceiling",
        "available_memory_bytes",
        "required_memory_bytes",
        "free_disk_bytes",
        "required_free_disk_bytes",
        "live_file_slots",
        "probe_errors",
        "checks",
        "passed",
    }
    if (
        set(resource) != expected_keys
        or resource.get("schema")
        != "gamma-theta-order13-k3-resource-gate-v1"
        or resource.get("phase") != phase
        or resource.get("load_ceiling") != limits["load_max"]
        or resource.get("required_memory_bytes") != required_memory
        or resource.get("required_free_disk_bytes") != required_disk
        or resource.get("live_file_slots") != LIVE_FILE_SLOTS
        or resource.get("probe_errors") != []
        or resource.get("checks")
        != {"load": True, "memory": True, "disk": True}
        or resource.get("passed") is not True
        or type(resource.get("checked_unix_ns")) is not int
        or int(resource["checked_unix_ns"]) <= 0
        or type(resource.get("load_average_one_minute"))
        not in (int, float)
        or not math.isfinite(float(resource["load_average_one_minute"]))
        or float(resource["load_average_one_minute"])
        > float(limits["load_max"])
        or type(resource.get("available_memory_bytes")) is not int
        or int(resource["available_memory_bytes"]) < required_memory
        or type(resource.get("free_disk_bytes")) is not int
        or int(resource["free_disk_bytes"]) < required_disk
    ):
        raise ValueError(f"{phase} did not have a clean resource gate")
    return resource


def _audit_success_attempt(
    attempt: Path,
    manifest: Mapping[str, object],
    config: Mapping[str, object],
    outcome: Mapping[str, object],
) -> None:
    commands = config.get("commands")
    limits = manifest.get("limits")
    if not isinstance(commands, dict) or not isinstance(limits, dict):
        raise ValueError("successful attempt command bindings differ")
    phases = (
        "solver",
        "raw_forward",
        "normalizer",
        "normalized_forward",
        "lrat_conversion",
        "lrat_check",
    )
    instance = attempt / INSTANCE_NAME
    raw = attempt / "proof.raw.bdrat"
    normalized = attempt / "proof.normalized.rup.bdrat"
    report = attempt / "normalization-report.json"
    lrat = attempt / "proof.converted.lrat"
    phase_readonly = {
        "solver": {"instance": instance},
        "raw_forward": {"instance": instance, "raw proof": raw},
        "normalizer": {
            "raw proof": raw,
            "normalizer source": (
                campaign_root()
                / "src/search/order13_k3/normalize_bdrat.py"
            ),
        },
        "normalized_forward": {
            "instance": instance,
            "normalized proof": normalized,
        },
        "lrat_conversion": {
            "instance": instance,
            "normalized proof": normalized,
        },
        "lrat_check": {"instance": instance, "LRAT": lrat},
    }
    phase_produced = {
        "solver": {
            "solver_result": attempt / "solver.result",
            "raw_binary_drat": raw,
        },
        "raw_forward": {},
        "normalizer": {
            "normalized_binary_rup": normalized,
            "normalization_report": report,
        },
        "normalized_forward": {},
        "lrat_conversion": {"converted_lrat": lrat},
        "lrat_check": {},
    }
    children: dict[str, ChildResult] = {}
    for phase in phases:
        _audit_resource_gate(attempt, phase, limits)
        expected_memory = int(
            limits[
                "solver_memory_mib"
                if phase == "solver"
                else "postprocess_memory_mib"
            ]
        )
        child = _read_phase_record(
            attempt,
            phase,
            readonly=phase_readonly[phase],
            produced=phase_produced[phase],
        )
        command = commands.get(phase)
        if not isinstance(command, list):
            raise ValueError(f"{phase} command is absent")
        _verify_child(
            child,
            command,
            stdout_path=attempt / f"{phase}.stdout",
            stderr_path=attempt / f"{phase}.stderr",
            wall_seconds=int(
                limits[
                    "solver_wall_seconds"
                    if phase == "solver"
                    else "postprocess_wall_seconds"
                ]
            ),
            memory_mib=expected_memory,
            file_mib=int(limits["file_limit_mib"]),
        )
        if _child_failure(child, phase) is not None:
            raise ValueError(f"{phase} child was resource-terminated")
        children[phase] = child
    if children["solver"].exit_code != 20 or any(
        children[phase].exit_code != 0 for phase in phases[1:]
    ):
        raise ValueError("successful attempt exit codes differ")
    cnf = parse_dimacs_bytes(instance.read_bytes())
    parsed = parse_solver_result_bytes(
        (attempt / "solver.result").read_bytes(), cnf.variable_count
    )
    if parsed.status != "UNSAT":
        raise ValueError("successful attempt solver result is not UNSAT")
    _strict_verified(
        attempt / "raw_forward.stdout",
        attempt / "raw_forward.stderr",
        "s VERIFIED",
    )
    if (
        (attempt / "normalizer.stdout").read_bytes() != b"s NORMALIZED\n"
        or (attempt / "normalizer.stderr").read_bytes()
    ):
        raise ValueError("successful attempt normalizer output differs")
    _validate_normalization(report, raw, normalized)
    _strict_verified(
        attempt / "normalized_forward.stdout",
        attempt / "normalized_forward.stderr",
        "s VERIFIED",
    )
    _strict_verified(
        attempt / "lrat_conversion.stdout",
        attempt / "lrat_conversion.stderr",
        "s VERIFIED",
    )
    if _binding(lrat, "converted LRAT")["size_bytes"] == 0:
        raise ValueError("successful attempt LRAT is empty")
    _strict_verified(
        attempt / "lrat_check.stdout",
        attempt / "lrat_check.stderr",
        "c VERIFIED",
    )
    certificate = _read_canonical_json(
        attempt / "certificate.json", "template certificate"
    )
    certificate_keys = {
        "schema",
        "schema_version",
        "status",
        "proof_pipeline",
        "template",
        "seed",
        "run_manifest",
        "constructor_manifest",
        "runtime_source_set_sha256",
        "tools",
        "instance",
        "raw_binary_drat",
        "normalized_binary_rup",
        "normalization_report",
        "converted_lrat",
        "lrat_check_tool",
        "claim_boundary",
    }
    if (
        set(certificate) != certificate_keys
        or certificate.get("schema")
        != "gamma-theta-order13-k3-template-lrat-certificate-v1"
        or certificate.get("schema_version") != 1
        or certificate.get("status") != FINAL_SUCCESS
        or certificate.get("proof_pipeline") != PIPELINE
        or certificate.get("template") != manifest.get("template")
        or certificate.get("seed") != manifest.get("seed")
        or certificate.get("run_manifest")
        != _binding(attempt.parents[1] / RUN_MANIFEST_NAME, "run manifest")
        or certificate.get("constructor_manifest")
        != _binding(
            attempt.parents[1] / CONSTRUCTOR_MANIFEST_NAME,
            "constructor manifest",
        )
        or certificate.get("runtime_source_set_sha256")
        != manifest.get("runtime_source_set_sha256")
        or certificate.get("tools") != manifest.get("tools")
        or certificate.get("instance") != _binding(instance, "attempt instance")
        or certificate.get("raw_binary_drat") != _binding(raw, "raw proof")
        or certificate.get("normalized_binary_rup")
        != _binding(normalized, "normalized proof")
        or certificate.get("normalization_report")
        != _binding(report, "normalization report")
        or certificate.get("converted_lrat") != _binding(lrat, "converted LRAT")
        or certificate.get("lrat_check_tool")
        != manifest["tools"]["lrat_check"]
        or certificate.get("claim_boundary")
        != CERTIFICATE_CLAIM_BOUNDARY
    ):
        raise ValueError("template certificate bindings differ")
    details = outcome.get("details")
    if details != {"certificate": certificate}:
        raise ValueError("successful outcome does not bind its certificate")


def _load_run(
    run_directory: Path,
    *,
    allow_uncheckpointed_outcome: bool = False,
    allow_precheckpoint_orphan: bool = False,
) -> tuple[dict[str, object], str, dict[str, object], str]:
    _assert_no_symlink_components(run_directory)
    if not run_directory.is_dir() or run_directory.is_symlink():
        raise ValueError("run directory is malformed")
    expected_root_entries = {
        INSTANCE_NAME,
        BANK_NAME,
        CONSTRUCTOR_MANIFEST_NAME,
        RUN_MANIFEST_NAME,
        LOCK_NAME,
        CHECKPOINTS_NAME,
        ATTEMPTS_NAME,
    }
    if {path.name for path in run_directory.iterdir()} != expected_root_entries:
        raise ValueError("run-directory entry set differs")
    manifest_path = run_directory / RUN_MANIFEST_NAME
    manifest = _read_canonical_json(manifest_path, "run manifest")
    manifest_hash = sha256_file(manifest_path)
    manifest_keys = {
        "schema",
        "schema_version",
        "proof_pipeline",
        "claim_status",
        "template",
        "order",
        "parameter",
        "seed",
        "constructor_artifacts",
        "expected_formula",
        "runtime_sources",
        "runtime_source_set_sha256",
        "tools",
        "accepted_production_tool_sha256",
        "tool_identity",
        "limits",
        "hardware",
        "normalized_resume_invocation",
        "normalized_audit_invocation",
        "created_unix_ns",
    }
    if (
        set(manifest) != manifest_keys
        or manifest.get("schema")
        != "gamma-theta-order13-k3-production-run-v1"
        or manifest.get("schema_version") != SCHEMA_VERSION
        or manifest.get("proof_pipeline") != PIPELINE
        or manifest.get("claim_status")
        != "NO_SAT_OR_UNSAT_CLAIM_AT_INITIALIZATION"
        or manifest.get("template") not in TEMPLATES
        or manifest.get("order") != 13
        or manifest.get("parameter") != 3
        or type(manifest.get("seed")) is not int
        or int(manifest["seed"]) < 0
        or type(manifest.get("created_unix_ns")) is not int
        or int(manifest["created_unix_ns"]) <= 0
    ):
        raise ValueError("run manifest semantics differ")
    hardware = manifest.get("hardware")
    if (
        not isinstance(hardware, dict)
        or set(hardware)
        != {"machine", "logical_cpus", "physical_memory_bytes"}
        or not isinstance(hardware.get("machine"), str)
        or not hardware["machine"]
        or type(hardware.get("logical_cpus")) is not int
        or int(hardware["logical_cpus"]) <= 0
        or type(hardware.get("physical_memory_bytes")) is not int
        or int(hardware["physical_memory_bytes"]) <= 0
    ):
        raise ValueError("run hardware record differs")
    expected_resume = [
        "/usr/bin/env",
        "PYTHONPATH=src",
        sys.executable,
        "-m",
        "search.order13_k3.production",
        "run",
        "--run-directory",
        str(run_directory.resolve()),
        "--production-gate",
    ]
    expected_audit = [
        "/usr/bin/env",
        "PYTHONPATH=src",
        sys.executable,
        "-m",
        "search.order13_k3.production",
        "audit",
        "--run-directory",
        str(run_directory.resolve()),
    ]
    if (
        manifest.get("normalized_resume_invocation") != expected_resume
        or manifest.get("normalized_audit_invocation") != expected_audit
    ):
        raise ValueError("normalized production invocation differs")
    sources = manifest.get("runtime_sources")
    _verify_sources(sources)
    if (
        not isinstance(sources, dict)
        or manifest.get("runtime_source_set_sha256")
        != _source_set_hash(sources)
    ):
        raise ValueError("runtime source-set hash differs")
    _verify_production_toolchain(
        manifest.get("tools"),
        manifest.get("accepted_production_tool_sha256"),
        manifest.get("tool_identity"),
    )
    limits = manifest.get("limits")
    if not isinstance(limits, dict):
        raise ValueError("run limits are absent")
    _validate_limits(limits)
    template = str(manifest["template"])
    if manifest.get("expected_formula") != dict(EXPECTED_FORMULAS[template]):
        raise ValueError("expected formula census differs")
    constructor = manifest.get("constructor_artifacts")
    if not isinstance(constructor, dict) or set(constructor) != {
        INSTANCE_NAME,
        BANK_NAME,
        CONSTRUCTOR_MANIFEST_NAME,
    }:
        raise ValueError("constructor artifact bindings differ")
    for name, binding in constructor.items():
        expected_path = run_directory / name
        if not isinstance(binding, dict) or binding.get("path") != str(
            expected_path.resolve()
        ):
            raise ValueError("constructor artifact path differs")
        _verify_binding(binding, f"constructor artifact {name}")
    instance = _binding(run_directory / INSTANCE_NAME, "frozen instance")
    expected = EXPECTED_FORMULAS[template]
    if (
        instance["sha256"] != expected["sha256"]
        or instance["size_bytes"] != expected["size_bytes"]
    ):
        raise ValueError("frozen formula differs")
    if _regular(run_directory / LOCK_NAME, "run lock").st_size != 0:
        raise ValueError("run lock payload differs")
    latest, latest_hash = _audit_checkpoints(run_directory, manifest_hash)
    attempt_count = _audit_attempts(
        run_directory,
        manifest,
        manifest_hash,
        latest,
        allow_uncheckpointed_outcome=allow_uncheckpointed_outcome,
        allow_precheckpoint_orphan=allow_precheckpoint_orphan,
    )
    if attempt_count != latest["attempt_count"]:
        raise ValueError("audited attempt count differs from checkpoint")
    return manifest, manifest_hash, latest, latest_hash


def audit(run_directory: Path) -> dict[str, object]:
    manifest, manifest_hash, latest, latest_hash = _load_run(run_directory)
    return {
        "accepted": True,
        "template": manifest["template"],
        "run_manifest_sha256": manifest_hash,
        "latest_checkpoint_sha256": latest_hash,
        "status": latest["status"],
        "attempt_count": latest["attempt_count"],
        "proof_freshly_replayed": False,
        "claim_boundary": (
            "Structural and cryptographic audit only. This audit operation "
            "launches no child and does not freshly replay an LRAT proof."
        ),
    }


def _commands(
    manifest: Mapping[str, object],
    attempt: Path,
) -> dict[str, list[str]]:
    tools = manifest["tools"]
    limits = manifest["limits"]
    if not isinstance(tools, dict) or not isinstance(limits, dict):
        raise ValueError("manifest command bindings are malformed")

    def tool(role: str) -> str:
        record = tools[role]
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            raise ValueError(f"tool {role} binding differs")
        return str(record["path"])

    instance = str((attempt / INSTANCE_NAME).resolve())
    raw = str((attempt / "proof.raw.bdrat").resolve())
    normalized = str((attempt / "proof.normalized.rup.bdrat").resolve())
    lrat = str((attempt / "proof.converted.lrat").resolve())
    return {
        "solver": [
            tool("cadical"),
            f"--seed={manifest['seed']}",
            "--binary",
            "--no-colors",
            "-q",
            "-t",
            str(limits["solver_wall_seconds"]),
            "-w",
            str((attempt / "solver.result").resolve()),
            instance,
            raw,
        ],
        "raw_forward": [
            tool("drat_trim"),
            instance,
            raw,
            "-i",
            "-f",
            "-W",
            "-t",
            str(limits["postprocess_wall_seconds"]),
        ],
        "normalizer": [
            tool("normalizer_python"),
            str(
                (
                    campaign_root()
                    / "src/search/order13_k3/normalize_bdrat.py"
                ).resolve()
            ),
            "--input",
            raw,
            "--output",
            normalized,
            "--report",
            str((attempt / "normalization-report.json").resolve()),
            "--max-variable",
            "9802",
        ],
        "normalized_forward": [
            tool("drat_trim"),
            instance,
            normalized,
            "-i",
            "-f",
            "-W",
            "-U",
            "-t",
            str(limits["postprocess_wall_seconds"]),
        ],
        "lrat_conversion": [
            tool("drat_trim"),
            instance,
            normalized,
            "-i",
            "-W",
            "-U",
            "-L",
            lrat,
            "-t",
            str(limits["postprocess_wall_seconds"]),
        ],
        "lrat_check": [
            tool("lrat_check"),
            instance,
            lrat,
        ],
    }


def _resource_report(
    run_directory: Path,
    phase: str,
    memory_mib: int,
    limits: Mapping[str, object],
) -> dict[str, object]:
    errors: list[str] = []
    try:
        load = os.getloadavg()[0]
    except (AttributeError, OSError) as error:
        load = None
        errors.append(f"load probe: {type(error).__name__}")
    try:
        available = _available_memory_bytes()
    except (RuntimeError, ValueError, OSError) as error:
        available = None
        errors.append(f"memory probe: {type(error).__name__}")
    free_disk = shutil.disk_usage(run_directory).free
    required_memory = (
        memory_mib + int(limits["memory_reserve_mib"])
    ) << 20
    required_disk = (
        int(limits["disk_reserve_mib"])
        + LIVE_FILE_SLOTS * int(limits["file_limit_mib"])
        + DISK_METADATA_MIB
    ) << 20
    checks = {
        "load": load is not None and load <= float(limits["load_max"]),
        "memory": available is not None and available >= required_memory,
        "disk": free_disk >= required_disk,
    }
    return {
        "schema": "gamma-theta-order13-k3-resource-gate-v1",
        "phase": phase,
        "checked_unix_ns": time.time_ns(),
        "load_average_one_minute": load,
        "load_ceiling": limits["load_max"],
        "available_memory_bytes": available,
        "required_memory_bytes": required_memory,
        "free_disk_bytes": free_disk,
        "required_free_disk_bytes": required_disk,
        "live_file_slots": LIVE_FILE_SLOTS,
        "probe_errors": errors,
        "checks": checks,
        "passed": all(checks.values()) and not errors,
    }


def _verify_child(
    child: ChildResult,
    command: Sequence[str],
    *,
    stdout_path: Path | None = None,
    stderr_path: Path | None = None,
    wall_seconds: int | None = None,
    memory_mib: int | None = None,
    file_mib: int | None = None,
) -> None:
    if tuple(child.command) != tuple(command):
        raise ValueError("child command record differs")
    if child.command_sha256 != _command_sha256(command):
        raise ValueError("child command hash differs")
    executable = Path(command[0])
    if (
        child.executable_sha256_before != child.executable_sha256_after
        or child.executable_sha256_before != sha256_file(executable)
    ):
        raise ValueError("child executable hash differs")
    for path_raw, digest, role in (
        (child.stdout_path, child.stdout_sha256, "child stdout"),
        (child.stderr_path, child.stderr_sha256, "child stderr"),
    ):
        path = Path(path_raw)
        _regular(path, role)
        if sha256_file(path) != digest:
            raise ValueError(f"{role} hash differs")
    if (
        (stdout_path is not None and child.stdout_path != str(stdout_path.resolve()))
        or (stderr_path is not None and child.stderr_path != str(stderr_path.resolve()))
        or (wall_seconds is not None and child.wall_limit_seconds != wall_seconds)
        or (memory_mib is not None and child.memory_limit_mib != memory_mib)
        or (file_mib is not None and child.file_limit_mib != file_mib)
        or type(child.started_unix_ns) is not int
        or type(child.finished_unix_ns) is not int
        or child.started_unix_ns <= 0
        or child.finished_unix_ns < child.started_unix_ns
        or any(
            not math.isfinite(float(value)) or float(value) < 0
            for value in (
                child.wall_seconds,
                child.user_cpu_seconds,
                child.system_cpu_seconds,
                child.maximum_resident_set_size_mib,
                child.peak_polled_resident_set_size_mib,
            )
        )
        or type(child.maximum_resident_set_size_raw) is not int
        or child.maximum_resident_set_size_raw < 0
        or type(child.available_memory_before_bytes) is not int
        or child.available_memory_before_bytes <= 0
    ):
        raise ValueError("child resource record differs")


def _read_phase_record(
    attempt: Path,
    phase: str,
    *,
    readonly: Mapping[str, Path],
    produced: Mapping[str, Path],
) -> ChildResult:
    record = _read_canonical_json(
        attempt / f"child-{phase}.json", f"{phase} phase record"
    )
    if (
        set(record)
        != {
            "schema",
            "schema_version",
            "phase",
            "readonly_inputs_before",
            "readonly_inputs_after",
            "produced_outputs",
            "child",
        }
        or record.get("schema")
        != "gamma-theta-order13-k3-phase-record-v1"
        or record.get("schema_version") != 1
        or record.get("phase") != phase
    ):
        raise ValueError(f"{phase} phase record shape differs")
    expected_readonly = {
        role: _binding(path, f"{phase} recorded input {role}")
        for role, path in readonly.items()
    }
    expected_produced = {
        role: _optional_binding(path, f"{phase} recorded output {role}")
        for role, path in produced.items()
    }
    if (
        record.get("readonly_inputs_before") != expected_readonly
        or record.get("readonly_inputs_after") != expected_readonly
        or record.get("produced_outputs") != expected_produced
    ):
        raise ValueError(f"{phase} phase input/output bindings differ")
    child_record = record.get("child")
    if not isinstance(child_record, dict):
        raise ValueError(f"{phase} child record is absent")
    try:
        return ChildResult(**child_record)
    except TypeError as error:
        raise ValueError(f"{phase} child record shape differs") from error


def _child_failure(child: ChildResult, phase: str) -> str | None:
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


def _run_phase(
    *,
    run_directory: Path,
    attempt: Path,
    manifest: Mapping[str, object],
    phase: str,
    command: Sequence[str],
    readonly: Mapping[str, Path],
    produced: Mapping[str, Path],
    memory_mib: int,
    wall_seconds: int,
) -> ChildResult:
    limits = manifest["limits"]
    if not isinstance(limits, dict):
        raise ValueError("limits differ")
    _verify_production_toolchain(
        manifest.get("tools"),
        manifest.get("accepted_production_tool_sha256"),
        manifest.get("tool_identity"),
    )
    report = _resource_report(run_directory, phase, memory_mib, limits)
    _write_exclusive(
        attempt / f"resource-{phase}.json", canonical_json_bytes(report)
    )
    if report["passed"] is not True:
        raise PhaseFailure(
            "RESOURCE_GATE_FAILED_NONCLAIM",
            {"phase": phase, "resource_report": report},
        )
    _verify_sources(manifest["runtime_sources"])
    _verify_production_toolchain(
        manifest.get("tools"),
        manifest.get("accepted_production_tool_sha256"),
        manifest.get("tool_identity"),
    )
    readonly_bindings = {
        role: _binding(path, f"phase readonly {role}")
        for role, path in readonly.items()
    }
    stdout = attempt / f"{phase}.stdout"
    stderr = attempt / f"{phase}.stderr"
    child = run_bounded_child(
        command=command,
        cwd=campaign_root(),
        stdout_path=stdout,
        stderr_path=stderr,
        wall_limit_seconds=wall_seconds,
        memory_limit_mib=memory_mib,
        file_limit_mib=int(limits["file_limit_mib"]),
        readonly_paths=readonly,
    )
    _verify_child(
        child,
        command,
        stdout_path=stdout,
        stderr_path=stderr,
        wall_seconds=wall_seconds,
        memory_mib=memory_mib,
        file_mib=int(limits["file_limit_mib"]),
    )
    _verify_sources(manifest["runtime_sources"])
    _verify_production_toolchain(
        manifest.get("tools"),
        manifest.get("accepted_production_tool_sha256"),
        manifest.get("tool_identity"),
    )
    readonly_after_bindings = {
        role: _binding(path, f"phase readonly after {role}")
        for role, path in readonly.items()
    }
    for role, binding in readonly_bindings.items():
        if readonly_after_bindings[role] != binding:
            raise ValueError(f"phase readonly {role} changed during child")
    produced_bindings = {
        role: _optional_binding(path, f"phase output {role}")
        for role, path in produced.items()
    }
    _write_exclusive(
        attempt / f"child-{phase}.json",
        canonical_json_bytes(
            {
                "schema": "gamma-theta-order13-k3-phase-record-v1",
                "schema_version": 1,
                "phase": phase,
                "readonly_inputs_before": readonly_bindings,
                "readonly_inputs_after": readonly_after_bindings,
                "produced_outputs": produced_bindings,
                "child": asdict(child),
            }
        ),
    )
    failure = _child_failure(child, phase)
    if failure is not None:
        raise PhaseFailure(failure, {"phase": phase, "child": asdict(child)})
    return child


def _strict_verified(stdout: Path, stderr: Path, marker: str) -> None:
    if stderr.read_bytes():
        raise ValueError("verification tool wrote to stderr")
    try:
        text = stdout.read_text(encoding="ascii")
    except UnicodeDecodeError as error:
        raise ValueError("verification output is not ASCII") from error
    lines = [line.strip() for line in text.replace("\r", "\n").splitlines()]
    lines = [line for line in lines if line]
    lowered = "\n".join(lines).lower()
    if (
        lines.count(marker) != 1
        or "warning" in lowered
        or "error" in lowered
        or "not verified" in lowered
    ):
        raise ValueError(f"verification output lacks one clean {marker}")


def _scan_bdrat(path: Path, maximum_variable: int) -> dict[str, object]:
    _regular(path, "binary DRAT")
    counts = {
        "total": 0,
        "additions": 0,
        "deletions": 0,
        "literals": 0,
        "post_empty_deletions": 0,
    }
    empty: int | None = None
    maximum = 0
    addition_digest = hashlib.sha256()
    addition_size = 0
    with path.open("rb") as source:
        while True:
            prefix = source.read(1)
            if not prefix:
                break
            counts["total"] += 1
            if prefix not in {b"a", b"d"}:
                raise ValueError("binary DRAT prefix differs")
            addition = prefix == b"a"
            encoded_clause = bytearray()
            length = 0
            while True:
                encoded = bytearray()
                value = 0
                shift = 0
                while True:
                    raw = source.read(1)
                    if not raw or len(encoded) >= 10:
                        raise ValueError("binary DRAT varint differs")
                    encoded.append(raw[0])
                    value |= (raw[0] & 0x7F) << shift
                    if raw[0] < 0x80:
                        break
                    shift += 7
                canonical = bytearray()
                remainder = value
                while True:
                    byte = remainder & 0x7F
                    remainder >>= 7
                    canonical.append(byte | (0x80 if remainder else 0))
                    if not remainder:
                        break
                if encoded != canonical or value > 2 * maximum_variable + 1:
                    raise ValueError("binary DRAT varint is noncanonical")
                encoded_clause.extend(encoded)
                if value == 0:
                    break
                if value == 1 or not 1 <= value >> 1 <= maximum_variable:
                    raise ValueError("binary DRAT literal differs")
                maximum = max(maximum, value >> 1)
                length += 1
                counts["literals"] += 1
            if addition:
                counts["additions"] += 1
                if empty is not None:
                    raise ValueError("addition follows empty addition")
                payload = prefix + bytes(encoded_clause)
                addition_digest.update(payload)
                addition_size += len(payload)
                if length == 0:
                    empty = counts["total"]
            else:
                counts["deletions"] += 1
                if length == 0:
                    raise ValueError("empty deletion")
                if empty is not None:
                    counts["post_empty_deletions"] += 1
    if counts["total"] == 0 or empty is None:
        raise ValueError("binary DRAT has no unique empty addition")
    return {
        "counts": counts,
        "empty_record": empty,
        "maximum_variable": maximum,
        "addition_sha256": addition_digest.hexdigest(),
        "addition_size_bytes": addition_size,
    }


def _validate_normalization(
    report_path: Path,
    raw_path: Path,
    normalized_path: Path,
) -> None:
    report = _read_canonical_json(report_path, "normalization report")
    expected_report_keys = {
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
    }
    if (
        set(report) != expected_report_keys
        or report.get("schema") != NORMALIZATION_SCHEMA
        or report.get("schema_version") != 1
        or report.get("policy") != NORMALIZATION_POLICY
        or report.get("claim_status") != "TRANSFORMATION_ONLY_NO_PROOF_CLAIM"
        or report.get("max_variable_allowed") != 9802
    ):
        raise ValueError("normalization report semantics differ")
    input_binding = report.get("input")
    output_binding = report.get("output")
    if not isinstance(input_binding, dict) or not isinstance(output_binding, dict):
        raise ValueError("normalization bindings are absent")
    if input_binding != _binding(raw_path, "raw proof"):
        raise ValueError("normalization input binding differs")
    if output_binding != _binding(normalized_path, "normalized proof"):
        raise ValueError("normalization output binding differs")
    raw = _scan_bdrat(raw_path, 9802)
    normalized = _scan_bdrat(normalized_path, 9802)
    report_counts = report.get("record_counts")
    if (
        not isinstance(report_counts, dict)
        or set(report_counts)
        != {
            "total",
            "additions",
            "deletions",
            "literals",
            "post_empty_deletions",
        }
        or report_counts != raw["counts"]
        or report.get("empty_addition_record_index") != raw["empty_record"]
        or report.get("max_variable_observed") != raw["maximum_variable"]
        or raw["addition_sha256"] != output_binding["sha256"]
        or raw["addition_size_bytes"] != output_binding["size_bytes"]
        or normalized["counts"]["deletions"] != 0
        or normalized["counts"]["total"] != raw["counts"]["additions"]
        or normalized["empty_record"] != normalized["counts"]["total"]
    ):
        raise ValueError("normalized proof is not the exact addition stream")


def _optional_binding(path: Path, role: str) -> dict[str, object] | None:
    if not path.exists() and not path.is_symlink():
        return None
    return _binding(path, role)


def _execute(
    run_directory: Path,
    attempt: Path,
    manifest: Mapping[str, object],
    commands: Mapping[str, Sequence[str]],
) -> tuple[str, dict[str, object]]:
    limits = manifest["limits"]
    if not isinstance(limits, dict):
        raise ValueError("limits differ")
    instance = attempt / INSTANCE_NAME
    instance_binding = _binding(instance, "attempt instance")

    solver = _run_phase(
        run_directory=run_directory,
        attempt=attempt,
        manifest=manifest,
        phase="solver",
        command=commands["solver"],
        readonly={"instance": instance},
        produced={
            "solver_result": attempt / "solver.result",
            "raw_binary_drat": attempt / "proof.raw.bdrat",
        },
        memory_mib=int(limits["solver_memory_mib"]),
        wall_seconds=int(limits["solver_wall_seconds"]),
    )
    result_path = attempt / "solver.result"
    result_binding = _optional_binding(result_path, "solver result")
    raw_path = attempt / "proof.raw.bdrat"
    raw_binding = _optional_binding(raw_path, "raw binary DRAT proof")
    if result_binding is None:
        raise PhaseFailure(
            "SOLVER_INVALID_OUTPUT_NONCLAIM", {"reason": "result file absent"}
        )
    cnf = parse_dimacs_bytes(instance.read_bytes())
    try:
        parsed = parse_solver_result_bytes(result_path.read_bytes(), cnf.variable_count)
    except ValueError as error:
        raise PhaseFailure(
            "SOLVER_INVALID_OUTPUT_NONCLAIM", {"reason": str(error)}
        ) from error
    if parsed.status == "UNKNOWN":
        raise PhaseFailure("SOLVER_UNKNOWN_NONCLAIM", {})
    if parsed.status == "SAT":
        if solver.exit_code != 10 or parsed.model is None:
            raise PhaseFailure(
                "SOLVER_INVALID_OUTPUT_NONCLAIM",
                {"reason": "SAT status/exit/model disagreement"},
            )
        validate_model_satisfies_cnf(cnf, parsed.model)
        encoding = build_full_encoding(str(manifest["template"]))
        edges = encoding.decode_edges(parsed.model)
        family = encoding.decode_family(parsed.model)
        validate_decoded_candidate(str(manifest["template"]), edges, family)
        assignment = canonical_json_bytes(
            [
                variable if parsed.model[variable] else -variable
                for variable in range(1, cnf.variable_count + 1)
            ]
        )
        candidate = {
            "schema": "gamma-theta-order13-k3-sat-candidate-v1",
            "schema_version": 1,
            "status": SAT_CANDIDATE,
            "template": manifest["template"],
            "instance": instance_binding,
            "solver_result": result_binding,
            "assignment_sha256": hashlib.sha256(assignment).hexdigest(),
            "h_edges": [list(pair) for pair in edges],
            "eternal_family": [list(state) for state in family],
            "required_next_action": (
                "Freeze and run a standalone candidate verifier independent "
                "of this search and decoding core."
            ),
        }
        _write_exclusive(attempt / "candidate.json", canonical_json_bytes(candidate))
        return SAT_CANDIDATE, {"candidate": candidate}
    if parsed.status != "UNSAT" or solver.exit_code != 20:
        raise PhaseFailure(
            "SOLVER_INVALID_OUTPUT_NONCLAIM",
            {"reason": "UNSAT status and exit code disagree"},
        )
    if raw_binding is None or raw_binding["size_bytes"] == 0:
        raise PhaseFailure(
            "SOLVER_INVALID_OUTPUT_NONCLAIM",
            {"reason": "UNSAT has no nonempty raw proof"},
        )

    raw_forward = _run_phase(
        run_directory=run_directory,
        attempt=attempt,
        manifest=manifest,
        phase="raw_forward",
        command=commands["raw_forward"],
        readonly={"instance": instance, "raw proof": raw_path},
        produced={},
        memory_mib=int(limits["postprocess_memory_mib"]),
        wall_seconds=int(limits["postprocess_wall_seconds"]),
    )
    if raw_forward.exit_code != 0:
        raise PhaseFailure("RAW_FORWARD_REJECTED_NONCLAIM", {})
    try:
        _strict_verified(
            attempt / "raw_forward.stdout",
            attempt / "raw_forward.stderr",
            "s VERIFIED",
        )
    except ValueError as error:
        raise PhaseFailure(
            "RAW_FORWARD_REJECTED_NONCLAIM", {"reason": str(error)}
        ) from error

    normalizer = _run_phase(
        run_directory=run_directory,
        attempt=attempt,
        manifest=manifest,
        phase="normalizer",
        command=commands["normalizer"],
        readonly={
            "raw proof": raw_path,
            "normalizer source": campaign_root()
            / "src/search/order13_k3/normalize_bdrat.py",
        },
        produced={
            "normalized_binary_rup": attempt
            / "proof.normalized.rup.bdrat",
            "normalization_report": attempt / "normalization-report.json",
        },
        memory_mib=int(limits["postprocess_memory_mib"]),
        wall_seconds=int(limits["postprocess_wall_seconds"]),
    )
    normalized_path = attempt / "proof.normalized.rup.bdrat"
    normalization_report = attempt / "normalization-report.json"
    if normalizer.exit_code != 0:
        raise PhaseFailure("NORMALIZER_REJECTED_NONCLAIM", {})
    try:
        if (
            (attempt / "normalizer.stdout").read_bytes() != b"s NORMALIZED\n"
            or (attempt / "normalizer.stderr").read_bytes()
        ):
            raise ValueError("normalizer success marker differs")
        _validate_normalization(normalization_report, raw_path, normalized_path)
    except (ValueError, OSError) as error:
        raise PhaseFailure(
            "NORMALIZER_REJECTED_NONCLAIM", {"reason": str(error)}
        ) from error

    normalized_forward = _run_phase(
        run_directory=run_directory,
        attempt=attempt,
        manifest=manifest,
        phase="normalized_forward",
        command=commands["normalized_forward"],
        readonly={"instance": instance, "normalized proof": normalized_path},
        produced={},
        memory_mib=int(limits["postprocess_memory_mib"]),
        wall_seconds=int(limits["postprocess_wall_seconds"]),
    )
    if normalized_forward.exit_code != 0:
        raise PhaseFailure("NORMALIZED_FORWARD_REJECTED_NONCLAIM", {})
    try:
        _strict_verified(
            attempt / "normalized_forward.stdout",
            attempt / "normalized_forward.stderr",
            "s VERIFIED",
        )
    except ValueError as error:
        raise PhaseFailure(
            "NORMALIZED_FORWARD_REJECTED_NONCLAIM", {"reason": str(error)}
        ) from error

    conversion = _run_phase(
        run_directory=run_directory,
        attempt=attempt,
        manifest=manifest,
        phase="lrat_conversion",
        command=commands["lrat_conversion"],
        readonly={"instance": instance, "normalized proof": normalized_path},
        produced={"converted_lrat": attempt / "proof.converted.lrat"},
        memory_mib=int(limits["postprocess_memory_mib"]),
        wall_seconds=int(limits["postprocess_wall_seconds"]),
    )
    lrat_path = attempt / "proof.converted.lrat"
    lrat_binding = _optional_binding(lrat_path, "converted LRAT")
    if conversion.exit_code != 0 or lrat_binding is None or lrat_binding["size_bytes"] == 0:
        raise PhaseFailure("LRAT_CONVERSION_REJECTED_NONCLAIM", {})
    try:
        _strict_verified(
            attempt / "lrat_conversion.stdout",
            attempt / "lrat_conversion.stderr",
            "s VERIFIED",
        )
    except ValueError as error:
        raise PhaseFailure(
            "LRAT_CONVERSION_REJECTED_NONCLAIM", {"reason": str(error)}
        ) from error

    checker = _run_phase(
        run_directory=run_directory,
        attempt=attempt,
        manifest=manifest,
        phase="lrat_check",
        command=commands["lrat_check"],
        readonly={"instance": instance, "LRAT": lrat_path},
        produced={},
        memory_mib=int(limits["postprocess_memory_mib"]),
        wall_seconds=int(limits["postprocess_wall_seconds"]),
    )
    if checker.exit_code != 0:
        raise PhaseFailure("LRAT_CHECK_REJECTED_NONCLAIM", {})
    try:
        _strict_verified(
            attempt / "lrat_check.stdout",
            attempt / "lrat_check.stderr",
            "c VERIFIED",
        )
    except ValueError as error:
        raise PhaseFailure(
            "LRAT_CHECK_REJECTED_NONCLAIM", {"reason": str(error)}
        ) from error

    certificate = {
        "schema": "gamma-theta-order13-k3-template-lrat-certificate-v1",
        "schema_version": 1,
        "status": FINAL_SUCCESS,
        "proof_pipeline": PIPELINE,
        "template": manifest["template"],
        "seed": manifest["seed"],
        "run_manifest": _binding(
            run_directory / RUN_MANIFEST_NAME, "run manifest"
        ),
        "constructor_manifest": _binding(
            run_directory / CONSTRUCTOR_MANIFEST_NAME,
            "constructor manifest",
        ),
        "runtime_source_set_sha256": manifest["runtime_source_set_sha256"],
        "tools": manifest["tools"],
        "instance": instance_binding,
        "raw_binary_drat": _binding(raw_path, "raw binary DRAT"),
        "normalized_binary_rup": _binding(
            normalized_path, "normalized binary RUP"
        ),
        "normalization_report": _binding(
            normalization_report, "normalization report"
        ),
        "converted_lrat": lrat_binding,
        "lrat_check_tool": manifest["tools"]["lrat_check"],
        "claim_boundary": CERTIFICATE_CLAIM_BOUNDARY,
    }
    _write_exclusive(attempt / "certificate.json", canonical_json_bytes(certificate))
    return FINAL_SUCCESS, {"certificate": certificate}


def _attempt_artifacts(attempt: Path) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for path in sorted(attempt.iterdir()):
        if path.name == "outcome.json":
            continue
        if not path.is_file() or path.is_symlink():
            raise ValueError("attempt contains a non-regular artifact")
        result[path.name] = _binding(path, f"attempt artifact {path.name}")
    return result


def _append_checkpoint(
    run_directory: Path,
    *,
    manifest_hash: str,
    previous_hash: str,
    previous: Mapping[str, object],
    status: str,
    event: str,
    attempt_binding: Mapping[str, object],
    outcome_binding: Mapping[str, object] | None,
) -> tuple[dict[str, object], str]:
    sequence = int(previous["sequence"]) + 1
    checkpoint = {
        "schema": "gamma-theta-order13-k3-production-checkpoint-v1",
        "schema_version": SCHEMA_VERSION,
        "sequence": sequence,
        "previous_checkpoint_sha256": previous_hash,
        "run_manifest_sha256": manifest_hash,
        "status": status,
        "attempt_count": (
            int(previous["attempt_count"]) + 1
            if event == "RUN_STARTED"
            else int(previous["attempt_count"])
        ),
        "attempt": dict(attempt_binding),
        "outcome": None if outcome_binding is None else dict(outcome_binding),
        "event": event,
        "written_unix_ns": time.time_ns(),
    }
    path = (
        run_directory
        / CHECKPOINTS_NAME
        / f"checkpoint-{sequence:06d}.json"
    )
    _write_exclusive(path, canonical_json_bytes(checkpoint))
    return checkpoint, sha256_file(path)


def _recover_interrupted(
    run_directory: Path,
    manifest_hash: str,
    latest: Mapping[str, object],
    latest_hash: str,
) -> dict[str, object]:
    attempt_binding = latest.get("attempt")
    if not isinstance(attempt_binding, dict):
        raise ValueError("interrupted attempt binding is absent")
    config_path = _verify_binding(attempt_binding, "interrupted attempt config")
    attempt = config_path.parent
    outcome_path = attempt / "outcome.json"
    quarantine: dict[str, object] | None = None
    if outcome_path.exists() or outcome_path.is_symlink():
        quarantine = _quarantine_entry(
            run_directory,
            outcome_path,
            reason=(
                "An outcome existed without a terminal checkpoint. It was "
                "preserved intact outside the run tree and was not interpreted "
                "or promoted."
            ),
        )
    outcome = {
        "schema": "gamma-theta-order13-k3-attempt-outcome-v1",
        "schema_version": 1,
        "status": RECOVERED_OUTCOME_STATUS,
        "claim_status": OUTCOME_CLAIM_STATUS[RECOVERED_OUTCOME_STATUS],
        "reason": RECOVERY_REASON,
        "artifacts": _attempt_artifacts(attempt),
        "finished_unix_ns": time.time_ns(),
    }
    _write_exclusive(outcome_path, canonical_json_bytes(outcome))
    outcome_binding = _binding(outcome_path, "recovery outcome")
    checkpoint, checkpoint_hash = _append_checkpoint(
        run_directory,
        manifest_hash=manifest_hash,
        previous_hash=latest_hash,
        previous=latest,
        status="RETRYABLE_NONCLAIM",
        event="INTERRUPTED_RECOVERED",
        attempt_binding=attempt_binding,
        outcome_binding=outcome_binding,
    )
    return {
        "recovered": True,
        "status": checkpoint["status"],
        "checkpoint_sha256": checkpoint_hash,
        "uncheckpointed_outcome_quarantined": quarantine is not None,
        "durable_outcome_quarantined": quarantine is not None,
        "quarantine": quarantine,
        "child_launched": False,
    }


def run(
    run_directory: Path,
    *,
    production_gate: object,
    recover_interrupted: bool,
) -> dict[str, object]:
    if production_gate is not True:
        raise PermissionError("explicit proof-production gate is required")
    with RunLock(run_directory, create=False):
        manifest, manifest_hash, latest, latest_hash = _load_run(
            run_directory,
            allow_uncheckpointed_outcome=recover_interrupted,
            allow_precheckpoint_orphan=recover_interrupted,
        )
        precheckpoint_orphan = _attempt_directory(
            run_directory, int(latest["attempt_count"]) + 1
        )
        if precheckpoint_orphan.exists() or precheckpoint_orphan.is_symlink():
            if not recover_interrupted or latest["status"] not in RUNNABLE:
                raise RuntimeError(
                    "precheckpoint orphan attempt requires explicit recovery"
                )
            quarantine = _quarantine_entry(
                run_directory,
                precheckpoint_orphan,
                reason=(
                    "An attempt directory existed before its RUN_STARTED "
                    "checkpoint. It was preserved intact outside the run tree; "
                    "no child or outcome from it is trusted."
                ),
            )
            return {
                "recovered": True,
                "status": "RETRYABLE_NONCLAIM",
                "checkpoint_sha256": latest_hash,
                "precheckpoint_orphan_quarantined": True,
                "quarantine": quarantine,
                "child_launched": False,
            }
        if latest["status"] == "RUNNING_UNFINISHED_NONCLAIM":
            if not recover_interrupted:
                raise RuntimeError(
                    "interrupted attempt requires --recover-interrupted after "
                    "the operator verifies no child remains active"
                )
            return _recover_interrupted(
                run_directory, manifest_hash, latest, latest_hash
            )
        if recover_interrupted:
            raise RuntimeError("there is no interrupted attempt to recover")
        if latest["status"] in FROZEN:
            raise RuntimeError(f"run is frozen at {latest['status']}")
        if latest["status"] not in RUNNABLE:
            raise RuntimeError(f"run is not runnable: {latest['status']}")

        attempt_number = int(latest["attempt_count"]) + 1
        attempt = run_directory / ATTEMPTS_NAME / f"attempt-{attempt_number:06d}"
        os.mkdir(attempt, 0o700)
        shutil.copyfile(run_directory / INSTANCE_NAME, attempt / INSTANCE_NAME)
        with (attempt / INSTANCE_NAME).open("rb") as handle:
            os.fsync(handle.fileno())
        attempt_instance_binding = _binding(
            attempt / INSTANCE_NAME, "attempt instance"
        )
        constructor_artifacts = manifest.get("constructor_artifacts")
        frozen_instance = (
            constructor_artifacts.get(INSTANCE_NAME)
            if isinstance(constructor_artifacts, dict)
            else None
        )
        if not _same_bound_contents(
            attempt_instance_binding, frozen_instance
        ):
            raise ValueError("attempt instance differs from frozen formula")
        commands = _commands(manifest, attempt)
        config = {
            "schema": "gamma-theta-order13-k3-attempt-config-v1",
            "schema_version": 1,
            "claim_status": "NO_SAT_OR_UNSAT_CLAIM_BEFORE_EXECUTION",
            "proof_pipeline": PIPELINE,
            "attempt_number": attempt_number,
            "template": manifest["template"],
            "seed": manifest["seed"],
            "run_manifest_sha256": manifest_hash,
            "instance": attempt_instance_binding,
            "runtime_source_set_sha256": manifest["runtime_source_set_sha256"],
            "tools": manifest["tools"],
            "limits": manifest["limits"],
            "commands": commands,
            "created_unix_ns": time.time_ns(),
        }
        config_path = attempt / "attempt-config.json"
        _write_exclusive(config_path, canonical_json_bytes(config))
        config_binding = _binding(config_path, "attempt config")
        running, running_hash = _append_checkpoint(
            run_directory,
            manifest_hash=manifest_hash,
            previous_hash=latest_hash,
            previous=latest,
            status="RUNNING_UNFINISHED_NONCLAIM",
            event="RUN_STARTED",
            attempt_binding=config_binding,
            outcome_binding=None,
        )

        try:
            status, details = _execute(
                run_directory, attempt, manifest, commands
            )
        except PhaseFailure as error:
            status = "RETRYABLE_NONCLAIM"
            details = {
                "phase_status": error.status,
                "phase_details": error.details,
            }
        except BaseException as error:
            status = "RETRYABLE_NONCLAIM"
            details = {
                "phase_status": "ORCHESTRATOR_EXCEPTION_NONCLAIM",
                "exception_type": type(error).__name__,
                "exception_message": str(error),
            }
        outcome = {
            "schema": "gamma-theta-order13-k3-attempt-outcome-v1",
            "schema_version": 1,
            "status": status,
            "claim_status": OUTCOME_CLAIM_STATUS[status],
            "details": details,
            "artifacts": _attempt_artifacts(attempt),
            "finished_unix_ns": time.time_ns(),
        }
        outcome_path = attempt / "outcome.json"
        _write_exclusive(outcome_path, canonical_json_bytes(outcome))
        outcome_binding = _binding(outcome_path, "attempt outcome")
        final_checkpoint, final_hash = _append_checkpoint(
            run_directory,
            manifest_hash=manifest_hash,
            previous_hash=running_hash,
            previous=running,
            status=status,
            event="RUN_FINISHED",
            attempt_binding=config_binding,
            outcome_binding=outcome_binding,
        )
        return {
            "attempt_number": attempt_number,
            "status": final_checkpoint["status"],
            "outcome_sha256": outcome_binding["sha256"],
            "checkpoint_sha256": final_hash,
            "child_launched": (
                any(attempt.glob("child-*.json"))
                or any(attempt.glob("*.stdout"))
                or any(attempt.glob("*.stderr"))
            ),
        }


def _limits_from_arguments(arguments: argparse.Namespace) -> dict[str, object]:
    return {
        "solver_wall_seconds": arguments.solver_wall_seconds,
        "postprocess_wall_seconds": arguments.postprocess_wall_seconds,
        "solver_memory_mib": arguments.solver_memory_mib,
        "postprocess_memory_mib": arguments.postprocess_memory_mib,
        "file_limit_mib": arguments.file_limit_mib,
        "disk_reserve_mib": arguments.disk_reserve_mib,
        "memory_reserve_mib": arguments.memory_reserve_mib,
        "load_max": arguments.load_max,
        "parallel_children": 1,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)

    initialize_parser = commands.add_parser("initialize")
    initialize_parser.add_argument("--package-directory", type=Path, required=True)
    initialize_parser.add_argument("--run-directory", type=Path, required=True)
    initialize_parser.add_argument("--cadical", type=Path, required=True)
    initialize_parser.add_argument("--drat-trim", type=Path, required=True)
    initialize_parser.add_argument("--lrat-check", type=Path, required=True)
    initialize_parser.add_argument(
        "--normalizer-python", type=Path, default=Path(sys.executable)
    )
    initialize_parser.add_argument("--seed", type=int, default=0)
    initialize_parser.add_argument(
        "--solver-wall-seconds", type=int, default=DEFAULT_SOLVER_WALL_SECONDS
    )
    initialize_parser.add_argument(
        "--postprocess-wall-seconds",
        type=int,
        default=DEFAULT_POSTPROCESS_WALL_SECONDS,
    )
    initialize_parser.add_argument(
        "--solver-memory-mib", type=int, default=DEFAULT_MEMORY_MIB
    )
    initialize_parser.add_argument(
        "--postprocess-memory-mib", type=int, default=DEFAULT_MEMORY_MIB
    )
    initialize_parser.add_argument(
        "--file-limit-mib", type=int, default=DEFAULT_FILE_MIB
    )
    initialize_parser.add_argument(
        "--disk-reserve-mib", type=int, default=DEFAULT_DISK_RESERVE_MIB
    )
    initialize_parser.add_argument(
        "--memory-reserve-mib", type=int, default=DEFAULT_MEMORY_RESERVE_MIB
    )
    initialize_parser.add_argument("--load-max", type=float, default=DEFAULT_LOAD_MAX)
    initialize_parser.add_argument("--validation-gate", action="store_true")

    run_parser = commands.add_parser("run")
    run_parser.add_argument("--run-directory", type=Path, required=True)
    run_parser.add_argument("--production-gate", action="store_true")
    run_parser.add_argument("--recover-interrupted", action="store_true")

    audit_parser = commands.add_parser("audit")
    audit_parser.add_argument("--run-directory", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.command == "initialize":
        result = initialize(
            package_directory=arguments.package_directory,
            run_directory=arguments.run_directory,
            cadical_path=arguments.cadical,
            drat_trim_path=arguments.drat_trim,
            lrat_check_path=arguments.lrat_check,
            normalizer_python_path=arguments.normalizer_python,
            seed=arguments.seed,
            limits=_limits_from_arguments(arguments),
            validation_gate=arguments.validation_gate,
        )
    elif arguments.command == "run":
        result = run(
            arguments.run_directory,
            production_gate=arguments.production_gate,
            recover_interrupted=arguments.recover_interrupted,
        )
    elif arguments.command == "audit":
        result = audit(arguments.run_directory)
    else:
        raise AssertionError("unreachable command")
    print(json.dumps(result, allow_nan=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
