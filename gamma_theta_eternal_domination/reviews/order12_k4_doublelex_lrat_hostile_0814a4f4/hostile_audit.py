#!/usr/bin/env python3
"""Independent hostile audit of the frozen DoubleLex LRAT package.

The script imports none of the author's generator, normalizer, producer, or
orchestrator code.  It is split into resumable phases because the forward and
backward proof checks take several minutes on the campaign laptop.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
from itertools import combinations, product
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import stat
import subprocess
import sys
import time
from typing import Any, Sequence


SCRIPT = Path(__file__).absolute()
REVIEW = SCRIPT.parent
ROOT = REVIEW.parents[1]
PACKAGE = ROOT / "certificates/order12_k4_doublelex_seed0_lrat"
REPLAY = REVIEW / "private-replay"
LOGS = REPLAY / "logs"
RESOURCES = REPLAY / "resources"
PROOF = REPLAY / "proof"
RETAINED = REPLAY / "retained"
SOURCE = REPLAY / "source"

VARIABLE_COUNT = 18_381
CLAUSE_COUNT = 115_507
LITERAL_COUNT = 1_190_774
WALL_LIMIT_SECONDS = 3_600
FILE_LIMIT_BYTES = 2 << 30
MINIMUM_FREE_DISK_BYTES = 8 << 30
MAX_VARINT_BYTES = 10

EXPECTED_PACKAGE_FILE_COUNT = 35
EXPECTED_PACKAGE_SIZE = 260_029_326
EXPECTED_PACKAGE_INVENTORY_SHA256 = (
    "0814a4f435f9a50784eb12dcd99116f5b4529587a78723bff328dcec86ec7113"
)

FORMULA_SHA256 = (
    "14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7"
)
FORMULA_SIZE = 4_030_657
PARENT_SHA256 = (
    "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac"
)
PARENT_SIZE = 3_992_947
SUFFIX_SHA256 = (
    "328eeeaadc688bbce63fd3ffd952f86a4eb9209e6d0abf5542979fe54ebdbbe0"
)
RAW_SHA256 = (
    "ed3975c5f0cfbe9475c607e440c0ddc012722d0fe68b797e693149fd6f7d5c51"
)
RAW_SIZE = 32_987_136
NORMALIZED_SHA256 = (
    "2741335a5ed9af769f0db4bd0c03a70e414d0568681d5b8261a5667ed30b6686"
)
NORMALIZED_SIZE = 15_783_377
LRAT_SHA256 = (
    "0e04eb639a3f7f7d335126d56040abb4ef11e8548770262c316a608390659263"
)
LRAT_SIZE = 228_381_671
DRAT_TRIM_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
LRAT_CHECK_SHA256 = (
    "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2"
)
PYTHON_SHA256 = (
    "b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf"
)

EXPECTED_EXTERNAL_HASHES = {
    "instances/order12_k4_connected_doublelex/instance.cnf": FORMULA_SHA256,
    "instances/order12_k4_connected_doublelex/manifest.json": (
        "4ca0b1d43c145acf35f7545b7a85e5d0aafa62e7279c120212455985312cba96"
    ),
    "instances/order12_k4_connected_parent/instance.cnf": PARENT_SHA256,
    "math/lemmas/order12_k4_doublelex.md": (
        "d5be9b6373d7aa7c49dec32c18c6202698b35fe05a1f58b2b97dcc98d9114a76"
    ),
    "src/search/k4_doublelex.py": (
        "e5aeb23eb3938631c62a29df45a880839fa9c8384121e0ec310d9740936baba1"
    ),
    "tests/test_k4_doublelex.py": (
        "36282f747f971cf5a57c90e1b645fbe2cd76ab51c3413b7b2268547144322469"
    ),
    "reviews/order12_k4_doublelex_hostile_review.md": (
        "4cf3c5012a8b0ecfdcbad82c0fd2c283c2aebbd3396eaba9b232902956f86d8f"
    ),
    "reviews/order12_k4_doublelex_hostile_probe.py": (
        "51c32b44b2e54ad05ecd80f08aaf20e8e60153b82f2de2001164782e5ea87c6f"
    ),
    "reviews/order12_k4_doublelex_hostile_probe.json": (
        "fc70fe871a03ccc23ab5cbbc244866537f63c600c1881c17a082b9b57186ed86"
    ),
    "results/order12_k4_doublelex_seed0/proof.raw.bdrat": RAW_SHA256,
    "results/order12_k4_doublelex_seed0/solver.result": (
        "bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162"
    ),
    "src/search/k4_production/normalize_bdrat.py": (
        "07229fce9293a05fed3fa6ef3f96415eb48ea4b0cdd8e9a329620017d2bced99"
    ),
    "src/synthesis_k3/cegar.py": (
        "411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c"
    ),
    "tools/drat_trim_2023_05_22/drat-trim": DRAT_TRIM_SHA256,
    "tools/drat_trim_2023_05_22/lrat-check": LRAT_CHECK_SHA256,
    "tools/drat_trim_2023_05_22.tar.gz": (
        "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108"
    ),
}

CERTIFICATE_SHA256 = (
    "a21bd3db71fb271965859237d7665c5d0c38d32d061fdf3eda285c014e366991"
)
MANIFEST_SHA256 = (
    "846a646ba951569f50a76b562fdc8ec005dcf0f06ff57e48b4e3d4d330fbd607"
)
PRODUCER_SHA256 = (
    "3cf037c1cefd9dc7607eb97a1e0ec7f9b32618beb22825abd60ab6093b58a396"
)


class AuditError(RuntimeError):
    """A fail-closed hostile-audit rejection."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: object, *, pretty: bool = True) -> bytes:
    if pretty:
        encoded = json.dumps(
            value, allow_nan=False, indent=2, sort_keys=True
        )
    else:
        encoded = json.dumps(
            value,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    return (encoded + "\n").encode("utf-8")


def _reject_constant(value: str) -> None:
    raise AuditError(f"non-finite JSON constant {value}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_bytes(),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditError(f"malformed JSON {path}: {error}") from error


def regular_single_link(path: Path, role: str) -> os.stat_result:
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise AuditError(f"{role} is absent: {path}") from error
    require(
        stat.S_ISREG(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode),
        f"{role} is not a regular non-symlink file",
    )
    require(metadata.st_nlink == 1, f"{role} does not have one hard link")
    return metadata


def binding(path: Path, role: str) -> dict[str, object]:
    metadata = regular_single_link(path, role)
    return {
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "size_bytes": metadata.st_size,
    }


def check_file(
    path: Path,
    expected_sha256: str,
    expected_size: int | None,
    role: str,
) -> dict[str, object]:
    record = binding(path, role)
    require(
        record["sha256"] == expected_sha256,
        f"{role} SHA-256 mismatch",
    )
    if expected_size is not None:
        require(
            record["size_bytes"] == expected_size,
            f"{role} size mismatch",
        )
    return record


def check_record(
    record: object,
    path: Path,
    role: str,
) -> None:
    require(isinstance(record, dict), f"{role} binding is not an object")
    actual = binding(path, role)
    require(
        record.get("sha256") == actual["sha256"]
        and record.get("size_bytes") == actual["size_bytes"]
        and Path(str(record.get("path"))).resolve() == path.resolve(),
        f"{role} binding differs from exact file",
    )


def write_new(path: Path, payload: bytes, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not path.exists() and not path.is_symlink(), f"refuse overwrite {path}")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, mode)
    completed = False
    try:
        with os.fdopen(descriptor, "wb", buffering=0) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        completed = True
    finally:
        if not completed:
            try:
                path.unlink()
            except FileNotFoundError:
                pass


def write_json(path: Path, value: object) -> None:
    write_new(path, canonical_json_bytes(value))


def copy_new(source: Path, destination: Path) -> dict[str, object]:
    regular_single_link(source, f"copy source {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    require(
        not destination.exists() and not destination.is_symlink(),
        f"copy destination already exists: {destination}",
    )
    with source.open("rb") as reader, destination.open("xb") as writer:
        shutil.copyfileobj(reader, writer, length=1 << 20)
        writer.flush()
        os.fsync(writer.fileno())
    return binding(destination, f"private copy {destination.name}")


def files_equal(first: Path, second: Path) -> bool:
    if first.stat().st_size != second.stat().st_size:
        return False
    with first.open("rb") as left, second.open("rb") as right:
        while True:
            left_block = left.read(1 << 20)
            right_block = right.read(1 << 20)
            if left_block != right_block:
                return False
            if not left_block:
                return True


def package_snapshot() -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for path in sorted(PACKAGE.rglob("*")):
        if not path.is_file():
            require(not path.is_symlink(), f"package symlink found: {path}")
            continue
        metadata = path.lstat()
        entry = {
            "mode": oct(metadata.st_mode & 0o777),
            "nlink": metadata.st_nlink,
            "path": path.relative_to(PACKAGE).as_posix(),
            "sha256": sha256_file(path),
            "size_bytes": metadata.st_size,
            "symlink": path.is_symlink(),
        }
        entries.append(entry)
    inventory_sha256 = hashlib.sha256(
        canonical_json_bytes(entries, pretty=False)
    ).hexdigest()
    result = {
        "file_count": len(entries),
        "total_size_bytes": sum(
            int(entry["size_bytes"]) for entry in entries
        ),
        "inventory_sha256": inventory_sha256,
        "inventory": entries,
    }
    require(
        result["file_count"] == EXPECTED_PACKAGE_FILE_COUNT
        and result["total_size_bytes"] == EXPECTED_PACKAGE_SIZE
        and inventory_sha256 == EXPECTED_PACKAGE_INVENTORY_SHA256,
        "author package snapshot differs from frozen hostile-review target",
    )
    require(
        all(
            entry["nlink"] == 1 and entry["symlink"] is False
            for entry in entries
        ),
        "author package contains a symlink or multiply linked file",
    )
    return result


def external_bindings() -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for relative, expected in sorted(EXPECTED_EXTERNAL_HASHES.items()):
        path = ROOT / relative
        record = check_file(path, expected, None, f"external source {relative}")
        records[relative] = record
    check_file(
        ROOT / "instances/order12_k4_connected_doublelex/instance.cnf",
        FORMULA_SHA256,
        FORMULA_SIZE,
        "exact DoubleLex formula",
    )
    check_file(
        ROOT / "instances/order12_k4_connected_parent/instance.cnf",
        PARENT_SHA256,
        PARENT_SIZE,
        "exact parent formula",
    )
    check_file(
        ROOT / "results/order12_k4_doublelex_seed0/proof.raw.bdrat",
        RAW_SHA256,
        RAW_SIZE,
        "raw binary DRAT",
    )
    require(
        (ROOT / "results/order12_k4_doublelex_seed0/solver.result").read_bytes()
        == b"s UNSATISFIABLE\n",
        "solver-result provenance bytes differ",
    )
    return records


def parse_dimacs(path: Path) -> dict[str, int]:
    variables: int | None = None
    declared: int | None = None
    clauses = 0
    literals = 0
    maximum = 0
    saw_header = False
    with path.open("rb") as handle:
        for line_number, raw_line in enumerate(handle, 1):
            require(raw_line.endswith(b"\n"), f"DIMACS line {line_number} lacks LF")
            try:
                fields = raw_line.decode("ascii").strip().split()
            except UnicodeDecodeError as error:
                raise AuditError(f"DIMACS line {line_number} not ASCII") from error
            require(fields, f"blank DIMACS line {line_number}")
            if fields[0] == "p":
                require(
                    not saw_header
                    and len(fields) == 4
                    and fields[:2] == ["p", "cnf"],
                    "malformed/repeated DIMACS header",
                )
                variables = int(fields[2])
                declared = int(fields[3])
                saw_header = True
                continue
            require(saw_header and variables is not None, "clause before header")
            try:
                values = tuple(int(field) for field in fields)
            except ValueError as error:
                raise AuditError(f"noninteger DIMACS line {line_number}") from error
            require(
                len(values) >= 2
                and values[-1] == 0
                and 0 not in values[:-1],
                f"bad clause terminator line {line_number}",
            )
            for literal in values[:-1]:
                require(
                    1 <= abs(literal) <= variables,
                    f"out-of-range literal line {line_number}",
                )
                maximum = max(maximum, abs(literal))
            clauses += 1
            literals += len(values) - 1
    require(
        saw_header
        and variables == VARIABLE_COUNT
        and declared == CLAUSE_COUNT
        and clauses == CLAUSE_COUNT
        and literals == LITERAL_COUNT
        and maximum == VARIABLE_COUNT,
        "DoubleLex DIMACS census mismatch",
    )
    return {
        "variable_count": variables,
        "clause_count": clauses,
        "literal_count": literals,
        "maximum_variable_observed": maximum,
    }


def edge(first: int, second: int) -> int:
    if first > second:
        first, second = second, first
    require(0 <= first < second < 12, "invalid independent edge index")
    return 1 + first * (23 - first) // 2 + second - first - 1


def independent_suffix() -> bytes:
    outer = tuple(range(4, 12))
    clauses: list[tuple[int, ...]] = []
    for left, right in ((0, 1), (1, 2), (2, 3)):
        for first_difference in range(8):
            for prefix in product((0, 1), repeat=first_difference):
                clause: list[int] = []
                for coordinate, bit in enumerate(prefix):
                    left_var = edge(left, outer[coordinate])
                    right_var = edge(right, outer[coordinate])
                    clause.extend(
                        (left_var, right_var)
                        if bit == 0
                        else (-left_var, -right_var)
                    )
                clause.extend(
                    (
                        -edge(left, outer[first_difference]),
                        edge(right, outer[first_difference]),
                    )
                )
                clauses.append(tuple(clause))
    require(
        len(clauses) == 765
        and sum(len(clause) for clause in clauses) == 10_758,
        "independent DoubleLex suffix census mismatch",
    )
    payload = b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in clauses
    )
    require(
        len(payload) == 37_710
        and hashlib.sha256(payload).hexdigest() == SUFFIX_SHA256,
        "independent DoubleLex suffix bytes mismatch",
    )
    return payload


