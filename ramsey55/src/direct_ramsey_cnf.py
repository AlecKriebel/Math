#!/usr/bin/env python3
"""Deterministic direct CNF for diagonal Ramsey (5,5) graphs.

Primary variable ``x_{i,j}`` is true exactly when ``{i,j}`` is an edge.
For every five-set, the generator emits a negative ten-literal clause
forbidding a clique followed by a positive ten-literal clause forbidding an
independent set.

The optional (enabled by default) degree constraints use the theorem
R(4,5) = R(5,4) = 25.  Every vertex of a (5,5)-graph of order n therefore has
degree in [n - 25, 24], intersected with [0,n-1].  Each upper bound is encoded
by a forward sequential threshold counter.  A lower bound on edges is an
upper bound on the corresponding negated edge literals.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import resource
import shutil
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence


GENERATOR_ID = "ramsey55_direct_xij_cnf_v1"
COUNTER_ID = "forward_sequential_threshold_at_most_v1"
FORBIDDEN_SIZE = 5
LOCAL_RAMSEY_NUMBER = 25


def variable_for_edge(order: int, left: int, right: int) -> int:
    """Map an unordered edge to a one-based variable, in lexicographic order."""
    if left > right:
        left, right = right, left
    if not (0 <= left < right < order):
        raise ValueError(f"invalid edge ({left},{right}) for order {order}")
    # Edges preceding first endpoint left, then offset within that block.
    return 1 + left * (2 * order - left - 1) // 2 + (right - left - 1)


def edge_for_variable(order: int, variable: int) -> tuple[int, int]:
    """Inverse of :func:`variable_for_edge`, used in tests and metadata."""
    if not 1 <= variable <= math.comb(order, 2):
        raise ValueError("edge variable is outside the primary range")
    for left in range(order):
        block = order - left - 1
        if variable <= block:
            return left, left + variable
        variable -= block
    raise AssertionError("unreachable edge-variable inverse")


def degree_bounds(
    order: int, local_ramsey_number: int = LOCAL_RAMSEY_NUMBER
) -> tuple[int, int]:
    """Return the sound degree interval derived from R(4,5)=25."""
    if order < 0:
        raise ValueError("order must be nonnegative")
    if local_ramsey_number < 1:
        raise ValueError("local Ramsey number must be positive")
    possible = max(0, order - 1)
    lower = max(0, order - local_ramsey_number)
    upper = min(possible, local_ramsey_number - 1)
    return lower, upper


@dataclass(frozen=True)
class SequentialCounter:
    """An existential CNF encoding of ``sum(input_literals) <= bound``.

    ``rows[i][j]`` represents the forward implication
    "at least j+1 of the first i+1 input literals are true".  Reverse
    implications are unnecessary: forward implications plus a false overflow
    threshold are equisatisfiable with the cardinality constraint.
    """

    input_literals: tuple[int, ...]
    bound: int
    rows: tuple[tuple[int, ...], ...]
    label: str

    @property
    def auxiliary_count(self) -> int:
        return sum(map(len, self.rows))

    def clauses(self) -> Iterator[tuple[int, ...]]:
        literals = self.input_literals
        count = len(literals)
        if self.bound < 0:
            yield ()
            return
        if self.bound >= count:
            return
        if self.bound == 0:
            for literal in literals:
                yield (-literal,)
            return

        width = self.bound + 1
        if len(self.rows) != count or len(self.rows[-1]) != width:
            raise AssertionError("malformed sequential-counter allocation")

        for index, literal in enumerate(literals):
            current = self.rows[index]
            # A true input makes the first threshold true.
            yield (-literal, current[0])
            if index == 0:
                continue
            previous = self.rows[index - 1]
            # Previously reached thresholds remain reached.
            for threshold in range(min(len(previous), len(current))):
                yield (-previous[threshold], current[threshold])
            # A true input advances every previously reached threshold.
            for threshold in range(1, len(current)):
                yield (
                    -literal,
                    -previous[threshold - 1],
                    current[threshold],
                )
        # Reaching bound+1 true inputs is forbidden.
        yield (-self.rows[-1][width - 1],)

    @property
    def clause_count(self) -> int:
        count = len(self.input_literals)
        if self.bound < 0:
            return 1
        if self.bound >= count:
            return 0
        if self.bound == 0:
            return count
        width = self.bound + 1
        input_implications = count
        carry_implications = sum(
            min(prefix, width) for prefix in range(1, count)
        )
        increment_implications = sum(
            min(prefix, width - 1) for prefix in range(1, count)
        )
        return (
            input_implications
            + carry_implications
            + increment_implications
            + 1
        )


def allocate_sequential_counter(
    input_literals: Sequence[int],
    bound: int,
    first_auxiliary: int,
    label: str,
) -> tuple[SequentialCounter, int]:
    """Allocate a deterministic forward counter and return its next free ID."""
    literals = tuple(input_literals)
    if any(literal == 0 for literal in literals):
        raise ValueError("counter input literals must be nonzero")
    if first_auxiliary < 1:
        raise ValueError("first auxiliary variable must be positive")

    if bound <= 0 or bound >= len(literals):
        rows: tuple[tuple[int, ...], ...] = tuple()
        return SequentialCounter(literals, bound, rows, label), first_auxiliary

    width = bound + 1
    next_variable = first_auxiliary
    mutable_rows: list[tuple[int, ...]] = []
    for prefix_length in range(1, len(literals) + 1):
        row_width = min(prefix_length, width)
        row = tuple(range(next_variable, next_variable + row_width))
        mutable_rows.append(row)
        next_variable += row_width
    return (
        SequentialCounter(literals, bound, tuple(mutable_rows), label),
        next_variable,
    )


@dataclass(frozen=True)
class DirectRamseyInstance:
    order: int
    forbidden_size: int
    local_ramsey_number: int
    degree_lower: int
    degree_upper: int
    counters: tuple[SequentialCounter, ...]
    variable_count: int

    @property
    def primary_variable_count(self) -> int:
        return math.comb(self.order, 2)

    @property
    def five_subset_count(self) -> int:
        return math.comb(self.order, self.forbidden_size)

    @property
    def ramsey_clause_count(self) -> int:
        return 2 * self.five_subset_count

    @property
    def degree_clause_count(self) -> int:
        return sum(counter.clause_count for counter in self.counters)

    @property
    def clause_count(self) -> int:
        return self.ramsey_clause_count + self.degree_clause_count

    @property
    def auxiliary_variable_count(self) -> int:
        return self.variable_count - self.primary_variable_count

    def ramsey_clauses(self) -> Iterator[tuple[int, ...]]:
        for vertices in itertools.combinations(
            range(self.order), self.forbidden_size
        ):
            variables = tuple(
                variable_for_edge(self.order, left, right)
                for left, right in itertools.combinations(vertices, 2)
            )
            yield tuple(-variable for variable in variables)
            yield variables

    def clauses(self) -> Iterator[tuple[int, ...]]:
        yield from self.ramsey_clauses()
        for counter in self.counters:
            yield from counter.clauses()


def build_direct_instance(
    order: int,
    *,
    use_degree_bounds: bool = True,
    local_ramsey_number: int = LOCAL_RAMSEY_NUMBER,
) -> DirectRamseyInstance:
    if order < FORBIDDEN_SIZE:
        # Small orders are useful for semantic tests and valid DIMACS output.
        if order < 0:
            raise ValueError("order must be nonnegative")
    primary_count = math.comb(order, 2)
    lower, upper = degree_bounds(order, local_ramsey_number)
    counters: list[SequentialCounter] = []
    next_variable = primary_count + 1

    if use_degree_bounds:
        for vertex in range(order):
            incident = tuple(
                variable_for_edge(order, vertex, other)
                for other in range(order)
                if other != vertex
            )
            upper_counter, next_variable = allocate_sequential_counter(
                incident,
                upper,
                next_variable,
                f"vertex_{vertex}_edges_at_most_{upper}",
            )
            counters.append(upper_counter)

            nonedge_upper = (order - 1) - lower
            lower_counter, next_variable = allocate_sequential_counter(
                tuple(-literal for literal in incident),
                nonedge_upper,
                next_variable,
                f"vertex_{vertex}_nonedges_at_most_{nonedge_upper}",
            )
            counters.append(lower_counter)

    return DirectRamseyInstance(
        order=order,
        forbidden_size=FORBIDDEN_SIZE,
        local_ramsey_number=local_ramsey_number,
        degree_lower=lower,
        degree_upper=upper,
        counters=tuple(counters),
        variable_count=next_variable - 1,
    )


def clause_is_satisfied(
    clause: Sequence[int], assignment: Mapping[int, bool]
) -> bool:
    return any(
        assignment.get(abs(literal), False) == (literal > 0)
        for literal in clause
    )


def canonical_counter_extension(
    counter: SequentialCounter, assignment: Mapping[int, bool]
) -> dict[int, bool]:
    """Return the intended prefix-threshold values for a primary assignment."""
    extension: dict[int, bool] = {}
    true_count = 0
    for index, literal in enumerate(counter.input_literals):
        literal_value = assignment.get(abs(literal), False) == (literal > 0)
        true_count += int(literal_value)
        if counter.rows:
            for threshold, variable in enumerate(counter.rows[index], start=1):
                extension[variable] = true_count >= threshold
    return extension


def _header_lines(instance: DirectRamseyInstance) -> list[str]:
    degree_enabled = bool(instance.counters)
    lines = [
        f"c generator {GENERATOR_ID}",
        f"c order {instance.order}",
        f"c forbidden_size {instance.forbidden_size}",
        (
            "c primary_variables x_i_j in lexicographic pair order "
            "(0,1),(0,2),..."
        ),
        (
            "c Ramsey clause order: for each lexicographic five-set, "
            "negative clique clause then positive independent-set clause"
        ),
        f"c degree_bounds_enabled {str(degree_enabled).lower()}",
        (
            f"c degree_bounds {instance.degree_lower} "
            f"{instance.degree_upper}"
        ),
        (
            "c degree_bound_basis R(4,5)=R(5,4)="
            f"{instance.local_ramsey_number}"
        ),
        f"c counter_encoding {COUNTER_ID}",
        (
            "c counter_order: for each vertex, edge upper bound then "
            "nonedge upper bound"
        ),
        (
            f"c counts primary {instance.primary_variable_count} "
            f"auxiliary {instance.auxiliary_variable_count} "
            f"five_subsets {instance.five_subset_count} "
            f"ramsey_clauses {instance.ramsey_clause_count} "
            f"degree_clauses {instance.degree_clause_count}"
        ),
        f"p cnf {instance.variable_count} {instance.clause_count}",
    ]
    return lines


def estimated_file_upper_bound(instance: DirectRamseyInstance) -> int:
    """Conservative byte bound for the generated ASCII DIMACS file."""
    digits = len(str(max(1, instance.variable_count)))
    header_bytes = sum(len(line) + 1 for line in _header_lines(instance))
    total = header_bytes
    for width, count in (
        (10, instance.ramsey_clause_count),
        (3, instance.degree_clause_count),
    ):
        # sign + digits + separator per literal, plus "0\n".
        total += count * (width * (digits + 2) + 2)
    return total


class _HashingWriter:
    def __init__(self, raw: object) -> None:
        self.raw = raw
        self.digest = hashlib.sha256()
        self.bytes_written = 0

    def write_ascii(self, line: str) -> None:
        data = line.encode("ascii")
        self.raw.write(data)  # type: ignore[attr-defined]
        self.digest.update(data)
        self.bytes_written += len(data)


def write_dimacs(instance: DirectRamseyInstance, output: Path) -> dict[str, object]:
    """Stream a DIMACS instance atomically and return measured generation data."""
    output.parent.mkdir(parents=True, exist_ok=True)
    started_wall = time.monotonic()
    started_cpu = time.process_time()
    clause_count = 0
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=output.name + ".",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as raw:
            temporary_name = raw.name
            writer = _HashingWriter(raw)
            for line in _header_lines(instance):
                writer.write_ascii(line + "\n")
            for clause in instance.clauses():
                writer.write_ascii(" ".join(map(str, clause)) + " 0\n")
                clause_count += 1
            raw.flush()
            os.fsync(raw.fileno())
        if clause_count != instance.clause_count:
            raise AssertionError(
                f"generated {clause_count} clauses, expected {instance.clause_count}"
            )
        os.replace(temporary_name, output)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)

    return {
        "cnf_sha256": writer.digest.hexdigest(),
        "cnf_bytes": writer.bytes_written,
        "generation_wall_seconds": time.monotonic() - started_wall,
        "generation_cpu_seconds": time.process_time() - started_cpu,
        "generation_max_rss_bytes": resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss,
    }


def metadata_for_instance(
    instance: DirectRamseyInstance,
    output: Path | None,
    measurements: Mapping[str, object] | None = None,
) -> dict[str, object]:
    source_path = Path(__file__).resolve()
    free_bytes = shutil.disk_usage(
        output.parent if output is not None else Path.cwd()
    ).free
    result: dict[str, object] = {
        "generator": GENERATOR_ID,
        "counter_encoding": COUNTER_ID,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "order": instance.order,
        "forbidden_size": instance.forbidden_size,
        "primary_variable_semantics": "x_i_j=true iff {i,j} is an edge",
        "primary_variable_order": "lexicographic unordered vertex pairs",
        "primary_variable_count": instance.primary_variable_count,
        "auxiliary_variable_count": instance.auxiliary_variable_count,
        "variable_count": instance.variable_count,
        "five_subset_count": instance.five_subset_count,
        "ramsey_clause_count": instance.ramsey_clause_count,
        "ramsey_clause_width": math.comb(instance.forbidden_size, 2),
        "degree_bounds_enabled": bool(instance.counters),
        "degree_lower": instance.degree_lower,
        "degree_upper": instance.degree_upper,
        "degree_bound_theorem_dependency": (
            f"R(4,5)=R(5,4)={instance.local_ramsey_number}"
        ),
        "degree_counter_count": len(instance.counters),
        "degree_clause_count": instance.degree_clause_count,
        "clause_count": instance.clause_count,
        "estimated_file_upper_bound_bytes": estimated_file_upper_bound(instance),
        "free_bytes_before_generation_or_estimate": free_bytes,
        "generator_source_sha256": hashlib.sha256(
            source_path.read_bytes()
        ).hexdigest(),
        "cnf_path": str(output.resolve()) if output is not None else None,
        "solve_attempted": False,
    }
    if measurements:
        result.update(measurements)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=43)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--no-degree-bounds", action="store_true")
    parser.add_argument("--estimate-only", action="store_true")
    args = parser.parse_args()

    if args.order < 0:
        raise SystemExit("order must be nonnegative")
    if not args.estimate_only and args.output is None:
        raise SystemExit("--output is required unless --estimate-only is used")

    instance = build_direct_instance(
        args.order, use_degree_bounds=not args.no_degree_bounds
    )
    metadata = metadata_for_instance(instance, args.output)
    if not args.estimate_only:
        assert args.output is not None
        required = int(metadata["estimated_file_upper_bound_bytes"])
        free = int(metadata["free_bytes_before_generation_or_estimate"])
        if required * 2 > free:
            raise SystemExit(
                "refusing generation: conservative output estimate does not "
                "leave a 2x free-space margin"
            )
        measurements = write_dimacs(instance, args.output)
        metadata.update(measurements)

    if args.metadata:
        args.metadata.parent.mkdir(parents=True, exist_ok=True)
        args.metadata.write_text(
            json.dumps(metadata, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
