#!/usr/bin/env python3
"""Exact histogram audit of all order-three row-sum pure-axis lifts.

After complementing the high-weight binary class words, a pure-axis lift is
equivalent to 24 weight-three blocks on ``Z/9`` in four groups of six.
Columns within each group are interchangeable before mixed cyclotomic
equations are imposed.  This verifier therefore uses four multiplicity
histograms over the 84 triples instead of 24 labeled blocks or twelve
7,056-row QPSK tables.

For each of the 1,756 exact aggregate row-sum words, the model has 336
integer multiplicities and 26 linear equations.  The full audit proves that
all 1,756 words admit at least one pure-axis/signature lift.  This is an
exact reformulation result, not a pruning theorem and not an LP(333)
construction.
"""

from __future__ import annotations

import argparse
import csv
from hashlib import sha256
from io import StringIO
from itertools import combinations
from pathlib import Path
import sys
import time
from typing import Sequence

from ortools.sat.python import cp_model

from verify_lp333_order3_difference_family import (
    CANONICAL_ZERO_EXPONENTS,
    CATALOG_DATA_ROWS,
    CATALOG_HEADER,
    CATALOG_RELATIVE_PATH,
    CATALOG_SHA256,
    ROOTS,
)


ROWS = 9
GROUP_NAMES = ("A_even", "B_even", "A_odd", "B_odd")
EXPECTED_FULL_COVERAGE_DIGEST = (
    "b32aa9116098ea455063d256b37541033d3a9f8eb6ff5e32f57c3d7039fb1049"
)

TRIPLES = tuple(combinations(range(ROWS), 3))
INCIDENCE = tuple(
    tuple(int(row in block) for row in range(ROWS)) for block in TRIPLES
)
INTERSECTIONS = tuple(
    tuple(
        sum(
            row in block and (row + lag) % ROWS in block
            for row in range(ROWS)
        )
        for lag in range(1, 5)
    )
    for block in TRIPLES
)


def catalog_path() -> Path:
    return Path(__file__).resolve().parent / CATALOG_RELATIVE_PATH