def reconstruct_formula() -> bytes:
    parent = (
        ROOT / "instances/order12_k4_connected_parent/instance.cnf"
    ).read_bytes()
    require(
        len(parent) == PARENT_SIZE
        and hashlib.sha256(parent).hexdigest() == PARENT_SHA256,
        "parent bytes differ",
    )
    header, body = parent.split(b"\n", 1)
    require(header == b"p cnf 18381 114742", "parent header differs")
    output = b"p cnf 18381 115507\n" + body + independent_suffix()
    require(
        len(output) == FORMULA_SIZE
        and hashlib.sha256(output).hexdigest() == FORMULA_SHA256,
        "independently reconstructed formula differs",
    )
    require(
        output
        == (
            ROOT / "instances/order12_k4_connected_doublelex/instance.cnf"
        ).read_bytes(),
        "source formula is not byte-identical to independent reconstruction",
    )
    return output


def encode_unsigned(value: int) -> bytes:
    encoded = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            encoded.append(byte | 0x80)
        else:
            encoded.append(byte)
            return bytes(encoded)


def scan_binary_drat(path: Path) -> dict[str, object]:
    regular_single_link(path, f"binary proof {path.name}")
    payload = path.read_bytes()
    cursor = 0
    records = additions = deletions = literals = addition_literals = 0
    maximum = 0
    empty_additions: list[int] = []
    post_empty_deletions = 0
    addition_after_empty = False
    while cursor < len(payload):
        prefix = payload[cursor]
        cursor += 1
        records += 1
        require(prefix in (ord("a"), ord("d")), f"bad prefix record {records}")
        is_addition = prefix == ord("a")
        additions += int(is_addition)
        deletions += int(not is_addition)
        clause_length = 0
        while True:
            start = cursor
            value = 0
            shift = 0
            while True:
                require(cursor < len(payload), f"truncated varint record {records}")
                byte = payload[cursor]
                cursor += 1
                require(
                    cursor - start <= MAX_VARINT_BYTES,
                    f"overlong varint record {records}",
                )
                value |= (byte & 0x7F) << shift
                if byte < 0x80:
                    break
                shift += 7
            require(
                payload[start:cursor] == encode_unsigned(value),
                f"noncanonical varint record {records}",
            )
            require(value <= 2 * VARIABLE_COUNT + 1, "encoded literal out of bound")
            if value == 0:
                break
            require(value != 1, f"negative zero record {records}")
            variable = value >> 1
            require(1 <= variable <= VARIABLE_COUNT, "variable out of bound")
            maximum = max(maximum, variable)
            clause_length += 1
            literals += 1
            addition_literals += int(is_addition)
        if is_addition and clause_length == 0:
            empty_additions.append(records)
        if not is_addition:
            require(clause_length > 0, f"empty deletion record {records}")
            if empty_additions:
                post_empty_deletions += 1
        elif empty_additions and empty_additions[-1] != records:
            addition_after_empty = True
    return {
        "size_bytes": len(payload),
        "records": records,
        "additions": additions,
        "deletions": deletions,
        "literals": literals,
        "addition_literals": addition_literals,
        "maximum_variable": maximum,
        "empty_addition_records": empty_additions,
        "post_empty_deletions": post_empty_deletions,
        "addition_after_empty": addition_after_empty,
    }


