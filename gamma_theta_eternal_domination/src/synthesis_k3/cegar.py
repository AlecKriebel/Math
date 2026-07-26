"""Resumable proof-producing CEGAR for the order-12, parameter-three slice.

Importing this module never starts a search.  The command-line entry point
requires an explicit validation-gate flag and a positive iteration budget.
See ``math/synthesis_k3_cegar_protocol.md`` for the certificate boundary and
crash semantics.
"""

from __future__ import annotations

import argparse
import ctypes
import fcntl
import gzip
import hashlib
import json
import math
import os
import platform
import re
import resource
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .coloring import find_coloring
from .encoding import (
    N,
    TEMPLATES,
    K3Encoding,
    build_k3_encoding,
    same_color_cut,
    validate_decoded_candidate,
)
from .generate import generate, sha256_file


SCHEMA_VERSION = 2
CADICAL_VERSION = "3.0.1"
CADICAL_COMMIT = "c60730422e758ef1cebe7aeddf2dda31c996bf04"
CADICAL_ARCHIVE_SHA256 = (
    "2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e"
)
CADICAL_BINARY_SHA256 = (
    "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
)
DRAT_TRIM_COMMIT = "2e5e29cb0019d5cfd547d4208dca1b3ec290349f"
DRAT_TRIM_ARCHIVE_SHA256 = (
    "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108"
)
DRAT_TRIM_BINARY_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/synthesis_k3/__init__.py",
    "src/synthesis_k3/encoding.py",
    "src/synthesis_k3/coloring.py",
    "src/synthesis_k3/generate.py",
    "src/synthesis_k3/cegar.py",
    "math/synthesis_k3_cegar_design.md",
    "math/synthesis_k3_cegar_protocol.md",
)
CHECKPOINT_NAME = "checkpoint.json"
RUN_MANIFEST_NAME = "run_manifest.json"
CANDIDATE_MARKER_NAME = "candidate.freeze.json"
UNSAT_MARKER_NAME = "unsat.verified.json"
LOCK_NAME = "run.lock"
_INTEGER_TOKEN = re.compile(r"(?:0|[1-9][0-9]*|-[1-9][0-9]*)\Z")
_ACTIVE_CHILD_PID: int | None = None
_HEAVY_CHILD_LOCK_NAME = "gamma-theta-k3-heavy-child"
_ORCHESTRATOR_SIGNALS = (
    signal.SIGTERM,
    signal.SIGHUP,
    signal.SIGINT,
)


@dataclass(frozen=True, slots=True)
class ParsedCNF:
    variable_count: int
    clauses: tuple[tuple[int, ...], ...]


@dataclass(frozen=True, slots=True)
class ParsedSolverResult:
    status: str
    model: Mapping[int, bool] | None


@dataclass(slots=True)
class AuditInstrumentation:
    """Exact work counters for the linear-history audit regression."""

    attempt_semantic_validations: int = 0
    historical_sat_base_cnf_validations: int = 0
    historical_own_cut_validations: int = 0
    cut_ledger_record_validations: int = 0
    decisive_cnf_reconstructions: int = 0


@dataclass(frozen=True, slots=True)
class ToolBinding:
    role: str
    path: str
    sha256: str
    source_archive_path: str
    source_archive_sha256: str
    commit: str
    version: str | None


@dataclass(frozen=True, slots=True)
class RunConfiguration:
    template: str
    run_directory: str
    solver_seed: int
    solver_wall_seconds: int
    solver_memory_mib: int
    checker_wall_seconds: int
    checker_memory_mib: int
    session_wall_seconds: int
    disk_reserve_mib: int
    child_file_limit_mib: int
    retained_attempt_limit_mib: int
    physical_memory_bytes: int
    logical_cpu_count: int
    python_executable: str
    python_implementation: str
    python_version: str
    runtime_source_manifest: tuple[tuple[str, str], ...]
    runtime_source_set_sha256: str
    cadical: ToolBinding
    drat_trim: ToolBinding
    schema_version: int = SCHEMA_VERSION

    @property
    def digest(self) -> str:
        return sha256_bytes(canonical_json_bytes(asdict(self), pretty=False))


@dataclass(frozen=True, slots=True)
class ChildResult:
    command: tuple[str, ...]
    command_sha256: str
    executable_sha256_before: str
    executable_sha256_after: str
    exit_code: int
    termination_signal: int | None
    timed_out: bool
    memory_limit_exceeded: bool
    started_unix_ns: int
    finished_unix_ns: int
    wall_seconds: float
    user_cpu_seconds: float
    system_cpu_seconds: float
    maximum_resident_set_size_mib: float
    maximum_resident_set_size_raw: int
    maximum_resident_set_size_raw_unit: str
    peak_polled_resident_set_size_mib: float
    available_memory_before_bytes: int
    wall_limit_seconds: int
    memory_limit_mib: int
    file_limit_mib: int
    stdout_path: str
    stdout_sha256: str
    stderr_path: str
    stderr_sha256: str


@dataclass(frozen=True, slots=True)
class RunOutcome:
    status: str
    checkpoint_path: str
    checkpoint_sha256: str
    cut_count: int
    attempt_count: int
    terminal_path: str | None


