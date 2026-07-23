#!/usr/bin/env python3
"""Independent structural checker for direct diagonal Ramsey CNFs.

This checker deliberately does not import the production generator.  It
reconstructs the primary edge map, every five-set clause, both degree bounds,
and every sequential-counter clause, then compares the DIMACS stream clause
by clause.
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


CHECKER_ID = "ramsey55_direct_xij_cnf_structural_checker_v1"
LOCAL_RAMSEY_NUMBER = 25


def independent_edge_table(order: int) -> dict[tuple[int, int], int]:
    return {
        pair: variable
        for variable, pair in enumerate(
            itertools.combinations(range(order), 2), start=1
        )
    }


def independent_counter(
    literals: Sequence[int],
    bound: int,
    first_auxiliary: int,
) -> tuple[list[tuple[int, ...]], int]:
    """Independently construct forward threshold clauses."""
    count = len(literals)
    if bound < 0:
        return [()], first_auxiliary
    if bound >= count:
        return [], first_auxiliary
    if bound == 0:
        return [(-literal,) for literal in literals], first_auxiliary

    overflow_threshold = bound + 1
    rows: list[list[int]] = []
    next_variable = first_auxiliary
    for prefix in range(1, count + 1):
        row_length = min(prefix, overflow_threshold)
        rows.append(list(range(next_variable, next_variable + row_length)))
        next_variable += row_length

    clauses: list[tuple[int, ...]] = []
    for prefix_index in range(count):
        literal = literals[prefix_index]
        row = rows[prefix_index]
        clauses.append((-literal, row[0]))
        if prefix_index:
            prior = rows[prefix_index - 1]
            clauses.extend(
                (-prior[threshold], row[threshold])
                for threshold in range(len(prior))
            )
            clauses.extend(
                (-literal, -prior[threshold - 1], row[threshold])
                for threshold in range(1, len(row))
            )
    clauses.append((-rows[-1][-1],))
    return clauses, next_variable


def expected_formula(
    order: int,
) -> tuple[int, int, Iterator[tuple[int, ...]], dict[str, int]]:
    edge_table = independent_edge_table(order)
    primary_count = len(edge_table)
    five_subset_count = math.comb(order, 5)
    lower = max(0, order - LOCAL_RAMSEY_NUMBER)
    upper = min(max(0, order - 1), LOCAL_RAMSEY_NUMBER - 1)
    next_variable = primary_count + 1
    counter_clauses: list[tuple[int, ...]] = []

    for vertex in range(order):
        incident = [
            edge_table[tuple(sorted((vertex, other)))]
            for other in range(order)
            if other != vertex
        ]
        upper_clauses, next_variable = independent_counter(
            incident, upper, next_variable
        )
        counter_clauses.extend(upper_clauses)
        nonedge_upper = order - 1 - lower
        lower_clauses, next_variable = independent_counter(
            [-variable for variable in incident],
            nonedge_upper,
            next_variable,
        )
        counter_clauses.extend(lower_clauses)

    def clauses() -> Iterator[tuple[int, ...]]:
        for vertices in itertools.combinations(range(order), 5):
            variables = tuple(
                edge_table[(left, right)]
                for left, right in itertools.combinations(vertices, 2)
            )
            yield tuple(-variable for variable in variables)
            yield variables
        yield from counter_clauses

    counts = {
        "primary_variable_count": primary_count,
        "auxiliary_variable_count": next_variable - 1 - primary_count,
        "five_subset_count": five_subset_count,
        "ramsey_clause_count": 2 * five_subset_count,
        "degree_clause_count": len(counter_clauses),
        "degree_lower": lower,
        "degree_upper": upper,
    }
    return (
        next_variable - 1,
        2 * five_subset_count + len(counter_clauses),
        clauses(),
        counts,
    )


def check_dimacs(path: Path, order: int) -> dict[str, object]:
    expected_variables, expected_count, expected, counts = expected_formula(order)
    digest = hashlib.sha256()
    declared_variables: int | None = None
    declared_clauses: int | None = None
    actual_count = 0
    current: list[int] = []
    first_mismatch: dict[str, object] | None = None
    generator_comment_seen = False

    with path.open("rb") as source:
        for line_number, raw in enumerate(source, start=1):
            digest.update(raw)
            try:
                fields = raw.decode("ascii").split()
            except UnicodeDecodeError as error:
                return {
                    "valid": False,
                    "error": f"non-ASCII input at line {line_number}: {error}",
                }
            if not fields:
                continue
            if fields[0] == "c":
                if fields[1:3] == ["generator", "ramsey55_direct_xij_cnf_v1"]:
                    generator_comment_seen = True
                continue
            if fields[0] == "p":
                if (
                    declared_variables is not None
                    or len(fields) != 4
                    or fields[1] != "cnf"
                ):
                    return {
                        "valid": False,
                        "error": f"invalid or duplicate header at line {line_number}",
                    }
                declared_variables = int(fields[2])
                declared_clauses = int(fields[3])
                continue
            if declared_variables is None:
                return {
                    "valid": False,
                    "error": f"clause before header at line {line_number}",
                }
            for field in fields:
                literal = int(field)
                if literal:
                    if abs(literal) > declared_variables:
                        return {
                            "valid": False,
                            "error": (
                                f"literal outside declared range at line "
                                f"{line_number}"
                            ),
                        }
                    current.append(literal)
                    continue

                actual_count += 1
                try:
                    wanted = next(expected)
                except StopIteration:
                    wanted = None
                observed = tuple(current)
                if first_mismatch is None and observed != wanted:
                    first_mismatch = {
                        "clause_index": actual_count,
                        "line_number": line_number,
                        "expected": list(wanted) if wanted is not None else None,
                        "actual": list(observed),
                    }
                current = []

    missing_expected = 0
    for _ in expected:
        missing_expected += 1
    valid = (
        generator_comment_seen
        and declared_variables == expected_variables
        and declared_clauses == expected_count
        and actual_count == expected_count
        and not current
        and first_mismatch is None
        and missing_expected == 0
    )
    result: dict[str, object] = {
        "checker": CHECKER_ID,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "valid": valid,
        "order": order,
        "cnf_sha256": digest.hexdigest(),
        "cnf_bytes": path.stat().st_size,
        "generator_comment_seen": generator_comment_seen,
        "declared_variable_count": declared_variables,
        "expected_variable_count": expected_variables,
        "declared_clause_count": declared_clauses,
        "actual_clause_count": actual_count,
        "expected_clause_count": expected_count,
        "missing_expected_clause_count": missing_expected,
        **counts,
    }
    if current:
        result["unterminated_literal_count"] = len(current)
    if first_mismatch is not None:
        result["first_mismatch"] = first_mismatch
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--order", type=int, default=43)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    try:
        result = check_dimacs(args.cnf, args.order)
    except (OSError, ValueError) as error:
        result = {
            "checker": CHECKER_ID,
            "valid": False,
            "error": str(error),
        }
    result["runtime_seconds"] = time.monotonic() - started
    result["checker_source_sha256"] = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()
    rendered = json.dumps(result, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(rendered)
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