def validate_resource_record(path: Path, expected_phase: str) -> dict[str, Any]:
    record = load_json(path)
    require(
        isinstance(record, dict)
        and set(record)
        == {"schema", "schema_version", "phase", "passed", "child"}
        and record["schema"] == "gamma-theta-doublelex-proof-child-resource-v1"
        and record["schema_version"] == 1
        and record["phase"] == expected_phase,
        f"resource schema mismatch for {expected_phase}",
    )
    child = record["child"]
    expected_child_keys = {
        "available_memory_before_bytes",
        "command",
        "command_sha256",
        "executable_sha256_after",
        "executable_sha256_before",
        "exit_code",
        "file_limit_mib",
        "finished_unix_ns",
        "maximum_resident_set_size_mib",
        "maximum_resident_set_size_raw",
        "maximum_resident_set_size_raw_unit",
        "memory_limit_exceeded",
        "memory_limit_mib",
        "peak_polled_resident_set_size_mib",
        "started_unix_ns",
        "stderr_path",
        "stderr_sha256",
        "stdout_path",
        "stdout_sha256",
        "system_cpu_seconds",
        "termination_signal",
        "timed_out",
        "user_cpu_seconds",
        "wall_limit_seconds",
        "wall_seconds",
    }
    require(
        isinstance(child, dict) and set(child) == expected_child_keys,
        f"child resource keys mismatch for {expected_phase}",
    )
    command = child["command"]
    require(
        isinstance(command, list)
        and all(isinstance(item, str) for item in command),
        f"command malformed for {expected_phase}",
    )
    command_hash = hashlib.sha256(
        canonical_json_bytes(command, pretty=False)
    ).hexdigest()
    require(
        child["command_sha256"] == command_hash,
        f"command digest mismatch for {expected_phase}",
    )
    return record


