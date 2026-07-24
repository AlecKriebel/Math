#!/usr/bin/env python3
"""Independent checker for the side-wise degree-order branch plan."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, Iterator, Sequence


ORDER = 43
BRANCH_DEGREES = (18, 19, 20)
PRIMARY_VARIABLE_COUNT = math.comb(ORDER, 2)
BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
BASE_CNF_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)
BASE_METADATA_SHA256 = (
    "88906686b2554cf1b5b9051eae4a200b878944278ed91682b78d9f40d43cf70c"
)
CHECKER_ID = "ramsey55.global_side_degree_order_checker.v1"


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


def dimacs_clauses(path: Path) -> tuple[tuple[int, int], Iterator[tuple[int, ...]]]:
    """Return a DIMACS header and a strict streaming clause iterator."""

    source = path.open("r", encoding="ascii")
    header: tuple[int, int] | None = None

    def clauses() -> Iterator[tuple[int, ...]]:
        nonlocal header
        try:
            for line_number, raw in enumerate(source, start=1):
                stripped = raw.strip()
                if not stripped or stripped.startswith("c"):
                    continue
                fields = stripped.split()
                if fields[0] == "p":
                    if (
                        header is not None
                        or len(fields) != 4
                        or fields[1] != "cnf"
                    ):
                        raise ValueError(
                            f"{path}:{line_number}: malformed problem line"
                        )
                    header = (int(fields[2]), int(fields[3]))
                    continue
                if header is None:
                    raise ValueError(
                        f"{path}:{line_number}: clause precedes problem line"
                    )
                values = tuple(map(int, fields))
                if not values or values[-1] != 0 or 0 in values[:-1]:
                    raise ValueError(
                        f"{path}:{line_number}: malformed clause terminator"
                    )
                yield values[:-1]
        finally:
            source.close()

    iterator = clauses()
    # Advance only until the header is seen; valid production files put it
    # before the first clause.  Pulling the first clause would complicate a
    # genuinely streaming comparison, so scan the small prefix separately.
    source.close()
    with path.open("r", encoding="ascii") as prefix:
        for line_number, raw in enumerate(prefix, start=1):
            fields = raw.split()
            if not fields or fields[0] == "c":
                continue
            if fields[0] != "p" or len(fields) != 4 or fields[1] != "cnf":
                raise ValueError(
                    f"{path}:{line_number}: expected problem line"
                )
            header = (int(fields[2]), int(fields[3]))
            break
    if header is None:
        raise ValueError(f"{path}: no problem line")

    def fresh_clauses() -> Iterator[tuple[int, ...]]:
        seen_header = False
        observed = 0
        with path.open("r", encoding="ascii") as stream:
            for line_number, raw in enumerate(stream, start=1):
                stripped = raw.strip()
                if not stripped or stripped.startswith("c"):
                    continue
                fields = stripped.split()
                if fields[0] == "p":
                    if seen_header:
                        raise ValueError(
                            f"{path}:{line_number}: duplicate problem line"
                        )
                    seen_header = True
                    continue
                if not seen_header:
                    raise ValueError(
                        f"{path}:{line_number}: clause precedes problem line"
                    )
                values = tuple(map(int, fields))
                if not values or values[-1] != 0 or 0 in values[:-1]:
                    raise ValueError(
                        f"{path}:{line_number}: malformed clause"
                    )
                clause = values[:-1]
                if any(abs(literal) > header[0] for literal in clause):
                    raise ValueError(
                        f"{path}:{line_number}: literal exceeds header"
                    )
                observed += 1
                yield clause
        if observed != header[1]:
            raise ValueError(
                f"{path}: header declares {header[1]} clauses, saw {observed}"
            )

    return header, fresh_clauses()


def edge_variable(left: int, right: int) -> int:
    if left > right:
        left, right = right, left
    if not 0 <= left < right < ORDER:
        raise ValueError("invalid edge")
    return 1 + left * (2 * ORDER - left - 1) // 2 + right - left - 1


def allocate_rows(
    first_auxiliary: int, input_count: int = 42, width: int = 25
) -> tuple[tuple[tuple[int, ...], ...], int]:
    rows: list[tuple[int, ...]] = []
    next_variable = first_auxiliary
    for prefix_length in range(1, input_count + 1):
        row_width = min(prefix_length, width)
        rows.append(tuple(range(next_variable, next_variable + row_width)))
        next_variable += row_width
    return tuple(rows), next_variable


def independently_allocate_counters() -> tuple[
    tuple[tuple[tuple[int, ...], ...], ...],
    tuple[tuple[tuple[int, ...], ...], ...],
]:
    next_variable = PRIMARY_VARIABLE_COUNT + 1
    edges: list[tuple[tuple[int, ...], ...]] = []
    nonedges: list[tuple[tuple[int, ...], ...]] = []
    for _vertex in range(ORDER):
        edge_rows, next_variable = allocate_rows(next_variable)
        nonedge_rows, next_variable = allocate_rows(next_variable)
        edges.append(edge_rows)
        nonedges.append(nonedge_rows)
    if next_variable - 1 != BASE_VARIABLE_COUNT:
        raise AssertionError("independent counter layout has wrong size")
    return tuple(edges), tuple(nonedges)


def reverse_for_rows(
    inputs: Sequence[int], rows: Sequence[Sequence[int]]
) -> Iterator[tuple[int, ...]]:
    if len(inputs) != len(rows):
        raise ValueError("input/row mismatch")
    for index, (literal, current) in enumerate(zip(inputs, rows)):
        if index == 0:
            yield (-current[0], literal)
            continue
        previous = rows[index - 1]
        for offset, variable in enumerate(current):
            if offset == 0:
                yield (-variable, previous[0], literal)
            elif offset >= len(previous):
                yield (-variable, literal)
                yield (-variable, previous[offset - 1])
            else:
                yield (-variable, previous[offset], literal)
                yield (-variable, previous[offset], previous[offset - 1])


def independent_reverse_clauses(
    edge_rows: Sequence[Sequence[Sequence[int]]],
) -> Iterator[tuple[int, ...]]:
    for vertex, rows in enumerate(edge_rows):
        inputs = tuple(
            edge_variable(vertex, other)
            for other in range(ORDER)
            if other != vertex
        )
        yield from reverse_for_rows(inputs, rows)


def strict_bound_units(
    degree: int,
    edge_rows: Sequence[Sequence[Sequence[int]]],
    nonedge_rows: Sequence[Sequence[Sequence[int]]],
) -> tuple[int, ...]:
    if degree == 18:
        return ()
    threshold = ORDER - degree
    units: list[int] = []
    for vertex in range(ORDER):
        units.append(-edge_rows[vertex][-1][threshold - 1])
        units.append(-nonedge_rows[vertex][-1][threshold - 1])
    return tuple(units)


def independent_branch_units(
    degree: int,
    edge_rows: Sequence[Sequence[Sequence[int]]],
    nonedge_rows: Sequence[Sequence[Sequence[int]]],
) -> tuple[int, ...]:
    star = tuple(
        edge_variable(0, other)
        if other <= degree
        else -edge_variable(0, other)
        for other in range(1, ORDER)
    )
    return star + strict_bound_units(degree, edge_rows, nonedge_rows)


def independent_order_clauses(
    degree: int,
    edge_rows: Sequence[Sequence[Sequence[int]]],
) -> Iterator[tuple[int, ...]]:
    sides = (
        tuple(range(1, degree + 1)),
        tuple(range(degree + 1, ORDER)),
    )
    for side in sides:
        for left, right in zip(side, side[1:]):
            for threshold in range(degree + 1, ORDER - degree):
                yield (
                    -edge_rows[left][-1][threshold - 1],
                    edge_rows[right][-1][threshold - 1],
                )


def intended_rows(bits: Sequence[bool], width: int = 25) -> tuple[
    tuple[bool, ...], ...
]:
    count = 0
    result: list[tuple[bool, ...]] = []
    for index, bit in enumerate(bits):
        count += int(bit)
        result.append(
            tuple(count >= threshold for threshold in range(1, min(index + 1, width) + 1))
        )
    return tuple(result)


def clause_value(clause: Sequence[int], assignment: dict[int, bool]) -> bool:
    return any(assignment[abs(literal)] == (literal > 0) for literal in clause)


def exhaustive_reverse_semantics(max_inputs: int = 7) -> bool:
    """Check reverse+forward recurrence truth tables on small counters."""

    for input_count in range(1, max_inputs + 1):
        width = min(4, input_count)
        inputs = tuple(range(1, input_count + 1))
        rows, _ = allocate_rows(input_count + 1, input_count, width)
        reverse = tuple(reverse_for_rows(inputs, rows))
        for values in itertools.product((False, True), repeat=input_count):
            intended = intended_rows(values, width)
            assignment = {
                variable: value for variable, value in zip(inputs, values)
            }
            for row_variables, row_values in zip(rows, intended):
                assignment.update(zip(row_variables, row_values))
            if not all(clause_value(clause, assignment) for clause in reverse):
                return False

            # Independently enumerate every auxiliary valuation for the
            # smallest sizes and verify that the forward recurrence plus the
            # added reverse clauses has exactly the intended valuation.
            if input_count <= 4:
                auxiliary = tuple(
                    variable for row in rows for variable in row
                )
                satisfying = 0
                for aux_values in itertools.product(
                    (False, True), repeat=len(auxiliary)
                ):
                    trial = {
                        variable: value
                        for variable, value in zip(inputs, values)
                    }
                    trial.update(zip(auxiliary, aux_values))
                    forward: list[tuple[int, ...]] = []
                    for index, literal in enumerate(inputs):
                        current = rows[index]
                        forward.append((-literal, current[0]))
                        if index == 0:
                            continue
                        previous = rows[index - 1]
                        for offset in range(min(len(previous), len(current))):
                            forward.append((-previous[offset], current[offset]))
                        for offset in range(1, len(current)):
                            forward.append(
                                (-literal, -previous[offset - 1], current[offset])
                            )
                    if all(
                        clause_value(clause, trial)
                        for clause in (*forward, *reverse)
                    ):
                        satisfying += 1
                        actual = tuple(
                            tuple(trial[variable] for variable in row)
                            for row in rows
                        )
                        if actual != intended:
                            return False
                if satisfying != 1:
                    return False
    return True


def check_plan(plan_path: Path) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if plan.get("schema") != "ramsey55.global_side_degree_order.v1":
        errors.append("schema mismatch")
    if plan.get("base_cnf_sha256") != BASE_CNF_SHA256:
        errors.append("base CNF hash mismatch")
    if plan.get("base_metadata_sha256") != BASE_METADATA_SHA256:
        errors.append("base metadata hash mismatch")
    if plan.get("base_variable_count") != BASE_VARIABLE_COUNT:
        errors.append("base variable count mismatch")
    if plan.get("base_clause_count") != BASE_CLAUSE_COUNT:
        errors.append("base clause count mismatch")

    edge_rows, nonedge_rows = independently_allocate_counters()
    reverse = tuple(independent_reverse_clauses(edge_rows))
    if plan.get("reverse_clause_count") != len(reverse):
        errors.append("reverse clause count mismatch")
    if plan.get("reverse_clause_stream_sha256") != clause_stream_sha256(reverse):
        errors.append("reverse clause hash mismatch")

    branch_results: list[dict[str, object]] = []
    plan_branches = {
        item.get("degree"): item for item in plan.get("branches", [])
    }
    if set(plan_branches) != set(BRANCH_DEGREES):
        errors.append("branch degree set mismatch")

    for degree in BRANCH_DEGREES:
        recorded = plan_branches.get(degree, {})
        units = independent_branch_units(
            degree, edge_rows, nonedge_rows
        )
        ordering = tuple(independent_order_clauses(degree, edge_rows))
        additions = tuple((literal,) for literal in units) + reverse + ordering
        local_errors: list[str] = []
        expected = {
            "root_star_and_bound_unit_count": len(units),
            "degree_order_clause_count": len(ordering),
            "degree_order_clause_stream_sha256": clause_stream_sha256(ordering),
            "appended_clause_count": len(additions),
            "appended_clause_stream_sha256": clause_stream_sha256(additions),
            "variable_count": BASE_VARIABLE_COUNT,
            "clause_count": BASE_CLAUSE_COUNT + len(additions),
        }
        for key, value in expected.items():
            if recorded.get(key) != value:
                local_errors.append(f"{key} mismatch")
        errors.extend(f"degree {degree}: {error}" for error in local_errors)
        branch_results.append(
            {
                "degree": degree,
                "unit_count": len(units),
                "order_clause_count": len(ordering),
                "appended_clause_count": len(additions),
                "errors": local_errors,
            }
        )

    semantics = exhaustive_reverse_semantics()
    if not semantics:
        errors.append("small exhaustive reverse semantics failed")

    return {
        "checker": CHECKER_ID,
        "plan_sha256": sha256_file(plan_path),
        "independent_variable_count": BASE_VARIABLE_COUNT,
        "independent_reverse_clause_count": len(reverse),
        "small_exhaustive_reverse_semantics": semantics,
        "branch_results": branch_results,
        "errors": errors,
        "valid": not errors,
        "claim_limit": (
            "This checks the exact symmetry-breaking cover and clause plan; "
            "it does not establish SAT or UNSAT."
        ),
    }


def check_materialized(
    *,
    base_cnf: Path,
    cnf: Path,
    metadata_path: Path,
    degree: int,
) -> dict[str, object]:
    """Compare a materialized formula clause-for-clause to reconstruction."""

    errors: list[str] = []
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if degree not in BRANCH_DEGREES:
        errors.append("invalid requested degree")
    if sha256_file(base_cnf) != BASE_CNF_SHA256:
        errors.append("base CNF SHA-256 mismatch")
    actual_cnf_sha256 = sha256_file(cnf)
    if metadata.get("cnf_sha256") != actual_cnf_sha256:
        errors.append("materialized CNF SHA-256 mismatch")
    if metadata.get("degree") != degree:
        errors.append("metadata degree mismatch")

    edge_rows, nonedge_rows = independently_allocate_counters()
    reverse = tuple(independent_reverse_clauses(edge_rows))
    units = independent_branch_units(degree, edge_rows, nonedge_rows)
    ordering = tuple(independent_order_clauses(degree, edge_rows))
    expected_additions = (
        tuple((literal,) for literal in units) + reverse + ordering
    )
    if metadata.get("appended_clause_count") != len(expected_additions):
        errors.append("metadata appended-clause count mismatch")
    expected_append_hash = clause_stream_sha256(expected_additions)
    if metadata.get("appended_clause_stream_sha256") != expected_append_hash:
        errors.append("metadata appended-clause hash mismatch")

    try:
        base_header, base_iterator = dimacs_clauses(base_cnf)
        cnf_header, cnf_iterator = dimacs_clauses(cnf)
        if base_header != (BASE_VARIABLE_COUNT, BASE_CLAUSE_COUNT):
            errors.append("base DIMACS header mismatch")
        expected_header = (
            BASE_VARIABLE_COUNT,
            BASE_CLAUSE_COUNT + len(expected_additions),
        )
        if cnf_header != expected_header:
            errors.append("materialized DIMACS header mismatch")

        prefix_mismatches = 0
        missing_prefix = 0
        for expected in base_iterator:
            try:
                actual = next(cnf_iterator)
            except StopIteration:
                missing_prefix += 1
                break
            if actual != expected:
                prefix_mismatches += 1
        appended_mismatches = 0
        missing_appended = 0
        for expected in expected_additions:
            try:
                actual = next(cnf_iterator)
            except StopIteration:
                missing_appended += 1
                break
            if actual != expected:
                appended_mismatches += 1
        try:
            extra_clause = next(cnf_iterator)
        except StopIteration:
            extra_clause = None
        if prefix_mismatches:
            errors.append(f"{prefix_mismatches} base-prefix clause mismatches")
        if missing_prefix:
            errors.append("materialized CNF ended inside base prefix")
        if appended_mismatches:
            errors.append(
                f"{appended_mismatches} appended clause mismatches"
            )
        if missing_appended:
            errors.append("materialized CNF ended inside appended clauses")
        if extra_clause is not None:
            errors.append("materialized CNF has extra clauses")
    except (OSError, ValueError) as error:
        errors.append(f"DIMACS comparison failed: {error}")
        prefix_mismatches = -1
        appended_mismatches = -1

    return {
        "checker": CHECKER_ID,
        "mode": "materialized_cnf",
        "degree": degree,
        "base_cnf_sha256": sha256_file(base_cnf),
        "cnf_sha256": actual_cnf_sha256,
        "metadata_sha256": sha256_file(metadata_path),
        "expected_appended_clause_count": len(expected_additions),
        "expected_appended_clause_stream_sha256": expected_append_hash,
        "base_prefix_clause_mismatches": prefix_mismatches,
        "appended_clause_mismatches": appended_mismatches,
        "errors": errors,
        "valid": not errors,
        "claim_limit": (
            "This checks the materialized encoding; it does not establish "
            "SAT or UNSAT."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--base-cnf", type=Path)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--degree", type=int, choices=BRANCH_DEGREES)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    materialized_arguments = (
        args.base_cnf,
        args.cnf,
        args.metadata,
        args.degree,
    )
    if args.plan is not None:
        if any(argument is not None for argument in materialized_arguments):
            parser.error("--plan cannot be combined with materialized inputs")
        result = check_plan(args.plan)
    else:
        if any(argument is None for argument in materialized_arguments):
            parser.error(
                "provide --plan, or all of --base-cnf --cnf --metadata "
                "--degree"
            )
        result = check_materialized(
            base_cnf=args.base_cnf,
            cnf=args.cnf,
            metadata_path=args.metadata,
            degree=args.degree,
        )
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
