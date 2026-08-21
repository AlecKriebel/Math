#!/usr/bin/env python3
"""Standalone recovery/auditor for the hole7 full-bank DRAT proof.

This program uses only the Python standard library.  It deliberately imports
neither the synthesis/search code nor the author proof wrapper.  It binds the
immutable source CNF and run, strictly parses the ASCII DRAT proof, removes
only syntactically valid deletion records, and accepts the addition-only proof
only after warning-fatal, RUP-only forward replay by the pinned checker.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Mapping, Sequence


SCHEMA = "gamma-theta-hole7-addition-only-recovery-v1"
ORDER = 12
VARIABLE_COUNT = 6886
CLAUSE_COUNT = 21718
EXPECTED_HEAD = "2e68a6396735381ee634a572dda409610b40891f"
EXPECTED_CNF_SHA256 = (
    "6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7"
)
EXPECTED_BANK_SHA256 = (
    "371ab3b01ce2add1138e0c0c78d267a796bcc536c79f95050face4bfcd4d11a7"
)
EXPECTED_PACKAGE_MANIFEST_SHA256 = (
    "7c46b015dd58e321428c7d0bb8b896d27ae8ce0fb4bc9566199e43f86fa17185"
)
EXPECTED_ORIGINAL_PROOF_SHA256 = (
    "7ceb4a63d393d8ff6fec33569c6284fee61533be4f15fd733777b85b08ee2b85"
)
EXPECTED_ORIGINAL_PROOF_SIZE = 35_285_574
EXPECTED_RUN_CONFIG_SHA256 = (
    "8cce1b89c3381e6b685b4d351c22b9edf2aaa17b42d1374631e878f323472dc9"
)
EXPECTED_OUTCOME_SHA256 = (
    "ffb19de770a003341b7050941531fca845626fe4cd086b727287122c57d510ff"
)
EXPECTED_SOLVER_RESULT_SHA256 = (
    "bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162"
)
EXPECTED_ORIGINAL_CHECKER_STDOUT_SHA256 = (
    "1d4d2e1f99c505742e9d1c698983257816b5be474aa423aa3fb4a1c81ab508ca"
)
EXPECTED_EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)
EXPECTED_CHECKER_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
EXPECTED_CHECKER_SOURCE_SHA256 = (
    "f7619bdc338bc8151b2f6bb87488052795c926b048d5040cf165742eb1ba9a26"
)
CHECKER_FLAGS = ("-I", "-f", "-W", "-U", "-t", "600")
DIAGNOSTIC_FLAGS = ("-I", "-f", "-W", "-v", "-t", "600")
PROOF_RELATIVE = Path("proof/addition-only.rup.drat")
CHECKER_STDOUT_RELATIVE = Path("checker/strict.stdout")
CHECKER_STDERR_RELATIVE = Path("checker/strict.stderr")
DIAGNOSTIC_STDOUT_RELATIVE = Path("checker/original-warning.stdout")
DIAGNOSTIC_STDERR_RELATIVE = Path("checker/original-warning.stderr")
REPRO_RELATIVE = Path("repro/hole7_deletion_strip_auditor.py")
SOUNDNESS_RELATIVE = Path("SOUNDNESS.md")
CERTIFICATE_RELATIVE = Path("certificate.json")


class AuditFailure(ValueError):
    """A malformed or incorrectly bound artifact."""


@dataclass(frozen=True)
class ProofStats:
    byte_count: int
    line_count: int
    addition_count: int
    deletion_count: int
    addition_literal_count: int
    deletion_literal_count: int
    maximum_variable: int
    maximum_clause_length: int
    empty_addition_count: int
    final_empty_line: int
    first_deletion_line: int | None
    proof_sha256: str
    addition_stream_sha256: str
    deletion_stream_sha256: str
    addition_stream_size_bytes: int
    deletion_stream_size_bytes: int


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def campaign_root() -> Path:
    source = Path(__file__).resolve()
    for ancestor in source.parents:
        if (
            (ancestor / "results/synthesis_k3_template_bank_packages/hole7").is_dir()
            and (ancestor / "tools/drat_trim_2023_05_22/drat-trim").is_file()
        ):
            return ancestor
    raise AuditFailure("cannot locate campaign root from auditor path")


def source_paths() -> dict[str, Path]:
    root = campaign_root()
    run = root / "results/synthesis_k3_template_bank_runs/hole7_seed0_600s"
    package = root / "results/synthesis_k3_template_bank_packages/hole7"
    return {
        "cnf": package / "instance.cnf",
        "bank": package / "coloring_bank.json",
        "package_manifest": package / "manifest.json",
        "proof": run / "proof.drat",
        "run_config": run / "run_config.json",
        "outcome": run / "outcome.json",
        "solver_result": run / "solver.result",
        "solver_stdout": run / "solver.stdout",
        "solver_stderr": run / "solver.stderr",
        "original_checker_stdout": run / "checker.stdout",
        "original_checker_stderr": run / "checker.stderr",
        "checker": root / "tools/drat_trim_2023_05_22/drat-trim",
        "checker_source": root
        / "tools/drat_trim_2023_05_22/drat-trim.c",
    }


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _strict_json_bytes(payload: bytes, role: str) -> object:
    def reject_constant(token: str) -> object:
        raise AuditFailure(f"{role}: non-finite JSON constant {token!r}")

    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"{role}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AuditFailure(f"{role}: JSON is not UTF-8") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise AuditFailure(f"{role}: malformed JSON") from error


def _assert_no_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        try:
            information = os.lstat(current)
        except FileNotFoundError:
            break
        require(
            not stat.S_ISLNK(information.st_mode),
            f"symlinked path component: {current}",
        )


def _assert_regular_single_link(path: Path, role: str) -> None:
    _assert_no_symlink_components(path)
    try:
        information = os.lstat(path)
    except FileNotFoundError as error:
        raise AuditFailure(f"{role} is missing: {path}") from error
    require(stat.S_ISREG(information.st_mode), f"{role} is not a regular file")
    require(information.st_nlink == 1, f"{role} has multiple hard links")


def _artifact_record(path: Path, root: Path) -> dict[str, object]:
    _assert_regular_single_link(path, str(path))
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _parse_literal(token: bytes, line_number: int) -> int:
    require(token != b"", f"proof line {line_number}: empty token")
    negative = token.startswith(b"-")
    digits = token[1:] if negative else token
    require(
        digits
        and all(48 <= byte <= 57 for byte in digits)
        and digits[0] != 48,
        f"proof line {line_number}: noncanonical integer token",
    )
    value = int(token)
    require(
        1 <= abs(value) <= VARIABLE_COUNT,
        f"proof line {line_number}: variable outside 1..{VARIABLE_COUNT}",
    )
    return value


def parse_proof_stream(
    source: BinaryIO,
    *,
    addition_sink: BinaryIO | None = None,
    allow_deletions: bool,
) -> ProofStats:
    """Strictly parse canonical ASCII DRAT and optionally emit additions."""

    proof_digest = hashlib.sha256()
    addition_digest = hashlib.sha256()
    deletion_digest = hashlib.sha256()
    byte_count = 0
    line_count = 0
    addition_count = 0
    deletion_count = 0
    addition_literals = 0
    deletion_literals = 0
    maximum_variable = 0
    maximum_clause_length = 0
    empty_additions = 0
    final_empty_line = 0
    first_deletion_line: int | None = None
    addition_bytes = 0
    deletion_bytes = 0
    seen_empty = False

    for raw in source:
        line_count += 1
        byte_count += len(raw)
        proof_digest.update(raw)
        require(raw.endswith(b"\n"), f"proof line {line_count}: missing LF")
        require(
            b"\r" not in raw and b"\x00" not in raw,
            f"proof line {line_count}: forbidden control byte",
        )
        require(
            len(raw) <= 16 << 20,
            f"proof line {line_count}: unreasonable length",
        )
        require(not seen_empty, "proof continues after the empty addition")

        body = raw[:-1]
        deletion = body.startswith(b"d ")
        if deletion:
            require(allow_deletions, f"proof line {line_count}: deletion forbidden")
            payload = body[2:]
        else:
            require(
                not body.startswith((b"c", b"d")),
                f"proof line {line_count}: unsupported prefix",
            )
            payload = body

        tokens = payload.split(b" ")
        require(
            tokens and all(token != b"" for token in tokens),
            f"proof line {line_count}: noncanonical spacing",
        )
        require(tokens[-1] == b"0", f"proof line {line_count}: missing terminal 0")
        literal_tokens = tokens[:-1]
        if deletion:
            require(literal_tokens, f"proof line {line_count}: empty deletion")

        literals = tuple(
            _parse_literal(token, line_count) for token in literal_tokens
        )
        require(
            len(set(literals)) == len(literals),
            f"proof line {line_count}: duplicate literal",
        )
        literal_set = set(literals)
        require(
            not any(-literal in literal_set for literal in literals),
            f"proof line {line_count}: tautological clause",
        )
        if literals:
            maximum_variable = max(
                maximum_variable, max(abs(literal) for literal in literals)
            )
        maximum_clause_length = max(maximum_clause_length, len(literals))

        if deletion:
            deletion_count += 1
            deletion_literals += len(literals)
            deletion_digest.update(raw)
            deletion_bytes += len(raw)
            if first_deletion_line is None:
                first_deletion_line = line_count
        else:
            addition_count += 1
            addition_literals += len(literals)
            addition_digest.update(raw)
            addition_bytes += len(raw)
            if addition_sink is not None:
                addition_sink.write(raw)
            if not literals:
                empty_additions += 1
                final_empty_line = line_count
                seen_empty = True

    require(byte_count > 0, "proof is empty")
    require(empty_additions == 1, "proof needs exactly one empty addition")
    require(final_empty_line == line_count, "empty addition is not final")
    return ProofStats(
        byte_count=byte_count,
        line_count=line_count,
        addition_count=addition_count,
        deletion_count=deletion_count,
        addition_literal_count=addition_literals,
        deletion_literal_count=deletion_literals,
        maximum_variable=maximum_variable,
        maximum_clause_length=maximum_clause_length,
        empty_addition_count=empty_additions,
        final_empty_line=final_empty_line,
        first_deletion_line=first_deletion_line,
        proof_sha256=proof_digest.hexdigest(),
        addition_stream_sha256=addition_digest.hexdigest(),
        deletion_stream_sha256=deletion_digest.hexdigest(),
        addition_stream_size_bytes=addition_bytes,
        deletion_stream_size_bytes=deletion_bytes,
    )


def parse_proof_file(
    path: Path,
    *,
    addition_output: Path | None = None,
    allow_deletions: bool,
) -> ProofStats:
    _assert_regular_single_link(path, "proof")
    before = (path.stat().st_size, sha256_file(path))
    if addition_output is None:
        with path.open("rb") as source:
            result = parse_proof_stream(
                source, allow_deletions=allow_deletions
            )
    else:
        require(not addition_output.exists(), "addition output already exists")
        addition_output.parent.mkdir(parents=True, exist_ok=True)
        with path.open("rb") as source, addition_output.open("xb") as sink:
            result = parse_proof_stream(
                source,
                addition_sink=sink,
                allow_deletions=allow_deletions,
            )
            sink.flush()
            os.fsync(sink.fileno())
    after = (path.stat().st_size, sha256_file(path))
    require(before == after, "source proof changed during parsing")
    require(
        result.byte_count == before[0] and result.proof_sha256 == before[1],
        "streaming proof digest differs from file binding",
    )
    return result


def parse_cnf(path: Path) -> dict[str, object]:
    _assert_regular_single_link(path, "CNF")
    payload = path.read_bytes()
    require(sha256_bytes(payload) == EXPECTED_CNF_SHA256, "CNF SHA-256 mismatch")
    require(
        payload.endswith(b"\n") and b"\r" not in payload and b"\x00" not in payload,
        "CNF framing is invalid",
    )
    lines = payload.splitlines()
    require(
        lines and lines[0] == b"p cnf 6886 21718",
        "CNF header is not the bound formula",
    )
    require(len(lines) == CLAUSE_COUNT + 1, "CNF clause-line count mismatch")
    literal_count = 0
    for line_number, line in enumerate(lines[1:], 2):
        tokens = line.split(b" ")
        require(
            tokens and all(token != b"" for token in tokens) and tokens[-1] == b"0",
            f"CNF line {line_number}: malformed clause",
        )
        literals = tuple(
            _parse_literal(token, line_number) for token in tokens[:-1]
        )
        require(literals, f"CNF line {line_number}: unexpected empty clause")
        require(
            len(set(literals)) == len(literals)
            and not any(-literal in literals for literal in literals),
            f"CNF line {line_number}: duplicate or tautology",
        )
        literal_count += len(literals)
    require(literal_count == 148_551, "CNF literal count mismatch")
    return {
        "sha256": EXPECTED_CNF_SHA256,
        "size_bytes": len(payload),
        "variable_count": VARIABLE_COUNT,
        "clause_count": CLAUSE_COUNT,
        "literal_count": literal_count,
    }


def audit_immutable_sources() -> dict[str, object]:
    paths = source_paths()
    expected = {
        "cnf": EXPECTED_CNF_SHA256,
        "bank": EXPECTED_BANK_SHA256,
        "package_manifest": EXPECTED_PACKAGE_MANIFEST_SHA256,
        "proof": EXPECTED_ORIGINAL_PROOF_SHA256,
        "run_config": EXPECTED_RUN_CONFIG_SHA256,
        "outcome": EXPECTED_OUTCOME_SHA256,
        "solver_result": EXPECTED_SOLVER_RESULT_SHA256,
        "solver_stdout": EXPECTED_EMPTY_SHA256,
        "solver_stderr": EXPECTED_EMPTY_SHA256,
        "original_checker_stdout": EXPECTED_ORIGINAL_CHECKER_STDOUT_SHA256,
        "original_checker_stderr": EXPECTED_EMPTY_SHA256,
        "checker": EXPECTED_CHECKER_SHA256,
        "checker_source": EXPECTED_CHECKER_SOURCE_SHA256,
    }
    records: dict[str, dict[str, object]] = {}
    for role, digest in expected.items():
        path = paths[role]
        _assert_regular_single_link(path, role)
        actual = sha256_file(path)
        require(actual == digest, f"{role} SHA-256 mismatch")
        records[role] = {
            "path": path.relative_to(campaign_root()).as_posix(),
            "sha256": actual,
            "size_bytes": path.stat().st_size,
        }
    require(
        records["proof"]["size_bytes"] == EXPECTED_ORIGINAL_PROOF_SIZE,
        "original proof size mismatch",
    )
    require(
        paths["solver_result"].read_bytes() == b"s UNSATISFIABLE\n",
        "solver result does not say UNSATISFIABLE",
    )
    run_config = _strict_json_bytes(
        paths["run_config"].read_bytes(), "run config"
    )
    outcome = _strict_json_bytes(paths["outcome"].read_bytes(), "outcome")
    require(isinstance(run_config, dict), "run config is not an object")
    require(isinstance(outcome, dict), "outcome is not an object")
    package = run_config.get("package")
    git_binding = run_config.get("git_source_binding")
    require(
        isinstance(package, dict)
        and package.get("cnf_sha256") == EXPECTED_CNF_SHA256
        and package.get("bank_sha256") == EXPECTED_BANK_SHA256
        and package.get("manifest_sha256") == EXPECTED_PACKAGE_MANIFEST_SHA256,
        "run config package binding is wrong",
    )
    require(
        isinstance(git_binding, dict)
        and git_binding.get("head_commit") == EXPECTED_HEAD
        and git_binding.get("runtime_sources_match_head") is True
        and git_binding.get("runtime_source_mismatches") == [],
        "run config source binding is wrong",
    )
    solver = outcome.get("solver")
    checker = outcome.get("checker")
    artifacts = outcome.get("artifacts")
    require(
        outcome.get("cnf_sha256") == EXPECTED_CNF_SHA256
        and outcome.get("run_config_sha256") == EXPECTED_RUN_CONFIG_SHA256
        and outcome.get("package_manifest_sha256")
        == EXPECTED_PACKAGE_MANIFEST_SHA256,
        "outcome input binding is wrong",
    )
    require(
        outcome.get("status") == "UNSAT_UNVERIFIED_CHECKER_EXIT"
        and outcome.get("claim_status") == "NO_MATHEMATICAL_CLAIM",
        "source outcome improperly claims proof verification",
    )
    require(
        isinstance(solver, dict)
        and solver.get("exit_code") == 20
        and solver.get("timed_out") is False
        and solver.get("memory_limit_exceeded") is False
        and solver.get("termination_signal") is None,
        "solver control record is inconsistent",
    )
    require(
        isinstance(checker, dict)
        and checker.get("exit_code") == 80
        and checker.get("timed_out") is False
        and checker.get("memory_limit_exceeded") is False
        and checker.get("termination_signal") is None,
        "original checker record is inconsistent",
    )
    require(
        isinstance(artifacts, dict)
        and artifacts.get("proof.drat", {}).get("sha256")
        == EXPECTED_ORIGINAL_PROOF_SHA256,
        "outcome proof binding is wrong",
    )
    require(
        paths["original_checker_stdout"].read_bytes()
        == (
            b"\rc parsing input formula with 6886 variables and 21718 clauses\n"
            b"\rc finished parsing\n"
            b"\rc start forward verification\n"
        ),
        "original checker stdout differs from the bound exit-80 prefix",
    )
    return {
        "records": records,
        "run_status": outcome["status"],
        "claim_status": outcome["claim_status"],
        "solver_exit_code": solver["exit_code"],
        "solver_wall_seconds": solver["wall_seconds"],
        "original_checker_exit_code": checker["exit_code"],
    }


def diagnose_original_warning() -> tuple[dict[str, object], bytes, bytes]:
    paths = source_paths()
    source_payload = paths["checker_source"].read_bytes()
    require(
        sha256_bytes(source_payload) == EXPECTED_CHECKER_SOURCE_SHA256,
        "checker source hash mismatch",
    )
    source_lines = source_payload.decode("utf-8").splitlines()
    require(
        source_lines[53].strip() == "#define HARDWARNING\t 80",
        "checker HARDWARNING definition differs",
    )
    require(
        "ignore pseudo unit clause deletion" in source_lines[807]
        and "WARNING: ignoring deletion instruction" in source_lines[809]
        and "exit (HARDWARNING)" in source_lines[810]
        and "S.warning    = HARDWARNING" in source_lines[1408],
        "checker warning-control source lines differ",
    )
    with paths["proof"].open("rb") as handle:
        proof_lines = handle.readlines()
    require(
        proof_lines[2373] == b"-741 0\n"
        and proof_lines[2374] == b"d -741 -1 -12 -17 0\n",
        "bound warning-trigger proof lines differ",
    )

    checker_before = sha256_file(paths["checker"])
    cnf_before = sha256_file(paths["cnf"])
    proof_before = sha256_file(paths["proof"])
    command = (
        str(paths["checker"].resolve()),
        str(paths["cnf"].resolve()),
        str(paths["proof"].resolve()),
        *DIAGNOSTIC_FLAGS,
    )
    completed = subprocess.run(
        command,
        cwd=campaign_root(),
        env={"LC_ALL": "C", "PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=620,
        check=False,
    )
    normalized = completed.stdout.replace(b"\r", b"\n")
    warning = (
        b"c WARNING: ignoring deletion instruction 90747: "
        b"[8166] -741 -17 -12 -1 0"
    )
    require(completed.returncode == 80, "warning diagnostic did not exit 80")
    require(warning in normalized, "warning diagnostic text differs")
    require(b"s VERIFIED" not in normalized, "exit-80 diagnostic claims VERIFIED")
    require(completed.stderr == b"", "warning diagnostic wrote stderr")
    require(
        sha256_file(paths["checker"]) == checker_before
        and sha256_file(paths["cnf"]) == cnf_before
        and sha256_file(paths["proof"]) == proof_before,
        "source artifact changed during warning diagnostic",
    )
    return (
        {
            "normalized_command": [
                "$CHECKER",
                "$CNF",
                "$ORIGINAL_PROOF",
                *DIAGNOSTIC_FLAGS,
            ],
            "command_flags": list(DIAGNOSTIC_FLAGS),
            "exit_code": completed.returncode,
            "checker_sha256": checker_before,
            "checker_source_sha256": EXPECTED_CHECKER_SOURCE_SHA256,
            "cnf_sha256": cnf_before,
            "original_proof_sha256": proof_before,
            "stdout_sha256": sha256_bytes(completed.stdout),
            "stderr_sha256": sha256_bytes(completed.stderr),
            "first_trigger": {
                "unit_addition_proof_line": 2374,
                "unit_addition": "-741 0",
                "deletion_proof_line": 2375,
                "deletion": "d -741 -1 -12 -17 0",
                "checker_internal_instruction": 90747,
                "checker_internal_clause": "[8166] -741 -17 -12 -1 0",
            },
            "source_mechanism": {
                "hardwarning_value": 80,
                "hardwarning_definition_line": 54,
                "pseudo_unit_deletion_comment_line": 808,
                "warning_print_line": 810,
                "hardwarning_exit_line": 811,
                "W_option_assignment_line": 1409,
                "meaning": (
                    "forward verification preserves the pseudo-unit reason "
                    "clause and ignores its deletion; -W makes that ignored "
                    "optimization instruction fatal"
                ),
            },
        },
        completed.stdout,
        completed.stderr,
    )


def _checker_verified(stdout: bytes, stderr: bytes) -> dict[str, object]:
    combined = stdout + b"\n" + stderr
    require(b"warning" not in combined.lower(), "strict checker emitted a warning")
    normalized = stdout.replace(b"\r", b"\n")
    verified_count = sum(
        line.strip() == b"s VERIFIED" for line in normalized.splitlines()
    )
    require(verified_count == 1, "strict checker lacks exactly one s VERIFIED")
    require(
        b"RAT lemmas in core" in normalized
        and b"0 RAT lemmas in core" in normalized,
        "strict checker did not report zero RAT lemmas in core",
    )
    return {
        "verified_line_count": verified_count,
        "warning_free": True,
        "zero_rat_lemmas_in_core": True,
    }


def run_strict_checker(
    cnf: Path, proof: Path, checker: Path
) -> tuple[dict[str, object], bytes, bytes]:
    cnf_before = (cnf.stat().st_size, sha256_file(cnf))
    proof_before = (proof.stat().st_size, sha256_file(proof))
    checker_before = sha256_file(checker)
    require(checker_before == EXPECTED_CHECKER_SHA256, "checker hash mismatch")
    command = (str(checker.resolve()), str(cnf.resolve()), str(proof.resolve()), *CHECKER_FLAGS)
    completed = subprocess.run(
        command,
        cwd=campaign_root(),
        env={
            "LC_ALL": "C",
            "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        },
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=620,
        check=False,
    )
    require(completed.returncode == 0, f"strict checker exit {completed.returncode}")
    semantic = _checker_verified(completed.stdout, completed.stderr)
    require(
        (cnf.stat().st_size, sha256_file(cnf)) == cnf_before,
        "CNF changed during strict replay",
    )
    require(
        (proof.stat().st_size, sha256_file(proof)) == proof_before,
        "addition-only proof changed during strict replay",
    )
    require(
        sha256_file(checker) == checker_before,
        "checker executable changed during replay",
    )
    record = {
        "normalized_command": [
            "$CHECKER",
            "$CNF",
            "$ADDITION_ONLY_PROOF",
            *CHECKER_FLAGS,
        ],
        "command_flags": list(CHECKER_FLAGS),
        "exit_code": completed.returncode,
        "checker_sha256_before": checker_before,
        "checker_sha256_after": sha256_file(checker),
        "cnf_sha256_before": cnf_before[1],
        "cnf_sha256_after": sha256_file(cnf),
        "proof_sha256_before": proof_before[1],
        "proof_sha256_after": sha256_file(proof),
        "stdout_sha256": sha256_bytes(completed.stdout),
        "stderr_sha256": sha256_bytes(completed.stderr),
        **semantic,
    }
    return record, completed.stdout, completed.stderr


def _safe_new_certificate(path: Path) -> Path:
    require(isinstance(path, Path), "certificate path must be a Path")
    _assert_no_symlink_components(path)
    require(not path.exists() and not path.is_symlink(), "certificate path exists")
    parent = path.parent
    _assert_no_symlink_components(parent)
    require(parent.is_dir(), "certificate parent is missing")
    resolved = path.resolve(strict=False)
    allowed = (campaign_root() / "certificates").resolve()
    try:
        resolved.relative_to(allowed)
    except ValueError as error:
        raise AuditFailure("certificate must lie below campaign certificates") from error
    require(resolved != allowed, "certificate cannot replace certificates root")
    return resolved


def _write_new(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def _proof_stats_dict(stats: ProofStats) -> dict[str, object]:
    return {
        field: getattr(stats, field)
        for field in ProofStats.__dataclass_fields__
    }


def _soundness_markdown(
    original: ProofStats,
    stripped: ProofStats,
    checker: Mapping[str, object],
    diagnostic: Mapping[str, object],
) -> bytes:
    text = f"""# Soundness of the hole7 addition-only recovery