def campaign_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json_bytes(payload: object, *, pretty: bool = True) -> bytes:
    if pretty:
        encoded = json.dumps(
            payload,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
    else:
        encoded = json.dumps(
            payload,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    return (encoded + "\n").encode("utf-8")


def _reject_constant(value: str) -> object:
    raise ValueError(f"non-finite JSON constant {value!r}")


def _object_without_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def strict_json_bytes(payload: bytes) -> object:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("JSON artifact is not UTF-8") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("malformed JSON artifact") from error


def strict_json_file(path: Path) -> object:
    return strict_json_bytes(path.read_bytes())


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


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


def _assert_regular_single_link(path: Path, role: str) -> None:
    _assert_no_symlink_components(path)
    try:
        information = os.lstat(path)
    except FileNotFoundError as error:
        raise ValueError(f"{role} is missing: {path}") from error
    if not stat.S_ISREG(information.st_mode):
        raise ValueError(f"{role} is not a regular file: {path}")
    if information.st_nlink != 1:
        raise ValueError(f"{role} has {information.st_nlink} hard links: {path}")


def _validate_existing_write_target(path: Path, role: str) -> None:
    _assert_no_symlink_components(path.parent)
    try:
        information = os.lstat(path)
    except FileNotFoundError:
        return
    if stat.S_ISLNK(information.st_mode):
        raise ValueError(f"{role} is a symbolic link: {path}")
    if not stat.S_ISREG(information.st_mode):
        raise ValueError(f"{role} is not a regular file: {path}")
    if information.st_nlink != 1:
        raise ValueError(f"{role} has {information.st_nlink} hard links: {path}")


def atomic_write(path: Path, payload: bytes) -> None:
    path = path.absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    _assert_no_symlink_components(path.parent)
    _validate_existing_write_target(path, "atomic write target")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".partial",
        dir=path.parent,
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
        _fsync_directory(path.parent)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def write_immutable(path: Path, payload: bytes) -> None:
    if path.exists() or path.is_symlink():
        _assert_regular_single_link(path, "immutable artifact")
        if path.read_bytes() != payload:
            raise RuntimeError(f"immutable artifact collision: {path}")
        return
    atomic_write(path, payload)


def _path_is_within(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
    except ValueError:
        return False
    return True


def validate_file_roles(
    *,
    readonly: Mapping[str, Path],
    writable: Mapping[str, Path],
) -> None:
    """Reject direct, symlink, and existing hard-link role collisions."""

    resolved_readonly: dict[str, Path] = {}
    for role, path in readonly.items():
        _assert_no_symlink_components(path)
        resolved = path.resolve(strict=True)
        _assert_regular_single_link(resolved, role)
        resolved_readonly[role] = resolved

    resolved_writable: dict[str, Path] = {}
    for role, path in writable.items():
        _assert_no_symlink_components(path.parent)
        _validate_existing_write_target(path, role)
        resolved_writable[role] = path.resolve(strict=False)

    writable_items = tuple(resolved_writable.items())
    for index, (first_role, first_path) in enumerate(writable_items):
        for second_role, second_path in writable_items[index + 1 :]:
            aliases = first_path == second_path
            if not aliases and first_path.exists() and second_path.exists():
                aliases = os.path.samefile(first_path, second_path)
            if aliases:
                raise ValueError(
                    f"writable roles alias: {first_role} and {second_role}"
                )

    for writable_role, writable_path in resolved_writable.items():
        for readonly_role, readonly_path in resolved_readonly.items():
            aliases = writable_path == readonly_path
            if not aliases and writable_path.exists():
                aliases = os.path.samefile(writable_path, readonly_path)
            if aliases:
                raise ValueError(
                    f"{writable_role} aliases readonly {readonly_role}"
                )


def _physical_memory_bytes() -> int:
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
    except (ValueError, OSError) as error:
        raise ValueError("cannot determine physical memory") from error
    if (
        type(pages) is not int
        or type(page_size) is not int
        or pages <= 0
        or page_size <= 0
    ):
        raise ValueError("invalid physical-memory report")
    return pages * page_size


class _DarwinVMStatistics64(ctypes.Structure):
    _fields_ = (
        ("free_count", ctypes.c_uint32),
        ("active_count", ctypes.c_uint32),
        ("inactive_count", ctypes.c_uint32),
        ("wire_count", ctypes.c_uint32),
        ("zero_fill_count", ctypes.c_uint64),
        ("reactivations", ctypes.c_uint64),
        ("pageins", ctypes.c_uint64),
        ("pageouts", ctypes.c_uint64),
        ("faults", ctypes.c_uint64),
        ("cow_faults", ctypes.c_uint64),
        ("lookups", ctypes.c_uint64),
        ("hits", ctypes.c_uint64),
        ("purges", ctypes.c_uint64),
        ("purgeable_count", ctypes.c_uint32),
        ("speculative_count", ctypes.c_uint32),
        ("decompressions", ctypes.c_uint64),
        ("compressions", ctypes.c_uint64),
        ("swapins", ctypes.c_uint64),
        ("swapouts", ctypes.c_uint64),
        ("compressor_page_count", ctypes.c_uint32),
        ("throttled_count", ctypes.c_uint32),
        ("external_page_count", ctypes.c_uint32),
        ("internal_page_count", ctypes.c_uint32),
        ("total_uncompressed_pages_in_compressor", ctypes.c_uint64),
    )


def _available_memory_bytes() -> int:
    """Return currently reclaimable memory without spawning a helper process."""

    if sys.platform == "darwin":
        library = ctypes.CDLL("/usr/lib/libSystem.B.dylib")
        mach_host_self = library.mach_host_self
        mach_host_self.restype = ctypes.c_uint32
        host_page_size = library.host_page_size
        host_page_size.argtypes = (ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32))
        host_page_size.restype = ctypes.c_int
        host_statistics64 = library.host_statistics64
        host_statistics64.argtypes = (
            ctypes.c_uint32,
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint32),
        )
        host_statistics64.restype = ctypes.c_int
        host = mach_host_self()
        page_size = ctypes.c_uint32()
        if host_page_size(host, ctypes.byref(page_size)) != 0:
            raise RuntimeError("host_page_size failed")
        statistics = _DarwinVMStatistics64()
        count = ctypes.c_uint32(
            ctypes.sizeof(statistics) // ctypes.sizeof(ctypes.c_int32)
        )
        if (
            host_statistics64(
                host,
                4,  # HOST_VM_INFO64
                ctypes.byref(statistics),
                ctypes.byref(count),
            )
            != 0
        ):
            raise RuntimeError("host_statistics64 failed")
        reclaimable_pages = (
            int(statistics.free_count)
            + int(statistics.inactive_count)
            + int(statistics.speculative_count)
            + int(statistics.purgeable_count)
        )
        return reclaimable_pages * int(page_size.value)
    if sys.platform.startswith("linux"):
        for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
            if line.startswith("MemAvailable:"):
                fields = line.split()
                if len(fields) == 3 and fields[2] == "kB":
                    return int(fields[1]) * 1024
        raise RuntimeError("MemAvailable is absent from /proc/meminfo")
    raise RuntimeError("current available-memory probe is unsupported")


def _current_memory_gate(memory_limit_mib: int) -> int:
    """Keep 512 MiB reclaimable beyond the requested child ceiling."""

    available = _available_memory_bytes()
    required = (memory_limit_mib + 512) << 20
    if available < required:
        raise RuntimeError(
            "current-memory gate failed: "
            f"{available} bytes reclaimable, {required} required"
        )
    return available


def runtime_source_manifest() -> tuple[tuple[str, str], ...]:
    root = campaign_root()
    records: list[tuple[str, str]] = []
    for relative in RUNTIME_SOURCE_RELATIVE_PATHS:
        source = root / relative
        _assert_regular_single_link(source, f"runtime source {relative}")
        records.append((relative, sha256_file(source)))
    return tuple(records)


def source_set_sha256(records: Sequence[tuple[str, str]]) -> str:
    payload = "".join(
        f"{relative} {digest}\n" for relative, digest in records
    ).encode("ascii")
    return sha256_bytes(payload)


def _tool_binding(
    *,
    role: str,
    binary: Path,
    expected_binary: Path,
    expected_binary_sha256: str,
    archive: Path,
    expected_archive_sha256: str,
    commit: str,
    version: str | None,
) -> ToolBinding:
    _assert_no_symlink_components(binary)
    resolved = binary.resolve(strict=True)
    if resolved != expected_binary.resolve(strict=True):
        raise ValueError(
            f"{role} must be the pinned campaign binary: {resolved}"
        )
    _assert_regular_single_link(resolved, role)
    if not os.access(resolved, os.X_OK):
        raise ValueError(f"{role} is not executable: {resolved}")
    binary_hash = sha256_file(resolved)
    if binary_hash != expected_binary_sha256:
        raise ValueError(
            f"{role} binary hash mismatch: {binary_hash} != "
            f"{expected_binary_sha256}"
        )
    _assert_regular_single_link(archive, f"{role} source archive")
    archive_hash = sha256_file(archive)
    if archive_hash != expected_archive_sha256:
        raise ValueError(
            f"{role} source archive hash mismatch: {archive_hash} != "
            f"{expected_archive_sha256}"
        )
    return ToolBinding(
        role=role,
        path=str(resolved),
        sha256=binary_hash,
        source_archive_path=str(archive.resolve()),
        source_archive_sha256=archive_hash,
        commit=commit,
        version=version,
    )


def verify_pinned_tools(
    cadical_path: Path,
    drat_trim_path: Path,
) -> tuple[ToolBinding, ToolBinding]:
    root = campaign_root()
    cadical = _tool_binding(
        role="cadical",
        binary=cadical_path,
        expected_binary=root / "tools/cadical_3_0_1/build/cadical",
        expected_binary_sha256=CADICAL_BINARY_SHA256,
        archive=root / "tools/cadical_3_0_1.tar.gz",
        expected_archive_sha256=CADICAL_ARCHIVE_SHA256,
        commit=CADICAL_COMMIT,
        version=CADICAL_VERSION,
    )
    drat_trim = _tool_binding(
        role="drat-trim",
        binary=drat_trim_path,
        expected_binary=root / "tools/drat_trim_2023_05_22/drat-trim",
        expected_binary_sha256=DRAT_TRIM_BINARY_SHA256,
        archive=root / "tools/drat_trim_2023_05_22.tar.gz",
        expected_archive_sha256=DRAT_TRIM_ARCHIVE_SHA256,
        commit=DRAT_TRIM_COMMIT,
        version=None,
    )
    return cadical, drat_trim


def _positive_exact_int(value: object, name: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive exact integer")
    return value


def _validate_run_directory_path(run_directory: Path) -> Path:
    _assert_no_symlink_components(run_directory)
    resolved = run_directory.resolve(strict=False)
    root = campaign_root().resolve()
    forbidden_exact = {
        root,
        Path(resolved.anchor),
        Path.home().resolve(),
    }
    if resolved in forbidden_exact:
        raise ValueError(f"unsafe run directory: {resolved}")
    for protected in (root / "src", root / "math", root / "tests", root / "tools"):
        if resolved == protected or _path_is_within(resolved, protected):
            raise ValueError(
                f"run directory lies in protected tree {protected}: {resolved}"
            )
        if _path_is_within(protected, resolved):
            raise ValueError(
                f"run directory contains protected tree {protected}: {resolved}"
            )
    if resolved.exists() and not resolved.is_dir():
        raise ValueError(f"run directory is not a directory: {resolved}")
    return resolved


def build_configuration(
    *,
    template: str,
    run_directory: Path,
    cadical_path: Path,
    drat_trim_path: Path,
    solver_seed: int,
    solver_wall_seconds: int,
    solver_memory_mib: int,
    checker_wall_seconds: int,
    checker_memory_mib: int,
    session_wall_seconds: int = 3600,
    disk_reserve_mib: int = 4096,
    child_file_limit_mib: int = 256,
    retained_attempt_limit_mib: int = 2,
) -> RunConfiguration:
    if template not in TEMPLATES:
        raise ValueError(f"unknown template {template!r}")
    if type(solver_seed) is not int or not 0 <= solver_seed <= 2_000_000_000:
        raise ValueError("solver seed must be an exact integer in [0, 2e9]")
    solver_wall_seconds = _positive_exact_int(
        solver_wall_seconds, "solver wall limit"
    )
    checker_wall_seconds = _positive_exact_int(
        checker_wall_seconds, "checker wall limit"
    )
    session_wall_seconds = _positive_exact_int(
        session_wall_seconds, "session wall limit"
    )
    solver_memory_mib = _positive_exact_int(
        solver_memory_mib, "solver memory limit"
    )
    checker_memory_mib = _positive_exact_int(
        checker_memory_mib, "checker memory limit"
    )
    disk_reserve_mib = _positive_exact_int(
        disk_reserve_mib, "disk reserve"
    )
    child_file_limit_mib = _positive_exact_int(
        child_file_limit_mib, "child file limit"
    )
    retained_attempt_limit_mib = _positive_exact_int(
        retained_attempt_limit_mib, "retained attempt limit"
    )
    if solver_memory_mib < 64 or checker_memory_mib < 64:
        raise ValueError("child memory limits must be at least 64 MiB")

    run_directory = _validate_run_directory_path(run_directory)
    physical_memory = _physical_memory_bytes()
    maximum_safe_mib = math.floor(physical_memory * 0.75 / (1 << 20))
    if solver_memory_mib > maximum_safe_mib:
        raise ValueError(
            f"solver memory limit exceeds 75% physical RAM ({maximum_safe_mib} MiB)"
        )
    if checker_memory_mib > maximum_safe_mib:
        raise ValueError(
            f"checker memory limit exceeds 75% physical RAM ({maximum_safe_mib} MiB)"
        )
    logical_cpus = os.cpu_count()
    if type(logical_cpus) is not int or logical_cpus < 1:
        raise ValueError("cannot determine logical CPU count")

    cadical, drat_trim = verify_pinned_tools(cadical_path, drat_trim_path)
    sources = runtime_source_manifest()
    return RunConfiguration(
        template=template,
        run_directory=str(run_directory),
        solver_seed=solver_seed,
        solver_wall_seconds=solver_wall_seconds,
        solver_memory_mib=solver_memory_mib,
        checker_wall_seconds=checker_wall_seconds,
        checker_memory_mib=checker_memory_mib,
        session_wall_seconds=session_wall_seconds,
        disk_reserve_mib=disk_reserve_mib,
        child_file_limit_mib=child_file_limit_mib,
        retained_attempt_limit_mib=retained_attempt_limit_mib,
        physical_memory_bytes=physical_memory,
        logical_cpu_count=logical_cpus,
        python_executable=str(Path(sys.executable).resolve()),
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
        runtime_source_manifest=sources,
        runtime_source_set_sha256=source_set_sha256(sources),
        cadical=cadical,
        drat_trim=drat_trim,
    )


def assert_configuration_bindings(configuration: RunConfiguration) -> None:
    if runtime_source_manifest() != configuration.runtime_source_manifest:
        raise RuntimeError("runtime source binding changed")
    if (
        source_set_sha256(configuration.runtime_source_manifest)
        != configuration.runtime_source_set_sha256
    ):
        raise RuntimeError("runtime source-set binding is inconsistent")
    for tool in (configuration.cadical, configuration.drat_trim):
        path = Path(tool.path)
        archive = Path(tool.source_archive_path)
        _assert_regular_single_link(path, tool.role)
        _assert_regular_single_link(archive, f"{tool.role} source archive")
        if sha256_file(path) != tool.sha256:
            raise RuntimeError(f"{tool.role} executable changed")
        if sha256_file(archive) != tool.source_archive_sha256:
            raise RuntimeError(f"{tool.role} source archive changed")


def disk_preflight(
    configuration: RunConfiguration,
    max_iterations: int,
) -> dict[str, int | bool]:
    """Refuse a session whose conservative artifact budget invades reserve."""

    max_iterations = _positive_exact_int(max_iterations, "iteration budget")
    usage = shutil.disk_usage(configuration.run_directory)
    mib = 1 << 20
    reserve_bytes = configuration.disk_reserve_mib * mib
    retained_session_bytes = (
        max_iterations * configuration.retained_attempt_limit_mib * mib
    )
    # One proof-producing solver may concurrently hold result, proof, stdout,
    # and stderr; the later checker may add stdout and stderr while those
    # solver artifacts remain. Each is bounded by RLIMIT_FSIZE.
    # At the UNSAT-certification peak, all three first-pass solver files
    # (result/stdout/stderr), all four proof-pass files
    # (result/proof/stdout/stderr), and both checker logs can coexist.
    terminal_workspace_bytes = (
        9 * configuration.child_file_limit_mib * mib
    )
    generation_workspace_bytes = 16 * mib
    required_free_bytes = (
        reserve_bytes
        + retained_session_bytes
        + terminal_workspace_bytes
        + generation_workspace_bytes
    )
    report: dict[str, int | bool] = {
        "available_free_bytes": usage.free,
        "disk_reserve_bytes": reserve_bytes,
        "iteration_budget": max_iterations,
        "retained_session_budget_bytes": retained_session_bytes,
        "terminal_workspace_budget_bytes": terminal_workspace_bytes,
        "generation_workspace_budget_bytes": generation_workspace_bytes,
        "required_free_bytes": required_free_bytes,
        "passed": usage.free >= required_free_bytes,
    }
    if not report["passed"]:
        raise RuntimeError(
            "disk preflight failed: "
            f"{usage.free} bytes free, {required_free_bytes} required "
            "by reserve and worst-case session budgets"
        )
    return report


def _normalized_resume_invocation(
    configuration: RunConfiguration,
    *,
    max_iterations: int = 1,
) -> list[str]:
    root = campaign_root()
    return [
        "/usr/bin/env",
        f"PYTHONPATH={root / 'src'}",
        configuration.python_executable,
        "-m",
        "synthesis_k3.cegar",
        "--validation-gate-open",
        "--template",
        configuration.template,
        "--run-dir",
        configuration.run_directory,
        "--max-iterations",
        str(_positive_exact_int(max_iterations, "iteration budget")),
        "--seed",
        str(configuration.solver_seed),
        "--solver-wall-seconds",
        str(configuration.solver_wall_seconds),
        "--solver-memory-mib",
        str(configuration.solver_memory_mib),
        "--checker-wall-seconds",
        str(configuration.checker_wall_seconds),
        "--checker-memory-mib",
        str(configuration.checker_memory_mib),
        "--session-wall-seconds",
        str(configuration.session_wall_seconds),
        "--disk-reserve-mib",
        str(configuration.disk_reserve_mib),
        "--child-file-limit-mib",
        str(configuration.child_file_limit_mib),
        "--retained-attempt-limit-mib",
        str(configuration.retained_attempt_limit_mib),
        "--cadical",
        configuration.cadical.path,
        "--drat-trim",
        configuration.drat_trim.path,
    ]


def _run_manifest_payload(configuration: RunConfiguration) -> dict[str, object]:
    return {
        "schema": "gamma-theta-k3-cegar-run-v2",
        "schema_version": SCHEMA_VERSION,
        "configuration": asdict(configuration),
        "configuration_sha256": configuration.digest,
        "working_directory": str(campaign_root()),
        "required_environment": {
            "PYTHONPATH": str(campaign_root() / "src"),
        },
        "normalized_resume_invocation": _normalized_resume_invocation(
            configuration
        ),
    }


class RunLock:
    def __init__(self, run_directory: Path, *, create: bool = True) -> None:
        self.path = run_directory / LOCK_NAME
        self.create = create
        self.descriptor: int | None = None

    def __enter__(self) -> "RunLock":
        if self.create:
            _validate_existing_write_target(self.path, "run lock")
        else:
            _assert_regular_single_link(self.path, "existing run lock")
        flags = os.O_RDWR if self.create else os.O_RDONLY
        if self.create:
            flags |= os.O_CREAT
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(self.path, flags, 0o600)
        information = os.fstat(descriptor)
        if not stat.S_ISREG(information.st_mode) or information.st_nlink != 1:
            os.close(descriptor)
            raise ValueError("run lock is not a single-link regular file")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(descriptor)
            raise RuntimeError("another orchestrator holds the run lock") from error
        self.descriptor = descriptor
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self.descriptor is None:
            raise RuntimeError("run lock exit without an acquired lock")
        fcntl.flock(self.descriptor, fcntl.LOCK_UN)
        os.close(self.descriptor)
        self.descriptor = None


def campaign_heavy_child_lock_path() -> Path:
    """Return the deterministic cross-process lock for this campaign checkout."""

    root_digest = sha256_bytes(str(campaign_root().resolve()).encode("utf-8"))[:20]
    temporary_root = Path(tempfile.gettempdir()).resolve()
    return temporary_root / f"{_HEAVY_CHILD_LOCK_NAME}-{root_digest}.lock"


class CampaignHeavyChildLock:
    """Serialize every solver/checker child across all template run folders."""

    def __init__(self) -> None:
        self.path = campaign_heavy_child_lock_path()
        self.descriptor: int | None = None

    def __enter__(self) -> "CampaignHeavyChildLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        _assert_no_symlink_components(self.path.parent)
        _validate_existing_write_target(self.path, "campaign heavy-child lock")
        flags = os.O_CREAT | os.O_RDWR
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(self.path, flags, 0o600)
        information = os.fstat(descriptor)
        if not stat.S_ISREG(information.st_mode) or information.st_nlink != 1:
            os.close(descriptor)
            raise ValueError(
                "campaign heavy-child lock is not a single-link regular file"
            )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(descriptor)
            raise RuntimeError(
                "another campaign solver/checker child is active"
            ) from error
        self.descriptor = descriptor
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self.descriptor is None:
            raise RuntimeError("heavy-child lock exit without acquisition")
        fcntl.flock(self.descriptor, fcntl.LOCK_UN)
        os.close(self.descriptor)
        self.descriptor = None


def canonical_coloring(raw: Sequence[int]) -> tuple[int, ...]:
    if len(raw) != N or any(
        type(color) is not int or color not in (0, 1, 2) for color in raw
    ):
        raise ValueError("coloring must contain 12 exact colors in {0,1,2}")
    relabel: dict[int, int] = {}
    canonical: list[int] = []
    for color in raw:
        if color not in relabel:
            relabel[color] = len(relabel)
        canonical.append(relabel[color])
    return tuple(canonical)


def coloring_bytes(coloring: Sequence[int]) -> bytes:
    canonical = canonical_coloring(coloring)
    return canonical_json_bytes(list(canonical), pretty=False)


def cuts_payload_bytes(cuts: Sequence[Mapping[str, object]]) -> bytes:
    rows = [record["coloring"] for record in cuts]
    return canonical_json_bytes(rows, pretty=False)


def cut_prefix_bindings(
    cuts: Sequence[Mapping[str, object]],
) -> tuple[tuple[str, int], ...]:
    """Hash every compact cut-list prefix in one streaming pass."""

    bindings: list[tuple[str, int]] = [
        (sha256_bytes(b"[]\n"), len(b"[]\n"))
    ]
    digest = hashlib.sha256()
    digest.update(b"[")
    payload_size = 1
    for index, record in enumerate(cuts):
        if not isinstance(record, Mapping):
            raise ValueError("cut prefix contains a non-object record")
        raw_coloring = record.get("coloring")
        if not isinstance(raw_coloring, list):
            raise ValueError("cut prefix coloring is not a list")
        row = canonical_json_bytes(raw_coloring, pretty=False)[:-1]
        if index:
            digest.update(b",")
            payload_size += 1
        digest.update(row)
        payload_size += len(row)
        closed = digest.copy()
        closed.update(b"]\n")
        bindings.append((closed.hexdigest(), payload_size + 2))
    return tuple(bindings)


def clause_bytes(clause: Sequence[int]) -> bytes:
    if not clause or any(type(literal) is not int or literal <= 0 for literal in clause):
        raise ValueError("a coloring cut must be a nonempty positive clause")
    return (" ".join(map(str, clause)) + "\n").encode("ascii")


def parse_dimacs_bytes(payload: bytes) -> ParsedCNF:
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError("DIMACS is not ASCII") from error
    if "\r" in text or not text.endswith("\n"):
        raise ValueError("DIMACS must use LF lines and end in LF")
    lines = text.splitlines()
    if not lines:
        raise ValueError("empty DIMACS")
    header = re.fullmatch(r"p cnf (0|[1-9][0-9]*) (0|[1-9][0-9]*)", lines[0])
    if header is None:
        raise ValueError("malformed DIMACS header")
    variable_count = int(header.group(1))
    declared_clauses = int(header.group(2))
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        if not line or line.startswith("c"):
            raise ValueError("unexpected DIMACS line")
        tokens = line.split(" ")
        if any(not token or _INTEGER_TOKEN.fullmatch(token) is None for token in tokens):
            raise ValueError("malformed DIMACS integer token")
        values = tuple(int(token) for token in tokens)
        if values[-1] != 0 or 0 in values[:-1]:
            raise ValueError("DIMACS clause is not terminated exactly once")
        clause = values[:-1]
        if any(abs(literal) > variable_count for literal in clause):
            raise ValueError("DIMACS literal exceeds declared variable count")
        if len(set(clause)) != len(clause):
            raise ValueError("DIMACS clause repeats a literal")
        if any(-literal in clause for literal in clause):
            raise ValueError("DIMACS clause is tautological")
        clauses.append(clause)
    if len(clauses) != declared_clauses:
        raise ValueError("DIMACS clause count does not match header")
    return ParsedCNF(variable_count, tuple(clauses))


def parse_dimacs_file(path: Path) -> ParsedCNF:
    _assert_regular_single_link(path, "DIMACS CNF")
    return parse_dimacs_bytes(path.read_bytes())


def parse_solver_result_bytes(
    payload: bytes,
    variable_count: int,
) -> ParsedSolverResult:
    if type(variable_count) is not int or variable_count < 0:
        raise ValueError("invalid model variable count")
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError("solver result is not ASCII") from error
    if "\r" in text or not text.endswith("\n"):
        raise ValueError("solver result must use LF lines and end in LF")
    lines = text.splitlines()
    if not lines:
        raise ValueError("empty solver result")
    status_by_line = {
        "s SATISFIABLE": "SAT",
        "s UNSATISFIABLE": "UNSAT",
        "s UNKNOWN": "UNKNOWN",
    }
    status = status_by_line.get(lines[0])
    if status is None:
        raise ValueError("solver result has an invalid status line")
    if any(line.startswith("s ") for line in lines[1:]):
        raise ValueError("solver result repeats its status")
    if status != "SAT":
        if len(lines) != 1:
            raise ValueError("non-SAT result contains model records")
        return ParsedSolverResult(status, None)

    if len(lines) == 1:
        raise ValueError("SAT result contains no model")
    literals: list[int] = []
    terminal_zero_seen = False
    for index, line in enumerate(lines[1:]):
        if not line.startswith("v "):
            raise ValueError("unexpected solver model record")
        tokens = line[2:].split(" ")
        if any(not token or _INTEGER_TOKEN.fullmatch(token) is None for token in tokens):
            raise ValueError("malformed model literal")
        values = tuple(int(token) for token in tokens)
        if 0 in values:
            if (
                terminal_zero_seen
                or values[-1] != 0
                or values.count(0) != 1
                or index != len(lines) - 2
            ):
                raise ValueError("model terminator is misplaced")
            terminal_zero_seen = True
            values = values[:-1]
        elif index == len(lines) - 2:
            raise ValueError("model has no final terminator")
        literals.extend(values)
    if not terminal_zero_seen:
        raise ValueError("model has no terminator")

    model: dict[int, bool] = {}
    for literal in literals:
        variable = abs(literal)
        if variable == 0 or variable > variable_count:
            raise ValueError("model literal is out of range")
        if variable in model:
            raise ValueError("model assigns a variable more than once")
        model[variable] = literal > 0
    if set(model) != set(range(1, variable_count + 1)):
        raise ValueError("model is not a complete assignment")
    return ParsedSolverResult("SAT", model)


def parse_solver_result_file(
    path: Path,
    variable_count: int,
) -> ParsedSolverResult:
    _assert_regular_single_link(path, "solver result")
    return parse_solver_result_bytes(path.read_bytes(), variable_count)


def validate_model_satisfies_cnf(
    cnf: ParsedCNF,
    model: Mapping[int, bool],
) -> None:
    if set(model) != set(range(1, cnf.variable_count + 1)):
        raise ValueError("model domain does not equal the DIMACS variables")
    for clause_index, clause in enumerate(cnf.clauses):
        if not any(
            model[abs(literal)] == (literal > 0) for literal in clause
        ):
            raise ValueError(f"model falsifies CNF clause {clause_index}")


def validate_model_satisfies_encoding_prefix(
    encoding: K3Encoding,
    cuts: Sequence[Mapping[str, object]],
    cut_count: int,
    model: Mapping[int, bool],
) -> None:
    """Forensic helper: evaluate one model against a complete cut prefix.

    Ordinary history audit deliberately does not call this once per attempt;
    doing so over growing prefixes would be quadratic.
    """

    if type(cut_count) is not int or not 0 <= cut_count <= len(cuts):
        raise ValueError("invalid model cut-prefix length")
    validate_model_satisfies_cnf(
        ParsedCNF(
            encoding.cnf.variable_count,
            tuple(encoding.cnf.clauses),
        ),
        model,
    )
    for cut_index, record in enumerate(cuts[:cut_count]):
        clause = record.get("clause")
        if (
            not isinstance(clause, list)
            or not clause
            or any(type(literal) is not int for literal in clause)
        ):
            raise ValueError("model cut-prefix clause is malformed")
        if not any(model[literal] for literal in clause):
            raise ValueError(
                f"model falsifies recorded coloring cut {cut_index}"
            )


def _expected_encoding(
    template: str,
    cuts: Sequence[Mapping[str, object]],
) -> K3Encoding:
    encoding = build_k3_encoding(template)
    for record in cuts:
        raw = record["coloring"]
        if not isinstance(raw, list):
            raise ValueError("checkpoint coloring is not a list")
        encoding.cnf.add_clause(same_color_cut(encoding, raw))
    return encoding


def validate_generated_cnf(
    *,
    template: str,
    cuts: Sequence[Mapping[str, object]],
    cnf_path: Path,
) -> tuple[K3Encoding, ParsedCNF]:
    parsed = parse_dimacs_file(cnf_path)
    encoding = _expected_encoding(template, cuts)
    if parsed.variable_count != encoding.cnf.variable_count:
        raise ValueError("generated DIMACS variable count is wrong")
    if parsed.clauses != tuple(encoding.cnf.clauses):
        raise ValueError("generated DIMACS clauses differ from reconstruction")
    return encoding, parsed


def _proper_coloring(
    edges: Iterable[tuple[int, int]],
    coloring: Sequence[int],
) -> None:
    canonical_coloring(coloring)
    edge_set = tuple(edges)
    for first, second in edge_set:
        if coloring[first] == coloring[second]:
            raise ValueError("coloring oracle returned a monochromatic H-edge")


def _decoded_candidate_payload(
    edges: Sequence[tuple[int, int]],
    family: Sequence[tuple[int, int, int]],
) -> dict[str, object]:
    h_edges = tuple(sorted(edges))
    h_edge_set = set(h_edges)
    g_edges = tuple(
        pair
        for pair in combinations(range(N), 2)
        if pair not in h_edge_set
    )
    return {
        "order": N,
        "h_is_complement_of_g": True,
        "h_edges": [list(pair) for pair in h_edges],
        "g_edges": [list(pair) for pair in g_edges],
        "eternal_family": [list(triple) for triple in sorted(family)],
    }


def _command_sha256(command: Sequence[str]) -> str:
    return sha256_bytes(canonical_json_bytes(list(command), pretty=False))


def _child_setup(
    memory_limit_bytes: int,
    cpu_limit_seconds: int,
    file_limit_bytes: int,
) -> None:
    os.setsid()
    if hasattr(signal, "pthread_sigmask"):
        signal.pthread_sigmask(signal.SIG_UNBLOCK, _ORCHESTRATOR_SIGNALS)
    if sys.platform != "darwin":
        resource.setrlimit(
            resource.RLIMIT_AS,
            (memory_limit_bytes, memory_limit_bytes),
        )
    resource.setrlimit(
        resource.RLIMIT_CPU,
        (cpu_limit_seconds, cpu_limit_seconds + 1),
    )
    resource.setrlimit(
        resource.RLIMIT_FSIZE,
        (file_limit_bytes, file_limit_bytes),
    )
    os.umask(0o077)


def _terminate_and_reap_process_group(pid: int) -> None:
    """Terminate a setsid child group and synchronously reap its leader."""

    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    deadline = time.perf_counter() + 0.5
    while time.perf_counter() < deadline:
        try:
            waited_pid, _, _ = os.wait4(pid, os.WNOHANG)
        except ChildProcessError:
            return
        if waited_pid == pid:
            return
        time.sleep(0.01)
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        os.wait4(pid, 0)
    except ChildProcessError:
        pass


def _orchestrator_signal_handler(signum: int, frame: object) -> None:
    """Fail closed: no solver/checker may outlive its orchestrator."""

    del frame
    global _ACTIVE_CHILD_PID
    pid = _ACTIVE_CHILD_PID
    if pid is not None:
        _terminate_and_reap_process_group(pid)
        _ACTIVE_CHILD_PID = None
    raise SystemExit(128 + signum)


def _maximum_rss_mib(raw: int) -> tuple[float, str]:
    if sys.platform == "darwin":
        return raw / (1 << 20), "bytes"
    return raw / 1024.0, "KiB"


class _DarwinProcTaskInfo(ctypes.Structure):
    _fields_ = (
        ("pti_virtual_size", ctypes.c_uint64),
        ("pti_resident_size", ctypes.c_uint64),
        ("pti_total_user", ctypes.c_uint64),
        ("pti_total_system", ctypes.c_uint64),
        ("pti_threads_user", ctypes.c_uint64),
        ("pti_threads_system", ctypes.c_uint64),
        ("pti_policy", ctypes.c_int32),
        ("pti_faults", ctypes.c_int32),
        ("pti_pageins", ctypes.c_int32),
        ("pti_cow_faults", ctypes.c_int32),
        ("pti_messages_sent", ctypes.c_int32),
        ("pti_messages_received", ctypes.c_int32),
        ("pti_syscalls_mach", ctypes.c_int32),
        ("pti_syscalls_unix", ctypes.c_int32),
        ("pti_csw", ctypes.c_int32),
        ("pti_threadnum", ctypes.c_int32),
        ("pti_numrunning", ctypes.c_int32),
        ("pti_priority", ctypes.c_int32),
    )


_DARWIN_PROC_PIDINFO = None


def _resident_set_size_bytes(pid: int) -> int | None:
    """Read child RSS without spawning a second process."""

    if sys.platform == "darwin":
        global _DARWIN_PROC_PIDINFO
        if _DARWIN_PROC_PIDINFO is None:
            library = ctypes.CDLL("/usr/lib/libproc.dylib")
            function = library.proc_pidinfo
            function.argtypes = (
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_uint64,
                ctypes.c_void_p,
                ctypes.c_int,
            )
            function.restype = ctypes.c_int
            _DARWIN_PROC_PIDINFO = function
        function = _DARWIN_PROC_PIDINFO
        information = _DarwinProcTaskInfo()
        returned = function(
            pid,
            4,  # PROC_PIDTASKINFO
            0,
            ctypes.byref(information),
            ctypes.sizeof(information),
        )
        if returned != ctypes.sizeof(information):
            return None
        return int(information.pti_resident_size)
    if sys.platform.startswith("linux"):
        try:
            lines = Path(f"/proc/{pid}/status").read_text(
                encoding="ascii"
            ).splitlines()
        except (FileNotFoundError, ProcessLookupError):
            return None
        for line in lines:
            if line.startswith("VmRSS:"):
                fields = line.split()
                if len(fields) == 3 and fields[2] == "kB":
                    return int(fields[1]) * 1024
        return None
    return None


def _run_bounded_child_with_campaign_lock(
    *,
    command: Sequence[str],
    cwd: Path,
    stdout_path: Path,
    stderr_path: Path,
    wall_limit_seconds: int,
    memory_limit_mib: int,
    file_limit_mib: int = 256,
    readonly_paths: Mapping[str, Path],
    available_memory_before_bytes: int,
) -> ChildResult:
    """Run one child with hard limits and exact wait4 resource accounting."""

    global _ACTIVE_CHILD_PID
    if _ACTIVE_CHILD_PID is not None:
        raise RuntimeError("a child process is already active")
    wall_limit_seconds = _positive_exact_int(
        wall_limit_seconds, "child wall limit"
    )
    memory_limit_mib = _positive_exact_int(
        memory_limit_mib, "child memory limit"
    )
    file_limit_mib = _positive_exact_int(
        file_limit_mib, "child file limit"
    )
    argv = tuple(str(value) for value in command)
    if not argv or any(not value for value in argv):
        raise ValueError("child command contains an empty argument")
    executable = Path(argv[0])
    if not executable.is_absolute():
        raise ValueError("child executable must be absolute")
    readonly = {"child executable": executable, **readonly_paths}
    validate_file_roles(
        readonly=readonly,
        writable={
            "child stdout": stdout_path,
            "child stderr": stderr_path,
        },
    )
    executable_hash_before = sha256_file(executable)
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    out_descriptor, out_temporary = tempfile.mkstemp(
        prefix=stdout_path.name + ".",
        suffix=".partial",
        dir=stdout_path.parent,
    )
    err_descriptor, err_temporary = tempfile.mkstemp(
        prefix=stderr_path.name + ".",
        suffix=".partial",
        dir=stderr_path.parent,
    )
    process: subprocess.Popen[bytes] | None = None
    started_unix_ns = time.time_ns()
    started = time.perf_counter()
    timed_out = False
    memory_limit_exceeded = False
    peak_polled_rss_bytes = 0
    usage = None
    wait_status = None
    previous_handlers: dict[int, object] = {}
    previous_signal_mask: set[signal.Signals] | None = None
    signals_unblocked = False
    if hasattr(signal, "pthread_sigmask"):
        previous_signal_mask = signal.pthread_sigmask(
            signal.SIG_BLOCK, _ORCHESTRATOR_SIGNALS
        )
    try:
        for handled_signal in _ORCHESTRATOR_SIGNALS:
            previous_handlers[handled_signal] = signal.getsignal(handled_signal)
            signal.signal(handled_signal, _orchestrator_signal_handler)
    except BaseException:
        if previous_signal_mask is not None:
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_signal_mask)
        raise
    try:
        with os.fdopen(out_descriptor, "wb") as stdout_handle, os.fdopen(
            err_descriptor, "wb"
        ) as stderr_handle:
            process = subprocess.Popen(
                argv,
                cwd=cwd,
                env={},
                stdin=subprocess.DEVNULL,
                stdout=stdout_handle,
                stderr=stderr_handle,
                close_fds=True,
                preexec_fn=lambda: _child_setup(
                    memory_limit_mib << 20,
                    wall_limit_seconds + 1,
                    file_limit_mib << 20,
                ),
            )
            _ACTIVE_CHILD_PID = process.pid
            if previous_signal_mask is not None:
                signal.pthread_sigmask(
                    signal.SIG_SETMASK, previous_signal_mask
                )
                signals_unblocked = True
            deadline = started + wall_limit_seconds
            while True:
                waited_pid, candidate_status, candidate_usage = os.wait4(
                    process.pid, os.WNOHANG
                )
                if waited_pid == process.pid:
                    wait_status = candidate_status
                    usage = candidate_usage
                    break
                resident = _resident_set_size_bytes(process.pid)
                if resident is not None:
                    peak_polled_rss_bytes = max(
                        peak_polled_rss_bytes, resident
                    )
                    if resident > (memory_limit_mib << 20):
                        memory_limit_exceeded = True
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        _, wait_status, usage = os.wait4(process.pid, 0)
                        break
                if time.perf_counter() >= deadline:
                    timed_out = True
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                    grace_deadline = time.perf_counter() + 0.5
                    while time.perf_counter() < grace_deadline:
                        waited_pid, candidate_status, candidate_usage = os.wait4(
                            process.pid, os.WNOHANG
                        )
                        if waited_pid == process.pid:
                            wait_status = candidate_status
                            usage = candidate_usage
                            break
                        time.sleep(0.02)
                    if wait_status is None:
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        _, wait_status, usage = os.wait4(process.pid, 0)
                    break
                time.sleep(0.02)
            if wait_status is None or usage is None:
                raise RuntimeError("child wait completed without resource status")
            process.returncode = os.waitstatus_to_exitcode(wait_status)
            _ACTIVE_CHILD_PID = None
            stdout_handle.flush()
            stderr_handle.flush()
            os.fsync(stdout_handle.fileno())
            os.fsync(stderr_handle.fileno())
        os.replace(out_temporary, stdout_path)
        os.replace(err_temporary, stderr_path)
        _fsync_directory(stdout_path.parent)
        if stderr_path.parent != stdout_path.parent:
            _fsync_directory(stderr_path.parent)
    except BaseException:
        if process is not None and process.returncode is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            try:
                _, wait_status, usage = os.wait4(process.pid, 0)
                process.returncode = os.waitstatus_to_exitcode(wait_status)
            except ChildProcessError:
                pass
        for temporary in (out_temporary, err_temporary):
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
        raise
    finally:
        _ACTIVE_CHILD_PID = None
        if previous_signal_mask is not None and signals_unblocked:
            signal.pthread_sigmask(signal.SIG_BLOCK, _ORCHESTRATOR_SIGNALS)
        for handled_signal, previous_handler in previous_handlers.items():
            signal.signal(handled_signal, previous_handler)
        if previous_signal_mask is not None:
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_signal_mask)

    finished = time.perf_counter()
    finished_unix_ns = time.time_ns()
    if process is None or process.returncode is None or usage is None:
        raise RuntimeError("child accounting is incomplete")
    executable_hash_after = sha256_file(executable)
    if executable_hash_after != executable_hash_before:
        raise RuntimeError("child executable changed during execution")
    maximum_rss, raw_unit = _maximum_rss_mib(int(usage.ru_maxrss))
    return ChildResult(
        command=argv,
        command_sha256=_command_sha256(argv),
        executable_sha256_before=executable_hash_before,
        executable_sha256_after=executable_hash_after,
        exit_code=process.returncode,
        termination_signal=(
            -process.returncode if process.returncode < 0 else None
        ),
        timed_out=timed_out,
        memory_limit_exceeded=memory_limit_exceeded,
        started_unix_ns=started_unix_ns,
        finished_unix_ns=finished_unix_ns,
        wall_seconds=finished - started,
        user_cpu_seconds=float(usage.ru_utime),
        system_cpu_seconds=float(usage.ru_stime),
        maximum_resident_set_size_mib=maximum_rss,
        maximum_resident_set_size_raw=int(usage.ru_maxrss),
        maximum_resident_set_size_raw_unit=raw_unit,
        peak_polled_resident_set_size_mib=(
            peak_polled_rss_bytes / (1 << 20)
        ),
        available_memory_before_bytes=available_memory_before_bytes,
        wall_limit_seconds=wall_limit_seconds,
        memory_limit_mib=memory_limit_mib,
        file_limit_mib=file_limit_mib,
        stdout_path=str(stdout_path.resolve()),
        stdout_sha256=sha256_file(stdout_path),
        stderr_path=str(stderr_path.resolve()),
        stderr_sha256=sha256_file(stderr_path),
    )


