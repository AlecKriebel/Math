#!/usr/bin/env python3
"""Clean-room binary-DRAT parser, deletion stripper, and hostile probe.

This file uses only the Python standard library and imports no campaign
generator, solver wrapper, or proof-recovery code.  Its production parser is
strict: binary records must have canonical base-128 varints, exact ``a``/``d``
prefixes, in-range nonzero literals, no duplicates or tautologies, no empty
deletion, and exactly one final empty addition.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Callable, Mapping, Sequence


SCHEMA = "gamma-theta-hole5-binary-drat-hostile-probe-v1"
SCHEMA_VERSION = 1
PINNED_CHECKER_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
PINNED_CHECKER_SOURCE_SHA256 = (
    "f7619bdc338bc8151b2f6bb87488052795c926b048d5040cf165742eb1ba9a26"
)
PRODUCTION_MAX_VAR = 6_886
MAX_UVARINT = (1 << 63) - 1
MAX_UVARINT_BYTES = 9
READ_BLOCK_BYTES = 1 << 20
STRICT_CHECKER_FLAGS = ("-i", "-f", "-W", "-U", "-t", "10")
TIME_LINE = re.compile(
    rb"(?m)^c verification time: ([0-9]+(?:\.[0-9]+)?) seconds$"
)


class BinaryDratFailure(ValueError):
    """A fail-closed binary-proof parse or artifact error."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


@dataclass(frozen=True)
class ProofStats:
    byte_count: int
    record_count: int
    addition_count: int
    deletion_count: int
    addition_literal_count: int
    deletion_literal_count: int
    maximum_variable: int
    maximum_clause_length: int
    empty_addition_count: int
    final_empty_record: int
    first_deletion_record: int | None
    proof_sha256: str
    addition_stream_sha256: str
    deletion_stream_sha256: str
    addition_stream_size_bytes: int
    deletion_stream_size_bytes: int


def fail(code: str, message: str) -> None:
    raise BinaryDratFailure(code, message)


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        fail(code, message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(READ_BLOCK_BYTES), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def campaign_root() -> Path:
    source = Path(__file__).resolve()
    for ancestor in source.parents:
        if (
            (ancestor / "tools/drat_trim_2023_05_22/drat-trim").is_file()
            and (ancestor / "tools/drat_trim_2023_05_22/drat-trim.c").is_file()
        ):
            return ancestor
    fail("campaign_root", "cannot locate pinned checker from probe path")


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
            "symlink",
            f"symlinked path component {current}",
        )


def _assert_regular_single_link(path: Path, role: str) -> None:
    _assert_no_symlink_components(path)
    try:
        information = os.lstat(path)
    except FileNotFoundError as error:
        raise BinaryDratFailure("missing", f"{role} is missing: {path}") from error
    require(
        stat.S_ISREG(information.st_mode),
        "file_type",
        f"{role} is not a regular file",
    )
    require(
        information.st_nlink == 1,
        "hard_link",
        f"{role} has multiple hard links",
    )


def _validate_max_var(max_var: int) -> None:
    require(
        type(max_var) is int and 1 <= max_var <= (MAX_UVARINT >> 1),
        "max_var",
        "maximum variable must be a positive bounded integer",
    )


class BlockReader:
    """Buffered single-byte reader with an exact consumed-byte offset."""

    def __init__(self, source: BinaryIO):
        self.source = source
        self.block = b""
        self.index = 0
        self.offset = 0

    def read_byte(self) -> int | None:
        if self.index == len(self.block):
            self.block = self.source.read(READ_BLOCK_BYTES)
            self.index = 0
            if not self.block:
                return None
        value = self.block[self.index]
        self.index += 1
        self.offset += 1
        return value


def encode_uvarint(value: int) -> bytes:
    require(
        type(value) is int and 0 <= value <= MAX_UVARINT,
        "uvarint_value",
        "unsigned varint value is outside the supported 63-bit range",
    )
    result = bytearray()
    while True:
        payload = value & 0x7F
        value >>= 7
        if value:
            result.append(payload | 0x80)
        else:
            result.append(payload)
            return bytes(result)


