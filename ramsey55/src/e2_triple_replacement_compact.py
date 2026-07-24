#!/usr/bin/env python3
"""Independent reader for atomic E2T3RP01 replacement-screen shards."""

from __future__ import annotations

import hashlib
import itertools
import os
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterator


MAGIC = b"E2T3RP01"
HEADER_BYTES = 64
RECORD_BYTES = 64
VARIABLES = 123
CORE_ORDER = 40
ADDED_VERTICES = 3
INPUT_ORDER = 43
TRIPLES_PER_INPUT = 12_341

STATUS_STRUCTURAL = 0
STATUS_OBSERVED_UNSAT = 1
STATUS_LIMIT = 2

HEADER_STRUCT = struct.Struct("<8sHHBBHIIIHBB32s")
RECORD_STRUCT = struct.Struct("<IBBBBBB9H6I12s")

if HEADER_STRUCT.size != HEADER_BYTES:  # pragma: no cover
    raise RuntimeError("E2T3RP01 header width is not 64 bytes")
if RECORD_STRUCT.size != RECORD_BYTES:  # pragma: no cover
    raise RuntimeError("E2T3RP01 record width is not 64 bytes")


class CompactFormatError(ValueError):
    """Raised when a replacement shard violates the frozen format."""


@dataclass(frozen=True)
class Header:
    input_index: int
    triple_start: int
    triple_end: int
    record_count: int
    corpus_sha256: str


@dataclass(frozen=True)
class Record:
    triple_ordinal: int
    deleted_vertices: tuple[int, int, int]
    status: int
    max_depth: int
    retained_conflicts: int
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


def all_triples() -> tuple[tuple[int, int, int], ...]:
    triples = tuple(itertools.combinations(range(INPUT_ORDER), 3))
    if len(triples) != TRIPLES_PER_INPUT:  # pragma: no cover
        raise AssertionError("unexpected C(43,3)")
    return triples


TRIPLES = all_triples()


def _fail(path: Path, message: str) -> CompactFormatError:
    return CompactFormatError(f"{path}: {message}")


def _read_header_from(handle: BinaryIO, path: Path) -> Header:
    raw = handle.read(HEADER_BYTES)
    if len(raw) != HEADER_BYTES:
        raise _fail(path, "truncated header")
    (
        magic,
        header_bytes,
        record_bytes,
        input_index,
        flags,
        reserved,
        triple_start,
        triple_end,
        record_count,
        variables,
        core_order,
        added_vertices,
        corpus_digest,
    ) = HEADER_STRUCT.unpack(raw)
    if magic != MAGIC:
        raise _fail(path, f"bad magic {magic!r}")
    if header_bytes != HEADER_BYTES or record_bytes != RECORD_BYTES:
        raise _fail(path, "unsupported header/record widths")
    if flags != 0 or reserved != 0:
        raise _fail(path, "nonzero reserved header fields")
    if input_index not in (1, 2):
        raise _fail(path, f"input index {input_index} is not 1 or 2")
    if not 0 <= triple_start < triple_end <= TRIPLES_PER_INPUT:
        raise _fail(path, "invalid half-open triple range")
    if record_count != triple_end - triple_start:
        raise _fail(path, "record count does not equal range width")
    if variables != VARIABLES:
        raise _fail(path, f"variables {variables} != {VARIABLES}")
    if core_order != CORE_ORDER or added_vertices != ADDED_VERTICES:
        raise _fail(path, "core/added order mismatch")
    return Header(
        input_index=input_index,
        triple_start=triple_start,
        triple_end=triple_end,
        record_count=record_count,
        corpus_sha256=corpus_digest.hex(),
    )


def read_header(path: str | Path) -> Header:
    shard = Path(path)
    with shard.open("rb") as handle:
        return _read_header_from(handle, shard)


def _unpack_record(raw: bytes) -> Record:
    values = RECORD_STRUCT.unpack(raw)
    return Record(
        triple_ordinal=values[0],
        deleted_vertices=(values[1], values[2], values[3]),
        status=values[4],
        max_depth=values[5],
        retained_conflicts=values[6],
        clauses=values[7],
        negative_clauses=values[8],
        positive_clauses=values[9],
        core_k4=values[10],
        core_i4=values[11],
        core_k3=values[12],
        core_i3=values[13],
        core_edges=values[14],
        core_nonedges=values[15],
        nodes=values[16],
        branches=values[17],
        leaves=values[18],
        unit_assignments=values[19],
        elapsed_microseconds=values[20],
        record_index=values[21],
    )


