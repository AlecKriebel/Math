#!/usr/bin/env python3
"""Exact Ramsey-anchor symmetry cover for global degree branches 19 and 20.

After the complement/minimum-degree normalization, let ``v=0`` be the root,
``A=N(v)`` and ``B=V\\(A union {v})``.  In both branches treated here:

* ``G[A]`` contains no K4, so ``|A| >= 19 = R(4,4)+1`` forces an I4;
* ``G[B]`` contains no I4 (otherwise it extends with ``v`` to an I5), so
  ``|B| >= 22 = R(4,4)+4`` forces a K4.

Relabel one such I4 and K4 to the first four vertices of A and B.  Their
4-by-4 cross matrix has neither an all-one row nor an all-zero column:
either pattern would immediately give a forbidden K5 or I5.  Independent
permutations of the two four-vertex anchors reduce the 35,714 feasible
matrices to 143 exact orbits.

This module provides both a 143-cube cover and a compact union encoding.  The
union encoding adds one selector per canonical matrix and primary-only
lexicographic ordering clauses for the remaining vertices' eight anchor
incidences.  These additions are symmetry breaking only: every graph in the
original degree branch has a relabelled representative satisfying them.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
import math
import os
import tempfile
import time
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from direct_ramsey_cnf import (
    SequentialCounter,
    allocate_sequential_counter,
    variable_for_edge,
)
from global_minmax_degree_cover import branch_units


ORDER = 43
DEGREES = (19, 20)
ANCHOR_SIZE = 4
MATRIX_BITS = ANCHOR_SIZE * ANCHOR_SIZE
BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
BASE_CNF_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)
BASE_METADATA_SHA256 = (
    "88906686b2554cf1b5b9051eae4a200b878944278ed91682b78d9f40d43cf70c"
)
R44 = 18
R35 = 14
SCHEMA = "ramsey55.global_anchor_cube_cover.v1"
GENERATOR_ID = "ramsey55_global_anchor_union_cnf_v1"
PERMUTATIONS4 = tuple(itertools.permutations(range(ANCHOR_SIZE)))


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


def units_sha256(units: Sequence[int]) -> str:
    return clause_stream_sha256((literal,) for literal in units)


def sides(degree: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if degree not in DEGREES:
        raise ValueError(f"degree must be one of {DEGREES}")
    return tuple(range(1, degree + 1)), tuple(range(degree + 1, ORDER))


def anchor_vertices(degree: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    side_a, side_b = sides(degree)
    return side_a[:ANCHOR_SIZE], side_b[:ANCHOR_SIZE]


def anchor_structure_units(degree: int) -> tuple[int, ...]:
    """Fix an independent four-set in A and a four-clique in B."""

    anchor_a, anchor_b = anchor_vertices(degree)
    independent = tuple(
        -variable_for_edge(ORDER, left, right)
        for left, right in itertools.combinations(anchor_a, 2)
    )
    clique = tuple(
        variable_for_edge(ORDER, left, right)
        for left, right in itertools.combinations(anchor_b, 2)
    )
    return independent + clique


def matrix_bit(matrix: int, row: int, column: int) -> int:
    return (matrix >> (ANCHOR_SIZE * row + column)) & 1


def feasible_matrix(matrix: int) -> bool:
    """Return whether the anchor cross matrix avoids immediate K5/I5."""

    if not 0 <= matrix < (1 << MATRIX_BITS):
        raise ValueError("matrix is outside the 16-bit range")
    no_all_one_row = all(
        any(not matrix_bit(matrix, row, column) for column in range(ANCHOR_SIZE))
        for row in range(ANCHOR_SIZE)
    )
    no_all_zero_column = all(
        any(matrix_bit(matrix, row, column) for row in range(ANCHOR_SIZE))
        for column in range(ANCHOR_SIZE)
    )
    return no_all_one_row and no_all_zero_column


def transform_matrix(
    matrix: int, row_permutation: Sequence[int], column_permutation: Sequence[int]
) -> int:
    """Relabel rows and columns; permutations map old indices to new ones."""

    if sorted(row_permutation) != list(range(ANCHOR_SIZE)):
        raise ValueError("row permutation is invalid")
    if sorted(column_permutation) != list(range(ANCHOR_SIZE)):
        raise ValueError("column permutation is invalid")
    result = 0
    for row in range(ANCHOR_SIZE):
        for column in range(ANCHOR_SIZE):
            if matrix_bit(matrix, row, column):
                new_index = (
                    ANCHOR_SIZE * row_permutation[row]
                    + column_permutation[column]
                )
                result |= 1 << new_index
    return result


@functools.lru_cache(maxsize=None)
def matrix_orbit(matrix: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                transform_matrix(matrix, row_permutation, column_permutation)
                for row_permutation in PERMUTATIONS4
                for column_permutation in PERMUTATIONS4
            }
        )
    )


@functools.lru_cache(maxsize=1)
def canonical_matrices() -> tuple[int, ...]:
    """One minimum-integer representative of every feasible S4 x S4 orbit."""

    seen: set[int] = set()
    representatives: list[int] = []
    for matrix in range(1 << MATRIX_BITS):
        if not feasible_matrix(matrix) or matrix in seen:
            continue
        orbit = matrix_orbit(matrix)
        if any(not feasible_matrix(member) for member in orbit):
            raise AssertionError("feasibility is not invariant under relabelling")
        seen.update(orbit)
        representatives.append(min(orbit))
    if len(seen) != 35_714 or len(representatives) != 143:
        raise AssertionError("unexpected 4-by-4 anchor orbit census")
    return tuple(sorted(representatives))


def matrix_units(degree: int, matrix: int) -> tuple[int, ...]:
    anchor_a, anchor_b = anchor_vertices(degree)
    return tuple(
        (
            variable_for_edge(ORDER, anchor_a[row], anchor_b[column])
            if matrix_bit(matrix, row, column)
            else -variable_for_edge(ORDER, anchor_a[row], anchor_b[column])
        )
        for row in range(ANCHOR_SIZE)
        for column in range(ANCHOR_SIZE)
    )


def cube_units(degree: int, matrix: int) -> tuple[int, ...]:
    if matrix not in canonical_matrices():
        raise ValueError("matrix is not a canonical feasible representative")
    return (
        branch_units(degree)
        + anchor_structure_units(degree)
        + matrix_units(degree, matrix)
    )


def anchor_signature(degree: int, vertex: int) -> tuple[int, ...]:
    """Eight primary variables describing one non-anchor vertex."""

    side_a, side_b = sides(degree)
    anchor_a, anchor_b = anchor_vertices(degree)
    if vertex not in (*side_a[ANCHOR_SIZE:], *side_b[ANCHOR_SIZE:]):
        raise ValueError("vertex is not a non-anchor side vertex")
    return tuple(
        variable_for_edge(ORDER, vertex, anchor)
        for anchor in (*anchor_a, *anchor_b)
    )


def lex_nondecreasing_clauses(
    left: Sequence[int], right: Sequence[int]
) -> Iterator[tuple[int, ...]]:
    """Encode the binary-vector relation ``left <=lex right`` without auxes."""

    if len(left) != len(right) or not left:
        raise ValueError("lex vectors must have one common positive length")
    if len(set(left)) != len(left) or len(set(right)) != len(right):
        raise ValueError("a lex vector repeats a variable")
    for index in range(len(left)):
        for prefix in itertools.product((0, 1), repeat=index):
            clause: list[int] = []
            for offset, value in enumerate(prefix):
                if value:
                    clause.extend((-left[offset], -right[offset]))
                else:
                    clause.extend((left[offset], right[offset]))
            clause.extend((-left[index], right[index]))
            yield tuple(clause)


def signature_sort_clauses(degree: int) -> Iterator[tuple[int, ...]]:
    """Sort labels not reserved for the triangle/I3 witnesses.

    Vertices 5, 6, and 7 on each side are reserved by the five-way witness
    unions below.  Every later vertex is still freely permutable within its
    side.
    """

    side_a, side_b = sides(degree)
    for side in (side_a[7:], side_b[7:]):
        for left_vertex, right_vertex in zip(side, side[1:]):
            yield from lex_nondecreasing_clauses(
                anchor_signature(degree, left_vertex),
                anchor_signature(degree, right_vertex),
            )


def selector_clauses(
    degree: int, first_selector: int = BASE_VARIABLE_COUNT + 1
) -> Iterator[tuple[int, ...]]:
    representatives = canonical_matrices()
    selectors = tuple(
        range(first_selector, first_selector + len(representatives))
    )
    yield selectors
    for selector, matrix in zip(selectors, representatives):
        for literal in matrix_units(degree, matrix):
            yield (-selector, literal)


def witness_selector_clauses(
    degree: int,
    first_selector: int = BASE_VARIABLE_COUNT + 1 + 143,
) -> Iterator[tuple[int, ...]]:
    """Fix a triangle in A and an I3 in B after fixing the cross matrix.

    A triangle meets the anchored I4 in either zero or one vertex.  The five
    selectors encode the disjoint case followed by the four possible
    intersection vertices.  The B-side independent triple is analogous.
    """

    side_a, side_b = sides(degree)
    anchor_a, anchor_b = anchor_vertices(degree)
    free_a = side_a[ANCHOR_SIZE : ANCHOR_SIZE + 3]
    free_b = side_b[ANCHOR_SIZE : ANCHOR_SIZE + 3]
    if len(free_a) != 3 or len(free_b) != 3:
        raise AssertionError("witness labels are unavailable")

    triangle_patterns: list[tuple[int, ...]] = [
        tuple(
            variable_for_edge(ORDER, left, right)
            for left, right in itertools.combinations(free_a, 2)
        )
    ]
    for anchor in anchor_a:
        triangle_patterns.append(
            (
                variable_for_edge(ORDER, anchor, free_a[0]),
                variable_for_edge(ORDER, anchor, free_a[1]),
                variable_for_edge(ORDER, free_a[0], free_a[1]),
            )
        )

    independent_patterns: list[tuple[int, ...]] = [
        tuple(
            -variable_for_edge(ORDER, left, right)
            for left, right in itertools.combinations(free_b, 2)
        )
    ]
    for anchor in anchor_b:
        independent_patterns.append(
            (
                -variable_for_edge(ORDER, anchor, free_b[0]),
                -variable_for_edge(ORDER, anchor, free_b[1]),
                -variable_for_edge(ORDER, free_b[0], free_b[1]),
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


def local_degree_counters(
    degree: int,
    first_auxiliary: int = BASE_VARIABLE_COUNT + 1 + 143 + 10,
) -> tuple[tuple[SequentialCounter, ...], int]:
    """Allocate theorem-strengthened internal-degree counters.

    For ``a in A``, ``d_A(a)`` lies in ``[degree-18, 13]``.  For ``b in B``,
    ``d_B(b)`` lies in ``[|B|-14, 17]``.  The upper endpoints follow from
    R(3,5)=14 and R(4,4)=18 in the appropriate local neighborhoods; the
    lower endpoints are their complementary nonneighborhood statements.
    """

    side_a, side_b = sides(degree)
    counters: list[SequentialCounter] = []
    next_variable = first_auxiliary
    for vertex in side_a:
        internal = tuple(
            variable_for_edge(ORDER, vertex, other)
            for other in side_a
            if other != vertex
        )
        upper, next_variable = allocate_sequential_counter(
            internal,
            13,
            next_variable,
            f"A_{vertex}_internal_edges_at_most_13",
        )
        counters.append(upper)
        lower, next_variable = allocate_sequential_counter(
            tuple(-literal for literal in internal),
            17,
            next_variable,
            f"A_{vertex}_internal_nonedges_at_most_17",
        )
        counters.append(lower)
    for vertex in side_b:
        internal = tuple(
            variable_for_edge(ORDER, vertex, other)
            for other in side_b
            if other != vertex
        )
        upper, next_variable = allocate_sequential_counter(
            internal,
            17,
            next_variable,
            f"B_{vertex}_internal_edges_at_most_17",
        )
        counters.append(upper)
        lower, next_variable = allocate_sequential_counter(
            tuple(-literal for literal in internal),
            13,
            next_variable,
            f"B_{vertex}_internal_nonedges_at_most_13",
        )
        counters.append(lower)
    if len(counters) != 2 * (ORDER - 1):
        raise AssertionError("unexpected local-counter count")
    return tuple(counters), next_variable


def local_degree_clauses(degree: int) -> Iterator[tuple[int, ...]]:
    counters, _next_variable = local_degree_counters(degree)
    for counter in counters:
        yield from counter.clauses()


def union_variable_count(
    degree: int, *, include_local_degree_counters: bool = False
) -> int:
    if not include_local_degree_counters:
        return BASE_VARIABLE_COUNT + 143 + 10
    _counters, next_variable = local_degree_counters(degree)
    return next_variable - 1


def appended_clauses(
    degree: int, *, include_local_degree_counters: bool = False
) -> Iterator[tuple[int, ...]]:
    for literal in branch_units(degree) + anchor_structure_units(degree):
        yield (literal,)
    yield from selector_clauses(degree)
    yield from witness_selector_clauses(degree)
    yield from signature_sort_clauses(degree)
    if include_local_degree_counters:
        yield from local_degree_clauses(degree)


def build_plan() -> dict[str, object]:
    representatives = canonical_matrices()
    orbit_sizes = [len(matrix_orbit(matrix)) for matrix in representatives]
    branches: list[dict[str, object]] = []
    for degree in DEGREES:
        common_units = branch_units(degree) + anchor_structure_units(degree)
        cubes: list[dict[str, object]] = []
        for index, matrix in enumerate(representatives):
            units = cube_units(degree, matrix)
            orbit_size = len(matrix_orbit(matrix))
            cubes.append(
                {
                    "cube_index": index,
                    "cube_id": f"d{degree}_m{index:03d}",
                    "matrix_integer": matrix,
                    "matrix_hex": f"{matrix:04x}",
                    "matrix_edge_count": matrix.bit_count(),
                    "matrix_orbit_size": orbit_size,
                    "matrix_stabilizer_order": math.factorial(4) ** 2 // orbit_size,
                    "assumption_count": len(units),
                    "assumptions_sha256": units_sha256(units),
                }
            )
        appended = tuple(appended_clauses(degree))
        strengthened = tuple(
            appended_clauses(degree, include_local_degree_counters=True)
        )
        local_counters, _next_variable = local_degree_counters(degree)
        local_counter_clause_count = sum(
            counter.clause_count for counter in local_counters
        )
        local_counter_auxiliary_count = sum(
            counter.auxiliary_count for counter in local_counters
        )
        branches.append(
            {
                "degree": degree,
                "degree_interval": [degree, ORDER - 1 - degree],
                "A_size": degree,
                "B_size": ORDER - 1 - degree,
                "common_assumption_count": len(common_units),
                "common_assumptions_sha256": units_sha256(common_units),
                "cube_count": len(cubes),
                "cube_assumption_count": len(cube_units(degree, representatives[0])),
                "cubes": cubes,
                "union_encoding": {
                    "selector_variable_first": BASE_VARIABLE_COUNT + 1,
                    "selector_variable_count": len(representatives),
                    "witness_selector_variable_first": (
                        BASE_VARIABLE_COUNT + len(representatives) + 1
                    ),
                    "witness_selector_variable_count": 10,
                    "variable_count": union_variable_count(degree),
                    "common_unit_clause_count": len(common_units),
                    "selector_at_least_one_clause_count": 1,
                    "selector_implication_clause_count": (
                        len(representatives) * MATRIX_BITS
                    ),
                    "witness_selector_clause_count": 32,
                    "witness_selector_semantics": (
                        "five A-triangle locations (disjoint from the I4 or "
                        "meeting one of its four vertices) and five analogous "
                        "B-independent-triple locations"
                    ),
                    "signature_vector_width": 8,
                    "signature_comparator_count": 26,
                    "signature_sort_clause_count": 26 * (2**8 - 1),
                    "appended_clause_count": len(appended),
                    "clause_count": BASE_CLAUSE_COUNT + len(appended),
                    "appended_clause_stream_sha256": clause_stream_sha256(appended),
                },
                "optional_local_degree_strengthening": {
                    "theorem_dependencies": ["R(4,4)=18", "R(3,5)=14"],
                    "variable_count": union_variable_count(
                        degree, include_local_degree_counters=True
                    ),
                    "local_degree_counter_count": len(local_counters),
                    "local_degree_counter_auxiliary_count": (
                        local_counter_auxiliary_count
                    ),
                    "local_degree_counter_clause_count": (
                        local_counter_clause_count
                    ),
                    "local_degree_bounds": {
                        "A": [degree - R44, R35 - 1],
                        "B": [ORDER - 1 - degree - R35, R44 - 1],
                    },
                    "appended_clause_count": len(strengthened),
                    "clause_count": BASE_CLAUSE_COUNT + len(strengthened),
                    "appended_clause_stream_sha256": clause_stream_sha256(
                        strengthened
                    ),
                    "claim_limit": (
                        "Redundant exact local bounds; benchmark separately "
                        "because stronger propagation need not mean faster solving."
                    ),
                },
            }
        )
    orbit_histogram = {
        str(size): orbit_sizes.count(size) for size in sorted(set(orbit_sizes))
    }
    return {
        "schema": SCHEMA,
        "status": "EXACT_BRANCH_COVER_AND_UNION_ENCODING_NO_SOLVE_CLAIM",
        "order": ORDER,
        "degrees": list(DEGREES),
        "base_cnf_sha256": BASE_CNF_SHA256,
        "base_metadata_sha256": BASE_METADATA_SHA256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
        "theorem_dependencies": ["R(4,4)=18", "R(3,5)=14"],
        "anchor_argument": {
            "A": (
                "A=N(0) has order at least 19 and no K4, hence contains I4"
            ),
            "B": (
                "B=V\\(A union {0}) has order at least 22 and no I4 "
                "(an I4 extends with 0 to I5), hence contains K4"
            ),
            "secondary_witnesses": (
                "A also contains a triangle because it has order at least 14 "
                "and no I5; B contains an independent triple by the "
                "complementary R(3,5)=14 statement and the absence of K5"
            ),
        },
        "matrix_bit_order": "bit (4*row+column), row-major, low bit first",
        "matrix_feasibility": (
            "no all-one row (would give K5 with the B-anchor K4) and no "
            "all-zero column (would give I5 with the A-anchor I4)"
        ),
        "raw_matrix_count": 1 << MATRIX_BITS,
        "feasible_matrix_count": 35_714,
        "canonical_matrix_count": len(representatives),
        "orbit_group": "S4 rows x S4 columns",
        "orbit_group_order": math.factorial(4) ** 2,
        "orbit_size_histogram": orbit_histogram,
        "canonical_matrices_sha256": hashlib.sha256(
            "".join(f"{matrix:04x}\n" for matrix in representatives).encode("ascii")
        ).hexdigest(),
        "branches": branches,
        "certificate_architecture": (
            "Either certify all 143 materialized cubes in each branch, or "
            "certify one selector-union CNF per branch.  The independent "
            "cover checker validates the finite orbit cover and all added "
            "clauses; each UNSAT proof must then be checked against its exact "
            "checked CNF."
        ),
        "claim_limit": (
            "This plan certifies a symmetry-complete decomposition of only "
            "the degree-19 and degree-20 global branches.  It contains no "
            "SAT model and no UNSAT certificate."
        ),
    }


def write_union_cnf(
    base_cnf: Path,
    output: Path,
    *,
    degree: int,
    include_local_degree_counters: bool = False,
    expected_base_sha256: str = BASE_CNF_SHA256,
) -> dict[str, object]:
    """Copy the audited base CNF and append the exact union encoding."""

    if degree not in DEGREES:
        raise ValueError(f"degree must be one of {DEGREES}")
    actual_base_sha256 = sha256_file(base_cnf)
    if actual_base_sha256 != expected_base_sha256:
        raise ValueError("base CNF SHA-256 mismatch")
    additions = tuple(
        appended_clauses(
            degree,
            include_local_degree_counters=include_local_degree_counters,
        )
    )
    variable_count = union_variable_count(
        degree,
        include_local_degree_counters=include_local_degree_counters,
    )
    clause_count = BASE_CLAUSE_COUNT + len(additions)
    output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    byte_count = 0
    base_header_seen = False
    started = time.monotonic()
    temporary_name: str | None = None
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
                    write(f"c normalized_root_degree {degree}\n".encode("ascii"))
                    write(
                        b"c anchors A[0:4]=I4 B[0:4]=K4; canonical "
                        b"4x4 cross matrix; sorted remaining signatures\n"
                    )
                    write(
                        (
                            "c local_degree_counters "
                            f"{str(include_local_degree_counters).lower()}\n"
                        ).encode("ascii")
                    )
                    write(f"p cnf {variable_count} {clause_count}\n".encode("ascii"))
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
        "local_degree_counters_enabled": include_local_degree_counters,
        "variable_count": variable_count,
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
            "This is a symmetry-complete branch encoding, not a SAT/UNSAT result."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--base-cnf", type=Path)
    parser.add_argument("--degree", type=int, choices=DEGREES)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--local-degree-counters", action="store_true")
    args = parser.parse_args()
    if args.base_cnf is None:
        if (
            args.degree is not None
            or args.output is not None
            or args.metadata is not None
            or args.local_degree_counters
        ):
            raise SystemExit(
                "--degree/--output/--metadata require --base-cnf; use --plan alone"
            )
        result = build_plan()
        rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
        if args.plan:
            args.plan.parent.mkdir(parents=True, exist_ok=True)
            args.plan.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0
    if args.degree is None or args.output is None:
        raise SystemExit("--base-cnf requires --degree and --output")
    result = write_union_cnf(
        args.base_cnf,
        args.output,
        degree=args.degree,
        include_local_degree_counters=args.local_degree_counters,
    )
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.metadata:
        args.metadata.parent.mkdir(parents=True, exist_ok=True)
        args.metadata.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
