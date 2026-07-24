#!/usr/bin/env python3
"""Independent exact reconstruction check for delete-three/add-four CNFs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import tempfile
from pathlib import Path
from typing import Iterator, Sequence


CHECKER_ID = "ramsey55_delete3_add4_completion_cnf_independent_check_v1"
GENERATOR_ID = "ramsey55_delete3_add4_completion_cnf_v1"
SCHEMA = "ramsey55.delete3_add4_completion_cnf.v1"
INPUT_ORDER = 42
CORE_ORDER = 39
ADDED_COUNT = 4
OUTPUT_ORDER = 43
VARIABLE_COUNT = ADDED_COUNT * CORE_ORDER + 6


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def parse_deleted(text: str) -> tuple[int, int, int]:
    try:
        values = tuple(int(item) for item in text.split(","))
    except ValueError as error:
        raise ValueError("delete value is not an integer triple") from error
    if (
        len(values) != 3
        or values != tuple(sorted(set(values)))
        or any(value < 0 or value >= INPUT_ORDER for value in values)
    ):
        raise ValueError("delete value must be three increasing labels in 0..41")
    return values


def selected_line(path: Path, line_number: int) -> bytes:
    if line_number < 1:
        raise ValueError("catalog line must be positive")
    data_lines = [
        line.strip()
        for line in path.read_bytes().splitlines()
        if line.strip() and not line.lstrip().startswith(b"#")
    ]
    if line_number > len(data_lines):
        raise ValueError("catalog line is out of range")
    return data_lines[line_number - 1] + b"\n"


def decode_short_graph6(raw: bytes) -> list[int]:
    text = raw.strip()
    marker = b">>graph6<<"
    if text.startswith(marker):
        text = text[len(marker) :]
    if not text:
        raise ValueError("empty graph6 record")
    order = text[0] - 63
    if order < 0 or order > 62:
        raise ValueError("only short graph6 is accepted")
    bit_count = order * (order - 1) // 2
    payload_count = (bit_count + 5) // 6
    if len(text) != 1 + payload_count:
        raise ValueError("graph6 payload has non-canonical length")
    payload = [byte - 63 for byte in text[1:]]
    if any(value < 0 or value > 63 for value in payload):
        raise ValueError("invalid graph6 byte")
    if bit_count % 6 and payload:
        unused = 6 - bit_count % 6
        if payload[-1] & ((1 << unused) - 1):
            raise ValueError("nonzero graph6 padding")
    adjacency = [0] * order
    bit_index = 0
    for right in range(1, order):
        for left in range(right):
            value = payload[bit_index // 6]
            bit = (value >> (5 - bit_index % 6)) & 1
            bit_index += 1
            if bit:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return adjacency


def encode_short_graph6(adjacency: Sequence[int]) -> str:
    order = len(adjacency)
    bits = [
        (adjacency[left] >> right) & 1
        for right in range(1, order)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload: list[int] = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(value + 63)
    return bytes([order + 63, *payload]).decode("ascii")


def induced_core(
    adjacency: Sequence[int], deleted: Sequence[int]
) -> tuple[list[int], tuple[int, ...]]:
    if len(adjacency) != INPUT_ORDER:
        raise ValueError("catalog record is not order 42")
    retained = tuple(vertex for vertex in range(INPUT_ORDER) if vertex not in deleted)
    if len(retained) != CORE_ORDER:
        raise AssertionError("wrong retained-label count")
    core = [0] * CORE_ORDER
    for new_left, old_left in enumerate(retained):
        for new_right in range(new_left + 1, CORE_ORDER):
            old_right = retained[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                core[new_left] |= 1 << new_right
                core[new_right] |= 1 << new_left
    return core, retained


def forbidden_counts(adjacency: Sequence[int]) -> tuple[int, int]:
    cliques = 0
    independents = 0
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        cliques += edge_count == 10
        independents += edge_count == 0
    return cliques, independents


def edge_variable(left: int, right: int) -> int:
    if left > right:
        left, right = right, left
    if left < CORE_ORDER <= right < OUTPUT_ORDER:
        return (right - CORE_ORDER) * CORE_ORDER + left + 1
    if CORE_ORDER <= left < right < OUTPUT_ORDER:
        pair_rank = 0
        for first in range(ADDED_COUNT):
            for second in range(first + 1, ADDED_COUNT):
                if (left - CORE_ORDER, right - CORE_ORDER) == (first, second):
                    return ADDED_COUNT * CORE_ORDER + pair_rank + 1
                pair_rank += 1
    raise ValueError("asked for a variable on a fixed or invalid edge")


def expected_clauses(
    core: Sequence[int],
) -> Iterator[tuple[int, tuple[int, ...]]]:
    added = tuple(range(CORE_ORDER, OUTPUT_ORDER))
    for new_count in range(1, ADDED_COUNT + 1):
        for selected_new in itertools.combinations(added, new_count):
            for selected_core in itertools.combinations(
                range(CORE_ORDER), 5 - new_count
            ):
                fixed_pairs = tuple(itertools.combinations(selected_core, 2))
                fixed_all_edges = all(
                    (core[left] >> right) & 1 for left, right in fixed_pairs
                )
                fixed_all_nonedges = all(
                    not ((core[left] >> right) & 1)
                    for left, right in fixed_pairs
                )
                vertices = selected_core + selected_new
                variables = tuple(
                    edge_variable(left, right)
                    for left, right in itertools.combinations(vertices, 2)
                    if right >= CORE_ORDER
                )
                if fixed_all_edges:
                    yield new_count, tuple(-value for value in variables)
                if fixed_all_nonedges:
                    yield new_count, variables


def parse_clause_line(raw: bytes, line_number: int) -> tuple[int, ...]:
    try:
        fields = tuple(int(field) for field in raw.split())
    except ValueError as error:
        raise ValueError(f"CNF line {line_number} is not integral") from error
    if not fields or fields[-1] != 0 or 0 in fields[:-1]:
        raise ValueError(f"CNF line {line_number} is not one terminated clause")
    return fields[:-1]


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            json.dump(payload, stream, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def verify(args: argparse.Namespace) -> dict:
    deleted = parse_deleted(args.delete)
    selected = selected_line(args.catalog, args.line)
    adjacency = decode_short_graph6(selected)
    core, retained = induced_core(adjacency, deleted)
    core_forbidden = forbidden_counts(core)
    if core_forbidden != (0, 0):
        raise ValueError(f"fixed core is invalid: counts={core_forbidden}")

    catalog_hash = sha256(args.catalog)
    selected_hash = hashlib.sha256(selected).hexdigest()
    expected_comments = (
        f"c generator {GENERATOR_ID}",
        f"c catalog_sha256 {catalog_hash}",
        f"c selected_graph6_sha256 {selected_hash}",
        f"c catalog_line {args.line}",
        "c deleted_original_labels " + ",".join(map(str, deleted)),
        "c retained_original_labels " + ",".join(map(str, retained)),
    )
    negative_counts = [0, 0, 0, 0]
    positive_counts = [0, 0, 0, 0]
    clause_count = 0
    with args.cnf.open("rb") as stream:
        for line_number, expected in enumerate(expected_comments, start=1):
            raw = stream.readline()
            if raw != (expected + "\n").encode("ascii"):
                raise ValueError(
                    f"CNF binding line {line_number} differs from reconstruction"
                )
        header_line_number = len(expected_comments) + 1
        raw_header = stream.readline()
        try:
            header = raw_header.decode("ascii").strip().split()
        except UnicodeDecodeError as error:
            raise ValueError("CNF header is not ASCII") from error
        if len(header) != 4 or header[:2] != ["p", "cnf"]:
            raise ValueError("malformed CNF header")
        try:
            header_variables = int(header[2])
            header_clauses = int(header[3])
        except ValueError as error:
            raise ValueError("non-integral CNF header") from error
        if header_variables != VARIABLE_COUNT:
            raise ValueError("CNF variable count differs from reconstruction")

        for new_count, expected_clause in expected_clauses(core):
            clause_count += 1
            raw = stream.readline()
            if not raw:
                raise ValueError(f"CNF ends before clause {clause_count}")
            actual_clause = parse_clause_line(
                raw, header_line_number + clause_count
            )
            if actual_clause != expected_clause:
                raise ValueError(
                    f"CNF clause {clause_count} differs from reconstruction"
                )
            if actual_clause[0] < 0:
                negative_counts[new_count - 1] += 1
            else:
                positive_counts[new_count - 1] += 1
        if stream.read():
            raise ValueError("CNF contains trailing data after reconstructed clauses")
    if header_clauses != clause_count:
        raise ValueError("CNF clause count differs from reconstruction")

    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError("metadata is not a JSON object")
    expected_metadata = {
        "schema": SCHEMA,
        "generator": GENERATOR_ID,
        "generator_source_sha256": sha256(args.generator),
        "graph_io_source_sha256": sha256(
            args.generator.resolve().parent / "graph_io.py"
        ),
        "catalog_path": str(args.catalog.resolve()),
        "catalog_sha256": catalog_hash,
        "selected_graph6": selected.decode("ascii").strip(),
        "selected_graph6_sha256": selected_hash,
        "catalog_line": args.line,
        "input_order": INPUT_ORDER,
        "deleted_original_labels": list(deleted),
        "retained_original_labels": list(retained),
        "core_order": CORE_ORDER,
        "added_vertex_count": ADDED_COUNT,
        "output_order": OUTPUT_ORDER,
        "variable_count": VARIABLE_COUNT,
        "negative_clause_counts_by_new_count": negative_counts,
        "positive_clause_counts_by_new_count": positive_counts,
        "clause_count": clause_count,
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "core_graph6": encode_short_graph6(core),
    }
    if metadata != expected_metadata:
        differing = sorted(
            key
            for key in set(metadata) | set(expected_metadata)
            if metadata.get(key) != expected_metadata.get(key)
        )
        raise ValueError(f"metadata differs on keys: {differing}")

    return {
        "schema": "ramsey55.delete3_add4_completion_cnf_check.v1",
        "checker": CHECKER_ID,
        "checker_source_sha256": sha256(Path(__file__)),
        "valid": True,
        "catalog_path": str(args.catalog.resolve()),
        "catalog_sha256": catalog_hash,
        "catalog_line": args.line,
        "selected_graph6_sha256": selected_hash,
        "deleted_original_labels": list(deleted),
        "retained_original_labels": list(retained),
        "core_graph6": encode_short_graph6(core),
        "core_forbidden_counts": {
            "clique_5": core_forbidden[0],
            "independent_5": core_forbidden[1],
        },
        "variable_count": VARIABLE_COUNT,
        "negative_clause_counts_by_new_count": negative_counts,
        "positive_clause_counts_by_new_count": positive_counts,
        "clause_count": clause_count,
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "metadata_path": str(args.metadata.resolve()),
        "metadata_sha256": sha256(args.metadata),
        "generator_source_sha256": sha256(args.generator),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--line", type=int, required=True)
    parser.add_argument("--delete", required=True)
    parser.add_argument("--generator", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        raise SystemExit(f"refusing to overwrite {args.output}")
    try:
        result = verify(args)
    except Exception as error:
        failure = {
            "schema": "ramsey55.delete3_add4_completion_cnf_check.v1",
            "checker": CHECKER_ID,
            "checker_source_sha256": sha256(Path(__file__)),
            "valid": False,
            "error": f"{type(error).__name__}: {error}",
        }
        if args.output is not None:
            atomic_json(args.output, failure)
        print(json.dumps(failure, sort_keys=True))
        return 1
    if args.output is not None:
        atomic_json(args.output, result)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