def encode_literal(literal: int) -> bytes:
    require(
        type(literal) is int and literal != 0,
        "literal_value",
        "a literal encoder input must be a nonzero integer",
    )
    magnitude = abs(literal)
    encoded = (magnitude << 1) | int(literal < 0)
    return encode_uvarint(encoded)


def encode_record(prefix: str, literals: Sequence[int]) -> bytes:
    require(prefix in {"a", "d"}, "prefix", "record prefix must be a or d")
    payload = bytearray(prefix.encode("ascii"))
    for literal in literals:
        payload.extend(encode_literal(literal))
    payload.append(0)
    return bytes(payload)


def _decode_uvarint(
    reader: BlockReader,
    raw_record: bytearray,
    record_number: int,
) -> int:
    value = 0
    raw = bytearray()
    for index in range(MAX_UVARINT_BYTES):
        byte = reader.read_byte()
        require(
            byte is not None,
            "truncated_varint",
            f"record {record_number} ends inside a varint",
        )
        raw.append(byte)
        raw_record.append(byte)
        value |= (byte & 0x7F) << (7 * index)
        if byte < 0x80:
            require(
                bytes(raw) == encode_uvarint(value),
                "noncanonical_varint",
                f"record {record_number} has a redundant varint byte",
            )
            return value
    fail(
        "varint_overflow",
        f"record {record_number} exceeds {MAX_UVARINT_BYTES} varint bytes",
    )


RecordObserver = Callable[[str, tuple[int, ...], bytes], None]


def parse_binary_drat_stream(
    source: BinaryIO,
    *,
    max_var: int,
    allow_deletions: bool,
    require_final_empty: bool = True,
    addition_sink: BinaryIO | None = None,
    observer: RecordObserver | None = None,
) -> ProofStats:
    """Parse strict binary DRAT and optionally emit exact addition records."""

    _validate_max_var(max_var)
    reader = BlockReader(source)
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

    while True:
        prefix_byte = reader.read_byte()
        if prefix_byte is None:
            break
        record_count += 1
        require(
            not seen_empty,
            "record_after_empty",
            "binary proof continues after its empty addition",
        )
        require(
            prefix_byte in (ord("a"), ord("d")),
            "wrong_prefix",
            f"record {record_count} has byte 0x{prefix_byte:02x}, not a/d",
        )
        prefix = chr(prefix_byte)
        deletion = prefix == "d"
        require(
            allow_deletions or not deletion,
            "deletion_forbidden",
            f"record {record_count} is a deletion",
        )
        raw_record = bytearray((prefix_byte,))
        literals: list[int] = []

        while True:
            encoded = _decode_uvarint(reader, raw_record, record_count)
            if encoded == 0:
                break
            require(
                encoded != 1,
                "negative_zero",
                f"record {record_count} uses the reserved negative-zero code",
            )
            magnitude = encoded >> 1
            require(
                1 <= magnitude <= max_var,
                "literal_range",
                f"record {record_count} variable {magnitude} exceeds {max_var}",
            )
            literal = -magnitude if encoded & 1 else magnitude
            literals.append(literal)

        require(
            not deletion or literals,
            "empty_deletion",
            f"record {record_count} deletes the empty clause",
        )
        require(
            len(set(literals)) == len(literals),
            "duplicate_literal",
            f"record {record_count} repeats a signed literal",
        )
        literal_set = set(literals)
        require(
            not any(-literal in literal_set for literal in literals),
            "tautological_clause",
            f"record {record_count} contains complementary literals",
        )

        raw = bytes(raw_record)
        proof_digest.update(raw)
        maximum_clause_length = max(maximum_clause_length, len(literals))
        if literals:
            maximum_variable = max(
                maximum_variable,
                max(abs(literal) for literal in literals),
            )
        if deletion:
            deletion_count += 1
            deletion_literals += len(literals)
            deletion_digest.update(raw)
            deletion_bytes += len(raw)
            if first_deletion_record is None:
                first_deletion_record = record_count
        else:
            addition_count += 1
            addition_literals += len(literals)
            addition_digest.update(raw)
            addition_bytes += len(raw)
            if addition_sink is not None:
                addition_sink.write(raw)
            if not literals:
                empty_additions += 1
                final_empty_record = record_count
                seen_empty = True
        if observer is not None:
            observer(prefix, tuple(literals), raw)

    require(
        reader.offset > 0,
        "empty_proof",
        "binary proof is empty",
    )
    if require_final_empty:
        require(
            empty_additions == 1 and final_empty_record == record_count,
            "missing_final_empty",
            "proof must have exactly one final empty addition",
        )
    else:
        require(
            empty_additions <= 1,
            "multiple_empty",
            "proof contains multiple empty additions",
        )
    if addition_sink is not None:
        addition_sink.flush()
    return ProofStats(
        byte_count=reader.offset,
        record_count=record_count,
        addition_count=addition_count,
        deletion_count=deletion_count,
        addition_literal_count=addition_literals,
        deletion_literal_count=deletion_literals,
        maximum_variable=maximum_variable,
        maximum_clause_length=maximum_clause_length,
        empty_addition_count=empty_additions,
        final_empty_record=final_empty_record,
        first_deletion_record=first_deletion_record,
        proof_sha256=proof_digest.hexdigest(),
        addition_stream_sha256=addition_digest.hexdigest(),
        deletion_stream_sha256=deletion_digest.hexdigest(),
        addition_stream_size_bytes=addition_bytes,
        deletion_stream_size_bytes=deletion_bytes,
    )


