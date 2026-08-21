#!/usr/bin/env python3
"""Standalone, fail-closed replay of the preserved v3 case 0111 proof.

This verifier deliberately does not invoke a SAT solver.  It binds a frozen
parent, partition, retained leaf, raw binary DRAT stream, strict normalizer,
drat-trim, and lrat-check by exact SHA-256 and size.  It reconstructs the leaf
CNF independently from the parent and cube, normalizes the complete raw stream,
requires warning-fatal RUP-only forward and backward checks, creates a fresh
LRAT proof, and checks that LRAT proof.

An author-side PASS is not promoted here to a leaf or aggregate mathematical
claim.  Promotion requires a separate hostile review of these exact bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any, BinaryIO, Sequence


SCHEMA = "gamma-theta-order12-k4-case0111-recovery-replay-v1"
SCHEMA_VERSION = 1
PIPELINE = "binary-drat-normalize-rup-forward-backward-lrat-recovery-v1"
NONCLAIM = (
    "NO_LEAF_OR_AGGREGATE_CLAIM_PENDING_SEPARATE_HOSTILE_REVIEW"
)

CASE_ID = "0111"
CUBE_VARIABLES = (4, 14, 23, 31)
CUBE_LITERALS = (-4, 14, 23, 31)
VARIABLE_COUNT = 18_381
PARENT_CLAUSE_COUNT = 114_742
CASE_CLAUSE_COUNT = 114_746
CASE_LITERAL_COUNT = 1_180_020
WALL_LIMIT_SECONDS = 1_800
MAX_LOG_BYTES = 1 << 20
MAX_UNSIGNED_VARINT_BYTES = 10

EXPECTED_SOURCE: dict[str, tuple[str, int]] = {
    "source/attempt/attempt-config.json": (
        "9bbb581acdae763ff06138ce6347f109531c7e490e7171f40a628e5295465eaa",
        4_444,
    ),
    "source/attempt/instance.cnf": (
        "c9c187a8a83485da527910c7bc24b666d43248077d6d690c04bf0485f9f90e99",
        3_992_967,
    ),
    "source/attempt/outcome.json": (
        "1aaba96b44a4554c9a56128cfc9d74c477399065c729eef5b9b0bccd6f2dab7f",
        8_574,
    ),
    "source/attempt/proof.raw.bdrat": (
        "64ffb7bf3a6a25d1839a234298b3e7bbebdbd491303821dcb613ff5d515b1ce7",
        6_481_140,
    ),
    "source/attempt/raw-forward.stderr": (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        0,
    ),
    "source/attempt/raw-forward.stdout": (
        "98d38ca1c57931602933c5b4ee760fbd5284a6b57133fd80b3421577d068c534",
        186,
    ),
    "source/attempt/resource-raw-forward.json": (
        "f62955d9cf18aeef16660f937c241120d03fc691d9d5b57fe3ef4d961b25326c",
        491,
    ),
    "source/attempt/resource-solver.json": (
        "e21d5a11f505eb781d52edcf379de5de0fa3dd987bfe0f2ea00cd3cfaa36b180",
        486,
    ),
    "source/attempt/solver.result": (
        "bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162",
        16,
    ),
    "source/attempt/solver.stderr": (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        0,
    ),
    "source/attempt/solver.stdout": (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        0,
    ),
    "source/frozen/normalize_bdrat.py": (
        "07229fce9293a05fed3fa6ef3f96415eb48ea4b0cdd8e9a329620017d2bced99",
        13_157,
    ),
    "source/frozen/parent-generator-manifest.json": (
        "621a0878c117dc8b4d6dbd0ba14c8402a8c24e8339d2f85cb23d61ffd74fbb61",
        4_113,
    ),
    "source/frozen/parent.cnf": (
        "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac",
        3_992_947,
    ),
    "source/frozen/partition.json": (
        "0cf8129734d5a5ea121a3f26c08b46dcbe2b4a154ef17ce24f50eb8d0266b33f",
        7_783,
    ),
    "source/frozen/run-manifest.json": (
        "d3c914f38ea3771d65db76ed14e092ea0ce84003b1fff73839e033903361ed60",
        7_691,
    ),
    "tools/drat-trim": (
        "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb",
        70_088,
    ),
    "tools/lrat-check": (
        "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2",
        36_520,
    ),
}

EXPECTED_NORMALIZED = (
    "b1bc9b3a26fe26acddf2c49c4202ebf82adba8298d5e3c0b386af35ec2c663e3",
    2_632_766,
)
EXPECTED_LRAT = (
    "5300c54b1e22492cbcae83a47898549c38ee799a33eba23fbe5d11123233dd54",
    23_297_665,
)
EXPECTED_NORMALIZER_PYTHON_SHA256 = (
    "b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf"
)
EXPECTED_RAW_STATS = {
    "records": 391_069,
    "additions": 158_688,
    "deletions": 232_381,
    "literals": 4_701_987,
    "addition_literals": 1_843_230,
    "maximum_variable": 18_381,
    "empty_addition_records": [391_069],
}
EXPECTED_NORMALIZED_STATS = {
    "records": 158_688,
    "additions": 158_688,
    "deletions": 0,
    "literals": 1_843_230,
    "addition_literals": 1_843_230,
    "maximum_variable": 18_381,
    "empty_addition_records": [158_688],
}


class AuditError(RuntimeError):
    """A fail-closed audit rejection."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_json_bytes(payload: object) -> bytes:
    return (
        json.dumps(
            payload,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _reject_constant(value: str) -> None:
    raise AuditError(f"non-finite JSON number {value!r}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AuditError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _load_json(path: Path) -> Any:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise AuditError(f"cannot read JSON {path}: {error}") from error
    try:
        return json.loads(
            payload,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditError(f"malformed JSON {path}: {error}") from error


def _write_exclusive(path: Path, payload: bytes, mode: int = 0o600) -> None:
    try:
        descriptor = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            mode,
        )
    except OSError as error:
        raise AuditError(f"cannot create {path}: {error}") from error
    try:
        with os.fdopen(descriptor, "wb", buffering=0) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        raise


def _write_json_exclusive(path: Path, payload: object) -> None:
    _write_exclusive(path, _canonical_json_bytes(payload))


def _regular_single_link(path: Path, role: str) -> os.stat_result:
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise AuditError(f"{role} is absent: {path}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise AuditError(f"{role} is not a regular non-symlink file: {path}")
    if metadata.st_nlink != 1:
        raise AuditError(f"{role} does not have exactly one link: {path}")
    return metadata


def _check_file(
    path: Path,
    expected_sha256: str,
    expected_size: int,
    role: str,
) -> dict[str, Any]:
    metadata = _regular_single_link(path, role)
    if metadata.st_size != expected_size:
        raise AuditError(
            f"{role} size mismatch: {metadata.st_size} != {expected_size}"
        )
    observed_sha256 = _sha256_file(path)
    if observed_sha256 != expected_sha256:
        raise AuditError(
            f"{role} SHA-256 mismatch: {observed_sha256} "
            f"!= {expected_sha256}"
        )
    return {
        "path": str(path),
        "sha256": observed_sha256,
        "size_bytes": metadata.st_size,
    }


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _validate_sources(package: Path) -> dict[str, Any]:
    inventory: dict[str, Any] = {}
    for relative, (digest, size) in sorted(EXPECTED_SOURCE.items()):
        path = package / relative
        inventory[relative] = _check_file(
            path, digest, size, f"frozen source {relative}"
        )
    for relative in ("tools/drat-trim", "tools/lrat-check"):
        path = package / relative
        _require(
            os.access(path, os.X_OK),
            f"frozen checker is not executable: {relative}",
        )

    run = _load_json(package / "source/frozen/run-manifest.json")
    _require(
        isinstance(run, dict)
        and run.get("schema") == "gamma-theta-order12-k4-production-run-v1"
        and run.get("schema_version") == 1,
        "frozen run manifest schema mismatch",
    )
    _require(
        run.get("proof_pipeline")
        == "binary-drat-raw-forward-normalize-rup-forward-backward-lrat-v3",
        "frozen run proof pipeline mismatch",
    )
    _require(
        run.get("claim_status") == "NO_SAT_OR_UNSAT_CLAIM",
        "frozen run claim boundary changed",
    )
    _require(
        run.get("retained_parent_cnf", {}).get("sha256")
        == EXPECTED_SOURCE["source/frozen/parent.cnf"][0],
        "run manifest retained-parent binding mismatch",
    )
    _require(
        run.get("partition", {}).get("sha256")
        == EXPECTED_SOURCE["source/frozen/partition.json"][0],
        "run manifest partition binding mismatch",
    )
    runtime_records = run.get("runtime_sources", {}).get("records")
    _require(isinstance(runtime_records, list), "runtime source records absent")
    normalizer_records = [
        record
        for record in runtime_records
        if isinstance(record, dict)
        and record.get("path")
        == "src/search/k4_production/normalize_bdrat.py"
    ]
    _require(
        len(normalizer_records) == 1
        and normalizer_records[0].get("sha256")
        == EXPECTED_SOURCE["source/frozen/normalize_bdrat.py"][0]
        and normalizer_records[0].get("size_bytes")
        == EXPECTED_SOURCE["source/frozen/normalize_bdrat.py"][1],
        "run manifest frozen-normalizer binding mismatch",
    )
    for role, relative in (
        ("drat_trim", "tools/drat-trim"),
        ("lrat_check", "tools/lrat-check"),
    ):
        _require(
            run.get("tools", {}).get(role, {}).get("sha256")
            == EXPECTED_SOURCE[relative][0],
            f"run manifest {role} binding mismatch",
        )
    _require(
        run.get("tools", {}).get("normalizer_python", {}).get("sha256")
        == EXPECTED_NORMALIZER_PYTHON_SHA256
        and _sha256_file(Path(sys.executable))
        == EXPECTED_NORMALIZER_PYTHON_SHA256,
        "active Python is not the frozen normalizer runtime",
    )

    parent_manifest = _load_json(
        package / "source/frozen/parent-generator-manifest.json"
    )
    _require(
        isinstance(parent_manifest, dict)
        and parent_manifest.get("schema")
        == "gamma-theta-order12-k4-parent-cnf-v1"
        and parent_manifest.get("schema_version") == 1,
        "parent generator manifest schema mismatch",
    )
    _require(
        parent_manifest.get("cnf_sha256")
        == EXPECTED_SOURCE["source/frozen/parent.cnf"][0]
        and parent_manifest.get("variable_count") == VARIABLE_COUNT
        and parent_manifest.get("clause_count") == PARENT_CLAUSE_COUNT
        and parent_manifest.get("literal_count") == 1_180_016,
        "parent generator census or binding mismatch",
    )
    _require(
        parent_manifest.get("mode") == "full"
        and parent_manifest.get("order") == 12
        and parent_manifest.get("parameter") == 4
        and parent_manifest.get("connected_graphs_only") is True
        and parent_manifest.get("complete_anchored_coloring_bank") is True
        and parent_manifest.get("outer_signature_breaker") is True,
        "parent generator scope mismatch",
    )

    partition = _load_json(package / "source/frozen/partition.json")
    _require(
        isinstance(partition, dict)
        and partition.get("schema")
        == "gamma-theta-order12-k4-boolean-cube-partition-v1"
        and partition.get("schema_version") == 1,
        "partition schema mismatch",
    )
    _require(
        partition.get("parent_cnf_sha256")
        == EXPECTED_SOURCE["source/frozen/parent.cnf"][0]
        and partition.get("cube_variables") == list(CUBE_VARIABLES)
        and partition.get("case_count") == 16,
        "partition parent/cube census mismatch",
    )
    cases = partition.get("cases")
    _require(isinstance(cases, list) and len(cases) == 16, "case list malformed")
    expected_case_ids = {f"{value:04b}" for value in range(16)}
    observed_case_ids = {
        entry.get("case_id") for entry in cases if isinstance(entry, dict)
    }
    _require(
        observed_case_ids == expected_case_ids,
        "partition does not contain each four-bit cube exactly once",
    )
    case_entries = [
        entry
        for entry in cases
        if isinstance(entry, dict) and entry.get("case_id") == CASE_ID
    ]
    _require(len(case_entries) == 1, "case 0111 entry is not unique")
    case_entry = case_entries[0]
    _require(
        case_entry
        == {
            "case_id": "0111",
            "case_index": 7,
            "clause_count": CASE_CLAUSE_COUNT,
            "cnf_sha256": EXPECTED_SOURCE[
                "source/attempt/instance.cnf"
            ][0],
            "cnf_size_bytes": EXPECTED_SOURCE[
                "source/attempt/instance.cnf"
            ][1],
            "cube_bits": [0, 1, 1, 1],
            "cube_literals": list(CUBE_LITERALS),
            "literal_count": CASE_LITERAL_COUNT,
            "seed": 7,
            "variable_count": VARIABLE_COUNT,
        },
        "case 0111 partition entry mismatch",
    )

    attempt = _load_json(package / "source/attempt/attempt-config.json")
    _require(
        isinstance(attempt, dict)
        and attempt.get("schema")
        == "gamma-theta-order12-k4-attempt-config-v3"
        and attempt.get("schema_version") == 3,
        "attempt config schema mismatch",
    )
    _require(
        attempt.get("claim_status") == "NO_SAT_OR_UNSAT_CLAIM"
        and attempt.get("construction_status") == "ORIGINAL_PRE_RESERVATION"
        and attempt.get("case_id") == CASE_ID
        and attempt.get("attempt_number") == 1
        and attempt.get("seed") == 7
        and attempt.get("cube_literals") == list(CUBE_LITERALS)
        and attempt.get("case_cnf_sha256")
        == EXPECTED_SOURCE["source/attempt/instance.cnf"][0]
        and attempt.get("run_manifest_sha256")
        == EXPECTED_SOURCE["source/frozen/run-manifest.json"][0]
        and attempt.get("partition_sha256")
        == EXPECTED_SOURCE["source/frozen/partition.json"][0],
        "attempt config source binding mismatch",
    )

    outcome = _load_json(package / "source/attempt/outcome.json")
    _require(
        isinstance(outcome, dict)
        and outcome.get("schema")
        == "gamma-theta-order12-k4-attempt-outcome-v2"
        and outcome.get("schema_version") == 2,
        "attempt outcome schema mismatch",
    )
    _require(
        outcome.get("status") == "RAW_FORWARD_REJECTED_NONCLAIM"
        and outcome.get("mathematical_claim") == "NONE"
        and outcome.get("aggregate_claim") == "NONE"
        and outcome.get("case_id") == CASE_ID
        and outcome.get("attempt_number") == 1,
        "preserved outcome claim boundary mismatch",
    )
    raw_forward = outcome.get("details", {}).get("raw_forward", {})
    _require(
        raw_forward.get("exit_code") == 80
        and raw_forward.get("timed_out") is False
        and raw_forward.get("memory_limit_exceeded") is False
        and "raw forward verifier exit code 80"
        in outcome.get("details", {}).get("reason", ""),
        "preserved raw-forward rejection is not the expected exit 80",
    )
    raw_proof = outcome.get("details", {}).get("raw_proof", {})
    _require(
        raw_proof.get("sha256")
        == EXPECTED_SOURCE["source/attempt/proof.raw.bdrat"][0]
        and raw_proof.get("size_bytes")
        == EXPECTED_SOURCE["source/attempt/proof.raw.bdrat"][1],
        "outcome raw-proof binding mismatch",
    )
    solver = outcome.get("details", {}).get("solver", {})
    _require(
        solver.get("exit_code") == 20
        and solver.get("timed_out") is False
        and solver.get("memory_limit_exceeded") is False,
        "preserved solver metadata mismatch",
    )
    _require(
        (package / "source/attempt/solver.result").read_bytes()
        == b"s UNSATISFIABLE\n",
        "preserved solver result bytes mismatch",
    )
    raw_forward_stdout = (
        package / "source/attempt/raw-forward.stdout"
    ).read_bytes()
    _require(
        b"start forward verification" in raw_forward_stdout
        and b"VERIFIED" not in raw_forward_stdout,
        "preserved raw-forward stdout is inconsistent with early rejection",
    )
    return inventory


def _parse_dimacs(path: Path) -> dict[str, int]:
    metadata = _regular_single_link(path, "DIMACS CNF")
    clause_count = 0
    literal_count = 0
    maximum_variable = 0
    with path.open("rb") as handle:
        header = handle.readline()
        try:
            fields = header.decode("ascii").split()
        except UnicodeDecodeError as error:
            raise AuditError("DIMACS header is not ASCII") from error
        _require(
            len(fields) == 4 and fields[:2] == ["p", "cnf"],
            "malformed DIMACS header",
        )
        try:
            declared_variables = int(fields[2])
            declared_clauses = int(fields[3])
        except ValueError as error:
            raise AuditError("non-integer DIMACS census") from error
        for line_number, raw_line in enumerate(handle, start=2):
            _require(raw_line.endswith(b"\n"), f"line {line_number} lacks LF")
            try:
                tokens = raw_line.decode("ascii").split()
                values = [int(token) for token in tokens]
            except (UnicodeDecodeError, ValueError) as error:
                raise AuditError(f"malformed DIMACS line {line_number}") from error
            _require(
                len(values) >= 2
                and values[-1] == 0
                and 0 not in values[:-1],
                f"malformed clause terminator at line {line_number}",
            )
            clause_count += 1
            literal_count += len(values) - 1
            for literal in values[:-1]:
                variable = abs(literal)
                _require(
                    1 <= variable <= declared_variables,
                    f"literal out of range at line {line_number}",
                )
                maximum_variable = max(maximum_variable, variable)
    _require(
        declared_clauses == clause_count,
        "DIMACS declared/observed clause count mismatch",
    )
    return {
        "size_bytes": metadata.st_size,
        "variables": declared_variables,
        "clauses": clause_count,
        "literals": literal_count,
        "maximum_variable": maximum_variable,
    }


def _reconstruct_case(package: Path, replay: Path) -> dict[str, Any]:
    parent_path = package / "source/frozen/parent.cnf"
    retained_case_path = package / "source/attempt/instance.cnf"
    parent = parent_path.read_bytes()
    _require(parent.endswith(b"\n"), "parent CNF does not end in LF")
    first_lf = parent.find(b"\n")
    _require(first_lf >= 0, "parent CNF header is absent")
    _require(
        parent[: first_lf + 1]
        == b"p cnf 18381 114742\n",
        "parent CNF header mismatch",
    )
    cube_bytes = b"".join(
        f"{literal} 0\n".encode("ascii") for literal in CUBE_LITERALS
    )
    reconstructed = (
        b"p cnf 18381 114746\n" + parent[first_lf + 1 :] + cube_bytes
    )
    output_path = replay / "reconstructed-instance.cnf"
    _write_exclusive(output_path, reconstructed)
    expected_hash, expected_size = EXPECTED_SOURCE[
        "source/attempt/instance.cnf"
    ]
    output_record = _check_file(
        output_path,
        expected_hash,
        expected_size,
        "independently reconstructed case CNF",
    )
    _require(
        reconstructed == retained_case_path.read_bytes(),
        "retained case CNF differs byte-for-byte from reconstruction",
    )
    census = _parse_dimacs(output_path)
    _require(
        census
        == {
            "size_bytes": expected_size,
            "variables": VARIABLE_COUNT,
            "clauses": CASE_CLAUSE_COUNT,
            "literals": CASE_LITERAL_COUNT,
            "maximum_variable": VARIABLE_COUNT,
        },
        "reconstructed case CNF census mismatch",
    )
    return {"artifact": output_record, "census": census}


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


def _scan_binary_drat(path: Path) -> dict[str, Any]:
    _regular_single_link(path, "binary DRAT stream")
    payload = path.read_bytes()
    cursor = 0
    records = 0
    additions = 0
    deletions = 0
    literals = 0
    addition_literals = 0
    maximum_variable = 0
    empty_additions: list[int] = []
    max_encoded_value = 2 * VARIABLE_COUNT + 1
    while cursor < len(payload):
        prefix = payload[cursor]
        cursor += 1
        records += 1
        _require(
            prefix in (ord("a"), ord("d")),
            f"binary DRAT record {records} has invalid prefix",
        )
        is_addition = prefix == ord("a")
        additions += int(is_addition)
        deletions += int(not is_addition)
        clause_length = 0
        while True:
            start = cursor
            value = 0
            shift = 0
            while True:
                _require(
                    cursor < len(payload),
                    f"binary DRAT record {records} has truncated varint",
                )
                byte = payload[cursor]
                cursor += 1
                _require(
                    cursor - start <= MAX_UNSIGNED_VARINT_BYTES,
                    f"binary DRAT record {records} has overlong varint",
                )
                value |= (byte & 0x7F) << shift
                if byte < 0x80:
                    break
                shift += 7
            _require(
                payload[start:cursor] == _encode_unsigned(value),
                f"binary DRAT record {records} has noncanonical varint",
            )
            _require(
                value <= max_encoded_value,
                f"binary DRAT record {records} exceeds variable bound",
            )
            if value == 0:
                break
            _require(
                value != 1,
                f"binary DRAT record {records} contains negative zero",
            )
            variable = value >> 1
            _require(
                1 <= variable <= VARIABLE_COUNT,
                f"binary DRAT record {records} variable is out of range",
            )
            maximum_variable = max(maximum_variable, variable)
            clause_length += 1
            literals += 1
            if is_addition:
                addition_literals += 1
        if is_addition and clause_length == 0:
            empty_additions.append(records)
        _require(
            is_addition or clause_length > 0,
            f"binary DRAT record {records} is an empty deletion",
        )
    return {
        "records": records,
        "additions": additions,
        "deletions": deletions,
        "literals": literals,
        "addition_literals": addition_literals,
        "maximum_variable": maximum_variable,
        "empty_addition_records": empty_additions,
    }


def _run_phase(
    replay: Path,
    phase: str,
    command: Sequence[str],
    *,
    expected_exit: int = 0,
) -> dict[str, Any]:
    _require(command, f"{phase}: empty command")
    executable = Path(command[0])
    executable_before = _sha256_file(executable)
    stdout_path = replay / f"{phase}.stdout"
    stderr_path = replay / f"{phase}.stderr"
    resource_path = replay / f"resource-{phase}.json"
    started_unix_ns = time.time_ns()
    started_monotonic = time.monotonic()
    timed_out = False
    usage: resource.struct_rusage | None = None
    with stdout_path.open("xb", buffering=0) as stdout_handle, stderr_path.open(
        "xb", buffering=0
    ) as stderr_handle:
        process = subprocess.Popen(
            list(command),
            stdin=subprocess.DEVNULL,
            stdout=stdout_handle,
            stderr=stderr_handle,
            close_fds=True,
            start_new_session=True,
        )
        deadline = started_monotonic + WALL_LIMIT_SECONDS
        while True:
            waited_pid, wait_status, child_usage = os.wait4(
                process.pid, os.WNOHANG
            )
            if waited_pid == process.pid:
                process.returncode = os.waitstatus_to_exitcode(wait_status)
                usage = child_usage
                break
            if time.monotonic() >= deadline:
                timed_out = True
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                waited_pid, wait_status, child_usage = os.wait4(process.pid, 0)
                _require(
                    waited_pid == process.pid,
                    f"{phase}: failed to reap timed-out child",
                )
                process.returncode = os.waitstatus_to_exitcode(wait_status)
                usage = child_usage
                break
            time.sleep(0.05)
    finished_unix_ns = time.time_ns()
    wall_seconds = time.monotonic() - started_monotonic
    _require(usage is not None, f"{phase}: child resource usage absent")
    executable_after = _sha256_file(executable)
    _require(
        executable_after == executable_before,
        f"{phase}: executable changed during execution",
    )
    stdout_size = stdout_path.stat().st_size
    stderr_size = stderr_path.stat().st_size
    _require(
        stdout_size <= MAX_LOG_BYTES and stderr_size <= MAX_LOG_BYTES,
        f"{phase}: checker log exceeds safety bound",
    )
    maxrss_unit = "bytes" if sys.platform == "darwin" else "kibibytes"
    maxrss_mib = (
        usage.ru_maxrss / (1024 * 1024)
        if sys.platform == "darwin"
        else usage.ru_maxrss / 1024
    )
    report = {
        "schema": "gamma-theta-case0111-recovery-resource-v1",
        "schema_version": 1,
        "phase": phase,
        "command": list(command),
        "command_sha256": hashlib.sha256(
            _canonical_json_bytes(list(command))
        ).hexdigest(),
        "executable_sha256_before": executable_before,
        "executable_sha256_after": executable_after,
        "started_unix_ns": started_unix_ns,
        "finished_unix_ns": finished_unix_ns,
        "wall_limit_seconds": WALL_LIMIT_SECONDS,
        "wall_seconds": wall_seconds,
        "user_cpu_seconds": usage.ru_utime,
        "system_cpu_seconds": usage.ru_stime,
        "maximum_resident_set_size_raw": usage.ru_maxrss,
        "maximum_resident_set_size_raw_unit": maxrss_unit,
        "maximum_resident_set_size_mib": maxrss_mib,
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "stdout": {
            "path": str(stdout_path),
            "sha256": _sha256_file(stdout_path),
            "size_bytes": stdout_size,
        },
        "stderr": {
            "path": str(stderr_path),
            "sha256": _sha256_file(stderr_path),
            "size_bytes": stderr_size,
        },
    }
    _write_json_exclusive(resource_path, report)
    _require(not timed_out, f"{phase}: checker timed out")
    _require(
        process.returncode == expected_exit,
        f"{phase}: exit {process.returncode}, expected {expected_exit}",
    )
    return report


def _require_verified_output(
    replay: Path,
    phase: str,
    verified_marker: bytes,
    *,
    require_zero_rat: bool,
) -> None:
    stdout = (replay / f"{phase}.stdout").read_bytes()
    stderr = (replay / f"{phase}.stderr").read_bytes()
    _require(verified_marker in stdout, f"{phase}: VERIFIED marker absent")
    _require(stderr == b"", f"{phase}: stderr is nonempty")
    lowered = stdout.lower()
    _require(b"warning" not in lowered, f"{phase}: warning text present")
    if require_zero_rat:
        _require(b"0 RAT lemmas" in stdout, f"{phase}: non-RUP proof observed")


def _artifact(path: Path) -> dict[str, Any]:
    metadata = _regular_single_link(path, f"replay artifact {path.name}")
    return {
        "path": str(path),
        "sha256": _sha256_file(path),
        "size_bytes": metadata.st_size,
    }


def _validate_stored_author_replay(package: Path) -> dict[str, Any] | None:
    stored = package / "author-replay"
    if not stored.is_dir():
        return None
    normalized = stored / "proof.normalized.rup.bdrat"
    lrat = stored / "proof.converted.lrat"
    reconstructed = stored / "reconstructed-instance.cnf"
    report_path = stored / "replay-report.json"
    for path in (normalized, lrat, reconstructed, report_path):
        _regular_single_link(path, f"stored author artifact {path.name}")
    normalized_record = _check_file(
        normalized,
        EXPECTED_NORMALIZED[0],
        EXPECTED_NORMALIZED[1],
        "stored normalized proof",
    )
    lrat_record = _check_file(
        lrat,
        EXPECTED_LRAT[0],
        EXPECTED_LRAT[1],
        "stored LRAT proof",
    )
    reconstructed_record = _check_file(
        reconstructed,
        EXPECTED_SOURCE["source/attempt/instance.cnf"][0],
        EXPECTED_SOURCE["source/attempt/instance.cnf"][1],
        "stored reconstructed CNF",
    )
    report = _load_json(report_path)
    _require(
        isinstance(report, dict)
        and report.get("schema") == SCHEMA
        and report.get("schema_version") == SCHEMA_VERSION
        and report.get("status") == "AUTHOR_RECOVERY_REPLAY_PASSED"
        and report.get("claim_status") == NONCLAIM
        and report.get("mathematical_claim") == "NONE",
        "stored author replay report crosses the claim boundary",
    )
    verifier_record = report.get("verifier", {})
    _require(
        isinstance(verifier_record, dict)
        and verifier_record.get("sha256")
        == _sha256_file(package / "verify_recovery.py")
        and verifier_record.get("size_bytes")
        == (package / "verify_recovery.py").stat().st_size,
        "stored author replay is not bound to the current verifier bytes",
    )
    expected_phase_exits = {
        "raw-forward-reproduction": 80,
        "normalizer": 0,
        "normalized-forward": 0,
        "lrat-conversion": 0,
        "lrat-check": 0,
    }
    for phase, expected_exit in expected_phase_exits.items():
        phase_report = _load_json(stored / f"resource-{phase}.json")
        _require(
            isinstance(phase_report, dict)
            and phase_report.get("exit_code") == expected_exit
            and phase_report.get("timed_out") is False,
            f"stored resource report rejects phase {phase}",
        )
    return {
        "normalized": normalized_record,
        "lrat": lrat_record,
        "reconstructed_cnf": reconstructed_record,
        "report": _artifact(report_path),
    }


def _replay(package: Path, replay: Path) -> dict[str, Any]:
    source_inventory = _validate_sources(package)
    reconstructed = _reconstruct_case(package, replay)
    raw_path = package / "source/attempt/proof.raw.bdrat"
    raw_stats = _scan_binary_drat(raw_path)
    _require(raw_stats == EXPECTED_RAW_STATS, "raw bDRAT census mismatch")
    _require(
        raw_stats["empty_addition_records"]
        == [raw_stats["records"]],
        "raw bDRAT empty addition is not unique and final",
    )

    drat_trim = package / "tools/drat-trim"
    case_cnf = replay / "reconstructed-instance.cnf"
    raw_forward_command = [
        str(drat_trim),
        str(case_cnf),
        str(raw_path),
        "-i",
        "-f",
        "-W",
        "-t",
        str(WALL_LIMIT_SECONDS),
    ]
    _run_phase(
        replay,
        "raw-forward-reproduction",
        raw_forward_command,
        expected_exit=80,
    )
    raw_forward_stdout = (
        replay / "raw-forward-reproduction.stdout"
    ).read_bytes()
    raw_forward_stderr = (
        replay / "raw-forward-reproduction.stderr"
    ).read_bytes()
    _require(
        b"start forward verification" in raw_forward_stdout
        and b"VERIFIED" not in raw_forward_stdout
        and raw_forward_stderr == b"",
        "fresh raw-forward exit-80 reproduction differs from preserved failure",
    )

    normalizer_path = package / "source/frozen/normalize_bdrat.py"
    normalized_path = replay / "proof.normalized.rup.bdrat"
    normalization_report_path = replay / "normalization-report.json"
    normalizer_command = [
        sys.executable,
        str(normalizer_path),
        "--input",
        str(raw_path),
        "--output",
        str(normalized_path),
        "--report",
        str(normalization_report_path),
        "--max-variable",
        str(VARIABLE_COUNT),
    ]
    _run_phase(replay, "normalizer", normalizer_command)
    _require_verified_output(
        replay, "normalizer", b"s NORMALIZED", require_zero_rat=False
    )
    normalized_record = _check_file(
        normalized_path,
        EXPECTED_NORMALIZED[0],
        EXPECTED_NORMALIZED[1],
        "fresh normalized addition-only proof",
    )
    normalization = _load_json(normalization_report_path)
    _require(
        isinstance(normalization, dict)
        and normalization.get("schema")
        == "gamma-theta-order12-k4-binary-drat-normalization-v1"
        and normalization.get("schema_version") == 1
        and normalization.get("policy")
        == "canonical-additions-only-unique-empty-full-stream-v1"
        and normalization.get("claim_status")
        == "TRANSFORMATION_ONLY_NO_PROOF_CLAIM"
        and normalization.get("max_variable_allowed") == VARIABLE_COUNT
        and normalization.get("max_variable_observed") == VARIABLE_COUNT
        and normalization.get("empty_addition_record_index") == 391_069
        and normalization.get("record_counts")
        == {
            "total": 391_069,
            "additions": 158_688,
            "deletions": 232_381,
            "post_empty_deletions": 0,
            "literals": 4_701_987,
        }
        and normalization.get("input", {}).get("sha256")
        == EXPECTED_SOURCE["source/attempt/proof.raw.bdrat"][0]
        and normalization.get("input", {}).get("size_bytes")
        == EXPECTED_SOURCE["source/attempt/proof.raw.bdrat"][1]
        and normalization.get("output", {}).get("sha256")
        == EXPECTED_NORMALIZED[0]
        and normalization.get("output", {}).get("size_bytes")
        == EXPECTED_NORMALIZED[1],
        "strict normalization report mismatch",
    )
    normalized_stats = _scan_binary_drat(normalized_path)
    _require(
        normalized_stats == EXPECTED_NORMALIZED_STATS,
        "normalized bDRAT census mismatch",
    )
    _require(
        normalized_stats["empty_addition_records"]
        == [normalized_stats["records"]],
        "normalized proof empty addition is not unique and final",
    )

    forward_command = [
        str(drat_trim),
        str(case_cnf),
        str(normalized_path),
        "-i",
        "-f",
        "-W",
        "-U",
        "-t",
        str(WALL_LIMIT_SECONDS),
    ]
    _run_phase(replay, "normalized-forward", forward_command)
    _require_verified_output(
        replay,
        "normalized-forward",
        b"s VERIFIED",
        require_zero_rat=True,
    )

    lrat_path = replay / "proof.converted.lrat"
    conversion_command = [
        str(drat_trim),
        str(case_cnf),
        str(normalized_path),
        "-i",
        "-W",
        "-U",
        "-L",
        str(lrat_path),
        "-t",
        str(WALL_LIMIT_SECONDS),
    ]
    _run_phase(replay, "lrat-conversion", conversion_command)
    _require_verified_output(
        replay,
        "lrat-conversion",
        b"s VERIFIED",
        require_zero_rat=True,
    )
    lrat_record = _check_file(
        lrat_path,
        EXPECTED_LRAT[0],
        EXPECTED_LRAT[1],
        "fresh converted LRAT proof",
    )

    lrat_check = package / "tools/lrat-check"
    lrat_check_command = [
        str(lrat_check),
        str(case_cnf),
        str(lrat_path),
    ]
    _run_phase(replay, "lrat-check", lrat_check_command)
    _require_verified_output(
        replay, "lrat-check", b"c VERIFIED", require_zero_rat=False
    )

    artifacts = {
        path.name: _artifact(path)
        for path in sorted(replay.iterdir())
        if path.is_file() and path.name != "replay-report.json"
    }
    report = {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "pipeline": PIPELINE,
        "status": "AUTHOR_RECOVERY_REPLAY_PASSED",
        "claim_status": NONCLAIM,
        "mathematical_claim": "NONE",
        "aggregate_claim": "NONE",
        "claim_boundary": (
            "This author-side package verifies only the exact case-0111 CNF "
            "against a fresh LRAT replay. It does not certify any other leaf, "
            "the 16-leaf aggregate, the (12,4) slice, or the conjecture. "
            "Separate hostile review is required before promoting even the "
            "case-0111 leaf to a certified-finite claim."
        ),
        "case_id": CASE_ID,
        "cube_variables": list(CUBE_VARIABLES),
        "cube_literals": list(CUBE_LITERALS),
        "verifier": _artifact(package / "verify_recovery.py"),
        "source_inventory": source_inventory,
        "independent_case_reconstruction": reconstructed,
        "raw_bdrat_stats": raw_stats,
        "normalized_bdrat_stats": normalized_stats,
        "normalized_proof": normalized_record,
        "converted_lrat": lrat_record,
        "required_checks": {
            "source_hashes_and_sizes": "PASS",
            "leaf_reconstruction_from_parent_and_cube": "PASS",
            "retained_leaf_byte_identity": "PASS",
            "complete_raw_bdrat_parse": "PASS",
            "unique_final_empty_raw_record": "PASS",
            "preserved_raw_forward_exit_80_reproduced": "PASS",
            "strict_frozen_normalization": "PASS",
            "addition_only_unique_final_empty_normalized_stream": "PASS",
            "warning_fatal_forward_i_f_W_U": "PASS",
            "warning_fatal_backward_i_W_U_L": "PASS",
            "fresh_lrat_check": "PASS",
            "cadical_invocations": 0,
        },
        "artifacts": artifacts,
        "finished_unix_ns": time.time_ns(),
    }
    _write_json_exclusive(replay / "replay-report.json", report)
    return report


def _prepare_explicit_replay(path: Path) -> Path:
    supplied = path.absolute()
    _require(not supplied.is_symlink(), "replay directory path is a symlink")
    _require(
        not supplied.exists(),
        "replay directory already exists; refusing to overwrite or reuse it",
    )
    parent = supplied.parent
    _require(
        parent.is_dir() and not parent.is_symlink(),
        "replay parent is absent, non-directory, or symlink",
    )
    supplied.mkdir(mode=0o700)
    return supplied.resolve(strict=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct and replay the preserved order-12 k=4 case 0111 "
            "proof without invoking a SAT solver."
        )
    )
    parser.add_argument(
        "--replay-dir",
        type=Path,
        help="create this new directory and retain all fresh replay artifacts",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="retain an automatically named temporary replay directory",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.replay_dir is not None and arguments.keep_temp:
        print(
            "REJECTED: --replay-dir and --keep-temp are mutually exclusive",
            file=sys.stderr,
        )
        return 2
    script_supplied = Path(__file__).absolute()
    if script_supplied.is_symlink():
        print("REJECTED: verifier script path is a symlink", file=sys.stderr)
        return 2
    package = script_supplied.parent.resolve(strict=True)
    try:
        _regular_single_link(script_supplied, "verifier script")
        stored = _validate_stored_author_replay(package)
        if arguments.replay_dir is not None:
            replay = _prepare_explicit_replay(arguments.replay_dir)
            report = _replay(package, replay)
            retained_replay = str(replay)
        elif arguments.keep_temp:
            replay = Path(
                tempfile.mkdtemp(prefix="gamma-theta-case0111-replay-")
            ).resolve(strict=True)
            report = _replay(package, replay)
            retained_replay = str(replay)
        else:
            with tempfile.TemporaryDirectory(
                prefix="gamma-theta-case0111-replay-"
            ) as temporary:
                replay = Path(temporary).resolve(strict=True)
                report = _replay(package, replay)
                retained_replay = None
        summary = {
            "schema": SCHEMA,
            "status": "PASS_AUTHOR_SIDE_PENDING_HOSTILE_REVIEW",
            "claim_status": NONCLAIM,
            "mathematical_claim": "NONE",
            "case_id": CASE_ID,
            "fresh_replay_report_sha256": _sha256_file(
                replay / "replay-report.json"
            )
            if retained_replay is not None
            else hashlib.sha256(_canonical_json_bytes(report)).hexdigest(),
            "stored_author_replay_checked": stored is not None,
            "retained_replay_directory": retained_replay,
        }
        print(json.dumps(summary, allow_nan=False, sort_keys=True))
        return 0
    except (AuditError, OSError, subprocess.SubprocessError) as error:
        print(f"REJECTED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