def audit_author_package() -> dict[str, object]:
    snapshot = package_snapshot()
    sources = external_bindings()
    certificate_path = PACKAGE / "certificate.json"
    manifest_path = PACKAGE / "artifact-manifest.json"
    producer_path = PACKAGE / "repro/produce_certificate.py"
    check_file(certificate_path, CERTIFICATE_SHA256, 15_723, "certificate")
    check_file(manifest_path, MANIFEST_SHA256, 16_369, "artifact manifest")
    check_file(producer_path, PRODUCER_SHA256, 22_586, "producer")
    certificate = load_json(certificate_path)
    manifest = load_json(manifest_path)
    certificate_keys = {
        "accepted_doublelex_hostile_evidence",
        "accepted_doublelex_hostile_probe",
        "accepted_doublelex_hostile_review",
        "artifact_manifest",
        "bounded_child_orchestrator_source",
        "checker_source_archive",
        "claim_boundary",
        "converted_lrat",
        "dimacs_census",
        "doublelex_theorem",
        "drat_trim_binary",
        "formula",
        "formula_manifest",
        "generator_source",
        "generator_tests",
        "git_head_observed",
        "lrat_check_binary",
        "normalization_report",
        "normalized_binary_rup",
        "normalizer_source",
        "phase_resources",
        "producer",
        "proof_pipeline",
        "raw_binary_drat",
        "raw_solver_result",
        "schema",
        "schema_version",
        "status",
    }
    require(
        isinstance(certificate, dict)
        and set(certificate) == certificate_keys
        and certificate["schema"]
        == "gamma-theta-order12-k4-doublelex-lrat-certificate-v1"
        and certificate["schema_version"] == 1
        and certificate["status"]
        == "UNSAT_LRAT_VERIFIED_PENDING_INDEPENDENT_HOSTILE_REVIEW",
        "certificate schema/status mismatch",
    )
    require(
        certificate["claim_boundary"]
        == (
            "This source-bound package verifies only that the exact "
            "DoubleLex-strengthened CNF is UNSAT. The accepted DoubleLex "
            "theorem is needed to transfer this to the exact anchored parent; "
            "no universal conjecture-resolution claim is made."
        ),
        "certificate claim boundary differs",
    )
    require(
        certificate["proof_pipeline"]
        == (
            "strict-full-binary-parse-additions-only-normalization;"
            "normalized-forward-rup-warning-fatal;"
            "backward-rup-lrat-warning-fatal;"
            "fresh-independent-lrat-check"
        ),
        "certificate pipeline label differs",
    )
    manifest_keys = {
        "claim_boundary",
        "dimacs_census",
        "frozen_inputs_before_and_after",
        "git_head_observed",
        "limits",
        "normalization",
        "outputs",
        "preserved_failed_attempts",
        "producer",
        "schema",
        "schema_version",
        "status",
    }
    require(
        isinstance(manifest, dict)
        and set(manifest) == manifest_keys
        and manifest["schema"]
        == "gamma-theta-order12-k4-doublelex-artifact-manifest-v1"
        and manifest["schema_version"] == 1
        and manifest["status"]
        == "PIPELINE_PASSED_PENDING_INDEPENDENT_HOSTILE_REVIEW"
        and manifest["claim_boundary"]
        == (
            "Exact DoubleLex CNF proof-chain evidence only; no campaign claim "
            "until independent hostile acceptance"
        ),
        "artifact manifest schema/status/claim mismatch",
    )
    source_field_paths = {
        "formula": "instances/order12_k4_connected_doublelex/instance.cnf",
        "formula_manifest": "instances/order12_k4_connected_doublelex/manifest.json",
        "doublelex_theorem": "math/lemmas/order12_k4_doublelex.md",
        "generator_source": "src/search/k4_doublelex.py",
        "generator_tests": "tests/test_k4_doublelex.py",
        "accepted_doublelex_hostile_review": "reviews/order12_k4_doublelex_hostile_review.md",
        "accepted_doublelex_hostile_probe": "reviews/order12_k4_doublelex_hostile_probe.py",
        "accepted_doublelex_hostile_evidence": "reviews/order12_k4_doublelex_hostile_probe.json",
        "raw_solver_result": "results/order12_k4_doublelex_seed0/solver.result",
        "raw_binary_drat": "results/order12_k4_doublelex_seed0/proof.raw.bdrat",
        "normalizer_source": "src/search/k4_production/normalize_bdrat.py",
        "bounded_child_orchestrator_source": "src/synthesis_k3/cegar.py",
        "drat_trim_binary": "tools/drat_trim_2023_05_22/drat-trim",
        "lrat_check_binary": "tools/drat_trim_2023_05_22/lrat-check",
        "checker_source_archive": "tools/drat_trim_2023_05_22.tar.gz",
    }
    for field, relative in source_field_paths.items():
        check_record(certificate[field], ROOT / relative, f"certificate {field}")
        require(
            manifest["frozen_inputs_before_and_after"][relative]
            == certificate[field],
            f"manifest/certificate source binding differs for {field}",
        )
    check_record(certificate["artifact_manifest"], manifest_path, "manifest binding")
    check_record(certificate["producer"], producer_path, "producer binding")
    require(certificate["producer"] == manifest["producer"], "producer records differ")

    output_paths = {
        "normalization_report": PACKAGE / "proof/normalization-report.json",
        "normalized_binary_rup": PACKAGE / "proof/proof.normalized.rup.bdrat",
        "converted_lrat": PACKAGE / "proof/proof.converted.lrat",
        "normalizer_stdout": PACKAGE / "logs/normalizer.stdout",
        "normalizer_stderr": PACKAGE / "logs/normalizer.stderr",
        "normalizer_resource": PACKAGE / "resources/resource-normalizer.json",
        "normalized-forward-rup_stdout": PACKAGE
        / "logs/normalized-forward-rup.stdout",
        "normalized-forward-rup_stderr": PACKAGE
        / "logs/normalized-forward-rup.stderr",
        "normalized-forward-rup_resource": PACKAGE
        / "resources/resource-normalized-forward-rup.json",
        "backward-lrat-conversion-rup_stdout": PACKAGE
        / "logs/backward-lrat-conversion-rup.stdout",
        "backward-lrat-conversion-rup_stderr": PACKAGE
        / "logs/backward-lrat-conversion-rup.stderr",
        "backward-lrat-conversion-rup_resource": PACKAGE
        / "resources/resource-backward-lrat-conversion-rup.json",
        "lrat-check_stdout": PACKAGE / "logs/lrat-check.stdout",
        "lrat-check_stderr": PACKAGE / "logs/lrat-check.stderr",
        "lrat-check_resource": PACKAGE / "resources/resource-lrat-check.json",
    }
    require(
        set(manifest["outputs"]) == set(output_paths),
        "manifest decisive output set differs",
    )
    for name, path in output_paths.items():
        check_record(manifest["outputs"][name], path, f"decisive output {name}")
    require(
        certificate["normalization_report"]
        == manifest["outputs"]["normalization_report"]
        and certificate["normalized_binary_rup"]
        == manifest["outputs"]["normalized_binary_rup"]
        and certificate["converted_lrat"] == manifest["outputs"]["converted_lrat"],
        "certificate decisive proof bindings differ from manifest",
    )
    check_file(
        output_paths["normalized_binary_rup"],
        NORMALIZED_SHA256,
        NORMALIZED_SIZE,
        "retained normalized proof",
    )
    check_file(
        output_paths["converted_lrat"],
        LRAT_SHA256,
        LRAT_SIZE,
        "retained LRAT proof",
    )

    normalization = load_json(output_paths["normalization_report"])
    require(manifest["normalization"] == normalization, "normalization records differ")
    require(
        normalization
        == {
            "claim_status": "TRANSFORMATION_ONLY_NO_PROOF_CLAIM",
            "empty_addition_record_index": 1_378_975,
            "input": {
                "path": str(
                    (
                        ROOT
                        / "results/order12_k4_doublelex_seed0/proof.raw.bdrat"
                    ).resolve()
                ),
                "sha256": RAW_SHA256,
                "size_bytes": RAW_SIZE,
            },
            "max_variable_allowed": VARIABLE_COUNT,
            "max_variable_observed": VARIABLE_COUNT,
            "output": {
                "path": str(
                    (
                        PACKAGE / "proof/proof.normalized.rup.bdrat"
                    ).resolve()
                ),
                "sha256": NORMALIZED_SHA256,
                "size_bytes": NORMALIZED_SIZE,
            },
            "policy": "canonical-additions-only-unique-empty-full-stream-v1",
            "record_counts": {
                "additions": 640_854,
                "deletions": 738_121,
                "literals": 22_445_080,
                "post_empty_deletions": 0,
                "total": 1_378_975,
            },
            "schema": "gamma-theta-order12-k4-binary-drat-normalization-v1",
            "schema_version": 1,
        },
        "normalization report differs from exact expected policy/census",
    )
    require(
        certificate["dimacs_census"] == manifest["dimacs_census"],
        "DIMACS records differ",
    )

    resource_paths = {
        "normalizer": PACKAGE / "resources/resource-normalizer.json",
        "normalized_forward_rup": PACKAGE
        / "resources/resource-normalized-forward-rup.json",
        "backward_lrat_conversion_rup": PACKAGE
        / "resources/resource-backward-lrat-conversion-rup.json",
        "lrat_check": PACKAGE / "resources/resource-lrat-check.json",
    }
    expected_commands = {
        "normalizer": [
            str(Path(sys.executable).resolve()),
            str(
                (
                    ROOT / "src/search/k4_production/normalize_bdrat.py"
                ).resolve()
            ),
            "--input",
            str(
                (
                    ROOT / "results/order12_k4_doublelex_seed0/proof.raw.bdrat"
                ).resolve()
            ),
            "--output",
            str((PACKAGE / "proof/proof.normalized.rup.bdrat").resolve()),
            "--report",
            str((PACKAGE / "proof/normalization-report.json").resolve()),
            "--max-variable",
            "18381",
        ],
        "normalized_forward_rup": [
            str(
                (
                    ROOT / "tools/drat_trim_2023_05_22/drat-trim"
                ).resolve()
            ),
            str(
                (
                    ROOT
                    / "instances/order12_k4_connected_doublelex/instance.cnf"
                ).resolve()
            ),
            str((PACKAGE / "proof/proof.normalized.rup.bdrat").resolve()),
            "-i",
            "-f",
            "-W",
            "-U",
            "-t",
            "3600",
        ],
        "backward_lrat_conversion_rup": [
            str(
                (
                    ROOT / "tools/drat_trim_2023_05_22/drat-trim"
                ).resolve()
            ),
            str(
                (
                    ROOT
                    / "instances/order12_k4_connected_doublelex/instance.cnf"
                ).resolve()
            ),
            str((PACKAGE / "proof/proof.normalized.rup.bdrat").resolve()),
            "-i",
            "-W",
            "-U",
            "-L",
            str((PACKAGE / "proof/proof.converted.lrat").resolve()),
            "-t",
            "3600",
        ],
        "lrat_check": [
            str(
                (
                    ROOT / "tools/drat_trim_2023_05_22/lrat-check"
                ).resolve()
            ),
            str(
                (
                    ROOT
                    / "instances/order12_k4_connected_doublelex/instance.cnf"
                ).resolve()
            ),
            str((PACKAGE / "proof/proof.converted.lrat").resolve()),
        ],
    }
    markers = {
        "normalizer": b"s NORMALIZED",
        "normalized_forward_rup": b"s VERIFIED",
        "backward_lrat_conversion_rup": b"s VERIFIED",
        "lrat_check": b"c VERIFIED",
    }
    for name, path in resource_paths.items():
        record = validate_resource_record(
            path,
            {
                "normalizer": "normalizer",
                "normalized_forward_rup": "normalized-forward-rup",
                "backward_lrat_conversion_rup": "backward-lrat-conversion-rup",
                "lrat_check": "lrat-check",
            }[name],
        )
        require(certificate["phase_resources"][name] == record, "embedded resource differs")
        child = record["child"]
        require(
            record["passed"] is True
            and child["command"] == expected_commands[name]
            and child["exit_code"] == 0
            and child["termination_signal"] is None
            and child["timed_out"] is False
            and child["memory_limit_exceeded"] is False
            and child["wall_limit_seconds"] == 3600
            and child["memory_limit_mib"] == 2048
            and child["file_limit_mib"] == 2048,
            f"decisive resource failure/options mismatch for {name}",
        )
        executable = Path(child["command"][0])
        expected_executable = (
            PYTHON_SHA256 if name == "normalizer" else
            LRAT_CHECK_SHA256 if name == "lrat_check" else
            DRAT_TRIM_SHA256
        )
        require(
            child["executable_sha256_before"]
            == child["executable_sha256_after"]
            == expected_executable
            == sha256_file(executable),
            f"decisive executable identity mismatch for {name}",
        )
        stdout_path = Path(child["stdout_path"])
        stderr_path = Path(child["stderr_path"])
        stdout = stdout_path.read_bytes().replace(b"\r", b"")
        require(
            hashlib.sha256(stdout_path.read_bytes()).hexdigest()
            == child["stdout_sha256"]
            and hashlib.sha256(stderr_path.read_bytes()).hexdigest()
            == child["stderr_sha256"]
            and stderr_path.stat().st_size == 0
            and markers[name] in stdout
            and b"warning" not in stdout.lower()
            and b"error" not in stdout.lower(),
            f"decisive checker log mismatch for {name}",
        )
        if name in {"normalized_forward_rup", "backward_lrat_conversion_rup"}:
            require(b"0 RAT lemmas" in stdout, f"{name} is not RUP-only")
        require(
            all("cadical" not in token.lower() for token in child["command"]),
            "SAT solver appears in decisive proof command",
        )

    failed_files = {
        path.relative_to(PACKAGE).as_posix(): path
        for path in sorted(PACKAGE.glob("failed-attempt-*/*"))
        if path.is_file()
    }
    failed_files = {
        path.relative_to(PACKAGE).as_posix(): path
        for directory in sorted(PACKAGE.glob("failed-attempt-*"))
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }
    require(
        set(manifest["preserved_failed_attempts"]) == set(failed_files),
        "preserved failed-attempt inventory differs",
    )
    for relative, path in failed_files.items():
        check_record(
            manifest["preserved_failed_attempts"][relative],
            path,
            f"failed-attempt artifact {relative}",
        )
    failed_raw = load_json(
        PACKAGE
        / "failed-attempt-000001/resources/resource-raw-forward.json"
    )
    require(
        failed_raw["passed"] is False
        and failed_raw["phase"] == "raw-forward"
        and failed_raw["child"]["exit_code"] == 80
        and failed_raw["child"]["timed_out"] is False
        and b"VERIFIED"
        not in (
            PACKAGE
            / "failed-attempt-000001/logs/raw-forward.stdout"
        ).read_bytes()
        and "raw_forward" not in certificate["phase_resources"]
        and all(
            "failed-attempt" not in str(record["path"])
            for record in manifest["outputs"].values()
        ),
        "raw-forward exit 80 leaked into the decisive chain",
    )
    require(
        manifest["limits"]
        == {
            "file_mib_per_child": 2048,
            "memory_mib_per_child": 2048,
            "minimum_free_disk_bytes": 8_589_934_592,
            "wall_seconds_per_child": 3600,
        },
        "resource limit manifest differs",
    )
    return {
        "package_snapshot": snapshot,
        "external_bindings": sources,
        "certificate": binding(certificate_path, "certificate"),
        "artifact_manifest": binding(manifest_path, "artifact manifest"),
        "formula_census": certificate["dimacs_census"],
        "failed_attempt_separation": "PASS_RAW_FORWARD_EXIT80_NONDECISIVE",
        "claim_boundary": certificate["claim_boundary"],
    }


