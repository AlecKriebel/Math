#!/usr/bin/env python3
"""Clean-room verifier for the frozen order-13, k=3, hole9 certificate.

Only the Python standard library and the two byte-pinned proof checkers are
used.  In particular, this module imports no constructor, search, production
runner, proof normalizer, or candidate-manifest logic.

The accepted scope is deliberately narrow: the exact frozen DIMACS instance
is UNSAT.  The source and review bindings recorded here make that fact usable
in a later integration audit, but this verifier alone makes no order-13-wide
or universal gamma-theta claim.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile
from typing import Callable, Mapping, Sequence


SCHEMA = "gamma-theta-order13-k3-hole9-certificate-verifier-b-v1"
EXPECTED_VARIABLES = 9802
EXPECTED_CLAUSES = 32108
EXPECTED_FORMULA_LITERALS = 281028
EXPECTED_FORMULA_MAX_CLAUSE = 286
EXPECTED_PROOF_RECORDS = 45281
EXPECTED_PROOF_LITERALS = 410400
EXPECTED_PROOF_MAX_CLAUSE = 284
EXPECTED_EMPTY_RECORD = 45281


@dataclass(frozen=True)
class FrozenFile:
    size_bytes: int
    sha256: str
    role: str


FROZEN_FILES: Mapping[str, FrozenFile] = {
    # Exact C-055 mathematical realization and its two-stage hostile review.
    "math/lemmas/order13_k3_synthesis_target.md": FrozenFile(
        26303,
        "7bec13620961adeaf61c60e88c8bc9366beecab7387e40c80083fe702484ab39",
        "C-055 exact graph-to-CNF realization theorem",
    ),
    "reviews/order13_k3_math_hostile/REVIEW.md": FrozenFile(
        15021,
        "284ec751a215e499de2adfa2f2b377d1a700a27a8b3e96964067c53f652698d8",
        "original hostile mathematical review",
    ),
    "reviews/order13_k3_math_hostile/evidence.json": FrozenFile(
        20660,
        "8c1f5b3fe4511a4d19efdc224a7ea6b10b38eac06275ddce615bd73949d22af1",
        "original hostile mathematical evidence",
    ),
    "reviews/order13_k3_math_hostile/audit.py": FrozenFile(
        47177,
        "35d405424127c1a28742ade277fd5c5add0a109749ccc51ab6d622740371241b",
        "original hostile mathematical audit",
    ),
    "reviews/order13_k3_math_hostile/ADDENDUM.md": FrozenFile(
        2415,
        "42fbc74ad916757a35df8bf5cbc6c4ab5205ae5f5d34abf915cff6bbb2203bd7",
        "revised-byte mathematical acceptance",
    ),
    "reviews/order13_k3_math_hostile/addendum_evidence.json": FrozenFile(
        3456,
        "e45d99d880af6350034d7ee9a4b83acb30cc4706c9aa4445d97a07a272d3dc14",
        "revised-byte mathematical acceptance evidence",
    ),
    "reviews/order13_k3_math_hostile/addendum_audit.py": FrozenFile(
        12336,
        "51f070e3ecb653a3381603a09f78e5ce43540eac49a3d95e0ec106e789ea8cc2",
        "revised-byte mathematical acceptance audit",
    ),
    # Constructor acceptance and the exact live-hole9 preflight.
    "reviews/order13_k3_constructor_acceptance/REVIEW.md": FrozenFile(
        6905,
        "7d05355fdc92db4ccbb4a6254934015ddc89f216392fad341cff0bdb82f5e428",
        "constructor integration review",
    ),
    "reviews/order13_k3_constructor_acceptance/evidence.json": FrozenFile(
        7248,
        "8318d036867da89c2b2b7b9599bde17f50e160731d21243584609d34a515ec74",
        "constructor integration evidence",
    ),
    "reviews/order13_k3_constructor_acceptance/audit.py": FrozenFile(
        37091,
        "cd421fb8c58035c2fdfad84811c2922e702c1dbe24d7d7d791242ed85721d0a6",
        "constructor integration audit",
    ),
    "reviews/order13_k3_hole9_preflight_constructor/REVIEW.md": FrozenFile(
        4352,
        "70e870564eca1c2ccb53f4db8607c52218e237637ec54ad183f442f5fc8e2548",
        "exact live-hole9 package review",
    ),
    "reviews/order13_k3_hole9_preflight_constructor/evidence.json": FrozenFile(
        2183,
        "2687e1f893f85b64c83fdfe86cfcbd2eb7670a3307cc23f0cc999c999a422de9",
        "exact live-hole9 package evidence",
    ),
    "reviews/order13_k3_hole9_preflight_constructor/audit.py": FrozenFile(
        15394,
        "53c9153d5c89408db7bd5705589ef7bffec67d0205d290ef9fc0f7f6a8530e79",
        "exact live-hole9 package audit",
    ),
    "instances/order13_k3_hole9/instance.cnf": FrozenFile(
        1168197,
        "3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea",
        "accepted constructor formula",
    ),
    "instances/order13_k3_hole9/constructor-manifest.json": FrozenFile(
        5408,
        "8f55019121df7280368528c1b7c0808d3cc06e7bd0f871be516057763c87ad5b",
        "accepted constructor manifest",
    ),
    "instances/order13_k3_hole9/coloring-bank.json": FrozenFile(
        227208,
        "a0f47a0aaa3be4659ce483f27a963d351f3a13424cac6a6a99ef6ac9e0c872f1",
        "complete coloring obstruction bank",
    ),
    # Decisive certificate bytes.  The candidate manifest is provenance only.
    "certificates/order13_k3_hole9_attempt000001_lrat/instance.cnf": FrozenFile(
        1168197,
        "3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea",
        "certificate formula",
    ),
    "certificates/order13_k3_hole9_attempt000001_lrat/proof.normalized.bdrat": FrozenFile(
        742337,
        "af216ef2d7698db2b1d1c55411bc05025bfe25f10c16f2e85c5301f7a88bdd5f",
        "addition-only binary RUP proof",
    ),
    "certificates/order13_k3_hole9_attempt000001_lrat/proof.lrat": FrozenFile(
        8546664,
        "f6ef614f2acee4cf43aa3b75372b354912c50248a13c3f863479cdc49b061805",
        "independent LRAT certificate",
    ),
    "certificates/order13_k3_hole9_attempt000001_lrat/candidate-manifest.json": FrozenFile(
        6953,
        "2c27a98e6a3a4ca66fdfedac4c3ae6839b11d0008ed63a1d8999b24c3f917fa1",
        "untrusted metadata retained only for provenance",
    ),
    "certificates/order13_k3_hole9_attempt000001_lrat/README.md": FrozenFile(
        2915,
        "456d100f2bff91084f7eb6d89ed7c62255caf4abe40c6bc40c63930e75f29c53",
        "corrected candidate claim boundary and proof census",
    ),
    # Independently invoked proof checkers.
    "tools/drat_trim_2023_05_22/drat-trim": FrozenFile(
        70088,
        "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb",
        "pinned warning-fatal RUP checker",
    ),
    "tools/drat_trim_2023_05_22/lrat-check": FrozenFile(
        36520,
        "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2",
        "pinned LRAT checker",
    ),
}

CANDIDATE_FORMULA = (
    "certificates/order13_k3_hole9_attempt000001_lrat/instance.cnf"
)
CONSTRUCTOR_FORMULA = "instances/order13_k3_hole9/instance.cnf"
NORMALIZED_PROOF = (
    "certificates/order13_k3_hole9_attempt000001_lrat/"
    "proof.normalized.bdrat"
)
LRAT_PROOF = "certificates/order13_k3_hole9_attempt000001_lrat/proof.lrat"
DRAT_TRIM = "tools/drat_trim_2023_05_22/drat-trim"
LRAT_CHECK = "tools/drat_trim_2023_05_22/lrat-check"


class VerificationError(RuntimeError):
    """A binding, parser, checker, or hostile-test condition failed closed."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
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