def proof_stats_dict(stats: ProofStats) -> dict[str, object]:
    return {
        field: getattr(stats, field)
        for field in ProofStats.__dataclass_fields__
    }


def parse_binary_drat_file(
    path: Path,
    *,
    max_var: int,
    allow_deletions: bool,
    addition_sink: BinaryIO | None = None,
) -> ProofStats:
    _assert_regular_single_link(path, "binary proof")
    before = (path.stat().st_size, sha256_file(path))
    with path.open("rb") as source:
        result = parse_binary_drat_stream(
            source,
            max_var=max_var,
            allow_deletions=allow_deletions,
            addition_sink=addition_sink,
        )
    after = (path.stat().st_size, sha256_file(path))
    require(before == after, "source_mutation", "proof changed while parsing")
    require(
        result.byte_count == before[0] and result.proof_sha256 == before[1],
        "source_digest",
        "stream digest differs from source proof binding",
    )
    return result


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def strip_binary_drat_file(
    source_path: Path,
    output_path: Path,
    *,
    max_var: int,
) -> dict[str, object]:
    """Atomically create a strict addition-only binary proof."""

    _validate_max_var(max_var)
    source = source_path.resolve(strict=True)
    output = output_path.absolute()
    _assert_regular_single_link(source, "binary proof")
    _assert_no_symlink_components(output.parent)
    require(
        output.parent.is_dir(),
        "output_parent",
        "output parent is not an existing directory",
    )
    require(not output.exists(), "output_exists", "output already exists")
    require(
        source != output.resolve(strict=False),
        "path_alias",
        "source and output paths alias",
    )

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output.name}.partial.",
        dir=output.parent,
    )
    temporary = Path(temporary_name)
    installed = False
    try:
        with os.fdopen(descriptor, "wb") as sink:
            original = parse_binary_drat_file(
                source,
                max_var=max_var,
                allow_deletions=True,
                addition_sink=sink,
            )
            sink.flush()
            os.fsync(sink.fileno())
        stripped = parse_binary_drat_file(
            temporary,
            max_var=max_var,
            allow_deletions=False,
        )
        require(
            original.addition_stream_sha256 == stripped.proof_sha256
            and original.addition_stream_size_bytes == stripped.byte_count,
            "addition_mismatch",
            "stripped proof differs from exact source addition stream",
        )
        require(
            stripped.addition_count == original.addition_count
            and stripped.deletion_count == 0
            and stripped.addition_literal_count
            == original.addition_literal_count,
            "strip_stats",
            "stripped proof statistics differ",
        )
        try:
            os.link(temporary, output)
        except FileExistsError as error:
            raise BinaryDratFailure(
                "output_race", "output appeared during installation"
            ) from error
        temporary.unlink()
        installed = True
        _fsync_directory(output.parent)
        return {
            "source": proof_stats_dict(original),
            "addition_only": proof_stats_dict(stripped),
            "all_addition_bytes_preserved_in_order": True,
        }
    finally:
        if not installed and temporary.exists():
            temporary.unlink()