class HeavyLock:
    def __init__(self) -> None:
        root_digest = hashlib.sha256(
            str(ROOT.resolve()).encode("utf-8")
        ).hexdigest()[:20]
        temporary = Path(
            os.environ.get("TMPDIR", "/tmp")
        ).resolve()
        self.path = temporary / (
            f"gamma-theta-k3-heavy-child-{root_digest}.lock"
        )
        self.descriptor: int | None = None

    def __enter__(self) -> "HeavyLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_CREAT | os.O_RDWR
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(self.path, flags, 0o600)
        metadata = os.fstat(descriptor)
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "heavy-child lock malformed",
        )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(descriptor)
            raise AuditError("another campaign heavy child is active") from error
        self.descriptor = descriptor
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        require(self.descriptor is not None, "heavy lock not acquired")
        fcntl.flock(self.descriptor, fcntl.LOCK_UN)
        os.close(self.descriptor)
        self.descriptor = None


def run_child(
    phase: str,
    command: Sequence[str],
    *,
    expected_exit: int = 0,
    environment: dict[str, str] | None = None,
) -> dict[str, object]:
    LOGS.mkdir(parents=True, exist_ok=True)
    RESOURCES.mkdir(parents=True, exist_ok=True)
    stdout_path = LOGS / f"{phase}.stdout"
    stderr_path = LOGS / f"{phase}.stderr"
    resource_path = RESOURCES / f"resource-{phase}.json"
    for path in (stdout_path, stderr_path, resource_path):
        require(not path.exists() and not path.is_symlink(), f"phase output exists: {path}")
    executable = Path(command[0])
    executable_before = sha256_file(executable)
    started_ns = time.time_ns()
    started = time.monotonic()
    print(f"START {phase}", flush=True)
    with HeavyLock(), stdout_path.open("xb", buffering=0) as stdout, stderr_path.open(
        "xb", buffering=0
    ) as stderr:
        process = subprocess.Popen(
            list(command),
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=stdout,
            stderr=stderr,
            env={} if environment is None else environment,
            close_fds=True,
            start_new_session=True,
        )
        deadline = started + WALL_LIMIT_SECONDS
        usage: resource.struct_rusage | None = None
        timed_out = False
        while True:
            waited, wait_status, child_usage = os.wait4(
                process.pid, os.WNOHANG
            )
            if waited == process.pid:
                process.returncode = os.waitstatus_to_exitcode(wait_status)
                usage = child_usage
                break
            if time.monotonic() >= deadline:
                timed_out = True
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                waited, wait_status, child_usage = os.wait4(process.pid, 0)
                require(waited == process.pid, "failed to reap timed-out child")
                process.returncode = os.waitstatus_to_exitcode(wait_status)
                usage = child_usage
                break
            time.sleep(0.1)
    require(usage is not None, "child resource usage missing")
    finished = time.monotonic()
    finished_ns = time.time_ns()
    executable_after = sha256_file(executable)
    require(executable_before == executable_after, "child executable changed")
    maxrss_mib = (
        usage.ru_maxrss / (1 << 20)
        if sys.platform == "darwin"
        else usage.ru_maxrss / 1024
    )
    report = {
        "schema": "gamma-theta-doublelex-hostile-child-resource-v1",
        "schema_version": 1,
        "phase": phase,
        "command": list(command),
        "command_sha256": hashlib.sha256(
            canonical_json_bytes(list(command), pretty=False)
        ).hexdigest(),
        "executable_sha256_before": executable_before,
        "executable_sha256_after": executable_after,
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "started_unix_ns": started_ns,
        "finished_unix_ns": finished_ns,
        "wall_limit_seconds": WALL_LIMIT_SECONDS,
        "wall_seconds": finished - started,
        "user_cpu_seconds": usage.ru_utime,
        "system_cpu_seconds": usage.ru_stime,
        "maximum_resident_set_size_mib": maxrss_mib,
        "maximum_resident_set_size_raw": usage.ru_maxrss,
        "maximum_resident_set_size_raw_unit": (
            "bytes" if sys.platform == "darwin" else "kibibytes"
        ),
        "stdout": binding(stdout_path, f"{phase} stdout"),
        "stderr": binding(stderr_path, f"{phase} stderr"),
    }
    write_json(resource_path, report)
    require(not timed_out, f"{phase} timed out")
    require(
        process.returncode == expected_exit,
        f"{phase} exit {process.returncode}, expected {expected_exit}",
    )
    print(
        f"PASS {phase} wall={report['wall_seconds']:.3f}s "
        f"rss={maxrss_mib:.3f}MiB",
        flush=True,
    )
    return report