def run_bounded_child(
    *,
    command: Sequence[str],
    cwd: Path,
    stdout_path: Path,
    stderr_path: Path,
    wall_limit_seconds: int,
    memory_limit_mib: int,
    file_limit_mib: int = 256,
    readonly_paths: Mapping[str, Path],
) -> ChildResult:
    """Run one bounded child while holding the campaign-global heavy-job lock."""

    memory_limit_mib = _positive_exact_int(
        memory_limit_mib, "child memory limit"
    )
    with CampaignHeavyChildLock():
        available_memory = _current_memory_gate(memory_limit_mib)
        return _run_bounded_child_with_campaign_lock(
            command=command,
            cwd=cwd,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            wall_limit_seconds=wall_limit_seconds,
            memory_limit_mib=memory_limit_mib,
            file_limit_mib=file_limit_mib,
            readonly_paths=readonly_paths,
            available_memory_before_bytes=available_memory,
        )


def _solver_command(
    configuration: RunConfiguration,
    *,
    cnf_path: Path,
    result_path: Path,
    proof_path: Path | None = None,
) -> tuple[str, ...]:
    command = [
        configuration.cadical.path,
        f"--seed={configuration.solver_seed}",
        "--no-binary",
        "--no-colors",
        "-q",
        "-t",
        str(configuration.solver_wall_seconds),
        "-w",
        str(result_path.resolve()),
        str(cnf_path.resolve()),
    ]
    if proof_path is not None:
        command.append(str(proof_path.resolve()))
    return tuple(command)


def _checker_command(
    configuration: RunConfiguration,
    *,
    cnf_path: Path,
    proof_path: Path,
) -> tuple[str, ...]:
    return (
        configuration.drat_trim.path,
        str(cnf_path.resolve()),
        str(proof_path.resolve()),
        "-I",
        "-f",
        "-W",
        "-t",
        str(configuration.checker_wall_seconds),
    )


