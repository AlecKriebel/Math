#!/usr/bin/env python3
"""Independent checker for the degree-19/20 Ramsey-anchor cube cover.

The checker deliberately does not import the production cover generator.  It
reconstructs edge variables, direct-counter final thresholds, all 65,536
cross matrices, the S4 x S4 action, cube assumptions, selector clauses, and
the primary-only signature-order clauses.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Generator, Iterable, Sequence


CHECKER_ID = "ramsey55.global_anchor_cube_cover_checker.v1"
SCHEMA = "ramsey55.global_anchor_cube_cover.v1"
ORDER = 43
DEGREES = (19, 20)
BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
BASE_CNF_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)
BASE_METADATA_SHA256 = (
    "88906686b2554cf1b5b9051eae4a200b878944278ed91682b78d9f40d43cf70c"
)
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def clause_hash(clauses: Iterable[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return digest.hexdigest()


def units_hash(units: Sequence[int]) -> str:
    return clause_hash((literal,) for literal in units)


def edge_map() -> dict[tuple[int, int], int]:
    return {
        pair: index
        for index, pair in enumerate(
            itertools.combinations(range(ORDER), 2), start=1
        )
    }


def allocate_final(
    first: int, input_count: int, bound: int
) -> tuple[tuple[int, ...], int]:
    width = bound + 1
    final: tuple[int, ...] = ()
    for prefix in range(1, input_count + 1):
        row_width = min(prefix, width)
        final = tuple(range(first, first + row_width))
        first += row_width
    return final, first


def counter_finals() -> tuple[tuple[tuple[int, ...], ...], int]:
    next_variable = math.comb(ORDER, 2) + 1
    finals: list[tuple[int, ...]] = []
    for _vertex in range(ORDER):
        final, next_variable = allocate_final(next_variable, 42, 24)
        finals.append(final)
        final, next_variable = allocate_final(next_variable, 42, 24)
        finals.append(final)
    return tuple(finals), next_variable - 1


def branch_units(degree: int) -> tuple[int, ...]:
    pairs = edge_map()
    star = tuple(
        pairs[(0, vertex)] if vertex <= degree else -pairs[(0, vertex)]
        for vertex in range(1, ORDER)
    )
    finals, variable_count = counter_finals()
    if variable_count != BASE_VARIABLE_COUNT:
        raise AssertionError("independent direct-counter layout changed")
    threshold = ORDER - degree
    strict = tuple(
        -finals[2 * vertex + kind][threshold - 1]
        for vertex in range(ORDER)
        for kind in (0, 1)
    )
    return star + strict


def anchor_vertices(degree: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return tuple(range(1, 5)), tuple(range(degree + 1, degree + 5))


def anchor_units(degree: int) -> tuple[int, ...]:
    pairs = edge_map()
    side_a, side_b = anchor_vertices(degree)
    return tuple(
        -pairs[pair] for pair in itertools.combinations(side_a, 2)
    ) + tuple(pairs[pair] for pair in itertools.combinations(side_b, 2))


def bit(matrix: int, row: int, column: int) -> int:
    return (matrix >> (4 * row + column)) & 1


def feasible(matrix: int) -> bool:
    return all(
        any(not bit(matrix, row, column) for column in range(4))
        for row in range(4)
    ) and all(
        any(bit(matrix, row, column) for row in range(4))
        for column in range(4)
    )


def transform(
    matrix: int, row_permutation: Sequence[int], column_permutation: Sequence[int]
) -> int:
    result = 0
    for row in range(4):
        for column in range(4):
            if bit(matrix, row, column):
                result |= 1 << (
                    4 * row_permutation[row] + column_permutation[column]
                )
    return result


@functools.lru_cache(maxsize=None)
def orbit(matrix: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                transform(matrix, row_permutation, column_permutation)
                for row_permutation in PERMUTATIONS4
                for column_permutation in PERMUTATIONS4
            }
        )
    )


def representatives_and_owner() -> tuple[tuple[int, ...], dict[int, int]]:
    representatives: list[int] = []
    owner: dict[int, int] = {}
    for matrix in range(1 << 16):
        if not feasible(matrix) or matrix in owner:
            continue
        members = orbit(matrix)
        representative = min(members)
        representatives.append(representative)
        for member in members:
            if not feasible(member) or member in owner:
                raise AssertionError("orbit partition failure")
            owner[member] = representative
    return tuple(sorted(representatives)), owner


def matrix_units(degree: int, matrix: int) -> tuple[int, ...]:
    pairs = edge_map()
    side_a, side_b = anchor_vertices(degree)
    return tuple(
        (
            pairs[tuple(sorted((side_a[row], side_b[column])))]
            if bit(matrix, row, column)
            else -pairs[tuple(sorted((side_a[row], side_b[column])))]
        )
        for row in range(4)
        for column in range(4)
    )


def signature(degree: int, vertex: int) -> tuple[int, ...]:
    pairs = edge_map()
    side_a, side_b = anchor_vertices(degree)
    return tuple(
        pairs[tuple(sorted((vertex, anchor)))]
        for anchor in (*side_a, *side_b)
    )


def lex_clauses(
    left: Sequence[int], right: Sequence[int]
) -> Iterable[tuple[int, ...]]:
    for index in range(len(left)):
        for prefix in itertools.product((0, 1), repeat=index):
            clause: list[int] = []
            for offset, value in enumerate(prefix):
                clause.extend(
                    (-left[offset], -right[offset])
                    if value
                    else (left[offset], right[offset])
                )
            clause.extend((-left[index], right[index]))
            yield tuple(clause)


def sort_clauses(degree: int) -> Iterable[tuple[int, ...]]:
    side_a = tuple(range(8, degree + 1))
    side_b = tuple(range(degree + 8, ORDER))
    for side in (side_a, side_b):
        for left, right in zip(side, side[1:]):
            yield from lex_clauses(
                signature(degree, left), signature(degree, right)
            )


def witness_clauses(
    degree: int, first_selector: int = BASE_VARIABLE_COUNT + 1 + 143
) -> Iterable[tuple[int, ...]]:
    pairs = edge_map()
    anchor_a, anchor_b = anchor_vertices(degree)
    free_a = (5, 6, 7)
    free_b = (degree + 5, degree + 6, degree + 7)
    triangle_patterns = [
        tuple(
            pairs[tuple(sorted(pair))]
            for pair in itertools.combinations(free_a, 2)
        )
    ]
    for anchor in anchor_a:
        triangle_patterns.append(
            (
                pairs[tuple(sorted((anchor, free_a[0])))],
                pairs[tuple(sorted((anchor, free_a[1])))],
                pairs[tuple(sorted((free_a[0], free_a[1])))],
            )
        )
    independent_patterns = [
        tuple(
            -pairs[tuple(sorted(pair))]
            for pair in itertools.combinations(free_b, 2)
        )
    ]
    for anchor in anchor_b:
        independent_patterns.append(
            (
                -pairs[tuple(sorted((anchor, free_b[0])))],
                -pairs[tuple(sorted((anchor, free_b[1])))],
                -pairs[tuple(sorted((free_b[0], free_b[1])))],
            )
        )
    triangle_selectors = tuple(range(first_selector, first_selector + 5))
    independent_selectors = tuple(
        range(first_selector + 5, first_selector + 10)
    )
    yield triangle_selectors
    for selector, pattern in zip(triangle_selectors, triangle_patterns):
        for literal in pattern:
            yield (-selector, literal)
    yield independent_selectors
    for selector, pattern in zip(independent_selectors, independent_patterns):
        for literal in pattern:
            yield (-selector, literal)


def allocate_counter_clauses(
    input_literals: Sequence[int], bound: int, first_auxiliary: int
) -> tuple[tuple[tuple[int, ...], ...], int, int]:
    """Independently allocate the forward threshold encoding."""

    width = bound + 1
    rows: list[tuple[int, ...]] = []
    next_variable = first_auxiliary
    for prefix_length in range(1, len(input_literals) + 1):
        row_width = min(prefix_length, width)
        rows.append(
            tuple(range(next_variable, next_variable + row_width))
        )
        next_variable += row_width
    clauses: list[tuple[int, ...]] = []
    for index, literal in enumerate(input_literals):
        current = rows[index]
        clauses.append((-literal, current[0]))
        if index == 0:
            continue
        previous = rows[index - 1]
        for threshold in range(min(len(previous), len(current))):
            clauses.append((-previous[threshold], current[threshold]))
        for threshold in range(1, len(current)):
            clauses.append(
                (-literal, -previous[threshold - 1], current[threshold])
            )
    clauses.append((-rows[-1][width - 1],))
    return tuple(clauses), next_variable, next_variable - first_auxiliary


def local_counter_data(
    degree: int, first_auxiliary: int = BASE_VARIABLE_COUNT + 1 + 143 + 10
) -> tuple[tuple[tuple[int, ...], ...], int, int, int]:
    pairs = edge_map()
    side_a = tuple(range(1, degree + 1))
    side_b = tuple(range(degree + 1, ORDER))
    all_clauses: list[tuple[int, ...]] = []
    next_variable = first_auxiliary
    auxiliary_count = 0
    counter_count = 0
    for side, upper_bound, nonedge_bound in (
        (side_a, 13, 17),
        (side_b, 17, 13),
    ):
        for vertex in side:
            internal = tuple(
                pairs[tuple(sorted((vertex, other)))]
                for other in side
                if other != vertex
            )
            for literals, bound in (
                (internal, upper_bound),
                (tuple(-literal for literal in internal), nonedge_bound),
            ):
                clauses, next_variable, allocated = allocate_counter_clauses(
                    literals, bound, next_variable
                )
                all_clauses.extend(clauses)
                auxiliary_count += allocated
                counter_count += 1
    return (
        tuple(all_clauses),
        next_variable - 1,
        auxiliary_count,
        counter_count,
    )


def appended_clauses(
    degree: int,
    representatives: Sequence[int],
    *,
    include_local_degree_counters: bool = False,
) -> Iterable[tuple[int, ...]]:
    common = branch_units(degree) + anchor_units(degree)
    for literal in common:
        yield (literal,)
    selectors = tuple(
        range(BASE_VARIABLE_COUNT + 1, BASE_VARIABLE_COUNT + 1 + len(representatives))
    )
    yield selectors
    for selector, matrix in zip(selectors, representatives):
        for literal in matrix_units(degree, matrix):
            yield (-selector, literal)
    yield from witness_clauses(degree)
    yield from sort_clauses(degree)
    if include_local_degree_counters:
        local_clauses, _last_variable, _auxiliary_count, _counter_count = (
            local_counter_data(degree)
        )
        yield from local_clauses


def lex_semantics_exhaustive() -> bool:
    """Exhaustively validate the clause template at widths zero through eight."""

    for width in range(1, 9):
        left_variables = tuple(range(1, width + 1))
        right_variables = tuple(range(width + 1, 2 * width + 1))
        clauses = tuple(lex_clauses(left_variables, right_variables))
        for left_value in range(1 << width):
            for right_value in range(1 << width):
                assignment = {
                    left_variables[index]: bool(
                        left_value & (1 << (width - 1 - index))
                    )
                    for index in range(width)
                }
                assignment.update(
                    {
                        right_variables[index]: bool(
                            right_value & (1 << (width - 1 - index))
                        )
                        for index in range(width)
                    }
                )
                accepted = all(
                    any(
                        assignment[abs(literal)] == (literal > 0)
                        for literal in clause
                    )
                    for clause in clauses
                )
                if accepted != (left_value <= right_value):
                    return False
    return True


def dimacs_stream(
    path: Path,
) -> Generator[tuple[int, ...], None, dict[str, int]]:
    variables: int | None = None
    declared_clauses: int | None = None
    actual_clauses = 0
    pending: list[int] = []
    with path.open("r", encoding="ascii") as source:
        for line_number, line in enumerate(source, start=1):
            fields = line.split()
            if not fields or fields[0] == "c":
                continue
            if fields[0] == "p":
                if (
                    variables is not None
                    or len(fields) != 4
                    or fields[1] != "cnf"
                ):
                    raise ValueError(
                        f"{path}: malformed/duplicate header at line {line_number}"
                    )
                variables = int(fields[2])
                declared_clauses = int(fields[3])
                continue
            if variables is None:
                raise ValueError(f"{path}: clause before header")
            for field in fields:
                literal = int(field)
                if literal:
                    if abs(literal) > variables:
                        raise ValueError(f"{path}: literal outside declared range")
                    pending.append(literal)
                else:
                    actual_clauses += 1
                    yield tuple(pending)
                    pending = []
    if pending:
        raise ValueError(f"{path}: unterminated final clause")
    if variables is None or declared_clauses is None:
        raise ValueError(f"{path}: missing DIMACS header")
    return {
        "variable_count": variables,
        "declared_clause_count": declared_clauses,
        "actual_clause_count": actual_clauses,
    }


def next_clause_or_summary(
    stream: Generator[tuple[int, ...], None, dict[str, int]],
) -> tuple[tuple[int, ...] | None, dict[str, int] | None]:
    try:
        return next(stream), None
    except StopIteration as stopped:
        return None, stopped.value


def check_materialized_union(
    *,
    base_cnf: Path,
    union_cnf: Path,
    metadata_path: Path,
    degree: int,
    representatives: Sequence[int],
) -> dict[str, object]:
    if degree not in DEGREES:
        raise ValueError(f"union degree must be one of {DEGREES}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    include_local_degree_counters = (
        metadata.get("local_degree_counters_enabled") is True
    )
    base_stream = dimacs_stream(base_cnf)
    union_stream = dimacs_stream(union_cnf)
    base_summary: dict[str, int] | None = None
    union_summary: dict[str, int] | None = None
    first_mismatch: dict[str, object] | None = None
    copied = 0
    while base_summary is None:
        expected, base_summary = next_clause_or_summary(base_stream)
        if base_summary is not None:
            break
        actual, union_summary = next_clause_or_summary(union_stream)
        if union_summary is not None:
            first_mismatch = {
                "kind": "union_ended_inside_base",
                "clause_index": copied + 1,
            }
            break
        copied += 1
        if first_mismatch is None and expected != actual:
            first_mismatch = {
                "kind": "copied_base_clause",
                "clause_index": copied,
                "expected": list(expected or ()),
                "actual": list(actual or ()),
            }

    expected_additions = tuple(
        appended_clauses(
            degree,
            representatives,
            include_local_degree_counters=include_local_degree_counters,
        )
    )
    observed_additions: list[tuple[int, ...]] = []
    if union_summary is None:
        while True:
            clause, union_summary = next_clause_or_summary(union_stream)
            if union_summary is not None:
                break
            assert clause is not None
            observed_additions.append(clause)
    assert base_summary is not None
    assert union_summary is not None

    if include_local_degree_counters:
        (
            _local_clauses,
            expected_variable_count,
            _local_auxiliary_count,
            _local_counter_count,
        ) = local_counter_data(degree)
    else:
        expected_variable_count = BASE_VARIABLE_COUNT + 143 + 10
    expected_clause_count = BASE_CLAUSE_COUNT + len(expected_additions)
    union_sha = sha256_file(union_cnf)
    metadata_sha = sha256_file(metadata_path)
    checks = {
        "base_declared_count": (
            base_summary["declared_clause_count"] == BASE_CLAUSE_COUNT
            and base_summary["actual_clause_count"] == BASE_CLAUSE_COUNT
            and base_summary["variable_count"] == BASE_VARIABLE_COUNT
        ),
        "all_base_clauses_copied": (
            first_mismatch is None and copied == BASE_CLAUSE_COUNT
        ),
        "exact_appended_clause_sequence": (
            tuple(observed_additions) == expected_additions
        ),
        "union_declared_count": (
            union_summary["declared_clause_count"] == expected_clause_count
            and union_summary["actual_clause_count"] == expected_clause_count
            and union_summary["variable_count"] == expected_variable_count
        ),
        "metadata_degree": metadata.get("degree") == degree,
        "metadata_local_degree_counter_mode": (
            metadata.get("local_degree_counters_enabled")
            is include_local_degree_counters
        ),
        "metadata_base_sha256": (
            metadata.get("base_cnf_sha256") == BASE_CNF_SHA256
        ),
        "metadata_cnf_sha256": metadata.get("cnf_sha256") == union_sha,
        "metadata_cnf_bytes": metadata.get("cnf_bytes") == union_cnf.stat().st_size,
        "metadata_counts": (
            metadata.get("variable_count") == expected_variable_count
            and metadata.get("clause_count") == expected_clause_count
            and metadata.get("appended_clause_count") == len(expected_additions)
        ),
        "metadata_appended_hash": (
            metadata.get("appended_clause_stream_sha256")
            == clause_hash(expected_additions)
        ),
    }
    result: dict[str, object] = {
        "valid": all(checks.values()),
        "degree": degree,
        "local_degree_counters_enabled": include_local_degree_counters,
        "union_cnf_sha256": union_sha,
        "union_cnf_bytes": union_cnf.stat().st_size,
        "metadata_sha256": metadata_sha,
        "copied_base_clause_count": copied,
        "observed_appended_clause_count": len(observed_additions),
        "expected_appended_clause_count": len(expected_additions),
        "checks": checks,
        "base_summary": base_summary,
        "union_summary": union_summary,
    }
    if first_mismatch is not None:
        result["first_mismatch"] = first_mismatch
    return result


def check(plan_path: Path, base_cnf: Path, base_metadata: Path) -> dict[str, object]:
    raw = plan_path.read_bytes()
    plan = json.loads(raw)
    errors: list[str] = []
    actual_base_sha = sha256_file(base_cnf)
    actual_metadata_sha = sha256_file(base_metadata)
    if actual_base_sha != BASE_CNF_SHA256:
        errors.append("base CNF SHA-256 mismatch")
    if actual_metadata_sha != BASE_METADATA_SHA256:
        errors.append("base metadata SHA-256 mismatch")
    for key, expected in (
        ("schema", SCHEMA),
        ("base_cnf_sha256", BASE_CNF_SHA256),
        ("base_metadata_sha256", BASE_METADATA_SHA256),
        ("base_variable_count", BASE_VARIABLE_COUNT),
        ("base_clause_count", BASE_CLAUSE_COUNT),
        ("feasible_matrix_count", 35_714),
        ("canonical_matrix_count", 143),
    ):
        if plan.get(key) != expected:
            errors.append(f"plan field mismatch: {key}")

    representatives, owner = representatives_and_owner()
    if len(owner) != 35_714 or len(representatives) != 143:
        errors.append("independent orbit census mismatch")
    if set(owner) != {
        matrix for matrix in range(1 << 16) if feasible(matrix)
    }:
        errors.append("feasible matrices are not covered exactly")
    expected_rep_hash = hashlib.sha256(
        "".join(f"{matrix:04x}\n" for matrix in representatives).encode("ascii")
    ).hexdigest()
    if plan.get("canonical_matrices_sha256") != expected_rep_hash:
        errors.append("canonical representative stream hash mismatch")

    records = plan.get("branches")
    if not isinstance(records, list) or len(records) != len(DEGREES):
        errors.append("branch record count mismatch")
        records = []
    branch_results: list[dict[str, object]] = []
    for degree, branch in zip(DEGREES, records):
        if not isinstance(branch, dict) or branch.get("degree") != degree:
            errors.append(f"branch {degree} identity mismatch")
            continue
        common = branch_units(degree) + anchor_units(degree)
        if branch.get("common_assumption_count") != len(common):
            errors.append(f"branch {degree} common assumption count mismatch")
        if branch.get("common_assumptions_sha256") != units_hash(common):
            errors.append(f"branch {degree} common assumptions hash mismatch")
        cubes = branch.get("cubes")
        if not isinstance(cubes, list) or len(cubes) != len(representatives):
            errors.append(f"branch {degree} cube count mismatch")
            cubes = []
        cube_errors = 0
        for index, (matrix, cube) in enumerate(zip(representatives, cubes)):
            units = common + matrix_units(degree, matrix)
            expected = {
                "cube_index": index,
                "cube_id": f"d{degree}_m{index:03d}",
                "matrix_integer": matrix,
                "matrix_hex": f"{matrix:04x}",
                "matrix_edge_count": matrix.bit_count(),
                "matrix_orbit_size": len(orbit(matrix)),
                "matrix_stabilizer_order": 576 // len(orbit(matrix)),
                "assumption_count": len(units),
                "assumptions_sha256": units_hash(units),
            }
            if not isinstance(cube, dict) or any(
                cube.get(key) != value for key, value in expected.items()
            ):
                cube_errors += 1
        if cube_errors:
            errors.append(f"branch {degree} has {cube_errors} malformed cubes")

        additions = tuple(appended_clauses(degree, representatives))
        (
            local_clauses,
            last_local_variable,
            local_auxiliary_count,
            local_counter_count,
        ) = local_counter_data(degree)
        strengthened_additions = tuple(
            appended_clauses(
                degree,
                representatives,
                include_local_degree_counters=True,
            )
        )
        union = branch.get("union_encoding")
        if not isinstance(union, dict):
            errors.append(f"branch {degree} union encoding missing")
            union = {}
        expected_union = {
            "selector_variable_first": BASE_VARIABLE_COUNT + 1,
            "selector_variable_count": 143,
            "witness_selector_variable_first": BASE_VARIABLE_COUNT + 144,
            "witness_selector_variable_count": 10,
            "variable_count": BASE_VARIABLE_COUNT + 143 + 10,
            "common_unit_clause_count": 140,
            "selector_at_least_one_clause_count": 1,
            "selector_implication_clause_count": 143 * 16,
            "witness_selector_clause_count": 32,
            "signature_vector_width": 8,
            "signature_comparator_count": 26,
            "signature_sort_clause_count": 26 * 255,
            "appended_clause_count": len(additions),
            "clause_count": BASE_CLAUSE_COUNT + len(additions),
            "appended_clause_stream_sha256": clause_hash(additions),
        }
        for key, value in expected_union.items():
            if union.get(key) != value:
                errors.append(f"branch {degree} union field mismatch: {key}")
        strengthening = branch.get("optional_local_degree_strengthening")
        if not isinstance(strengthening, dict):
            errors.append(f"branch {degree} local strengthening missing")
            strengthening = {}
        expected_strengthening = {
            "theorem_dependencies": ["R(4,4)=18", "R(3,5)=14"],
            "variable_count": last_local_variable,
            "local_degree_counter_count": local_counter_count,
            "local_degree_counter_auxiliary_count": local_auxiliary_count,
            "local_degree_counter_clause_count": len(local_clauses),
            "local_degree_bounds": {
                "A": [degree - 18, 13],
                "B": [28 - degree, 17],
            },
            "appended_clause_count": len(strengthened_additions),
            "clause_count": BASE_CLAUSE_COUNT + len(strengthened_additions),
            "appended_clause_stream_sha256": clause_hash(
                strengthened_additions
            ),
        }
        for key, value in expected_strengthening.items():
            if strengthening.get(key) != value:
                errors.append(
                    f"branch {degree} local strengthening field mismatch: {key}"
                )
        branch_results.append(
            {
                "degree": degree,
                "common_assumption_count": len(common),
                "cube_count": len(cubes),
                "cube_error_count": cube_errors,
                "appended_clause_count": len(additions),
                "appended_clause_stream_sha256": clause_hash(additions),
                "signature_sort_clause_count": sum(
                    1 for _ in sort_clauses(degree)
                ),
                "local_degree_counter_count": local_counter_count,
                "local_degree_counter_auxiliary_count": local_auxiliary_count,
                "local_degree_counter_clause_count": len(local_clauses),
                "strengthened_appended_clause_count": len(
                    strengthened_additions
                ),
                "strengthened_appended_clause_stream_sha256": clause_hash(
                    strengthened_additions
                ),
            }
        )

    lex_valid = lex_semantics_exhaustive()
    if not lex_valid:
        errors.append("lexicographic clause template failed exhaustive semantics")
    infeasible_all_one_row = sum(
        not feasible(matrix)
        and any(all(bit(matrix, row, column) for column in range(4)) for row in range(4))
        for matrix in range(1 << 16)
    )
    infeasible_all_zero_column = sum(
        not feasible(matrix)
        and any(
            all(not bit(matrix, row, column) for row in range(4))
            for column in range(4)
        )
        for matrix in range(1 << 16)
    )
    return {
        "checker": CHECKER_ID,
        "checker_source_sha256": sha256_file(Path(__file__)),
        "valid": not errors,
        "errors": errors,
        "plan_sha256": hashlib.sha256(raw).hexdigest(),
        "base_cnf_sha256": actual_base_sha,
        "base_metadata_sha256": actual_metadata_sha,
        "independent_feasible_matrix_count": len(owner),
        "independent_canonical_matrix_count": len(representatives),
        "independent_orbit_partition_exact": len(owner) == 35_714,
        "infeasible_with_all_one_row_count": infeasible_all_one_row,
        "infeasible_with_all_zero_column_count": infeasible_all_zero_column,
        "lex_template_exhaustive_widths_1_through_8": lex_valid,
        "branch_results": branch_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--base-metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--union-degree", type=int, choices=DEGREES)
    parser.add_argument("--union-cnf", type=Path)
    parser.add_argument("--union-metadata", type=Path)
    args = parser.parse_args()
    result = check(args.plan, args.base_cnf, args.base_metadata)
    union_arguments = (
        args.union_degree,
        args.union_cnf,
        args.union_metadata,
    )
    if any(value is not None for value in union_arguments):
        if not all(value is not None for value in union_arguments):
            raise SystemExit(
                "--union-degree, --union-cnf, and --union-metadata "
                "must be supplied together"
            )
        representatives, _owner = representatives_and_owner()
        union_result = check_materialized_union(
            base_cnf=args.base_cnf,
            union_cnf=args.union_cnf,
            metadata_path=args.union_metadata,
            degree=args.union_degree,
            representatives=representatives,
        )
        result["materialized_union"] = union_result
        if not union_result["valid"]:
            result["valid"] = False
            result["errors"].append("materialized union check failed")
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