def _parse_bytes(
    payload: bytes,
    *,
    max_var: int,
    allow_deletions: bool = True,
    observer: RecordObserver | None = None,
) -> ProofStats:
    return parse_binary_drat_stream(
        io.BytesIO(payload),
        max_var=max_var,
        allow_deletions=allow_deletions,
        observer=observer,
    )


def _expect_failure(
    *,
    name: str,
    payload: bytes,
    expected_code: str,
    max_var: int = 4,
    allow_deletions: bool = True,
) -> dict[str, str]:
    try:
        _parse_bytes(
            payload,
            max_var=max_var,
            allow_deletions=allow_deletions,
        )
    except BinaryDratFailure as error:
        require(
            error.code == expected_code,
            "mutation_wrong_failure",
            f"{name} raised {error.code}, expected {expected_code}",
        )
        return {"mutation": name, "rejected_as": error.code}
    fail("mutation_accepted", f"{name} was accepted")


def _stable_checker_stdout(stdout: bytes) -> bytes:
    normalized = stdout.replace(b"\r", b"")
    matches = TIME_LINE.findall(normalized)
    require(
        len(matches) == 1,
        "checker_time",
        "checker output lacks one canonical verification-time line",
    )
    try:
        elapsed = float(matches[0].decode("ascii"))
    except (UnicodeDecodeError, ValueError) as error:
        raise BinaryDratFailure(
            "checker_time", "checker time is malformed"
        ) from error
    require(
        0.0 <= elapsed <= 10.0,
        "checker_time",
        "checker time is outside the smoke-test bound",
    )
    return TIME_LINE.sub(
        b"c verification time: <nondeterministic-seconds> seconds",
        normalized,
    )


def _strict_checker_smoke() -> dict[str, object]:
    root = campaign_root()
    checker = root / "tools/drat_trim_2023_05_22/drat-trim"
    checker_source = root / "tools/drat_trim_2023_05_22/drat-trim.c"
    _assert_regular_single_link(checker, "pinned checker")
    _assert_regular_single_link(checker_source, "pinned checker source")
    require(
        sha256_file(checker) == PINNED_CHECKER_SHA256,
        "checker_hash",
        "pinned checker hash differs",
    )
    require(
        sha256_file(checker_source) == PINNED_CHECKER_SOURCE_SHA256,
        "checker_source_hash",
        "pinned checker source hash differs",
    )

    # The four clauses forbid all assignments.  Units +1 and -1 are both RUP.
    cnf_payload = (
        b"p cnf 2 4\n"
        b"1 2 0\n"
        b"-1 2 0\n"
        b"1 -2 0\n"
        b"-1 -2 0\n"
    )
    source_proof = (
        bytes.fromhex("61 02 00")       # a 1 0
        + bytes.fromhex("64 02 04 00")  # d 1 2 0
        + bytes.fromhex("61 03 00")     # a -1 0
        + bytes.fromhex("61 00")        # a 0
    )
    expected_stripped = bytes.fromhex(
        "61 02 00 61 03 00 61 00"
    )

    with tempfile.TemporaryDirectory(
        prefix=".hole5-binary-drat-smoke-",
        dir=root / "reviews",
    ) as directory_text:
        directory = Path(directory_text)
        cnf = directory / "tiny.cnf"
        source = directory / "source.bdrat"
        stripped = directory / "addition-only.bdrat"
        cnf.write_bytes(cnf_payload)
        source.write_bytes(source_proof)
        transformation = strip_binary_drat_file(
            source,
            stripped,
            max_var=2,
        )
        require(
            stripped.read_bytes() == expected_stripped,
            "smoke_strip",
            "tiny stripped proof bytes differ",
        )
        command = (
            str(checker.resolve()),
            str(cnf.resolve()),
            str(stripped.resolve()),
            *STRICT_CHECKER_FLAGS,
        )
        checker_before = sha256_file(checker)
        cnf_before = sha256_file(cnf)
        proof_before = sha256_file(stripped)
        completed = subprocess.run(
            command,
            cwd=root,
            env={
                "LC_ALL": "C",
                "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
            },
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=15,
            check=False,
        )
        require(
            completed.returncode == 0,
            "checker_exit",
            f"strict binary checker exited {completed.returncode}",
        )
        combined = completed.stdout + b"\n" + completed.stderr
        require(
            b"warning" not in combined.lower(),
            "checker_warning",
            "strict binary checker emitted a warning",
        )
        normalized = completed.stdout.replace(b"\r", b"\n")
        require(
            sum(
                line.strip() == b"s VERIFIED"
                for line in normalized.splitlines()
            )
            == 1,
            "checker_verdict",
            "strict binary checker lacks exactly one s VERIFIED",
        )
        require(
            b"0 RAT lemmas in core" in normalized,
            "checker_rat",
            "strict binary checker did not report zero RAT lemmas",
        )
        stable_stdout = _stable_checker_stdout(completed.stdout)
        require(
            sha256_file(checker) == checker_before
            and sha256_file(cnf) == cnf_before
            and sha256_file(stripped) == proof_before,
            "smoke_mutation",
            "checker, CNF, or proof changed during smoke replay",
        )
        return {
            "cnf_sha256": sha256_bytes(cnf_payload),
            "source_proof_hex": source_proof.hex(),
            "source_proof_sha256": sha256_bytes(source_proof),
            "addition_only_proof_hex": expected_stripped.hex(),
            "addition_only_proof_sha256": sha256_bytes(expected_stripped),
            "transformation": transformation,
            "normalized_command": [
                "$CHECKER",
                "$CNF",
                "$ADDITION_ONLY_BINARY_PROOF",
                *STRICT_CHECKER_FLAGS,
            ],
            "exit_code": completed.returncode,
            "verified_line_count": 1,
            "warning_free": True,
            "zero_rat_lemmas_in_core": True,
            "stderr_sha256": sha256_bytes(completed.stderr),
            "stable_stdout_sha256": sha256_bytes(stable_stdout),
            "checker_sha256": checker_before,
            "checker_source_sha256": sha256_file(checker_source),
        }


