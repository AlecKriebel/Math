"""Strict binary-DRAT to addition-only normalization.

This transformation makes no proof claim.  It accepts a canonical binary DRAT
stream only when there is exactly one empty addition, no later addition, and
only nonempty deletions after that empty addition.  It emits the canonical
addition stream, whose final record is therefore the unique empty addition.
Soundness still requires a fresh warning-fatal RUP-only check and LRAT replay.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import BinaryIO, Sequence


SCHEMA = "gamma-theta-order13-k3-binary-drat-normalization-v1"
POLICY = "canonical-additions-only-unique-final-empty-v1"
MAX_VARINT_BYTES = 10


class NormalizationError(ValueError):
    pass


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _regular(path: Path, role: str) -> os.stat_result:
    try:
        information = path.lstat()
    except FileNotFoundError as error:
        raise NormalizationError(f"{role} is absent") from error
    if (
        stat.S_ISLNK(information.st_mode)
        or not stat.S_ISREG(information.st_mode)
        or information.st_nlink != 1
    ):
        raise NormalizationError(f"{role} is not a single-link regular file")
    return information


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _encode_unsigned(value: int) -> bytes:
    result = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            result.append(byte | 0x80)
        else:
            result.append(byte)
            return bytes(result)


def _decode_unsigned(
    source: BinaryIO,
    *,
    record: int,
    maximum: int,
) -> tuple[int, bytes]:
    encoded = bytearray()
    value = 0
    shift = 0
    while True:
        raw = source.read(1)
        if not raw:
            raise NormalizationError(f"record {record}: unterminated varint")
        encoded.append(raw[0])
        if len(encoded) > MAX_VARINT_BYTES:
            raise NormalizationError(f"record {record}: oversized varint")
        value |= (raw[0] & 0x7F) << shift
        if raw[0] < 0x80:
            break
        shift += 7
    if bytes(encoded) != _encode_unsigned(value):
        raise NormalizationError(f"record {record}: noncanonical varint")
    if value > maximum:
        raise NormalizationError(f"record {record}: literal exceeds variable bound")
    return value, bytes(encoded)


def normalize_binary_drat(
    input_path: Path,
    output_path: Path,
    report_path: Path,
    *,
    max_variable: int,
) -> dict[str, object]:
    if type(max_variable) is not int or max_variable < 1:
        raise NormalizationError("max-variable must be a positive exact integer")
    supplied = tuple(
        path.absolute() for path in (input_path, output_path, report_path)
    )
    if len(set(supplied)) != 3:
        raise NormalizationError("input, output, and report paths must differ")
    if any(path.is_symlink() for path in supplied):
        raise NormalizationError("symlinked path is forbidden")
    input_path, output_path, report_path = (
        path.resolve(strict=False) for path in supplied
    )
    if output_path.parent != report_path.parent:
        raise NormalizationError("output and report must share a directory")
    if not output_path.parent.is_dir() or output_path.parent.is_symlink():
        raise NormalizationError("output directory is malformed")
    before = _regular(input_path, "input proof")
    if output_path.exists() or output_path.is_symlink():
        raise NormalizationError("normalized output already exists")
    if report_path.exists() or report_path.is_symlink():
        raise NormalizationError("normalization report already exists")

    input_hash = _sha256_file(input_path)
    output_hash = hashlib.sha256()
    counts = {
        "total": 0,
        "additions": 0,
        "deletions": 0,
        "literals": 0,
        "post_empty_deletions": 0,
    }
    maximum_seen = 0
    empty_record: int | None = None
    output_size = 0
    created: list[Path] = []
    completed = False
    output_descriptor: int | None = None
    report_descriptor: int | None = None
    try:
        output_descriptor = os.open(
            output_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
        created.append(output_path)
        with os.fdopen(output_descriptor, "wb", buffering=1 << 20) as destination:
            output_descriptor = None
            with input_path.open("rb", buffering=1 << 20) as source:
                while True:
                    prefix = source.read(1)
                    if not prefix:
                        break
                    counts["total"] += 1
                    record = counts["total"]
                    if prefix not in {b"a", b"d"}:
                        raise NormalizationError(
                            f"record {record}: invalid prefix 0x{prefix[0]:02x}"
                        )
                    addition = prefix == b"a"
                    encoded_clause = bytearray()
                    clause_length = 0
                    while True:
                        value, encoded = _decode_unsigned(
                            source,
                            record=record,
                            maximum=2 * max_variable + 1,
                        )
                        encoded_clause.extend(encoded)
                        if value == 0:
                            break
                        if value == 1:
                            raise NormalizationError(
                                f"record {record}: negative zero literal"
                            )
                        variable = value >> 1
                        if variable < 1 or variable > max_variable:
                            raise NormalizationError(
                                f"record {record}: variable outside bound"
                            )
                        maximum_seen = max(maximum_seen, variable)
                        counts["literals"] += 1
                        clause_length += 1
                    if addition:
                        counts["additions"] += 1
                        if empty_record is not None:
                            raise NormalizationError(
                                f"record {record}: addition after empty addition"
                            )
                        payload = prefix + bytes(encoded_clause)
                        destination.write(payload)
                        output_hash.update(payload)
                        output_size += len(payload)
                        if clause_length == 0:
                            empty_record = record
                    else:
                        counts["deletions"] += 1
                        if clause_length == 0:
                            raise NormalizationError(
                                f"record {record}: empty deletion"
                            )
                        if empty_record is not None:
                            counts["post_empty_deletions"] += 1
            destination.flush()
            os.fsync(destination.fileno())

        if counts["total"] == 0:
            raise NormalizationError("input proof is empty")
        if empty_record is None:
            raise NormalizationError("input has no empty addition")
        after = _regular(input_path, "input proof")
        identity_before = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
        )
        identity_after = (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        )
        if identity_before != identity_after:
            raise NormalizationError("input changed during normalization")
        if empty_record + counts["post_empty_deletions"] != counts["total"]:
            raise NormalizationError("records after empty addition are not all deletions")

        report = {
            "schema": SCHEMA,
            "schema_version": 1,
            "policy": POLICY,
            "claim_status": "TRANSFORMATION_ONLY_NO_PROOF_CLAIM",
            "max_variable_allowed": max_variable,
            "max_variable_observed": maximum_seen,
            "record_counts": counts,
            "empty_addition_record_index": empty_record,
            "input": {
                "path": str(input_path),
                "sha256": input_hash,
                "size_bytes": after.st_size,
            },
            "output": {
                "path": str(output_path),
                "sha256": output_hash.hexdigest(),
                "size_bytes": output_size,
            },
        }
        report_descriptor = os.open(
            report_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
        created.append(report_path)
        with os.fdopen(report_descriptor, "wb", buffering=0) as destination:
            report_descriptor = None
            destination.write(_json_bytes(report))
            destination.flush()
            os.fsync(destination.fileno())
        _fsync_directory(output_path.parent)
        completed = True
        return report
    finally:
        for descriptor in (output_descriptor, report_descriptor):
            if descriptor is not None:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
        if not completed:
            removed = False
            for path in reversed(created):
                try:
                    path.unlink()
                    removed = True
                except FileNotFoundError:
                    pass
            if removed:
                _fsync_directory(output_path.parent)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--max-variable", type=int, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        normalize_binary_drat(
            arguments.input,
            arguments.output,
            arguments.report,
            max_variable=arguments.max_variable,
        )
    except (NormalizationError, OSError) as error:
        print(f"e NORMALIZATION REJECTED: {error}", file=sys.stderr)
        return 2
    print("s NORMALIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