def aggregate_catalog() -> tuple[tuple[int, ...], ...]:
    """Load and convert the pinned full-row-sum catalog to aggregate ``t``."""

    payload = catalog_path().read_bytes()
    actual_hash = sha256(payload).hexdigest()
    if actual_hash != CATALOG_SHA256:
        raise AssertionError(
            f"row-sum catalog hash changed: {actual_hash} != {CATALOG_SHA256}"
        )
    rows = list(csv.reader(StringIO(payload.decode("ascii"), newline="")))
    if not rows or tuple(rows[0]) != CATALOG_HEADER:
        raise AssertionError("row-sum catalog header changed")
    zero = tuple(ROOTS[value] for value in CANONICAL_ZERO_EXPONENTS)
    result: list[tuple[int, ...]] = []
    for raw in rows[1:]:
        values = tuple(int(value) for value in raw)
        if len(values) != 2 * ROWS:
            raise AssertionError("catalog row width changed")
        aggregate: list[int] = []
        for row in range(ROWS):
            difference = (
                values[2 * row] - zero[row][0],
                values[2 * row + 1] - zero[row][1],
            )
            if difference[0] % 3 or difference[1] % 3:
                raise AssertionError("catalog row is not x+3t")
            aggregate.extend((difference[0] // 3, difference[1] // 3))
        result.append(tuple(aggregate))
    if len(result) != CATALOG_DATA_ROWS or len(set(result)) != len(result):
        raise AssertionError("aggregate catalog count or uniqueness changed")
    return tuple(result)


def transform_aggregate_c2(
    aggregate: Sequence[int],
) -> tuple[int, ...]:
    """Apply the corrected B reflection to aggregate A/B row sums."""

    if len(aggregate) != 2 * ROWS:
        raise ValueError("aggregate word must have 18 coordinates")
    a_sums = tuple(
        aggregate[2 * row] - aggregate[2 * row + 1]
        for row in range(ROWS)
    )
    b_sums = tuple(
        aggregate[2 * row] + aggregate[2 * row + 1]
        for row in range(ROWS)
    )
    result: list[int] = []
    for row in range(ROWS):
        a_sum = a_sums[row]
        b_sum = b_sums[(3 - row) % ROWS]
        if (a_sum + b_sum) % 2 or (b_sum - a_sum) % 2:
            raise AssertionError("C2 channel sums have incompatible parity")
        result.extend(((a_sum + b_sum) // 2, (b_sum - a_sum) // 2))
    return tuple(result)


def verify_catalog_c2_action() -> dict[str, int]:
    """Verify the exact involution on all 1,756 aggregate words."""

    catalog = aggregate_catalog()
    catalog_set = set(catalog)
    images = tuple(transform_aggregate_c2(word) for word in catalog)
    if set(images) != catalog_set:
        raise AssertionError("corrected C2 does not preserve the aggregate catalog")
    if any(
        transform_aggregate_c2(image) != word
        for word, image in zip(catalog, images, strict=True)
    ):
        raise AssertionError("aggregate C2 action is not involutive")
    fixed = sum(word == image for word, image in zip(catalog, images, strict=True))
    orbits = (len(catalog) + fixed) // 2
    if (fixed, orbits) != (4, 880):
        raise AssertionError("aggregate C2 orbit census changed")
    return {"catalog_words": len(catalog), "fixed_words": fixed, "orbits": orbits}


def build_histogram_model(
    aggregate: Sequence[int],
) -> tuple[cp_model.CpModel, tuple[tuple[cp_model.IntVar, ...], ...]]:
    """Build one exact four-histogram pure-axis lift model."""

    if len(aggregate) != 2 * ROWS:
        raise ValueError("aggregate word must have 18 integer coordinates")
    if any(type(value) is not int for value in aggregate):
        raise ValueError("aggregate coordinates must be integers")

    model = cp_model.CpModel()
    multiplicities = tuple(
        tuple(
            model.new_int_var(0, 6, f"{GROUP_NAMES[group]}_triple_{index}")
            for index in range(len(TRIPLES))
        )
        for group in range(len(GROUP_NAMES))
    )
    for group in range(len(GROUP_NAMES)):
        model.add(sum(multiplicities[group]) == 6).with_name(
            f"{GROUP_NAMES[group]}_has_six_blocks"
        )

    # Group order is E_A,E_B,O_A,O_B.  The exact incidence equations are
    #
    #   O_A-E_A=(Re t-Im t)/2,
    #   E_B-O_B=(Re t+Im t)/2.
    for row in range(ROWS):
        real = aggregate[2 * row]
        imag = aggregate[2 * row + 1]
        if (real - imag) % 2 or (real + imag) % 2:
            raise ValueError("aggregate coordinates have incompatible parity")
        incident = tuple(
            index
            for index in range(len(TRIPLES))
            if INCIDENCE[index][row]
        )
        model.add(
            sum(multiplicities[2][index] for index in incident)
            - sum(multiplicities[0][index] for index in incident)
            == (real - imag) // 2
        ).with_name(f"a_incidence_row_{row}")
        model.add(
            sum(multiplicities[1][index] for index in incident)
            - sum(multiplicities[3][index] for index in incident)
            == (real + imag) // 2
        ).with_name(f"b_incidence_row_{row}")

    # Sum of all 24 binary cyclic intersections must be 18 at lags 1..4.
    for lag_index in range(4):
        model.add(
            sum(
                INTERSECTIONS[index][lag_index] * multiplicities[group][index]
                for group in range(4)
                for index in range(len(TRIPLES))
                if INTERSECTIONS[index][lag_index]
            )
            == 18
        ).with_name(f"difference_family_lag_{lag_index + 1}")
    if len(model.proto.variables) != 336 or len(model.proto.constraints) != 26:
        raise AssertionError("histogram model size changed")
    return model, multiplicities


def replay_histogram(
    aggregate: Sequence[int],
    multiplicities: Sequence[Sequence[int]],
) -> None:
    """Independently replay one integer histogram witness."""

    if len(multiplicities) != 4 or any(
        len(group) != len(TRIPLES) for group in multiplicities
    ):
        raise ValueError("expected four 84-entry multiplicity histograms")
    if any(
        type(value) is not int or not 0 <= value <= 6
        for group in multiplicities
        for value in group
    ):
        raise ValueError("histogram entries must be integers in [0,6]")
    if any(sum(group) != 6 for group in multiplicities):
        raise ValueError("each histogram must contain six blocks")

    for row in range(ROWS):
        degrees = tuple(
            sum(
                multiplicities[group][index] * INCIDENCE[index][row]
                for index in range(len(TRIPLES))
            )
            for group in range(4)
        )
        real = aggregate[2 * row]
        imag = aggregate[2 * row + 1]
        if degrees[2] - degrees[0] != (real - imag) // 2:
            raise ValueError("A incidence equation failed")
        if degrees[1] - degrees[3] != (real + imag) // 2:
            raise ValueError("B incidence equation failed")
    for lag_index in range(4):
        total = sum(
            multiplicities[group][index] * INTERSECTIONS[index][lag_index]
            for group in range(4)
            for index in range(len(TRIPLES))
        )
        if total != 18:
            raise ValueError("difference-family equation failed")


def solve_histogram(
    aggregate: Sequence[int],
    *,
    time_limit: float = 2.0,
    workers: int = 8,
    max_memory_mb: int = 2048,
    random_seed: int = 668,
) -> tuple[str, tuple[tuple[int, ...], ...] | None, float]:
    """Solve and replay one exact histogram lift."""

    model, variables = build_histogram_model(aggregate)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.max_memory_in_mb = max_memory_mb
    solver.parameters.random_seed = random_seed
    status = solver.solve(model)
    name = solver.status_name(status)
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return name, None, solver.wall_time
    witness = tuple(
        tuple(solver.value(variable) for variable in group)
        for group in variables
    )
    replay_histogram(aggregate, witness)
    return name, witness, solver.wall_time


def audit_catalog(
    *,
    start: int = 0,
    stop: int | None = None,
    time_limit: float = 2.0,
    workers: int = 8,
    max_memory_mb: int = 2048,
    random_seed: int = 668,
    progress_interval: int = 100,
) -> dict[str, object]:
    """Audit a half-open catalog range and report exact coverage."""

    catalog = aggregate_catalog()
    actual_stop = len(catalog) if stop is None else stop
    if not 0 <= start <= actual_stop <= len(catalog):
        raise ValueError("audit range is outside the row-sum catalog")
    feasible: list[int] = []
    infeasible: list[int] = []
    unknown: list[int] = []
    worst_time = 0.0
    worst_index = -1
    begin = time.monotonic()
    for index in range(start, actual_stop):
        status, witness, wall_time = solve_histogram(
            catalog[index],
            time_limit=time_limit,
            workers=workers,
            max_memory_mb=max_memory_mb,
            random_seed=random_seed,
        )
        if wall_time > worst_time:
            worst_time, worst_index = wall_time, index
        if witness is not None:
            feasible.append(index)
        elif status == "INFEASIBLE":
            infeasible.append(index)
        else:
            unknown.append(index)
        completed = index - start + 1
        if progress_interval and (
            completed % progress_interval == 0 or index + 1 == actual_stop
        ):
            print(
                f"completed={completed} feasible={len(feasible)} "
                f"infeasible={len(infeasible)} unknown={len(unknown)}",
                flush=True,
            )

    coverage_digest = sha256(
        b"".join(index.to_bytes(2, "little") for index in feasible)
    ).hexdigest()
    full_range = start == 0 and actual_stop == len(catalog)
    if full_range and not infeasible and not unknown:
        if coverage_digest != EXPECTED_FULL_COVERAGE_DIGEST:
            raise AssertionError("full-coverage digest changed")
    return {
        "start": start,
        "stop": actual_stop,
        "tested": actual_stop - start,
        "feasible": len(feasible),
        "infeasible_indices": tuple(infeasible),
        "unknown_indices": tuple(unknown),
        "coverage_digest": coverage_digest,
        "worst_wall_time": worst_time,
        "worst_index": worst_index,
        "elapsed": time.monotonic() - begin,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int)
    parser.add_argument("--time-limit", type=float, default=2.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-memory-mb", type=int, default=2048)
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument("--progress-interval", type=int, default=100)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (
        args.time_limit <= 0
        or args.workers <= 0
        or args.max_memory_mb <= 0
        or args.progress_interval < 0
    ):
        print("error=solver limits must be positive", file=sys.stderr)
        return 2
    try:
        result = audit_catalog(
            start=args.start,
            stop=args.stop,
            time_limit=args.time_limit,
            workers=args.workers,
            max_memory_mb=args.max_memory_mb,
            random_seed=args.random_seed,
            progress_interval=args.progress_interval,
        )
    except (AssertionError, OSError, ValueError) as error:
        print(f"error={error}", file=sys.stderr)
        return 2
    for key, value in result.items():
        print(f"{key}={value}")
    return int(bool(result["infeasible_indices"] or result["unknown_indices"]))


if __name__ == "__main__":
    raise SystemExit(main())