def require_checker_pass(
    phase: str,
    marker: bytes,
    *,
    zero_rat: bool,
) -> None:
    stdout = (LOGS / f"{phase}.stdout").read_bytes().replace(b"\r", b"")
    stderr = (LOGS / f"{phase}.stderr").read_bytes()
    require(stderr == b"", f"{phase} emitted stderr")
    require(marker in stdout, f"{phase} lacks verification marker")
    require(
        b"warning" not in stdout.lower()
        and b"error" not in stdout.lower()
        and b"not verified" not in stdout.lower(),
        f"{phase} contains warning/error marker",
    )
    if zero_rat:
        require(b"0 RAT lemmas" in stdout, f"{phase} is not RUP-only")


def mutation_tests() -> dict[str, str]:
    mutation_dir = REPLAY / "mutation-probes"
    mutation_dir.mkdir()
    tests: dict[str, str] = {}

    def expect_rejection(
        label: str,
        source: Path,
        expected_hash: str,
        expected_size: int,
        *,
        truncate: bool,
    ) -> None:
        target = mutation_dir / f"{label}.bin"
        copy_new(source, target)
        if truncate:
            os.truncate(target, expected_size - 1)
        else:
            with target.open("r+b", buffering=0) as handle:
                first = handle.read(1)
                require(len(first) == 1, "mutation target empty")
                handle.seek(0)
                handle.write(bytes((first[0] ^ 1,)))
                handle.flush()
                os.fsync(handle.fileno())
        try:
            check_file(target, expected_hash, expected_size, label)
        except AuditError:
            tests[label] = "PASS_MUTATION_REJECTED"
        else:
            raise AuditError(f"mutation binding unexpectedly accepted: {label}")
        target.unlink()

    def expect_small_truncation_rejection(
        label: str,
        source: Path,
        expected_hash: str,
        expected_size: int,
    ) -> None:
        target = mutation_dir / f"{label}.bin"
        with source.open("rb") as reader:
            write_new(target, reader.read(1 << 20))
        try:
            check_file(target, expected_hash, expected_size, label)
        except AuditError:
            tests[label] = "PASS_TRUNCATION_REJECTED"
        else:
            raise AuditError(f"truncated binding unexpectedly accepted: {label}")
        target.unlink()

    expect_rejection(
        "formula-byte-flip",
        REPLAY / "formula.reconstructed.cnf",
        FORMULA_SHA256,
        FORMULA_SIZE,
        truncate=False,
    )
    expect_rejection(
        "normalized-byte-flip",
        RETAINED / "proof.normalized.rup.bdrat",
        NORMALIZED_SHA256,
        NORMALIZED_SIZE,
        truncate=False,
    )
    expect_small_truncation_rejection(
        "lrat-truncation",
        RETAINED / "proof.converted.lrat",
        LRAT_SHA256,
        LRAT_SIZE,
    )
    expect_rejection(
        "certificate-byte-flip",
        PACKAGE / "certificate.json",
        CERTIFICATE_SHA256,
        15_723,
        truncate=False,
    )
    symlink = mutation_dir / "formula-symlink"
    symlink.symlink_to(REPLAY / "formula.reconstructed.cnf")
    try:
        binding(symlink, "formula symlink")
    except AuditError:
        tests["symlink-binding"] = "PASS_SYMLINK_REJECTED"
    else:
        raise AuditError("symlink binding unexpectedly accepted")
    symlink.unlink()
    hardlink = mutation_dir / "formula-hardlink"
    os.link(REPLAY / "formula.reconstructed.cnf", hardlink)
    try:
        binding(REPLAY / "formula.reconstructed.cnf", "multiply-linked formula")
    except AuditError:
        tests["hardlink-binding"] = "PASS_HARDLINK_REJECTED"
    else:
        raise AuditError("hardlink binding unexpectedly accepted")
    hardlink.unlink()
    mutation_dir.rmdir()
    return tests


