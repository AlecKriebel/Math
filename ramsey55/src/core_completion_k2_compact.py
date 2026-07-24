#!/usr/bin/env python3
"""Independent reader and structural validator for K2SCRN01 shard files.

The fixed-width format is intentionally small enough for the complete
delete-two/add-three screen while still retaining exact pair coverage,
per-instance solver status, formula statistics, and DPLL counters.
"""

from __future__ import annotations

import hashlib
import os
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterator


MAGIC = b"K2SCRN01"
HEADER_BYTES = 64
RECORD_BYTES = 48
VARIABLES = 123
CORE_ORDER = 40
ADDED_VERTICES = 3
PAIRS_PER_LINE = 861
STATUS_UNSAT = 0
STATUS_LIMIT = 1

HEADER_STRUCT = struct.Struct("<8sHHHHIHBB32s8s")
RECORD_STRUCT = struct.Struct("<HBBBB9H6I")

if HEADER_STRUCT.size != HEADER_BYTES:  # pragma: no cover - import invariant
    raise RuntimeError("internal K2SCRN01 header format is not 64 bytes")
if RECORD_STRUCT.size != RECORD_BYTES:  # pragma: no cover - import invariant
    raise RuntimeError("internal K2SCRN01 record format is not 48 bytes")


class CompactFormatError(ValueError):
    """Raised when a compact shard violates its frozen format or invariants."""


@dataclass(frozen=True)
class Header:
    line_start: int
    line_end: int
    record_count: int
    catalog_sha256: str


@dataclass(frozen=True)
class Record:
    catalog_line: int
    deleted_left: int
    deleted_right: int
    status: int
    max_depth: int
    clauses: int
    negative_clauses: int
    positive_clauses: int
    core_k4: int
    core_i4: int
    core_k3: int
    core_i3: int
    core_edges: int
    core_nonedges: int
    nodes: int
    branches: int
    leaves: int
    unit_assignments: int
    elapsed_microseconds: int
    record_index: int


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _fail(path: Path, message: str) -> CompactFormatError:
    return CompactFormatError(f"{path}: {message}")


def _read_header_from(handle: BinaryIO, path: Path) -> Header:
    raw = handle.read(HEADER_BYTES)
    if len(raw) != HEADER_BYTES:
        raise _fail(path, "truncated 64-byte header")
    (
        magic,
        header_bytes,
        record_bytes,
        line_start,
        line_end,
        record_count,
        variables,
        core_order,
        added_vertices,
        catalog_digest,
        reserved,
    ) = HEADER_STRUCT.unpack(raw)
    if magic != MAGIC:
        raise _fail(path, f"bad magic {magic!r}")
    if header_bytes != HEADER_BYTES or record_bytes != RECORD_BYTES:
        raise _fail(
            path,
            f"unsupported widths header={header_bytes} record={record_bytes}",
        )
    if line_start == 0 or line_end < line_start:
        raise _fail(path, f"invalid catalog range {line_start}..{line_end}")
    expected_records = (line_end - line_start + 1) * PAIRS_PER_LINE
    if record_count != expected_records:
        raise _fail(
            path,
            f"record_count {record_count} != range total {expected_records}",
        )
    if variables != VARIABLES:
        raise _fail(path, f"variables {variables} != {VARIABLES}")
    if core_order != CORE_ORDER:
        raise _fail(path, f"core order {core_order} != {CORE_ORDER}")
    if added_vertices != ADDED_VERTICES:
        raise _fail(
            path,
            f"added vertices {added_vertices} != {ADDED_VERTICES}",
        )
    if reserved != b"\0" * 8:
        raise _fail(path, "nonzero reserved header bytes")
    return Header(
        line_start=line_start,
        line_end=line_end,
        record_count=record_count,
        catalog_sha256=catalog_digest.hex(),
    )


def read_header(path: str | Path) -> Header:
    shard = Path(path)
    with shard.open("rb") as handle:
        return _read_header_from(handle, shard)


def _expected_pair(record_index: int, line_start: int) -> tuple[int, int, int]:
    line_offset, pair_offset = divmod(record_index, PAIRS_PER_LINE)
    cursor = 0
    for deleted_left in range(41):
        width = 41 - deleted_left
        if pair_offset < cursor + width:
            deleted_right = deleted_left + 1 + pair_offset - cursor
            return line_start + line_offset, deleted_left, deleted_right
        cursor += width
    raise AssertionError("pair offset outside 0..860")


def _unpack_record(raw: bytes) -> Record:
    values = RECORD_STRUCT.unpack(raw)
    return Record(
        catalog_line=values[0],
        deleted_left=values[1],
        deleted_right=values[2],
        status=values[3],
        max_depth=values[4],
        clauses=values[5],
        negative_clauses=values[6],
        positive_clauses=values[7],
        core_k4=values[8],
        core_i4=values[9],
        core_k3=values[10],
        core_i3=values[11],
        core_edges=values[12],
        core_nonedges=values[13],
        nodes=values[14],
        branches=values[15],
        leaves=values[16],
        unit_assignments=values[17],
        elapsed_microseconds=values[18],
        record_index=values[19],
    )


