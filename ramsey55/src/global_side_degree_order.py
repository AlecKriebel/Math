#!/usr/bin/env python3
"""Exact side-wise degree-order symmetry breaking for the global branches.

The direct order-43 CNF uses forward-only sequential threshold counters.
Those counters are sufficient for the degree bounds, but their auxiliary
variables need not equal the represented prefix thresholds when a threshold
is false.  This module appends the missing reverse implications for the
*edge* counters, making every edge-counter variable equal to its intended
prefix threshold.

In a normalized minimum-degree branch, vertex 0 has neighbours
``1..degree`` and antineighbours ``degree+1..42``.  Relabelling vertices
independently inside those two sides preserves the root star.  We may
therefore require nondecreasing whole-graph degrees inside each side.  With
truthful unary thresholds this needs only the implications

    degree(u) >= threshold  ->  degree(v) >= threshold

for consecutive vertices ``u,v`` in each side and every possible threshold.
The result is one exact symmetry-broken formula per global degree branch; it
is not a SAT or UNSAT result by itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from direct_ramsey_cnf import SequentialCounter
from global_minmax_degree_cover import (
    BASE_CNF_SHA256,
    BASE_METADATA_SHA256,
    BRANCH_DEGREES,
    ORDER,
    branch_units,
    direct_instance,
)


BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
SCHEMA = "ramsey55.global_side_degree_order.v1"
GENERATOR_ID = "ramsey55_global_side_degree_order_cnf_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def clause_stream_sha256(clauses: Iterable[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return digest.hexdigest()


def reverse_counter_clauses(
    counter: SequentialCounter,
) -> Iterator[tuple[int, ...]]:
    """Complete a forward sequential counter to exact prefix thresholds.

    The existing forward clauses encode

    ``s[i,j] <- s[i-1,j] or (x[i] and s[i-1,j-1])``.

    These clauses encode the reverse direction.  Boundary values outside the
    allocated triangular rows are treated as false, and threshold zero as
    true.
    """

    if not counter.rows:
        return
    if len(counter.rows) != len(counter.input_literals):
        raise ValueError("counter row/input mismatch")

    for index, (literal, current) in enumerate(
        zip(counter.input_literals, counter.rows)
    ):
        if index == 0:
            if len(current) != 1:
                raise ValueError("first counter row must have width one")
            yield (-current[0], literal)
            continue

        previous = counter.rows[index - 1]
        for offset, threshold_variable in enumerate(current):
            threshold = offset + 1
            same = previous[offset] if offset < len(previous) else None
            if threshold == 1:
                if same is None:
                    raise ValueError("threshold-one predecessor is missing")
                yield (-threshold_variable, same, literal)
                continue

            lower = previous[offset - 1]
            if same is None:
                # A newly allocated diagonal threshold can be reached only by
                # the current input and the previous lower threshold.
                yield (-threshold_variable, literal)
                yield (-threshold_variable, lower)
            else:
                # s -> same OR (literal AND lower).
                yield (-threshold_variable, same, literal)
                yield (-threshold_variable, same, lower)


def edge_counters() -> tuple[SequentialCounter, ...]:
    instance = direct_instance()
    counters = tuple(instance.counters[2 * vertex] for vertex in range(ORDER))
    if len(counters) != ORDER:
        raise AssertionError("unexpected edge-counter count")
    for vertex, counter in enumerate(counters):
        if not counter.label.startswith(f"vertex_{vertex}_edges_"):
            raise AssertionError("edge-counter ordering changed")
    return counters


def final_threshold_variable(
    counter: SequentialCounter, threshold: int
) -> int:
    if threshold < 1 or not counter.rows:
        raise ValueError("counter has no requested threshold")
    final = counter.rows[-1]
    if threshold > len(final):
        raise ValueError("requested threshold is not allocated")
    return final[threshold - 1]


def side_vertices(degree: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if degree not in BRANCH_DEGREES:
        raise ValueError(f"degree must be one of {BRANCH_DEGREES}")
    return tuple(range(1, degree + 1)), tuple(range(degree + 1, ORDER))


def degree_order_clauses(
    degree: int, counters: Sequence[SequentialCounter] | None = None
) -> Iterator[tuple[int, ...]]:
    """Require nondecreasing degrees within each normalized root side."""

    if degree not in BRANCH_DEGREES:
        raise ValueError(f"degree must be one of {BRANCH_DEGREES}")
    if counters is None:
        counters = edge_counters()
    if len(counters) != ORDER:
        raise ValueError("wrong number of edge counters")

    lower = degree
    upper = ORDER - 1 - degree
    for side in side_vertices(degree):
        for left, right in zip(side, side[1:]):
            for threshold in range(lower + 1, upper + 1):
                left_threshold = final_threshold_variable(
                    counters[left], threshold
                )
                right_threshold = final_threshold_variable(
                    counters[right], threshold
                )
                yield (-left_threshold, right_threshold)


def reverse_clauses(
    counters: Sequence[SequentialCounter] | None = None,
) -> Iterator[tuple[int, ...]]:
    if counters is None:
        counters = edge_counters()
    if len(counters) != ORDER:
        raise ValueError("wrong number of edge counters")
    for counter in counters:
        yield from reverse_counter_clauses(counter)


def appended_clauses(degree: int) -> Iterator[tuple[int, ...]]:
    counters = edge_counters()
    for literal in branch_units(degree):
        yield (literal,)
    yield from reverse_clauses(counters)
    yield from degree_order_clauses(degree, counters)


def build_plan() -> dict[str, object]:
    counters = edge_counters()
    reverse = tuple(reverse_clauses(counters))
    branches: list[dict[str, object]] = []
    for degree in BRANCH_DEGREES:
        units = branch_units(degree)
        ordering = tuple(degree_order_clauses(degree, counters))
        additions = tuple((literal,) for literal in units) + reverse + ordering
        left_side, right_side = side_vertices(degree)
        branches.append(
            {
                "degree": degree,
                "degree_interval": [degree, ORDER - 1 - degree],
                "root_star_and_bound_unit_count": len(units),
                "neighbour_side_size": len(left_side),
                "antineighbour_side_size": len(right_side),
                "adjacent_side_comparator_count": (
                    max(0, len(left_side) - 1)
                    + max(0, len(right_side) - 1)
                ),
                "degree_threshold_count": ORDER - 1 - 2 * degree,
                "degree_order_clause_count": len(ordering),
                "degree_order_clause_stream_sha256": clause_stream_sha256(
                    ordering
                ),
                "appended_clause_count": len(additions),
                "appended_clause_stream_sha256": clause_stream_sha256(
                    additions
                ),
                "variable_count": BASE_VARIABLE_COUNT,
                "clause_count": BASE_CLAUSE_COUNT + len(additions),
            }
        )
    return {
        "schema": SCHEMA,
        "status": "EXACT_SYMMETRY_BREAKING_PLAN_NO_SOLVE_CLAIM",
        "order": ORDER,
        "base_cnf_sha256": BASE_CNF_SHA256,
        "base_metadata_sha256": BASE_METADATA_SHA256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
        "edge_counter_count": len(counters),
        "reverse_clause_count": len(reverse),
        "reverse_clause_stream_sha256": clause_stream_sha256(reverse),
        "branches": branches,
        "cover_argument": (
            "Normalize by complement and a minimum-degree root as in the "
            "three-branch cover, then independently relabel the root's "
            "neighbours and antineighbours into nondecreasing whole-graph "
            "degree order. Canonical threshold extensions satisfy every "
            "reverse counter clause."
        ),
        "claim_limit": (
            "This is an exact isomorphism cover and symmetry-breaking "
            "encoding. It contains no SAT model and no UNSAT certificate."
        ),
    }


def write_cnf(
    base_cnf: Path,
    output: Path,
    *,
    degree: int,
    expected_base_sha256: str = BASE_CNF_SHA256,
) -> dict[str, object]:
    if degree not in BRANCH_DEGREES:
        raise ValueError(f"degree must be one of {BRANCH_DEGREES}")
    actual_base_sha256 = sha256_file(base_cnf)
    if actual_base_sha256 != expected_base_sha256:
        raise ValueError("base CNF SHA-256 mismatch")

    additions = tuple(appended_clauses(degree))
    clause_count = BASE_CLAUSE_COUNT + len(additions)
    output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    byte_count = 0
    base_header_seen = False
    temporary_name: str | None = None
    started = time.monotonic()
    try:
        with base_cnf.open("rb") as source, tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=output.name + ".",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as target:
            temporary_name = target.name

            def write(data: bytes) -> None:
                nonlocal byte_count
                target.write(data)
                digest.update(data)
                byte_count += len(data)

            for raw in source:
                fields = raw.split()
                if fields[:2] == [b"p", b"cnf"]:
                    if base_header_seen or len(fields) != 4:
                        raise ValueError("invalid or duplicate base CNF header")
                    if int(fields[2]) != BASE_VARIABLE_COUNT:
                        raise ValueError("unexpected base variable count")
                    if int(fields[3]) != BASE_CLAUSE_COUNT:
                        raise ValueError("unexpected base clause count")
                    write(f"c generator {GENERATOR_ID}\n".encode("ascii"))
                    write(
                        f"c normalized_root_degree {degree}\n".encode("ascii")
                    )
                    write(
                        b"c exact edge thresholds; side-wise nondecreasing "
                        b"whole-graph degrees\n"
                    )
                    write(
                        f"p cnf {BASE_VARIABLE_COUNT} {clause_count}\n".encode(
                            "ascii"
                        )
                    )
                    base_header_seen = True
                else:
                    write(raw)
            if not base_header_seen:
                raise ValueError("base CNF has no problem line")
            for clause in additions:
                write((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary_name, output)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)

    return {
        "generator": GENERATOR_ID,
        "schema": SCHEMA,
        "status": "GENERATED_NOT_SOLVED",
        "degree": degree,
        "base_cnf_sha256": actual_base_sha256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
        "variable_count": BASE_VARIABLE_COUNT,
        "clause_count": clause_count,
        "appended_clause_count": len(additions),
        "appended_clause_stream_sha256": clause_stream_sha256(additions),
        "cnf_path": str(output.resolve()),
        "cnf_sha256": digest.hexdigest(),
        "cnf_bytes": byte_count,
        "generation_wall_seconds": time.monotonic() - started,
        "generator_source_sha256": sha256_file(Path(__file__)),
        "solve_attempted": False,
        "claim_limit": (
            "This is a symmetry-complete branch encoding, not a SAT/UNSAT "
            "result."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--base-cnf", type=Path)
    parser.add_argument("--degree", type=int, choices=BRANCH_DEGREES)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()

    if args.base_cnf is None:
        if (
            args.degree is not None
            or args.output is not None
            or args.metadata is not None
        ):
            raise SystemExit(
                "--degree/--output/--metadata require --base-cnf; "
                "use --plan alone"
            )
        result = build_plan()
    else:
        if args.degree is None or args.output is None:
            raise SystemExit("--base-cnf requires --degree and --output")
        result = write_cnf(args.base_cnf, args.output, degree=args.degree)

    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    destination = args.metadata if args.base_cnf is not None else args.plan
    if destination:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