def prepare() -> None:
    require(REVIEW.name == "order12_k4_doublelex_lrat_hostile_0814a4f4", "review path differs")
    require(not REPLAY.exists() and not REPLAY.is_symlink(), "private replay exists")
    require(shutil.disk_usage(REVIEW).free >= MINIMUM_FREE_DISK_BYTES, "disk gate failed")
    static = audit_author_package()
    formula_census = parse_dimacs(
        ROOT / "instances/order12_k4_connected_doublelex/instance.cnf"
    )
    reconstructed = reconstruct_formula()
    REPLAY.mkdir(mode=0o700)
    for directory in (LOGS, RESOURCES, PROOF, RETAINED, SOURCE):
        directory.mkdir(mode=0o700)
    write_new(REPLAY / "formula.reconstructed.cnf", reconstructed)
    parse_dimacs(REPLAY / "formula.reconstructed.cnf")
    raw_copy = copy_new(
        ROOT / "results/order12_k4_doublelex_seed0/proof.raw.bdrat",
        SOURCE / "proof.raw.bdrat",
    )
    retained_normalized = copy_new(
        PACKAGE / "proof/proof.normalized.rup.bdrat",
        RETAINED / "proof.normalized.rup.bdrat",
    )
    retained_lrat = copy_new(
        PACKAGE / "proof/proof.converted.lrat",
        RETAINED / "proof.converted.lrat",
    )
    check_file(SOURCE / "proof.raw.bdrat", RAW_SHA256, RAW_SIZE, "private raw proof")
    check_file(
        RETAINED / "proof.normalized.rup.bdrat",
        NORMALIZED_SHA256,
        NORMALIZED_SIZE,
        "private retained normalized proof",
    )
    check_file(
        RETAINED / "proof.converted.lrat",
        LRAT_SHA256,
        LRAT_SIZE,
        "private retained LRAT proof",
    )
    raw_stats = scan_binary_drat(SOURCE / "proof.raw.bdrat")
    normalized_stats = scan_binary_drat(
        RETAINED / "proof.normalized.rup.bdrat"
    )
    require(
        raw_stats["records"] == 1_378_975
        and raw_stats["additions"] == 640_854
        and raw_stats["deletions"] == 738_121
        and raw_stats["literals"] == 22_445_080
        and raw_stats["maximum_variable"] == VARIABLE_COUNT
        and raw_stats["empty_addition_records"] == [1_378_975]
        and raw_stats["post_empty_deletions"] == 0
        and raw_stats["addition_after_empty"] is False,
        "independent raw binary-DRAT census differs",
    )
    require(
        normalized_stats["records"] == 640_854
        and normalized_stats["additions"] == 640_854
        and normalized_stats["deletions"] == 0
        and normalized_stats["maximum_variable"] == VARIABLE_COUNT
        and normalized_stats["empty_addition_records"] == [640_854]
        and normalized_stats["post_empty_deletions"] == 0
        and normalized_stats["addition_after_empty"] is False
        and normalized_stats["literals"] == raw_stats["addition_literals"]
        and normalized_stats["addition_literals"] == raw_stats["addition_literals"],
        "independent normalized binary-DRAT census differs",
    )

    normalizer = ROOT / "src/search/k4_production/normalize_bdrat.py"
    normalizer_output = PROOF / "proof.normalized.rederived.rup.bdrat"
    normalizer_report = PROOF / "normalization-report.rederived.json"
    run_child(
        "normalizer-rederived",
        (
            str(Path(sys.executable).resolve()),
            str(normalizer.resolve()),
            "--input",
            str((SOURCE / "proof.raw.bdrat").resolve()),
            "--output",
            str(normalizer_output.resolve()),
            "--report",
            str(normalizer_report.resolve()),
            "--max-variable",
            str(VARIABLE_COUNT),
        ),
        environment={},
    )
    require_checker_pass(
        "normalizer-rederived", b"s NORMALIZED", zero_rat=False
    )
    rederived = check_file(
        normalizer_output,
        NORMALIZED_SHA256,
        NORMALIZED_SIZE,
        "independently rederived normalized proof",
    )
    require(
        files_equal(
            normalizer_output,
            RETAINED / "proof.normalized.rup.bdrat",
        ),
        "rederived normalized stream is not byte-identical to retained stream",
    )
    rederived_stats = scan_binary_drat(normalizer_output)
    require(rederived_stats == normalized_stats, "rederived normalized census differs")
    rederived_report = load_json(normalizer_report)
    require(
        rederived_report["schema"]
        == "gamma-theta-order12-k4-binary-drat-normalization-v1"
        and rederived_report["policy"]
        == "canonical-additions-only-unique-empty-full-stream-v1"
        and rederived_report["claim_status"]
        == "TRANSFORMATION_ONLY_NO_PROOF_CLAIM"
        and rederived_report["record_counts"]
        == {
            "additions": 640_854,
            "deletions": 738_121,
            "literals": 22_445_080,
            "post_empty_deletions": 0,
            "total": 1_378_975,
        }
        and rederived_report["empty_addition_record_index"] == 1_378_975
        and rederived_report["output"]["sha256"] == NORMALIZED_SHA256,
        "rederived normalization report differs",
    )

    python_env = {"PYTHONPATH": str((ROOT / "src").resolve())}
    run_child(
        "generator-tests",
        (
            str(Path(sys.executable).resolve()),
            str((ROOT / "tests/test_k4_doublelex.py").resolve()),
        ),
        environment=python_env,
    )
    require(
        b"OK" in (LOGS / "generator-tests.stderr").read_bytes(),
        "bound generator tests did not report OK",
    )
    run_child(
        "accepted-doublelex-hostile-probe",
        (
            str(Path(sys.executable).resolve()),
            str(
                (
                    ROOT / "reviews/order12_k4_doublelex_hostile_probe.py"
                ).resolve()
            ),
        ),
        environment=python_env,
    )
    require(
        (LOGS / "accepted-doublelex-hostile-probe.stderr").stat().st_size == 0
        and (
            LOGS / "accepted-doublelex-hostile-probe.stdout"
        ).read_bytes()
        == (
            ROOT / "reviews/order12_k4_doublelex_hostile_probe.json"
        ).read_bytes(),
        "accepted DoubleLex hostile probe did not reproduce byte-for-byte",
    )
    mutations = mutation_tests()
    prepare_evidence = {
        "schema": "gamma-theta-doublelex-hostile-prepare-v1",
        "schema_version": 1,
        "status": "PASS_PREPARED_PENDING_PROOF_REPLAY",
        "claim_status": "NO_HOSTILE_ACCEPTANCE_YET",
        "author_package_audit": static,
        "formula_census": formula_census,
        "formula_reconstruction": binding(
            REPLAY / "formula.reconstructed.cnf", "reconstructed formula"
        ),
        "private_raw_copy": raw_copy,
        "private_retained_normalized_copy": retained_normalized,
        "private_retained_lrat_copy": retained_lrat,
        "raw_binary_drat_stats": raw_stats,
        "normalized_binary_drat_stats": normalized_stats,
        "rederived_normalized": rederived,
        "rederived_normalized_stats": rederived_stats,
        "rederived_normalization_report": binding(
            normalizer_report, "rederived normalization report"
        ),
        "mutation_tests": mutations,
        "generator_tests": "PASS_4_TESTS",
        "accepted_doublelex_hostile_probe": "PASS_BYTE_IDENTICAL_REPLAY",
        "scope": (
            "Exact DoubleLex formula proof package only. Transfer from the "
            "DoubleLex formula to graph exclusion is a separate audit."
        ),
    }
    write_json(REPLAY / "prepare-evidence.json", prepare_evidence)
    print(
        json.dumps(
            {
                "status": prepare_evidence["status"],
                "raw_stats": raw_stats,
                "normalized_stats": normalized_stats,
            },
            sort_keys=True,
        )
    )


def require_prepared() -> None:
    audit_author_package()
    require(
        (REPLAY / "prepare-evidence.json").is_file(),
        "prepare evidence absent",
    )
    check_file(
        REPLAY / "formula.reconstructed.cnf",
        FORMULA_SHA256,
        FORMULA_SIZE,
        "private reconstructed formula",
    )
    check_file(
        PROOF / "proof.normalized.rederived.rup.bdrat",
        NORMALIZED_SHA256,
        NORMALIZED_SIZE,
        "private rederived normalized proof",
    )
    check_file(
        RETAINED / "proof.converted.lrat",
        LRAT_SHA256,
        LRAT_SIZE,
        "private retained LRAT",
    )


def forward() -> None:
    require_prepared()
    drat = ROOT / "tools/drat_trim_2023_05_22/drat-trim"
    run_child(
        "normalized-forward-rup",
        (
            str(drat.resolve()),
            str((REPLAY / "formula.reconstructed.cnf").resolve()),
            str((PROOF / "proof.normalized.rederived.rup.bdrat").resolve()),
            "-i",
            "-f",
            "-W",
            "-U",
            "-t",
            str(WALL_LIMIT_SECONDS),
        ),
    )
    require_checker_pass(
        "normalized-forward-rup", b"s VERIFIED", zero_rat=True
    )