def _validate_record(path: Path, record: Record, ordinal: int) -> None:
    prefix = f"triple {ordinal}"
    if record.triple_ordinal != ordinal or record.record_index != ordinal:
        raise _fail(path, f"{prefix}: ordinal redundancy mismatch")
    if record.deleted_vertices != TRIPLES[ordinal]:
        raise _fail(
            path,
            f"{prefix}: labels {record.deleted_vertices}"
            f" != {TRIPLES[ordinal]}",
        )
    if record.status not in (
        STATUS_STRUCTURAL,
        STATUS_OBSERVED_UNSAT,
        STATUS_LIMIT,
    ):
        raise _fail(path, f"{prefix}: invalid status {record.status}")
    if record.max_depth > VARIABLES:
        raise _fail(path, f"{prefix}: max depth exceeds variables")
    counts = (
        record.clauses,
        record.negative_clauses,
        record.positive_clauses,
        record.core_k4,
        record.core_i4,
        record.core_k3,
        record.core_i3,
        record.core_edges,
        record.core_nonedges,
    )
    statistics = (
        record.nodes,
        record.branches,
        record.leaves,
        record.unit_assignments,
        record.elapsed_microseconds,
    )
    if record.status == STATUS_STRUCTURAL:
        if record.retained_conflicts not in (1, 2):
            raise _fail(path, f"{prefix}: bad retained-conflict count")
        if any(counts) or any(statistics) or record.max_depth:
            raise _fail(path, f"{prefix}: structural record has solver data")
        return
    if record.retained_conflicts != 0:
        raise _fail(path, f"{prefix}: solver record retains a conflict")
    if record.nodes == 0:
        raise _fail(path, f"{prefix}: solver visited no node")
    if record.clauses != (
        record.negative_clauses + record.positive_clauses
    ):
        raise _fail(path, f"{prefix}: polarity counts do not sum")
    expected_negative = (
        3 * record.core_k4
        + 3 * record.core_k3
        + record.core_edges
    )
    expected_positive = (
        3 * record.core_i4
        + 3 * record.core_i3
        + record.core_nonedges
    )
    if record.negative_clauses != expected_negative:
        raise _fail(path, f"{prefix}: negative formula count mismatch")
    if record.positive_clauses != expected_positive:
        raise _fail(path, f"{prefix}: positive formula count mismatch")
    if record.core_edges + record.core_nonedges != 780:
        raise _fail(path, f"{prefix}: core pair count is not C(40,2)")
    if record.branches > record.nodes or record.leaves > record.nodes:
        raise _fail(path, f"{prefix}: tree count exceeds nodes")
    if record.status == STATUS_OBSERVED_UNSAT:
        if record.nodes != record.branches + record.leaves:
            raise _fail(path, f"{prefix}: UNSAT node identity fails")
        if record.leaves != record.branches + 1:
            raise _fail(path, f"{prefix}: UNSAT full-tree identity fails")


def iter_records(
    path: str | Path,
    *,
    expected_input_index: int | None = None,
    expected_range: tuple[int, int] | None = None,
    expected_corpus_sha256: str | None = None,
) -> Iterator[Record]:
    shard = Path(path)
    with shard.open("rb") as handle:
        header = _read_header_from(handle, shard)
        if (
            expected_input_index is not None
            and header.input_index != expected_input_index
        ):
            raise _fail(shard, "unexpected input index")
        if expected_range is not None and (
            header.triple_start,
            header.triple_end,
        ) != expected_range:
            raise _fail(shard, "unexpected triple range")
        if (
            expected_corpus_sha256 is not None
            and header.corpus_sha256 != expected_corpus_sha256.lower()
        ):
            raise _fail(shard, "unexpected corpus SHA-256")
        expected_size = HEADER_BYTES + header.record_count * RECORD_BYTES
        if os.fstat(handle.fileno()).st_size != expected_size:
            raise _fail(shard, "file size does not match exact record count")
        for ordinal in range(header.triple_start, header.triple_end):
            raw = handle.read(RECORD_BYTES)
            if len(raw) != RECORD_BYTES:
                raise _fail(shard, f"truncated record for triple {ordinal}")
            record = _unpack_record(raw)
            _validate_record(shard, record, ordinal)
            yield record
        if handle.read(1):
            raise _fail(shard, "trailing bytes")


def validate_file(
    path: str | Path,
    *,
    expected_input_index: int | None = None,
    expected_range: tuple[int, int] | None = None,
    expected_corpus_sha256: str | None = None,
    node_limit: int | None = None,
) -> dict[str, int | str]:
    shard = Path(path)
    header = read_header(shard)
    structural = observed_unsat = limits = 0
    total_nodes = max_nodes = max_elapsed = 0
    for record in iter_records(
        shard,
        expected_input_index=expected_input_index,
        expected_range=expected_range,
        expected_corpus_sha256=expected_corpus_sha256,
    ):
        if node_limit is not None and record.nodes > node_limit:
            raise _fail(shard, "node limit exceeded")
        structural += record.status == STATUS_STRUCTURAL
        observed_unsat += record.status == STATUS_OBSERVED_UNSAT
        limits += record.status == STATUS_LIMIT
        total_nodes += record.nodes
        max_nodes = max(max_nodes, record.nodes)
        max_elapsed = max(max_elapsed, record.elapsed_microseconds)
    return {
        "input_index": header.input_index,
        "triple_start": header.triple_start,
        "triple_end": header.triple_end,
        "record_count": header.record_count,
        "structural_obstruction_count": structural,
        "observed_unsat_count": observed_unsat,
        "limit_count": limits,
        "total_nodes": total_nodes,
        "max_nodes": max_nodes,
        "max_elapsed_microseconds": max_elapsed,
        "record_bytes": shard.stat().st_size,
        "sha256": sha256_file(shard),
    }