The immutable source proof has SHA-256
`{original.proof_sha256}` and contains
{original.addition_count:,} additions and {original.deletion_count:,} deletion
records.  The recovery parser accepted only canonical ASCII DRAT records,
preserved every addition byte-for-byte and in order, and removed exactly the
deletion records.  The resulting proof has SHA-256
`{stripped.proof_sha256}` and contains {stripped.addition_count:,} additions,
no deletions, and one final empty clause.

The original wrapper's exit 80 is explained by pinned checker source lines
806--811 and 1409.  In forward mode, DRAT-trim preserves a clause currently
serving as a pseudo-unit reason and ignores a requested deletion; `-W` maps
that ignored optimization instruction to `HARDWARNING=80`.  The first trigger
is source proof line 2375, `d -741 -1 -12 -17 0`, immediately after unit
addition `-741 0`.  A retained verbose diagnostic reproduced exit
{diagnostic["exit_code"]} and the exact warning without reaching `s VERIFIED`.

Deletion records are proof-database optimization instructions, not derived
clauses.  Removing them cannot weaken reverse unit propagation: every clause
that would have been deleted remains available.  Soundness does not rest on
that observation alone.  Pinned DRAT-trim
`{checker["checker_sha256_before"]}` replayed the complete addition-only proof
against CNF `{EXPECTED_CNF_SHA256}` with `-I -f -W -U -t 600`, exited zero,
emitted exactly one warning-free `s VERIFIED`, and reported zero RAT lemmas in
the core.  Thus the retained proof is a checked RUP-only refutation of the
exact full-bank `hole7` formula.