def run_self_test() -> dict[str, object]:
    # Published README fixture:
    # d -63 -8193 0 ; a 129 -8191 0 ; followed here by final a 0.
    readme_fixture = bytes.fromhex(
        "64 7f 83 80 01 00 61 82 02 ff 7f 00 61 00"
    )
    observed: list[tuple[str, tuple[int, ...], str]] = []

    def observe(prefix: str, literals: tuple[int, ...], raw: bytes) -> None:
        observed.append((prefix, literals, raw.hex()))

    fixture_stats = _parse_bytes(
        readme_fixture,
        max_var=8_193,
        observer=observe,
    )
    require(
        observed
        == [
            ("d", (-63, -8_193), "647f83800100"),
            ("a", (129, -8_191), "618202ff7f00"),
            ("a", (), "6100"),
        ],
        "readme_fixture",
        "published binary fixture decoded incorrectly",
    )
    require(
        encode_uvarint(0) == b"\x00"
        and encode_uvarint(1) == b"\x01"
        and encode_uvarint(127) == b"\x7f"
        and encode_uvarint(128) == b"\x80\x01"
        and encode_uvarint(258) == b"\x82\x02"
        and encode_uvarint(16_383) == b"\xff\x7f"
        and encode_uvarint(16_387) == b"\x83\x80\x01",
        "varint_boundaries",
        "canonical unsigned boundary encodings differ",
    )
    require(
        encode_literal(63) == bytes.fromhex("7e")
        and encode_literal(-63) == bytes.fromhex("7f")
        and encode_literal(64) == bytes.fromhex("8001")
        and encode_literal(-64) == bytes.fromhex("8101")
        and encode_literal(PRODUCTION_MAX_VAR) == bytes.fromhex("cc6b")
        and encode_literal(-PRODUCTION_MAX_VAR) == bytes.fromhex("cd6b"),
        "signed_boundaries",
        "signed literal mapping differs",
    )
    production_boundary = (
        encode_record("a", (PRODUCTION_MAX_VAR,))
        + encode_record("a", (-PRODUCTION_MAX_VAR,))
        + encode_record("a", ())
    )
    production_boundary_stats = _parse_bytes(
        production_boundary,
        max_var=PRODUCTION_MAX_VAR,
    )

    valid_with_deletions = (
        encode_record("a", (1,))
        + encode_record("d", (2,))
        + encode_record("a", (-1, 3))
        + encode_record("d", (-4, 3))
        + encode_record("a", ())
    )
    sink = io.BytesIO()
    original = parse_binary_drat_stream(
        io.BytesIO(valid_with_deletions),
        max_var=4,
        allow_deletions=True,
        addition_sink=sink,
    )
    expected_additions = (
        encode_record("a", (1,))
        + encode_record("a", (-1, 3))
        + encode_record("a", ())
    )
    require(
        sink.getvalue() == expected_additions
        and original.addition_stream_sha256
        == sha256_bytes(expected_additions),
        "byte_preservation",
        "addition stream was not preserved byte-for-byte",
    )
    stripped = _parse_bytes(
        sink.getvalue(),
        max_var=4,
        allow_deletions=False,
    )

    base_final = encode_record("a", ())
    mutations = [
        ("empty_proof", b"", "empty_proof", 4, True),
        ("wrong_prefix", b"x\x00", "wrong_prefix", 4, True),
        ("prefix_eof", b"a", "truncated_varint", 4, True),
        ("truncated_varint", b"a\x80", "truncated_varint", 4, True),
        ("unterminated_record", b"a\x02", "truncated_varint", 4, True),
        (
            "truncated_after_record",
            encode_record("a", (1,)) + b"d\x80",
            "truncated_varint",
            4,
            True,
        ),
        (
            "noncanonical_zero",
            b"a\x80\x00",
            "noncanonical_varint",
            4,
            True,
        ),
        (
            "noncanonical_literal",
            b"a\x82\x00\x00" + base_final,
            "noncanonical_varint",
            4,
            True,
        ),
        (
            "negative_zero",
            b"a\x01\x00" + base_final,
            "negative_zero",
            4,
            True,
        ),
        (
            "varint_overflow",
            b"a" + b"\xff" * 9 + b"\x01\x00",
            "varint_overflow",
            4,
            True,
        ),
        (
            "literal_range",
            encode_record("a", (5,)) + base_final,
            "literal_range",
            4,
            True,
        ),
        (
            "duplicate_literal",
            encode_record("a", (1, 1)) + base_final,
            "duplicate_literal",
            4,
            True,
        ),
        (
            "tautological_clause",
            encode_record("a", (1, -1)) + base_final,
            "tautological_clause",
            4,
            True,
        ),
        (
            "empty_deletion",
            encode_record("d", ()) + base_final,
            "empty_deletion",
            4,
            True,
        ),
        (
            "nonfinal_empty",
            base_final + encode_record("a", (1,)),
            "record_after_empty",
            4,
            True,
        ),
        (
            "double_empty",
            base_final + base_final,
            "record_after_empty",
            4,
            True,
        ),
        (
            "missing_final_empty",
            encode_record("a", (1,)),
            "missing_final_empty",
            4,
            True,
        ),
        (
            "deletion_only",
            encode_record("d", (1,)),
            "missing_final_empty",
            4,
            True,
        ),
        (
            "deletion_forbidden",
            valid_with_deletions,
            "deletion_forbidden",
            4,
            False,
        ),
        (
            "raw_literal_after_record",
            encode_record("a", (1,)) + b"\x02\x00",
            "wrong_prefix",
            4,
            True,
        ),
    ]
    rejected = [
        _expect_failure(
            name=name,
            payload=payload,
            expected_code=code,
            max_var=max_var,
            allow_deletions=allow_deletions,
        )
        for name, payload, code, max_var, allow_deletions in mutations
    ]
    smoke = _strict_checker_smoke()
    source_hash = sha256_file(Path(__file__))
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "status": "PASS",
        "probe_sha256": source_hash,
        "canonical_encoding": {
            "record_prefixes_hex": {"addition": "61", "deletion": "64"},
            "terminator_hex": "00",
            "literal_map": "2*abs(literal)+(1 iff literal<0)",
            "varint": "unsigned little-endian base-128, minimal bytes",
            "negative_zero_rejected": True,
            "maximum_supported_uvarint": MAX_UVARINT,
            "maximum_varint_bytes": MAX_UVARINT_BYTES,
        },
        "readme_fixture": {
            "proof_hex": readme_fixture.hex(),
            "decoded_records": [
                [prefix, list(literals), raw_hex]
                for prefix, literals, raw_hex in observed
            ],
            "stats": proof_stats_dict(fixture_stats),
        },
        "production_variable_boundary": {
            "maximum_variable": PRODUCTION_MAX_VAR,
            "positive_literal_hex": encode_literal(PRODUCTION_MAX_VAR).hex(),
            "negative_literal_hex": encode_literal(-PRODUCTION_MAX_VAR).hex(),
            "proof_hex": production_boundary.hex(),
            "stats": proof_stats_dict(production_boundary_stats),
        },
        "deletion_strip": {
            "source_hex": valid_with_deletions.hex(),
            "source_stats": proof_stats_dict(original),
            "addition_only_hex": expected_additions.hex(),
            "addition_only_stats": proof_stats_dict(stripped),
            "byte_exact": True,
        },
        "mutations": {
            "attempted": len(mutations),
            "rejected": rejected,
        },
        "strict_pinned_checker_smoke": smoke,
        "production_gate": {
            "expected_max_var": PRODUCTION_MAX_VAR,
            "parse_before_checker": True,
            "strip_all_deletions": True,
            "reparse_addition_only": True,
            "strict_checker_flags": [
                "-i",
                "-f",
                "-W",
                "-U",
            ],
            "require_exactly_one_verified": True,
            "require_warning_free": True,
            "require_zero_rat": True,
        },
    }