def _validate_record(
    path: Path,
    record: Record,
    expected_index: int,
    line_start: int,
) -> None:
    prefix = f"record {expected_index}"
    expected_pair = _expected_pair(expected_index, line_start)
    actual_pair = (
        record.catalog_line,
        record.deleted_left,
        record.deleted_right,
    )
    if record.record_index != expected_index:
        raise _fail(
            path,
            f"{prefix}: stored index {record.record_index} does not match",
        )
    if actual_pair != expected_pair:
        raise _fail(
            path,
            f"{prefix}: pair {actual_pair} != expected {expected_pair}",
        )
    if record.status not in (STATUS_UNSAT, STATUS_LIMIT):
        raise _fail(path, f"{prefix}: invalid status {record.status}")
    if record.max_depth > VARIABLES:
        raise _fail(
            path,
            f"{prefix}: max depth {record.max_depth} > {VARIABLES}",
        )
    if record.clauses != (
        record.negative_clauses + record.positive_clauses
    ):
        raise _fail(path, f"{prefix}: clause total does not split by polarity")
    expected_negative = (
        3 * record.core_k4 + 3 * record.core_k3 + record.core_edges
    )
    expected_positive = (
        3 * record.core_i4
        + 3 * record.core_i3
        + record.core_nonedges
    )
    if record.negative_clauses != expected_negative:
        raise _fail(
            path,
            f"{prefix}: negative clauses {record.negative_clauses}"
            f" != count-derived {expected_negative}",
        )
    if record.positive_clauses != expected_positive:
        raise _fail(
            path,
            f"{prefix}: positive clauses {record.positive_clauses}"
            f" != count-derived {expected_positive}",
        )
    if record.core_edges + record.core_nonedges != 780:
        raise _fail(path, f"{prefix}: core edge/nonedge total is not 780")
    if record.nodes == 0:
        raise _fail(path, f"{prefix}: solver visited no nodes")
    if record.branches > record.nodes or record.leaves > record.nodes:
        raise _fail(path, f"{prefix}: branch/leaf counter exceeds nodes")
    if record.status == STATUS_UNSAT:
        if record.nodes != record.branches + record.leaves:
            raise _fail(path, f"{prefix}: UNSAT node/tree identity fails")
        if record.leaves != record.branches + 1:
            raise _fail(path, f"{prefix}: UNSAT full-tree identity fails")


def iter_records(
    path: str | Path,
    *,
    expected_range: tuple[int, int] | None = None,
    expected_catalog_sha256: str | None = None,
) -> Iterator[Record]:
    """Yield validated records in their mandatory lexicographic order."""

    shard = Path(path)
    with shard.open("rb") as handle:
        header = _read_header_from(handle, shard)
        if expected_range is not None and (
            header.line_start,
            header.line_end,
        ) != expected_range:
            raise _fail(
                shard,
                f"range {(header.line_start, header.line_end)}"
                f" != expected {expected_range}",
            )
        if expected_catalog_sha256 is not None and (
            header.catalog_sha256 != expected_catalog_sha256.lower()
        ):
            raise _fail(
                shard,
                f"catalog SHA-256 {header.catalog_sha256}"
                f" != expected {expected_catalog_sha256.lower()}",
            )
        expected_size = HEADER_BYTES + header.record_count * RECORD_BYTES
        actual_size = os.fstat(handle.fileno()).st_size
        if actual_size != expected_size:
            raise _fail(
                shard,
                f"size {actual_size} != exact expected {expected_size}",
            )
        for index in range(header.record_count):
            raw = handle.read(RECORD_BYTES)
            if len(raw) != RECORD_BYTES:
                raise _fail(shard, f"truncated record {index}")
            record = _unpack_record(raw)
            _validate_record(shard, record, index, header.line_start)
            yield record
        if handle.read(1):
            raise _fail(shard, "trailing bytes after exact record sequence")


def validate_file(
    path: str | Path,
    *,
    expected_range: tuple[int, int] | None = None,
    expected_catalog_sha256: str | None = None,
    node_limit: int | None = None,
) -> dict[str, int | str]:
    """Validate one shard and return a compact aggregate audit record."""

    shard = Path(path)
    header = read_header(shard)
    unsat_count = 0
    limit_count = 0
    total_nodes = 0
    max_nodes = 0
    max_elapsed_microseconds = 0
    for record in iter_records(
        shard,
        expected_range=expected_range,
        expected_catalog_sha256=expected_catalog_sha256,
    ):
        if node_limit is not None and record.nodes > node_limit:
            raise _fail(
                shard,
                f"record {record.record_index}: nodes {record.nodes}"
                f" > limit {node_limit}",
            )
        unsat_count += record.status == STATUS_UNSAT
        limit_count += record.status == STATUS_LIMIT
        total_nodes += record.nodes
        max_nodes = max(max_nodes, record.nodes)
        max_elapsed_microseconds = max(
            max_elapsed_microseconds, record.elapsed_microseconds
        )
    return {
        "line_start": header.line_start,
        "line_end": header.line_end,
        "record_count": header.record_count,
        "unsat_count": unsat_count,
        "limit_count": limit_count,
        "total_nodes": total_nodes,
        "max_nodes": max_nodes,
        "max_elapsed_microseconds": max_elapsed_microseconds,
        "record_bytes": shard.stat().st_size,
        "sha256": sha256_file(shard),
    }
