#!/usr/bin/env python3
"""Deterministic delete-three/add-four fixed-core completion CNF."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence

from graph_io import encode_graph6, read_graph, validate_simple


GENERATOR_ID = "ramsey55_delete3_add4_completion_cnf_v1"
INPUT_ORDER = 42
CORE_ORDER = 39
ADDED_COUNT = 4
OUTPUT_ORDER = 43
FORBIDDEN_SIZE = 5


def parse_deleted(text: str) -> tuple[int, int, int]:
    try:
        values = tuple(int(value) for value in text.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "deleted labels must be three comma-separated integers"
        ) from error
    if (
        len(values) != 3
        or values != tuple(sorted(set(values)))
        or any(not 0 <= value < INPUT_ORDER for value in values)
    ):
        raise argparse.ArgumentTypeError(
            "deleted labels must be three distinct increasing values in 0..41"
        )
    return values


def selected_graph6_bytes(path: Path, line_number: int) -> bytes:
    if line_number < 1:
        raise ValueError("catalog line must be positive")
    lines = [
        line.strip()
        for line in path.read_bytes().splitlines()
        if line.strip() and not line.lstrip().startswith(b"#")
    ]
    if line_number > len(lines):
        raise ValueError("catalog line is out of range")
    return lines[line_number - 1] + b"\n"


def induced_core_three(
    adjacency: list[int], deleted: Sequence[int]
) -> tuple[list[int], tuple[int, ...]]:
    validate_simple(adjacency)
    deleted_tuple = tuple(deleted)
    if (
        len(adjacency) != INPUT_ORDER
        or len(deleted_tuple) != 3
        or deleted_tuple != tuple(sorted(set(deleted_tuple)))
        or any(not 0 <= value < INPUT_ORDER for value in deleted_tuple)
    ):
        raise ValueError("invalid order-42 delete-three selection")
    retained = tuple(
        vertex for vertex in range(INPUT_ORDER) if vertex not in deleted_tuple
    )
    core = [0] * len(retained)
    for left, old_left in enumerate(retained):
        for right in range(left + 1, len(retained)):
            old_right = retained[right]
            if (adjacency[old_left] >> old_right) & 1:
                core[left] |= 1 << right
                core[right] |= 1 << left
    validate_simple(core)
    return core, retained


def added_pair_order() -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations(range(ADDED_COUNT), 2))


def variable_for_unknown_edge(
    core_count: int, left: int, right: int
) -> int:
    if left > right:
        left, right = right, left
    if 0 <= left < core_count <= right < core_count + ADDED_COUNT:
        return (right - core_count) * core_count + left + 1
    if left >= core_count and right < core_count + ADDED_COUNT:
        pair = (left - core_count, right - core_count)
        pairs = added_pair_order()
        if pair in pairs:
            return ADDED_COUNT * core_count + pairs.index(pair) + 1
    raise ValueError(f"edge ({left},{right}) is fixed or outside the instance")


def unknown_variables(
    core_count: int, vertices: Sequence[int]
) -> tuple[int, ...]:
    return tuple(
        variable_for_unknown_edge(core_count, left, right)
        for left, right in itertools.combinations(vertices, 2)
        if right >= core_count
    )


def fixed_homogeneity(
    core: Sequence[int], vertices: Sequence[int]
) -> tuple[bool, bool]:
    all_edges = True
    all_nonedges = True
    for left, right in itertools.combinations(vertices, 2):
        if (core[left] >> right) & 1:
            all_nonedges = False
        else:
            all_edges = False
    return all_edges, all_nonedges


@dataclass(frozen=True)
class CompletionInstance:
    core: tuple[int, ...]
    retained_labels: tuple[int, ...]
    clauses: tuple[tuple[int, ...], ...]
    negative_counts: tuple[int, int, int, int]
    positive_counts: tuple[int, int, int, int]

    @property
    def variable_count(self) -> int:
        return ADDED_COUNT * len(self.core) + len(added_pair_order())


def check_core(core: Sequence[int]) -> tuple[int, int]:
    clique_count = 0
    independent_count = 0
    for vertices in itertools.combinations(range(len(core)), FORBIDDEN_SIZE):
        edges = sum(
            (core[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        clique_count += edges == 10
        independent_count += edges == 0
    return clique_count, independent_count


def build_completion_instance(
    core: list[int], retained_labels: Sequence[int]
) -> CompletionInstance:
    validate_simple(core)
    if len(core) != CORE_ORDER or len(retained_labels) != CORE_ORDER:
        raise ValueError("delete-three completion requires a 39-vertex core")
    if check_core(core) != (0, 0):
        raise ValueError("fixed core already contains a forbidden five-set")
    added = tuple(range(CORE_ORDER, OUTPUT_ORDER))
    clauses: list[tuple[int, ...]] = []
    negative_counts = [0] * ADDED_COUNT
    positive_counts = [0] * ADDED_COUNT
    for new_count in range(1, ADDED_COUNT + 1):
        for selected_new in itertools.combinations(added, new_count):
            for selected_core in itertools.combinations(
                range(CORE_ORDER), FORBIDDEN_SIZE - new_count
            ):
                all_edges, all_nonedges = fixed_homogeneity(core, selected_core)
                variables = unknown_variables(
                    CORE_ORDER, selected_core + selected_new
                )
                if all_edges:
                    clauses.append(tuple(-variable for variable in variables))
                    negative_counts[new_count - 1] += 1
                if all_nonedges:
                    clauses.append(variables)
                    positive_counts[new_count - 1] += 1
    return CompletionInstance(
        tuple(core),
        tuple(retained_labels),
        tuple(clauses),
        tuple(negative_counts),
        tuple(positive_counts),
    )


def render_cnf(
    instance: CompletionInstance,
    *,
    catalog_sha256: str,
    selected_graph6_sha256: str,
    catalog_line: int,
    deleted: Sequence[int],
) -> bytes:
    headers = [
        f"c generator {GENERATOR_ID}",
        f"c catalog_sha256 {catalog_sha256}",
        f"c selected_graph6_sha256 {selected_graph6_sha256}",
        f"c catalog_line {catalog_line}",
        "c deleted_original_labels " + ",".join(map(str, deleted)),
        "c retained_original_labels "
        + ",".join(map(str, instance.retained_labels)),
        (
            f"p cnf {instance.variable_count} "
            f"{len(instance.clauses)}"
        ),
    ]
    lines = headers + [
        " ".join(map(str, clause)) + (" " if clause else "") + "0"
        for clause in instance.clauses
    ]
    return ("\n".join(lines) + "\n").encode("ascii")


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--line", type=int, required=True)
    parser.add_argument("--delete", type=parse_deleted, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() == args.metadata.resolve():
        raise SystemExit("CNF and metadata paths must differ")
    for output in (args.output, args.metadata):
        if output.exists():
            raise SystemExit(f"refusing to overwrite {output}")

    catalog_bytes = args.catalog.read_bytes()
    selected_bytes = selected_graph6_bytes(args.catalog, args.line)
    adjacency = read_graph(args.catalog, args.line)
    core, retained = induced_core_three(adjacency, args.delete)
    instance = build_completion_instance(core, retained)
    catalog_sha256 = hashlib.sha256(catalog_bytes).hexdigest()
    selected_sha256 = hashlib.sha256(selected_bytes).hexdigest()
    cnf = render_cnf(
        instance,
        catalog_sha256=catalog_sha256,
        selected_graph6_sha256=selected_sha256,
        catalog_line=args.line,
        deleted=args.delete,
    )
    write_atomic(args.output, cnf)
    metadata = {
        "schema": "ramsey55.delete3_add4_completion_cnf.v1",
        "generator": GENERATOR_ID,
        "generator_source_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "graph_io_source_sha256": hashlib.sha256(
            (Path(__file__).resolve().parent / "graph_io.py").read_bytes()
        ).hexdigest(),
        "catalog_path": str(args.catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "selected_graph6": selected_bytes.decode("ascii").strip(),
        "selected_graph6_sha256": selected_sha256,
        "catalog_line": args.line,
        "input_order": INPUT_ORDER,
        "deleted_original_labels": list(args.delete),
        "retained_original_labels": list(retained),
        "core_order": CORE_ORDER,
        "added_vertex_count": ADDED_COUNT,
        "output_order": OUTPUT_ORDER,
        "variable_count": instance.variable_count,
        "negative_clause_counts_by_new_count": list(instance.negative_counts),
        "positive_clause_counts_by_new_count": list(instance.positive_counts),
        "clause_count": len(instance.clauses),
        "cnf_path": str(args.output.resolve()),
        "cnf_sha256": hashlib.sha256(cnf).hexdigest(),
        "cnf_bytes": len(cnf),
        "core_graph6": encode_graph6(core),
    }
    write_atomic(
        args.metadata,
        (json.dumps(metadata, sort_keys=True, indent=2) + "\n").encode("utf-8"),
    )
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