def backward() -> None:
    require_prepared()
    fresh_lrat = PROOF / "proof.fresh-converted.lrat"
    require(not fresh_lrat.exists(), "fresh LRAT output already exists")
    drat = ROOT / "tools/drat_trim_2023_05_22/drat-trim"
    run_child(
        "backward-lrat-conversion-rup",
        (
            str(drat.resolve()),
            str((REPLAY / "formula.reconstructed.cnf").resolve()),
            str((PROOF / "proof.normalized.rederived.rup.bdrat").resolve()),
            "-i",
            "-W",
            "-U",
            "-L",
            str(fresh_lrat.resolve()),
            "-t",
            str(WALL_LIMIT_SECONDS),
        ),
    )
    require_checker_pass(
        "backward-lrat-conversion-rup", b"s VERIFIED", zero_rat=True
    )
    check_file(
        fresh_lrat,
        LRAT_SHA256,
        LRAT_SIZE,
        "fresh independently converted LRAT",
    )
    require(
        files_equal(fresh_lrat, RETAINED / "proof.converted.lrat"),
        "fresh LRAT is not byte-identical to retained LRAT",
    )


def lrat() -> None:
    require_prepared()
    fresh_lrat = PROOF / "proof.fresh-converted.lrat"
    check_file(
        fresh_lrat,
        LRAT_SHA256,
        LRAT_SIZE,
        "fresh independently converted LRAT",
    )
    checker = ROOT / "tools/drat_trim_2023_05_22/lrat-check"
    formula = REPLAY / "formula.reconstructed.cnf"
    for phase, proof in (
        ("lrat-check-retained-private-copy", RETAINED / "proof.converted.lrat"),
        ("lrat-check-fresh-conversion", fresh_lrat),
    ):
        run_child(
            phase,
            (
                str(checker.resolve()),
                str(formula.resolve()),
                str(proof.resolve()),
            ),
        )
        require_checker_pass(phase, b"c VERIFIED", zero_rat=False)


def validate_replay_resource(
    phase: str,
    expected_flags: Sequence[str] | None,
) -> dict[str, Any]:
    path = RESOURCES / f"resource-{phase}.json"
    record = load_json(path)
    require(
        isinstance(record, dict)
        and record["schema"]
        == "gamma-theta-doublelex-hostile-child-resource-v1"
        and record["schema_version"] == 1
        and record["phase"] == phase
        and record["exit_code"] == 0
        and record["timed_out"] is False,
        f"hostile replay resource rejected: {phase}",
    )
    command = record["command"]
    if expected_flags is not None:
        require(
            command[3:] == list(expected_flags),
            f"hostile replay options differ: {phase}",
        )
    require(
        record["executable_sha256_before"]
        == record["executable_sha256_after"]
        and record["stderr"]["size_bytes"] == 0,
        f"hostile child identity/log differs: {phase}",
    )
    return record


def finalize() -> None:
    require_prepared()
    forward_resource = validate_replay_resource(
        "normalized-forward-rup",
        ("-i", "-f", "-W", "-U", "-t", "3600"),
    )
    backward_resource = validate_replay_resource(
        "backward-lrat-conversion-rup",
        (
            "-i",
            "-W",
            "-U",
            "-L",
            str((PROOF / "proof.fresh-converted.lrat").resolve()),
            "-t",
            "3600",
        ),
    )
    retained_lrat_resource = validate_replay_resource(
        "lrat-check-retained-private-copy", None
    )
    fresh_lrat_resource = validate_replay_resource(
        "lrat-check-fresh-conversion", None
    )
    require_checker_pass(
        "normalized-forward-rup", b"s VERIFIED", zero_rat=True
    )
    require_checker_pass(
        "backward-lrat-conversion-rup", b"s VERIFIED", zero_rat=True
    )
    require_checker_pass(
        "lrat-check-retained-private-copy", b"c VERIFIED", zero_rat=False
    )
    require_checker_pass(
        "lrat-check-fresh-conversion", b"c VERIFIED", zero_rat=False
    )
    static_after = audit_author_package()
    proof_bindings = {
        "formula": check_file(
            REPLAY / "formula.reconstructed.cnf",
            FORMULA_SHA256,
            FORMULA_SIZE,
            "final formula",
        ),
        "normalized": check_file(
            PROOF / "proof.normalized.rederived.rup.bdrat",
            NORMALIZED_SHA256,
            NORMALIZED_SIZE,
            "final normalized proof",
        ),
        "retained_lrat_copy": check_file(
            RETAINED / "proof.converted.lrat",
            LRAT_SHA256,
            LRAT_SIZE,
            "final retained LRAT copy",
        ),
        "fresh_lrat": check_file(
            PROOF / "proof.fresh-converted.lrat",
            LRAT_SHA256,
            LRAT_SIZE,
            "final fresh LRAT",
        ),
    }
    evidence = {
        "schema": "gamma-theta-order12-k4-doublelex-lrat-hostile-evidence-v1",
        "schema_version": 1,
        "verdict": "ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY",
        "claim_boundary": (
            "The exact CNF with SHA-256 14284db1... is UNSAT. This review "
            "does not itself transfer that fact to the anchored parent, the "
            "(12,4) graph slice, or the universal gamma-theta conjecture."
        ),
        "transfer_to_graph_exclusion": "OUT_OF_SCOPE_SEPARATE_AUDIT_REQUIRED",
        "author_package_snapshot": static_after["package_snapshot"],
        "author_certificate": static_after["certificate"],
        "author_artifact_manifest": static_after["artifact_manifest"],
        "proof_bindings": proof_bindings,
        "raw_and_normalized_parse": {
            "raw": load_json(REPLAY / "prepare-evidence.json")[
                "raw_binary_drat_stats"
            ],
            "normalized": load_json(REPLAY / "prepare-evidence.json")[
                "normalized_binary_drat_stats"
            ],
        },
        "mutation_tests": load_json(REPLAY / "prepare-evidence.json")[
            "mutation_tests"
        ],
        "failed_attempt_separation": (
            "PASS: raw-forward exit 80 is preserved only as a failed "
            "nonclaim and is absent from every decisive resource/output set"
        ),
        "theorem_source_test_bindings": (
            "PASS hashes; accepted theorem probe and four bound generator "
            "tests replayed. Mathematical transfer remains separately scoped."
        ),
        "independent_replay": {
            "normalized_forward_rup": forward_resource,
            "backward_lrat_conversion_rup": backward_resource,
            "lrat_check_retained_private_copy": retained_lrat_resource,
            "lrat_check_fresh_conversion": fresh_lrat_resource,
        },
        "reviewer_source": binding(SCRIPT, "hostile reviewer source"),
        "finished_unix_ns": time.time_ns(),
    }
    write_json(REVIEW / "hostile-evidence.json", evidence)
    print(
        json.dumps(
            {
                "verdict": evidence["verdict"],
                "formula_sha256": FORMULA_SHA256,
                "normalized_sha256": NORMALIZED_SHA256,
                "lrat_sha256": LRAT_SHA256,
                "evidence_sha256": sha256_file(
                    REVIEW / "hostile-evidence.json"
                ),
            },
            sort_keys=True,
        )
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument(
        "phase",
        choices=("prepare", "forward", "backward", "lrat", "finalize"),
    )
    return result


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        {
            "prepare": prepare,
            "forward": forward,
            "backward": backward,
            "lrat": lrat,
            "finalize": finalize,
        }[arguments.phase]()
        return 0
    except (AuditError, OSError, subprocess.SubprocessError) as error:
        print(f"REJECTED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
