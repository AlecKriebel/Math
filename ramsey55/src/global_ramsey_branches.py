#!/usr/bin/env python3
"""Lossless complement/relabel symmetry branches for the global n=43 CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Iterator, Sequence

from direct_ramsey_cnf import variable_for_edge


GENERATOR_ID = "ramsey55_global_vertex0_degree_branch_v1"
ORDER = 43
BRANCH_DEGREES = (18, 19, 20, 21)


def branch_units(order: int, degree: int) -> tuple[int, ...]:
    if not 0 <= degree < order:
        raise ValueError("degree is outside the graph")
    return tuple(
        (
            variable_for_edge(order, 0, vertex)
            if vertex <= degree
            else -variable_for_edge(order, 0, vertex)
        )
        for vertex in range(1, order)
    )


def complement(adjacency: Sequence[int]) -> list[int]:
    order = len(adjacency)
    mask = (1 << order) - 1
    return [
        mask & ~(adjacency[vertex] | (1 << vertex))
        for vertex in range(order)
    ]


def relabel(adjacency: Sequence[int], old_order: Sequence[int]) -> list[int]:
    if sorted(old_order) != list(range(len(adjacency))):
        raise ValueError("old_order is not a permutation")
    result = [0] * len(adjacency)
    for new_left, old_left in enumerate(old_order):
        for new_right in range(new_left + 1, len(adjacency)):
            old_right = old_order[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                result[new_left] |= 1 << new_right
                result[new_right] |= 1 << new_left
    return result


def normalize_vertex_zero(adjacency: Sequence[int]) -> tuple[list[int], bool, int]:
    """Use complement and relabeling to sort vertex-0 neighbors first."""
    order = len(adjacency)
    graph = list(adjacency)
    complemented = graph[0].bit_count() > (order - 1) // 2
    if complemented:
        graph = complement(graph)
    neighbors = [
        vertex for vertex in range(1, order) if (graph[0] >> vertex) & 1
    ]
    nonneighbors = [
        vertex for vertex in range(1, order) if not (graph[0] >> vertex) & 1
    ]
    normalized = relabel(graph, (0, *neighbors, *nonneighbors))
    return normalized, complemented, len(neighbors)


def write_branch_cnf(
    base_cnf: Path,
    output: Path,
    *,
    degree: int,
    expected_base_sha256: str,
) -> dict[str, object]:
    if degree not in BRANCH_DEGREES:
        raise ValueError(f"degree must be one of {BRANCH_DEGREES}")
    base_sha256 = hashlib.sha256(base_cnf.read_bytes()).hexdigest()
    if base_sha256 != expected_base_sha256:
        raise ValueError("base CNF hash mismatch")
    units = branch_units(ORDER, degree)
    output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    bytes_written = 0
    header_seen = False
    base_variables: int | None = None
    base_clause_count: int | None = None
    started = time.monotonic()
    temporary: str | None = None
    try:
        with base_cnf.open("rb") as source, tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=output.name + ".",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as target:
            temporary = target.name

            def write(data: bytes) -> None:
                nonlocal bytes_written
                target.write(data)
                digest.update(data)
                bytes_written += len(data)

            for raw in source:
                fields = raw.split()
                if fields[:2] == [b"p", b"cnf"]:
                    if header_seen or len(fields) != 4:
                        raise ValueError("invalid or duplicate base CNF header")
                    base_variables = int(fields[2])
                    base_clause_count = int(fields[3])
                    write(f"c branch_generator {GENERATOR_ID}\n".encode("ascii"))
                    write(f"c vertex0_degree {degree}\n".encode("ascii"))
                    write(
                        b"c symmetry: complement if needed, relabel chosen "
                        b"vertex to 0, sort its neighbors first\n"
                    )
                    write(
                        (
                            f"p cnf {base_variables} "
                            f"{base_clause_count + len(units)}\n"
                        ).encode("ascii")
                    )
                    header_seen = True
                else:
                    write(raw)
            if not header_seen or base_variables is None or base_clause_count is None:
                raise ValueError("base CNF has no problem line")
            for literal in units:
                write(f"{literal} 0\n".encode("ascii"))
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary, output)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)
    return {
        "generator": GENERATOR_ID,
        "order": ORDER,
        "degree": degree,
        "base_cnf_sha256": base_sha256,
        "base_variable_count": base_variables,
        "base_clause_count": base_clause_count,
        "unit_literals": list(units),
        "unit_clause_count": len(units),
        "variable_count": base_variables,
        "clause_count": base_clause_count + len(units),
        "cnf_sha256": digest.hexdigest(),
        "cnf_bytes": bytes_written,
        "generation_wall_seconds": time.monotonic() - started,
        "cnf_path": str(output.resolve()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--base-metadata", type=Path, required=True)
    parser.add_argument("--degree", type=int, choices=BRANCH_DEGREES, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    base_metadata = json.loads(
        args.base_metadata.read_text(encoding="utf-8")
    )
    result = write_branch_cnf(
        args.base_cnf,
        args.output,
        degree=args.degree,
        expected_base_sha256=str(base_metadata["cnf_sha256"]),
    )
    result["base_metadata_sha256"] = hashlib.sha256(
        args.base_metadata.read_bytes()
    ).hexdigest()
    result["generator_source_sha256"] = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()
    result["equivalence_scope"] = (
        "base formula SAT iff at least one degree branch 18,19,20,21 is SAT"
    )
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
