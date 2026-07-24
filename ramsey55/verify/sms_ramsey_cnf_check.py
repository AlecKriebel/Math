#!/usr/bin/env python3
"""Independent clause-by-clause checker for the PySMS Ramsey encoding.

This module intentionally does not import the production generator or PySMS.
It reconstructs the official row-major edge map, the sequential degree
counter, and both Ramsey clause families directly.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Sequence


CHECKER_ID = "independent_pysms_ramsey_cnf_reconstruction_v1"


def edge_table(order: int) -> dict[tuple[int, int], int]:
    return {
        pair: variable
        for variable, pair in enumerate(
            itertools.combinations(range(order), 2), start=1
        )
    }


def sequential_counter_clauses(
    inputs: Sequence[int],
    count_upto: int,
    at_most: int,
    at_least: int,
    first_auxiliary: int,
) -> tuple[Iterator[tuple[int, ...]], int]:
    """Reconstruct ``pysms.counters.seqCounter`` without importing it."""
    count = len(inputs)
    if count_upto < 1 or count < 1:
        raise ValueError("checker requires a nonempty positive-width counter")
    rows: list[list[int]] = []
    next_variable = first_auxiliary
    for _ in range(count):
        rows.append(
            list(range(next_variable, next_variable + count_upto))
        )
        next_variable += count_upto
    # PySMS allocates this variable and then overwrites its table entry.
    rows[0][0] = inputs[0]

    def clauses() -> Iterator[tuple[int, ...]]:
        for threshold in range(1, count_upto):
            yield (-rows[0][threshold],)
        for index in range(count - 1):
            new_input = inputs[index + 1]
            yield (-new_input, rows[index + 1][0])
            for threshold in range(count_upto):
                yield (-rows[index][threshold], rows[index + 1][threshold])
                yield (
                    rows[index][threshold],
                    new_input,
                    -rows[index + 1][threshold],
                )
                if threshold < count_upto - 1:
                    yield (
                        -rows[index][threshold],
                        -new_input,
                        rows[index + 1][threshold + 1],
                    )
                    yield (
                        rows[index][threshold],
                        -rows[index + 1][threshold + 1],
                    )
        if at_most:
            for index in range(count - 1):
                yield (-rows[index][at_most - 1], -inputs[index + 1])
        if at_least:
            yield (rows[-1][at_least - 1],)

    return clauses(), next_variable


def expected_formula(
    *,
    order: int,
    independent_size: int,
    clique_size: int,
    degree_lower: int,
    degree_upper: int,
) -> tuple[int, int, Iterator[tuple[int, ...]], dict[str, int]]:
    if not 0 < degree_lower <= degree_upper < order:
        raise ValueError("this checker expects positive finite degree bounds")
    edges = edge_table(order)
    next_variable = len(edges) + 1
    counter_clause_lists: list[list[tuple[int, ...]]] = []
    for vertex in range(order):
        incident = [
            edges[tuple(sorted((vertex, other)))]
            for other in range(order)
            if other != vertex
        ]
        clauses, next_variable = sequential_counter_clauses(
            incident,
            degree_upper,
            degree_upper,
            degree_lower,
            next_variable,
        )
        counter_clause_lists.append(list(clauses))
    degree_clause_count = sum(map(len, counter_clause_lists))
    independent_clause_count = math.comb(order, independent_size)
    clique_clause_count = math.comb(order, clique_size)

    def clauses() -> Iterator[tuple[int, ...]]:
        for counter in counter_clause_lists:
            yield from counter
        for vertices in itertools.combinations(range(order), independent_size):
            yield tuple(
                edges[(left, right)]
                for left, right in itertools.combinations(vertices, 2)
            )
        for vertices in itertools.combinations(range(order), clique_size):
            yield tuple(
                -edges[(left, right)]
                for left, right in itertools.combinations(vertices, 2)
            )

    counts = {
        "primary_variable_count": len(edges),
        "auxiliary_variable_count": next_variable - 1 - len(edges),
        "degree_clause_count": degree_clause_count,
        "independent_clause_count": independent_clause_count,
        "clique_clause_count": clique_clause_count,
    }
    clause_count = (
        degree_clause_count
        + independent_clause_count
        + clique_clause_count
    )
    return next_variable - 1, clause_count, clauses(), counts


def check(
    path: Path,
    *,
    order: int,
    independent_size: int,
    clique_size: int,
    degree_lower: int,
    degree_upper: int,
) -> dict[str, object]:
    expected_variables, expected_clauses, expected, counts = expected_formula(
        order=order,
        independent_size=independent_size,
        clique_size=clique_size,
        degree_lower=degree_lower,
        degree_upper=degree_upper,
    )
    digest = hashlib.sha256()
    declared_variables: int | None = None
    declared_clauses: int | None = None
    actual_clause_count = 0
    pending: list[int] = []
    first_mismatch: dict[str, object] | None = None
    with path.open("rb") as source:
        for line_number, raw in enumerate(source, start=1):
            digest.update(raw)
            fields = raw.decode("ascii").split()
            if not fields or fields[0] == "c":
                continue
            if fields[0] == "p":
                if (
                    declared_variables is not None
                    or len(fields) != 4
                    or fields[1] != "cnf"
                ):
                    raise ValueError(f"bad DIMACS header at line {line_number}")
                declared_variables = int(fields[2])
                declared_clauses = int(fields[3])
                continue
            if declared_variables is None:
                raise ValueError("clause precedes the DIMACS header")
            for field in fields:
                literal = int(field)
                if literal:
                    if abs(literal) > declared_variables:
                        raise ValueError("literal exceeds declared variables")
                    pending.append(literal)
                    continue
                actual_clause_count += 1
                try:
                    wanted = next(expected)
                except StopIteration:
                    wanted = None
                observed = tuple(pending)
                if first_mismatch is None and observed != wanted:
                    first_mismatch = {
                        "clause_index": actual_clause_count,
                        "line_number": line_number,
                        "expected": list(wanted) if wanted is not None else None,
                        "actual": list(observed),
                    }
                pending = []
    missing = sum(1 for _ in expected)
    valid = (
        declared_variables == expected_variables
        and declared_clauses == expected_clauses
        and actual_clause_count == expected_clauses
        and first_mismatch is None
        and not pending
        and missing == 0
    )
    result: dict[str, object] = {
        "schema": "ramsey55.sms_cnf_check.v1",
        "checker": CHECKER_ID,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "valid": valid,
        "order": order,
        "independent_size_forbidden": independent_size,
        "clique_size_forbidden": clique_size,
        "degree_lower": degree_lower,
        "degree_upper": degree_upper,
        "cnf_path": str(path.resolve()),
        "cnf_sha256": digest.hexdigest(),
        "cnf_bytes": path.stat().st_size,
        "declared_variable_count": declared_variables,
        "expected_variable_count": expected_variables,
        "declared_clause_count": declared_clauses,
        "actual_clause_count": actual_clause_count,
        "expected_clause_count": expected_clauses,
        "missing_expected_clause_count": missing,
        **counts,
    }
    if pending:
        result["unterminated_literal_count"] = len(pending)
    if first_mismatch is not None:
        result["first_mismatch"] = first_mismatch
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--order", type=int, default=43)
    parser.add_argument("--independent-size", type=int, default=5)
    parser.add_argument("--clique-size", type=int, default=5)
    parser.add_argument("--degree-lower", type=int, default=18)
    parser.add_argument("--degree-upper", type=int, default=24)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    try:
        result = check(
            args.cnf,
            order=args.order,
            independent_size=args.independent_size,
            clique_size=args.clique_size,
            degree_lower=args.degree_lower,
            degree_upper=args.degree_upper,
        )
    except (OSError, UnicodeDecodeError, ValueError) as error:
        result = {
            "schema": "ramsey55.sms_cnf_check.v1",
            "checker": CHECKER_ID,
            "valid": False,
            "error": str(error),
        }
    result["runtime_seconds"] = time.monotonic() - started
    result["checker_source_sha256"] = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, sort_keys=True))
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
