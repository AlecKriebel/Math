"""Fail-closed, resumable proof production for the frozen order-12 k=4 CNF.

There are deliberately three separate operations:

``initialize``
    Create an exclusive run directory and its immutable 16-cube partition.
    This never starts a solver.

``run-next``
    Run at most one leaf through the solver, an independent forward replay
    of the raw binary DRAT proof, a separate backward LRAT conversion, and
    LRAT replay.  An explicit production gate is required.

``audit``
    Rehash immutable inputs, tools, sources, checkpoints, and attempts without
    starting a solver.

SAT is always candidate-only.  A leaf is called ``UNSAT_LRAT_VERIFIED`` only
after warning-fatal drat-trim first verifies the raw binary DRAT proof in
forward mode, a second warning-fatal drat-trim process converts the same raw
proof to LRAT in backward mode, and the resulting LRAT is replayed by the
separately pinned lrat-check binary.  Even sixteen such leaves remain pending
an independent aggregate coverage audit.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import math
import os
import platform
import re
import shutil
import signal
import stat
import subprocess
import sys
import time
from dataclasses import asdict
from itertools import combinations, product
from pathlib import Path
from typing import Mapping, Sequence

from synthesis_k3.cegar import (
    ChildResult,
    RunLock,
    _available_memory_bytes,
    parse_dimacs_bytes,
    parse_solver_result_bytes,
    run_bounded_child,
    validate_model_satisfies_cnf,
    verify_pinned_tools,
)


SCHEMA_VERSION = 1
PROOF_PIPELINE_ID = "binary-drat-forward-check-backward-lrat-v2"
EXPECTED_PARENT_CNF_SHA256 = (
    "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac"
)
EXPECTED_PARENT_MANIFEST_SHA256 = (
    "621a0878c117dc8b4d6dbd0ba14c8402a8c24e8339d2f85cb23d61ffd74fbb61"
)
EXPECTED_PARENT_SIZE_BYTES = 3_992_947
EXPECTED_VARIABLE_COUNT = 18_381
EXPECTED_PARENT_CLAUSE_COUNT = 114_742
EXPECTED_PARENT_LITERAL_COUNT = 1_180_016
CASE_CLAUSE_COUNT = EXPECTED_PARENT_CLAUSE_COUNT + 4
CASE_LITERAL_COUNT = EXPECTED_PARENT_LITERAL_COUNT + 4

# e_(0,4), e_(1,4), e_(2,4), e_(3,4), in the lexicographic edge layout.
DEFAULT_CUBE_VARIABLES = (4, 14, 23, 31)
DEFAULT_CUBE_LABELS = ("e_0_4", "e_1_4", "e_2_4", "e_3_4")

CADICAL_BINARY_SHA256 = (
    "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
)
CADICAL_ARCHIVE_SHA256 = (
    "2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e"
)
DRAT_TRIM_BINARY_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
LRAT_CHECK_BINARY_SHA256 = (
    "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2"
)
DRAT_TOOL_ARCHIVE_SHA256 = (
    "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108"
)

PARENT_COPY_NAME = "parent.cnf"
PARENT_MANIFEST_COPY_NAME = "parent-generator-manifest.json"
RUN_MANIFEST_NAME = "run-manifest.json"
PARTITION_NAME = "partition.json"
CHECKPOINT_DIRECTORY_NAME = "checkpoints"
CASE_DIRECTORY_NAME = "cases"
CHECKPOINT_PATTERN = re.compile(r"checkpoint-([0-9]{6})\.json\Z")
CASE_PATTERN = re.compile(r"case-([01]{4})\Z")
ATTEMPT_PATTERN = re.compile(r"attempt-([0-9]{6})\Z")

ALLOWED_CASE_STATUSES = frozenset(
    {
        "PENDING",
        "RUNNING_UNFINISHED_NONCLAIM",
        "RETRYABLE_NONCLAIM",
        "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION",
        "UNSAT_LRAT_VERIFIED",
    }
)
RETRYABLE_OUTCOMES = frozenset(
    {
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
)

RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/search/k4_production/__init__.py",
    "src/search/k4_production/__main__.py",
    "src/search/k4_production/runner.py",
    "src/synthesis_k3/cegar.py",
    "src/synthesis_k3/coloring.py",
    "src/synthesis_k3/encoding.py",
    "src/synthesis_k3/generate.py",
    "math/lemmas/order12_k4_partition_plan.md",
)

DEFAULT_SOLVER_WALL_SECONDS = 1_800
DEFAULT_CONVERTER_WALL_SECONDS = 1_800
DEFAULT_CHECKER_WALL_SECONDS = 1_800
DEFAULT_SOLVER_MEMORY_MIB = 4_096
DEFAULT_POSTPROCESS_MEMORY_MIB = 4_096
DEFAULT_FILE_LIMIT_MIB = 768
DEFAULT_DISK_RESERVE_MIB = 6_144
DEFAULT_MEMORY_RESERVE_MIB = 2_048
DEFAULT_LOAD_MAX = 7.5
MAX_WALL_SECONDS = 21_600
MAX_FILE_LIMIT_MIB = 4_096
MIN_DISK_RESERVE_MIB = 4_096
MIN_MEMORY_RESERVE_MIB = 512
WORST_CASE_LIVE_FILE_SLOTS = 11
DISK_METADATA_ALLOWANCE_MIB = 64


def campaign_root() -> Path:
    return Path(__file__).resolve().parents[3]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(payload: object) -> bytes:
    encoded = json.dumps(
        payload,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    )
    return (encoded + "\n").encode("utf-8")


def _strict_json_bytes(payload: bytes) -> object:
    def reject_constant(value: str) -> object:
        raise ValueError(f"non-finite JSON constant {value!r}")

    def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
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
            object_pairs_hook=no_duplicates,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("malformed JSON") from error


def _strict_json_file(path: Path) -> object:
    _assert_regular_single_link(path, "JSON artifact")
    return _strict_json_bytes(path.read_bytes())


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


def _write_exclusive(path: Path, payload: bytes) -> None:
    """Create one durable regular file without following or replacing links."""

    _assert_no_symlink_components(path.parent)
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass
        raise
    _fsync_directory(path.parent)


def _file_binding(path: Path, role: str) -> dict[str, object]:
    _assert_regular_single_link(path, role)
    return {
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _optional_file_binding(path: Path, role: str) -> dict[str, object] | None:
    if not path.exists() and not path.is_symlink():
        return None
    return _file_binding(path, role)


def _verify_file_binding(record: Mapping[str, object], role: str) -> None:
    if set(record) != {"path", "sha256", "size_bytes"}:
        raise ValueError(f"{role} binding shape is wrong")
    raw_path = record["path"]
    digest = record["sha256"]
    size = record["size_bytes"]
    if (
        type(raw_path) is not str
        or type(digest) is not str
        or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        or type(size) is not int
        or size < 0
    ):
        raise ValueError(f"{role} binding is malformed")
    path = Path(raw_path)
    _assert_regular_single_link(path, role)
    if path.stat().st_size != size or sha256_file(path) != digest:
        raise ValueError(f"{role} binding no longer holds")


def _exact_int(
    value: object,
    role: str,
    *,
    minimum: int,
    maximum: int,
) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(
            f"{role} must be an exact integer in {minimum}..{maximum}"
        )
    return value


def _exact_finite_number(
    value: object,
    role: str,
    *,
    minimum: float,
    maximum: float,
) -> float:
    if type(value) not in (int, float):
        raise ValueError(f"{role} must be an exact finite number")
    result = float(value)
    if not math.isfinite(result) or not minimum <= result <= maximum:
        raise ValueError(f"{role} must be in {minimum}..{maximum}")
    return result


def _require_gate(value: object, role: str) -> None:
    if value is not True:
        raise PermissionError(f"explicit {role} gate is required")


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


def _hardware_report() -> dict[str, object]:
    logical = os.cpu_count()
    if type(logical) is not int or logical < 1:
        raise ValueError("logical CPU count is invalid")
    physical = _physical_memory_bytes()
    brand = platform.processor()
    if sys.platform == "darwin":
        completed = subprocess.run(
            ("/usr/sbin/sysctl", "-n", "machdep.cpu.brand_string"),
            cwd=campaign_root(),
            env={},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
            timeout=5,
        )
        if completed.returncode == 0:
            brand = completed.stdout.decode("utf-8", "strict").strip()
    return {
        "logical_cpu_count": logical,
        "physical_memory_bytes": physical,
        "machine": platform.machine(),
        "processor": brand,
        "platform": platform.platform(),
        "python_executable": str(Path(sys.executable).resolve()),
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
    }


def _git_output(arguments: Sequence[str]) -> str:
    completed = subprocess.run(
        ("git", *arguments),
        cwd=campaign_root(),
        env={},
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        raise ValueError(
            f"Git binding command failed: {' '.join(arguments)}"
        )
    return completed.stdout.decode("ascii", "strict").strip()


def _committed_source_binding() -> dict[str, object]:
    """Bind only runtime paths, allowing unrelated worktree changes."""

    head = _git_output(("rev-parse", "HEAD"))
    records: list[dict[str, object]] = []
    for relative in RUNTIME_SOURCE_RELATIVE_PATHS:
        path = campaign_root() / relative
        _assert_regular_single_link(path, f"runtime source {relative}")
        worktree_blob = _git_output(("hash-object", "--", relative))
        # Revision paths are repository-root-relative unless ``./`` is used.
        # Git runs from the campaign subdirectory, so retain that prefix
        # instead of accidentally looking for ``src/...`` at the repo root.
        head_blob = _git_output(("rev-parse", f"HEAD:./{relative}"))
        if worktree_blob != head_blob:
            raise ValueError(
                f"runtime source is not committed byte-for-byte: {relative}"
            )
        records.append(
            {
                "path": relative,
                "git_blob": head_blob,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    source_set_sha256 = sha256_bytes(canonical_json_bytes(records))
    return {
        "head_at_creation": head,
        "global_worktree_cleanliness_required": False,
        "records": records,
        "source_set_sha256": source_set_sha256,
    }


def _verify_committed_source_binding(binding: Mapping[str, object]) -> None:
    if set(binding) != {
        "head_at_creation",
        "global_worktree_cleanliness_required",
        "records",
        "source_set_sha256",
    }:
        raise ValueError("runtime source binding shape is wrong")
    records = binding["records"]
    if (
        not isinstance(records, list)
        or binding["global_worktree_cleanliness_required"] is not False
        or type(binding["source_set_sha256"]) is not str
    ):
        raise ValueError("runtime source binding is malformed")
    expected_paths = list(RUNTIME_SOURCE_RELATIVE_PATHS)
    if [record.get("path") for record in records if isinstance(record, dict)] != (
        expected_paths
    ):
        raise ValueError("runtime source path sequence differs")
    if sha256_bytes(canonical_json_bytes(records)) != binding["source_set_sha256"]:
        raise ValueError("runtime source-set digest differs")
    for record in records:
        if not isinstance(record, dict) or set(record) != {
            "path",
            "git_blob",
            "sha256",
            "size_bytes",
        }:
            raise ValueError("runtime source record is malformed")
        relative = record["path"]
        if type(relative) is not str:
            raise ValueError("runtime source path is malformed")
        path = campaign_root() / relative
        _assert_regular_single_link(path, f"runtime source {relative}")
        if (
            path.stat().st_size != record["size_bytes"]
            or sha256_file(path) != record["sha256"]
            or _git_output(("hash-object", "--", relative))
            != record["git_blob"]
            or _git_output(("rev-parse", f"HEAD:./{relative}"))
            != record["git_blob"]
        ):
            raise ValueError(f"runtime source binding changed: {relative}")


def _tool_bindings() -> dict[str, object]:
    root = campaign_root()
    cadical_path = root / "tools/cadical_3_0_1/build/cadical"
    drat_trim_path = root / "tools/drat_trim_2023_05_22/drat-trim"
    lrat_check_path = root / "tools/drat_trim_2023_05_22/lrat-check"
    cadical, drat_trim = verify_pinned_tools(cadical_path, drat_trim_path)
    if cadical.sha256 != CADICAL_BINARY_SHA256:
        raise ValueError("CaDiCaL hash differs from the production pin")
    if drat_trim.sha256 != DRAT_TRIM_BINARY_SHA256:
        raise ValueError("drat-trim hash differs from the production pin")
    _assert_regular_single_link(lrat_check_path, "lrat-check")
    if not os.access(lrat_check_path, os.X_OK):
        raise ValueError("lrat-check is not executable")
    lrat_hash = sha256_file(lrat_check_path)
    if lrat_hash != LRAT_CHECK_BINARY_SHA256:
        raise ValueError("lrat-check hash differs from the production pin")
    archive = Path(drat_trim.source_archive_path)
    if (
        drat_trim.source_archive_sha256 != DRAT_TOOL_ARCHIVE_SHA256
        or sha256_file(archive) != DRAT_TOOL_ARCHIVE_SHA256
    ):
        raise ValueError("DRAT tool source archive differs from the pin")
    return {
        "cadical": asdict(cadical),
        "drat_trim": asdict(drat_trim),
        "lrat_check": {
            "role": "lrat-check",
            "path": str(lrat_check_path.resolve()),
            "sha256": lrat_hash,
            "source_archive_path": str(archive.resolve()),
            "source_archive_sha256": DRAT_TOOL_ARCHIVE_SHA256,
            "commit": drat_trim.commit,
            "version": None,
        },
    }


def _verify_tool_bindings(bindings: Mapping[str, object]) -> None:
    if set(bindings) != {"cadical", "drat_trim", "lrat_check"}:
        raise ValueError("tool binding roles differ")
    expected = {
        "cadical": (CADICAL_BINARY_SHA256, CADICAL_ARCHIVE_SHA256),
        "drat_trim": (
            DRAT_TRIM_BINARY_SHA256,
            DRAT_TOOL_ARCHIVE_SHA256,
        ),
        "lrat_check": (
            LRAT_CHECK_BINARY_SHA256,
            DRAT_TOOL_ARCHIVE_SHA256,
        ),
    }
    for role, (expected_hash, expected_archive) in expected.items():
        record = bindings[role]
        if not isinstance(record, dict):
            raise ValueError(f"{role} tool record is malformed")
        path = Path(str(record.get("path")))
        archive = Path(str(record.get("source_archive_path")))
        _assert_regular_single_link(path, role)
        _assert_regular_single_link(archive, f"{role} source archive")
        if (
            not os.access(path, os.X_OK)
            or
            record.get("sha256") != expected_hash
            or sha256_file(path) != expected_hash
            or record.get("source_archive_sha256") != expected_archive
            or sha256_file(archive) != expected_archive
        ):
            raise ValueError(f"{role} tool binding changed")


def _validate_parent(
    cnf_path: Path,
    manifest_path: Path,
) -> tuple[bytes, bytes]:
    _assert_regular_single_link(cnf_path, "parent CNF")
    _assert_regular_single_link(manifest_path, "parent generator manifest")
    cnf_bytes = cnf_path.read_bytes()
    manifest_bytes = manifest_path.read_bytes()
    if (
        len(cnf_bytes) != EXPECTED_PARENT_SIZE_BYTES
        or sha256_bytes(cnf_bytes) != EXPECTED_PARENT_CNF_SHA256
        or sha256_bytes(manifest_bytes) != EXPECTED_PARENT_MANIFEST_SHA256
    ):
        raise ValueError("parent input bytes differ from the frozen pins")
    parsed = parse_dimacs_bytes(cnf_bytes)
    if (
        parsed.variable_count != EXPECTED_VARIABLE_COUNT
        or len(parsed.clauses) != EXPECTED_PARENT_CLAUSE_COUNT
        or sum(map(len, parsed.clauses)) != EXPECTED_PARENT_LITERAL_COUNT
    ):
        raise ValueError("parent DIMACS census differs from the frozen census")
    manifest = _strict_json_bytes(manifest_bytes)
    if not isinstance(manifest, dict) or (
        manifest.get("cnf_sha256") != EXPECTED_PARENT_CNF_SHA256
        or manifest.get("variable_count") != EXPECTED_VARIABLE_COUNT
        or manifest.get("clause_count") != EXPECTED_PARENT_CLAUSE_COUNT
        or manifest.get("literal_count") != EXPECTED_PARENT_LITERAL_COUNT
        or manifest.get("claim_status") != "NO_MATHEMATICAL_CLAIM"
    ):
        raise ValueError("parent generator manifest disagrees with the pin")
    return cnf_bytes, manifest_bytes


def _case_cnf_bytes(parent: bytes, literals: Sequence[int]) -> bytes:
    if (
        len(literals) != 4
        or len({abs(literal) for literal in literals}) != 4
        or any(
            type(literal) is not int
            or literal == 0
            or abs(literal) > EXPECTED_VARIABLE_COUNT
            for literal in literals
        )
    ):
        raise ValueError("a top-level cube must contain four distinct literals")
    newline = parent.find(b"\n")
    if newline < 0:
        raise ValueError("parent DIMACS has no header terminator")
    expected_header = (
        f"p cnf {EXPECTED_VARIABLE_COUNT} "
        f"{EXPECTED_PARENT_CLAUSE_COUNT}\n"
    ).encode("ascii")
    if parent[: newline + 1] != expected_header:
        raise ValueError("parent DIMACS header differs")
    header = f"p cnf {EXPECTED_VARIABLE_COUNT} {CASE_CLAUSE_COUNT}\n".encode(
        "ascii"
    )
    units = b"".join(f"{literal} 0\n".encode("ascii") for literal in literals)
    result = header + parent[newline + 1 :] + units
    return result


def _partition_payload(parent: bytes, base_seed: int) -> dict[str, object]:
    cases: list[dict[str, object]] = []
    for index, bits in enumerate(product((0, 1), repeat=4)):
        literals = tuple(
            variable if bit else -variable
            for variable, bit in zip(DEFAULT_CUBE_VARIABLES, bits, strict=True)
        )
        case_bytes = _case_cnf_bytes(parent, literals)
        case_id = "".join(map(str, bits))
        cases.append(
            {
                "case_id": case_id,
                "case_index": index,
                "cube_bits": list(bits),
                "cube_literals": list(literals),
                "seed": base_seed + index,
                "cnf_sha256": sha256_bytes(case_bytes),
                "cnf_size_bytes": len(case_bytes),
                "variable_count": EXPECTED_VARIABLE_COUNT,
                "clause_count": CASE_CLAUSE_COUNT,
                "literal_count": CASE_LITERAL_COUNT,
            }
        )
    return {
        "schema": "gamma-theta-order12-k4-boolean-cube-partition-v1",
        "schema_version": SCHEMA_VERSION,
        "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
        "aggregate_terminal_status": (
            "ALL_LEAVES_VERIFIED_PENDING_INDEPENDENT_COVERAGE_AUDIT"
        ),
        "coverage_basis": (
            "All 2^4 total assignments to four distinct Boolean variables; "
            "every total parent assignment belongs to exactly one cube."
        ),
        "parent_cnf_sha256": EXPECTED_PARENT_CNF_SHA256,
        "cube_variables": list(DEFAULT_CUBE_VARIABLES),
        "cube_variable_labels": list(DEFAULT_CUBE_LABELS),
        "case_count": 16,
        "cases": cases,
    }


def _validate_partition(partition: Mapping[str, object], parent: bytes) -> None:
    if (
        partition.get("schema")
        != "gamma-theta-order12-k4-boolean-cube-partition-v1"
        or partition.get("schema_version") != SCHEMA_VERSION
        or partition.get("claim_status") != "NO_SAT_OR_UNSAT_CLAIM"
        or partition.get("parent_cnf_sha256") != EXPECTED_PARENT_CNF_SHA256
        or partition.get("cube_variables") != list(DEFAULT_CUBE_VARIABLES)
        or partition.get("cube_variable_labels") != list(DEFAULT_CUBE_LABELS)
        or partition.get("case_count") != 16
    ):
        raise ValueError("partition header is malformed")
    cases = partition.get("cases")
    if not isinstance(cases, list) or len(cases) != 16:
        raise ValueError("partition does not contain 16 cases")
    observed_bits: set[tuple[int, ...]] = set()
    for index, record in enumerate(cases):
        if not isinstance(record, dict):
            raise ValueError("partition case is not an object")
        bits_raw = record.get("cube_bits")
        literals_raw = record.get("cube_literals")
        if (
            not isinstance(bits_raw, list)
            or tuple(bits_raw) not in set(product((0, 1), repeat=4))
            or not isinstance(literals_raw, list)
        ):
            raise ValueError("partition cube is malformed")
        bits = tuple(bits_raw)
        if bits in observed_bits:
            raise ValueError("partition repeats a cube")
        observed_bits.add(bits)
        expected_literals = [
            variable if bit else -variable
            for variable, bit in zip(
                DEFAULT_CUBE_VARIABLES, bits, strict=True
            )
        ]
        case_bytes = _case_cnf_bytes(parent, expected_literals)
        expected_id = "".join(map(str, bits))
        if (
            record.get("case_id") != expected_id
            or record.get("case_index") != index
            or literals_raw != expected_literals
            or type(record.get("seed")) is not int
            or record.get("cnf_sha256") != sha256_bytes(case_bytes)
            or record.get("cnf_size_bytes") != len(case_bytes)
            or record.get("variable_count") != EXPECTED_VARIABLE_COUNT
            or record.get("clause_count") != CASE_CLAUSE_COUNT
            or record.get("literal_count") != CASE_LITERAL_COUNT
        ):
            raise ValueError(f"partition case {expected_id} differs")
    if observed_bits != set(product((0, 1), repeat=4)):
        raise ValueError("partition does not cover the full four-cube")


def _validate_limits(
    *,
    solver_wall_seconds: int,
    converter_wall_seconds: int,
    checker_wall_seconds: int,
    solver_memory_mib: int,
    postprocess_memory_mib: int,
    file_limit_mib: int,
    disk_reserve_mib: int,
    memory_reserve_mib: int,
    load_max: float,
    physical_memory_bytes: int,
) -> dict[str, object]:
    solver_wall_seconds = _exact_int(
        solver_wall_seconds,
        "solver wall seconds",
        minimum=1,
        maximum=MAX_WALL_SECONDS,
    )
    converter_wall_seconds = _exact_int(
        converter_wall_seconds,
        "converter wall seconds",
        minimum=1,
        maximum=MAX_WALL_SECONDS,
    )
    checker_wall_seconds = _exact_int(
        checker_wall_seconds,
        "checker wall seconds",
        minimum=1,
        maximum=MAX_WALL_SECONDS,
    )
    solver_memory_mib = _exact_int(
        solver_memory_mib,
        "solver memory MiB",
        minimum=64,
        maximum=1 << 20,
    )
    postprocess_memory_mib = _exact_int(
        postprocess_memory_mib,
        "postprocess memory MiB",
        minimum=64,
        maximum=1 << 20,
    )
    maximum_responsive_mib = math.floor(
        physical_memory_bytes * 0.75 / (1 << 20)
    )
    if max(solver_memory_mib, postprocess_memory_mib) > maximum_responsive_mib:
        raise ValueError("child memory limit exceeds 75% of physical RAM")
    file_limit_mib = _exact_int(
        file_limit_mib,
        "per-file limit MiB",
        minimum=16,
        maximum=MAX_FILE_LIMIT_MIB,
    )
    disk_reserve_mib = _exact_int(
        disk_reserve_mib,
        "disk reserve MiB",
        minimum=MIN_DISK_RESERVE_MIB,
        maximum=1 << 20,
    )
    memory_reserve_mib = _exact_int(
        memory_reserve_mib,
        "memory reserve MiB",
        minimum=MIN_MEMORY_RESERVE_MIB,
        maximum=1 << 20,
    )
    load_max = _exact_finite_number(
        load_max,
        "load ceiling",
        minimum=0.1,
        maximum=1_000.0,
    )
    return {
        "solver_wall_seconds": solver_wall_seconds,
        "converter_wall_seconds": converter_wall_seconds,
        "checker_wall_seconds": checker_wall_seconds,
        "solver_memory_mib": solver_memory_mib,
        "postprocess_memory_mib": postprocess_memory_mib,
        "file_limit_mib": file_limit_mib,
        "disk_reserve_mib": disk_reserve_mib,
        "memory_reserve_mib": memory_reserve_mib,
        "load_max": load_max,
        "maximum_responsive_child_memory_mib": maximum_responsive_mib,
        "worst_case_live_file_slots": WORST_CASE_LIVE_FILE_SLOTS,
    }


def _summary_for_cases(cases: Sequence[Mapping[str, object]]) -> str:
    statuses = [record.get("status") for record in cases]
    if any(
        status == "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION"
        for status in statuses
    ):
        return "SAT_CANDIDATE_HOLD_NONCLAIM"
    if statuses and all(status == "UNSAT_LRAT_VERIFIED" for status in statuses):
        return "ALL_LEAVES_VERIFIED_PENDING_INDEPENDENT_COVERAGE_AUDIT"
    if any(status == "RUNNING_UNFINISHED_NONCLAIM" for status in statuses):
        return "INCOMPLETE_ACTIVE_NONCLAIM"
    return "INCOMPLETE_NONCLAIM"


def _initial_case_states(partition: Mapping[str, object]) -> list[dict[str, object]]:
    raw_cases = partition["cases"]
    if not isinstance(raw_cases, list):
        raise ValueError("partition cases are malformed")
    return [
        {
            "case_id": record["case_id"],
            "status": "PENDING",
            "attempt_count": 0,
            "active_attempt": None,
            "last_completed_outcome_sha256": None,
        }
        for record in raw_cases
        if isinstance(record, dict)
    ]


def _checkpoint_payload(
    *,
    sequence: int,
    previous_checkpoint_sha256: str | None,
    run_manifest_sha256: str,
    partition_sha256: str,
    cases: Sequence[Mapping[str, object]],
    event: Mapping[str, object],
) -> dict[str, object]:
    return {
        "schema": "gamma-theta-order12-k4-production-checkpoint-v1",
        "schema_version": SCHEMA_VERSION,
        "sequence": sequence,
        "previous_checkpoint_sha256": previous_checkpoint_sha256,
        "run_manifest_sha256": run_manifest_sha256,
        "partition_sha256": partition_sha256,
        "cases": [dict(record) for record in cases],
        "aggregate_status": _summary_for_cases(cases),
        "claim_boundary": (
            "No aggregate SAT/UNSAT claim is made. SAT is candidate-only; "
            "all verified UNSAT leaves still require an independent coverage "
            "and proof replay."
        ),
        "event": dict(event),
        "written_unix_ns": time.time_ns(),
    }


def _write_checkpoint(
    run_directory: Path,
    payload: Mapping[str, object],
) -> dict[str, object]:
    sequence = payload.get("sequence")
    if type(sequence) is not int or sequence < 0:
        raise ValueError("checkpoint sequence is malformed")
    path = (
        run_directory
        / CHECKPOINT_DIRECTORY_NAME
        / f"checkpoint-{sequence:06d}.json"
    )
    _write_exclusive(path, canonical_json_bytes(payload))
    return _file_binding(path, "checkpoint")


def _safe_new_run_directory(path: Path) -> Path:
    _assert_no_symlink_components(path)
    resolved = path.resolve(strict=False)
    root = campaign_root().resolve()
    forbidden = {
        root,
        Path(resolved.anchor),
        Path.home().resolve(),
        (root / "src").resolve(),
        (root / "math").resolve(),
        (root / "tests").resolve(),
        (root / "tools").resolve(),
        (root / "instances").resolve(),
    }
    if resolved in forbidden:
        raise ValueError(f"unsafe run directory: {resolved}")
    for protected in (
        root / "src",
        root / "math",
        root / "tests",
        root / "tools",
        root / "instances",
    ):
        try:
            resolved.relative_to(protected.resolve())
        except ValueError:
            pass
        else:
            raise ValueError(f"run directory lies in protected tree: {resolved}")
    if resolved.exists() or resolved.is_symlink():
        raise FileExistsError(
            f"exclusive run directory already exists: {resolved}"
        )
    resolved.parent.mkdir(parents=True, exist_ok=True)
    _assert_no_symlink_components(resolved.parent)
    os.mkdir(resolved, 0o700)
    _fsync_directory(resolved.parent)
    return resolved


def initialize_run(
    *,
    run_directory: Path,
    parent_cnf: Path | None = None,
    parent_manifest: Path | None = None,
    base_seed: int = 0,
    solver_wall_seconds: int = DEFAULT_SOLVER_WALL_SECONDS,
    converter_wall_seconds: int = DEFAULT_CONVERTER_WALL_SECONDS,
    checker_wall_seconds: int = DEFAULT_CHECKER_WALL_SECONDS,
    solver_memory_mib: int = DEFAULT_SOLVER_MEMORY_MIB,
    postprocess_memory_mib: int = DEFAULT_POSTPROCESS_MEMORY_MIB,
    file_limit_mib: int = DEFAULT_FILE_LIMIT_MIB,
    disk_reserve_mib: int = DEFAULT_DISK_RESERVE_MIB,
    memory_reserve_mib: int = DEFAULT_MEMORY_RESERVE_MIB,
    load_max: float = DEFAULT_LOAD_MAX,
    validation_gate_open: bool = False,
) -> dict[str, object]:
    """Create a new immutable production plan without running a solver."""

    _require_gate(validation_gate_open, "initialization validation")
    base_seed = _exact_int(
        base_seed,
        "base seed",
        minimum=0,
        maximum=2_000_000_000 - 15,
    )
    root = campaign_root()
    if parent_cnf is None:
        parent_cnf = (
            root / "instances/order12_k4_connected_parent/instance.cnf"
        )
    if parent_manifest is None:
        parent_manifest = (
            root / "instances/order12_k4_connected_parent/manifest.json"
        )
    parent_bytes, parent_manifest_bytes = _validate_parent(
        parent_cnf, parent_manifest
    )
    hardware = _hardware_report()
    physical = hardware["physical_memory_bytes"]
    if type(physical) is not int:
        raise ValueError("hardware report has malformed physical memory")
    limits = _validate_limits(
        solver_wall_seconds=solver_wall_seconds,
        converter_wall_seconds=converter_wall_seconds,
        checker_wall_seconds=checker_wall_seconds,
        solver_memory_mib=solver_memory_mib,
        postprocess_memory_mib=postprocess_memory_mib,
        file_limit_mib=file_limit_mib,
        disk_reserve_mib=disk_reserve_mib,
        memory_reserve_mib=memory_reserve_mib,
        load_max=load_max,
        physical_memory_bytes=physical,
    )
    sources = _committed_source_binding()
    tools = _tool_bindings()
    partition = _partition_payload(parent_bytes, base_seed)
    _validate_partition(partition, parent_bytes)

    run_directory = _safe_new_run_directory(run_directory)
    try:
        (run_directory / CHECKPOINT_DIRECTORY_NAME).mkdir(mode=0o700)
        (run_directory / CASE_DIRECTORY_NAME).mkdir(mode=0o700)
        for record in partition["cases"]:  # type: ignore[index]
            if not isinstance(record, dict):
                raise ValueError("partition case is malformed")
            (
                run_directory
                / CASE_DIRECTORY_NAME
                / f"case-{record['case_id']}"
            ).mkdir(mode=0o700)

        parent_copy = run_directory / PARENT_COPY_NAME
        parent_manifest_copy = run_directory / PARENT_MANIFEST_COPY_NAME
        _write_exclusive(parent_copy, parent_bytes)
        _write_exclusive(parent_manifest_copy, parent_manifest_bytes)
        partition_path = run_directory / PARTITION_NAME
        _write_exclusive(partition_path, canonical_json_bytes(partition))
        partition_binding = _file_binding(partition_path, "partition")

        run_manifest = {
            "schema": "gamma-theta-order12-k4-production-run-v1",
            "schema_version": SCHEMA_VERSION,
            "proof_pipeline": PROOF_PIPELINE_ID,
            "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
            "run_directory": str(run_directory),
            "campaign_root": str(root.resolve()),
            "original_parent_cnf": _file_binding(
                parent_cnf, "original parent CNF"
            ),
            "original_parent_generator_manifest": _file_binding(
                parent_manifest, "original parent generator manifest"
            ),
            "retained_parent_cnf": _file_binding(
                parent_copy, "retained parent CNF"
            ),
            "retained_parent_generator_manifest": _file_binding(
                parent_manifest_copy,
                "retained parent generator manifest",
            ),
            "partition": partition_binding,
            "base_seed": base_seed,
            "limits": limits,
            "hardware": hardware,
            "runtime_sources": sources,
            "tools": tools,
            "normalized_resume_invocation": [
                "/usr/bin/env",
                f"PYTHONPATH={root / 'src'}",
                str(Path(sys.executable).resolve()),
                "-m",
                "search.k4_production",
                "run-next",
                "--production-gate-open",
                "--run-dir",
                str(run_directory),
            ],
            "created_unix_ns": time.time_ns(),
        }
        run_manifest_path = run_directory / RUN_MANIFEST_NAME
        _write_exclusive(
            run_manifest_path, canonical_json_bytes(run_manifest)
        )
        run_binding = _file_binding(run_manifest_path, "run manifest")
        initial_cases = _initial_case_states(partition)
        checkpoint = _checkpoint_payload(
            sequence=0,
            previous_checkpoint_sha256=None,
            run_manifest_sha256=str(run_binding["sha256"]),
            partition_sha256=str(partition_binding["sha256"]),
            cases=initial_cases,
            event={
                "kind": "INITIALIZED_NO_SOLVER_RUN",
                "base_seed": base_seed,
                "case_count": 16,
            },
        )
        checkpoint_binding = _write_checkpoint(run_directory, checkpoint)
        _fsync_directory(run_directory)
    except BaseException:
        # Deliberately retain a partially initialized exclusive directory for
        # forensic inspection.  It must never be silently reused.
        raise
    return {
        "status": "INITIALIZED_NO_SOLVER_RUN",
        "run_directory": str(run_directory),
        "run_manifest_sha256": run_binding["sha256"],
        "partition_sha256": partition_binding["sha256"],
        "checkpoint_sha256": checkpoint_binding["sha256"],
        "case_count": 16,
        "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
    }


def _case_state_shape(record: object, expected_id: str) -> dict[str, object]:
    if not isinstance(record, dict) or set(record) != {
        "case_id",
        "status",
        "attempt_count",
        "active_attempt",
        "last_completed_outcome_sha256",
    }:
        raise ValueError(f"case state {expected_id} has the wrong shape")
    if (
        record["case_id"] != expected_id
        or record["status"] not in ALLOWED_CASE_STATUSES
        or type(record["attempt_count"]) is not int
        or record["attempt_count"] < 0
        or (
            record["active_attempt"] is not None
            and (
                type(record["active_attempt"]) is not int
                or record["active_attempt"] <= 0
            )
        )
        or (
            record["last_completed_outcome_sha256"] is not None
            and (
                type(record["last_completed_outcome_sha256"]) is not str
                or re.fullmatch(
                    r"[0-9a-f]{64}",
                    record["last_completed_outcome_sha256"],
                )
                is None
            )
        )
    ):
        raise ValueError(f"case state {expected_id} is malformed")
    active = record["active_attempt"]
    if (
        (record["status"] == "RUNNING_UNFINISHED_NONCLAIM")
        != (active is not None)
        or (active is not None and active != record["attempt_count"])
    ):
        raise ValueError(f"case state {expected_id} has inconsistent activity")
    status = record["status"]
    attempts = record["attempt_count"]
    last = record["last_completed_outcome_sha256"]
    if status == "PENDING" and (
        attempts != 0 or active is not None or last is not None
    ):
        raise ValueError(f"pending case state {expected_id} is not pristine")
    if status == "RUNNING_UNFINISHED_NONCLAIM" and attempts < 1:
        raise ValueError(f"active case state {expected_id} has no attempt")
    if status in {
        "RETRYABLE_NONCLAIM",
        "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION",
        "UNSAT_LRAT_VERIFIED",
    } and (attempts < 1 or active is not None or last is None):
        raise ValueError(f"completed case state {expected_id} lacks an outcome")
    return dict(record)


def _checkpoint_files(run_directory: Path) -> list[Path]:
    directory = run_directory / CHECKPOINT_DIRECTORY_NAME
    _assert_no_symlink_components(directory)
    if not directory.is_dir():
        raise ValueError("checkpoint directory is missing")
    paths = sorted(directory.iterdir())
    for index, path in enumerate(paths):
        match = CHECKPOINT_PATTERN.fullmatch(path.name)
        if match is None or int(match.group(1)) != index:
            raise ValueError("checkpoint filenames are not consecutive")
        _assert_regular_single_link(path, "checkpoint")
    if not paths:
        raise ValueError("run has no checkpoint")
    return paths


def _audit_checkpoints(
    run_directory: Path,
    *,
    run_manifest_sha256: str,
    partition_sha256: str,
    case_ids: Sequence[str],
) -> tuple[dict[str, object], dict[str, object]]:
    previous_hash: str | None = None
    previous_cases: list[dict[str, object]] | None = None
    previous_written_ns: int | None = None
    latest: dict[str, object] | None = None
    latest_binding: dict[str, object] | None = None
    for sequence, path in enumerate(_checkpoint_files(run_directory)):
        checkpoint = _strict_json_file(path)
        if not isinstance(checkpoint, dict):
            raise ValueError("checkpoint is not an object")
        if (
            checkpoint.get("schema")
            != "gamma-theta-order12-k4-production-checkpoint-v1"
            or checkpoint.get("schema_version") != SCHEMA_VERSION
            or checkpoint.get("sequence") != sequence
            or checkpoint.get("previous_checkpoint_sha256") != previous_hash
            or checkpoint.get("run_manifest_sha256")
            != run_manifest_sha256
            or checkpoint.get("partition_sha256") != partition_sha256
            or not isinstance(checkpoint.get("event"), dict)
            or type(checkpoint.get("written_unix_ns")) is not int
        ):
            raise ValueError(f"checkpoint {sequence} header is malformed")
        raw_cases = checkpoint.get("cases")
        if not isinstance(raw_cases, list) or len(raw_cases) != len(case_ids):
            raise ValueError(f"checkpoint {sequence} case list differs")
        cases = [
            _case_state_shape(record, expected_id)
            for record, expected_id in zip(
                raw_cases, case_ids, strict=True
            )
        ]
        if checkpoint.get("aggregate_status") != _summary_for_cases(cases):
            raise ValueError(f"checkpoint {sequence} aggregate status differs")
        event = checkpoint["event"]
        if not isinstance(event, dict):
            raise ValueError(f"checkpoint {sequence} event is malformed")
        written_ns = checkpoint["written_unix_ns"]
        if (
            type(written_ns) is not int
            or (
                previous_written_ns is not None
                and written_ns < previous_written_ns
            )
        ):
            raise ValueError(f"checkpoint {sequence} time order differs")
        if sequence == 0:
            if (
                event.get("kind") != "INITIALIZED_NO_SOLVER_RUN"
                or any(record["status"] != "PENDING" for record in cases)
            ):
                raise ValueError("initial checkpoint is not a pristine plan")
        else:
            if previous_cases is None:
                raise AssertionError("checkpoint transition lacks predecessor")
            changed = [
                index
                for index, (before, after) in enumerate(
                    zip(previous_cases, cases, strict=True)
                )
                if before != after
            ]
            if len(changed) != 1:
                raise ValueError(
                    f"checkpoint {sequence} must change exactly one case"
                )
            index = changed[0]
            before = previous_cases[index]
            after = cases[index]
            kind = event.get("kind")
            if (
                event.get("case_id") != after["case_id"]
                or before["case_id"] != after["case_id"]
            ):
                raise ValueError(f"checkpoint {sequence} case event differs")
            if kind == "ATTEMPT_RESERVED_NO_RESULT":
                valid = (
                    before["status"] in {"PENDING", "RETRYABLE_NONCLAIM"}
                    and after["status"] == "RUNNING_UNFINISHED_NONCLAIM"
                    and after["attempt_count"]
                    == before["attempt_count"] + 1
                    and after["active_attempt"] == after["attempt_count"]
                    and after["last_completed_outcome_sha256"]
                    == before["last_completed_outcome_sha256"]
                    and event.get("attempt_number")
                    == after["attempt_count"]
                    and isinstance(
                        event.get("attempt_config_sha256"), str
                    )
                    and re.fullmatch(
                        r"[0-9a-f]{64}",
                        str(event.get("attempt_config_sha256")),
                    )
                    is not None
                )
            elif kind == "ATTEMPT_COMPLETED":
                outcome_status = event.get("outcome_status")
                if outcome_status in {
                    "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION",
                    "UNSAT_LRAT_VERIFIED",
                }:
                    expected_after_status = outcome_status
                elif outcome_status in RETRYABLE_OUTCOMES:
                    expected_after_status = "RETRYABLE_NONCLAIM"
                else:
                    expected_after_status = None
                valid = (
                    before["status"] == "RUNNING_UNFINISHED_NONCLAIM"
                    and after["status"] == expected_after_status
                    and after["attempt_count"] == before["attempt_count"]
                    and after["active_attempt"] is None
                    and after["last_completed_outcome_sha256"]
                    == event.get("outcome_sha256")
                    and event.get("attempt_number")
                    == after["attempt_count"]
                )
            elif kind == "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM":
                valid = (
                    before["status"] == "RUNNING_UNFINISHED_NONCLAIM"
                    and after["status"] == "RETRYABLE_NONCLAIM"
                    and after["attempt_count"] == before["attempt_count"]
                    and after["active_attempt"] is None
                    and after["last_completed_outcome_sha256"]
                    == event.get("outcome_sha256")
                    and event.get("attempt_number")
                    == after["attempt_count"]
                )
            elif kind == "ORPHAN_ATTEMPT_RECONCILED_NONCLAIM":
                valid = (
                    before["status"] in {"PENDING", "RETRYABLE_NONCLAIM"}
                    and after["status"] == "RETRYABLE_NONCLAIM"
                    and after["attempt_count"]
                    == before["attempt_count"] + 1
                    and after["active_attempt"] is None
                    and after["last_completed_outcome_sha256"]
                    == event.get("outcome_sha256")
                    and event.get("attempt_number")
                    == after["attempt_count"]
                    and event.get("outcome_status")
                    == "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM"
                    and isinstance(
                        event.get("attempt_config_sha256"), str
                    )
                    and re.fullmatch(
                        r"[0-9a-f]{64}",
                        str(event.get("attempt_config_sha256")),
                    )
                    is not None
                )
            elif kind == "OUTCOME_CHECKPOINT_RECONCILED_NONCLAIM":
                valid = (
                    before["status"] == "RUNNING_UNFINISHED_NONCLAIM"
                    and after["status"] == "RETRYABLE_NONCLAIM"
                    and after["attempt_count"] == before["attempt_count"]
                    and after["active_attempt"] is None
                    and after["last_completed_outcome_sha256"]
                    == event.get("outcome_sha256")
                    and event.get("attempt_number")
                    == after["attempt_count"]
                    and event.get("original_outcome_status")
                    in RETRYABLE_OUTCOMES
                    | {
                        "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION",
                        "UNSAT_LRAT_VERIFIED",
                    }
                )
            else:
                valid = False
            if not valid:
                raise ValueError(
                    f"checkpoint {sequence} transition is not permitted"
                )
        latest = checkpoint
        latest_binding = _file_binding(path, "checkpoint")
        previous_hash = str(latest_binding["sha256"])
        previous_cases = cases
        previous_written_ns = written_ns
    if latest is None or latest_binding is None:
        raise AssertionError("checkpoint audit returned no latest checkpoint")
    return latest, latest_binding


def _checkpoint_attempt_event_index(
    run_directory: Path,
) -> dict[str, object]:
    """Index already-audited attempt bindings without trusting case files."""

    config_bindings: dict[tuple[str, int], str] = {}
    reconciled_outcomes: dict[tuple[str, int], str] = {}
    for path in _checkpoint_files(run_directory):
        checkpoint = _strict_json_file(path)
        if not isinstance(checkpoint, dict):
            raise ValueError("checkpoint is not an object")
        event = checkpoint.get("event")
        if not isinstance(event, dict):
            raise ValueError("checkpoint event is malformed")
        kind = event.get("kind")
        if kind in {
            "ATTEMPT_RESERVED_NO_RESULT",
            "ORPHAN_ATTEMPT_RECONCILED_NONCLAIM",
        }:
            case_id = event.get("case_id")
            attempt_number = event.get("attempt_number")
            digest = event.get("attempt_config_sha256")
            if (
                not isinstance(case_id, str)
                or type(attempt_number) is not int
                or not isinstance(digest, str)
                or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            ):
                raise ValueError("checkpoint attempt binding is malformed")
            key = (case_id, attempt_number)
            if key in config_bindings:
                raise ValueError("attempt has duplicate configuration bindings")
            config_bindings[key] = digest
        if kind == "OUTCOME_CHECKPOINT_RECONCILED_NONCLAIM":
            case_id = event.get("case_id")
            attempt_number = event.get("attempt_number")
            digest = event.get("outcome_sha256")
            if (
                not isinstance(case_id, str)
                or type(attempt_number) is not int
                or not isinstance(digest, str)
                or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            ):
                raise ValueError("checkpoint outcome reconciliation is malformed")
            key = (case_id, attempt_number)
            if key in reconciled_outcomes:
                raise ValueError("attempt has duplicate outcome reconciliations")
            reconciled_outcomes[key] = digest
    return {
        "attempt_config_sha256": config_bindings,
        "reconciled_outcome_sha256": reconciled_outcomes,
    }


def _path_within(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
    except ValueError:
        return False
    return True


def _artifact_inventory(
    attempt_directory: Path,
    *,
    exclude: frozenset[str] = frozenset({"outcome.json"}),
) -> dict[str, dict[str, object]]:
    inventory: dict[str, dict[str, object]] = {}
    for path in sorted(attempt_directory.iterdir()):
        _assert_no_symlink_components(path)
        if path.name in exclude:
            continue
        if not path.is_file():
            raise ValueError("nested or non-file attempt artifact is forbidden")
        _assert_regular_single_link(path, f"attempt artifact {path.name}")
        inventory[path.name] = _file_binding(
            path, f"attempt artifact {path.name}"
        )
    return inventory


def _validate_inventory(
    inventory: object,
    attempt_directory: Path,
) -> None:
    if not isinstance(inventory, dict):
        raise ValueError("attempt inventory is not an object")
    observed = _artifact_inventory(attempt_directory)
    if set(observed) != set(inventory):
        raise ValueError("attempt inventory filenames differ")
    for name, record in inventory.items():
        if not isinstance(record, dict):
            raise ValueError("attempt inventory binding is malformed")
        expected_path = attempt_directory / name
        if record.get("path") != str(expected_path.resolve()):
            raise ValueError("attempt inventory path differs")
        _verify_file_binding(record, f"attempt artifact {name}")
        if observed[name] != record:
            raise ValueError("attempt inventory record differs")


def _audit_decisive_outcome(
    *,
    outcome: Mapping[str, object],
    attempt_directory: Path,
    attempt_config: Mapping[str, object],
    case_id: str,
) -> None:
    status = outcome.get("status")
    details = outcome.get("details")
    if not isinstance(details, dict):
        raise ValueError("attempt outcome details are malformed")
    if status == "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION":
        candidate_path = attempt_directory / "candidate.json"
        raw_result_path = attempt_directory / "solver.result"
        candidate = _strict_json_file(candidate_path)
        if (
            not isinstance(candidate, dict)
            or candidate.get("schema")
            != "gamma-theta-order12-k4-sat-candidate-v1"
            or candidate.get("claim_status")
            != "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION"
            or candidate.get("case_id") != case_id
        ):
            raise ValueError("SAT candidate artifact is malformed")
        status_again, _ = classify_solver_result(
            (attempt_directory / "instance.cnf").read_bytes(),
            raw_result_path.read_bytes(),
        )
        if status_again != "SAT":
            raise ValueError("retained SAT result no longer validates")
        if "certificate.json" in outcome["artifact_inventory"]:
            raise ValueError("SAT candidate unexpectedly has an UNSAT certificate")
        return
    if status != "UNSAT_LRAT_VERIFIED":
        return
    certificate_path = attempt_directory / "certificate.json"
    certificate = _strict_json_file(certificate_path)
    if (
        not isinstance(certificate, dict)
        or certificate.get("schema")
        != "gamma-theta-order12-k4-leaf-lrat-certificate-v2"
        or certificate.get("schema_version") != SCHEMA_VERSION
        or certificate.get("proof_pipeline") != PROOF_PIPELINE_ID
        or certificate.get("leaf_status") != "UNSAT_LRAT_VERIFIED"
        or certificate.get("case_id") != case_id
        or certificate.get("cube_literals")
        != attempt_config.get("cube_literals")
    ):
        raise ValueError("leaf LRAT certificate is malformed")
    for key, role in (
        ("case_cnf", "certificate case CNF"),
        ("raw_solver_result", "certificate raw result"),
        ("raw_binary_drat", "certificate raw DRAT"),
        ("converted_lrat", "certificate LRAT"),
        ("raw_forward_stdout", "certificate raw forward stdout"),
        ("raw_forward_stderr", "certificate raw forward stderr"),
        (
            "lrat_conversion_stdout",
            "certificate LRAT conversion stdout",
        ),
        (
            "lrat_conversion_stderr",
            "certificate LRAT conversion stderr",
        ),
        ("lrat_check_stdout", "certificate lrat-check stdout"),
        ("lrat_check_stderr", "certificate lrat-check stderr"),
    ):
        binding = certificate.get(key)
        if not isinstance(binding, dict):
            raise ValueError(f"{role} binding is malformed")
        _verify_file_binding(binding, role)
        if not _path_within(Path(str(binding["path"])), attempt_directory):
            raise ValueError(f"{role} escapes the attempt directory")
    _strict_converter_success(
        (attempt_directory / "raw-forward.stdout").read_bytes(),
        (attempt_directory / "raw-forward.stderr").read_bytes(),
    )
    _strict_converter_success(
        (attempt_directory / "lrat-conversion.stdout").read_bytes(),
        (attempt_directory / "lrat-conversion.stderr").read_bytes(),
    )
    _strict_lrat_success(
        (attempt_directory / "lrat-check.stdout").read_bytes(),
        (attempt_directory / "lrat-check.stderr").read_bytes(),
    )
    child_expectations = (
        ("solver", "solver_command", 20),
        ("raw_forward", "raw_forward_command", 0),
        ("lrat_conversion", "lrat_conversion_command", 0),
        ("lrat_check", "lrat_check_command", 0),
    )
    for child_key, command_key, exit_code in child_expectations:
        child = certificate.get(child_key)
        if (
            not isinstance(child, dict)
            or child.get("command") != attempt_config.get(command_key)
            or child.get("exit_code") != exit_code
            or child.get("timed_out") is not False
            or child.get("memory_limit_exceeded") is not False
            or child.get("termination_signal") is not None
            or child.get("executable_sha256_before")
            != child.get("executable_sha256_after")
        ):
            raise ValueError(f"certificate {child_key} record is malformed")


def _audit_attempts(
    run_directory: Path,
    manifest: Mapping[str, object],
    manifest_hash: str,
    partition: Mapping[str, object],
    partition_hash: str,
    latest: Mapping[str, object],
    event_index: Mapping[str, object],
) -> dict[str, int]:
    partition_cases = partition["cases"]
    state_cases = latest["cases"]
    if not isinstance(partition_cases, list) or not isinstance(state_cases, list):
        raise ValueError("case lists are malformed")
    config_bindings = event_index.get("attempt_config_sha256")
    reconciled_outcomes = event_index.get("reconciled_outcome_sha256")
    if not isinstance(config_bindings, dict) or not isinstance(
        reconciled_outcomes, dict
    ):
        raise ValueError("checkpoint attempt event index is malformed")
    expected_case_names = {
        f"case-{record['case_id']}"
        for record in partition_cases
        if isinstance(record, dict)
    }
    case_root = run_directory / CASE_DIRECTORY_NAME
    observed_case_names = {path.name for path in case_root.iterdir()}
    if observed_case_names != expected_case_names:
        raise ValueError("case directory set differs from partition")
    completed = 0
    active = 0
    for partition_record, state in zip(
        partition_cases, state_cases, strict=True
    ):
        if not isinstance(partition_record, dict) or not isinstance(state, dict):
            raise ValueError("case record is malformed")
        case_id = str(partition_record["case_id"])
        case_directory = case_root / f"case-{case_id}"
        if not case_directory.is_dir() or case_directory.is_symlink():
            raise ValueError(f"case directory {case_id} is malformed")
        attempts = sorted(case_directory.iterdir())
        attempt_count = state["attempt_count"]
        if type(attempt_count) is not int or len(attempts) != attempt_count:
            raise ValueError(f"case {case_id} attempt count differs")
        last_outcome_hash: str | None = None
        last_outcome_status: str | None = None
        for attempt_number, attempt_directory in enumerate(attempts, start=1):
            match = ATTEMPT_PATTERN.fullmatch(attempt_directory.name)
            if (
                match is None
                or int(match.group(1)) != attempt_number
                or not attempt_directory.is_dir()
                or attempt_directory.is_symlink()
            ):
                raise ValueError(f"case {case_id} attempt layout differs")
            config_path = attempt_directory / "attempt-config.json"
            case_cnf_path = attempt_directory / "instance.cnf"
            _assert_regular_single_link(config_path, "attempt configuration")
            _assert_regular_single_link(case_cnf_path, "case CNF")
            if (
                sha256_file(case_cnf_path)
                != partition_record["cnf_sha256"]
                or case_cnf_path.stat().st_size
                != partition_record["cnf_size_bytes"]
            ):
                raise ValueError(f"case {case_id} materialized CNF differs")
            config = _strict_json_file(config_path)
            config = _validate_attempt_config(
                config,
                manifest=manifest,
                manifest_hash=manifest_hash,
                partition_hash=partition_hash,
                case=partition_record,
                attempt_number=attempt_number,
                attempt_directory=attempt_directory,
            )
            key = (case_id, attempt_number)
            expected_config_hash = config_bindings.get(key)
            if (
                not isinstance(expected_config_hash, str)
                or sha256_file(config_path) != expected_config_hash
            ):
                raise ValueError(
                    f"case {case_id} attempt config lacks its exact "
                    "checkpoint binding"
                )
            outcome_path = attempt_directory / "outcome.json"
            is_active = state.get("active_attempt") == attempt_number
            if is_active:
                active += 1
                if outcome_path.exists() or outcome_path.is_symlink():
                    raise ValueError("active attempt already has an outcome")
                continue
            _assert_regular_single_link(outcome_path, "attempt outcome")
            outcome = _strict_json_file(outcome_path)
            if (
                not isinstance(outcome, dict)
                or outcome.get("schema")
                != "gamma-theta-order12-k4-attempt-outcome-v1"
                or outcome.get("schema_version") != SCHEMA_VERSION
                or outcome.get("case_id") != case_id
                or outcome.get("attempt_number") != attempt_number
            ):
                raise ValueError(f"case {case_id} attempt outcome differs")
            outcome_status = outcome.get("status")
            if outcome_status not in RETRYABLE_OUTCOMES and outcome_status not in {
                "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION",
                "UNSAT_LRAT_VERIFIED",
            }:
                raise ValueError(f"case {case_id} outcome status is unknown")
            if (
                outcome.get("aggregate_claim") != "NONE"
                or (
                    outcome_status == "UNSAT_LRAT_VERIFIED"
                    and outcome.get("mathematical_claim")
                    != "LEAF_UNSAT_AFTER_LRAT_REPLAY"
                )
                or (
                    outcome_status != "UNSAT_LRAT_VERIFIED"
                    and outcome.get("mathematical_claim") != "NONE"
                )
            ):
                raise ValueError(f"case {case_id} outcome claim boundary differs")
            _validate_inventory(
                outcome.get("artifact_inventory"), attempt_directory
            )
            _audit_decisive_outcome(
                outcome=outcome,
                attempt_directory=attempt_directory,
                attempt_config=config,
                case_id=case_id,
            )
            last_outcome_hash = sha256_file(outcome_path)
            last_outcome_status = str(outcome_status)
            completed += 1
        if last_outcome_hash != state["last_completed_outcome_sha256"]:
            raise ValueError(f"case {case_id} latest outcome binding differs")
        if state["status"] == "PENDING":
            expected_status = None
        elif state["status"] == "RUNNING_UNFINISHED_NONCLAIM":
            expected_status = last_outcome_status
        elif state["status"] == "RETRYABLE_NONCLAIM":
            if last_outcome_status not in RETRYABLE_OUTCOMES:
                reconciled_hash = reconciled_outcomes.get(
                    (case_id, int(state["attempt_count"]))
                )
                if reconciled_hash != last_outcome_hash:
                    raise ValueError(
                        f"case {case_id} retryable state has decisive outcome"
                    )
            expected_status = last_outcome_status
        else:
            expected_status = state["status"]
        if state["status"] not in {
            "PENDING",
            "RUNNING_UNFINISHED_NONCLAIM",
            "RETRYABLE_NONCLAIM",
        } and last_outcome_status != expected_status:
            raise ValueError(
                f"case {case_id} state does not match its last outcome"
            )
    return {
        "completed_attempt_count": completed,
        "active_attempt_count": active,
    }


def _load_run_manifest(run_directory: Path) -> tuple[dict[str, object], str]:
    path = run_directory / RUN_MANIFEST_NAME
    manifest = _strict_json_file(path)
    if not isinstance(manifest, dict):
        raise ValueError("run manifest is not an object")
    if (
        manifest.get("schema") != "gamma-theta-order12-k4-production-run-v1"
        or manifest.get("schema_version") != SCHEMA_VERSION
        or manifest.get("proof_pipeline") != PROOF_PIPELINE_ID
        or manifest.get("claim_status") != "NO_SAT_OR_UNSAT_CLAIM"
        or manifest.get("run_directory") != str(run_directory)
        or manifest.get("campaign_root") != str(campaign_root().resolve())
    ):
        raise ValueError("run manifest header differs")
    return manifest, sha256_file(path)


def audit_run(
    run_directory: Path,
    *,
    verify_runtime_sources: bool = True,
) -> dict[str, object]:
    """Audit a run read-only.  No solver, converter, or checker is started."""

    _assert_no_symlink_components(run_directory)
    run_directory = run_directory.resolve(strict=True)
    if not run_directory.is_dir():
        raise ValueError("run path is not a directory")
    manifest, manifest_hash = _load_run_manifest(run_directory)

    retained_parent_record = manifest.get("retained_parent_cnf")
    retained_generator_record = manifest.get(
        "retained_parent_generator_manifest"
    )
    partition_record = manifest.get("partition")
    sources = manifest.get("runtime_sources")
    tools = manifest.get("tools")
    limits = manifest.get("limits")
    if not all(
        isinstance(record, dict)
        for record in (
            retained_parent_record,
            retained_generator_record,
            partition_record,
            sources,
            tools,
            limits,
        )
    ):
        raise ValueError("run manifest bindings are malformed")
    _verify_file_binding(retained_parent_record, "retained parent CNF")
    _verify_file_binding(
        retained_generator_record, "retained parent generator manifest"
    )
    _verify_file_binding(partition_record, "partition")
    if (
        retained_parent_record["path"]
        != str((run_directory / PARENT_COPY_NAME).resolve())
        or retained_parent_record["sha256"] != EXPECTED_PARENT_CNF_SHA256
        or retained_generator_record["path"]
        != str((run_directory / PARENT_MANIFEST_COPY_NAME).resolve())
        or retained_generator_record["sha256"]
        != EXPECTED_PARENT_MANIFEST_SHA256
        or partition_record["path"]
        != str((run_directory / PARTITION_NAME).resolve())
    ):
        raise ValueError("retained input paths or hashes differ")
    parent = (run_directory / PARENT_COPY_NAME).read_bytes()
    generator = (run_directory / PARENT_MANIFEST_COPY_NAME).read_bytes()
    _validate_parent(
        run_directory / PARENT_COPY_NAME,
        run_directory / PARENT_MANIFEST_COPY_NAME,
    )
    if (
        sha256_bytes(parent) != EXPECTED_PARENT_CNF_SHA256
        or sha256_bytes(generator) != EXPECTED_PARENT_MANIFEST_SHA256
    ):
        raise AssertionError("retained input validation is inconsistent")
    partition_raw = _strict_json_file(run_directory / PARTITION_NAME)
    if not isinstance(partition_raw, dict):
        raise ValueError("partition is not an object")
    _validate_partition(partition_raw, parent)
    if verify_runtime_sources:
        _verify_committed_source_binding(sources)
    _verify_tool_bindings(tools)

    case_records = partition_raw["cases"]
    if not isinstance(case_records, list):
        raise ValueError("partition cases are malformed")
    case_ids = [
        str(record["case_id"])
        for record in case_records
        if isinstance(record, dict)
    ]
    latest, latest_binding = _audit_checkpoints(
        run_directory,
        run_manifest_sha256=manifest_hash,
        partition_sha256=str(partition_record["sha256"]),
        case_ids=case_ids,
    )
    event_index = _checkpoint_attempt_event_index(run_directory)
    attempts = _audit_attempts(
        run_directory,
        manifest,
        manifest_hash,
        partition_raw,
        str(partition_record["sha256"]),
        latest,
        event_index,
    )
    states = latest["cases"]
    if not isinstance(states, list):
        raise ValueError("latest checkpoint states are malformed")
    histogram: dict[str, int] = {}
    for record in states:
        if not isinstance(record, dict):
            raise ValueError("latest case state is malformed")
        status = str(record["status"])
        histogram[status] = histogram.get(status, 0) + 1
    return {
        "status": "PASS_READ_ONLY_AUDIT_NO_MATHEMATICAL_CLAIM",
        "run_directory": str(run_directory),
        "run_manifest_sha256": manifest_hash,
        "partition_sha256": partition_record["sha256"],
        "latest_checkpoint": latest_binding,
        "latest_checkpoint_sequence": latest["sequence"],
        "aggregate_status": latest["aggregate_status"],
        "case_status_histogram": dict(sorted(histogram.items())),
        "attempts": attempts,
        "runtime_sources_verified": verify_runtime_sources,
        "proofs_freshly_replayed": False,
        "claim_status": "NO_MATHEMATICAL_CLAIM",
    }


def _resource_report(
    run_directory: Path,
    *,
    phase: str,
    memory_limit_mib: int,
    limits: Mapping[str, object],
) -> dict[str, object]:
    errors: list[str] = []
    load_one: float | None
    available_memory: int | None
    try:
        load_one = os.getloadavg()[0]
    except (AttributeError, OSError) as error:
        load_one = None
        errors.append(f"load probe failed: {type(error).__name__}")
    try:
        available_memory = _available_memory_bytes()
    except (RuntimeError, ValueError, OSError) as error:
        available_memory = None
        errors.append(f"memory probe failed: {type(error).__name__}")
    disk = shutil.disk_usage(run_directory)
    load_max = limits.get("load_max")
    memory_reserve = limits.get("memory_reserve_mib")
    file_limit = limits.get("file_limit_mib")
    disk_reserve = limits.get("disk_reserve_mib")
    if (
        type(load_max) not in (int, float)
        or type(memory_reserve) is not int
        or type(file_limit) is not int
        or type(disk_reserve) is not int
    ):
        raise ValueError("stored resource limits are malformed")
    memory_required = (memory_limit_mib + memory_reserve) << 20
    disk_required = (
        disk_reserve
        + WORST_CASE_LIVE_FILE_SLOTS * file_limit
        + DISK_METADATA_ALLOWANCE_MIB
    ) << 20
    checks = {
        "load": load_one is not None and load_one <= float(load_max),
        "memory": (
            available_memory is not None
            and available_memory >= memory_required
        ),
        "disk": disk.free >= disk_required,
    }
    return {
        "schema": "gamma-theta-k4-resource-gate-v1",
        "phase": phase,
        "checked_unix_ns": time.time_ns(),
        "load_average_one_minute": load_one,
        "load_ceiling": load_max,
        "available_memory_bytes": available_memory,
        "required_memory_bytes": memory_required,
        "free_disk_bytes": disk.free,
        "required_free_disk_bytes": disk_required,
        "worst_case_live_file_slots": WORST_CASE_LIVE_FILE_SLOTS,
        "checks": checks,
        "probe_errors": errors,
        "passed": all(checks.values()) and not errors,
    }


def _solver_command(
    manifest: Mapping[str, object],
    case: Mapping[str, object],
    attempt_directory: Path,
) -> tuple[str, ...]:
    tools = manifest["tools"]
    limits = manifest["limits"]
    if not isinstance(tools, dict) or not isinstance(limits, dict):
        raise ValueError("run tool or limit binding is malformed")
    cadical = tools["cadical"]
    if not isinstance(cadical, dict):
        raise ValueError("CaDiCaL binding is malformed")
    return (
        str(cadical["path"]),
        f"--seed={case['seed']}",
        "--binary",
        "--no-colors",
        "-q",
        "-t",
        str(limits["solver_wall_seconds"]),
        "-w",
        str((attempt_directory / "solver.result").resolve()),
        str((attempt_directory / "instance.cnf").resolve()),
        str((attempt_directory / "proof.raw.bdrat").resolve()),
    )


def _raw_forward_command(
    manifest: Mapping[str, object],
    attempt_directory: Path,
) -> tuple[str, ...]:
    tools = manifest["tools"]
    limits = manifest["limits"]
    if not isinstance(tools, dict) or not isinstance(limits, dict):
        raise ValueError("run tool or limit binding is malformed")
    converter = tools["drat_trim"]
    if not isinstance(converter, dict):
        raise ValueError("drat-trim binding is malformed")
    return (
        str(converter["path"]),
        str((attempt_directory / "instance.cnf").resolve()),
        str((attempt_directory / "proof.raw.bdrat").resolve()),
        "-i",
        "-f",
        "-W",
        "-t",
        str(limits["converter_wall_seconds"]),
    )


def _lrat_conversion_command(
    manifest: Mapping[str, object],
    attempt_directory: Path,
) -> tuple[str, ...]:
    tools = manifest["tools"]
    limits = manifest["limits"]
    if not isinstance(tools, dict) or not isinstance(limits, dict):
        raise ValueError("run tool or limit binding is malformed")
    converter = tools["drat_trim"]
    if not isinstance(converter, dict):
        raise ValueError("drat-trim binding is malformed")
    return (
        str(converter["path"]),
        str((attempt_directory / "instance.cnf").resolve()),
        str((attempt_directory / "proof.raw.bdrat").resolve()),
        "-i",
        "-W",
        "-L",
        str((attempt_directory / "proof.converted.lrat").resolve()),
        "-t",
        str(limits["converter_wall_seconds"]),
    )


def _lrat_check_command(
    manifest: Mapping[str, object],
    attempt_directory: Path,
) -> tuple[str, ...]:
    tools = manifest["tools"]
    if not isinstance(tools, dict):
        raise ValueError("run tool binding is malformed")
    checker = tools["lrat_check"]
    if not isinstance(checker, dict):
        raise ValueError("lrat-check binding is malformed")
    return (
        str(checker["path"]),
        str((attempt_directory / "instance.cnf").resolve()),
        str((attempt_directory / "proof.converted.lrat").resolve()),
    )


def _validate_attempt_config(
    config: object,
    *,
    manifest: Mapping[str, object],
    manifest_hash: str,
    partition_hash: str,
    case: Mapping[str, object],
    attempt_number: int,
    attempt_directory: Path,
) -> dict[str, object]:
    expected_keys = {
        "schema",
        "schema_version",
        "proof_pipeline",
        "claim_status",
        "case_id",
        "attempt_number",
        "seed",
        "cube_literals",
        "case_cnf_sha256",
        "run_manifest_sha256",
        "partition_sha256",
        "solver_command",
        "raw_forward_command",
        "lrat_conversion_command",
        "lrat_check_command",
        "created_unix_ns",
    }
    if not isinstance(config, dict) or set(config) != expected_keys:
        raise ValueError("attempt configuration has the wrong shape")
    if (
        config.get("schema")
        != "gamma-theta-order12-k4-attempt-config-v1"
        or config.get("schema_version") != SCHEMA_VERSION
        or config.get("proof_pipeline") != PROOF_PIPELINE_ID
        or config.get("claim_status") != "NO_SAT_OR_UNSAT_CLAIM"
        or config.get("case_id") != case.get("case_id")
        or config.get("attempt_number") != attempt_number
        or config.get("seed") != case.get("seed")
        or config.get("cube_literals") != case.get("cube_literals")
        or config.get("case_cnf_sha256") != case.get("cnf_sha256")
        or config.get("run_manifest_sha256") != manifest_hash
        or config.get("partition_sha256") != partition_hash
        or config.get("solver_command")
        != list(_solver_command(manifest, case, attempt_directory))
        or config.get("raw_forward_command")
        != list(_raw_forward_command(manifest, attempt_directory))
        or config.get("lrat_conversion_command")
        != list(_lrat_conversion_command(manifest, attempt_directory))
        or config.get("lrat_check_command")
        != list(_lrat_check_command(manifest, attempt_directory))
        or type(config.get("created_unix_ns")) is not int
        or int(config["created_unix_ns"]) <= 0
    ):
        raise ValueError("attempt configuration differs from frozen inputs")
    return dict(config)


def _child_failure_status(child: ChildResult, phase: str) -> str | None:
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


def _verify_child_artifacts(child: ChildResult, command: Sequence[str]) -> None:
    if tuple(child.command) != tuple(command):
        raise ValueError("child command record differs")
    if (
        child.executable_sha256_before
        != child.executable_sha256_after
        or child.executable_sha256_before
        != sha256_file(Path(command[0]))
    ):
        raise ValueError("child executable binding differs")
    for role, path_raw, expected_hash in (
        ("child stdout", child.stdout_path, child.stdout_sha256),
        ("child stderr", child.stderr_path, child.stderr_sha256),
    ):
        path = Path(path_raw)
        _assert_regular_single_link(path, role)
        if sha256_file(path) != expected_hash:
            raise ValueError(f"{role} binding differs")


def _strict_converter_success(stdout: bytes, stderr: bytes) -> None:
    if stderr:
        raise ValueError("drat-trim wrote to stderr")
    try:
        text = stdout.decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError("drat-trim output is not ASCII") from error
    lines = [line.strip() for line in text.replace("\r", "\n").splitlines()]
    lines = [line for line in lines if line]
    lowered = "\n".join(lines).lower()
    if (
        lines.count("s VERIFIED") != 1
        or "warning" in lowered
        or "error" in lowered
        or "not verified" in lowered
    ):
        raise ValueError("drat-trim did not produce one clean VERIFIED status")


def _strict_lrat_success(stdout: bytes, stderr: bytes) -> None:
    if stderr:
        raise ValueError("lrat-check wrote to stderr")
    try:
        text = stdout.decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError("lrat-check output is not ASCII") from error
    lines = [line.strip() for line in text.replace("\r", "\n").splitlines()]
    lines = [line for line in lines if line]
    lowered = "\n".join(lines).lower()
    if (
        lines.count("c VERIFIED") != 1
        or "error" in lowered
        or "not verified" in lowered
    ):
        raise ValueError("lrat-check did not produce one clean VERIFIED status")


def classify_solver_result(
    cnf_bytes: bytes,
    result_bytes: bytes,
) -> tuple[str, dict[str, object] | None]:
    """Strictly parse a solver result; validate every clause for SAT."""

    cnf = parse_dimacs_bytes(cnf_bytes)
    parsed = parse_solver_result_bytes(result_bytes, cnf.variable_count)
    if parsed.status != "SAT":
        return parsed.status, None
    if parsed.model is None:
        raise ValueError("SAT result has no model")
    validate_model_satisfies_cnf(cnf, parsed.model)
    edge_pairs = tuple(combinations(range(12), 2))
    edge_assignment = [
        {
            "variable": variable,
            "pair": list(pair),
            "h_edge": parsed.model[variable],
        }
        for variable, pair in enumerate(edge_pairs, start=1)
        if variable <= cnf.variable_count
    ]
    canonical_assignment = canonical_json_bytes(
        [
            variable if parsed.model[variable] else -variable
            for variable in range(1, cnf.variable_count + 1)
        ]
    )
    return (
        "SAT",
        {
            "claim_status": (
                "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION"
            ),
            "variable_count": cnf.variable_count,
            "assignment_sha256": sha256_bytes(canonical_assignment),
            "true_variable_count": sum(parsed.model.values()),
            "h_edge_assignment": edge_assignment,
            "raw_result_retained": True,
        },
    )


def _child_record(child: ChildResult | None) -> dict[str, object] | None:
    return None if child is None else asdict(child)


def _write_phase_resource(
    run_directory: Path,
    attempt_directory: Path,
    *,
    phase: str,
    memory_limit_mib: int,
    limits: Mapping[str, object],
) -> dict[str, object]:
    report = _resource_report(
        run_directory,
        phase=phase,
        memory_limit_mib=memory_limit_mib,
        limits=limits,
    )
    _write_exclusive(
        attempt_directory / f"resource-{phase}.json",
        canonical_json_bytes(report),
    )
    return report


def _write_outcome(
    attempt_directory: Path,
    *,
    case_id: str,
    attempt_number: int,
    status: str,
    details: Mapping[str, object],
) -> dict[str, object]:
    if status not in RETRYABLE_OUTCOMES and status not in {
        "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION",
        "UNSAT_LRAT_VERIFIED",
    }:
        raise ValueError(f"unknown attempt outcome status {status}")
    payload = {
        "schema": "gamma-theta-order12-k4-attempt-outcome-v1",
        "schema_version": SCHEMA_VERSION,
        "case_id": case_id,
        "attempt_number": attempt_number,
        "status": status,
        "mathematical_claim": (
            "LEAF_UNSAT_AFTER_LRAT_REPLAY"
            if status == "UNSAT_LRAT_VERIFIED"
            else "NONE"
        ),
        "aggregate_claim": "NONE",
        "details": dict(details),
        "artifact_inventory": _artifact_inventory(attempt_directory),
        "finished_unix_ns": time.time_ns(),
    }
    path = attempt_directory / "outcome.json"
    _write_exclusive(path, canonical_json_bytes(payload))
    return _file_binding(path, "attempt outcome")


def _case_by_id(
    partition: Mapping[str, object],
    case_id: str,
) -> dict[str, object]:
    cases = partition.get("cases")
    if not isinstance(cases, list):
        raise ValueError("partition cases are malformed")
    for record in cases:
        if isinstance(record, dict) and record.get("case_id") == case_id:
            return dict(record)
    raise ValueError(f"unknown case id {case_id!r}")


def _append_checkpoint_transition(
    run_directory: Path,
    *,
    latest: Mapping[str, object],
    latest_hash: str,
    run_manifest_sha256: str,
    partition_sha256: str,
    case_id: str,
    replacement: Mapping[str, object],
    event: Mapping[str, object],
) -> dict[str, object]:
    raw_cases = latest.get("cases")
    if not isinstance(raw_cases, list):
        raise ValueError("latest checkpoint cases are malformed")
    cases: list[dict[str, object]] = []
    found = False
    for record in raw_cases:
        if not isinstance(record, dict):
            raise ValueError("latest checkpoint case is malformed")
        if record.get("case_id") == case_id:
            cases.append(dict(replacement))
            found = True
        else:
            cases.append(dict(record))
    if not found:
        raise ValueError(f"case {case_id} is absent from checkpoint")
    sequence = latest.get("sequence")
    if type(sequence) is not int:
        raise ValueError("latest checkpoint sequence is malformed")
    payload = _checkpoint_payload(
        sequence=sequence + 1,
        previous_checkpoint_sha256=latest_hash,
        run_manifest_sha256=run_manifest_sha256,
        partition_sha256=partition_sha256,
        cases=cases,
        event=event,
    )
    return _write_checkpoint(run_directory, payload)


def _reload_context(
    run_directory: Path,
) -> tuple[
    dict[str, object],
    str,
    dict[str, object],
    str,
    dict[str, object],
    str,
]:
    manifest, manifest_hash = _load_run_manifest(run_directory)
    partition_path = run_directory / PARTITION_NAME
    partition = _strict_json_file(partition_path)
    if not isinstance(partition, dict):
        raise ValueError("partition is malformed")
    partition_hash = sha256_file(partition_path)
    cases = partition.get("cases")
    if not isinstance(cases, list):
        raise ValueError("partition cases are malformed")
    ids = [
        str(record["case_id"])
        for record in cases
        if isinstance(record, dict)
    ]
    latest, latest_binding = _audit_checkpoints(
        run_directory,
        run_manifest_sha256=manifest_hash,
        partition_sha256=partition_hash,
        case_ids=ids,
    )
    return (
        manifest,
        manifest_hash,
        partition,
        partition_hash,
        latest,
        str(latest_binding["sha256"]),
    )


def _load_recovery_foundation(
    run_directory: Path,
) -> tuple[
    dict[str, object],
    str,
    dict[str, object],
    str,
    dict[str, object],
    str,
]:
    """Audit immutable run foundations even when attempt layout is torn."""

    (
        manifest,
        manifest_hash,
        partition,
        partition_hash,
        latest,
        latest_hash,
    ) = _reload_context(run_directory)
    retained_parent = manifest.get("retained_parent_cnf")
    retained_generator = manifest.get(
        "retained_parent_generator_manifest"
    )
    partition_binding = manifest.get("partition")
    sources = manifest.get("runtime_sources")
    tools = manifest.get("tools")
    if not all(
        isinstance(record, dict)
        for record in (
            retained_parent,
            retained_generator,
            partition_binding,
            sources,
            tools,
        )
    ):
        raise ValueError("recovery foundation bindings are malformed")
    _verify_file_binding(retained_parent, "retained parent CNF")
    _verify_file_binding(
        retained_generator, "retained parent generator manifest"
    )
    _verify_file_binding(partition_binding, "partition")
    if (
        retained_parent["path"]
        != str((run_directory / PARENT_COPY_NAME).resolve())
        or retained_parent["sha256"] != EXPECTED_PARENT_CNF_SHA256
        or retained_generator["path"]
        != str((run_directory / PARENT_MANIFEST_COPY_NAME).resolve())
        or retained_generator["sha256"]
        != EXPECTED_PARENT_MANIFEST_SHA256
        or partition_binding["path"]
        != str((run_directory / PARTITION_NAME).resolve())
        or partition_binding["sha256"] != partition_hash
    ):
        raise ValueError("recovery foundation paths or hashes differ")
    parent, _ = _validate_parent(
        run_directory / PARENT_COPY_NAME,
        run_directory / PARENT_MANIFEST_COPY_NAME,
    )
    _validate_partition(partition, parent)
    _verify_committed_source_binding(sources)
    _verify_tool_bindings(tools)
    return (
        manifest,
        manifest_hash,
        partition,
        partition_hash,
        latest,
        latest_hash,
    )


def _select_case_state(
    latest: Mapping[str, object],
    requested_case_id: str | None,
) -> dict[str, object]:
    raw_cases = latest.get("cases")
    if not isinstance(raw_cases, list):
        raise ValueError("latest case states are malformed")
    states = [record for record in raw_cases if isinstance(record, dict)]
    if len(states) != len(raw_cases):
        raise ValueError("latest case state is malformed")
    if any(
        record["status"]
        == "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION"
        for record in states
    ):
        raise RuntimeError(
            "a SAT candidate freezes the run pending independent verification"
        )
    if any(
        record["status"] == "RUNNING_UNFINISHED_NONCLAIM"
        for record in states
    ):
        raise RuntimeError(
            "an interrupted active attempt must be explicitly recovered first"
        )
    eligible = [
        record
        for record in states
        if record["status"] in {"PENDING", "RETRYABLE_NONCLAIM"}
    ]
    if requested_case_id is not None:
        if not re.fullmatch(r"[01]{4}", requested_case_id):
            raise ValueError("case id must be four bits")
        selected = next(
            (
                record
                for record in states
                if record["case_id"] == requested_case_id
            ),
            None,
        )
        if selected is None:
            raise ValueError("requested case is absent")
        if selected not in eligible:
            raise RuntimeError(
                f"requested case is not runnable: {selected['status']}"
            )
        return dict(selected)
    if not eligible:
        raise RuntimeError("no pending or retryable case remains")
    return dict(eligible[0])


def _execute_attempt(
    *,
    run_directory: Path,
    manifest: Mapping[str, object],
    case: Mapping[str, object],
    attempt_directory: Path,
) -> tuple[str, dict[str, object]]:
    limits = manifest.get("limits")
    tools = manifest.get("tools")
    sources = manifest.get("runtime_sources")
    if (
        not isinstance(limits, dict)
        or not isinstance(tools, dict)
        or not isinstance(sources, dict)
    ):
        raise ValueError("run manifest execution bindings are malformed")
    case_cnf = attempt_directory / "instance.cnf"
    case_binding = _file_binding(case_cnf, "case CNF")
    solver_command = _solver_command(manifest, case, attempt_directory)
    raw_forward_command = _raw_forward_command(
        manifest, attempt_directory
    )
    lrat_conversion_command = _lrat_conversion_command(
        manifest, attempt_directory
    )
    checker_command = _lrat_check_command(manifest, attempt_directory)

    solver_resource = _write_phase_resource(
        run_directory,
        attempt_directory,
        phase="solver",
        memory_limit_mib=int(limits["solver_memory_mib"]),
        limits=limits,
    )
    if solver_resource["passed"] is not True:
        return (
            "RESOURCE_GATE_FAILED_NONCLAIM",
            {"failed_phase": "solver", "resource_report": solver_resource},
        )
    _verify_committed_source_binding(sources)
    _verify_tool_bindings(tools)
    solver_stdout = attempt_directory / "solver.stdout"
    solver_stderr = attempt_directory / "solver.stderr"
    solver = run_bounded_child(
        command=solver_command,
        cwd=campaign_root(),
        stdout_path=solver_stdout,
        stderr_path=solver_stderr,
        wall_limit_seconds=int(limits["solver_wall_seconds"]),
        memory_limit_mib=int(limits["solver_memory_mib"]),
        file_limit_mib=int(limits["file_limit_mib"]),
        readonly_paths={"case CNF": case_cnf},
    )
    _verify_child_artifacts(solver, solver_command)
    _verify_file_binding(case_binding, "case CNF")
    solver_failure = _child_failure_status(solver, "solver")
    if solver_failure is not None:
        return solver_failure, {"solver": _child_record(solver)}

    result_path = attempt_directory / "solver.result"
    proof_path = attempt_directory / "proof.raw.bdrat"
    result_binding = _optional_file_binding(result_path, "raw solver result")
    proof_binding = _optional_file_binding(proof_path, "raw binary DRAT proof")
    if result_binding is None:
        return (
            "SOLVER_INVALID_OUTPUT_NONCLAIM",
            {
                "reason": "solver result is absent",
                "solver": _child_record(solver),
                "raw_proof": proof_binding,
            },
        )
    try:
        parsed_status, candidate = classify_solver_result(
            case_cnf.read_bytes(), result_path.read_bytes()
        )
    except (ValueError, OSError) as error:
        return (
            "SOLVER_INVALID_OUTPUT_NONCLAIM",
            {
                "reason": f"{type(error).__name__}: {error}",
                "solver": _child_record(solver),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
            },
        )

    if parsed_status == "UNKNOWN":
        return (
            "SOLVER_UNKNOWN_NONCLAIM",
            {
                "solver": _child_record(solver),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
            },
        )
    if parsed_status == "SAT":
        if solver.exit_code != 10 or candidate is None:
            return (
                "SOLVER_INVALID_OUTPUT_NONCLAIM",
                {
                    "reason": "SAT status and exit code disagree",
                    "solver": _child_record(solver),
                    "raw_result": result_binding,
                    "raw_proof": proof_binding,
                },
            )
        candidate_payload = {
            "schema": "gamma-theta-order12-k4-sat-candidate-v1",
            "schema_version": SCHEMA_VERSION,
            "claim_status": (
                "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION"
            ),
            "case_id": case["case_id"],
            "case_cnf": case_binding,
            "raw_solver_result": result_binding,
            "solver": _child_record(solver),
            "decoded_assignment_summary": candidate,
            "required_next_action": (
                "Freeze the graph and family, then run a standalone verifier "
                "that imports no search transition or decoding core."
            ),
        }
        candidate_path = attempt_directory / "candidate.json"
        _write_exclusive(
            candidate_path, canonical_json_bytes(candidate_payload)
        )
        return (
            "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION",
            {
                "candidate": _file_binding(candidate_path, "SAT candidate"),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
                "solver": _child_record(solver),
            },
        )
    if parsed_status != "UNSAT" or solver.exit_code != 20:
        return (
            "SOLVER_INVALID_OUTPUT_NONCLAIM",
            {
                "reason": "UNSAT status and exit code disagree",
                "solver": _child_record(solver),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
            },
        )
    if proof_binding is None or proof_binding["size_bytes"] == 0:
        return (
            "SOLVER_INVALID_OUTPUT_NONCLAIM",
            {
                "reason": "UNSAT result has no nonempty raw proof",
                "solver": _child_record(solver),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
            },
        )

    raw_forward_resource = _write_phase_resource(
        run_directory,
        attempt_directory,
        phase="raw-forward",
        memory_limit_mib=int(limits["postprocess_memory_mib"]),
        limits=limits,
    )
    if raw_forward_resource["passed"] is not True:
        return (
            "RESOURCE_GATE_FAILED_NONCLAIM",
            {
                "failed_phase": "raw-forward",
                "resource_report": raw_forward_resource,
                "solver": _child_record(solver),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
            },
    )
    _verify_committed_source_binding(sources)
    _verify_tool_bindings(tools)
    raw_forward_stdout = attempt_directory / "raw-forward.stdout"
    raw_forward_stderr = attempt_directory / "raw-forward.stderr"
    raw_forward = run_bounded_child(
        command=raw_forward_command,
        cwd=campaign_root(),
        stdout_path=raw_forward_stdout,
        stderr_path=raw_forward_stderr,
        wall_limit_seconds=int(limits["converter_wall_seconds"]),
        memory_limit_mib=int(limits["postprocess_memory_mib"]),
        file_limit_mib=int(limits["file_limit_mib"]),
        readonly_paths={
            "case CNF": case_cnf,
            "raw binary DRAT proof": proof_path,
        },
    )
    _verify_child_artifacts(raw_forward, raw_forward_command)
    _verify_file_binding(case_binding, "case CNF")
    _verify_file_binding(proof_binding, "raw binary DRAT proof")
    raw_forward_failure = _child_failure_status(
        raw_forward, "raw_forward"
    )
    if raw_forward_failure is not None:
        return (
            raw_forward_failure,
            {
                "solver": _child_record(solver),
                "raw_forward": _child_record(raw_forward),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
            },
        )
    try:
        if raw_forward.exit_code != 0:
            raise ValueError(
                f"raw forward verifier exit code {raw_forward.exit_code}"
            )
        _strict_converter_success(
            raw_forward_stdout.read_bytes(),
            raw_forward_stderr.read_bytes(),
        )
    except (ValueError, OSError) as error:
        return (
            "RAW_FORWARD_REJECTED_NONCLAIM",
            {
                "reason": f"{type(error).__name__}: {error}",
                "solver": _child_record(solver),
                "raw_forward": _child_record(raw_forward),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
            },
        )

    conversion_resource = _write_phase_resource(
        run_directory,
        attempt_directory,
        phase="lrat-conversion",
        memory_limit_mib=int(limits["postprocess_memory_mib"]),
        limits=limits,
    )
    if conversion_resource["passed"] is not True:
        return (
            "RESOURCE_GATE_FAILED_NONCLAIM",
            {
                "failed_phase": "lrat-conversion",
                "resource_report": conversion_resource,
                "solver": _child_record(solver),
                "raw_forward": _child_record(raw_forward),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
            },
        )
    _verify_committed_source_binding(sources)
    _verify_tool_bindings(tools)
    conversion_stdout = attempt_directory / "lrat-conversion.stdout"
    conversion_stderr = attempt_directory / "lrat-conversion.stderr"
    conversion = run_bounded_child(
        command=lrat_conversion_command,
        cwd=campaign_root(),
        stdout_path=conversion_stdout,
        stderr_path=conversion_stderr,
        wall_limit_seconds=int(limits["converter_wall_seconds"]),
        memory_limit_mib=int(limits["postprocess_memory_mib"]),
        file_limit_mib=int(limits["file_limit_mib"]),
        readonly_paths={
            "case CNF": case_cnf,
            "raw binary DRAT proof": proof_path,
        },
    )
    _verify_child_artifacts(conversion, lrat_conversion_command)
    _verify_file_binding(case_binding, "case CNF")
    _verify_file_binding(proof_binding, "raw binary DRAT proof")
    conversion_failure = _child_failure_status(
        conversion, "lrat_conversion"
    )
    if conversion_failure is not None:
        return (
            conversion_failure,
            {
                "solver": _child_record(solver),
                "raw_forward": _child_record(raw_forward),
                "lrat_conversion": _child_record(conversion),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
            },
        )
    lrat_path = attempt_directory / "proof.converted.lrat"
    lrat_binding = _optional_file_binding(lrat_path, "converted LRAT proof")
    try:
        if conversion.exit_code != 0:
            raise ValueError(
                f"LRAT converter exit code {conversion.exit_code}"
            )
        _strict_converter_success(
            conversion_stdout.read_bytes(),
            conversion_stderr.read_bytes(),
        )
        if lrat_binding is None or lrat_binding["size_bytes"] == 0:
            raise ValueError("converted LRAT is absent or empty")
    except (ValueError, OSError) as error:
        return (
            "LRAT_CONVERSION_REJECTED_NONCLAIM",
            {
                "reason": f"{type(error).__name__}: {error}",
                "solver": _child_record(solver),
                "raw_forward": _child_record(raw_forward),
                "lrat_conversion": _child_record(conversion),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
                "converted_lrat": lrat_binding,
            },
        )

    checker_resource = _write_phase_resource(
        run_directory,
        attempt_directory,
        phase="lrat-check",
        memory_limit_mib=int(limits["postprocess_memory_mib"]),
        limits=limits,
    )
    if checker_resource["passed"] is not True:
        return (
            "RESOURCE_GATE_FAILED_NONCLAIM",
            {
                "failed_phase": "lrat-check",
                "resource_report": checker_resource,
                "solver": _child_record(solver),
                "raw_forward": _child_record(raw_forward),
                "lrat_conversion": _child_record(conversion),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
                "converted_lrat": lrat_binding,
            },
        )
    _verify_committed_source_binding(sources)
    _verify_tool_bindings(tools)
    checker_stdout = attempt_directory / "lrat-check.stdout"
    checker_stderr = attempt_directory / "lrat-check.stderr"
    checker = run_bounded_child(
        command=checker_command,
        cwd=campaign_root(),
        stdout_path=checker_stdout,
        stderr_path=checker_stderr,
        wall_limit_seconds=int(limits["checker_wall_seconds"]),
        memory_limit_mib=int(limits["postprocess_memory_mib"]),
        file_limit_mib=int(limits["file_limit_mib"]),
        readonly_paths={
            "case CNF": case_cnf,
            "converted LRAT proof": lrat_path,
        },
    )
    _verify_child_artifacts(checker, checker_command)
    _verify_file_binding(case_binding, "case CNF")
    _verify_file_binding(proof_binding, "raw binary DRAT proof")
    if lrat_binding is None:
        raise AssertionError("LRAT binding disappeared")
    _verify_file_binding(lrat_binding, "converted LRAT proof")
    checker_failure = _child_failure_status(checker, "lrat_check")
    if checker_failure is not None:
        return (
            checker_failure,
            {
                "solver": _child_record(solver),
                "raw_forward": _child_record(raw_forward),
                "lrat_conversion": _child_record(conversion),
                "lrat_check": _child_record(checker),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
                "converted_lrat": lrat_binding,
            },
        )
    try:
        if checker.exit_code != 0:
            raise ValueError(f"lrat-check exit code {checker.exit_code}")
        _strict_lrat_success(
            checker_stdout.read_bytes(), checker_stderr.read_bytes()
        )
    except (ValueError, OSError) as error:
        return (
            "LRAT_CHECK_REJECTED_NONCLAIM",
            {
                "reason": f"{type(error).__name__}: {error}",
                "solver": _child_record(solver),
                "raw_forward": _child_record(raw_forward),
                "lrat_conversion": _child_record(conversion),
                "lrat_check": _child_record(checker),
                "raw_result": result_binding,
                "raw_proof": proof_binding,
                "converted_lrat": lrat_binding,
            },
        )

    certificate_payload = {
        "schema": "gamma-theta-order12-k4-leaf-lrat-certificate-v2",
        "schema_version": SCHEMA_VERSION,
        "proof_pipeline": PROOF_PIPELINE_ID,
        "leaf_status": "UNSAT_LRAT_VERIFIED",
        "aggregate_status": (
            "NO_AGGREGATE_CLAIM_PENDING_INDEPENDENT_COVERAGE_AUDIT"
        ),
        "case_id": case["case_id"],
        "cube_literals": case["cube_literals"],
        "case_cnf": case_binding,
        "raw_solver_result": result_binding,
        "raw_binary_drat": proof_binding,
        "converted_lrat": lrat_binding,
        "solver": _child_record(solver),
        "raw_forward": _child_record(raw_forward),
        "lrat_conversion": _child_record(conversion),
        "lrat_check": _child_record(checker),
        "raw_forward_stdout": _file_binding(
            raw_forward_stdout, "raw forward stdout"
        ),
        "raw_forward_stderr": _file_binding(
            raw_forward_stderr, "raw forward stderr"
        ),
        "lrat_conversion_stdout": _file_binding(
            conversion_stdout, "LRAT conversion stdout"
        ),
        "lrat_conversion_stderr": _file_binding(
            conversion_stderr, "LRAT conversion stderr"
        ),
        "lrat_check_stdout": _file_binding(
            checker_stdout, "lrat-check stdout"
        ),
        "lrat_check_stderr": _file_binding(
            checker_stderr, "lrat-check stderr"
        ),
    }
    certificate_path = attempt_directory / "certificate.json"
    _write_exclusive(
        certificate_path, canonical_json_bytes(certificate_payload)
    )
    return (
        "UNSAT_LRAT_VERIFIED",
        {
            "certificate": _file_binding(
                certificate_path, "leaf certificate"
            ),
            "solver": _child_record(solver),
            "raw_forward": _child_record(raw_forward),
            "lrat_conversion": _child_record(conversion),
            "lrat_check": _child_record(checker),
        },
    )


def run_next_case(
    run_directory: Path,
    *,
    case_id: str | None = None,
    production_gate_open: bool = False,
) -> dict[str, object]:
    """Run at most one complete attempt, preserving every raw artifact."""

    _require_gate(production_gate_open, "production")
    run_directory = run_directory.resolve(strict=True)
    with RunLock(run_directory):
        audit_run(run_directory)
        (
            manifest,
            manifest_hash,
            partition,
            partition_hash,
            latest,
            latest_hash,
        ) = _reload_context(run_directory)
        selected_state = _select_case_state(latest, case_id)
        selected_id = str(selected_state["case_id"])
        case = _case_by_id(partition, selected_id)
        attempt_number = int(selected_state["attempt_count"]) + 1
        attempt_directory = (
            run_directory
            / CASE_DIRECTORY_NAME
            / f"case-{selected_id}"
            / f"attempt-{attempt_number:06d}"
        )
        os.mkdir(attempt_directory, 0o700)
        _fsync_directory(attempt_directory.parent)
        parent = (run_directory / PARENT_COPY_NAME).read_bytes()
        case_bytes = _case_cnf_bytes(parent, case["cube_literals"])
        if (
            sha256_bytes(case_bytes) != case["cnf_sha256"]
            or len(case_bytes) != case["cnf_size_bytes"]
        ):
            raise ValueError("materialized case CNF differs from partition")
        case_cnf_path = attempt_directory / "instance.cnf"
        _write_exclusive(case_cnf_path, case_bytes)
        attempt_config = {
            "schema": "gamma-theta-order12-k4-attempt-config-v1",
            "schema_version": SCHEMA_VERSION,
            "proof_pipeline": PROOF_PIPELINE_ID,
            "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
            "case_id": selected_id,
            "attempt_number": attempt_number,
            "seed": case["seed"],
            "cube_literals": case["cube_literals"],
            "case_cnf_sha256": case["cnf_sha256"],
            "run_manifest_sha256": manifest_hash,
            "partition_sha256": partition_hash,
            "solver_command": list(
                _solver_command(manifest, case, attempt_directory)
            ),
            "raw_forward_command": list(
                _raw_forward_command(manifest, attempt_directory)
            ),
            "lrat_conversion_command": list(
                _lrat_conversion_command(manifest, attempt_directory)
            ),
            "lrat_check_command": list(
                _lrat_check_command(manifest, attempt_directory)
            ),
            "created_unix_ns": time.time_ns(),
        }
        _write_exclusive(
            attempt_directory / "attempt-config.json",
            canonical_json_bytes(attempt_config),
        )

        reserved_state = dict(selected_state)
        reserved_state["status"] = "RUNNING_UNFINISHED_NONCLAIM"
        reserved_state["attempt_count"] = attempt_number
        reserved_state["active_attempt"] = attempt_number
        reserved_checkpoint = _append_checkpoint_transition(
            run_directory,
            latest=latest,
            latest_hash=latest_hash,
            run_manifest_sha256=manifest_hash,
            partition_sha256=partition_hash,
            case_id=selected_id,
            replacement=reserved_state,
            event={
                "kind": "ATTEMPT_RESERVED_NO_RESULT",
                "case_id": selected_id,
                "attempt_number": attempt_number,
                "attempt_config_sha256": sha256_file(
                    attempt_directory / "attempt-config.json"
                ),
            },
        )
        try:
            status, details = _execute_attempt(
                run_directory=run_directory,
                manifest=manifest,
                case=case,
                attempt_directory=attempt_directory,
            )
        except Exception as error:
            status = "ORCHESTRATOR_EXCEPTION_NONCLAIM"
            details = {
                "exception_type": type(error).__name__,
                "exception_message": str(error),
            }
        outcome = _write_outcome(
            attempt_directory,
            case_id=selected_id,
            attempt_number=attempt_number,
            status=status,
            details=details,
        )
        completed_state = dict(reserved_state)
        completed_state["status"] = (
            status
            if status
            in {
                "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION",
                "UNSAT_LRAT_VERIFIED",
            }
            else "RETRYABLE_NONCLAIM"
        )
        completed_state["active_attempt"] = None
        completed_state["last_completed_outcome_sha256"] = outcome["sha256"]
        completion_checkpoint = _append_checkpoint_transition(
            run_directory,
            latest={
                **latest,
                "sequence": int(latest["sequence"]) + 1,
                "cases": [
                    reserved_state
                    if isinstance(record, dict)
                    and record.get("case_id") == selected_id
                    else record
                    for record in latest["cases"]  # type: ignore[index]
                ],
            },
            latest_hash=str(reserved_checkpoint["sha256"]),
            run_manifest_sha256=manifest_hash,
            partition_sha256=partition_hash,
            case_id=selected_id,
            replacement=completed_state,
            event={
                "kind": "ATTEMPT_COMPLETED",
                "case_id": selected_id,
                "attempt_number": attempt_number,
                "outcome_status": status,
                "outcome_sha256": outcome["sha256"],
            },
        )
        final_audit = audit_run(run_directory)
    return {
        "status": status,
        "case_id": selected_id,
        "attempt_number": attempt_number,
        "outcome": outcome,
        "checkpoint": completion_checkpoint,
        "aggregate_status": final_audit["aggregate_status"],
        "claim_status": (
            "LEAF_UNSAT_ONLY"
            if status == "UNSAT_LRAT_VERIFIED"
            else "NO_MATHEMATICAL_CLAIM"
        ),
    }


def _commands_containing(path: Path) -> list[dict[str, object]]:
    """Conservatively detect a surviving child that still names an attempt."""

    completed = subprocess.run(
        ("/bin/ps", "-axo", "pid=,command="),
        cwd=campaign_root(),
        env={},
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
        timeout=15,
    )
    if completed.returncode != 0:
        raise RuntimeError("cannot audit process table before recovery")
    needle = str(path.resolve())
    matches: list[dict[str, object]] = []
    for raw_line in completed.stdout.decode("utf-8", "strict").splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        fields = stripped.split(maxsplit=1)
        if len(fields) != 2 or not fields[0].isdigit():
            raise RuntimeError("process table row is malformed")
        pid = int(fields[0])
        command = fields[1]
        if pid != os.getpid() and needle in command:
            matches.append({"pid": pid, "command": command})
    return matches


def recover_interrupted_attempt(
    run_directory: Path,
    *,
    recovery_gate_open: bool = False,
) -> dict[str, object]:
    """Reconcile one torn attempt as a preserved, retryable nonclaim."""

    _require_gate(recovery_gate_open, "interrupted-attempt recovery")
    run_directory = run_directory.resolve(strict=True)
    with RunLock(run_directory):
        audit_passed = False
        audit_error: ValueError | None = None
        try:
            audit_run(run_directory)
            audit_passed = True
        except ValueError as error:
            audit_error = error
        (
            manifest,
            manifest_hash,
            partition,
            partition_hash,
            latest,
            latest_hash,
        ) = _load_recovery_foundation(run_directory)
        raw_cases = latest.get("cases")
        if not isinstance(raw_cases, list):
            raise ValueError("latest cases are malformed")
        active = [
            record
            for record in raw_cases
            if isinstance(record, dict)
            and record.get("status") == "RUNNING_UNFINISHED_NONCLAIM"
        ]

        mode: str
        if audit_passed:
            if len(active) != 1:
                raise RuntimeError(
                    "expected exactly one active attempt, found "
                    f"{len(active)}"
                )
            state = dict(active[0])
            case_id = str(state["case_id"])
            attempt_number = int(state["active_attempt"])
            mode = "ACTIVE_WITHOUT_OUTCOME"
        else:
            orphan_candidates: list[tuple[dict[str, object], int]] = []
            for raw_state in raw_cases:
                if not isinstance(raw_state, dict):
                    raise ValueError("latest case state is malformed")
                if raw_state.get("active_attempt") is not None:
                    continue
                candidate_case_id = str(raw_state["case_id"])
                case_directory = (
                    run_directory
                    / CASE_DIRECTORY_NAME
                    / f"case-{candidate_case_id}"
                )
                attempts = sorted(case_directory.iterdir())
                expected_count = int(raw_state["attempt_count"])
                if len(attempts) == expected_count + 1:
                    orphan_candidates.append(
                        (dict(raw_state), expected_count + 1)
                    )
                elif len(attempts) != expected_count:
                    raise ValueError(
                        f"case {candidate_case_id} has an unsupported "
                        "attempt-count tear"
                    )
            active_with_outcome: list[dict[str, object]] = []
            for raw_state in active:
                candidate_case_id = str(raw_state["case_id"])
                candidate_attempt = int(raw_state["active_attempt"])
                candidate_directory = (
                    run_directory
                    / CASE_DIRECTORY_NAME
                    / f"case-{candidate_case_id}"
                    / f"attempt-{candidate_attempt:06d}"
                )
                if (candidate_directory / "outcome.json").is_file():
                    active_with_outcome.append(dict(raw_state))
            anomaly_count = len(orphan_candidates) + len(active_with_outcome)
            if anomaly_count != 1:
                if audit_error is not None:
                    raise ValueError(
                        "failed audit is not one supported crash window: "
                        f"{audit_error}"
                    ) from audit_error
                raise RuntimeError("no supported interrupted attempt found")
            if orphan_candidates:
                state, attempt_number = orphan_candidates[0]
                case_id = str(state["case_id"])
                mode = "ORPHAN_BEFORE_RESERVATION"
            else:
                state = active_with_outcome[0]
                case_id = str(state["case_id"])
                attempt_number = int(state["active_attempt"])
                mode = "OUTCOME_BEFORE_COMPLETION_CHECKPOINT"

        attempt_directory = (
            run_directory
            / CASE_DIRECTORY_NAME
            / f"case-{case_id}"
            / f"attempt-{attempt_number:06d}"
        )
        live = _commands_containing(attempt_directory)
        if live:
            raise RuntimeError(
                "refusing recovery because a process still names the "
                f"attempt directory: {live}"
            )
        case = _case_by_id(partition, case_id)
        config_path = attempt_directory / "attempt-config.json"
        _validate_attempt_config(
            _strict_json_file(config_path),
            manifest=manifest,
            manifest_hash=manifest_hash,
            partition_hash=partition_hash,
            case=case,
            attempt_number=attempt_number,
            attempt_directory=attempt_directory,
        )
        config_hash = sha256_file(config_path)
        event_index = _checkpoint_attempt_event_index(run_directory)

        if mode == "ORPHAN_BEFORE_RESERVATION":
            config_bindings = dict(
                event_index["attempt_config_sha256"]  # type: ignore[arg-type]
            )
            config_bindings[(case_id, attempt_number)] = config_hash
            synthetic_index = {
                **event_index,
                "attempt_config_sha256": config_bindings,
            }
            outcome_path = attempt_directory / "outcome.json"
            if outcome_path.exists() or outcome_path.is_symlink():
                outcome_hash = sha256_file(outcome_path)
                replacement = dict(state)
                replacement["status"] = "RETRYABLE_NONCLAIM"
                replacement["attempt_count"] = attempt_number
                replacement["active_attempt"] = None
                replacement["last_completed_outcome_sha256"] = outcome_hash
                synthetic_latest = {
                    **latest,
                    "cases": [
                        replacement
                        if isinstance(record, dict)
                        and record.get("case_id") == case_id
                        else record
                        for record in raw_cases
                    ],
                }
                _audit_attempts(
                    run_directory,
                    manifest,
                    manifest_hash,
                    partition,
                    partition_hash,
                    synthetic_latest,
                    synthetic_index,
                )
                outcome = _file_binding(
                    outcome_path, "orphan recovery outcome"
                )
            else:
                active_replacement = dict(state)
                active_replacement["status"] = (
                    "RUNNING_UNFINISHED_NONCLAIM"
                )
                active_replacement["attempt_count"] = attempt_number
                active_replacement["active_attempt"] = attempt_number
                synthetic_latest = {
                    **latest,
                    "cases": [
                        active_replacement
                        if isinstance(record, dict)
                        and record.get("case_id") == case_id
                        else record
                        for record in raw_cases
                    ],
                }
                _audit_attempts(
                    run_directory,
                    manifest,
                    manifest_hash,
                    partition,
                    partition_hash,
                    synthetic_latest,
                    synthetic_index,
                )
                outcome = _write_outcome(
                    attempt_directory,
                    case_id=case_id,
                    attempt_number=attempt_number,
                    status="INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM",
                    details={
                        "reconciliation_mode": mode,
                        "live_process_matches": live,
                        "action": (
                            "Preserve every byte and retry only in a new "
                            "exclusive attempt directory."
                        ),
                    },
                )
            replacement = dict(state)
            replacement["status"] = "RETRYABLE_NONCLAIM"
            replacement["attempt_count"] = attempt_number
            replacement["active_attempt"] = None
            replacement["last_completed_outcome_sha256"] = outcome["sha256"]
            event_kind = "ORPHAN_ATTEMPT_RECONCILED_NONCLAIM"
            event = {
                "kind": event_kind,
                "case_id": case_id,
                "attempt_number": attempt_number,
                "attempt_config_sha256": config_hash,
                "outcome_status": "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM",
                "outcome_sha256": outcome["sha256"],
            }
        elif mode == "OUTCOME_BEFORE_COMPLETION_CHECKPOINT":
            outcome_path = attempt_directory / "outcome.json"
            outcome_payload = _strict_json_file(outcome_path)
            if not isinstance(outcome_payload, dict):
                raise ValueError("torn completion outcome is malformed")
            outcome_hash = sha256_file(outcome_path)
            reconciled_outcomes = dict(
                event_index[
                    "reconciled_outcome_sha256"
                ]  # type: ignore[arg-type]
            )
            reconciled_outcomes[(case_id, attempt_number)] = outcome_hash
            synthetic_index = {
                **event_index,
                "reconciled_outcome_sha256": reconciled_outcomes,
            }
            replacement = dict(state)
            replacement["status"] = "RETRYABLE_NONCLAIM"
            replacement["active_attempt"] = None
            replacement["last_completed_outcome_sha256"] = outcome_hash
            synthetic_latest = {
                **latest,
                "cases": [
                    replacement
                    if isinstance(record, dict)
                    and record.get("case_id") == case_id
                    else record
                    for record in raw_cases
                ],
            }
            _audit_attempts(
                run_directory,
                manifest,
                manifest_hash,
                partition,
                partition_hash,
                synthetic_latest,
                synthetic_index,
            )
            outcome = _file_binding(
                outcome_path, "torn completion outcome"
            )
            event_kind = "OUTCOME_CHECKPOINT_RECONCILED_NONCLAIM"
            event = {
                "kind": event_kind,
                "case_id": case_id,
                "attempt_number": attempt_number,
                "original_outcome_status": outcome_payload.get("status"),
                "outcome_sha256": outcome_hash,
            }
        else:
            outcome = _write_outcome(
                attempt_directory,
                case_id=case_id,
                attempt_number=attempt_number,
                status="INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM",
                details={
                    "reconciliation_mode": mode,
                    "live_process_matches": live,
                    "action": (
                        "Preserve every byte and retry only in a new "
                        "exclusive attempt directory."
                    ),
                },
            )
            replacement = dict(state)
            replacement["status"] = "RETRYABLE_NONCLAIM"
            replacement["active_attempt"] = None
            replacement["last_completed_outcome_sha256"] = outcome["sha256"]
            event_kind = "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM"
            event = {
                "kind": event_kind,
                "case_id": case_id,
                "attempt_number": attempt_number,
                "outcome_sha256": outcome["sha256"],
            }

        checkpoint = _append_checkpoint_transition(
            run_directory,
            latest=latest,
            latest_hash=latest_hash,
            run_manifest_sha256=manifest_hash,
            partition_sha256=partition_hash,
            case_id=case_id,
            replacement=replacement,
            event=event,
        )
        final = audit_run(run_directory)
    return {
        "status": event_kind,
        "reconciliation_mode": mode,
        "case_id": case_id,
        "attempt_number": attempt_number,
        "outcome": outcome,
        "checkpoint": checkpoint,
        "aggregate_status": final["aggregate_status"],
        "claim_status": "NO_MATHEMATICAL_CLAIM",
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fail-closed production workflow for the exact order-12 k=4 CNF"
        )
    )
    subparsers = parser.add_subparsers(dest="operation", required=True)

    initialize = subparsers.add_parser(
        "initialize", help="create an exclusive run; never start a solver"
    )
    initialize.add_argument("--validation-gate-open", action="store_true")
    initialize.add_argument("--run-dir", type=Path, required=True)
    initialize.add_argument("--parent-cnf", type=Path)
    initialize.add_argument("--parent-manifest", type=Path)
    initialize.add_argument("--base-seed", type=int, default=0)
    initialize.add_argument(
        "--solver-wall-seconds",
        type=int,
        default=DEFAULT_SOLVER_WALL_SECONDS,
    )
    initialize.add_argument(
        "--converter-wall-seconds",
        type=int,
        default=DEFAULT_CONVERTER_WALL_SECONDS,
    )
    initialize.add_argument(
        "--checker-wall-seconds",
        type=int,
        default=DEFAULT_CHECKER_WALL_SECONDS,
    )
    initialize.add_argument(
        "--solver-memory-mib",
        type=int,
        default=DEFAULT_SOLVER_MEMORY_MIB,
    )
    initialize.add_argument(
        "--postprocess-memory-mib",
        type=int,
        default=DEFAULT_POSTPROCESS_MEMORY_MIB,
    )
    initialize.add_argument(
        "--file-limit-mib", type=int, default=DEFAULT_FILE_LIMIT_MIB
    )
    initialize.add_argument(
        "--disk-reserve-mib", type=int, default=DEFAULT_DISK_RESERVE_MIB
    )
    initialize.add_argument(
        "--memory-reserve-mib",
        type=int,
        default=DEFAULT_MEMORY_RESERVE_MIB,
    )
    initialize.add_argument(
        "--load-max", type=float, default=DEFAULT_LOAD_MAX
    )

    run = subparsers.add_parser(
        "run-next", help="run at most one pending or retryable leaf"
    )
    run.add_argument("--production-gate-open", action="store_true")
    run.add_argument("--run-dir", type=Path, required=True)
    run.add_argument("--case-id")

    recover = subparsers.add_parser(
        "recover-interrupted",
        help="preserve and close one interrupted attempt as a nonclaim",
    )
    recover.add_argument("--recovery-gate-open", action="store_true")
    recover.add_argument("--run-dir", type=Path, required=True)

    audit = subparsers.add_parser(
        "audit", help="rehash a run without starting any proof process"
    )
    audit.add_argument("--run-dir", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _build_parser().parse_args(argv)
    if arguments.operation == "initialize":
        report = initialize_run(
            run_directory=arguments.run_dir,
            parent_cnf=arguments.parent_cnf,
            parent_manifest=arguments.parent_manifest,
            base_seed=arguments.base_seed,
            solver_wall_seconds=arguments.solver_wall_seconds,
            converter_wall_seconds=arguments.converter_wall_seconds,
            checker_wall_seconds=arguments.checker_wall_seconds,
            solver_memory_mib=arguments.solver_memory_mib,
            postprocess_memory_mib=arguments.postprocess_memory_mib,
            file_limit_mib=arguments.file_limit_mib,
            disk_reserve_mib=arguments.disk_reserve_mib,
            memory_reserve_mib=arguments.memory_reserve_mib,
            load_max=arguments.load_max,
            validation_gate_open=arguments.validation_gate_open,
        )
    elif arguments.operation == "run-next":
        report = run_next_case(
            arguments.run_dir,
            case_id=arguments.case_id,
            production_gate_open=arguments.production_gate_open,
        )
    elif arguments.operation == "recover-interrupted":
        report = recover_interrupted_attempt(
            arguments.run_dir,
            recovery_gate_open=arguments.recovery_gate_open,
        )
    elif arguments.operation == "audit":
        report = audit_run(arguments.run_dir)
    else:
        raise AssertionError(f"unhandled operation {arguments.operation}")
    sys.stdout.buffer.write(canonical_json_bytes(report))
    if report["status"] in {
        "INITIALIZED_NO_SOLVER_RUN",
        "PASS_READ_ONLY_AUDIT_NO_MATHEMATICAL_CLAIM",
        "UNSAT_LRAT_VERIFIED",
        "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM",
    }:
        return 0
    if report["status"] == (
        "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION"
    ):
        return 3
    return 4
