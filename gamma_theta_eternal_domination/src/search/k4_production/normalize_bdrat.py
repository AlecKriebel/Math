"""Strictly normalize binary DRAT to an addition-only candidate stream.

This module makes no proof claim.  It parses the complete input, requires one
unique empty addition and only deletions after it, strips every deletion, and
writes canonical binary addition records.  Soundness must be established by a
fresh RUP-only proof check and independent LRAT replay.
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


NORMALIZATION_SCHEMA = (
    "gamma-theta-order12-k4-binary-drat-normalization-v1"
)
NORMALIZATION_POLICY = (
    "canonical-additions-only-unique-empty-full-stream-v1"
)
MAX_UNSIGNED_VARINT_BYTES = 10


class NormalizationError(ValueError):
    """A fail-closed binary DRAT normalization rejection."""


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


def _require_regular_single_link(path: Path, role: str) -> os.stat_result:
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise NormalizationError(f"{role} is absent") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise NormalizationError(f"{role} is not a regular non-symlink file")
    if metadata.st_nlink != 1:
        raise NormalizationError(f"{role} does not have exactly one link")
    return metadata


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


def _decode_unsigned(
    source: BinaryIO,
    *,
    record_index: int,
    max_encoded_value: int,
) -> tuple[int, bytes]:
    encoded = bytearray()
    value = 0
    shift = 0
    while True:
        byte = source.read(1)
        if not byte:
            raise NormalizationError(
                f"record {record_index}: unterminated unsigned varint"
            )
        encoded.append(byte[0])
        if len(encoded) > MAX_UNSIGNED_VARINT_BYTES:
            raise NormalizationError(
                f"record {record_index}: unsigned varint is too long"
            )
        value |= (byte[0] & 0x7F) << shift
        if byte[0] < 0x80:
            break
        shift += 7
    if bytes(encoded) != _encode_unsigned(value):
        raise NormalizationError(
            f"record {record_index}: noncanonical unsigned varint"
        )
    if value > max_encoded_value:
        raise NormalizationError(
            f"record {record_index}: encoded literal exceeds variable bound"
        )
    return value, bytes(encoded)


def _open_exclusive(path: Path, role: str) -> int:
    try:
        return os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
    except FileExistsError as error:
        raise NormalizationError(f"{role} already exists") from error


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def normalize_binary_drat(
    input_path: Path,
    output_path: Path,
    report_path: Path,
    *,
    max_variable: int,
) -> dict[str, object]:
    """Normalize one complete binary DRAT stream and publish bound outputs."""

    if type(max_variable) is not int or max_variable < 1:
        raise NormalizationError("max-variable must be a positive integer")
    input_supplied = input_path.absolute()
    output_supplied = output_path.absolute()
    report_supplied = report_path.absolute()
    for supplied, role in (
        (input_supplied, "input proof"),
        (output_supplied, "normalized output"),
        (report_supplied, "normalization report"),
    ):
        if supplied.is_symlink():
            raise NormalizationError(f"{role} path is a symlink")
    input_path = input_path.resolve(strict=False)
    output_path = output_path.resolve(strict=False)
    report_path = report_path.resolve(strict=False)
    if output_path == report_path or input_path in {output_path, report_path}:
        raise NormalizationError("input, output, and report paths must differ")
    if output_path.parent != report_path.parent:
        raise NormalizationError("output and report must share a directory")
    input_metadata_before = _require_regular_single_link(
        input_path, "input proof"
    )
    if output_path.exists() or output_path.is_symlink():
        raise NormalizationError("normalized output already exists")
    if report_path.exists() or report_path.is_symlink():
        raise NormalizationError("normalization report already exists")
    if not output_path.parent.is_dir() or output_path.parent.is_symlink():
        raise NormalizationError("output directory is malformed")

    input_sha256 = _sha256_file(input_path)
    output_digest = hashlib.sha256()
    total_records = 0
    addition_records = 0
    deletion_records = 0
    literal_count = 0
    maximum_variable_observed = 0
    empty_addition_record_index: int | None = None
    post_empty_deletion_records = 0
    output_size = 0
    max_encoded_value = 2 * max_variable + 1
    created_paths: list[Path] = []
    output_descriptor: int | None = None
    report_descriptor: int | None = None
    completed = False

    try:
        output_descriptor = _open_exclusive(
            output_path, "normalized output"
        )
        created_paths.append(output_path)
        output_handle = os.fdopen(
            output_descriptor, "wb", buffering=1 << 20
        )
        output_descriptor = None
        with output_handle as destination, input_path.open(
            "rb", buffering=1 << 20
        ) as source:
            while True:
                prefix = source.read(1)
                if not prefix:
                    break
                total_records += 1
                if prefix not in {b"a", b"d"}:
                    raise NormalizationError(
                        f"record {total_records}: invalid record prefix "
                        f"0x{prefix[0]:02x}"
                    )
                is_addition = prefix == b"a"
                encoded_clause = bytearray()
                clause_length = 0
                while True:
                    value, encoded = _decode_unsigned(
                        source,
                        record_index=total_records,
                        max_encoded_value=max_encoded_value,
                    )
                    encoded_clause.extend(encoded)
                    if value == 0:
                        break
                    if value == 1:
                        raise NormalizationError(
                            f"record {total_records}: negative zero literal"
                        )
                    variable = value >> 1
                    if variable < 1 or variable > max_variable:
                        raise NormalizationError(
                            f"record {total_records}: variable {variable} "
                            "is outside the declared bound"
                        )
                    maximum_variable_observed = max(
                        maximum_variable_observed, variable
                    )
                    clause_length += 1
                    literal_count += 1

                if is_addition:
                    addition_records += 1
                    if empty_addition_record_index is not None:
                        if clause_length == 0:
                            raise NormalizationError(
                                "multiple empty addition records"
                            )
                        raise NormalizationError(
                            f"record {total_records}: addition after the "
                            "empty addition"
                        )
                    payload = prefix + bytes(encoded_clause)
                    destination.write(payload)
                    output_digest.update(payload)
                    output_size += len(payload)
                    if clause_length == 0:
                        empty_addition_record_index = total_records
                else:
                    deletion_records += 1
                    if clause_length == 0:
                        raise NormalizationError(
                            f"record {total_records}: empty deletion record"
                        )
                    if empty_addition_record_index is not None:
                        post_empty_deletion_records += 1
            destination.flush()
            os.fsync(destination.fileno())

        if total_records == 0:
            raise NormalizationError("input proof is empty")
        if empty_addition_record_index is None:
            raise NormalizationError("input has no empty addition record")
        input_metadata = _require_regular_single_link(
            input_path, "input proof"
        )
        if (
            input_metadata.st_dev,
            input_metadata.st_ino,
            input_metadata.st_size,
            input_metadata.st_mtime_ns,
            input_metadata.st_ctime_ns,
        ) != (
            input_metadata_before.st_dev,
            input_metadata_before.st_ino,
            input_metadata_before.st_size,
            input_metadata_before.st_mtime_ns,
            input_metadata_before.st_ctime_ns,
        ):
            raise NormalizationError("input proof changed during normalization")
        report = {
            "schema": NORMALIZATION_SCHEMA,
            "schema_version": 1,
            "policy": NORMALIZATION_POLICY,
            "claim_status": "TRANSFORMATION_ONLY_NO_PROOF_CLAIM",
            "max_variable_allowed": max_variable,
            "max_variable_observed": maximum_variable_observed,
            "record_counts": {
                "total": total_records,
                "additions": addition_records,
                "deletions": deletion_records,
                "post_empty_deletions": post_empty_deletion_records,
                "literals": literal_count,
            },
            "empty_addition_record_index": empty_addition_record_index,
            "input": {
                "path": str(input_path),
                "sha256": input_sha256,
                "size_bytes": input_metadata.st_size,
            },
            "output": {
                "path": str(output_path),
                "sha256": output_digest.hexdigest(),
                "size_bytes": output_size,
            },
        }
        report_descriptor = _open_exclusive(
            report_path, "normalization report"
        )
        created_paths.append(report_path)
        report_handle = os.fdopen(
            report_descriptor, "wb", buffering=0
        )
        report_descriptor = None
        with report_handle as destination:
            destination.write(_canonical_json_bytes(report))
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
            for created in reversed(created_paths):
                try:
                    created.unlink()
                    removed = True
                except FileNotFoundError:
                    pass
            if removed:
                _fsync_directory(output_path.parent)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Strictly strip deletion records from a complete binary DRAT "
            "stream. This transformation makes no proof claim."
        )
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--max-variable", required=True, type=int)
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