def _safe_new_output(path: Path) -> Path:
    output = path.absolute()
    _assert_no_symlink_components(output.parent)
    require(
        output.parent.is_dir(),
        "output_parent",
        "output parent is not an existing directory",
    )
    require(not output.exists(), "output_exists", "output already exists")
    return output


def _write_new(path: Path, payload: bytes) -> None:
    output = _safe_new_output(path)
    with output.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    _fsync_directory(output.parent)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Strict standard-library binary-DRAT parser, deletion stripper, "
            "and hostile mutation probe"
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    self_test = subparsers.add_parser(
        "self-test",
        help="run grammar mutations and a tiny pinned-checker binary smoke",
    )
    self_test.add_argument(
        "--output",
        type=Path,
        help="write canonical JSON to this new path instead of stdout",
    )

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="strictly inspect a complete binary DRAT proof",
    )
    inspect_parser.add_argument("--proof", type=Path, required=True)
    inspect_parser.add_argument("--max-var", type=int, required=True)

    strip_parser = subparsers.add_parser(
        "strip",
        help="create and reparse a new addition-only binary proof",
    )
    strip_parser.add_argument("--proof", type=Path, required=True)
    strip_parser.add_argument("--output", type=Path, required=True)
    strip_parser.add_argument("--max-var", type=int, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        if arguments.command == "self-test":
            result = run_self_test()
            payload = canonical_json_bytes(result)
            if arguments.output is None:
                sys.stdout.buffer.write(payload)
            else:
                _write_new(arguments.output, payload)
                print(
                    json.dumps(
                        {
                            "output": str(arguments.output.absolute()),
                            "sha256": sha256_bytes(payload),
                            "status": "PASS",
                        },
                        sort_keys=True,
                    )
                )
        elif arguments.command == "inspect":
            result = parse_binary_drat_file(
                arguments.proof,
                max_var=arguments.max_var,
                allow_deletions=True,
            )
            print(
                canonical_json_bytes(proof_stats_dict(result)).decode("utf-8"),
                end="",
            )
        elif arguments.command == "strip":
            result = strip_binary_drat_file(
                arguments.proof,
                arguments.output,
                max_var=arguments.max_var,
            )
            print(canonical_json_bytes(result).decode("utf-8"), end="")
        else:
            fail("command", "unsupported command")
        return 0
    except (
        BinaryDratFailure,
        OSError,
        subprocess.SubprocessError,
    ) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