def _artifact_binding(path: Path, role: str) -> dict[str, object]:
    _assert_regular_single_link(path, role)
    return {
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _artifact_map(paths: Mapping[str, Path]) -> dict[str, dict[str, object]]:
    return {
        role: _artifact_binding(path, role)
        for role, path in sorted(paths.items())
    }


def _unlink_uncommitted_artifact(path: Path, role: str) -> None:
    _assert_regular_single_link(path, role)
    os.unlink(path)
    _fsync_directory(path.parent)


def _compress_artifact(path: Path, role: str) -> dict[str, object]:
    raw = path.read_bytes()
    raw_binding = _artifact_binding(path, role)
    compressed = gzip.compress(raw, compresslevel=9, mtime=0)
    compressed_path = path.with_name(path.name + ".gz")
    write_immutable(compressed_path, compressed)
    if gzip.decompress(compressed_path.read_bytes()) != raw:
        raise RuntimeError(f"gzip round trip failed for {role}")
    compressed_binding = _artifact_binding(
        compressed_path, f"compressed {role}"
    )
    _unlink_uncommitted_artifact(path, role)
    return {
        "format": "gzip",
        "raw_path": raw_binding["path"],
        "raw_sha256": raw_binding["sha256"],
        "raw_size_bytes": raw_binding["size_bytes"],
        "gzip_path": compressed_binding["path"],
        "gzip_sha256": compressed_binding["sha256"],
        "gzip_size_bytes": compressed_binding["size_bytes"],
    }


def _compact_intermediate_artifacts(
    *,
    artifacts: Mapping[str, Path],
    checkpoint: Mapping[str, object],
    configuration: RunConfiguration,
) -> tuple[
    dict[str, Path],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
    dict[str, object],
]:
    """Compact a nonterminal attempt before it becomes checkpoint-visible."""

    retained = dict(artifacts)
    cuts = checkpoint["cuts"]
    if not isinstance(cuts, list):
        raise ValueError("checkpoint cuts are not a list")
    cut_count = len(cuts)
    cut_prefix_hash = sha256_bytes(cuts_payload_bytes(cuts))
    cuts_path = retained.pop("cuts_input")
    cnf_path = retained.pop("cnf")
    cuts_binding = _artifact_binding(cuts_path, "cuts input")
    cnf_binding = _artifact_binding(cnf_path, "CNF")
    generator_path = retained["generator_manifest"]
    generator = strict_json_file(generator_path)
    if not isinstance(generator, dict):
        raise ValueError("generator manifest is not an object")
    if (
        generator.get("colorings_sha256") != cuts_binding["sha256"]
        or generator.get("cnf_sha256") != cnf_binding["sha256"]
        or generator.get("coloring_cut_count") != cut_count
    ):
        raise ValueError("generator manifest disagrees before compaction")
    reconstructible = {
        "cuts_input": {
            "kind": "cut_prefix",
            "raw_path": cuts_binding["path"],
            "raw_sha256": cuts_binding["sha256"],
            "raw_size_bytes": cuts_binding["size_bytes"],
            "cut_count": cut_count,
            "cut_prefix_sha256": cut_prefix_hash,
        },
        "cnf": {
            "kind": "generated_cnf",
            "raw_path": cnf_binding["path"],
            "raw_sha256": cnf_binding["sha256"],
            "raw_size_bytes": cnf_binding["size_bytes"],
            "cut_count": cut_count,
            "cut_prefix_sha256": cut_prefix_hash,
            "template": configuration.template,
            "generator_manifest_path": str(generator_path.resolve()),
            "generator_manifest_sha256": sha256_file(generator_path),
        },
    }
    _unlink_uncommitted_artifact(cuts_path, "cuts input")
    _unlink_uncommitted_artifact(cnf_path, "CNF")

    compressed: dict[str, dict[str, object]] = {}
    for role in ("solver_result", "solver_stdout", "solver_stderr"):
        path = retained.pop(role, None)
        if path is not None:
            compressed[role] = _compress_artifact(path, role)

    retained_bytes = sum(
        path.stat().st_size for path in retained.values()
    ) + sum(
        int(record["gzip_size_bytes"]) for record in compressed.values()
    )
    limit_bytes = configuration.retained_attempt_limit_mib << 20
    if retained_bytes > limit_bytes:
        raise RuntimeError(
            f"compacted attempt uses {retained_bytes} bytes, exceeding "
            f"the {limit_bytes}-byte retained-attempt limit"
        )
    storage = {
        "policy": "compact-intermediate-v1",
        "raw_cnf_and_cut_input_removed_after_validation": True,
        "compressed_roles": sorted(compressed),
        "reconstructible_roles": sorted(reconstructible),
        "retained_payload_bytes_before_attempt_manifest": retained_bytes,
        "retained_attempt_limit_bytes": limit_bytes,
    }
    return retained, compressed, reconstructible, storage


def _attempt_directory_size(path: Path) -> int:
    total = 0
    for candidate in path.iterdir():
        _assert_no_symlink_components(candidate)
        if candidate.is_file():
            _assert_regular_single_link(candidate, "attempt payload")
            total += candidate.stat().st_size
        elif candidate.is_dir():
            raise ValueError("nested attempt directories are forbidden")
        else:
            raise ValueError("non-file attempt artifact is forbidden")
    return total


def _verify_artifact_map(
    artifacts: object,
    run_directory: Path,
) -> None:
    if not isinstance(artifacts, dict):
        raise ValueError("attempt artifact map is not an object")
    for role, raw in artifacts.items():
        if type(role) is not str or not isinstance(raw, dict):
            raise ValueError("malformed attempt artifact record")
        if set(raw) != {"path", "sha256", "size_bytes"}:
            raise ValueError("attempt artifact record has unexpected keys")
        path_raw = raw["path"]
        digest = raw["sha256"]
        size = raw["size_bytes"]
        if (
            type(path_raw) is not str
            or type(digest) is not str
            or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            or type(size) is not int
            or size < 0
        ):
            raise ValueError("malformed attempt artifact binding")
        path = Path(path_raw)
        if not path.is_absolute() or not _path_is_within(path, run_directory):
            raise ValueError("attempt artifact escapes the run directory")
        _assert_regular_single_link(path, f"attempt artifact {role}")
        if path.stat().st_size != size or sha256_file(path) != digest:
            raise ValueError(f"attempt artifact binding failed for {role}")


_ATTEMPT_ROLE_BASENAMES = {
    "cuts_input": "cuts.json",
    "cnf": "instance.cnf",
    "generator_manifest": "generator.json",
    "solver_result": "solver.result",
    "solver_stdout": "solver.stdout",
    "solver_stderr": "solver.stderr",
    "decoded_candidate": "decoded-candidate.json",
    "coloring": "coloring.json",
    "proof_result": "proof.result",
    "drat_proof": "proof.drat",
    "proof_solver_stdout": "proof-solver.stdout",
    "proof_solver_stderr": "proof-solver.stderr",
    "checker_stdout": "checker.stdout",
    "checker_stderr": "checker.stderr",
}


def _validate_attempt_storage_layout(
    manifest: Mapping[str, object],
    attempt_directory: Path,
) -> None:
    """Enforce exact outcome-specific roles and one distinct path per role."""

    outcome = manifest.get("outcome")
    retained = manifest.get("artifacts")
    compressed = manifest.get("compressed_artifacts")
    reconstructible = manifest.get("reconstructible_artifacts")
    if not all(
        isinstance(mapping, dict)
        for mapping in (retained, compressed, reconstructible)
    ):
        raise ValueError("attempt storage maps are malformed")
    retained_roles = set(retained)  # type: ignore[arg-type]
    compressed_roles = set(compressed)  # type: ignore[arg-type]
    reconstructible_roles = set(reconstructible)  # type: ignore[arg-type]
    if outcome == "coloring_cut_committed":
        expected_retained = {
            "generator_manifest",
            "decoded_candidate",
            "coloring",
        }
        expected_compressed = {
            "solver_result",
            "solver_stdout",
            "solver_stderr",
        }
        expected_reconstructible = {"cuts_input", "cnf"}
    elif outcome == "candidate_review_pending":
        expected_retained = {
            "cuts_input",
            "cnf",
            "generator_manifest",
            "solver_result",
            "solver_stdout",
            "solver_stderr",
            "decoded_candidate",
        }
        expected_compressed = set()
        expected_reconstructible = set()
    elif outcome == "unsat_verified":
        expected_retained = {
            "cuts_input",
            "cnf",
            "generator_manifest",
            "solver_result",
            "solver_stdout",
            "solver_stderr",
            "proof_result",
            "drat_proof",
            "proof_solver_stdout",
            "proof_solver_stderr",
            "checker_stdout",
            "checker_stderr",
        }
        expected_compressed = set()
        expected_reconstructible = set()
    elif outcome == "solver_unknown":
        expected_retained = {"generator_manifest"}
        expected_compressed = {
            "solver_result",
            "solver_stdout",
            "solver_stderr",
        }
        expected_reconstructible = {"cuts_input", "cnf"}
    elif outcome in {"solver_timeout", "solver_memory_limit"}:
        expected_retained = {"generator_manifest"}
        expected_compressed = {"solver_stdout", "solver_stderr"}
        if "solver_result" in compressed_roles:
            expected_compressed.add("solver_result")
        expected_reconstructible = {"cuts_input", "cnf"}
    else:
        raise ValueError("attempt outcome has no storage layout")
    if (
        retained_roles != expected_retained
        or compressed_roles != expected_compressed
        or reconstructible_roles != expected_reconstructible
    ):
        raise ValueError("attempt artifact roles contradict its outcome")

    logical_paths: dict[Path, str] = {}
    existing_paths: dict[Path, str] = {}

    def bind(role: str, raw_path: object, *, existing: bool) -> None:
        if role not in _ATTEMPT_ROLE_BASENAMES or type(raw_path) is not str:
            raise ValueError("attempt artifact role/path is malformed")
        path = Path(raw_path)
        expected = (attempt_directory / _ATTEMPT_ROLE_BASENAMES[role]).resolve()
        if path != expected:
            raise ValueError(f"attempt artifact {role} has a noncanonical path")
        prior = logical_paths.get(path)
        if prior is not None and prior != role:
            raise ValueError(f"attempt artifact roles alias: {prior} and {role}")
        logical_paths[path] = role
        if existing:
            resolved = path.resolve(strict=True)
            prior_existing = existing_paths.get(resolved)
            if prior_existing is not None and prior_existing != role:
                raise ValueError(
                    f"attempt artifact files alias: {prior_existing} and {role}"
                )
            existing_paths[resolved] = role

    for role, record in retained.items():  # type: ignore[union-attr]
        bind(role, record.get("path"), existing=True)
    for role, record in compressed.items():  # type: ignore[union-attr]
        bind(role, record.get("raw_path"), existing=False)
        gzip_path = Path(str(record.get("gzip_path")))
        expected_gzip = (
            attempt_directory / (_ATTEMPT_ROLE_BASENAMES[role] + ".gz")
        ).resolve()
        if gzip_path != expected_gzip:
            raise ValueError(
                f"compressed attempt artifact {role} has a noncanonical path"
            )
        resolved_gzip = gzip_path.resolve(strict=True)
        if resolved_gzip in existing_paths:
            raise ValueError("compressed attempt artifacts alias")
        existing_paths[resolved_gzip] = f"{role}:gzip"
    for role, record in reconstructible.items():  # type: ignore[union-attr]
        bind(role, record.get("raw_path"), existing=False)


def _verify_compressed_artifacts(
    records: object,
    run_directory: Path,
) -> None:
    if not isinstance(records, dict):
        raise ValueError("compressed artifact map is not an object")
    expected_keys = {
        "format",
        "raw_path",
        "raw_sha256",
        "raw_size_bytes",
        "gzip_path",
        "gzip_sha256",
        "gzip_size_bytes",
    }
    for role, raw in records.items():
        if type(role) is not str or not isinstance(raw, dict):
            raise ValueError("malformed compressed artifact record")
        if set(raw) != expected_keys or raw["format"] != "gzip":
            raise ValueError("compressed artifact has an unexpected schema")
        raw_path = Path(str(raw["raw_path"]))
        gzip_path = Path(str(raw["gzip_path"]))
        if (
            not raw_path.is_absolute()
            or not gzip_path.is_absolute()
            or not _path_is_within(raw_path, run_directory)
            or not _path_is_within(gzip_path, run_directory)
            or raw_path.exists()
            or raw_path.is_symlink()
        ):
            raise ValueError("compressed artifact path discipline failed")
        if any(
            type(raw[key]) is not str
            or re.fullmatch(r"[0-9a-f]{64}", raw[key]) is None
            for key in ("raw_sha256", "gzip_sha256")
        ) or any(
            type(raw[key]) is not int or raw[key] < 0
            for key in ("raw_size_bytes", "gzip_size_bytes")
        ):
            raise ValueError("compressed artifact hashes/sizes are malformed")
        _assert_regular_single_link(gzip_path, f"compressed artifact {role}")
        compressed = gzip_path.read_bytes()
        if (
            len(compressed) != raw["gzip_size_bytes"]
            or sha256_bytes(compressed) != raw["gzip_sha256"]
        ):
            raise ValueError(f"compressed binding failed for {role}")
        try:
            expanded = gzip.decompress(compressed)
        except (gzip.BadGzipFile, EOFError) as error:
            raise ValueError(f"invalid gzip artifact for {role}") from error
        if (
            len(expanded) != raw["raw_size_bytes"]
            or sha256_bytes(expanded) != raw["raw_sha256"]
        ):
            raise ValueError(f"expanded binding failed for {role}")


def _verify_reconstructible_artifacts(
    records: object,
    *,
    run_directory: Path,
    configuration: RunConfiguration,
    cuts: Sequence[Mapping[str, object]],
    retained_artifacts: Mapping[str, object],
    deep_reconstruct: bool,
    prefix_bindings: Sequence[tuple[str, int]] | None = None,
) -> None:
    if not isinstance(records, dict):
        raise ValueError("reconstructible artifact map is not an object")
    if not records:
        return
    if set(records) != {"cuts_input", "cnf"}:
        raise ValueError("reconstructible artifact roles are incomplete")
    cuts_record = records["cuts_input"]
    cnf_record = records["cnf"]
    if not isinstance(cuts_record, dict) or set(cuts_record) != {
        "kind",
        "raw_path",
        "raw_sha256",
        "raw_size_bytes",
        "cut_count",
        "cut_prefix_sha256",
    }:
        raise ValueError("cut-prefix reconstruction record is malformed")
    if not isinstance(cnf_record, dict) or set(cnf_record) != {
        "kind",
        "raw_path",
        "raw_sha256",
        "raw_size_bytes",
        "cut_count",
        "cut_prefix_sha256",
        "template",
        "generator_manifest_path",
        "generator_manifest_sha256",
    }:
        raise ValueError("CNF reconstruction record is malformed")
    if cuts_record["kind"] != "cut_prefix" or cnf_record["kind"] != "generated_cnf":
        raise ValueError("unknown reconstruction recipe")
    cut_count = cuts_record["cut_count"]
    if (
        type(cut_count) is not int
        or not 0 <= cut_count <= len(cuts)
        or cnf_record["cut_count"] != cut_count
        or cnf_record["template"] != configuration.template
    ):
        raise ValueError("reconstruction cut count/template is invalid")
    if prefix_bindings is None:
        prefix_bytes = cuts_payload_bytes(cuts[:cut_count])
        prefix_hash = sha256_bytes(prefix_bytes)
        prefix_size = len(prefix_bytes)
    else:
        if len(prefix_bindings) != len(cuts) + 1:
            raise ValueError("cut-prefix binding table has the wrong length")
        prefix_hash, prefix_size = prefix_bindings[cut_count]
    if (
        cuts_record["cut_prefix_sha256"] != prefix_hash
        or cnf_record["cut_prefix_sha256"] != prefix_hash
        or cuts_record["raw_sha256"] != prefix_hash
        or cuts_record["raw_size_bytes"] != prefix_size
    ):
        raise ValueError("cut-prefix reconstruction hash mismatch")
    for record in (cuts_record, cnf_record):
        raw_path = Path(str(record["raw_path"]))
        if (
            not raw_path.is_absolute()
            or not _path_is_within(raw_path, run_directory)
            or raw_path.exists()
            or raw_path.is_symlink()
            or type(record["raw_sha256"]) is not str
            or re.fullmatch(r"[0-9a-f]{64}", record["raw_sha256"]) is None
            or type(record["raw_size_bytes"]) is not int
            or record["raw_size_bytes"] < 0
        ):
            raise ValueError("reconstructible raw artifact binding is malformed")
    generator_artifact = retained_artifacts.get("generator_manifest")
    if not isinstance(generator_artifact, dict):
        raise ValueError("reconstruction lacks its generator manifest")
    if (
        cnf_record["generator_manifest_path"] != generator_artifact.get("path")
        or cnf_record["generator_manifest_sha256"]
        != generator_artifact.get("sha256")
    ):
        raise ValueError("CNF recipe does not bind the generator manifest")
    generator = strict_json_file(
        Path(str(cnf_record["generator_manifest_path"]))
    )
    if not isinstance(generator, dict) or (
        generator.get("template") != configuration.template
        or generator.get("coloring_cut_count") != cut_count
        or generator.get("colorings_sha256") != prefix_hash
        or generator.get("cnf_sha256") != cnf_record["raw_sha256"]
        or generator.get("cnf_path") != cnf_record["raw_path"]
        or generator.get("colorings_path") != cuts_record["raw_path"]
    ):
        raise ValueError("generator manifest and reconstruction recipe disagree")
    if deep_reconstruct:
        encoding = _expected_encoding(
            configuration.template, cuts[:cut_count]
        )
        reconstructed = encoding.cnf.dimacs().encode("ascii")
        if (
            len(reconstructed) != cnf_record["raw_size_bytes"]
            or sha256_bytes(reconstructed) != cnf_record["raw_sha256"]
        ):
            raise ValueError("deep CNF reconstruction failed")


def _lookup_raw_artifact(
    role: str,
    retained: Mapping[str, object],
    compressed: Mapping[str, object],
    reconstructible: Mapping[str, object],
) -> Mapping[str, object] | None:
    raw = retained.get(role)
    if isinstance(raw, dict):
        return {
            "path": raw.get("path"),
            "sha256": raw.get("sha256"),
        }
    raw = compressed.get(role)
    if isinstance(raw, dict):
        return {
            "path": raw.get("raw_path"),
            "sha256": raw.get("raw_sha256"),
        }
    raw = reconstructible.get(role)
    if isinstance(raw, dict):
        return {
            "path": raw.get("raw_path"),
            "sha256": raw.get("raw_sha256"),
        }
    return None


def _verify_child_record(
    record: object,
    *,
    expected_executable: ToolBinding,
    artifacts: Mapping[str, object],
    compressed_artifacts: Mapping[str, object],
    reconstructible_artifacts: Mapping[str, object],
    stdout_role: str,
    stderr_role: str,
    expected_wall_limit_seconds: int,
    expected_memory_limit_mib: int,
    expected_file_limit_mib: int,
) -> None:
    if not isinstance(record, dict) or set(record) != set(
        ChildResult.__dataclass_fields__
    ):
        raise ValueError("child resource record has an unexpected schema")
    command = record["command"]
    if (
        not isinstance(command, list)
        or not command
        or any(type(argument) is not str or not argument for argument in command)
        or command[0] != expected_executable.path
    ):
        raise ValueError("child command does not use the bound executable")
    if record["command_sha256"] != _command_sha256(command):
        raise ValueError("child command hash mismatch")
    if (
        record["executable_sha256_before"] != expected_executable.sha256
        or record["executable_sha256_after"] != expected_executable.sha256
    ):
        raise ValueError("child executable hash record is inconsistent")
    for role, path_key, hash_key in (
        (stdout_role, "stdout_path", "stdout_sha256"),
        (stderr_role, "stderr_path", "stderr_sha256"),
    ):
        artifact = _lookup_raw_artifact(
            role,
            artifacts,
            compressed_artifacts,
            reconstructible_artifacts,
        )
        if not isinstance(artifact, dict):
            raise ValueError(f"child log artifact {role} is missing")
        if (
            record[path_key] != artifact.get("path")
            or record[hash_key] != artifact.get("sha256")
        ):
            raise ValueError(f"child log binding disagrees for {role}")
    numeric_nonnegative = (
        "wall_seconds",
        "user_cpu_seconds",
        "system_cpu_seconds",
        "maximum_resident_set_size_mib",
        "peak_polled_resident_set_size_mib",
    )
    if any(
        isinstance(record[key], bool)
        or not isinstance(record[key], (int, float))
        or not math.isfinite(record[key])
        or record[key] < 0
        for key in numeric_nonnegative
    ):
        raise ValueError("child resource accounting is malformed")
    if (
        type(record["exit_code"]) is not int
        or (
            record["termination_signal"] is not None
            and type(record["termination_signal"]) is not int
        )
        or type(record["timed_out"]) is not bool
        or type(record["memory_limit_exceeded"]) is not bool
        or type(record["started_unix_ns"]) is not int
        or type(record["finished_unix_ns"]) is not int
        or type(record["maximum_resident_set_size_raw"]) is not int
        or type(record["maximum_resident_set_size_raw_unit"]) is not str
        or type(record["available_memory_before_bytes"]) is not int
        or type(record["wall_limit_seconds"]) is not int
        or type(record["memory_limit_mib"]) is not int
        or type(record["file_limit_mib"]) is not int
    ):
        raise ValueError("child status/limit accounting is malformed")
    expected_signal = (
        -record["exit_code"] if record["exit_code"] < 0 else None
    )
    expected_raw_unit = "bytes" if sys.platform == "darwin" else "KiB"
    if (
        record["termination_signal"] != expected_signal
        or record["timed_out"] and record["memory_limit_exceeded"]
        or record["started_unix_ns"] < 0
        or record["finished_unix_ns"] < record["started_unix_ns"]
        or record["maximum_resident_set_size_raw"] < 0
        or record["maximum_resident_set_size_raw_unit"] != expected_raw_unit
        or record["available_memory_before_bytes"]
        < (expected_memory_limit_mib + 512) << 20
        or record["wall_limit_seconds"] != expected_wall_limit_seconds
        or record["memory_limit_mib"] != expected_memory_limit_mib
        or record["file_limit_mib"] != expected_file_limit_mib
    ):
        raise ValueError("child status/limits contradict the run configuration")


def _verify_orchestrator_session(
    record: object,
    configuration: RunConfiguration,
) -> None:
    if not isinstance(record, dict) or set(record) != {
        "command",
        "command_sha256",
    }:
        raise ValueError("orchestrator session command is malformed")
    command = record["command"]
    if (
        not isinstance(command, list)
        or record["command_sha256"] != _command_sha256(command)
    ):
        raise ValueError("orchestrator session command hash mismatch")
    try:
        budget_index = command.index("--max-iterations") + 1
        budget = int(command[budget_index])
    except (ValueError, IndexError) as error:
        raise ValueError("orchestrator session lacks its iteration budget") from error
    if command != _normalized_resume_invocation(
        configuration, max_iterations=budget
    ):
        raise ValueError("orchestrator session command is not canonical")


def _verify_attempt_commands(
    manifest: Mapping[str, object],
    configuration: RunConfiguration,
    attempt_directory: Path,
) -> None:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValueError("attempt artifacts are missing")
    compressed = manifest.get("compressed_artifacts")
    reconstructible = manifest.get("reconstructible_artifacts")
    if not isinstance(compressed, dict) or not isinstance(reconstructible, dict):
        raise ValueError("attempt storage maps are missing")
    _verify_orchestrator_session(
        manifest.get("orchestrator_session"), configuration
    )
    _verify_child_record(
        manifest.get("initial_solver"),
        expected_executable=configuration.cadical,
        artifacts=artifacts,
        compressed_artifacts=compressed,
        reconstructible_artifacts=reconstructible,
        stdout_role="solver_stdout",
        stderr_role="solver_stderr",
        expected_wall_limit_seconds=configuration.solver_wall_seconds,
        expected_memory_limit_mib=configuration.solver_memory_mib,
        expected_file_limit_mib=configuration.child_file_limit_mib,
    )
    initial_command = manifest["initial_solver"]["command"]  # type: ignore[index]
    cnf_artifact = _lookup_raw_artifact(
        "cnf", artifacts, compressed, reconstructible
    )
    if not isinstance(cnf_artifact, dict):
        raise ValueError("initial solver command lacks its CNF")
    expected_initial_command = list(
        _solver_command(
            configuration,
            cnf_path=Path(str(cnf_artifact["path"])),
            result_path=attempt_directory / "solver.result",
        )
    )
    if initial_command != expected_initial_command:
        raise ValueError("initial solver command is not exact")
    if manifest.get("outcome") == "unsat_verified":
        _verify_child_record(
            manifest.get("proof_solver"),
            expected_executable=configuration.cadical,
            artifacts=artifacts,
            compressed_artifacts=compressed,
            reconstructible_artifacts=reconstructible,
            stdout_role="proof_solver_stdout",
            stderr_role="proof_solver_stderr",
            expected_wall_limit_seconds=configuration.solver_wall_seconds,
            expected_memory_limit_mib=configuration.solver_memory_mib,
            expected_file_limit_mib=configuration.child_file_limit_mib,
        )
        _verify_child_record(
            manifest.get("proof_checker"),
            expected_executable=configuration.drat_trim,
            artifacts=artifacts,
            compressed_artifacts=compressed,
            reconstructible_artifacts=reconstructible,
            stdout_role="checker_stdout",
            stderr_role="checker_stderr",
            expected_wall_limit_seconds=configuration.checker_wall_seconds,
            expected_memory_limit_mib=configuration.checker_memory_mib,
            expected_file_limit_mib=configuration.child_file_limit_mib,
        )
        proof_command = manifest["proof_solver"]["command"]  # type: ignore[index]
        checker_command = manifest["proof_checker"]["command"]  # type: ignore[index]
        proof_artifact = _lookup_raw_artifact(
            "drat_proof", artifacts, compressed, reconstructible
        )
        if not isinstance(proof_artifact, dict):
            raise ValueError("proof command lacks its proof artifact")
        expected_proof_command = list(
            _solver_command(
                configuration,
                cnf_path=Path(str(cnf_artifact["path"])),
                result_path=attempt_directory / "proof.result",
                proof_path=Path(str(proof_artifact["path"])),
            )
        )
        expected_checker_command = list(
            _checker_command(
                configuration,
                cnf_path=Path(str(cnf_artifact["path"])),
                proof_path=Path(str(proof_artifact["path"])),
            )
        )
        if (
            proof_command != expected_proof_command
            or checker_command != expected_checker_command
        ):
            raise ValueError("proof/checker commands are not exact")


def _expected_attempt_manifest_keys(outcome: str) -> set[str]:
    keys = {
        "schema",
        "schema_version",
        "attempt_index",
        "outcome",
        "configuration_sha256",
        "run_manifest_sha256",
        "checkpoint_before_sha256",
        "history_chain_before_sha256",
        "cut_count_before",
        "artifacts",
        "compressed_artifacts",
        "reconstructible_artifacts",
        "storage",
        "disk_preflight",
        "orchestrator_session",
        "initial_solver",
    }
    if outcome in {
        "coloring_cut_committed",
        "candidate_review_pending",
        "unsat_verified",
    }:
        keys.add("validation")
    if outcome == "coloring_cut_committed":
        keys.add("committed_cut")
    if outcome == "unsat_verified":
        keys.update(("proof_solver", "proof_checker"))
    return keys


def _bound_artifact_bytes(
    manifest: Mapping[str, object],
    role: str,
) -> bytes:
    retained = manifest["artifacts"]
    compressed = manifest["compressed_artifacts"]
    if not isinstance(retained, dict) or not isinstance(compressed, dict):
        raise ValueError("attempt artifact maps are malformed")
    raw = retained.get(role)
    if isinstance(raw, dict):
        return Path(str(raw["path"])).read_bytes()
    packed = compressed.get(role)
    if isinstance(packed, dict):
        try:
            return gzip.decompress(Path(str(packed["gzip_path"])).read_bytes())
        except (gzip.BadGzipFile, EOFError) as error:
            raise ValueError(f"invalid compressed artifact {role}") from error
    raise ValueError(f"attempt lacks raw bytes for {role}")


def _validate_decoded_payload(
    payload: object,
    *,
    expected_edges: Sequence[tuple[int, int]],
    expected_family: Sequence[tuple[int, int, int]],
) -> None:
    expected = _decoded_candidate_payload(expected_edges, expected_family)
    if payload != expected:
        raise ValueError("decoded candidate artifact contradicts the SAT model")


def _validate_attempt_semantics(
    manifest: Mapping[str, object],
    *,
    configuration: RunConfiguration,
    encoding: K3Encoding,
    cuts: Sequence[Mapping[str, object]],
    base_cnf: ParsedCNF | None = None,
    instrumentation: AuditInstrumentation | None = None,
) -> None:
    """Derive each recorded outcome from its bound raw mathematical artifacts."""

    if instrumentation is not None:
        instrumentation.attempt_semantic_validations += 1
    outcome = manifest["outcome"]
    cut_count = manifest["cut_count_before"]
    if type(cut_count) is not int or not 0 <= cut_count <= len(cuts):
        raise ValueError("attempt cut count is invalid")
    initial = manifest["initial_solver"]
    if not isinstance(initial, dict):
        raise ValueError("attempt lacks its initial child record")
    flags_clear = (
        initial["timed_out"] is False
        and initial["memory_limit_exceeded"] is False
    )
    result: ParsedSolverResult | None = None
    if outcome not in {"solver_timeout", "solver_memory_limit"}:
        result = parse_solver_result_bytes(
            _bound_artifact_bytes(manifest, "solver_result"),
            encoding.cnf.variable_count,
        )

    if outcome == "solver_timeout":
        if initial["timed_out"] is not True or initial["memory_limit_exceeded"]:
            raise ValueError("timeout outcome contradicts child status")
        return
    if outcome == "solver_memory_limit":
        if (
            initial["memory_limit_exceeded"] is not True
            or initial["timed_out"]
        ):
            raise ValueError("memory outcome contradicts child status")
        return
    if outcome == "solver_unknown":
        if not flags_clear or initial["exit_code"] != 0 or result is None:
            raise ValueError("UNKNOWN outcome contradicts child status")
        if result.status != "UNKNOWN":
            raise ValueError("UNKNOWN outcome lacks an UNKNOWN result")
        return

    if not flags_clear:
        raise ValueError("decisive attempt records a child resource failure")
    if outcome in {"coloring_cut_committed", "candidate_review_pending"}:
        if (
            initial["exit_code"] != 10
            or result is None
            or result.status != "SAT"
            or result.model is None
        ):
            raise ValueError("SAT outcome contradicts solver result")
        model = result.model
        if outcome == "coloring_cut_committed":
            fixed_base = base_cnf or ParsedCNF(
                encoding.cnf.variable_count,
                tuple(encoding.cnf.clauses),
            )
            validate_model_satisfies_cnf(fixed_base, model)
            if instrumentation is not None:
                instrumentation.historical_sat_base_cnf_validations += 1
        edges = encoding.decode_edges(model)
        family = encoding.decode_family(model)
        validate_decoded_candidate(encoding, edges, family)
        decoded = strict_json_bytes(
            _bound_artifact_bytes(manifest, "decoded_candidate")
        )
        _validate_decoded_payload(
            decoded,
            expected_edges=edges,
            expected_family=family,
        )
        if outcome == "coloring_cut_committed":
            raw_coloring = strict_json_bytes(
                _bound_artifact_bytes(manifest, "coloring")
            )
            if not isinstance(raw_coloring, list):
                raise ValueError("coloring artifact is not a list")
            coloring = canonical_coloring(raw_coloring)
            if list(coloring) != raw_coloring:
                raise ValueError("coloring artifact is not canonical")
            _proper_coloring(edges, coloring)
            clause = same_color_cut(encoding, coloring)
            if any(model[literal] for literal in clause):
                raise ValueError("recorded cut is true in its source model")
            if instrumentation is not None:
                instrumentation.historical_own_cut_validations += 1
            expected_cut = {
                "index": cut_count,
                "coloring": list(coloring),
                "coloring_sha256": sha256_bytes(coloring_bytes(coloring)),
                "clause": list(clause),
                "clause_sha256": sha256_bytes(clause_bytes(clause)),
            }
            if manifest.get("committed_cut") != expected_cut:
                raise ValueError("committed cut contradicts its source artifacts")
            expected_validation = {
                "dimacs_exact": True,
                "complete_model": True,
                "all_clauses_satisfied": True,
                "decoded_candidate_directly_validated": True,
                "proper_three_coloring_directly_validated": True,
                "cut_false_in_current_model": True,
            }
        else:
            if instrumentation is not None:
                instrumentation.decisive_cnf_reconstructions += 1
            cnf_artifact = manifest["artifacts"]["cnf"]  # type: ignore[index]
            _, parsed_cnf = validate_generated_cnf(
                template=configuration.template,
                cuts=cuts[:cut_count],
                cnf_path=Path(str(cnf_artifact["path"])),
            )
            validate_model_satisfies_cnf(parsed_cnf, model)
            if find_coloring(N, edges, 3) is not None:
                raise ValueError("candidate terminal graph is three-colorable")
            expected_validation = {
                "dimacs_exact": True,
                "complete_model": True,
                "all_clauses_satisfied": True,
                "decoded_candidate_directly_validated": True,
                "three_coloring": None,
            }
        if manifest.get("validation") != expected_validation:
            raise ValueError("SAT validation ledger is not exact")
        return

    if outcome != "unsat_verified":
        raise ValueError("attempt has unknown semantic outcome")
    if initial["exit_code"] != 20 or result is None or result.status != "UNSAT":
        raise ValueError("UNSAT terminal contradicts initial solver result")
    if instrumentation is not None:
        instrumentation.decisive_cnf_reconstructions += 1
    cnf_artifact = manifest["artifacts"]["cnf"]  # type: ignore[index]
    _, parsed_cnf = validate_generated_cnf(
        template=configuration.template,
        cuts=cuts[:cut_count],
        cnf_path=Path(str(cnf_artifact["path"])),
    )
    proof_result = parse_solver_result_bytes(
        _bound_artifact_bytes(manifest, "proof_result"),
        parsed_cnf.variable_count,
    )
    proof_solver = manifest.get("proof_solver")
    proof_checker = manifest.get("proof_checker")
    if (
        not isinstance(proof_solver, dict)
        or not isinstance(proof_checker, dict)
        or proof_solver["exit_code"] != 20
        or proof_solver["timed_out"]
        or proof_solver["memory_limit_exceeded"]
        or proof_result.status != "UNSAT"
        or proof_checker["exit_code"] != 0
        or proof_checker["timed_out"]
        or proof_checker["memory_limit_exceeded"]
    ):
        raise ValueError("UNSAT proof/checker child records are contradictory")
    proof_path = Path(
        str(manifest["artifacts"]["drat_proof"]["path"])  # type: ignore[index]
    )
    if proof_path.stat().st_size == 0:
        raise ValueError("UNSAT terminal has an empty DRAT proof")
    _checker_verified(
        Path(str(manifest["artifacts"]["checker_stdout"]["path"])),  # type: ignore[index]
        Path(str(manifest["artifacts"]["checker_stderr"]["path"])),  # type: ignore[index]
    )
    expected_validation = {
        "initial_unsat": True,
        "identical_cnf_rerun": True,
        "proof_rerun_unsat": True,
        "drat_trim_flags": ["-I", "-f", "-W"],
        "drat_trim_exact_verified_line": True,
        "drat_trim_warning_free": True,
        "cnf_unchanged": True,
        "proof_unchanged_during_check": True,
    }
    if manifest.get("validation") != expected_validation:
        raise ValueError("UNSAT validation ledger is not exact")


def _initial_history_chain_sha256(
    configuration: RunConfiguration,
    run_manifest_sha256: str,
) -> str:
    return sha256_bytes(
        canonical_json_bytes(
            {
                "domain": "gamma-theta-k3-cegar-history-v1",
                "configuration_sha256": configuration.digest,
                "run_manifest_sha256": run_manifest_sha256,
            },
            pretty=False,
        )
    )


def _history_chain_step(
    before_sha256: str,
    *,
    attempt_reference: Mapping[str, object],
    cut_record: Mapping[str, object] | None,
    status_value: str,
    terminal: Mapping[str, object] | None,
) -> str:
    if re.fullmatch(r"[0-9a-f]{64}", before_sha256) is None:
        raise ValueError("history-chain predecessor is malformed")
    return sha256_bytes(
        canonical_json_bytes(
            {
                "domain": "gamma-theta-k3-cegar-history-v1",
                "before_sha256": before_sha256,
                "attempt_reference": dict(attempt_reference),
                "cut_record": (
                    dict(cut_record) if cut_record is not None else None
                ),
                "status": status_value,
                "terminal": dict(terminal) if terminal is not None else None,
            },
            pretty=False,
        )
    )


def _initial_checkpoint(
    run_manifest_path: Path,
    run_manifest_sha256: str,
    configuration: RunConfiguration,
) -> dict[str, object]:
    cuts: list[dict[str, object]] = []
    return {
        "schema": "gamma-theta-k3-cegar-checkpoint-v2",
        "schema_version": SCHEMA_VERSION,
        "configuration_sha256": configuration.digest,
        "run_manifest_path": str(run_manifest_path.resolve()),
        "run_manifest_sha256": run_manifest_sha256,
        "status": "running",
        "attempts": [],
        "cuts": cuts,
        "cuts_payload_sha256": sha256_bytes(cuts_payload_bytes(cuts)),
        "history_chain_sha256": _initial_history_chain_sha256(
            configuration, run_manifest_sha256
        ),
        "terminal": None,
    }


def _checkpoint_state_digest(
    *,
    configuration_sha256: str,
    run_manifest_path: str,
    run_manifest_sha256: str,
    status_value: str,
    attempt_count: int,
    cut_count: int,
    cuts_payload_sha256: str,
    history_chain_sha256: str,
    terminal: Mapping[str, object] | None,
) -> str:
    """Bind one logical checkpoint state without reserializing its full history."""

    if (
        re.fullmatch(r"[0-9a-f]{64}", configuration_sha256) is None
        or not Path(run_manifest_path).is_absolute()
        or re.fullmatch(r"[0-9a-f]{64}", run_manifest_sha256) is None
        or status_value
        not in {"running", "candidate_review_pending", "unsat_verified"}
        or type(attempt_count) is not int
        or attempt_count < 0
        or type(cut_count) is not int
        or not 0 <= cut_count <= attempt_count
        or re.fullmatch(r"[0-9a-f]{64}", cuts_payload_sha256) is None
        or re.fullmatch(r"[0-9a-f]{64}", history_chain_sha256) is None
        or (terminal is not None and not isinstance(terminal, Mapping))
    ):
        raise ValueError("logical checkpoint state is malformed")
    return sha256_bytes(
        canonical_json_bytes(
            {
                "domain": "gamma-theta-k3-cegar-checkpoint-state-v1",
                "schema": "gamma-theta-k3-cegar-checkpoint-v2",
                "schema_version": SCHEMA_VERSION,
                "configuration_sha256": configuration_sha256,
                "run_manifest_path": run_manifest_path,
                "run_manifest_sha256": run_manifest_sha256,
                "status": status_value,
                "attempt_count": attempt_count,
                "cut_count": cut_count,
                "cuts_payload_sha256": cuts_payload_sha256,
                "history_chain_sha256": history_chain_sha256,
                "terminal": dict(terminal) if terminal is not None else None,
            },
            pretty=False,
        )
    )


def checkpoint_state_sha256(checkpoint: Mapping[str, object]) -> str:
    """Return the canonical compact digest recorded by the next attempt."""

    attempts = checkpoint.get("attempts")
    cuts = checkpoint.get("cuts")
    terminal = checkpoint.get("terminal")
    if not isinstance(attempts, list) or not isinstance(cuts, list):
        raise ValueError("checkpoint state has malformed history ledgers")
    if terminal is not None and not isinstance(terminal, Mapping):
        raise ValueError("checkpoint state has a malformed terminal binding")
    return _checkpoint_state_digest(
        configuration_sha256=str(checkpoint.get("configuration_sha256")),
        run_manifest_path=str(checkpoint.get("run_manifest_path")),
        run_manifest_sha256=str(checkpoint.get("run_manifest_sha256")),
        status_value=str(checkpoint.get("status")),
        attempt_count=len(attempts),
        cut_count=len(cuts),
        cuts_payload_sha256=str(checkpoint.get("cuts_payload_sha256")),
        history_chain_sha256=str(checkpoint.get("history_chain_sha256")),
        terminal=terminal,
    )


def _validate_cut_record(
    record: object,
    index: int,
    encoding: K3Encoding,
    attempts: Sequence[Mapping[str, object]],
    *,
    attempt_manifests: Sequence[Mapping[str, object]] | None = None,
    instrumentation: AuditInstrumentation | None = None,
) -> tuple[int, ...]:
    if not isinstance(record, dict) or set(record) != {
        "index",
        "coloring",
        "coloring_sha256",
        "clause",
        "clause_sha256",
        "source_attempt_index",
        "source_attempt_manifest_path",
        "source_attempt_manifest_sha256",
    }:
        raise ValueError("malformed cut checkpoint record")
    if record["index"] != index:
        raise ValueError("cut indices are not consecutive")
    raw_coloring = record["coloring"]
    if not isinstance(raw_coloring, list):
        raise ValueError("cut coloring is not a list")
    coloring = canonical_coloring(raw_coloring)
    if tuple(raw_coloring) != coloring:
        raise ValueError("cut coloring is not canonical")
    if record["coloring_sha256"] != sha256_bytes(coloring_bytes(coloring)):
        raise ValueError("cut coloring hash mismatch")
    clause = same_color_cut(encoding, coloring)
    raw_clause = record["clause"]
    if not isinstance(raw_clause, list) or tuple(raw_clause) != clause:
        raise ValueError("cut clause does not match its coloring")
    if record["clause_sha256"] != sha256_bytes(clause_bytes(clause)):
        raise ValueError("cut clause hash mismatch")
    source_attempt = record["source_attempt_index"]
    if type(source_attempt) is not int or not 0 <= source_attempt < len(attempts):
        raise ValueError("cut source attempt is invalid")
    attempt = attempts[source_attempt]
    if (
        record["source_attempt_manifest_path"] != attempt["manifest_path"]
        or record["source_attempt_manifest_sha256"]
        != attempt["manifest_sha256"]
        or attempt["outcome"] != "coloring_cut_committed"
    ):
        raise ValueError("cut source attempt binding is inconsistent")
    if attempt_manifests is None:
        source_manifest = strict_json_file(
            Path(str(attempt["manifest_path"]))
        )
        if not isinstance(source_manifest, dict):
            raise ValueError("cut source attempt manifest is malformed")
    else:
        if len(attempt_manifests) != len(attempts):
            raise ValueError("attempt-manifest cache has the wrong length")
        source_manifest = attempt_manifests[source_attempt]
    committed = source_manifest.get("committed_cut")
    expected_committed = {
        key: record[key]
        for key in (
            "index",
            "coloring",
            "coloring_sha256",
            "clause",
            "clause_sha256",
        )
    }
    if committed != expected_committed:
        raise ValueError("cut record differs from its source attempt")
    if instrumentation is not None:
        instrumentation.cut_ledger_record_validations += 1
    return coloring


def _validate_attempt_reference(
    raw: object,
    index: int,
    configuration: RunConfiguration,
    run_manifest_sha256: str,
    run_directory: Path,
    cuts: Sequence[Mapping[str, object]],
    deep_reconstruct: bool,
    prefix_bindings: Sequence[tuple[str, int]] | None = None,
    encoding: K3Encoding | None = None,
    base_cnf: ParsedCNF | None = None,
    manifest_cache: dict[int, Mapping[str, object]] | None = None,
    instrumentation: AuditInstrumentation | None = None,
) -> Mapping[str, object]:
    if not isinstance(raw, dict) or set(raw) != {
        "index",
        "manifest_path",
        "manifest_sha256",
        "outcome",
        "checkpoint_before_sha256",
        "history_chain_before_sha256",
    }:
        raise ValueError("malformed attempt reference")
    if raw["index"] != index:
        raise ValueError("attempt indices are not consecutive")
    if raw["outcome"] not in {
        "coloring_cut_committed",
        "candidate_review_pending",
        "unsat_verified",
        "solver_timeout",
        "solver_memory_limit",
        "solver_unknown",
    }:
        raise ValueError("unknown attempt outcome")
    path_raw = raw["manifest_path"]
    digest = raw["manifest_sha256"]
    if (
        type(path_raw) is not str
        or type(digest) is not str
        or re.fullmatch(r"[0-9a-f]{64}", digest) is None
    ):
        raise ValueError("malformed attempt manifest binding")
    path = Path(path_raw)
    if not path.is_absolute() or not _path_is_within(path, run_directory):
        raise ValueError("attempt manifest escapes the run directory")
    _assert_regular_single_link(path, "attempt manifest")
    if sha256_file(path) != digest:
        raise ValueError("attempt manifest hash mismatch")
    manifest = strict_json_file(path)
    if not isinstance(manifest, dict):
        raise ValueError("attempt manifest is not an object")
    if manifest_cache is not None:
        if index in manifest_cache:
            raise ValueError("attempt manifest cache repeats an index")
        manifest_cache[index] = manifest
    expected_keys = _expected_attempt_manifest_keys(str(raw["outcome"]))
    if set(manifest) != expected_keys:
        raise ValueError("attempt manifest has an unexpected outcome schema")
    if (
        manifest["schema"] != "gamma-theta-k3-cegar-attempt-v2"
        or manifest["schema_version"] != SCHEMA_VERSION
        or manifest["attempt_index"] != index
        or manifest["outcome"] != raw["outcome"]
        or manifest["configuration_sha256"] != configuration.digest
        or manifest["run_manifest_sha256"] != run_manifest_sha256
        or manifest["checkpoint_before_sha256"]
        != raw["checkpoint_before_sha256"]
        or manifest["history_chain_before_sha256"]
        != raw["history_chain_before_sha256"]
    ):
        raise ValueError("attempt manifest provenance mismatch")
    if (
        type(manifest["checkpoint_before_sha256"]) is not str
        or re.fullmatch(
            r"[0-9a-f]{64}", manifest["checkpoint_before_sha256"]
        )
        is None
        or type(manifest["history_chain_before_sha256"]) is not str
        or re.fullmatch(
            r"[0-9a-f]{64}", manifest["history_chain_before_sha256"]
        )
        is None
    ):
        raise ValueError("attempt predecessor binding is malformed")
    if (
        type(manifest["cut_count_before"]) is not int
        or not 0 <= manifest["cut_count_before"] <= len(cuts)
    ):
        raise ValueError("attempt cut-prefix count is invalid")
    _verify_artifact_map(manifest["artifacts"], run_directory)
    _verify_compressed_artifacts(
        manifest["compressed_artifacts"], run_directory
    )
    _verify_reconstructible_artifacts(
        manifest["reconstructible_artifacts"],
        run_directory=run_directory,
        configuration=configuration,
        cuts=cuts,
        retained_artifacts=manifest["artifacts"],
        deep_reconstruct=deep_reconstruct,
        prefix_bindings=prefix_bindings,
    )
    _validate_attempt_storage_layout(manifest, path.parent)
    _verify_attempt_commands(manifest, configuration, path.parent)
    _validate_attempt_semantics(
        manifest,
        configuration=configuration,
        encoding=encoding or build_k3_encoding(configuration.template),
        cuts=cuts,
        base_cnf=base_cnf,
        instrumentation=instrumentation,
    )
    storage = manifest["storage"]
    preflight = manifest["disk_preflight"]
    session_command = manifest["orchestrator_session"]["command"]  # type: ignore[index]
    session_budget = int(
        session_command[session_command.index("--max-iterations") + 1]
    )
    mib = 1 << 20
    expected_reserve = configuration.disk_reserve_mib * mib
    expected_retained = (
        session_budget * configuration.retained_attempt_limit_mib * mib
    )
    expected_terminal = 9 * configuration.child_file_limit_mib * mib
    expected_generation = 16 * mib
    expected_required = (
        expected_reserve
        + expected_retained
        + expected_terminal
        + expected_generation
    )
    if (
        not isinstance(storage, dict)
        or not isinstance(preflight, dict)
        or set(preflight)
        != {
            "available_free_bytes",
            "disk_reserve_bytes",
            "iteration_budget",
            "retained_session_budget_bytes",
            "terminal_workspace_budget_bytes",
            "generation_workspace_budget_bytes",
            "required_free_bytes",
            "passed",
        }
        or preflight.get("passed") is not True
        or preflight.get("iteration_budget") != session_budget
        or preflight.get("disk_reserve_bytes") != expected_reserve
        or preflight.get("retained_session_budget_bytes") != expected_retained
        or preflight.get("terminal_workspace_budget_bytes") != expected_terminal
        or preflight.get("generation_workspace_budget_bytes")
        != expected_generation
        or preflight.get("required_free_bytes") != expected_required
        or type(preflight.get("available_free_bytes")) is not int
        or preflight["available_free_bytes"] < expected_required
    ):
        raise ValueError("attempt storage/disk-preflight record is malformed")
    reconstructible = manifest["reconstructible_artifacts"]
    if reconstructible:
        retained_payload_bytes = sum(
            int(record["size_bytes"])
            for record in manifest["artifacts"].values()  # type: ignore[union-attr]
        ) + sum(
            int(record["gzip_size_bytes"])
            for record in manifest["compressed_artifacts"].values()  # type: ignore[union-attr]
        )
        if (
            set(storage)
            != {
                "policy",
                "raw_cnf_and_cut_input_removed_after_validation",
                "compressed_roles",
                "reconstructible_roles",
                "retained_payload_bytes_before_attempt_manifest",
                "retained_attempt_limit_bytes",
            }
            or storage.get("policy") != "compact-intermediate-v1"
            or storage.get(
                "raw_cnf_and_cut_input_removed_after_validation"
            )
            is not True
            or storage.get("compressed_roles")
            != sorted(manifest["compressed_artifacts"])
            or storage.get("reconstructible_roles")
            != sorted(reconstructible)
            or type(
                storage.get("retained_payload_bytes_before_attempt_manifest")
            )
            is not int
            or storage["retained_payload_bytes_before_attempt_manifest"] < 0
            or storage["retained_payload_bytes_before_attempt_manifest"]
            != retained_payload_bytes
            or storage.get("retained_attempt_limit_bytes")
            != configuration.retained_attempt_limit_mib << 20
            or reconstructible["cnf"]["cut_count"]  # type: ignore[index]
            != manifest["cut_count_before"]
        ):
            raise ValueError("intermediate storage policy is inconsistent")
    elif storage != {
        "policy": "terminal-raw-v1",
        "raw_terminal_artifacts_retained": True,
    }:
        raise ValueError("terminal storage policy is inconsistent")
    return raw


def validate_checkpoint_payload(
    payload: object,
    *,
    configuration: RunConfiguration,
    run_manifest_path: Path,
    run_manifest_sha256: str,
    deep_reconstruct: bool = False,
    verify_terminal_proof: bool = False,
    instrumentation: AuditInstrumentation | None = None,
) -> dict[str, object]:
    if not isinstance(payload, dict) or set(payload) != {
        "schema",
        "schema_version",
        "configuration_sha256",
        "run_manifest_path",
        "run_manifest_sha256",
        "status",
        "attempts",
        "cuts",
        "cuts_payload_sha256",
        "history_chain_sha256",
        "terminal",
    }:
        raise ValueError("checkpoint has an unexpected schema")
    if (
        payload["schema"] != "gamma-theta-k3-cegar-checkpoint-v2"
        or payload["schema_version"] != SCHEMA_VERSION
        or payload["configuration_sha256"] != configuration.digest
        or payload["run_manifest_path"] != str(run_manifest_path.resolve())
        or payload["run_manifest_sha256"] != run_manifest_sha256
    ):
        raise ValueError("checkpoint provenance does not match this run")
    status_value = payload["status"]
    if status_value not in {
        "running",
        "candidate_review_pending",
        "unsat_verified",
    }:
        raise ValueError("checkpoint status is invalid")
    attempts_raw = payload["attempts"]
    cuts_raw = payload["cuts"]
    if not isinstance(attempts_raw, list) or not isinstance(cuts_raw, list):
        raise ValueError("checkpoint attempt/cut ledger is not a list")
    run_directory = Path(configuration.run_directory)
    prefix_bindings = cut_prefix_bindings(cuts_raw)
    encoding = build_k3_encoding(configuration.template)
    base_cnf = ParsedCNF(
        encoding.cnf.variable_count,
        tuple(encoding.cnf.clauses),
    )
    attempt_manifest_cache: dict[int, Mapping[str, object]] = {}
    attempts: list[Mapping[str, object]] = []
    terminal_outcomes = {
        "candidate_review_pending",
        "unsat_verified",
    }
    for index, raw in enumerate(attempts_raw):
        raw_outcome = raw.get("outcome") if isinstance(raw, dict) else None
        if raw_outcome in terminal_outcomes and (
            index != len(attempts_raw) - 1 or status_value != raw_outcome
        ):
            raise ValueError(
                "candidate/UNSAT outcome is permitted only as the final "
                "matching terminal attempt"
            )
        attempts.append(
            _validate_attempt_reference(
                raw,
                index,
                configuration,
                run_manifest_sha256,
                run_directory,
                cuts_raw,
                False,
                prefix_bindings,
                encoding,
                base_cnf,
                attempt_manifest_cache,
                instrumentation,
            )
        )
    attempt_manifests = [
        attempt_manifest_cache[index] for index in range(len(attempts))
    ]
    seen: set[tuple[int, ...]] = set()
    for index, record in enumerate(cuts_raw):
        coloring = _validate_cut_record(
            record,
            index,
            encoding,
            attempts,
            attempt_manifests=attempt_manifests,
            instrumentation=instrumentation,
        )
        if coloring in seen:
            raise ValueError("checkpoint repeats a coloring partition")
        seen.add(coloring)
    if payload["cuts_payload_sha256"] != prefix_bindings[-1][0]:
        raise ValueError("checkpoint cut-list hash mismatch")
    if (
        type(payload["history_chain_sha256"]) is not str
        or re.fullmatch(r"[0-9a-f]{64}", payload["history_chain_sha256"])
        is None
    ):
        raise ValueError("checkpoint history-chain head is malformed")
    terminal = payload["terminal"]
    if status_value == "running":
        if terminal is not None:
            raise ValueError("running checkpoint has a terminal record")
    else:
        if not isinstance(terminal, dict) or set(terminal) != {
            "kind",
            "path",
            "sha256",
        }:
            raise ValueError("terminal checkpoint lacks its marker binding")
        expected_kind = (
            "candidate"
            if status_value == "candidate_review_pending"
            else "unsat"
        )
        if terminal["kind"] != expected_kind:
            raise ValueError("terminal kind and checkpoint status disagree")
        expected_path = (
            Path(configuration.run_directory) / CANDIDATE_MARKER_NAME
            if expected_kind == "candidate"
            else Path(configuration.run_directory) / UNSAT_MARKER_NAME
        )
        if (
            terminal["path"] != str(expected_path.resolve())
            or type(terminal["sha256"]) is not str
            or re.fullmatch(r"[0-9a-f]{64}", terminal["sha256"]) is None
        ):
            raise ValueError("terminal marker binding is malformed")
        marker = _validate_terminal_marker(
            expected_path,
            expected_kind=expected_kind,
            configuration=configuration,
            run_manifest_sha256=run_manifest_sha256,
            cuts=cuts_raw,
        )
        if sha256_file(expected_path) != terminal["sha256"]:
            raise ValueError("terminal marker hash mismatch")
        if (
            not attempts
            or attempts[-1]["outcome"] != status_value
            or marker["attempt_manifest_path"]
            != attempts[-1]["manifest_path"]
            or marker["attempt_manifest_sha256"]
            != attempts[-1]["manifest_sha256"]
        ):
            raise ValueError("terminal marker does not bind the final attempt")

    cuts_by_source: dict[int, Mapping[str, object]] = {}
    for cut in cuts_raw:
        source = cut["source_attempt_index"]
        if source in cuts_by_source:
            raise ValueError("one attempt is the source of multiple cuts")
        cuts_by_source[source] = cut
    history_head = _initial_history_chain_sha256(
        configuration, run_manifest_sha256
    )
    expected_checkpoint_before = checkpoint_state_sha256(
        _initial_checkpoint(
            run_manifest_path,
            run_manifest_sha256,
            configuration,
        )
    )
    committed_cut_count = 0
    for index, reference in enumerate(attempts):
        attempt_manifest = attempt_manifests[index]
        if (
            reference["history_chain_before_sha256"] != history_head
            or attempt_manifest["history_chain_before_sha256"] != history_head
            or attempt_manifest["cut_count_before"] != committed_cut_count
        ):
            raise ValueError("attempt predecessor history chain is broken")
        if (
            reference["checkpoint_before_sha256"]
            != expected_checkpoint_before
            or attempt_manifest["checkpoint_before_sha256"]
            != expected_checkpoint_before
        ):
            raise ValueError(
                "attempt checkpoint-before chronology is broken"
            )
        cut = cuts_by_source.get(index)
        if reference["outcome"] == "coloring_cut_committed":
            if cut is None:
                raise ValueError("coloring attempt has no committed cut")
            committed_cut_count += 1
        elif cut is not None:
            raise ValueError("non-coloring attempt is the source of a cut")
        is_terminal_step = (
            status_value != "running" and index == len(attempts) - 1
        )
        step_status = status_value if is_terminal_step else "running"
        step_terminal = terminal if is_terminal_step else None
        history_head = _history_chain_step(
            history_head,
            attempt_reference=reference,
            cut_record=cut,
            status_value=step_status,
            terminal=step_terminal,
        )
        expected_checkpoint_before = _checkpoint_state_digest(
            configuration_sha256=configuration.digest,
            run_manifest_path=str(run_manifest_path.resolve()),
            run_manifest_sha256=run_manifest_sha256,
            status_value=step_status,
            attempt_count=index + 1,
            cut_count=committed_cut_count,
            cuts_payload_sha256=prefix_bindings[committed_cut_count][0],
            history_chain_sha256=history_head,
            terminal=step_terminal,
        )
    if committed_cut_count != len(cuts_raw):
        raise ValueError("cut ledger is not covered by its attempt history")
    if history_head != payload["history_chain_sha256"]:
        raise ValueError("checkpoint history-chain head mismatch")
    if expected_checkpoint_before != checkpoint_state_sha256(payload):
        raise ValueError("checkpoint logical-state chronology is inconsistent")
    if deep_reconstruct:
        for reference in reversed(attempts):
            latest_manifest = strict_json_file(
                Path(str(reference["manifest_path"]))
            )
            if not isinstance(latest_manifest, dict):
                raise ValueError("latest reconstruction manifest is malformed")
            reconstructible = latest_manifest["reconstructible_artifacts"]
            if reconstructible:
                _verify_reconstructible_artifacts(
                    reconstructible,
                    run_directory=run_directory,
                    configuration=configuration,
                    cuts=cuts_raw,
                    retained_artifacts=latest_manifest["artifacts"],
                    deep_reconstruct=True,
                    prefix_bindings=prefix_bindings,
                )
                break
    if verify_terminal_proof:
        if status_value != "unsat_verified":
            raise ValueError(
                "live terminal-proof verification requires an UNSAT terminal"
            )
        terminal_attempt = strict_json_file(
            Path(str(attempts[-1]["manifest_path"]))
        )
        if not isinstance(terminal_attempt, dict):
            raise ValueError("terminal attempt manifest is malformed")
        artifacts = terminal_attempt["artifacts"]
        verify_stored_drat_certificate(
            configuration=configuration,
            cnf_path=Path(str(artifacts["cnf"]["path"])),
            proof_path=Path(str(artifacts["drat_proof"]["path"])),
        )
    return payload


def _terminal_marker_paths(run_directory: Path) -> tuple[Path, Path]:
    return (
        run_directory / CANDIDATE_MARKER_NAME,
        run_directory / UNSAT_MARKER_NAME,
    )


def _validate_terminal_marker(
    path: Path,
    *,
    expected_kind: str,
    configuration: RunConfiguration,
    run_manifest_sha256: str,
    cuts: Sequence[Mapping[str, object]],
    validate_semantics: bool = False,
    instrumentation: AuditInstrumentation | None = None,
) -> dict[str, object]:
    _assert_regular_single_link(path, f"{expected_kind} terminal marker")
    marker = strict_json_file(path)
    if not isinstance(marker, dict) or set(marker) != {
        "schema",
        "schema_version",
        "kind",
        "status",
        "configuration_sha256",
        "run_manifest_sha256",
        "checkpoint_before_sha256",
        "history_chain_before_sha256",
        "attempt_manifest_path",
        "attempt_manifest_sha256",
    }:
        raise ValueError("terminal marker has an unexpected schema")
    expected_status = (
        "candidate_review_pending"
        if expected_kind == "candidate"
        else "unsat_verified"
    )
    if (
        marker["schema"] != "gamma-theta-k3-cegar-terminal-v2"
        or marker["schema_version"] != SCHEMA_VERSION
        or marker["kind"] != expected_kind
        or marker["status"] != expected_status
        or marker["configuration_sha256"] != configuration.digest
        or marker["run_manifest_sha256"] != run_manifest_sha256
        or type(marker["checkpoint_before_sha256"]) is not str
        or re.fullmatch(
            r"[0-9a-f]{64}", marker["checkpoint_before_sha256"]
        )
        is None
        or type(marker["history_chain_before_sha256"]) is not str
        or re.fullmatch(
            r"[0-9a-f]{64}", marker["history_chain_before_sha256"]
        )
        is None
    ):
        raise ValueError("terminal marker provenance mismatch")
    attempt_path_raw = marker["attempt_manifest_path"]
    attempt_hash = marker["attempt_manifest_sha256"]
    if (
        type(attempt_path_raw) is not str
        or type(attempt_hash) is not str
        or re.fullmatch(r"[0-9a-f]{64}", attempt_hash) is None
    ):
        raise ValueError("terminal marker attempt binding is malformed")
    attempt_path = Path(attempt_path_raw)
    if not _path_is_within(attempt_path, Path(configuration.run_directory)):
        raise ValueError("terminal attempt manifest escapes the run directory")
    _assert_regular_single_link(attempt_path, "terminal attempt manifest")
    if sha256_file(attempt_path) != attempt_hash:
        raise ValueError("terminal attempt manifest hash mismatch")
    attempt = strict_json_file(attempt_path)
    if (
        not isinstance(attempt, dict)
        or set(attempt)
        != _expected_attempt_manifest_keys(expected_status)
        or attempt.get("outcome") != expected_status
        or attempt.get("configuration_sha256") != configuration.digest
        or attempt.get("run_manifest_sha256") != run_manifest_sha256
        or marker["checkpoint_before_sha256"]
        != attempt.get("checkpoint_before_sha256")
        or marker["history_chain_before_sha256"]
        != attempt.get("history_chain_before_sha256")
        or attempt.get("cut_count_before") != len(cuts)
    ):
        raise ValueError("terminal attempt manifest has wrong provenance")
    _verify_artifact_map(
        attempt.get("artifacts"),
        Path(configuration.run_directory),
    )
    _verify_compressed_artifacts(
        attempt.get("compressed_artifacts"),
        Path(configuration.run_directory),
    )
    _verify_reconstructible_artifacts(
        attempt.get("reconstructible_artifacts"),
        run_directory=Path(configuration.run_directory),
        configuration=configuration,
        cuts=cuts,
        retained_artifacts=attempt.get("artifacts"),  # type: ignore[arg-type]
        deep_reconstruct=False,
    )
    _validate_attempt_storage_layout(attempt, attempt_path.parent)
    _verify_attempt_commands(attempt, configuration, attempt_path.parent)
    if validate_semantics:
        encoding = build_k3_encoding(configuration.template)
        _validate_attempt_semantics(
            attempt,
            configuration=configuration,
            encoding=encoding,
            cuts=cuts,
            base_cnf=ParsedCNF(
                encoding.cnf.variable_count,
                tuple(encoding.cnf.clauses),
            ),
            instrumentation=instrumentation,
        )
    return marker


def _terminal_outcome(
    *,
    run_directory: Path,
    configuration: RunConfiguration,
    run_manifest_sha256: str,
    checkpoint_path: Path,
    checkpoint: Mapping[str, object],
    instrumentation: AuditInstrumentation | None = None,
) -> RunOutcome | None:
    candidate_path, unsat_path = _terminal_marker_paths(run_directory)
    candidate_exists = candidate_path.exists() or candidate_path.is_symlink()
    unsat_exists = unsat_path.exists() or unsat_path.is_symlink()
    if candidate_exists and unsat_exists:
        raise RuntimeError("both candidate and UNSAT terminal markers exist")
    terminal_path: Path | None = None
    status_value: str | None = None
    if candidate_exists:
        _validate_terminal_marker(
            candidate_path,
            expected_kind="candidate",
            configuration=configuration,
            run_manifest_sha256=run_manifest_sha256,
            cuts=checkpoint["cuts"],  # type: ignore[arg-type]
            validate_semantics=checkpoint["status"] == "running",
            instrumentation=instrumentation,
        )
        terminal_path = candidate_path
        status_value = "candidate_review_pending"
    elif unsat_exists:
        _validate_terminal_marker(
            unsat_path,
            expected_kind="unsat",
            configuration=configuration,
            run_manifest_sha256=run_manifest_sha256,
            cuts=checkpoint["cuts"],  # type: ignore[arg-type]
            validate_semantics=checkpoint["status"] == "running",
            instrumentation=instrumentation,
        )
        terminal_path = unsat_path
        status_value = "unsat_verified"
    elif checkpoint["status"] != "running":
        raise RuntimeError("terminal checkpoint is missing its fail-closed marker")
    if terminal_path is None or status_value is None:
        return None
    return RunOutcome(
        status=status_value,
        checkpoint_path=str(checkpoint_path.resolve()),
        checkpoint_sha256=sha256_file(checkpoint_path),
        cut_count=len(checkpoint["cuts"]),  # type: ignore[arg-type]
        attempt_count=len(checkpoint["attempts"]),  # type: ignore[arg-type]
        terminal_path=str(terminal_path.resolve()),
    )


def _prepare_run(
    configuration: RunConfiguration,
    *,
    initialize: bool = True,
    deep_reconstruct: bool = False,
    verify_terminal_proof: bool = False,
    instrumentation: AuditInstrumentation | None = None,
) -> tuple[Path, Path, str, dict[str, object]]:
    run_directory = Path(configuration.run_directory)
    run_directory.mkdir(parents=True, exist_ok=True)
    _assert_no_symlink_components(run_directory)
    run_manifest_path = run_directory / RUN_MANIFEST_NAME
    checkpoint_path = run_directory / CHECKPOINT_NAME
    expected_manifest = _run_manifest_payload(configuration)
    expected_manifest_bytes = canonical_json_bytes(expected_manifest)

    if not run_manifest_path.exists():
        if not initialize:
            raise ValueError("audit requires an existing run manifest")
        unexpected = [
            entry.name
            for entry in run_directory.iterdir()
            if entry.name != LOCK_NAME
        ]
        if unexpected:
            raise ValueError(
                "new run directory is not empty: " + ", ".join(sorted(unexpected))
            )
        write_immutable(run_manifest_path, expected_manifest_bytes)
    else:
        _assert_regular_single_link(run_manifest_path, "run manifest")
        if run_manifest_path.read_bytes() != expected_manifest_bytes:
            raise ValueError("run configuration does not match existing manifest")
    run_manifest_sha256 = sha256_file(run_manifest_path)

    if not checkpoint_path.exists():
        if not initialize:
            raise ValueError("audit requires an existing checkpoint")
        checkpoint = _initial_checkpoint(
            run_manifest_path,
            run_manifest_sha256,
            configuration,
        )
        atomic_write(checkpoint_path, canonical_json_bytes(checkpoint))
    checkpoint = validate_checkpoint_payload(
        strict_json_file(checkpoint_path),
        configuration=configuration,
        run_manifest_path=run_manifest_path,
        run_manifest_sha256=run_manifest_sha256,
        deep_reconstruct=deep_reconstruct,
        verify_terminal_proof=verify_terminal_proof,
        instrumentation=instrumentation,
    )
    return (
        run_manifest_path,
        checkpoint_path,
        run_manifest_sha256,
        checkpoint,
    )


def _new_attempt_directory(run_directory: Path, index: int) -> Path:
    attempts = run_directory / "attempts"
    if attempts.exists() or attempts.is_symlink():
        _assert_no_symlink_components(attempts)
        if not attempts.is_dir():
            raise ValueError("attempts path is not a directory")
    else:
        attempts.mkdir(mode=0o700)
        _fsync_directory(run_directory)
    path = Path(
        tempfile.mkdtemp(prefix=f"{index:06d}.", dir=attempts)
    ).resolve()
    _fsync_directory(attempts)
    if not _path_is_within(path, attempts):
        raise RuntimeError("temporary attempt escaped its directory")
    return path


def _attempt_reference(
    index: int,
    outcome: str,
    manifest_path: Path,
) -> dict[str, object]:
    manifest = strict_json_file(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError("attempt manifest is not an object")
    return {
        "index": index,
        "outcome": outcome,
        "manifest_path": str(manifest_path.resolve()),
        "manifest_sha256": sha256_file(manifest_path),
        "checkpoint_before_sha256": manifest.get(
            "checkpoint_before_sha256"
        ),
        "history_chain_before_sha256": manifest.get(
            "history_chain_before_sha256"
        ),
    }


def _commit_checkpoint(
    *,
    checkpoint_path: Path,
    checkpoint: Mapping[str, object],
    attempt_reference: Mapping[str, object],
    configuration: RunConfiguration,
    run_manifest_path: Path,
    run_manifest_sha256: str,
    cut_record: Mapping[str, object] | None = None,
    status_value: str = "running",
    terminal: Mapping[str, object] | None = None,
) -> dict[str, object]:
    if checkpoint["status"] != "running":
        raise RuntimeError("a terminal checkpoint cannot be extended")
    prior_attempts = list(checkpoint["attempts"])  # type: ignore[arg-type]
    prior_cuts = list(checkpoint["cuts"])  # type: ignore[arg-type]
    history_before = checkpoint["history_chain_sha256"]
    if (
        type(history_before) is not str
        or attempt_reference.get("history_chain_before_sha256")
        != history_before
    ):
        raise ValueError("new attempt does not extend the checkpoint history")
    if (
        attempt_reference.get("checkpoint_before_sha256")
        != checkpoint_state_sha256(checkpoint)
    ):
        raise ValueError(
            "new attempt does not bind the current logical checkpoint"
        )
    reference_outcome = attempt_reference.get("outcome")
    terminal_outcomes = {
        "candidate_review_pending",
        "unsat_verified",
    }
    if (
        reference_outcome in terminal_outcomes
        and status_value != reference_outcome
    ) or (
        status_value in terminal_outcomes
        and reference_outcome != status_value
    ):
        raise ValueError(
            "candidate/UNSAT attempt and terminal checkpoint must coincide"
        )
    new_attempt_index = len(prior_attempts)
    _validate_attempt_reference(
        attempt_reference,
        new_attempt_index,
        configuration,
        run_manifest_sha256,
        Path(configuration.run_directory),
        prior_cuts,
        False,
    )
    attempts = [*prior_attempts, dict(attempt_reference)]
    cuts = list(prior_cuts)
    if cut_record is not None:
        encoding = build_k3_encoding(configuration.template)
        coloring = _validate_cut_record(
            cut_record,
            len(prior_cuts),
            encoding,
            attempts,
        )
        existing = {
            tuple(record["coloring"])
            for record in prior_cuts
        }
        if coloring in existing:
            raise ValueError("new checkpoint cut repeats a partition")
        cuts.append(dict(cut_record))
    if status_value not in {
        "running",
        "candidate_review_pending",
        "unsat_verified",
    }:
        raise ValueError("invalid checkpoint transition status")
    if status_value == "running" and terminal is not None:
        raise ValueError("running checkpoint cannot have a terminal")
    if status_value != "running":
        if terminal is None:
            raise ValueError("terminal checkpoint requires a marker")
        expected_kind = (
            "candidate"
            if status_value == "candidate_review_pending"
            else "unsat"
        )
        if terminal.get("kind") != expected_kind:
            raise ValueError("terminal marker kind does not match status")
        marker_path = Path(str(terminal.get("path")))
        marker_hash = terminal.get("sha256")
        if (
            not marker_path.is_absolute()
            or not _path_is_within(
                marker_path, Path(configuration.run_directory)
            )
            or type(marker_hash) is not str
        ):
            raise ValueError("malformed terminal marker binding")
        _validate_terminal_marker(
            marker_path,
            expected_kind=expected_kind,
            configuration=configuration,
            run_manifest_sha256=run_manifest_sha256,
            cuts=prior_cuts,
        )
        if sha256_file(marker_path) != marker_hash:
            raise ValueError("terminal marker hash mismatch")
    updated = {
        "schema": checkpoint["schema"],
        "schema_version": checkpoint["schema_version"],
        "configuration_sha256": checkpoint["configuration_sha256"],
        "run_manifest_path": checkpoint["run_manifest_path"],
        "run_manifest_sha256": checkpoint["run_manifest_sha256"],
        "status": status_value,
        "attempts": attempts,
        "cuts": cuts,
        "cuts_payload_sha256": sha256_bytes(cuts_payload_bytes(cuts)),
        "history_chain_sha256": _history_chain_step(
            history_before,
            attempt_reference=attempt_reference,
            cut_record=cut_record,
            status_value=status_value,
            terminal=terminal,
        ),
        "terminal": dict(terminal) if terminal is not None else None,
    }
    atomic_write(checkpoint_path, canonical_json_bytes(updated))
    installed = strict_json_file(checkpoint_path)
    if installed != updated:
        raise RuntimeError("installed checkpoint differs from committed payload")
    if not isinstance(installed, dict):
        raise RuntimeError("installed checkpoint is not an object")
    return installed


def _generate_attempt_instance(
    *,
    configuration: RunConfiguration,
    checkpoint: Mapping[str, object],
    attempt_directory: Path,
) -> tuple[Path, Path, Path, K3Encoding, ParsedCNF]:
    cuts_path = attempt_directory / "cuts.json"
    cnf_path = attempt_directory / "instance.cnf"
    generator_manifest_path = attempt_directory / "generator.json"
    cuts = checkpoint["cuts"]
    if not isinstance(cuts, list):
        raise ValueError("checkpoint cuts are not a list")
    cuts_bytes = cuts_payload_bytes(cuts)
    if sha256_bytes(cuts_bytes) != checkpoint["cuts_payload_sha256"]:
        raise ValueError("checkpoint cut bytes changed before generation")
    write_immutable(cuts_path, cuts_bytes)
    validate_file_roles(
        readonly={
            "cut input": cuts_path,
            **{
                f"runtime source {relative}": campaign_root() / relative
                for relative, _ in configuration.runtime_source_manifest
            },
        },
        writable={
            "CNF output": cnf_path,
            "generator manifest": generator_manifest_path,
        },
    )
    generated = generate(
        template=configuration.template,
        output=cnf_path,
        manifest=generator_manifest_path,
        colorings_path=cuts_path,
    )
    installed = strict_json_file(generator_manifest_path)
    if installed != generated:
        raise RuntimeError("generator return value and manifest differ")
    if not isinstance(installed, dict):
        raise RuntimeError("generator manifest is not an object")
    if (
        installed.get("template") != configuration.template
        or installed.get("colorings_sha256") != sha256_file(cuts_path)
        or installed.get("cnf_sha256") != sha256_file(cnf_path)
        or installed.get("coloring_cut_count") != len(cuts)
    ):
        raise RuntimeError("generator manifest binding is inconsistent")
    encoding, parsed = validate_generated_cnf(
        template=configuration.template,
        cuts=cuts,
        cnf_path=cnf_path,
    )
    return (
        cuts_path,
        cnf_path,
        generator_manifest_path,
        encoding,
        parsed,
    )


def _common_attempt_manifest(
    *,
    attempt_index: int,
    outcome: str,
    configuration: RunConfiguration,
    run_manifest_sha256: str,
    checkpoint_before_sha256: str,
    history_chain_before_sha256: str,
    cut_count_before: int,
    artifacts: Mapping[str, Path],
    solver: ChildResult,
    session_invocation: Sequence[str],
    disk_preflight_report: Mapping[str, int | bool],
    compressed_artifacts: Mapping[str, Mapping[str, object]] | None = None,
    reconstructible_artifacts: Mapping[str, Mapping[str, object]] | None = None,
    storage: Mapping[str, object] | None = None,
) -> dict[str, object]:
    normalized_session = tuple(str(value) for value in session_invocation)
    return {
        "schema": "gamma-theta-k3-cegar-attempt-v2",
        "schema_version": SCHEMA_VERSION,
        "attempt_index": attempt_index,
        "outcome": outcome,
        "configuration_sha256": configuration.digest,
        "run_manifest_sha256": run_manifest_sha256,
        "checkpoint_before_sha256": checkpoint_before_sha256,
        "history_chain_before_sha256": history_chain_before_sha256,
        "cut_count_before": cut_count_before,
        "artifacts": _artifact_map(artifacts),
        "compressed_artifacts": dict(compressed_artifacts or {}),
        "reconstructible_artifacts": dict(
            reconstructible_artifacts or {}
        ),
        "storage": dict(
            storage
            or {
                "policy": "terminal-raw-v1",
                "raw_terminal_artifacts_retained": True,
            }
        ),
        "disk_preflight": dict(disk_preflight_report),
        "orchestrator_session": {
            "command": normalized_session,
            "command_sha256": _command_sha256(normalized_session),
        },
        "initial_solver": asdict(solver),
    }


def _write_attempt_manifest(
    attempt_directory: Path,
    payload: Mapping[str, object],
) -> Path:
    path = attempt_directory / "attempt.json"
    write_immutable(path, canonical_json_bytes(payload))
    return path


def _write_terminal_marker(
    *,
    path: Path,
    kind: str,
    status_value: str,
    configuration: RunConfiguration,
    run_manifest_sha256: str,
    checkpoint_before_sha256: str,
    history_chain_before_sha256: str,
    attempt_manifest_path: Path,
) -> dict[str, object]:
    payload = {
        "schema": "gamma-theta-k3-cegar-terminal-v2",
        "schema_version": SCHEMA_VERSION,
        "kind": kind,
        "status": status_value,
        "configuration_sha256": configuration.digest,
        "run_manifest_sha256": run_manifest_sha256,
        "checkpoint_before_sha256": checkpoint_before_sha256,
        "history_chain_before_sha256": history_chain_before_sha256,
        "attempt_manifest_path": str(attempt_manifest_path.resolve()),
        "attempt_manifest_sha256": sha256_file(attempt_manifest_path),
    }
    write_immutable(path, canonical_json_bytes(payload))
    return {
        "kind": kind,
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
    }


def _checker_verified(stdout_path: Path, stderr_path: Path) -> None:
    try:
        stdout = stdout_path.read_text(encoding="ascii")
        stderr = stderr_path.read_text(encoding="ascii")
    except UnicodeDecodeError as error:
        raise ValueError("DRAT-trim logs are not ASCII") from error
    combined = stdout + "\n" + stderr
    if "warning" in combined.lower():
        raise ValueError("DRAT-trim emitted a warning")
    if [line.strip() for line in stdout.splitlines()].count("s VERIFIED") != 1:
        raise ValueError("DRAT-trim did not emit exactly one 's VERIFIED'")


def run_unsat_proof_replay(
    *,
    configuration: RunConfiguration,
    cnf_path: Path,
    parsed_cnf: ParsedCNF,
    attempt_directory: Path,
) -> tuple[ChildResult, ChildResult, dict[str, Path]]:
    """Rerun an identical UNSAT CNF, save DRAT, and require DRAT-trim."""

    proof_result_path = attempt_directory / "proof.result"
    proof_path = attempt_directory / "proof.drat"
    proof_stdout = attempt_directory / "proof-solver.stdout"
    proof_stderr = attempt_directory / "proof-solver.stderr"
    proof_command = _solver_command(
        configuration,
        cnf_path=cnf_path,
        result_path=proof_result_path,
        proof_path=proof_path,
    )
    validate_file_roles(
        readonly={
            "CNF": cnf_path,
            "CaDiCaL": Path(configuration.cadical.path),
        },
        writable={
            "proof result": proof_result_path,
            "DRAT proof": proof_path,
            "proof stdout": proof_stdout,
            "proof stderr": proof_stderr,
        },
    )
    cnf_hash_before = sha256_file(cnf_path)
    proof_solver = run_bounded_child(
        command=proof_command,
        cwd=Path(configuration.run_directory),
        stdout_path=proof_stdout,
        stderr_path=proof_stderr,
        wall_limit_seconds=configuration.solver_wall_seconds,
        memory_limit_mib=configuration.solver_memory_mib,
        file_limit_mib=configuration.child_file_limit_mib,
        readonly_paths={"CNF": cnf_path},
    )
    if proof_solver.timed_out or proof_solver.exit_code != 20:
        raise RuntimeError("proof-producing CaDiCaL rerun did not return UNSAT")
    parsed_result = parse_solver_result_file(
        proof_result_path, parsed_cnf.variable_count
    )
    if parsed_result.status != "UNSAT":
        raise RuntimeError("proof-producing result file is not UNSAT")
    _assert_regular_single_link(proof_path, "DRAT proof")
    if proof_path.stat().st_size == 0:
        raise RuntimeError("CaDiCaL produced an empty DRAT proof")
    if sha256_file(cnf_path) != cnf_hash_before:
        raise RuntimeError("CNF changed during proof-producing rerun")

    checker_stdout = attempt_directory / "checker.stdout"
    checker_stderr = attempt_directory / "checker.stderr"
    checker_command = _checker_command(
        configuration,
        cnf_path=cnf_path,
        proof_path=proof_path,
    )
    validate_file_roles(
        readonly={
            "CNF": cnf_path,
            "DRAT proof": proof_path,
            "DRAT-trim": Path(configuration.drat_trim.path),
        },
        writable={
            "checker stdout": checker_stdout,
            "checker stderr": checker_stderr,
        },
    )
    proof_hash_before = sha256_file(proof_path)
    checker = run_bounded_child(
        command=checker_command,
        cwd=Path(configuration.run_directory),
        stdout_path=checker_stdout,
        stderr_path=checker_stderr,
        wall_limit_seconds=configuration.checker_wall_seconds,
        memory_limit_mib=configuration.checker_memory_mib,
        file_limit_mib=configuration.child_file_limit_mib,
        readonly_paths={
            "CNF": cnf_path,
            "DRAT proof": proof_path,
        },
    )
    if checker.timed_out or checker.exit_code != 0:
        raise RuntimeError("DRAT-trim did not exit successfully")
    _checker_verified(checker_stdout, checker_stderr)
    if sha256_file(cnf_path) != cnf_hash_before:
        raise RuntimeError("CNF changed during DRAT verification")
    if sha256_file(proof_path) != proof_hash_before:
        raise RuntimeError("DRAT proof changed during verification")
    return (
        proof_solver,
        checker,
        {
            "proof_result": proof_result_path,
            "drat_proof": proof_path,
            "proof_solver_stdout": proof_stdout,
            "proof_solver_stderr": proof_stderr,
            "checker_stdout": checker_stdout,
            "checker_stderr": checker_stderr,
        },
    )


def verify_stored_drat_certificate(
    *,
    configuration: RunConfiguration,
    cnf_path: Path,
    proof_path: Path,
) -> ChildResult:
    """Independently rerun pinned DRAT-trim against retained decisive bytes."""

    _assert_regular_single_link(cnf_path, "stored decisive CNF")
    _assert_regular_single_link(proof_path, "stored DRAT proof")
    cnf_hash_before = sha256_file(cnf_path)
    proof_hash_before = sha256_file(proof_path)
    with tempfile.TemporaryDirectory(prefix="k3-drat-reaudit.") as raw:
        temporary = Path(raw).resolve()
        stdout_path = temporary / "checker.stdout"
        stderr_path = temporary / "checker.stderr"
        command = _checker_command(
            configuration,
            cnf_path=cnf_path,
            proof_path=proof_path,
        )
        result = run_bounded_child(
            command=command,
            cwd=Path(configuration.run_directory),
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            wall_limit_seconds=configuration.checker_wall_seconds,
            memory_limit_mib=configuration.checker_memory_mib,
            file_limit_mib=configuration.child_file_limit_mib,
            readonly_paths={
                "CNF": cnf_path,
                "DRAT proof": proof_path,
            },
        )
        if result.timed_out or result.memory_limit_exceeded or result.exit_code != 0:
            raise RuntimeError("live DRAT certificate verification failed")
        _checker_verified(stdout_path, stderr_path)
    if (
        sha256_file(cnf_path) != cnf_hash_before
        or sha256_file(proof_path) != proof_hash_before
    ):
        raise RuntimeError("decisive bytes changed during live proof verification")
    return result


def _result_outcome(
    status_value: str,
    checkpoint_path: Path,
    checkpoint: Mapping[str, object],
    terminal_path: Path | None = None,
) -> RunOutcome:
    return RunOutcome(
        status=status_value,
        checkpoint_path=str(checkpoint_path.resolve()),
        checkpoint_sha256=sha256_file(checkpoint_path),
        cut_count=len(checkpoint["cuts"]),  # type: ignore[arg-type]
        attempt_count=len(checkpoint["attempts"]),  # type: ignore[arg-type]
        terminal_path=(
            str(terminal_path.resolve()) if terminal_path is not None else None
        ),
    )


def run_cegar(
    *,
    template: str,
    run_directory: Path,
    cadical_path: Path,
    drat_trim_path: Path,
    max_iterations: int,
    solver_seed: int = 0,
    solver_wall_seconds: int = 900,
    solver_memory_mib: int = 4096,
    checker_wall_seconds: int = 900,
    checker_memory_mib: int = 4096,
    session_wall_seconds: int = 3600,
    disk_reserve_mib: int = 4096,
    child_file_limit_mib: int = 256,
    retained_attempt_limit_mib: int = 2,
) -> RunOutcome:
    """Run at most ``max_iterations`` initial solver calls, then checkpoint."""

    session_started = time.perf_counter()
    max_iterations = _positive_exact_int(max_iterations, "iteration budget")
    configuration = build_configuration(
        template=template,
        run_directory=run_directory,
        cadical_path=cadical_path,
        drat_trim_path=drat_trim_path,
        solver_seed=solver_seed,
        solver_wall_seconds=solver_wall_seconds,
        solver_memory_mib=solver_memory_mib,
        checker_wall_seconds=checker_wall_seconds,
        checker_memory_mib=checker_memory_mib,
        session_wall_seconds=session_wall_seconds,
        disk_reserve_mib=disk_reserve_mib,
        child_file_limit_mib=child_file_limit_mib,
        retained_attempt_limit_mib=retained_attempt_limit_mib,
    )
    run_directory = Path(configuration.run_directory)
    run_directory.mkdir(parents=True, exist_ok=True)
    with RunLock(run_directory):
        session_disk_preflight = None
        if not (run_directory / RUN_MANIFEST_NAME).exists():
            session_disk_preflight = disk_preflight(
                configuration, max_iterations
            )
        session_invocation = _normalized_resume_invocation(
            configuration,
            max_iterations=max_iterations,
        )
        (
            run_manifest_path,
            checkpoint_path,
            run_manifest_sha256,
            checkpoint,
        ) = _prepare_run(configuration)
        terminal = _terminal_outcome(
            run_directory=run_directory,
            configuration=configuration,
            run_manifest_sha256=run_manifest_sha256,
            checkpoint_path=checkpoint_path,
            checkpoint=checkpoint,
        )
        if terminal is not None:
            return terminal
        if session_disk_preflight is None:
            session_disk_preflight = disk_preflight(
                configuration, max_iterations
            )

        session_deadline = (
            session_started + configuration.session_wall_seconds
        )
        worst_case_iteration_seconds = (
            2 * configuration.solver_wall_seconds
            + configuration.checker_wall_seconds
            + 5
        )
        for _ in range(max_iterations):
            if (
                session_deadline - time.perf_counter()
                < worst_case_iteration_seconds
            ):
                return _result_outcome(
                    "session_wall_exhausted",
                    checkpoint_path,
                    checkpoint,
                )
            assert_configuration_bindings(configuration)
            checkpoint_before_sha256 = checkpoint_state_sha256(checkpoint)
            history_chain_before_sha256 = str(
                checkpoint["history_chain_sha256"]
            )
            attempt_index = len(checkpoint["attempts"])  # type: ignore[arg-type]
            cut_count_before = len(checkpoint["cuts"])  # type: ignore[arg-type]
            attempt_directory = _new_attempt_directory(
                run_directory, attempt_index
            )
            (
                cuts_path,
                cnf_path,
                generator_manifest_path,
                encoding,
                parsed_cnf,
            ) = _generate_attempt_instance(
                configuration=configuration,
                checkpoint=checkpoint,
                attempt_directory=attempt_directory,
            )
            cnf_hash_before = sha256_file(cnf_path)
            result_path = attempt_directory / "solver.result"
            solver_stdout = attempt_directory / "solver.stdout"
            solver_stderr = attempt_directory / "solver.stderr"
            solver_command = _solver_command(
                configuration,
                cnf_path=cnf_path,
                result_path=result_path,
            )
            validate_file_roles(
                readonly={
                    "CNF": cnf_path,
                    "CaDiCaL": Path(configuration.cadical.path),
                },
                writable={
                    "solver result": result_path,
                    "solver stdout": solver_stdout,
                    "solver stderr": solver_stderr,
                },
            )
            solver = run_bounded_child(
                command=solver_command,
                cwd=run_directory,
                stdout_path=solver_stdout,
                stderr_path=solver_stderr,
                wall_limit_seconds=configuration.solver_wall_seconds,
                memory_limit_mib=configuration.solver_memory_mib,
                file_limit_mib=configuration.child_file_limit_mib,
                readonly_paths={"CNF": cnf_path},
            )
            if sha256_file(cnf_path) != cnf_hash_before:
                raise RuntimeError("CNF changed while CaDiCaL was running")
            assert_configuration_bindings(configuration)

            common_artifacts = {
                "cuts_input": cuts_path,
                "cnf": cnf_path,
                "generator_manifest": generator_manifest_path,
                "solver_stdout": solver_stdout,
                "solver_stderr": solver_stderr,
            }
            if result_path.exists():
                common_artifacts["solver_result"] = result_path

            if solver.timed_out or solver.memory_limit_exceeded:
                bounded_outcome = (
                    "solver_memory_limit"
                    if solver.memory_limit_exceeded
                    else "solver_timeout"
                )
                (
                    retained_artifacts,
                    compressed_artifacts,
                    reconstructible_artifacts,
                    storage,
                ) = _compact_intermediate_artifacts(
                    artifacts=common_artifacts,
                    checkpoint=checkpoint,
                    configuration=configuration,
                )
                attempt = _common_attempt_manifest(
                    attempt_index=attempt_index,
                    outcome=bounded_outcome,
                    configuration=configuration,
                    run_manifest_sha256=run_manifest_sha256,
                    checkpoint_before_sha256=checkpoint_before_sha256,
                    history_chain_before_sha256=history_chain_before_sha256,
                    cut_count_before=cut_count_before,
                    artifacts=retained_artifacts,
                    solver=solver,
                    session_invocation=session_invocation,
                    disk_preflight_report=session_disk_preflight,
                    compressed_artifacts=compressed_artifacts,
                    reconstructible_artifacts=reconstructible_artifacts,
                    storage=storage,
                )
                attempt_path = _write_attempt_manifest(
                    attempt_directory, attempt
                )
                if _attempt_directory_size(attempt_directory) > (
                    configuration.retained_attempt_limit_mib << 20
                ):
                    raise RuntimeError(
                        "compacted attempt exceeds retained-attempt limit"
                    )
                reference = _attempt_reference(
                    attempt_index, bounded_outcome, attempt_path
                )
                checkpoint = _commit_checkpoint(
                    checkpoint_path=checkpoint_path,
                    checkpoint=checkpoint,
                    attempt_reference=reference,
                    configuration=configuration,
                    run_manifest_path=run_manifest_path,
                    run_manifest_sha256=run_manifest_sha256,
                )
                return _result_outcome(
                    bounded_outcome, checkpoint_path, checkpoint
                )

            if solver.exit_code not in (0, 10, 20):
                raise RuntimeError(
                    f"CaDiCaL returned unexpected status {solver.exit_code}"
                )
            parsed_result = parse_solver_result_file(
                result_path, parsed_cnf.variable_count
            )

            if solver.exit_code == 0:
                if parsed_result.status != "UNKNOWN":
                    raise RuntimeError("CaDiCaL exit/model status mismatch")
                (
                    retained_artifacts,
                    compressed_artifacts,
                    reconstructible_artifacts,
                    storage,
                ) = _compact_intermediate_artifacts(
                    artifacts=common_artifacts,
                    checkpoint=checkpoint,
                    configuration=configuration,
                )
                attempt = _common_attempt_manifest(
                    attempt_index=attempt_index,
                    outcome="solver_unknown",
                    configuration=configuration,
                    run_manifest_sha256=run_manifest_sha256,
                    checkpoint_before_sha256=checkpoint_before_sha256,
                    history_chain_before_sha256=history_chain_before_sha256,
                    cut_count_before=cut_count_before,
                    artifacts=retained_artifacts,
                    solver=solver,
                    session_invocation=session_invocation,
                    disk_preflight_report=session_disk_preflight,
                    compressed_artifacts=compressed_artifacts,
                    reconstructible_artifacts=reconstructible_artifacts,
                    storage=storage,
                )
                attempt_path = _write_attempt_manifest(
                    attempt_directory, attempt
                )
                if _attempt_directory_size(attempt_directory) > (
                    configuration.retained_attempt_limit_mib << 20
                ):
                    raise RuntimeError(
                        "compacted attempt exceeds retained-attempt limit"
                    )
                reference = _attempt_reference(
                    attempt_index, "solver_unknown", attempt_path
                )
                checkpoint = _commit_checkpoint(
                    checkpoint_path=checkpoint_path,
                    checkpoint=checkpoint,
                    attempt_reference=reference,
                    configuration=configuration,
                    run_manifest_path=run_manifest_path,
                    run_manifest_sha256=run_manifest_sha256,
                )
                return _result_outcome(
                    "solver_unknown", checkpoint_path, checkpoint
                )

            if solver.exit_code == 10:
                if parsed_result.status != "SAT" or parsed_result.model is None:
                    raise RuntimeError("CaDiCaL exit/model status mismatch")
                model = parsed_result.model
                validate_model_satisfies_cnf(parsed_cnf, model)
                edges = encoding.decode_edges(model)
                family = encoding.decode_family(model)
                validate_decoded_candidate(encoding, edges, family)
                decoded_path = attempt_directory / "decoded-candidate.json"
                write_immutable(
                    decoded_path,
                    canonical_json_bytes(
                        _decoded_candidate_payload(edges, family)
                    ),
                )
                common_artifacts["decoded_candidate"] = decoded_path

                coloring_result = find_coloring(N, edges, 3)
                if coloring_result is None:
                    outcome = "candidate_review_pending"
                    attempt = _common_attempt_manifest(
                        attempt_index=attempt_index,
                        outcome=outcome,
                        configuration=configuration,
                        run_manifest_sha256=run_manifest_sha256,
                        checkpoint_before_sha256=checkpoint_before_sha256,
                        history_chain_before_sha256=history_chain_before_sha256,
                        cut_count_before=cut_count_before,
                        artifacts=common_artifacts,
                        solver=solver,
                        session_invocation=session_invocation,
                        disk_preflight_report=session_disk_preflight,
                    )
                    attempt["validation"] = {
                        "dimacs_exact": True,
                        "complete_model": True,
                        "all_clauses_satisfied": True,
                        "decoded_candidate_directly_validated": True,
                        "three_coloring": None,
                    }
                    attempt_path = _write_attempt_manifest(
                        attempt_directory, attempt
                    )
                    candidate_marker_path = (
                        run_directory / CANDIDATE_MARKER_NAME
                    )
                    terminal_record = _write_terminal_marker(
                        path=candidate_marker_path,
                        kind="candidate",
                        status_value=outcome,
                        configuration=configuration,
                        run_manifest_sha256=run_manifest_sha256,
                        checkpoint_before_sha256=checkpoint_before_sha256,
                        history_chain_before_sha256=history_chain_before_sha256,
                        attempt_manifest_path=attempt_path,
                    )
                    reference = _attempt_reference(
                        attempt_index, outcome, attempt_path
                    )
                    checkpoint = _commit_checkpoint(
                        checkpoint_path=checkpoint_path,
                        checkpoint=checkpoint,
                        attempt_reference=reference,
                        configuration=configuration,
                        run_manifest_path=run_manifest_path,
                        run_manifest_sha256=run_manifest_sha256,
                        status_value=outcome,
                        terminal=terminal_record,
                    )
                    return _result_outcome(
                        outcome,
                        checkpoint_path,
                        checkpoint,
                        candidate_marker_path,
                    )

                coloring = canonical_coloring(coloring_result)
                _proper_coloring(edges, coloring)
                existing = {
                    tuple(record["coloring"])
                    for record in checkpoint["cuts"]  # type: ignore[union-attr]
                }
                if coloring in existing:
                    raise RuntimeError(
                        "coloring oracle repeated an already committed partition"
                    )
                clause = same_color_cut(encoding, coloring)
                if any(model[literal] for literal in clause):
                    raise RuntimeError(
                        "same-color cut is not false in the current SAT model"
                    )
                coloring_path = attempt_directory / "coloring.json"
                write_immutable(coloring_path, coloring_bytes(coloring))
                common_artifacts["coloring"] = coloring_path
                (
                    retained_artifacts,
                    compressed_artifacts,
                    reconstructible_artifacts,
                    storage,
                ) = _compact_intermediate_artifacts(
                    artifacts=common_artifacts,
                    checkpoint=checkpoint,
                    configuration=configuration,
                )
                cut_payload = {
                    "index": cut_count_before,
                    "coloring": list(coloring),
                    "coloring_sha256": sha256_bytes(
                        coloring_bytes(coloring)
                    ),
                    "clause": list(clause),
                    "clause_sha256": sha256_bytes(clause_bytes(clause)),
                }
                outcome = "coloring_cut_committed"
                attempt = _common_attempt_manifest(
                    attempt_index=attempt_index,
                    outcome=outcome,
                    configuration=configuration,
                    run_manifest_sha256=run_manifest_sha256,
                    checkpoint_before_sha256=checkpoint_before_sha256,
                    history_chain_before_sha256=history_chain_before_sha256,
                    cut_count_before=cut_count_before,
                    artifacts=retained_artifacts,
                    solver=solver,
                    session_invocation=session_invocation,
                    disk_preflight_report=session_disk_preflight,
                    compressed_artifacts=compressed_artifacts,
                    reconstructible_artifacts=reconstructible_artifacts,
                    storage=storage,
                )
                attempt["validation"] = {
                    "dimacs_exact": True,
                    "complete_model": True,
                    "all_clauses_satisfied": True,
                    "decoded_candidate_directly_validated": True,
                    "proper_three_coloring_directly_validated": True,
                    "cut_false_in_current_model": True,
                }
                attempt["committed_cut"] = cut_payload
                attempt_path = _write_attempt_manifest(
                    attempt_directory, attempt
                )
                if _attempt_directory_size(attempt_directory) > (
                    configuration.retained_attempt_limit_mib << 20
                ):
                    raise RuntimeError(
                        "compacted attempt exceeds retained-attempt limit"
                    )
                reference = _attempt_reference(
                    attempt_index, outcome, attempt_path
                )
                cut_record = {
                    **cut_payload,
                    "source_attempt_index": attempt_index,
                    "source_attempt_manifest_path": str(
                        attempt_path.resolve()
                    ),
                    "source_attempt_manifest_sha256": sha256_file(
                        attempt_path
                    ),
                }
                checkpoint = _commit_checkpoint(
                    checkpoint_path=checkpoint_path,
                    checkpoint=checkpoint,
                    attempt_reference=reference,
                    configuration=configuration,
                    run_manifest_path=run_manifest_path,
                    run_manifest_sha256=run_manifest_sha256,
                    cut_record=cut_record,
                )
                continue

            if parsed_result.status != "UNSAT":
                raise RuntimeError("CaDiCaL exit/model status mismatch")
            proof_solver, checker, proof_artifacts = run_unsat_proof_replay(
                configuration=configuration,
                cnf_path=cnf_path,
                parsed_cnf=parsed_cnf,
                attempt_directory=attempt_directory,
            )
            assert_configuration_bindings(configuration)
            common_artifacts.update(proof_artifacts)
            outcome = "unsat_verified"
            attempt = _common_attempt_manifest(
                attempt_index=attempt_index,
                outcome=outcome,
                configuration=configuration,
                run_manifest_sha256=run_manifest_sha256,
                checkpoint_before_sha256=checkpoint_before_sha256,
                history_chain_before_sha256=history_chain_before_sha256,
                cut_count_before=cut_count_before,
                artifacts=common_artifacts,
                solver=solver,
                session_invocation=session_invocation,
                disk_preflight_report=session_disk_preflight,
            )
            attempt["proof_solver"] = asdict(proof_solver)
            attempt["proof_checker"] = asdict(checker)
            attempt["validation"] = {
                "initial_unsat": True,
                "identical_cnf_rerun": True,
                "proof_rerun_unsat": True,
                "drat_trim_flags": ["-I", "-f", "-W"],
                "drat_trim_exact_verified_line": True,
                "drat_trim_warning_free": True,
                "cnf_unchanged": True,
                "proof_unchanged_during_check": True,
            }
            attempt_path = _write_attempt_manifest(
                attempt_directory, attempt
            )
            unsat_marker_path = run_directory / UNSAT_MARKER_NAME
            terminal_record = _write_terminal_marker(
                path=unsat_marker_path,
                kind="unsat",
                status_value=outcome,
                configuration=configuration,
                run_manifest_sha256=run_manifest_sha256,
                checkpoint_before_sha256=checkpoint_before_sha256,
                history_chain_before_sha256=history_chain_before_sha256,
                attempt_manifest_path=attempt_path,
            )
            reference = _attempt_reference(
                attempt_index, outcome, attempt_path
            )
            checkpoint = _commit_checkpoint(
                checkpoint_path=checkpoint_path,
                checkpoint=checkpoint,
                attempt_reference=reference,
                configuration=configuration,
                run_manifest_path=run_manifest_path,
                run_manifest_sha256=run_manifest_sha256,
                status_value=outcome,
                terminal=terminal_record,
            )
            return _result_outcome(
                outcome,
                checkpoint_path,
                checkpoint,
                unsat_marker_path,
            )

        return _result_outcome(
            "iteration_budget_exhausted",
            checkpoint_path,
            checkpoint,
        )


def audit_run(
    *,
    template: str,
    run_directory: Path,
    cadical_path: Path,
    drat_trim_path: Path,
    solver_seed: int = 0,
    solver_wall_seconds: int = 900,
    solver_memory_mib: int = 4096,
    checker_wall_seconds: int = 900,
    checker_memory_mib: int = 4096,
    session_wall_seconds: int = 3600,
    disk_reserve_mib: int = 4096,
    child_file_limit_mib: int = 256,
    retained_attempt_limit_mib: int = 2,
    deep_reconstruct: bool = False,
    verify_terminal_proof: bool = False,
    instrumentation: AuditInstrumentation | None = None,
) -> RunOutcome:
    """Validate all committed bindings without launching a solver."""

    configuration = build_configuration(
        template=template,
        run_directory=run_directory,
        cadical_path=cadical_path,
        drat_trim_path=drat_trim_path,
        solver_seed=solver_seed,
        solver_wall_seconds=solver_wall_seconds,
        solver_memory_mib=solver_memory_mib,
        checker_wall_seconds=checker_wall_seconds,
        checker_memory_mib=checker_memory_mib,
        session_wall_seconds=session_wall_seconds,
        disk_reserve_mib=disk_reserve_mib,
        child_file_limit_mib=child_file_limit_mib,
        retained_attempt_limit_mib=retained_attempt_limit_mib,
    )
    run_directory = Path(configuration.run_directory)
    if not run_directory.is_dir():
        raise ValueError("run directory does not exist")
    for required_name, role in (
        (LOCK_NAME, "run lock"),
        (RUN_MANIFEST_NAME, "run manifest"),
        (CHECKPOINT_NAME, "checkpoint"),
    ):
        _assert_regular_single_link(
            run_directory / required_name, f"audit {role}"
        )
    with RunLock(run_directory, create=False):
        (
            _,
            checkpoint_path,
            run_manifest_sha256,
            checkpoint,
        ) = _prepare_run(
            configuration,
            initialize=False,
            deep_reconstruct=deep_reconstruct,
            verify_terminal_proof=False,
            instrumentation=instrumentation,
        )
        terminal = _terminal_outcome(
            run_directory=run_directory,
            configuration=configuration,
            run_manifest_sha256=run_manifest_sha256,
            checkpoint_path=checkpoint_path,
            checkpoint=checkpoint,
            instrumentation=instrumentation,
        )
        if verify_terminal_proof:
            if terminal is None or terminal.status != "unsat_verified":
                raise ValueError(
                    "live terminal-proof verification requires an UNSAT terminal"
                )
            marker = strict_json_file(Path(str(terminal.terminal_path)))
            if not isinstance(marker, dict):
                raise ValueError("UNSAT terminal marker is malformed")
            attempt = strict_json_file(
                Path(str(marker["attempt_manifest_path"]))
            )
            if not isinstance(attempt, dict):
                raise ValueError("UNSAT terminal attempt is malformed")
            artifacts = attempt["artifacts"]
            verify_stored_drat_certificate(
                configuration=configuration,
                cnf_path=Path(str(artifacts["cnf"]["path"])),
                proof_path=Path(str(artifacts["drat_proof"]["path"])),
            )
        if terminal is not None:
            return terminal
        return _result_outcome(
            "running_audit_passed", checkpoint_path, checkpoint
        )


def _parser() -> argparse.ArgumentParser:
    root = campaign_root()
    parser = argparse.ArgumentParser(
        description="Resumable proof-producing k=3 coloring-cut CEGAR"
    )
    parser.add_argument("--validation-gate-open", action="store_true")
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--template", choices=TEMPLATES, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--solver-wall-seconds", type=int, default=900)
    parser.add_argument("--solver-memory-mib", type=int, default=4096)
    parser.add_argument("--checker-wall-seconds", type=int, default=900)
    parser.add_argument("--checker-memory-mib", type=int, default=4096)
    parser.add_argument("--session-wall-seconds", type=int, default=3600)
    parser.add_argument("--disk-reserve-mib", type=int, default=4096)
    parser.add_argument("--child-file-limit-mib", type=int, default=256)
    parser.add_argument("--retained-attempt-limit-mib", type=int, default=2)
    parser.add_argument("--deep-reconstruct", action="store_true")
    parser.add_argument("--verify-terminal-proof", action="store_true")
    parser.add_argument(
        "--cadical",
        type=Path,
        default=root / "tools/cadical_3_0_1/build/cadical",
    )
    parser.add_argument(
        "--drat-trim",
        type=Path,
        default=root / "tools/drat_trim_2023_05_22/drat-trim",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    common = {
        "template": arguments.template,
        "run_directory": arguments.run_dir,
        "cadical_path": arguments.cadical,
        "drat_trim_path": arguments.drat_trim,
        "solver_seed": arguments.seed,
        "solver_wall_seconds": arguments.solver_wall_seconds,
        "solver_memory_mib": arguments.solver_memory_mib,
        "checker_wall_seconds": arguments.checker_wall_seconds,
        "checker_memory_mib": arguments.checker_memory_mib,
        "session_wall_seconds": arguments.session_wall_seconds,
        "disk_reserve_mib": arguments.disk_reserve_mib,
        "child_file_limit_mib": arguments.child_file_limit_mib,
        "retained_attempt_limit_mib": arguments.retained_attempt_limit_mib,
    }
    if arguments.audit_only:
        outcome = audit_run(
            **common,
            deep_reconstruct=arguments.deep_reconstruct,
            verify_terminal_proof=arguments.verify_terminal_proof,
        )
    else:
        if arguments.deep_reconstruct:
            raise SystemExit("--deep-reconstruct requires --audit-only")
        if arguments.verify_terminal_proof:
            raise SystemExit("--verify-terminal-proof requires --audit-only")
        if not arguments.validation_gate_open:
            raise SystemExit(
                "refusing to solve: pass --validation-gate-open only after "
                "the synthesis validation gate is explicitly open"
            )
        outcome = run_cegar(
            **common,
            max_iterations=arguments.max_iterations,
        )
    print(json.dumps(asdict(outcome), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
