#!/usr/bin/env python3
"""Clean-room post-run verifier for the retained hole5 binary certificate.

This script uses only the Python standard library and pinned standalone
executables.  It does not import or execute ``hole5_binary_production.py``.
It independently checks the formula package, S6 breaker, Git provenance,
binary proofs, recorded artifacts, certificate activation, and a fresh strict
drat-trim replay.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import itertools
import json
import math
import os
import re
import resource
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import BinaryIO, Mapping, Sequence


CAMPAIGN = Path(__file__).resolve().parents[1]
REPOSITORY = CAMPAIGN.parent
RUN = CAMPAIGN / "results/synthesis_k3_hole5_signature_seed0_600s_binary"
DERIVED = CAMPAIGN / "results/synthesis_k3_hole5_signature_package"
SOURCE = CAMPAIGN / "results/synthesis_k3_template_bank_packages/hole5"
PARSER = CAMPAIGN / "reviews/hole5_binary_drat_hostile_probe.py"
PACKAGE_PROBE = CAMPAIGN / "reviews/hole5_signature_package_hostile_probe.py"
PACKAGE_PROBE_LOG = (
    CAMPAIGN / "reviews/hole5_signature_package_hostile_probe_log.json"
)
CADICAL = CAMPAIGN / "tools/cadical_3_0_1/build/cadical"
CADICAL_ARCHIVE = CAMPAIGN / "tools/cadical_3_0_1.tar.gz"
CHECKER = CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim"
CHECKER_ARCHIVE = CAMPAIGN / "tools/drat_trim_2023_05_22.tar.gz"
PYTHON = Path(
    "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/"
    "Python.framework/Versions/3.14/bin/python3.14"
)
COMMIT = "6f3ef0a0970b7214c34018fe32ea1ceeb5764d17"
PRESERVATION_COMMIT = "dff45f4239e4acabc461533a0a213beec18ec56d"
PRESERVATION_COMMIT_TREE = "7e2e9e6c056f4c1460d260f0e266dfa59d510cc4"
PRESERVED_RUN_TREE = "aaef13bba428f8722ad167158360da831a7d1998"
CAMPAIGN_IN_REPOSITORY = "gamma_theta_eternal_domination"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
MAX_VAR = 6886

EXPECTED_RUN_FILES = {
    "certificate.json": (
        4200,
        "f54d7bf8a50f24e3a5084442d84f07548a60401faca8ec18bfd07f24f0e337e8",
        0o644,
    ),
    "checker.stderr": (0, EMPTY_SHA256, 0o600),
    "checker.stdout": (
        482,
        "582074fe80efc122bef5586bc9768e32dfbb3a7bb5758f04b5fe23d0862b6515",
        0o600,
    ),
    "outcome.json": (
        10429,
        "ea2ea36321a786aa40aff1e68587474bbdba5402abc800b1a0816d65b6df8df4",
        0o644,
    ),
    "parser.stderr": (0, EMPTY_SHA256, 0o600),
    "parser.stdout": (
        1531,
        "435ac813fbc0a345816256397bccf9a3f0dc662f3e4a338cc3cc31bd25c19fe1",
        0o600,
    ),
    "proof.additions.bdrat": (
        6337621,
        "c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3",
        0o600,
    ),
    "proof.raw.bdrat": (
        12524020,
        "c17ed1ee2782270ed861462ae7bdd94420a2079edf419a7d778d7096a67d1be4",
        0o600,
    ),
    "run_config.json": (
        19323,
        "6d899e212d2f349b48eefad5037ea007981a331b7e581966165ae861c741221b",
        0o644,
    ),
    "solver.result": (
        16,
        "bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162",
        0o600,
    ),
    "solver.stderr": (0, EMPTY_SHA256, 0o600),
    "solver.stdout": (0, EMPTY_SHA256, 0o600),
}

EXPECTED_PACKAGE_FILES = {
    "derived:instance.cnf": (
        DERIVED / "instance.cnf",
        754323,
        "c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104",
    ),
    "derived:manifest.json": (
        DERIVED / "manifest.json",
        5530,
        "da33bc1708f7d21b92ceedc68710d5433a1aacbe6e32b8a7432bbab45d8cc788",
    ),
    "derived:signature_breaker.json": (
        DERIVED / "signature_breaker.json",
        38296,
        "62ce8f60ecfe74f58bcd113166009637f854d7d663aea2e59395ae224682d18a",
    ),
    "source:coloring_bank.json": (
        SOURCE / "coloring_bank.json",
        335343,
        "b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00",
    ),
    "source:instance.cnf": (
        SOURCE / "instance.cnf",
        742899,
        "76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7",
    ),
    "source:manifest.json": (
        SOURCE / "manifest.json",
        3079,
        "99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402",
    ),
}

EXPECTED_TOOLS = {
    "cadical": (
        CADICAL,
        1571160,
        "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6",
    ),
    "cadical_archive": (
        CADICAL_ARCHIVE,
        890795,
        "2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e",
    ),
    "checker": (
        CHECKER,
        70088,
        "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb",
    ),
    "checker_archive": (
        CHECKER_ARCHIVE,
        7290624,
        "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108",
    ),
    "parser": (
        PARSER,
        33996,
        "02c3c00faf7afb91a3217f5b738d0dacf7699875928162d01ce2df97e600007d",
    ),
    "python": (
        PYTHON,
        52448,
        "b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf",
    ),
    "package_probe": (
        PACKAGE_PROBE,
        34730,
        "ddf75d62dda73779cca880d2c3ec60ee00b91d5f1110ffa84426678a8ef32cc9",
    ),
    "package_probe_log": (
        PACKAGE_PROBE_LOG,
        7319,
        "58edf995b84de703c466e956f47d50443de025fa8b5c5268d781f8962a39d694",
    ),
}

CHILD_KEYS = {
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


def require(condition: object, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json(value: object, *, pretty: bool = True) -> bytes:
    options: dict[str, object] = {
        "allow_nan": False,
        "ensure_ascii": True,
        "sort_keys": True,
    }
    if pretty:
        options["indent"] = 2
    else:
        options["separators"] = (",", ":")
    return (json.dumps(value, **options) + "\n").encode("ascii")


def strict_json_bytes(payload: bytes, role: str) -> object:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AssertionError(f"{role} is not UTF-8") from error

    def pairs(rows: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in rows:
            require(key not in result, f"{role} has duplicate JSON key {key}")
            result[key] = value
        return result

    def reject_constant(value: str) -> object:
        raise AssertionError(f"{role} has nonfinite JSON constant {value}")

    try:
        result = json.loads(
            text,
            object_pairs_hook=pairs,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise AssertionError(f"{role} is malformed JSON") from error
    require(canonical_json(result) == payload, f"{role} is not canonical JSON")
    return result


def strict_json_file(path: Path, role: str) -> object:
    return strict_json_bytes(path.read_bytes(), role)


def assert_no_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current /= component
        try:
            information = os.lstat(current)
        except FileNotFoundError:
            break
        require(
            not stat.S_ISLNK(information.st_mode),
            f"symlinked path component: {current}",
        )


def assert_regular_single_link(path: Path, role: str) -> os.stat_result:
    assert_no_symlink_components(path)
    information = os.lstat(path)
    require(stat.S_ISREG(information.st_mode), f"{role} is not regular")
    require(information.st_nlink == 1, f"{role} has multiple links")
    return information


def artifact_record(path: Path) -> dict[str, object]:
    information = assert_regular_single_link(path, path.name)
    return {
        "size_bytes": information.st_size,
        "sha256": sha256_file(path),
    }


def audit_run_tree() -> dict[str, object]:
    assert_no_symlink_components(RUN)
    information = os.lstat(RUN)
    require(stat.S_ISDIR(information.st_mode), "run is not a directory")
    require(stat.S_IMODE(information.st_mode) == 0o700, "run mode is not 0700")
    names = {entry.name for entry in RUN.iterdir()}
    require(names == set(EXPECTED_RUN_FILES), "run file set differs")
    records: dict[str, object] = {}
    tree_digest = hashlib.sha256()
    total = 0
    for name in sorted(EXPECTED_RUN_FILES):
        expected_size, expected_hash, expected_mode = EXPECTED_RUN_FILES[name]
        path = RUN / name
        file_info = assert_regular_single_link(path, f"run artifact {name}")
        payload = path.read_bytes()
        observed_hash = hashlib.sha256(payload).hexdigest()
        require(file_info.st_size == expected_size, f"{name} size differs")
        require(observed_hash == expected_hash, f"{name} hash differs")
        require(
            stat.S_IMODE(file_info.st_mode) == expected_mode,
            f"{name} mode differs",
        )
        encoded_name = name.encode("utf-8")
        tree_digest.update(len(encoded_name).to_bytes(8, "big"))
        tree_digest.update(encoded_name)
        tree_digest.update(len(payload).to_bytes(8, "big"))
        tree_digest.update(payload)
        total += len(payload)
        records[name] = {
            "mode": f"{expected_mode:04o}",
            "sha256": observed_hash,
            "size_bytes": len(payload),
        }
    return {
        "directory_mode": "0700",
        "file_count": len(records),
        "files": records,
        "length_delimited_tree_sha256": tree_digest.hexdigest(),
        "total_file_bytes": total,
    }


def parse_dimacs(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    require(payload.endswith(b"\n"), f"{path.name} lacks final LF")
    try:
        lines = payload.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise AssertionError(f"{path.name} is not ASCII") from error
    require(lines, f"{path.name} is empty")
    header = lines[0].split()
    require(
        len(header) == 4 and header[:2] == ["p", "cnf"],
        f"{path.name} header differs",
    )
    variable_count = int(header[2])
    declared_clauses = int(header[3])
    clauses: list[tuple[int, ...]] = []
    literal_count = 0
    maximum_variable = 0
    maximum_clause_length = 0
    for index, line in enumerate(lines[1:], 1):
        require(line and not line.startswith("c"), f"unexpected CNF line {index}")
        tokens = line.split()
        require(tokens and tokens[-1] == "0", f"unterminated clause {index}")
        require("0" not in tokens[:-1], f"internal zero in clause {index}")
        clause = tuple(int(token) for token in tokens[:-1])
        require(clause, f"empty input clause {index}")
        literal_set = set(clause)
        require(len(literal_set) == len(clause), f"duplicate literal {index}")
        require(
            not any(-literal in literal_set for literal in clause),
            f"tautological clause {index}",
        )
        for literal in clause:
            require(
                1 <= abs(literal) <= variable_count,
                f"literal range at clause {index}",
            )
        clauses.append(clause)
        literal_count += len(clause)
        maximum_clause_length = max(maximum_clause_length, len(clause))
        maximum_variable = max(
            maximum_variable, max(abs(literal) for literal in clause)
        )
    require(len(clauses) == declared_clauses, "DIMACS clause count differs")
    return {
        "byte_count": len(payload),
        "clause_count": len(clauses),
        "clauses": clauses,
        "literal_count": literal_count,
        "maximum_clause_length": maximum_clause_length,
        "maximum_variable": maximum_variable,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "variable_count": variable_count,
    }


def edge_variables() -> dict[tuple[int, int], int]:
    return {
        pair: index
        for index, pair in enumerate(
            itertools.combinations(range(12), 2), start=1
        )
    }


def expected_breaker_clauses() -> list[tuple[int, ...]]:
    edge = edge_variables()
    clauses: list[tuple[int, ...]] = []
    for left, right in zip(range(6, 11), range(7, 12)):
        for difference in range(6):
            for prefix in itertools.product((0, 1), repeat=difference):
                clause: list[int] = []
                for core, bit in enumerate(prefix):
                    left_edge = edge[tuple(sorted((core, left)))]
                    right_edge = edge[tuple(sorted((core, right)))]
                    if bit == 0:
                        clause.extend((left_edge, right_edge))
                    else:
                        clause.extend((-left_edge, -right_edge))
                left_difference = edge[tuple(sorted((difference, left)))]
                right_difference = edge[tuple(sorted((difference, right)))]
                clause.extend((-left_difference, right_difference))
                clauses.append(tuple(clause))
    return clauses


def audit_breaker_truth(clauses: Sequence[tuple[int, ...]]) -> list[dict[str, int]]:
    edge = edge_variables()
    reports: list[dict[str, int]] = []
    for pair_index, (left, right) in enumerate(
        zip(range(6, 11), range(7, 12))
    ):
        local = clauses[pair_index * 63 : (pair_index + 1) * 63]
        mismatches = 0
        accepted = 0
        for assignment in itertools.product((False, True), repeat=12):
            left_bits = assignment[:6]
            right_bits = assignment[6:]
            values: dict[int, bool] = {}
            for core in range(6):
                values[edge[tuple(sorted((core, left)))]] = left_bits[core]
                values[edge[tuple(sorted((core, right)))]] = right_bits[core]
            clauses_hold = all(
                any(
                    values[abs(literal)] == (literal > 0)
                    for literal in clause
                )
                for clause in local
            )
            expected = left_bits <= right_bits
            mismatches += clauses_hold != expected
            accepted += clauses_hold
        require(mismatches == 0, f"S6 comparator mismatch {left},{right}")
        reports.append(
            {
                "accepted_assignments": accepted,
                "assignments": 4096,
                "left": left,
                "mismatches": mismatches,
                "right": right,
            }
        )
    return reports


def run_package_probe() -> dict[str, object]:
    completed = subprocess.run(
        (str(PYTHON), "-I", "-B", str(PACKAGE_PROBE)),
        cwd=CAMPAIGN,
        env={},
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=60,
        check=False,
    )
    retained = PACKAGE_PROBE_LOG.read_bytes()
    require(completed.returncode == 0, "package probe rerun failed")
    require(completed.stderr == b"", "package probe emitted stderr")
    require(completed.stdout == retained, "package probe rerun differs")
    report = strict_json_bytes(retained, "package hostile log")
    require(isinstance(report, Mapping), "package log shape differs")
    require(report.get("status") == "PASS", "package hostile status differs")
    require(
        report.get("claim_status") == "NO_MATHEMATICAL_CLAIM",
        "package log claim boundary differs",
    )
    reconstruction = report.get("independent_reconstruction")
    require(isinstance(reconstruction, Mapping), "package reconstruction absent")
    require(
        reconstruction.get("derived_cnf_byte_exact") is True
        and reconstruction.get("signature_breaker_json_byte_exact") is True
        and reconstruction.get("source_body_preserved_byte_for_byte") is True,
        "package reconstruction is incomplete",
    )
    return {
        "exit_code": completed.returncode,
        "retained_log_sha256": hashlib.sha256(retained).hexdigest(),
        "stdout_byte_identical": True,
    }


def audit_formula() -> dict[str, object]:
    for role, (path, size, digest) in EXPECTED_PACKAGE_FILES.items():
        info = assert_regular_single_link(path, role)
        require(info.st_size == size, f"{role} size differs")
        require(sha256_file(path) == digest, f"{role} hash differs")
    source = parse_dimacs(SOURCE / "instance.cnf")
    derived = parse_dimacs(DERIVED / "instance.cnf")
    require(
        (
            source["variable_count"],
            source["clause_count"],
            source["literal_count"],
        )
        == (6886, 23653, 188959),
        "source CNF counts differ",
    )
    require(
        (
            derived["variable_count"],
            derived["clause_count"],
            derived["literal_count"],
        )
        == (6886, 23968, 192169),
        "derived CNF counts differ",
    )
    expected_clauses = expected_breaker_clauses()
    require(len(expected_clauses) == 315, "breaker clause count differs")
    require(
        sum(map(len, expected_clauses)) == 3210,
        "breaker literal count differs",
    )
    breaker_payload = (DERIVED / "signature_breaker.json").read_bytes()
    breaker = strict_json_bytes(breaker_payload, "signature breaker")
    require(isinstance(breaker, Mapping), "signature breaker shape differs")
    require(
        set(breaker)
        == {
            "auxiliary_variables",
            "clause_count",
            "clauses",
            "comparison",
            "core_vertices",
            "encoding",
            "free_vertices",
            "literal_count",
            "order",
            "ordered_adjacent_pairs",
            "schema",
            "schema_version",
            "signature_bit_order",
            "signature_edge_variables",
            "template",
        },
        "signature breaker keys differ",
    )
    require(
        breaker["schema"]
        == "gamma-theta-hole5-signature-breaker-clauses-v1"
        and breaker["schema_version"] == 1
        and breaker["template"] == "hole5"
        and breaker["order"] == 12
        and breaker["auxiliary_variables"] == 0
        and breaker["clause_count"] == 315
        and breaker["literal_count"] == 3210,
        "signature breaker identity differs",
    )
    require(
        breaker["core_vertices"] == list(range(6))
        and breaker["free_vertices"] == list(range(6, 12))
        and breaker["signature_bit_order"] == list(range(6))
        and breaker["ordered_adjacent_pairs"]
        == [[value, value + 1] for value in range(6, 11)],
        "signature breaker vertex metadata differs",
    )
    edge = edge_variables()
    expected_edge_map = {
        str(vertex): [
            edge[tuple(sorted((core, vertex)))] for core in range(6)
        ]
        for vertex in range(6, 12)
    }
    require(
        breaker["signature_edge_variables"] == expected_edge_map,
        "signature edge variables differ",
    )
    require(
        breaker["clauses"] == [list(clause) for clause in expected_clauses],
        "signature breaker clause sequence differs",
    )
    require(
        derived["clauses"][: source["clause_count"]] == source["clauses"],
        "source clause prefix differs",
    )
    require(
        derived["clauses"][source["clause_count"] :] == expected_clauses,
        "derived CNF suffix differs",
    )
    source_lines = (SOURCE / "instance.cnf").read_bytes().splitlines(
        keepends=True
    )
    breaker_stream = b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in expected_clauses
    )
    expected_derived = (
        b"p cnf 6886 23968\n"
        + b"".join(source_lines[1:])
        + breaker_stream
    )
    require(
        (DERIVED / "instance.cnf").read_bytes() == expected_derived,
        "derived CNF bytes differ from reconstruction",
    )
    package_probe = run_package_probe()
    return {
        "breaker_clause_length_distribution": {
            str(length): count
            for length, count in sorted(
                Counter(map(len, expected_clauses)).items()
            )
        },
        "breaker_clause_stream_sha256": hashlib.sha256(
            breaker_stream
        ).hexdigest(),
        "breaker_clause_stream_size_bytes": len(breaker_stream),
        "breaker_clauses": len(expected_clauses),
        "breaker_literals": sum(map(len, expected_clauses)),
        "comparator_truth_checks": audit_breaker_truth(expected_clauses),
        "derived": {
            key: derived[key]
            for key in (
                "byte_count",
                "clause_count",
                "literal_count",
                "maximum_clause_length",
                "maximum_variable",
                "sha256",
                "variable_count",
            )
        },
        "package_probe_rerun": package_probe,
        "source": {
            key: source[key]
            for key in (
                "byte_count",
                "clause_count",
                "literal_count",
                "maximum_clause_length",
                "maximum_variable",
                "sha256",
                "variable_count",
            )
        },
        "source_body_preserved_byte_for_byte": True,
    }


class BlockReader:
    def __init__(self, handle: BinaryIO) -> None:
        self.handle = handle
        self.block = b""
        self.index = 0
        self.offset = 0

    def read_byte(self) -> int | None:
        if self.index == len(self.block):
            self.block = self.handle.read(1 << 20)
            self.index = 0
            if not self.block:
                return None
        result = self.block[self.index]
        self.index += 1
        self.offset += 1
        return result


def decode_uvarint(
    reader: BlockReader, raw: bytearray, record: int
) -> int:
    value = 0
    shift = 0
    count = 0
    while True:
        byte = reader.read_byte()
        require(byte is not None, f"mid-varint EOF at record {record}")
        raw.append(byte)
        count += 1
        payload = byte & 0x7F
        require(count <= 10, f"varint overflow at record {record}")
        value |= payload << shift
        if byte & 0x80 == 0:
            require(
                count == 1 or payload != 0,
                f"noncanonical varint at record {record}",
            )
            return value
        shift += 7


def parse_binary_proof(
    path: Path,
    *,
    allow_deletions: bool,
    addition_comparison: BinaryIO | None = None,
) -> dict[str, object]:
    assert_regular_single_link(path, "binary proof")
    proof_digest = hashlib.sha256()
    addition_digest = hashlib.sha256()
    deletion_digest = hashlib.sha256()
    record_count = 0
    addition_count = 0
    deletion_count = 0
    addition_literals = 0
    deletion_literals = 0
    maximum_variable = 0
    maximum_clause_length = 0
    empty_additions = 0
    final_empty_record = 0
    first_deletion_record: int | None = None
    addition_bytes = 0
    deletion_bytes = 0
    seen_empty = False
    with path.open("rb") as handle:
        reader = BlockReader(handle)
        while True:
            prefix = reader.read_byte()
            if prefix is None:
                break
            require(not seen_empty, "record follows final empty addition")
            record_count += 1
            require(prefix in (ord("a"), ord("d")), "invalid proof prefix")
            deletion = prefix == ord("d")
            require(allow_deletions or not deletion, "deletion is forbidden")
            raw = bytearray((prefix,))
            literals: list[int] = []
            while True:
                encoded = decode_uvarint(reader, raw, record_count)
                if encoded == 0:
                    break
                require(encoded != 1, "negative-zero literal")
                variable = encoded >> 1
                require(1 <= variable <= MAX_VAR, "proof variable out of range")
                literals.append(-variable if encoded & 1 else variable)
            require(not deletion or literals, "empty deletion")
            literal_set = set(literals)
            require(len(literal_set) == len(literals), "duplicate proof literal")
            require(
                not any(-literal in literal_set for literal in literals),
                "tautological proof clause",
            )
            raw_bytes = bytes(raw)
            proof_digest.update(raw_bytes)
            maximum_clause_length = max(
                maximum_clause_length, len(literals)
            )
            if literals:
                maximum_variable = max(
                    maximum_variable,
                    max(abs(literal) for literal in literals),
                )
            if deletion:
                deletion_count += 1
                deletion_literals += len(literals)
                deletion_digest.update(raw_bytes)
                deletion_bytes += len(raw_bytes)
                if first_deletion_record is None:
                    first_deletion_record = record_count
            else:
                addition_count += 1
                addition_literals += len(literals)
                addition_digest.update(raw_bytes)
                addition_bytes += len(raw_bytes)
                if addition_comparison is not None:
                    require(
                        addition_comparison.read(len(raw_bytes)) == raw_bytes,
                        "addition subsequence differs byte-for-byte",
                    )
                if not literals:
                    empty_additions += 1
                    final_empty_record = record_count
                    seen_empty = True
        byte_count = reader.offset
    require(byte_count > 0, "binary proof is empty")
    require(
        empty_additions == 1 and final_empty_record == record_count,
        "proof lacks one final empty addition",
    )
    if addition_comparison is not None:
        require(
            addition_comparison.read(1) == b"",
            "addition proof has unmatched trailing bytes",
        )
    return {
        "addition_count": addition_count,
        "addition_literal_count": addition_literals,
        "addition_stream_sha256": addition_digest.hexdigest(),
        "addition_stream_size_bytes": addition_bytes,
        "byte_count": byte_count,
        "deletion_count": deletion_count,
        "deletion_literal_count": deletion_literals,
        "deletion_stream_sha256": deletion_digest.hexdigest(),
        "deletion_stream_size_bytes": deletion_bytes,
        "empty_addition_count": empty_additions,
        "final_empty_record": final_empty_record,
        "first_deletion_record": first_deletion_record,
        "maximum_clause_length": maximum_clause_length,
        "maximum_variable": maximum_variable,
        "proof_sha256": proof_digest.hexdigest(),
        "record_count": record_count,
    }


def files_equal(left: Path, right: Path) -> bool:
    with left.open("rb") as left_handle, right.open("rb") as right_handle:
        while True:
            left_block = left_handle.read(1 << 20)
            right_block = right_handle.read(1 << 20)
            if left_block != right_block:
                return False
            if not left_block:
                return True


def rerun_parser(recorded_report: Mapping[str, object]) -> dict[str, object]:
    with tempfile.TemporaryDirectory(
        prefix=".hole5-postrun-parser-", dir=CAMPAIGN / "results"
    ) as temporary:
        root = Path(temporary).resolve()
        output = root / "additions.bdrat"
        command = (
            str(PYTHON),
            "-I",
            "-B",
            str(PARSER),
            "strip",
            "--proof",
            str((RUN / "proof.raw.bdrat").resolve()),
            "--output",
            str(output),
            "--max-var",
            str(MAX_VAR),
        )
        completed = subprocess.run(
            command,
            cwd=CAMPAIGN,
            env={},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=180,
            check=False,
        )
        require(completed.returncode == 0, "standalone parser rerun failed")
        require(completed.stderr == b"", "standalone parser emitted stderr")
        report = strict_json_bytes(completed.stdout, "fresh parser report")
        require(report == recorded_report, "fresh parser report differs")
        require(
            files_equal(output, RUN / "proof.additions.bdrat"),
            "fresh stripped proof differs byte-for-byte",
        )
        return {
            "addition_proof_byte_identical": True,
            "command": [
                *command[:8],
                "<TEMP>/additions.bdrat",
                *command[9:],
            ],
            "exit_code": completed.returncode,
            "report_byte_identical": (
                completed.stdout == (RUN / "parser.stdout").read_bytes()
            ),
            "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
        }


def audit_proofs(parser_report: Mapping[str, object]) -> dict[str, object]:
    raw_path = RUN / "proof.raw.bdrat"
    addition_path = RUN / "proof.additions.bdrat"
    with addition_path.open("rb") as comparison:
        raw = parse_binary_proof(
            raw_path,
            allow_deletions=True,
            addition_comparison=comparison,
        )
    addition = parse_binary_proof(
        addition_path,
        allow_deletions=False,
    )
    require(
        parser_report
        == {
            "addition_only": addition,
            "all_addition_bytes_preserved_in_order": True,
            "source": raw,
        },
        "recorded parser report differs from clean-room parse",
    )
    require(
        raw["addition_stream_sha256"] == addition["proof_sha256"]
        and raw["addition_stream_size_bytes"] == addition["byte_count"]
        and raw["addition_count"] == addition["record_count"]
        and raw["addition_literal_count"] == addition["addition_literal_count"],
        "raw addition stream does not equal stripped proof",
    )
    parser_rerun = rerun_parser(parser_report)
    return {
        "addition_only": addition,
        "addition_subsequence_byte_exact": True,
        "accepted_parser_rerun": parser_rerun,
        "raw": raw,
    }


def git_environment(git: Path) -> dict[str, str]:
    return {
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "LC_ALL": "C",
        "PATH": str(git.parent),
    }


def git_run(arguments: Sequence[str]) -> bytes:
    git_name = shutil.which("git")
    require(git_name is not None, "git executable is unavailable")
    git = Path(git_name).resolve()
    completed = subprocess.run(
        (str(git), "--no-pager", "-C", str(REPOSITORY), *arguments),
        env=git_environment(git),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=60,
        check=False,
    )
    require(completed.returncode == 0, f"git command failed: {arguments}")
    require(completed.stderr == b"", f"git emitted stderr: {arguments}")
    return completed.stdout


def git_object(commit: str, repository_relative: str) -> tuple[str, bytes]:
    specification = f"{commit}:{repository_relative}"
    object_id = git_run(("rev-parse", "--verify", specification)).decode(
        "ascii"
    ).strip()
    require(
        len(object_id) in (40, 64)
        and all(character in "0123456789abcdef" for character in object_id),
        "Git object ID is malformed",
    )
    payload = git_run(("show", specification))
    return object_id, payload


def audit_git_and_inputs(
    configuration: Mapping[str, object],
) -> dict[str, object]:
    head = git_run(("rev-parse", "--verify", "HEAD")).decode("ascii").strip()
    origin = git_run(("rev-parse", "--verify", "origin/main")).decode(
        "ascii"
    ).strip()
    git_run(("merge-base", "--is-ancestor", COMMIT, PRESERVATION_COMMIT))
    git_run(("merge-base", "--is-ancestor", PRESERVATION_COMMIT, head))
    git_run(("merge-base", "--is-ancestor", PRESERVATION_COMMIT, origin))
    require(configuration["expected_head_commit"] == COMMIT, "expected HEAD differs")
    binding = configuration["git_source_binding"]
    require(isinstance(binding, Mapping), "Git binding shape differs")
    require(
        binding
        == {
            "global_worktree_cleanliness_required": False,
            "head_commit": COMMIT,
            "repository_relative_campaign_path": CAMPAIGN_IN_REPOSITORY,
            "runtime_source_mismatches": [],
            "runtime_sources_match_head": True,
        },
        "recorded Git binding differs",
    )
    manifest = configuration["runtime_source_manifest"]
    require(isinstance(manifest, list) and len(manifest) == 23, "runtime manifest")
    records: list[tuple[str, str]] = []
    seen: set[str] = set()
    git_objects: list[dict[str, object]] = []
    for row in manifest:
        require(
            isinstance(row, list)
            and len(row) == 2
            and all(isinstance(value, str) for value in row),
            "runtime source row differs",
        )
        relative, digest = row
        require(relative not in seen, "duplicate runtime source")
        require(
            relative == Path(relative).as_posix()
            and not Path(relative).is_absolute()
            and ".." not in Path(relative).parts,
            "unsafe runtime source path",
        )
        require(
            len(digest) == 64
            and all(character in "0123456789abcdef" for character in digest),
            "runtime digest is malformed",
        )
        seen.add(relative)
        records.append((relative, digest))
        working = CAMPAIGN / relative
        info = assert_regular_single_link(working, f"runtime source {relative}")
        require(sha256_file(working) == digest, f"runtime source changed {relative}")
        repository_relative = f"{CAMPAIGN_IN_REPOSITORY}/{relative}"
        object_id, payload = git_object(COMMIT, repository_relative)
        require(
            hashlib.sha256(payload).hexdigest() == digest,
            f"Git object differs {relative}",
        )
        require(payload == working.read_bytes(), f"working/Git differ {relative}")
        git_objects.append(
            {
                "git_object": object_id,
                "path": relative,
                "sha256": digest,
                "size_bytes": info.st_size,
            }
        )
    expected_source_set = hashlib.sha256(
        "".join(f"{path} {digest}\n" for path, digest in records).encode(
            "ascii"
        )
    ).hexdigest()
    require(
        configuration["runtime_source_set_sha256"] == expected_source_set,
        "runtime source-set hash differs",
    )
    preservation_tree = git_run(
        ("rev-parse", "--verify", f"{PRESERVATION_COMMIT}^{{tree}}")
    ).decode("ascii").strip()
    require(
        preservation_tree == PRESERVATION_COMMIT_TREE,
        "preservation commit tree differs",
    )
    preserved_run_path = (
        f"{CAMPAIGN_IN_REPOSITORY}/results/"
        "synthesis_k3_hole5_signature_seed0_600s_binary"
    )
    preserved_run_tree = git_run(
        (
            "rev-parse",
            "--verify",
            f"{PRESERVATION_COMMIT}:{preserved_run_path}",
        )
    ).decode("ascii").strip()
    require(preserved_run_tree == PRESERVED_RUN_TREE, "preserved run tree differs")
    preserved_run_objects: list[dict[str, object]] = []
    for name in sorted(EXPECTED_RUN_FILES):
        size, digest, _ = EXPECTED_RUN_FILES[name]
        object_id, payload = git_object(
            PRESERVATION_COMMIT, f"{preserved_run_path}/{name}"
        )
        require(len(payload) == size, f"preserved run size differs {name}")
        require(
            hashlib.sha256(payload).hexdigest() == digest,
            f"preserved run hash differs {name}",
        )
        require(
            payload == (RUN / name).read_bytes(),
            f"preserved/working run bytes differ {name}",
        )
        preserved_run_objects.append(
            {
                "git_object": object_id,
                "path": name,
                "sha256": digest,
                "size_bytes": size,
            }
        )
    package_git: list[dict[str, object]] = []
    for role, (path, size, digest) in EXPECTED_PACKAGE_FILES.items():
        relative = path.relative_to(CAMPAIGN).as_posix()
        object_id, payload = git_object(
            COMMIT, f"{CAMPAIGN_IN_REPOSITORY}/{relative}"
        )
        require(len(payload) == size, f"Git package size differs {role}")
        require(
            hashlib.sha256(payload).hexdigest() == digest,
            f"Git package hash differs {role}",
        )
        require(payload == path.read_bytes(), f"Git package bytes differ {role}")
        package_git.append(
            {
                "git_object": object_id,
                "path": relative,
                "sha256": digest,
                "size_bytes": size,
            }
        )
    immutable = configuration["immutable_input_bindings"]
    require(isinstance(immutable, Mapping), "immutable bindings shape differs")
    expected_immutable_roles = set(EXPECTED_PACKAGE_FILES)
    expected_immutable_roles.update(f"runtime:{path}" for path, _ in records)
    expected_immutable_roles.update(
        {
            "tool:cadical",
            "tool:cadical:source",
            "tool:drat_trim",
            "tool:drat_trim:source",
            "tool:parser",
            "tool:python",
        }
    )
    require(
        set(immutable) == expected_immutable_roles,
        "immutable binding roles differ",
    )
    for role, record in immutable.items():
        require(
            isinstance(record, Mapping)
            and set(record) == {"path", "sha256", "size_bytes"},
            f"immutable record shape differs {role}",
        )
        path = Path(record["path"])
        info = assert_regular_single_link(path, role)
        require(
            info.st_size == record["size_bytes"]
            and sha256_file(path) == record["sha256"],
            f"immutable binding differs {role}",
        )
    return {
        "preservation_commit": PRESERVATION_COMMIT,
        "preservation_commit_is_ancestor_of_current_head": True,
        "preservation_commit_is_ancestor_of_origin_main": True,
        "preservation_commit_tree": preservation_tree,
        "preserved_run_git_objects": preserved_run_objects,
        "preserved_run_tree": preserved_run_tree,
        "package_git_objects": package_git,
        "source_commit": COMMIT,
        "source_commit_is_ancestor_of_preservation_commit": True,
        "runtime_source_set_sha256": expected_source_set,
        "runtime_sources": git_objects,
    }


def audit_tools() -> dict[str, object]:
    records: dict[str, object] = {}
    for role, (path, size, digest) in EXPECTED_TOOLS.items():
        info = assert_regular_single_link(path, role)
        require(info.st_size == size, f"{role} size differs")
        require(sha256_file(path) == digest, f"{role} hash differs")
        if role in {"cadical", "checker", "python"}:
            require(os.access(path, os.X_OK), f"{role} is not executable")
        records[role] = {
            "sha256": digest,
            "size_bytes": size,
        }
    return records


def normalize_checker_output(payload: bytes, role: str) -> list[str]:
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise AssertionError(f"{role} output is not ASCII") from error
    require("warning" not in text.lower(), f"{role} contains warning")
    lines = [
        line.strip()
        for line in text.replace("\r", "").splitlines()
        if line.strip()
    ]
    expected_prefix = [
        "c turning on binary mode checking",
        "c parsing input formula with 6886 variables and 23968 clauses",
        "c finished parsing, read 6337621 bytes from proof file",
        "c start forward verification",
        "c 18740 of 23968 clauses in core",
        (
            "c 148710 of 247982 lemmas in core using 10912555 "
            "resolution steps"
        ),
        "c 0 RAT lemmas in core; 0 redundant literals in core lemmas",
        "c optimized proofs are not supported for forward checking",
        "s VERIFIED",
    ]
    require(lines[:9] == expected_prefix, f"{role} checker transcript differs")
    require(len(lines) == 10, f"{role} checker line count differs")
    require(
        re.fullmatch(
            r"c verification time: [0-9]+(?:\.[0-9]+)? seconds", lines[9]
        )
        is not None,
        f"{role} checker time line differs",
    )
    return [*expected_prefix, "c verification time: <ELAPSED> seconds"]


def campaign_lock_path() -> Path:
    digest = hashlib.sha256(str(CAMPAIGN.resolve()).encode("utf-8")).hexdigest()
    return (
        Path(tempfile.gettempdir()).resolve()
        / f"gamma-theta-k3-heavy-child-{digest[:20]}.lock"
    )


def checker_child_setup() -> None:
    os.setsid()
    os.nice(5)
    resource.setrlimit(resource.RLIMIT_CPU, (240, 241))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 << 20, 16 << 20))
    os.umask(0o077)


def replay_checker(recorded_stdout: bytes) -> dict[str, object]:
    lock_path = campaign_lock_path()
    assert_no_symlink_components(lock_path.parent)
    flags = os.O_CREAT | os.O_RDWR
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(lock_path, flags, 0o600)
    try:
        lock_info = os.fstat(descriptor)
        require(
            stat.S_ISREG(lock_info.st_mode) and lock_info.st_nlink == 1,
            "campaign lock is unsafe",
        )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise AssertionError("another campaign heavy child is active") from error
        command = (
            str(CHECKER),
            str((DERIVED / "instance.cnf").resolve()),
            str((RUN / "proof.additions.bdrat").resolve()),
            "-i",
            "-f",
            "-W",
            "-U",
            "-t",
            "1200",
        )
        completed = subprocess.run(
            command,
            cwd=CAMPAIGN,
            env={},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=300,
            check=False,
            preexec_fn=checker_child_setup,
        )
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)
    require(completed.returncode == 0, "fresh strict checker exited nonzero")
    require(completed.stderr == b"", "fresh strict checker emitted stderr")
    recorded_normalized = normalize_checker_output(
        recorded_stdout, "recorded"
    )
    fresh_normalized = normalize_checker_output(completed.stdout, "fresh")
    require(
        fresh_normalized == recorded_normalized,
        "fresh/recorded checker transcripts differ",
    )
    normalized_bytes = ("\n".join(fresh_normalized) + "\n").encode("ascii")
    return {
        "command": list(command),
        "exit_code": completed.returncode,
        "normalized_stdout": fresh_normalized,
        "normalized_stdout_sha256": hashlib.sha256(
            normalized_bytes
        ).hexdigest(),
        "recorded_and_fresh_semantics_identical": True,
        "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
    }


def exact_command_hash(command: Sequence[str]) -> str:
    return hashlib.sha256(canonical_json(list(command), pretty=False)).hexdigest()


def audit_child(
    phase: str,
    record: Mapping[str, object],
    configuration: Mapping[str, object],
    *,
    expected_exit: int,
    executable_hash: str,
) -> dict[str, object]:
    require(set(record) == CHILD_KEYS, f"{phase} child shape differs")
    command = configuration["commands"][phase]
    require(record["command"] == command, f"{phase} command differs")
    require(
        record["command_sha256"] == exact_command_hash(command),
        f"{phase} command hash differs",
    )
    require(record["exit_code"] == expected_exit, f"{phase} exit differs")
    require(
        record["termination_signal"] is None
        and record["timed_out"] is False
        and record["memory_limit_exceeded"] is False,
        f"{phase} resource status differs",
    )
    require(
        record["executable_sha256_before"] == executable_hash
        and record["executable_sha256_after"] == executable_hash,
        f"{phase} executable hash differs",
    )
    for stream in ("stdout", "stderr"):
        path = RUN / f"{phase}.{stream}"
        require(
            record[f"{stream}_path"] == str(path.resolve()),
            f"{phase} {stream} path differs",
        )
        require(
            record[f"{stream}_sha256"] == sha256_file(path),
            f"{phase} {stream} hash differs",
        )
    started = record["started_unix_ns"]
    finished = record["finished_unix_ns"]
    wall = record["wall_seconds"]
    require(
        type(started) is int
        and type(finished) is int
        and started < finished
        and isinstance(wall, (int, float))
        and wall > 0,
        f"{phase} timing differs",
    )
    require(
        abs((finished - started) / 1e9 - wall) < 0.1,
        f"{phase} wall accounting differs",
    )
    memory_limit = configuration["resources"][f"{phase}_memory_mib"]
    require(
        record["memory_limit_mib"] == memory_limit
        and record["maximum_resident_set_size_raw_unit"] == "bytes"
        and math.isclose(
            record["maximum_resident_set_size_raw"] / (1 << 20),
            record["maximum_resident_set_size_mib"],
            rel_tol=0,
            abs_tol=1e-9,
        )
        and record["maximum_resident_set_size_mib"] <= memory_limit
        and record["peak_polled_resident_set_size_mib"] <= memory_limit,
        f"{phase} memory accounting differs",
    )
    require(
        record["available_memory_before_bytes"]
        >= (memory_limit + 512) << 20,
        f"{phase} available-memory gate differs",
    )
    require(
        record["file_limit_mib"] == configuration["resources"]["file_limit_mib"],
        f"{phase} file limit differs",
    )
    for key in ("user_cpu_seconds", "system_cpu_seconds"):
        require(
            isinstance(record[key], (int, float)) and record[key] >= 0,
            f"{phase} CPU accounting differs",
        )
    return {
        "command_sha256": record["command_sha256"],
        "exit_code": record["exit_code"],
        "maximum_resident_set_size_mib": record[
            "maximum_resident_set_size_mib"
        ],
        "stderr_sha256": record["stderr_sha256"],
        "stdout_sha256": record["stdout_sha256"],
        "wall_seconds": record["wall_seconds"],
    }


def audit_configuration(
    configuration: Mapping[str, object],
    tools: Mapping[str, object],
) -> None:
    require(
        configuration["schema"]
        == "gamma-theta-hole5-binary-production-config-v1"
        and configuration["schema_version"] == 1
        and configuration["seed"] == 0,
        "run configuration identity differs",
    )
    require(
        configuration["gates"]
        == {
            "atomic_new_output": True,
            "hostile_audit_gate": True,
            "raw_binary_proof_preserved": True,
            "source_to_head_gate": True,
            "validation_gate": True,
        },
        "run gates differ",
    )
    require(
        configuration["source_package_path"] == str(SOURCE.resolve()),
        "source package path differs",
    )
    package = configuration["package"]
    require(
        package
        == {
            "breaker_clause_stream_sha256": (
                "ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6"
            ),
            "breaker_sha256": (
                "62ce8f60ecfe74f58bcd113166009637f854d7d663aea2e59395ae224682d18a"
            ),
            "clause_count": 23968,
            "cnf_sha256": (
                "c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104"
            ),
            "literal_count": 192169,
            "manifest_sha256": (
                "da33bc1708f7d21b92ceedc68710d5433a1aacbe6e32b8a7432bbab45d8cc788"
            ),
            "path": str(DERIVED.resolve()),
            "variable_count": 6886,
        },
        "run package record differs",
    )
    expected_commands = {
        "solver": [
            str(CADICAL.resolve()),
            "--seed=0",
            "--binary",
            "--no-colors",
            "-q",
            "-t",
            "600",
            "-w",
            str((RUN / "solver.result").resolve()),
            str((DERIVED / "instance.cnf").resolve()),
            str((RUN / "proof.raw.bdrat").resolve()),
        ],
        "parser": [
            str(PYTHON),
            "-I",
            "-B",
            str(PARSER.resolve()),
            "strip",
            "--proof",
            str((RUN / "proof.raw.bdrat").resolve()),
            "--output",
            str((RUN / "proof.additions.bdrat").resolve()),
            "--max-var",
            "6886",
        ],
        "checker": [
            str(CHECKER.resolve()),
            str((DERIVED / "instance.cnf").resolve()),
            str((RUN / "proof.additions.bdrat").resolve()),
            "-i",
            "-f",
            "-W",
            "-U",
            "-t",
            "1200",
        ],
    }
    require(
        configuration["commands"] == expected_commands,
        "normalized commands differ",
    )
    resources = configuration["resources"]
    require(
        resources["physical_memory_bytes"] == 16 << 30
        and resources["maximum_responsive_child_memory_mib"] == 4096
        and resources["solver_internal_seconds"] == 600
        and resources["solver_supervisor_seconds"] == 615
        and resources["parser_supervisor_seconds"] == 615
        and resources["checker_internal_seconds"] == 1200
        and resources["checker_supervisor_seconds"] == 1215
        and resources["solver_memory_mib"] == 1024
        and resources["parser_memory_mib"] == 512
        and resources["checker_memory_mib"] == 2048
        and resources["file_limit_mib"] == 512
        and resources["disk_reserve_mib"] == 4096,
        "resource configuration differs",
    )
    initial_disk = resources["initial_disk_gate"]
    require(
        initial_disk["remaining_file_slots"] == 9
        and initial_disk["free_bytes"] >= initial_disk["required_bytes"]
        and initial_disk["required_bytes"] == 9160359936,
        "initial disk gate differs",
    )
    tool_records = configuration["tools"]
    require(
        tool_records["cadical"]["sha256"]
        == EXPECTED_TOOLS["cadical"][2]
        and tool_records["cadical"]["source_archive_sha256"]
        == EXPECTED_TOOLS["cadical_archive"][2]
        and tool_records["drat_trim"]["sha256"]
        == EXPECTED_TOOLS["checker"][2]
        and tool_records["drat_trim"]["source_archive_sha256"]
        == EXPECTED_TOOLS["checker_archive"][2]
        and tool_records["clean_room_parser"]["sha256"]
        == EXPECTED_TOOLS["parser"][2]
        and tool_records["python"]["sha256"] == EXPECTED_TOOLS["python"][2],
        "tool records differ",
    )
    del tools


def audit_activation_and_children(
    configuration: Mapping[str, object],
    certificate: Mapping[str, object],
    outcome: Mapping[str, object],
    parser_report: Mapping[str, object],
    checker_replay: Mapping[str, object],
) -> dict[str, object]:
    require(
        certificate["schema"] == "gamma-theta-hole5-binary-certificate-v1"
        and certificate["schema_version"] == 1
        and certificate["status"] == "UNSAT_REPLAY_ARTIFACT"
        and certificate["claim_status"] == "NO_STANDALONE_MATHEMATICAL_CLAIM",
        "certificate identity differs",
    )
    require(
        certificate["scope"]
        == "exact retained hole5 S6 signature-broken full-bank CNF",
        "certificate scope differs",
    )
    require(
        certificate["package_manifest_sha256"]
        == EXPECTED_PACKAGE_FILES["derived:manifest.json"][2]
        and certificate["cnf_sha256"]
        == EXPECTED_PACKAGE_FILES["derived:instance.cnf"][2],
        "certificate formula binding differs",
    )
    require(
        certificate["raw_binary_proof"]
        == {
            "path": "proof.raw.bdrat",
            "preserved": True,
            "sha256": EXPECTED_RUN_FILES["proof.raw.bdrat"][1],
            "size_bytes": EXPECTED_RUN_FILES["proof.raw.bdrat"][0],
        }
        and certificate["addition_only_binary_proof"]
        == {
            "path": "proof.additions.bdrat",
            "sha256": EXPECTED_RUN_FILES["proof.additions.bdrat"][1],
            "size_bytes": EXPECTED_RUN_FILES["proof.additions.bdrat"][0],
        },
        "certificate proof binding differs",
    )
    require(
        certificate["parser_report"] == parser_report
        and certificate["parser_command"] == configuration["commands"]["parser"]
        and certificate["checker_command"]
        == configuration["commands"]["checker"],
        "certificate replay binding differs",
    )
    require(
        certificate["strict_checker_requirements"]
        == {
            "binary_input": True,
            "exactly_one_verified_line": True,
            "forward": True,
            "rup_only": True,
            "warning_fatal": True,
            "zero_rat_lemmas": True,
        },
        "certificate strict requirements differ",
    )
    activation = certificate["activation_condition"]
    require(
        activation
        == {
            "required_claim_status": "VERIFIED_FINITE_CERTIFICATE",
            "required_file": "outcome.json",
            "required_self_hash_binding": (
                "outcome.artifacts.certificate.json.sha256"
            ),
            "required_status": "UNSAT_VERIFIED_FINITE_CERTIFICATE",
        },
        "certificate activation condition differs",
    )
    require(
        outcome["schema"]
        == "gamma-theta-hole5-binary-production-outcome-v1"
        and outcome["schema_version"] == 1
        and outcome["status"] == activation["required_status"]
        and outcome["claim_status"] == activation["required_claim_status"],
        "outcome activation status differs",
    )
    require(
        outcome["package_manifest_sha256"]
        == certificate["package_manifest_sha256"]
        and outcome["cnf_sha256"] == certificate["cnf_sha256"]
        and outcome["run_config_sha256"]
        == EXPECTED_RUN_FILES["run_config.json"][1],
        "outcome formula/config binding differs",
    )
    require(outcome["failures"] == [], "outcome records failures")
    require(
        outcome["parser_report"] == parser_report,
        "outcome parser report differs",
    )
    require(
        outcome["semantic_checks"]
        == {
            "addition_only_reparsed": True,
            "all_deletions_removed": True,
            "checker_warning_free": True,
            "checker_zero_rat_lemmas": True,
            "clean_room_parser_max_var": 6886,
            "raw_binary_proof_preserved": True,
            "solver_result_unsat": True,
            "strict_binary_forward_rup_replay": True,
        },
        "outcome semantic checks differ",
    )
    expected_artifacts = {
        name: {"sha256": digest, "size_bytes": size}
        for name, (size, digest, _) in EXPECTED_RUN_FILES.items()
        if name != "outcome.json"
    }
    require(
        outcome["artifacts"] == expected_artifacts,
        "outcome artifact map differs",
    )
    require(
        outcome["artifacts"]["certificate.json"]["sha256"]
        == EXPECTED_RUN_FILES["certificate.json"][1],
        "certificate activation hash differs",
    )
    require(
        (RUN / "solver.result").read_bytes() == b"s UNSATISFIABLE\n"
        and (RUN / "solver.stdout").read_bytes() == b""
        and (RUN / "solver.stderr").read_bytes() == b"",
        "solver result/output differs",
    )
    require(
        (RUN / "parser.stderr").read_bytes() == b""
        and (RUN / "checker.stderr").read_bytes() == b"",
        "parser/checker stderr differs",
    )
    recorded_normalized = normalize_checker_output(
        (RUN / "checker.stdout").read_bytes(), "recorded"
    )
    require(
        recorded_normalized == checker_replay["normalized_stdout"],
        "checker replay normalization differs",
    )
    children = {
        "solver": audit_child(
            "solver",
            outcome["solver"],
            configuration,
            expected_exit=20,
            executable_hash=EXPECTED_TOOLS["cadical"][2],
        ),
        "parser": audit_child(
            "parser",
            outcome["parser"],
            configuration,
            expected_exit=0,
            executable_hash=EXPECTED_TOOLS["python"][2],
        ),
        "checker": audit_child(
            "checker",
            outcome["checker"],
            configuration,
            expected_exit=0,
            executable_hash=EXPECTED_TOOLS["checker"][2],
        ),
    }
    disk_gates = outcome["disk_gates"]
    require(
        set(disk_gates) == {"before_parser", "before_checker"},
        "post-run disk gate keys differ",
    )
    for name, slots in (("before_parser", 5), ("before_checker", 2)):
        record = disk_gates[name]
        require(
            record["remaining_file_slots"] == slots
            and record["free_bytes"] >= record["required_bytes"],
            f"{name} disk gate differs",
        )
    return {
        "activation_binding_valid": True,
        "artifact_map": expected_artifacts,
        "children": children,
        "recorded_checker_output_exact": True,
        "solver_result_exact": True,
    }


def audit() -> dict[str, object]:
    require(
        "hole5_binary_production" not in {
            module for module in sys.modules if module != "__main__"
        },
        "production runner entered the verifier module graph",
    )
    tree = audit_run_tree()
    tools = audit_tools()
    configuration_raw = strict_json_file(RUN / "run_config.json", "run config")
    certificate_raw = strict_json_file(RUN / "certificate.json", "certificate")
    outcome_raw = strict_json_file(RUN / "outcome.json", "outcome")
    parser_raw = strict_json_file(RUN / "parser.stdout", "parser report")
    require(
        all(
            isinstance(value, Mapping)
            for value in (
                configuration_raw,
                certificate_raw,
                outcome_raw,
                parser_raw,
            )
        ),
        "structured artifact root differs",
    )
    configuration = configuration_raw
    certificate = certificate_raw
    outcome = outcome_raw
    parser_report = parser_raw
    audit_configuration(configuration, tools)
    git = audit_git_and_inputs(configuration)
    formula = audit_formula()
    proofs = audit_proofs(parser_report)
    checker_replay = replay_checker((RUN / "checker.stdout").read_bytes())
    activation = audit_activation_and_children(
        configuration,
        certificate,
        outcome,
        parser_report,
        checker_replay,
    )
    return {
        "schema": "gamma-theta-hole5-binary-postrun-hostile-audit-v1",
        "schema_version": 1,
        "verdict": "ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033",
        "claim_boundary": (
            "The exact retained hole5 S6 formula is certified UNSAT. "
            "This is a finite branch result, not a universal resolution."
        ),
        "production_runner_imported_or_trusted": False,
        "production_solver_launched": False,
        "checks": {
            "activation_and_children": activation,
            "formula_and_s6_breaker": formula,
            "git_provenance": git,
            "proofs": proofs,
            "run_tree": tree,
            "strict_checker_replay": checker_replay,
            "tools": tools,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    payload = canonical_json(audit())
    if arguments.output is None:
        sys.stdout.buffer.write(payload)
    else:
        output = arguments.output
        require(not output.exists() and not output.is_symlink(), "output exists")
        with output.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
