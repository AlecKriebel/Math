#!/usr/bin/env python3
"""Read-only replay for the independent verifier-B exact-byte code audit.

Repository inputs are opened read-only.  Compilation and checker replay use
only a fresh temporary directory, which is deleted on exit.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Mapping


SCHEMA = "gamma-theta-order13-k3-hole9-external-code-audit-replay-v1"
VERDICT = "ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER"

ROOT = Path(__file__).resolve().parents[3]

FORMULA = "certificates/order13_k3_hole9_attempt000001_lrat/instance.cnf"
CONSTRUCTOR_FORMULA = "instances/order13_k3_hole9/instance.cnf"
BDRAT = (
    "certificates/order13_k3_hole9_attempt000001_lrat/"
    "proof.normalized.bdrat"
)
LRAT = "certificates/order13_k3_hole9_attempt000001_lrat/proof.lrat"
DRAT_BINARY = "tools/drat_trim_2023_05_22/drat-trim"
LRAT_BINARY = "tools/drat_trim_2023_05_22/lrat-check"
DRAT_SOURCE = "tools/drat_trim_2023_05_22/drat-trim.c"
LRAT_SOURCE = "tools/drat_trim_2023_05_22/lrat-check.c"
TOOL_MAKEFILE = "tools/drat_trim_2023_05_22/Makefile"
VERIFIER = "src/verifier_b/order13_k3_hole9_certificate.py"
FOCUSED_TEST = "tests/test_order13_k3_hole9_certificate_verifier_b.py"
RETAINED_EVIDENCE = (
    "reviews/order13_k3_hole9_certificate_verifier_b/evidence.json"
)
TOOL_PROVENANCE = (
    "reviews/order13_k3_hole9_certificate_verifier_b/"
    "tool-source-provenance.json"
)


BINDINGS: Mapping[str, tuple[int, str]] = {
    BDRAT: (
        742337,
        "af216ef2d7698db2b1d1c55411bc05025bfe25f10c16f2e85c5301f7a88bdd5f",
    ),
    CONSTRUCTOR_FORMULA: (
        1168197,
        "3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea",
    ),
    DRAT_BINARY: (
        70088,
        "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb",
    ),
    DRAT_SOURCE: (
        59498,
        "f7619bdc338bc8151b2f6bb87488052795c926b048d5040cf165742eb1ba9a26",
    ),
    FOCUSED_TEST: (
        3826,
        "2ca00e46efee4597fcc532ffe9e8d9fc61c73631def42011d26ab7a3cf516fc5",
    ),
    FORMULA: (
        1168197,
        "3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea",
    ),
    LRAT: (
        8546664,
        "f6ef614f2acee4cf43aa3b75372b354912c50248a13c3f863479cdc49b061805",
    ),
    LRAT_BINARY: (
        36520,
        "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2",
    ),
    LRAT_SOURCE: (
        17332,
        "05b3c92f6734fdfc9ee5c72217c9935540c1255b58bc9bdc134b6b26f5b43c9f",
    ),
    RETAINED_EVIDENCE: (
        15105,
        "3de45d16b906e52c3960e4b2e75604908c8cacf356b84d7337db721f4fa49af8",
    ),
    TOOL_MAKEFILE: (
        493,
        "1f3c7128b1dd739723257edd95cc28a2ee747779ca01ae80ed9252f02ec5149d",
    ),
    TOOL_PROVENANCE: (
        2518,
        "95702f678c8fbbde5f733e121105d59b2c3890821b1195300d7ec5f03cefa275",
    ),
    VERIFIER: (
        39193,
        "4adf3691f438c03b230ff323ea5f7c180db9b5c8cd895b6f31327f5e154a97ee",
    ),
}


class AuditError(RuntimeError):
    """The replay failed closed."""


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("ascii")


def load_json_unique(payload: bytes, label: str) -> object:
    def reject_constant(value: str) -> object:
        raise AuditError(f"non-finite JSON constant in {label}: {value}")

    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise AuditError(f"duplicate JSON key in {label}: {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(
            payload,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditError(f"malformed JSON in {label}") from exc


def bind_inputs() -> dict[str, bytes]:
    payloads: dict[str, bytes] = {}
    for relative in sorted(BINDINGS):
        expected_size, expected_hash = BINDINGS[relative]
        if expected_size < 0 or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise AuditError(
                f"external audit has an unfinished binding for {relative}"
            )
        path = ROOT / relative
        if path.is_symlink() or not path.is_file():
            raise AuditError(f"not a nonsymlink regular file: {relative}")
        payload = path.read_bytes()
        actual = sha256(payload)
        if len(payload) != expected_size or actual != expected_hash:
            raise AuditError(
                f"binding mismatch for {relative}: "
                f"size={len(payload)}, sha256={actual}"
            )
        payloads[relative] = payload
    if payloads[FORMULA] != payloads[CONSTRUCTOR_FORMULA]:
        raise AuditError("certificate and constructor formulas differ")
    return payloads


def independent_dimacs_census(payload: bytes) -> dict[str, int]:
    try:
        lines = payload.decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise AuditError("formula is not ASCII") from exc
    header: tuple[int, int] | None = None
    clause_size = 0
    clauses = 0
    comments = 0
    empty = 0
    literals = 0
    maximum_clause = 0
    maximum_variable = 0
    for line in lines:
        stripped = line.strip()
        if not stripped:
            raise AuditError("blank formula line")
        if stripped.startswith("c"):
            if clause_size:
                raise AuditError("comment splits a formula clause")
            comments += 1
            continue
        fields = stripped.split()
        if fields[0] == "p":
            if header is not None or clauses or clause_size:
                raise AuditError("duplicate or misplaced formula header")
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise AuditError("malformed formula header")
            header = (int(fields[2]), int(fields[3]))
            continue
        if header is None:
            raise AuditError("formula clause precedes header")
        for token in fields:
            if re.fullmatch(r"(?:0|-[1-9][0-9]*|[1-9][0-9]*)", token) is None:
                raise AuditError(f"malformed formula token: {token!r}")
            literal = int(token)
            if literal == 0:
                clauses += 1
                if clause_size == 0:
                    empty += 1
                maximum_clause = max(maximum_clause, clause_size)
                clause_size = 0
                continue
            variable = abs(literal)
            if variable > header[0]:
                raise AuditError("formula variable exceeds header")
            clause_size += 1
            literals += 1
            maximum_variable = max(maximum_variable, variable)
    if header is None or clause_size or clauses != header[1]:
        raise AuditError("incomplete or miscounted formula")
    result = {
        "clauses": clauses,
        "comments": comments,
        "empty_clauses": empty,
        "literals": literals,
        "maximum_clause_size": maximum_clause,
        "maximum_variable_observed": maximum_variable,
        "variables": header[0],
    }
    expected = {
        "clauses": 32108,
        "comments": 0,
        "empty_clauses": 0,
        "literals": 281028,
        "maximum_clause_size": 286,
        "maximum_variable_observed": 9802,
        "variables": 9802,
    }
    if result != expected:
        raise AuditError(f"unexpected formula census: {result}")
    return result


def encode_unsigned(value: int) -> bytes:
    encoded = bytearray()
    while value & ~0x7F:
        encoded.append((value & 0x7F) | 0x80)
        value >>= 7
    encoded.append(value)
    return bytes(encoded)


def independent_bdrat_census(payload: bytes) -> dict[str, int]:
    offset = 0
    records = 0
    literals = 0
    maximum_clause = 0
    maximum_variable = 0
    empty_record = 0
    while offset < len(payload):
        if payload[offset] != ord("a"):
            raise AuditError("binary proof contains a nonaddition prefix")
        offset += 1
        records += 1
        clause_size = 0
        while True:
            start = offset
            value = 0
            shift = 0
            while True:
                if offset >= len(payload):
                    raise AuditError("truncated binary proof varint")
                byte = payload[offset]
                offset += 1
                value |= (byte & 0x7F) << shift
                if byte < 0x80:
                    break
                shift += 7
                if shift > 63:
                    raise AuditError("oversized binary proof varint")
            if payload[start:offset] != encode_unsigned(value):
                raise AuditError("noncanonical binary proof varint")
            if value == 0:
                break
            variable = value >> 1
            if not 1 <= variable <= 9802:
                raise AuditError("binary proof variable is out of range")
            clause_size += 1
            literals += 1
            maximum_variable = max(maximum_variable, variable)
        maximum_clause = max(maximum_clause, clause_size)
        if clause_size == 0:
            if empty_record:
                raise AuditError("multiple empty binary proof additions")
            empty_record = records
            if offset != len(payload):
                raise AuditError("binary proof has post-empty bytes")
    result = {
        "addition_records": records,
        "deletion_records": 0,
        "empty_addition_record": empty_record,
        "empty_additions": int(empty_record != 0),
        "literals": literals,
        "maximum_clause_size": maximum_clause,
        "maximum_variable_observed": maximum_variable,
        "post_empty_records": 0,
    }
    expected = {
        "addition_records": 45281,
        "deletion_records": 0,
        "empty_addition_record": 45281,
        "empty_additions": 1,
        "literals": 410400,
        "maximum_clause_size": 284,
        "maximum_variable_observed": 9802,
        "post_empty_records": 0,
    }
    if result != expected:
        raise AuditError(f"unexpected binary proof census: {result}")
    return result


def require_process(
    command: list[str],
    *,
    cwd: Path,
    environment: Mapping[str, str],
    timeout: int,
) -> subprocess.CompletedProcess[bytes]:
    try:
        process = subprocess.run(
            command,
            cwd=cwd,
            env=dict(environment),
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise AuditError(f"process timed out: {command[0]}") from exc
    if process.returncode != 0:
        raise AuditError(
            f"process failed ({process.returncode}): {' '.join(command)}"
        )
    return process


def validate_retained_evidence(payload: bytes) -> dict[str, object]:
    value = load_json_unique(payload, RETAINED_EVIDENCE)
    if not isinstance(value, dict):
        raise AuditError("retained verifier evidence is not an object")
    if value.get("verdict") != (
        "VERIFIED_EXACT_HOLE9_CNF_UNSAT_CANDIDATE_ONLY_"
        "PENDING_HOSTILE_ACCEPTANCE"
    ):
        raise AuditError("retained evidence has the wrong claim boundary")
    hostile = value.get("hostile_mutations")
    if not isinstance(hostile, dict):
        raise AuditError("retained evidence lacks hostile mutation results")
    if hostile.get("count") != 24 or hostile.get("all_rejected") is not True:
        raise AuditError("retained evidence does not reject all 24 mutations")
    tests = hostile.get("tests")
    if not isinstance(tests, list) or len(tests) != 24:
        raise AuditError("retained hostile mutation list has the wrong size")
    if any(
        not isinstance(item, dict) or item.get("rejected") is not True
        for item in tests
    ):
        raise AuditError("a retained hostile mutation did not fail closed")
    source = value.get("source")
    if not isinstance(source, dict):
        raise AuditError("retained evidence lacks source provenance")
    if source.get("sha256") != BINDINGS[VERIFIER][1]:
        raise AuditError("retained evidence names the wrong verifier source")
    if source.get("binding_scope") != (
        "The source file was identical before and after this run. "
        "This self-observation is provenance, not authentication of "
        "already-loaded interpreter state; the external hostile review must "
        "bind these exact bytes."
    ):
        raise AuditError("retained evidence overstates source self-authentication")
    return value


def validate_tool_provenance(payload: bytes) -> dict[str, object]:
    value = load_json_unique(payload, TOOL_PROVENANCE)
    if not isinstance(value, dict):
        raise AuditError("tool-source provenance is not an object")
    clean = value.get("clean_rebuild")
    if not isinstance(clean, dict):
        raise AuditError("tool-source provenance lacks clean rebuild data")
    executables = clean.get("executables")
    expected = {
        "drat-trim": BINDINGS[DRAT_BINARY][1],
        "lrat-check": BINDINGS[LRAT_BINARY][1],
    }
    if not isinstance(executables, list):
        raise AuditError("tool-source provenance executable list is malformed")
    found = {
        item.get("name"): item.get("sha256")
        for item in executables
        if isinstance(item, dict)
    }
    if found != expected:
        raise AuditError(
            f"tool-source provenance has stale rebuild hashes: {found}"
        )
    return value


def replay_verifier_and_tests(
    retained_evidence: bytes,
) -> dict[str, object]:
    environment = dict(os.environ)
    environment["LC_ALL"] = "C"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONWARNINGS"] = "error"
    verifier = require_process(
        [
            sys.executable,
            "-B",
            "-W",
            "error",
            VERIFIER,
        ],
        cwd=ROOT,
        environment=environment,
        timeout=120,
    )
    if verifier.stderr:
        raise AuditError("complete verifier replay wrote to stderr")
    if verifier.stdout != retained_evidence:
        raise AuditError("complete verifier replay differs from retained evidence")
    tests = require_process(
        [
            sys.executable,
            "-B",
            "-W",
            "error",
            "-m",
            "unittest",
            "-v",
            "tests.test_order13_k3_hole9_certificate_verifier_b",
        ],
        cwd=ROOT,
        environment=environment,
        timeout=120,
    )
    transcript = (tests.stdout + tests.stderr).decode("utf-8", "strict")
    if "Ran 7 tests" not in transcript or not transcript.rstrip().endswith("OK"):
        raise AuditError("focused test transcript has an unexpected shape")
    return {
        "complete_verifier_evidence_byte_identical": True,
        "complete_verifier_exit_code": verifier.returncode,
        "complete_verifier_stderr_empty": True,
        "focused_tests": 7,
        "focused_tests_exit_code": tests.returncode,
        "focused_tests_passed": True,
    }


def rebuild_and_replay_checkers(
    payloads: Mapping[str, bytes],
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(
        prefix="gamma-theta-hole9-external-code-audit-"
    ) as temporary:
        private = Path(temporary)
        os.chmod(private, 0o700)
        for name, relative in (
            ("drat-trim.c", DRAT_SOURCE),
            ("lrat-check.c", LRAT_SOURCE),
            ("instance.cnf", FORMULA),
            ("proof.normalized.bdrat", BDRAT),
            ("proof.lrat", LRAT),
        ):
            destination = private / name
            destination.write_bytes(payloads[relative])
        environment = {
            "HOME": temporary,
            "LC_ALL": "C",
            "PATH": "/usr/bin:/bin",
            "TMPDIR": temporary,
        }
        drat_compile = require_process(
            [
                "/usr/bin/cc",
                "drat-trim.c",
                "-std=c99",
                "-O2",
                "-o",
                "drat-trim",
            ],
            cwd=private,
            environment=environment,
            timeout=60,
        )
        lrat_compile = require_process(
            [
                "/usr/bin/cc",
                "lrat-check.c",
                "-std=c99",
                "-DLONGTYPE",
                "-O2",
                "-o",
                "lrat-check",
            ],
            cwd=private,
            environment=environment,
            timeout=60,
        )
        if drat_compile.stderr or lrat_compile.stderr:
            raise AuditError("clean checker compilation wrote to stderr")
        rebuilt_drat = (private / "drat-trim").read_bytes()
        rebuilt_lrat = (private / "lrat-check").read_bytes()
        if sha256(rebuilt_drat) != BINDINGS[DRAT_BINARY][1]:
            raise AuditError("clean drat-trim build differs from retained binary")
        if sha256(rebuilt_lrat) != BINDINGS[LRAT_BINARY][1]:
            raise AuditError("clean lrat-check build differs from retained binary")
        drat = require_process(
            [
                str(private / "drat-trim"),
                "instance.cnf",
                "proof.normalized.bdrat",
                "-i",
                "-f",
                "-W",
                "-U",
                "-t",
                "1800",
            ],
            cwd=private,
            environment=environment,
            timeout=120,
        )
        if drat.stderr:
            raise AuditError("rebuilt drat-trim wrote to stderr")
        drat_lines = [
            line.strip()
            for line in drat.stdout.decode("ascii").replace("\r", "").splitlines()
            if line.strip()
        ]
        if drat_lines.count("s VERIFIED") != 1:
            raise AuditError("rebuilt drat-trim lacks a unique VERIFIED marker")
        if (
            "c 0 RAT lemmas in core; 0 redundant literals in core lemmas"
            not in drat_lines
        ):
            raise AuditError("rebuilt drat-trim did not report a zero-RAT core")
        if any("WARNING" in line for line in drat_lines):
            raise AuditError("rebuilt drat-trim emitted a warning")
        lrat = require_process(
            [
                str(private / "lrat-check"),
                "instance.cnf",
                "proof.lrat",
            ],
            cwd=private,
            environment=environment,
            timeout=120,
        )
        if lrat.stderr:
            raise AuditError("rebuilt lrat-check wrote to stderr")
        lrat_lines = [
            line.strip()
            for line in lrat.stdout.decode("ascii").replace("\r", "").splitlines()
            if line.strip()
        ]
        if lrat_lines.count("c VERIFIED") != 1:
            raise AuditError("rebuilt lrat-check lacks a unique VERIFIED marker")
        expected_total = (
            "c Added clauses = 57299.  Deleted clauses = 57168.  "
            "Max live clauses = 32108"
        )
        if expected_total not in lrat_lines:
            raise AuditError("rebuilt lrat-check has unexpected clause totals")
        return {
            "compiler": "Apple clang version 21.0.0 (clang-2100.1.1.101)",
            "drat_trim": {
                "clean_build_matches_retained_executable": True,
                "exit_code": drat.returncode,
                "marker": "s VERIFIED",
                "sha256": sha256(rebuilt_drat),
                "stderr_empty": True,
                "zero_rat_lemmas_in_core": True,
            },
            "lrat_check": {
                "clean_build_matches_retained_executable": True,
                "exit_code": lrat.returncode,
                "marker": "c VERIFIED",
                "sha256": sha256(rebuilt_lrat),
                "stderr_empty": True,
            },
            "target": "arm64-apple-darwin25.5.0",
        }


def replay() -> dict[str, object]:
    payloads = bind_inputs()
    retained = validate_retained_evidence(payloads[RETAINED_EVIDENCE])
    validate_tool_provenance(payloads[TOOL_PROVENANCE])
    formula = independent_dimacs_census(payloads[FORMULA])
    proof = independent_bdrat_census(payloads[BDRAT])
    runtime = replay_verifier_and_tests(payloads[RETAINED_EVIDENCE])
    source_build = rebuild_and_replay_checkers(payloads)
    hostile = retained["hostile_mutations"]
    assert isinstance(hostile, dict)
    return {
        "bindings_verified": len(BINDINGS),
        "candidate_only": True,
        "checker_source_build_and_replay": source_build,
        "claim_boundary":
            "Exact SHA-256-bound hole9 CNF UNSAT only; no order-13-wide "
            "or universal gamma-theta claim.",
        "formula_census": formula,
        "hostile_mutations_rejected": hostile["count"],
        "normalized_binary_proof_census": proof,
        "runtime_replay": runtime,
        "schema": SCHEMA,
        "schema_version": 1,
        "verdict": VERDICT,
    }


def main() -> int:
    try:
        result = replay()
    except (AuditError, OSError, ValueError) as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