This certificate excludes only the exact `hole7` order-12, parameter-three
template formula.  The graph-theoretic theorem additionally depends on the
separate encoding-soundness and structural-template coverage proofs.  It does
not by itself exclude `hole5`, larger orders, other parameters, or resolve the
universal gamma-theta conjecture.
"""
    return text.encode("utf-8")


def _seal_tree(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_file():
            path.chmod(0o444)
        elif path.is_dir():
            path.chmod(0o555)
    root.chmod(0o555)


def recover(output_directory: Path, validation_gate: object) -> dict[str, object]:
    require(validation_gate is True, "explicit validation gate is required")
    destination = _safe_new_certificate(output_directory)
    source_audit = audit_immutable_sources()
    cnf_record = parse_cnf(source_paths()["cnf"])
    original = parse_proof_file(
        source_paths()["proof"], allow_deletions=True
    )
    require(
        original.proof_sha256 == EXPECTED_ORIGINAL_PROOF_SHA256
        and original.byte_count == EXPECTED_ORIGINAL_PROOF_SIZE,
        "original proof binding changed",
    )
    require(original.deletion_count > 0, "source proof has no deletions to strip")

    temporary = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.partial.",
            dir=destination.parent,
        )
    )
    installed = False
    try:
        stripped_path = temporary / PROOF_RELATIVE
        emitted = parse_proof_file(
            source_paths()["proof"],
            addition_output=stripped_path,
            allow_deletions=True,
        )
        stripped = parse_proof_file(stripped_path, allow_deletions=False)
        require(
            emitted.addition_stream_sha256 == stripped.proof_sha256
            and emitted.addition_stream_size_bytes == stripped.byte_count,
            "addition-only output differs from source addition stream",
        )
        require(
            stripped.addition_count == original.addition_count
            and stripped.deletion_count == 0
            and stripped.addition_literal_count
            == original.addition_literal_count,
            "addition-only proof statistics are inconsistent",
        )

        checker_record, checker_stdout, checker_stderr = run_strict_checker(
            source_paths()["cnf"], stripped_path, source_paths()["checker"]
        )
        diagnostic_record, diagnostic_stdout, diagnostic_stderr = (
            diagnose_original_warning()
        )
        _write_new(temporary / CHECKER_STDOUT_RELATIVE, checker_stdout)
        _write_new(temporary / CHECKER_STDERR_RELATIVE, checker_stderr)
        _write_new(temporary / DIAGNOSTIC_STDOUT_RELATIVE, diagnostic_stdout)
        _write_new(temporary / DIAGNOSTIC_STDERR_RELATIVE, diagnostic_stderr)
        _write_new(temporary / REPRO_RELATIVE, Path(__file__).read_bytes())
        _write_new(
            temporary / SOUNDNESS_RELATIVE,
            _soundness_markdown(
                original, stripped, checker_record, diagnostic_record
            ),
        )
        artifact_paths = (
            temporary / PROOF_RELATIVE,
            temporary / CHECKER_STDOUT_RELATIVE,
            temporary / CHECKER_STDERR_RELATIVE,
            temporary / DIAGNOSTIC_STDOUT_RELATIVE,
            temporary / DIAGNOSTIC_STDERR_RELATIVE,
            temporary / REPRO_RELATIVE,
            temporary / SOUNDNESS_RELATIVE,
        )
        certificate = {
            "schema": SCHEMA,
            "schema_version": 1,
            "status": "VERIFIED_FINITE_CERTIFICATE",
            "claim": (
                "the exact full-bank order-12 parameter-three hole7 CNF "
                "is unsatisfiable"
            ),
            "claim_boundary": {
                "template": "hole7",
                "order": ORDER,
                "parameter": 3,
                "universal_conjecture_resolved": False,
                "hole5_addressed": False,
                "graph_theoretic_use_requires_separate_coverage_proofs": True,
            },
            "source_audit": source_audit,
            "cnf": cnf_record,
            "transformation": {
                "operation": "delete_only_lines_whose_exact_prefix_is_d_space",
                "all_additions_preserved_byte_for_byte_in_order": True,
                "original": _proof_stats_dict(original),
                "addition_only": _proof_stats_dict(stripped),
            },
            "strict_checker": checker_record,
            "original_warning_diagnostic": diagnostic_record,
            "artifacts": {
                path.relative_to(temporary).as_posix(): _artifact_record(
                    path, temporary
                )
                for path in artifact_paths
            },
            "reproduction": {
                "auditor": REPRO_RELATIVE.as_posix(),
                "audit_command": [
                    "python3",
                    REPRO_RELATIVE.as_posix(),
                    "audit",
                    "--package",
                    "$CERTIFICATE_ROOT",
                    "--replay-checker",
                ],
            },
        }
        _write_new(
            temporary / CERTIFICATE_RELATIVE,
            canonical_json_bytes(certificate),
        )
        os.rename(temporary, destination)
        installed = True
        _seal_tree(destination)
        audit = audit_certificate(destination, replay_checker=True)
        return {
            "status": "generated_and_verified",
            "certificate_directory": str(destination),
            **audit,
        }
    finally:
        if not installed and temporary.exists():
            shutil.rmtree(temporary)


def _expected_package_entries() -> set[str]:
    return {
        PROOF_RELATIVE.as_posix(),
        CHECKER_STDOUT_RELATIVE.as_posix(),
        CHECKER_STDERR_RELATIVE.as_posix(),
        DIAGNOSTIC_STDOUT_RELATIVE.as_posix(),
        DIAGNOSTIC_STDERR_RELATIVE.as_posix(),
        REPRO_RELATIVE.as_posix(),
        SOUNDNESS_RELATIVE.as_posix(),
        CERTIFICATE_RELATIVE.as_posix(),
    }


def audit_certificate(
    package_directory: Path, *, replay_checker: bool
) -> dict[str, object]:
    require(type(replay_checker) is bool, "replay_checker must be boolean")
    _assert_no_symlink_components(package_directory)
    require(package_directory.is_dir(), "certificate directory is missing")
    package = package_directory.resolve(strict=True)
    files = {
        path.relative_to(package).as_posix()
        for path in package.rglob("*")
        if path.is_file()
    }
    require(files == _expected_package_entries(), "certificate entries differ")
    for relative in files:
        _assert_regular_single_link(package / relative, relative)

    certificate_path = package / CERTIFICATE_RELATIVE
    certificate_payload = certificate_path.read_bytes()
    parsed = _strict_json_bytes(certificate_payload, "certificate")
    require(isinstance(parsed, dict), "certificate root is not an object")
    require(
        certificate_payload == canonical_json_bytes(parsed),
        "certificate JSON is not canonical",
    )
    require(
        parsed.get("schema") == SCHEMA
        and parsed.get("schema_version") == 1
        and parsed.get("status") == "VERIFIED_FINITE_CERTIFICATE",
        "certificate identity/status is wrong",
    )
    audit_immutable_sources()
    cnf_record = parse_cnf(source_paths()["cnf"])
    require(parsed.get("cnf") == cnf_record, "certificate CNF record differs")

    original = parse_proof_file(
        source_paths()["proof"], allow_deletions=True
    )
    stripped_path = package / PROOF_RELATIVE
    stripped = parse_proof_file(stripped_path, allow_deletions=False)
    transformation = parsed.get("transformation")
    require(isinstance(transformation, dict), "transformation record is missing")
    require(
        transformation.get("all_additions_preserved_byte_for_byte_in_order")
        is True
        and transformation.get("original") == _proof_stats_dict(original)
        and transformation.get("addition_only") == _proof_stats_dict(stripped)
        and original.addition_stream_sha256 == stripped.proof_sha256
        and original.addition_stream_size_bytes == stripped.byte_count,
        "certificate transformation binding is wrong",
    )

    artifacts = parsed.get("artifacts")
    require(isinstance(artifacts, dict), "artifact map is missing")
    for relative in _expected_package_entries() - {CERTIFICATE_RELATIVE.as_posix()}:
        require(
            artifacts.get(relative) == _artifact_record(package / relative, package),
            f"artifact record differs for {relative}",
        )
    require(
        (package / REPRO_RELATIVE).read_bytes() == Path(__file__).read_bytes(),
        "packaged auditor differs from installed auditor",
    )
    saved_stdout = (package / CHECKER_STDOUT_RELATIVE).read_bytes()
    saved_stderr = (package / CHECKER_STDERR_RELATIVE).read_bytes()
    saved_semantic = _checker_verified(saved_stdout, saved_stderr)
    checker_record = parsed.get("strict_checker")
    require(isinstance(checker_record, dict), "strict checker record is missing")
    require(
        checker_record.get("exit_code") == 0
        and checker_record.get("stdout_sha256") == sha256_bytes(saved_stdout)
        and checker_record.get("stderr_sha256") == sha256_bytes(saved_stderr)
        and all(checker_record.get(key) == value for key, value in saved_semantic.items()),
        "saved strict checker record differs",
    )
    diagnostic_record = parsed.get("original_warning_diagnostic")
    require(
        isinstance(diagnostic_record, dict),
        "original warning diagnostic is missing",
    )
    diagnostic_stdout = (package / DIAGNOSTIC_STDOUT_RELATIVE).read_bytes()
    diagnostic_stderr = (package / DIAGNOSTIC_STDERR_RELATIVE).read_bytes()
    require(
        diagnostic_record.get("exit_code") == 80
        and diagnostic_record.get("stdout_sha256")
        == sha256_bytes(diagnostic_stdout)
        and diagnostic_record.get("stderr_sha256")
        == sha256_bytes(diagnostic_stderr)
        and b"WARNING: ignoring deletion instruction 90747"
        in diagnostic_stdout.replace(b"\r", b"\n")
        and b"s VERIFIED" not in diagnostic_stdout.replace(b"\r", b"\n"),
        "saved warning diagnostic differs",
    )
    replayed = False
    if replay_checker:
        fresh, fresh_stdout, fresh_stderr = run_strict_checker(
            source_paths()["cnf"], stripped_path, source_paths()["checker"]
        )
        require(
            fresh_stdout == saved_stdout and fresh_stderr == saved_stderr,
            "fresh strict replay logs differ from retained logs",
        )
        for key in (
            "exit_code",
            "checker_sha256_before",
            "checker_sha256_after",
            "cnf_sha256_before",
            "cnf_sha256_after",
            "proof_sha256_before",
            "proof_sha256_after",
            "stdout_sha256",
            "stderr_sha256",
            "verified_line_count",
            "warning_free",
            "zero_rat_lemmas_in_core",
        ):
            require(fresh[key] == checker_record.get(key), f"fresh checker {key} differs")
        replayed = True
    return {
        "certificate_sha256": sha256_bytes(certificate_payload),
        "addition_only_proof_sha256": stripped.proof_sha256,
        "addition_only_proof_size_bytes": stripped.byte_count,
        "addition_count": stripped.addition_count,
        "deleted_record_count": original.deletion_count,
        "strict_checker_replayed": replayed,
        "strict_checker_warning_free": True,
        "strict_checker_rup_only": True,
    }


def self_test() -> dict[str, object]:
    valid = b"1 -2 0\nd 1 -2 0\n2 0\n0\n"
    sink = io.BytesIO()
    stats = parse_proof_stream(
        io.BytesIO(valid), addition_sink=sink, allow_deletions=True
    )
    require(
        sink.getvalue() == b"1 -2 0\n2 0\n0\n"
        and stats.addition_count == 3
        and stats.deletion_count == 1,
        "valid strip self-test failed",
    )
    parse_proof_stream(io.BytesIO(sink.getvalue()), allow_deletions=False)
    mutations = {
        "carriage_return": valid.replace(b"\n", b"\r\n", 1),
        "missing_final_lf": valid[:-1],
        "unsupported_comment": b"c comment\n" + valid,
        "empty_deletion": b"d 0\n0\n",
        "duplicate_literal": b"1 1 0\n0\n",
        "tautological_clause": b"1 -1 0\n0\n",
        "leading_zero": b"01 0\n0\n",
        "out_of_range": b"6887 0\n0\n",
        "nonfinal_empty": b"0\n1 0\n",
        "double_space": b"1  2 0\n0\n",
    }
    rejected: list[str] = []
    for name, payload in mutations.items():
        try:
            parse_proof_stream(io.BytesIO(payload), allow_deletions=True)
        except AuditFailure:
            rejected.append(name)
        else:
            raise AuditFailure(f"mutation {name} was accepted")
    return {
        "status": "PASS",
        "valid_additions": stats.addition_count,
        "valid_deletions": stats.deletion_count,
        "mutation_count": len(mutations),
        "rejected_mutations": rejected,
    }


def inspect_sources() -> dict[str, object]:
    source_audit = audit_immutable_sources()
    cnf = parse_cnf(source_paths()["cnf"])
    proof = parse_proof_file(source_paths()["proof"], allow_deletions=True)
    return {
        "status": "PASS",
        "source_audit": source_audit,
        "cnf": cnf,
        "proof": _proof_stats_dict(proof),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("self-test")
    commands.add_parser("inspect")
    recover_parser = commands.add_parser("recover")
    recover_parser.add_argument("--validation-gate-open", action="store_true")
    recover_parser.add_argument("--output", required=True, type=Path)
    audit_parser = commands.add_parser("audit")
    audit_parser.add_argument("--package", required=True, type=Path)
    audit_parser.add_argument("--replay-checker", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "self-test":
            result = self_test()
        elif arguments.command == "inspect":
            result = inspect_sources()
        elif arguments.command == "recover":
            result = recover(
                arguments.output,
                validation_gate=arguments.validation_gate_open,
            )
        else:
            result = audit_certificate(
                arguments.package,
                replay_checker=arguments.replay_checker,
            )
    except (AuditFailure, OSError, subprocess.SubprocessError) as error:
        sys.stderr.write(f"FAIL: {error}\n")
        return 1
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
