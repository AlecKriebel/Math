#!/usr/bin/env python3
"""Direct Ramsey CNF restricted to a Hamming radius around a fixed core.

The Ramsey clauses use all 903 global edge variables.  Edges in the selected
free boundary are unrestricted and do not contribute to distance.  Every
other edge contributes one signed difference literal, and a deterministic
sequential counter limits the number of such differences.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Mapping

from direct_ramsey_cnf import (
    COUNTER_ID,
    SequentialCounter,
    allocate_sequential_counter,
    build_direct_instance,
    variable_for_edge,
)
from graph_io import encode_graph6, read_graph, validate_simple


GENERATOR_ID = "ramsey55_direct_core_hamming_radius_cnf_v1"


@dataclass(frozen=True)
class CoreRadiusInstance:
    order: int
    radius: int
    core_edges: tuple[tuple[int, int], ...]
    difference_literals: tuple[int, ...]
    counter: SequentialCounter

    @property
    def primary_variable_count(self) -> int:
        return self.order * (self.order - 1) // 2

    @property
    def variable_count(self) -> int:
        return self.primary_variable_count + self.counter.auxiliary_count

    @property
    def ramsey_clause_count(self) -> int:
        direct = build_direct_instance(self.order, use_degree_bounds=False)
        return direct.ramsey_clause_count

    @property
    def clause_count(self) -> int:
        return self.ramsey_clause_count + self.counter.clause_count

    def clauses(self) -> Iterator[tuple[int, ...]]:
        yield from build_direct_instance(
            self.order, use_degree_bounds=False
        ).ramsey_clauses()
        yield from self.counter.clauses()


def validated_boundary_free_edges(
    boundary: Mapping[str, object],
    adjacency: list[int],
    base_graph_bytes: bytes,
) -> set[tuple[int, int]]:
    """Fail closed unless boundary metadata is pinned to this exact graph."""
    order = len(adjacency)
    required = {
        "base_graph6",
        "base_file_sha256",
        "order",
        "variable_count",
        "free_edges",
        "incident_free_vertices",
        "induced_free_vertices",
    }
    missing = required - boundary.keys()
    if missing:
        raise ValueError(f"boundary metadata is missing {sorted(missing)}")
    if int(boundary["order"]) != order:
        raise ValueError("boundary metadata graph order mismatch")
    if str(boundary["base_graph6"]) != encode_graph6(adjacency):
        raise ValueError("boundary metadata graph6 mismatch")
    if str(boundary["base_file_sha256"]) != hashlib.sha256(
        base_graph_bytes
    ).hexdigest():
        raise ValueError("boundary metadata base-file hash mismatch")

    raw_edges = boundary["free_edges"]
    if not isinstance(raw_edges, list):
        raise ValueError("boundary free_edges must be a list")
    canonical: list[tuple[int, int]] = []
    for raw in raw_edges:
        if (
            not isinstance(raw, list)
            or len(raw) != 2
            or type(raw[0]) is not int
            or type(raw[1]) is not int
        ):
            raise ValueError("boundary free edge is malformed")
        left, right = raw
        if not 0 <= left < right < order:
            raise ValueError("boundary free edge is not canonical")
        canonical.append((left, right))
    if canonical != sorted(set(canonical)):
        raise ValueError("boundary free edges are duplicated or unsorted")
    if int(boundary["variable_count"]) != len(canonical):
        raise ValueError("boundary variable count mismatch")

    incident = tuple(int(value) for value in boundary["incident_free_vertices"])
    induced = tuple(int(value) for value in boundary["induced_free_vertices"])
    if incident != tuple(sorted(set(incident))) or induced:
        raise ValueError(
            "core-radius production boundary must be a pure canonical "
            "incident-vertex set"
        )
    if any(not 0 <= vertex < order for vertex in incident):
        raise ValueError("incident boundary vertex outside graph")
    incident_set = set(incident)
    exact = {
        (left, right)
        for left in range(order)
        for right in range(left + 1, order)
        if left in incident_set or right in incident_set
    }
    if set(canonical) != exact:
        raise ValueError("free edges are not the exact incident boundary")
    return set(canonical)


def build_core_radius_instance(
    adjacency: list[int],
    free_edges: set[tuple[int, int]],
    radius: int,
) -> CoreRadiusInstance:
    validate_simple(adjacency)
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    order = len(adjacency)
    all_edges = {
        (left, right)
        for left in range(order)
        for right in range(left + 1, order)
    }
    if not free_edges <= all_edges:
        raise ValueError("free boundary contains an invalid edge")
    core_edges = tuple(sorted(all_edges - free_edges))
    difference_literals = tuple(
        (
            -variable_for_edge(order, left, right)
            if (adjacency[left] >> right) & 1
            else variable_for_edge(order, left, right)
        )
        for left, right in core_edges
    )
    primary_count = order * (order - 1) // 2
    counter, next_variable = allocate_sequential_counter(
        difference_literals,
        radius,
        primary_count + 1,
        f"core_hamming_distance_at_most_{radius}",
    )
    if next_variable - 1 != primary_count + counter.auxiliary_count:
        raise AssertionError("counter allocation is not contiguous")
    return CoreRadiusInstance(
        order=order,
        radius=radius,
        core_edges=core_edges,
        difference_literals=difference_literals,
        counter=counter,
    )


def write_cnf(
    instance: CoreRadiusInstance,
    output: Path,
    *,
    base_graph6: str,
    base_graph_sha256: str,
    boundary_metadata_sha256: str,
) -> dict[str, object]:
    output.parent.mkdir(parents=True, exist_ok=True)
    header = [
        f"c generator {GENERATOR_ID}",
        f"c base_graph_sha256 {base_graph_sha256}",
        f"c boundary_metadata_sha256 {boundary_metadata_sha256}",
        f"c base_graph6 {base_graph6}",
        f"c radius {instance.radius}",
        f"c core_edge_count {len(instance.core_edges)}",
        (
            "c difference literal true iff the corresponding core edge "
            "differs from the base graph"
        ),
        f"c counter_encoding {COUNTER_ID}",
        "c clause order: direct Ramsey clauses, then sequential counter",
        (
            f"p cnf {instance.variable_count} "
            f"{instance.clause_count}"
        ),
    ]
    digest = hashlib.sha256()
    byte_count = 0
    clause_count = 0
    started = time.monotonic()
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=output.name + ".",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            for line in header:
                data = (line + "\n").encode("ascii")
                stream.write(data)
                digest.update(data)
                byte_count += len(data)
            for clause in instance.clauses():
                data = (
                    " ".join(map(str, clause))
                    + (" " if clause else "")
                    + "0\n"
                ).encode("ascii")
                stream.write(data)
                digest.update(data)
                byte_count += len(data)
                clause_count += 1
            stream.flush()
            os.fsync(stream.fileno())
        if clause_count != instance.clause_count:
            raise AssertionError("written clause count differs from plan")
        os.replace(temporary, output)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)
    return {
        "cnf_sha256": digest.hexdigest(),
        "cnf_bytes": byte_count,
        "generation_wall_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-graph", type=Path, required=True)
    parser.add_argument("--boundary-metadata", type=Path, required=True)
    parser.add_argument("--radius", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()

    graph_bytes = args.base_graph.read_bytes()
    graph = read_graph(args.base_graph)
    boundary = json.loads(
        args.boundary_metadata.read_text(encoding="utf-8")
    )
    free_edges = validated_boundary_free_edges(boundary, graph, graph_bytes)
    instance = build_core_radius_instance(graph, free_edges, args.radius)
    base_sha256 = hashlib.sha256(graph_bytes).hexdigest()
    boundary_sha256 = hashlib.sha256(
        args.boundary_metadata.read_bytes()
    ).hexdigest()
    measurements = write_cnf(
        instance,
        args.output,
        base_graph6=encode_graph6(graph),
        base_graph_sha256=base_sha256,
        boundary_metadata_sha256=boundary_sha256,
    )
    result: dict[str, object] = {
        "generator": GENERATOR_ID,
        "generator_source_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "base_graph_path": str(args.base_graph.resolve()),
        "base_graph_sha256": base_sha256,
        "base_graph6": encode_graph6(graph),
        "boundary_metadata_path": str(args.boundary_metadata.resolve()),
        "boundary_metadata_sha256": boundary_sha256,
        "order": len(graph),
        "radius": args.radius,
        "free_boundary_edge_count": len(free_edges),
        "core_edge_count": len(instance.core_edges),
        "core_edges": [list(edge) for edge in instance.core_edges],
        "difference_literals": list(instance.difference_literals),
        "primary_variable_count": instance.primary_variable_count,
        "auxiliary_variable_count": instance.counter.auxiliary_count,
        "variable_count": instance.variable_count,
        "ramsey_clause_count": instance.ramsey_clause_count,
        "counter_clause_count": instance.counter.clause_count,
        "clause_count": instance.clause_count,
        "counter_encoding": COUNTER_ID,
        "cnf_path": str(args.output.resolve()),
        **measurements,
    }
    if args.metadata:
        args.metadata.parent.mkdir(parents=True, exist_ok=True)
        args.metadata.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