def _read_regular_file(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise VerificationError(f"cannot open regular file {path}: {exc}") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise VerificationError(f"not a regular file: {path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    before_key = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )
    after_key = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    )
    if before_key != after_key:
        raise VerificationError(f"file changed while read: {path}")
    return b"".join(chunks)


def _bind_one(relative: str, expected: FrozenFile, root: Path) -> bytes:
    path = root / relative
    payload = _read_regular_file(path)
    if len(payload) != expected.size_bytes:
        raise VerificationError(
            f"size mismatch for {relative}: {len(payload)} != "
            f"{expected.size_bytes}"
        )
    actual = sha256_bytes(payload)
    if actual != expected.sha256:
        raise VerificationError(
            f"SHA-256 mismatch for {relative}: {actual} != {expected.sha256}"
        )
    if relative in (DRAT_TRIM, LRAT_CHECK):
        mode = os.stat(path, follow_symlinks=False).st_mode
        if mode & 0o111 == 0:
            raise VerificationError(f"proof checker is not executable: {relative}")
    return payload


def bind_frozen_files(root: Path) -> tuple[dict[str, bytes], list[dict[str, object]]]:
    payloads: dict[str, bytes] = {}
    evidence: list[dict[str, object]] = []
    for relative in sorted(FROZEN_FILES):
        expected = FROZEN_FILES[relative]
        payloads[relative] = _bind_one(relative, expected, root)
        evidence.append(
            {
                "path": relative,
                "role": expected.role,
                "sha256": expected.sha256,
                "size_bytes": expected.size_bytes,
            }
        )
    return payloads, evidence


_DIMACS_INTEGER = re.compile(r"(?:0|-[1-9][0-9]*|[1-9][0-9]*)\Z")


def parse_dimacs(payload: bytes) -> dict[str, int]:
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("DIMACS is not ASCII") from exc
    header: tuple[int, int] | None = None
    current_clause_size = 0
    clause_count = 0
    literal_count = 0
    maximum_variable = 0
    maximum_clause_size = 0
    empty_clause_count = 0
    comment_count = 0
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if not line:
            raise VerificationError(f"blank DIMACS line {line_number}")
        if line.startswith("c"):
            if current_clause_size:
                raise VerificationError("DIMACS comment splits a clause")
            comment_count += 1
            continue
        if line.startswith("p"):
            if header is not None or clause_count or current_clause_size:
                raise VerificationError("misplaced or duplicate DIMACS header")
            fields = line.split()
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise VerificationError("malformed DIMACS header")
            if not fields[2].isdigit() or not fields[3].isdigit():
                raise VerificationError("nondecimal DIMACS header count")
            header = (int(fields[2]), int(fields[3]))
            if header[0] <= 0 or header[1] <= 0:
                raise VerificationError("nonpositive DIMACS header count")
            continue
        if header is None:
            raise VerificationError("DIMACS clause precedes header")
        for token in line.split():
            if _DIMACS_INTEGER.fullmatch(token) is None:
                raise VerificationError(
                    f"malformed DIMACS integer on line {line_number}: {token!r}"
                )
            value = int(token)
            if value == 0:
                clause_count += 1
                if current_clause_size == 0:
                    empty_clause_count += 1
                maximum_clause_size = max(
                    maximum_clause_size, current_clause_size
                )
                current_clause_size = 0
                continue
            variable = abs(value)
            if variable > header[0]:
                raise VerificationError(
                    f"DIMACS variable {variable} exceeds header bound {header[0]}"
                )
            literal_count += 1
            current_clause_size += 1
            maximum_variable = max(maximum_variable, variable)
    if header is None:
        raise VerificationError("missing DIMACS header")
    if current_clause_size:
        raise VerificationError("unterminated final DIMACS clause")
    if clause_count != header[1]:
        raise VerificationError(
            f"DIMACS clause count mismatch: {clause_count} != {header[1]}"
        )
    return {
        "clauses": clause_count,
        "comments": comment_count,
        "empty_clauses": empty_clause_count,
        "literals": literal_count,
        "maximum_clause_size": maximum_clause_size,
        "maximum_variable_observed": maximum_variable,
        "variables": header[0],
    }


def _encode_unsigned(value: int) -> bytes:
    if value < 0:
        raise ValueError("negative unsigned value")
    encoded = bytearray()
    while value & ~0x7F:
        encoded.append((value & 0x7F) | 0x80)
        value >>= 7
    encoded.append(value)
    return bytes(encoded)


def parse_addition_only_bdrat(
    payload: bytes, *, max_variable: int = EXPECTED_VARIABLES
) -> dict[str, int]:
    offset = 0
    record_count = 0
    literal_count = 0
    maximum_variable = 0
    maximum_clause_size = 0
    empty_records: list[int] = []
    while offset < len(payload):
        prefix = payload[offset]
        offset += 1
        if prefix == ord("d"):
            raise VerificationError(
                f"deletion record at binary proof record {record_count + 1}"
            )
        if prefix != ord("a"):
            raise VerificationError(
                f"invalid binary proof prefix 0x{prefix:02x} "
                f"at record {record_count + 1}"
            )
        record_count += 1
        clause_size = 0
        while True:
            start = offset
            value = 0
            shift = 0
            while True:
                if offset >= len(payload):
                    raise VerificationError(
                        f"truncated varint in binary proof record {record_count}"
                    )
                byte = payload[offset]
                offset += 1
                value |= (byte & 0x7F) << shift
                if byte & 0x80 == 0:
                    break
                shift += 7
                if shift > 63:
                    raise VerificationError("oversized binary proof varint")
            if payload[start:offset] != _encode_unsigned(value):
                raise VerificationError(
                    f"noncanonical varint in binary proof record {record_count}"
                )
            if value == 0:
                break
            variable = value >> 1
            if variable == 0:
                raise VerificationError(
                    f"zero-variable literal in binary proof record {record_count}"
                )
            if variable > max_variable:
                raise VerificationError(
                    f"binary proof variable {variable} exceeds {max_variable}"
                )
            clause_size += 1
            literal_count += 1
            maximum_variable = max(maximum_variable, variable)
        maximum_clause_size = max(maximum_clause_size, clause_size)
        if clause_size == 0:
            empty_records.append(record_count)
            if offset != len(payload):
                raise VerificationError(
                    f"post-empty binary proof data starts at byte {offset}"
                )
    if not payload:
        raise VerificationError("empty binary proof")
    if len(empty_records) != 1:
        raise VerificationError(
            f"binary proof has {len(empty_records)} empty additions, expected one"
        )
    if empty_records[0] != record_count:
        raise VerificationError("binary proof empty addition is not final")
    return {
        "addition_records": record_count,
        "deletion_records": 0,
        "empty_addition_record": empty_records[0],
        "empty_additions": 1,
        "literals": literal_count,
        "maximum_clause_size": maximum_clause_size,
        "maximum_variable_observed": maximum_variable,
        "post_empty_records": 0,
    }


def _normalize_checker_lines(stdout: bytes) -> list[str]:
    try:
        text = stdout.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("checker stdout is not ASCII") from exc
    return [
        line.strip()
        for line in text.replace("\r", "").splitlines()
        if line.strip()
    ]


def validate_drat_trim_result(
    exit_code: int, stdout: bytes, stderr: bytes
) -> dict[str, object]:
    if exit_code != 0:
        raise VerificationError(f"drat-trim exit code is {exit_code}, expected 0")
    if stderr != b"":
        raise VerificationError("drat-trim wrote to stderr")
    lines = _normalize_checker_lines(stdout)
    allowed = (
        re.compile(r"c turning on binary mode checking\Z"),
        re.compile(
            r"c parsing input formula with 9802 variables and 32108 clauses\Z"
        ),
        re.compile(r"c finished parsing, read 742337 bytes from proof file\Z"),
        re.compile(r"c start forward verification\Z"),
        re.compile(r"c [0-9]+ of 32108 clauses in core\Z"),
        re.compile(
            r"c [0-9]+ of 45282 lemmas in core using "
            r"[0-9]+ resolution steps\Z"
        ),
        re.compile(
            r"c 0 RAT lemmas in core; 0 redundant literals in core lemmas\Z"
        ),
        re.compile(
            r"c optimized proofs are not supported for forward checking\Z"
        ),
        re.compile(r"s VERIFIED\Z"),
        re.compile(r"c verification time: [0-9]+(?:\.[0-9]+)? seconds\Z"),
    )
    if len(lines) != len(allowed):
        raise VerificationError(
            f"unexpected drat-trim stdout line count {len(lines)}"
        )
    for index, (line, pattern) in enumerate(zip(lines, allowed), 1):
        if pattern.fullmatch(line) is None:
            raise VerificationError(
                f"unexpected drat-trim stdout line {index}: {line!r}"
            )
    if lines.count("s VERIFIED") != 1:
        raise VerificationError("drat-trim verification marker is not unique")
    stable_lines = [
        line for line in lines if not line.startswith("c verification time:")
    ]
    return {
        "exit_code": exit_code,
        "marker": "s VERIFIED",
        "marker_count": 1,
        "rat_lemmas_in_core": 0,
        "stable_stdout_lines": stable_lines,
        "stderr_empty": True,
    }


def validate_lrat_check_result(
    exit_code: int, stdout: bytes, stderr: bytes
) -> dict[str, object]:
    if exit_code != 0:
        raise VerificationError(f"lrat-check exit code is {exit_code}, expected 0")
    if stderr != b"":
        raise VerificationError("lrat-check wrote to stderr")
    lines = _normalize_checker_lines(stdout)
    allowed = (
        re.compile(
            r"c parsed a formula with 9802 variables and 32108 clauses\Z"
        ),
        re.compile(r"c VERIFIED\Z"),
        re.compile(r"c allocated [0-9]+ [0-9]+ [0-9]+\Z"),
        re.compile(
            r"c Added clauses = 57299\.  Deleted clauses = 57168\.  "
            r"Max live clauses = 32108\Z"
        ),
        re.compile(r"c verification time = [0-9]+(?:\.[0-9]+)? secs\Z"),
    )
    if len(lines) != len(allowed):
        raise VerificationError(
            f"unexpected lrat-check stdout line count {len(lines)}"
        )
    for index, (line, pattern) in enumerate(zip(lines, allowed), 1):
        if pattern.fullmatch(line) is None:
            raise VerificationError(
                f"unexpected lrat-check stdout line {index}: {line!r}"
            )
    if lines.count("c VERIFIED") != 1:
        raise VerificationError("lrat-check verification marker is not unique")
    stable_lines = [
        line for line in lines if not line.startswith("c verification time =")
    ]
    return {
        "exit_code": exit_code,
        "marker": "c VERIFIED",
        "marker_count": 1,
        "stable_stdout_lines": stable_lines,
        "stderr_empty": True,
    }


def _write_private(path: Path, payload: bytes, mode: int) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise VerificationError(f"short write to private file {path}")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def run_private_checkers(payloads: Mapping[str, bytes]) -> dict[str, object]:
    with tempfile.TemporaryDirectory(
        prefix="gamma-theta-hole9-verifier-b-"
    ) as temporary:
        private = Path(temporary)
        os.chmod(private, 0o700)
        copies = {
            "instance.cnf": (payloads[CANDIDATE_FORMULA], 0o400),
            "proof.normalized.bdrat": (payloads[NORMALIZED_PROOF], 0o400),
            "proof.lrat": (payloads[LRAT_PROOF], 0o400),
            "drat-trim": (payloads[DRAT_TRIM], 0o500),
            "lrat-check": (payloads[LRAT_CHECK], 0o500),
        }
        for name, (payload, mode) in copies.items():
            _write_private(private / name, payload, mode)
        environment = {
            "HOME": temporary,
            "LC_ALL": "C",
            "PATH": "/usr/bin:/bin",
            "TMPDIR": temporary,
        }
        drat_command = [
            str(private / "drat-trim"),
            "instance.cnf",
            "proof.normalized.bdrat",
            "-i",
            "-f",
            "-W",
            "-U",
            "-t",
            "1800",
        ]
        try:
            drat = subprocess.run(
                drat_command,
                cwd=private,
                env=environment,
                capture_output=True,
                check=False,
                timeout=120,
            )
        except subprocess.TimeoutExpired as exc:
            raise VerificationError("drat-trim exceeded 120-second wall limit") from exc
        drat_evidence = validate_drat_trim_result(
            drat.returncode, drat.stdout, drat.stderr
        )

        lrat_command = [
            str(private / "lrat-check"),
            "instance.cnf",
            "proof.lrat",
        ]
        try:
            lrat = subprocess.run(
                lrat_command,
                cwd=private,
                env=environment,
                capture_output=True,
                check=False,
                timeout=120,
            )
        except subprocess.TimeoutExpired as exc:
            raise VerificationError("lrat-check exceeded 120-second wall limit") from exc
        lrat_evidence = validate_lrat_check_result(
            lrat.returncode, lrat.stdout, lrat.stderr
        )

        expected_entries = set(copies)
        actual_entries = {entry.name for entry in private.iterdir()}
        if actual_entries != expected_entries:
            raise VerificationError(
                "proof checker created unexpected private-directory entries: "
                f"{sorted(actual_entries - expected_entries)}"
            )
        for name, (payload, _mode) in copies.items():
            if _read_regular_file(private / name) != payload:
                raise VerificationError(
                    f"private checker input or executable changed: {name}"
                )
        return {
            "drat_trim": {
                "command": [
                    "drat-trim",
                    "instance.cnf",
                    "proof.normalized.bdrat",
                    "-i",
                    "-f",
                    "-W",
                    "-U",
                    "-t",
                    "1800",
                ],
                **drat_evidence,
            },
            "fresh_private_directory": True,
            "inputs_and_executables_unchanged_after_checks": True,
            "lrat_check": {
                "command": ["lrat-check", "instance.cnf", "proof.lrat"],
                **lrat_evidence,
            },
            "timeouts_seconds": {
                "drat_trim": 120,
                "lrat_check": 120,
            },
        }


def _expect_rejection(name: str, action: Callable[[], object]) -> dict[str, object]:
    try:
        action()
    except VerificationError as exc:
        return {"name": name, "reason": str(exc), "rejected": True}
    raise VerificationError(f"hostile mutation was accepted: {name}")


_GOOD_DRAT_STDOUT = b"""\
c turning on binary mode checking
c parsing input formula with 9802 variables and 32108 clauses
c finished parsing, read 742337 bytes from proof file
c start forward verification
c 1 of 32108 clauses in core
c 1 of 45282 lemmas in core using 1 resolution steps
c 0 RAT lemmas in core; 0 redundant literals in core lemmas
c optimized proofs are not supported for forward checking
s VERIFIED
c verification time: 1.0 seconds
"""

_GOOD_LRAT_STDOUT = b"""\
c parsed a formula with 9802 variables and 32108 clauses
c VERIFIED
c allocated 1 2 3
c Added clauses = 57299.  Deleted clauses = 57168.  Max live clauses = 32108
c verification time = 1.0 secs
"""


def run_hostile_mutations(
    formula: bytes,
    proof: bytes,
    *,
    decisive_payloads: Mapping[str, bytes] | None = None,
) -> list[dict[str, object]]:
    valid_tiny_proof = (
        b"a" + _encode_unsigned(2) + b"\x00" + b"a\x00"
    )
    if parse_addition_only_bdrat(valid_tiny_proof, max_variable=1)[
        "addition_records"
    ] != 2:
        raise VerificationError("internal valid binary-proof control failed")
    if parse_dimacs(b"p cnf 2 2\n1 -2 0\n2 0\n")["clauses"] != 2:
        raise VerificationError("internal valid DIMACS control failed")

    mutations: list[tuple[str, Callable[[], object]]] = [
        (
            "formula_sha256_bit_flip",
            lambda: _require_sha256(
                formula[:-1] + bytes([formula[-1] ^ 1]),
                FROZEN_FILES[CANDIDATE_FORMULA].sha256,
                "mutated formula",
            ),
        ),
        (
            "dimacs_unterminated_clause",
            lambda: parse_dimacs(b"p cnf 1 1\n1\n"),
        ),
        (
            "dimacs_declared_clause_count_mismatch",
            lambda: parse_dimacs(b"p cnf 1 2\n1 0\n"),
        ),
        (
            "dimacs_out_of_range_variable",
            lambda: parse_dimacs(b"p cnf 1 1\n2 0\n"),
        ),
        (
            "binary_deletion_record",
            lambda: parse_addition_only_bdrat(
                b"d" + proof[1:], max_variable=EXPECTED_VARIABLES
            ),
        ),
        (
            "binary_post_empty_record",
            lambda: parse_addition_only_bdrat(
                proof + b"a\x00", max_variable=EXPECTED_VARIABLES
            ),
        ),
        (
            "binary_early_empty_record",
            lambda: parse_addition_only_bdrat(
                b"a\x00" + proof, max_variable=EXPECTED_VARIABLES
            ),
        ),
        (
            "binary_variable_above_9802",
            lambda: parse_addition_only_bdrat(
                b"a"
                + _encode_unsigned(2 * (EXPECTED_VARIABLES + 1))
                + b"\x00a\x00",
                max_variable=EXPECTED_VARIABLES,
            ),
        ),
        (
            "binary_noncanonical_varint",
            lambda: parse_addition_only_bdrat(
                b"a\x82\x00\x00a\x00", max_variable=EXPECTED_VARIABLES
            ),
        ),
        (
            "binary_truncated_varint",
            lambda: parse_addition_only_bdrat(
                b"a\x80", max_variable=EXPECTED_VARIABLES
            ),
        ),
        (
            "binary_invalid_record_prefix",
            lambda: parse_addition_only_bdrat(
                b"x\x00", max_variable=EXPECTED_VARIABLES
            ),
        ),
        (
            "drat_nonzero_exit",
            lambda: validate_drat_trim_result(
                1, _GOOD_DRAT_STDOUT, b""
            ),
        ),
        (
            "drat_missing_verified_marker",
            lambda: validate_drat_trim_result(
                0, _GOOD_DRAT_STDOUT.replace(b"s VERIFIED\n", b""), b""
            ),
        ),
        (
            "drat_nonempty_stderr",
            lambda: validate_drat_trim_result(
                0, _GOOD_DRAT_STDOUT, b"warning\n"
            ),
        ),
        (
            "drat_rat_core",
            lambda: validate_drat_trim_result(
                0,
                _GOOD_DRAT_STDOUT.replace(
                    b"c 0 RAT lemmas in core",
                    b"c 1 RAT lemmas in core",
                ),
                b"",
            ),
        ),
        (
            "lrat_nonzero_exit",
            lambda: validate_lrat_check_result(
                1, _GOOD_LRAT_STDOUT, b""
            ),
        ),
        (
            "lrat_missing_verified_marker",
            lambda: validate_lrat_check_result(
                0, _GOOD_LRAT_STDOUT.replace(b"c VERIFIED\n", b""), b""
            ),
        ),
        (
            "lrat_nonempty_stderr",
            lambda: validate_lrat_check_result(
                0, _GOOD_LRAT_STDOUT, b"diagnostic\n"
            ),
        ),
    ]
    if decisive_payloads is not None:
        additionally_mutated = (
            NORMALIZED_PROOF,
            LRAT_PROOF,
            DRAT_TRIM,
            LRAT_CHECK,
            "math/lemmas/order13_k3_synthesis_target.md",
            "reviews/order13_k3_constructor_acceptance/evidence.json",
        )
        for path in additionally_mutated:
            payload = decisive_payloads[path]
            expected = FROZEN_FILES[path].sha256
            mutations.append(
                (
                    f"decisive_sha256_bit_flip:{path}",
                    lambda payload=payload, expected=expected, path=path:
                        _require_sha256(
                            payload[:-1] + bytes([payload[-1] ^ 1]),
                            expected,
                            f"mutated {path}",
                        ),
                )
            )
    return [_expect_rejection(name, action) for name, action in mutations]


def _require_sha256(payload: bytes, expected: str, label: str) -> None:
    actual = sha256_bytes(payload)
    if actual != expected:
        raise VerificationError(
            f"SHA-256 mismatch for {label}: {actual} != {expected}"
        )


def _load_json_unique(payload: bytes, label: str) -> object:
    def reject_constant(value: str) -> object:
        raise VerificationError(f"non-finite JSON constant in {label}: {value}")

    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise VerificationError(f"duplicate JSON key in {label}: {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(
            payload,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"malformed JSON in {label}") from exc


def _require_review_verdicts(payloads: Mapping[str, bytes]) -> dict[str, str]:
    expected = {
        "reviews/order13_k3_math_hostile/evidence.json":
            "ACCEPT_MATHEMATICS_WITH_NONMATHEMATICAL_WORDING_GAPS",
        "reviews/order13_k3_math_hostile/addendum_evidence.json":
            "ACCEPT_REVISED_BYTES_MATHEMATICS_UNCHANGED",
        "reviews/order13_k3_constructor_acceptance/evidence.json":
            "ACCEPT_CONSTRUCTOR_A_FOR_PROOF_PRODUCTION_INPUTS",
        "reviews/order13_k3_hole9_preflight_constructor/evidence.json":
            "ACCEPT_LIVE_HOLE9_PACKAGE_PREFLIGHT",
    }
    found: dict[str, str] = {}
    for path, verdict in expected.items():
        value = _load_json_unique(payloads[path], path)
        if not isinstance(value, dict) or value.get("verdict") != verdict:
            raise VerificationError(f"unexpected frozen review verdict in {path}")
        found[path] = verdict
    return found


def _require_corrected_readme_census(payload: bytes) -> None:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError("candidate README is not UTF-8") from exc
    required = (
        "45,281 additions total: 45,280 nonempty additions\n"
        "followed by one unique empty addition",
    )
    for phrase in required:
        if text.count(phrase) != 1:
            raise VerificationError(
                "corrected candidate README proof census is absent or nonunique"
            )
    if "45,281 nonempty" in text:
        raise VerificationError("candidate README retains the old off-by-one census")


def verify(root: Path) -> dict[str, object]:
    root = root.resolve()
    source = Path(__file__).resolve()
    source_before = _read_regular_file(source)
    payloads, binding_evidence = bind_frozen_files(root)
    pre_checker_hashes = {
        path: sha256_bytes(payload) for path, payload in payloads.items()
    }
    if payloads[CANDIDATE_FORMULA] != payloads[CONSTRUCTOR_FORMULA]:
        raise VerificationError(
            "certificate formula differs byte-for-byte from constructor formula"
        )

    formula_stats = parse_dimacs(payloads[CANDIDATE_FORMULA])
    expected_formula_stats = {
        "clauses": EXPECTED_CLAUSES,
        "comments": 0,
        "empty_clauses": 0,
        "literals": EXPECTED_FORMULA_LITERALS,
        "maximum_clause_size": EXPECTED_FORMULA_MAX_CLAUSE,
        "maximum_variable_observed": EXPECTED_VARIABLES,
        "variables": EXPECTED_VARIABLES,
    }
    if formula_stats != expected_formula_stats:
        raise VerificationError(
            f"unexpected exact formula census: {formula_stats}"
        )

    proof_stats = parse_addition_only_bdrat(payloads[NORMALIZED_PROOF])
    expected_proof_stats = {
        "addition_records": EXPECTED_PROOF_RECORDS,
        "deletion_records": 0,
        "empty_addition_record": EXPECTED_EMPTY_RECORD,
        "empty_additions": 1,
        "literals": EXPECTED_PROOF_LITERALS,
        "maximum_clause_size": EXPECTED_PROOF_MAX_CLAUSE,
        "maximum_variable_observed": EXPECTED_VARIABLES,
        "post_empty_records": 0,
    }
    if proof_stats != expected_proof_stats:
        raise VerificationError(
            f"unexpected normalized proof census: {proof_stats}"
        )

    _require_corrected_readme_census(
        payloads[
            "certificates/order13_k3_hole9_attempt000001_lrat/README.md"
        ]
    )
    review_verdicts = _require_review_verdicts(payloads)
    hostile_mutations = run_hostile_mutations(
        payloads[CANDIDATE_FORMULA],
        payloads[NORMALIZED_PROOF],
        decisive_payloads=payloads,
    )
    checker_evidence = run_private_checkers(payloads)

    post_payloads, _unused = bind_frozen_files(root)
    post_checker_hashes = {
        path: sha256_bytes(payload) for path, payload in post_payloads.items()
    }
    if pre_checker_hashes != post_checker_hashes:
        raise VerificationError("frozen input changed during verification")

    source_after = _read_regular_file(source)
    if source_before != source_after:
        raise VerificationError("verifier source file changed during verification")
    return {
        "candidate_manifest_policy": {
            "claims_used_for_decision": False,
            "interpretation":
                "The candidate manifest is hash-bound provenance only. "
                "Every formula, proof, source, tool, parser census, and "
                "checker condition is established independently here.",
        },
        "candidate_readme_census_matches_parser": True,
        "checkers": checker_evidence,
        "claim_boundary":
            "Certifies UNSAT only for the exact SHA-256-bound order-13, "
            "k=3, hole9 DIMACS formula. The C-055 and constructor bindings "
            "are frozen for a later integration audit. This verifier makes "
            "no order-13-wide or universal gamma-theta claim.",
        "formula": {
            **formula_stats,
            "certificate_equals_constructor_byte_for_byte": True,
            "sha256": FROZEN_FILES[CANDIDATE_FORMULA].sha256,
            "size_bytes": FROZEN_FILES[CANDIDATE_FORMULA].size_bytes,
        },
        "frozen_bindings": binding_evidence,
        "frozen_inputs_unchanged_pre_post": True,
        "hostile_mutations": {
            "all_rejected": all(
                item["rejected"] is True for item in hostile_mutations
            ),
            "count": len(hostile_mutations),
            "tests": hostile_mutations,
        },
        "normalized_binary_proof": {
            **proof_stats,
            "nonempty_additions": proof_stats["addition_records"] - 1,
            "policy":
                "strict canonical binary additions only; unique final empty; "
                "no post-empty bytes",
            "sha256": FROZEN_FILES[NORMALIZED_PROOF].sha256,
            "size_bytes": FROZEN_FILES[NORMALIZED_PROOF].size_bytes,
        },
        "review_verdicts_bound": review_verdicts,
        "schema": SCHEMA,
        "schema_version": 1,
        "source": {
            "binding_scope":
                "The source file was identical before and after this run. "
                "This self-observation is provenance, not authentication of "
                "already-loaded interpreter state; the external hostile "
                "review must bind these exact bytes.",
            "path": "src/verifier_b/order13_k3_hole9_certificate.py",
            "sha256": sha256_bytes(source_before),
            "size_bytes": len(source_before),
            "source_file_unchanged_during_verification": True,
            "runtime_dependencies":
                "Python standard library plus two exact SHA-256-pinned "
                "Mach-O proof checker executables",
        },
        "verdict":
            "VERIFIED_EXACT_HOLE9_CNF_UNSAT_CANDIDATE_ONLY_"
            "PENDING_HOSTILE_ACCEPTANCE",
    }


def _default_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=_default_root(),
        help="campaign root (default: inferred from this source file)",
    )
    arguments = parser.parse_args(argv)
    try:
        evidence = verify(arguments.root)
    except VerificationError as exc:
        print(f"REJECT: {exc}", file=os.sys.stderr)
        return 1
    os.sys.stdout.buffer.write(canonical_json_bytes(evidence))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
