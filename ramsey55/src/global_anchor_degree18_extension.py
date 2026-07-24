#!/usr/bin/env python3
"""Exact 143-orbit Ramsey-anchor cover for the global degree-18 branch.

This is a standalone extension of the degree-19/20 anchor architecture.  It
does not modify or import the v1 cover, so the v1 source and artifact hashes
remain untouched.

After global complement/minimum-degree normalization, vertex 0 has degree
18, ``A=N(0)`` has order 18, and ``B`` has order 24.  The exact boundary
``|A|=R(4,4)=18`` is sufficient: A has no K4 and hence has an I4.  B has no
I4 (or it extends with vertex 0 to an I5), so R(4,4)=18 forces a K4 in B.
The resulting 4-by-4 cross matrix has neither an all-one row nor an all-zero
column, and its exact S4 x S4 quotient has 143 orbits.
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

from direct_ramsey_cnf import variable_for_edge
from global_minmax_degree_cover import branch_units


ORDER = 43
DEGREE = 18
SIDE_A = tuple(range(1, DEGREE + 1))
SIDE_B = tuple(range(DEGREE + 1, ORDER))
ANCHOR_SIZE = 4
MATRIX_BITS = 16
BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
BASE_CNF_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)
BASE_METADATA_SHA256 = (
    "88906686b2554cf1b5b9051eae4a200b878944278ed91682b78d9f40d43cf70c"
)
PARENT_V1_PLAN_SHA256 = (
    "c4f7bc7e1e6191c81006530ca5204ef81e79ddb4403dbc790bedd77865cec28a"
)
R44 = 18
R35 = 14
SCHEMA = "ramsey55.global_anchor_degree18_extension.v1"
GENERATOR_ID = "ramsey55_global_anchor_degree18_union_cnf_v1"
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


def anchor_vertices() -> tuple[tuple[int, ...], tuple[int, ...]]:
    return SIDE_A[:ANCHOR_SIZE], SIDE_B[:ANCHOR_SIZE]


def anchor_structure_units() -> tuple[int, ...]:
    """Fix an independent four-set in A and a four-clique in B."""

    anchor_a, anchor_b = anchor_vertices()
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
    matrix: int,
    row_permutation: Sequence[int],
    column_permutation: Sequence[int],
) -> int:
    if sorted(row_permutation) != list(range(ANCHOR_SIZE)):
        raise ValueError("row permutation is invalid")
    if sorted(column_permutation) != list(range(ANCHOR_SIZE)):
        raise ValueError("column permutation is invalid")
    result = 0
    for row in range(ANCHOR_SIZE):
        for column in range(ANCHOR_SIZE):
            if matrix_bit(matrix, row, column):
                result |= 1 << (
                    ANCHOR_SIZE * row_permutation[row]
                    + column_permutation[column]
                )
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
    seen: set[int] = set()
    representatives: list[int] = []
    for matrix in range(1 << MATRIX_BITS):
        if not feasible_matrix(matrix) or matrix in seen:
            continue
        orbit = matrix_orbit(matrix)
        if any(not feasible_matrix(member) for member in orbit):
            raise AssertionError("feasibility is not orbit-invariant")
        seen.update(orbit)
        representatives.append(min(orbit))
    if len(seen) != 35_714 or len(representatives) != 143:
        raise AssertionError("unexpected anchor-matrix orbit census")
    return tuple(sorted(representatives))


def matrix_units(matrix: int) -> tuple[int, ...]:
    if matrix not in canonical_matrices():
        raise ValueError("matrix is not a canonical feasible representative")
    anchor_a, anchor_b = anchor_vertices()
    return tuple(
        (
            variable_for_edge(ORDER, anchor_a[row], anchor_b[column])
            if matrix_bit(matrix, row, column)
            else -variable_for_edge(ORDER, anchor_a[row], anchor_b[column])
        )
        for row in range(ANCHOR_SIZE)
        for column in range(ANCHOR_SIZE)
    )


def common_units() -> tuple[int, ...]:
    units = branch_units(DEGREE) + anchor_structure_units()
    if len(units) != 54 or len(set(map(abs, units))) != 54:
        raise AssertionError("degree-18 common units have the wrong layout")
    return units


def cube_units(matrix: int) -> tuple[int, ...]:
    units = common_units() + matrix_units(matrix)
    if len(units) != 70 or len(set(map(abs, units))) != 70:
        raise AssertionError("degree-18 cube units have the wrong layout")
    return units


def anchor_signature(vertex: int) -> tuple[int, ...]:
    anchor_a, anchor_b = anchor_vertices()
    if vertex not in (*SIDE_A[ANCHOR_SIZE:], *SIDE_B[ANCHOR_SIZE:]):
        raise ValueError("vertex is not a non-anchor side vertex")
    return tuple(
        variable_for_edge(ORDER, vertex, anchor)
        for anchor in (*anchor_a, *anchor_b)
    )


def lex_nondecreasing_clauses(
    left: Sequence[int], right: Sequence[int]
) -> Iterator[tuple[int, ...]]:
    """Encode ``left <=lex right`` directly, without auxiliaries."""

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


def signature_sort_clauses() -> Iterator[tuple[int, ...]]:
    """Sort every non-reserved label within A and B by anchor signature."""

    for side in (SIDE_A[7:], SIDE_B[7:]):
        for left_vertex, right_vertex in zip(side, side[1:]):
            yield from lex_nondecreasing_clauses(
                anchor_signature(left_vertex),
                anchor_signature(right_vertex),
            )


def selector_clauses(
    first_selector: int = BASE_VARIABLE_COUNT + 1,
) -> Iterator[tuple[int, ...]]:
    representatives = canonical_matrices()
    selectors = tuple(
        range(first_selector, first_selector + len(representatives))
    )
    yield selectors
    for selector, matrix in zip(selectors, representatives):
        for literal in matrix_units(matrix):
            yield (-selector, literal)


def witness_patterns() -> tuple[
    tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]
]:
    """Return five exhaustive A-triangle and B-I3 location patterns."""

    anchor_a, anchor_b = anchor_vertices()
    free_a = SIDE_A[ANCHOR_SIZE : ANCHOR_SIZE + 3]
    free_b = SIDE_B[ANCHOR_SIZE : ANCHOR_SIZE + 3]
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
    return tuple(triangle_patterns), tuple(independent_patterns)


def witness_selector_clauses(
    first_selector: int = BASE_VARIABLE_COUNT + 1 + 143,
) -> Iterator[tuple[int, ...]]:
    triangle_patterns, independent_patterns = witness_patterns()
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


def appended_clauses() -> Iterator[tuple[int, ...]]:
    for literal in common_units():
        yield (literal,)
    yield from selector_clauses()
    yield from witness_selector_clauses()
    yield from signature_sort_clauses()


def build_plan() -> dict[str, object]:
    representatives = canonical_matrices()
    orbit_sizes = [len(matrix_orbit(matrix)) for matrix in representatives]
    cubes = []
    for index, matrix in enumerate(representatives):
        units = cube_units(matrix)
        orbit_size = len(matrix_orbit(matrix))
        cubes.append(
            {
                "cube_index": index,
                "cube_id": f"d18_m{index:03d}",
                "matrix_integer": matrix,
                "matrix_hex": f"{matrix:04x}",
                "matrix_edge_count": matrix.bit_count(),
                "matrix_orbit_size": orbit_size,
                "matrix_stabilizer_order": math.factorial(4) ** 2 // orbit_size,
                "assumption_count": len(units),
                "assumptions_sha256": units_sha256(units),
            }
        )
    additions = tuple(appended_clauses())
    if len(additions) != 9_005:
        raise AssertionError("unexpected degree-18 union addition count")
    return {
        "schema": SCHEMA,
        "status": "EXACT_DEGREE18_BRANCH_COVER_AND_UNION_ENCODING_NO_SOLVE_CLAIM",
        "order": ORDER,
        "degree": DEGREE,
        "degree_interval": [18, 24],
        "A_size": len(SIDE_A),
        "B_size": len(SIDE_B),
        "base_cnf_sha256": BASE_CNF_SHA256,
        "base_metadata_sha256": BASE_METADATA_SHA256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
        "parent_v1_plan_sha256": PARENT_V1_PLAN_SHA256,
        "parent_v1_preserved": True,
        "theorem_dependencies": ["R(4,4)=18", "R(3,5)=14"],
        "anchor_argument": {
            "A": (
                "|A|=18=R(4,4); A has no K4 because the root is adjacent "
                "to A, so A contains I4"
            ),
            "B": (
                "|B|=24>=R(4,4); B has no I4 because it would extend with "
                "the root to I5, so B contains K4"
            ),
            "boundary_case_checked": True,
        },
        "secondary_witness_argument": {
            "A": (
                "|A|=18>=R(3,5); A has no I5, so A contains a triangle"
            ),
            "B": (
                "|B|=24>=R(3,5); B has no K5, so B contains I3 by "
                "complementation"
            ),
            "anchor_intersection_sizes": [0, 1],
            "selector_locations_per_side": 5,
        },
        "matrix_bit_order": "bit (4*row+column), row-major, low bit first",
        "matrix_feasibility": (
            "no all-one row (K5 with B-anchor K4) and no all-zero column "
            "(I5 with A-anchor I4)"
        ),
        "raw_matrix_count": 1 << MATRIX_BITS,
        "feasible_matrix_count": 35_714,
        "canonical_matrix_count": len(representatives),
        "canonical_matrices_sha256": hashlib.sha256(
            "".join(f"{matrix:04x}\n" for matrix in representatives).encode(
                "ascii"
            )
        ).hexdigest(),
        "orbit_group": "S4 rows x S4 columns",
        "orbit_group_order": math.factorial(4) ** 2,
        "orbit_size_histogram": {
            str(size): orbit_sizes.count(size)
            for size in sorted(set(orbit_sizes))
        },
        "common_assumption_count": len(common_units()),
        "common_assumptions_sha256": units_sha256(common_units()),
        "cube_count": len(cubes),
        "cube_assumption_count": len(cube_units(representatives[0])),
        "cubes": cubes,
        "union_encoding": {
            "selector_variable_first": BASE_VARIABLE_COUNT + 1,
            "selector_variable_count": len(representatives),
            "witness_selector_variable_first": (
                BASE_VARIABLE_COUNT + len(representatives) + 1
            ),
            "witness_selector_variable_count": 10,
            "variable_count": BASE_VARIABLE_COUNT + 143 + 10,
            "common_unit_clause_count": len(common_units()),
            "selector_at_least_one_clause_count": 1,
            "selector_implication_clause_count": 143 * 16,
            "witness_selector_clause_count": 32,
            "signature_vector_width": 8,
            "signature_comparator_count": 26,
            "signature_sort_clause_count": 26 * (2**8 - 1),
            "appended_clause_count": len(additions),
            "appended_clause_stream_sha256": clause_stream_sha256(additions),
            "clause_count": BASE_CLAUSE_COUNT + len(additions),
        },
        "derived_local_degree_bounds_not_encoded": {
            "A": [DEGREE - R44, R35 - 1],
            "B": [ORDER - 1 - DEGREE - R35, R44 - 1],
        },
        "claim_limit": (
            "This is an exact symmetry cover and checked union-encoding "
            "design only. It contains no SAT model and no UNSAT certificate."
        ),
    }


def write_union_cnf(base_cnf: Path, output: Path) -> dict[str, object]:
    actual_base_sha256 = sha256_file(base_cnf)
    if actual_base_sha256 != BASE_CNF_SHA256:
        raise ValueError("base CNF SHA-256 mismatch")
    additions = tuple(appended_clauses())
    variable_count = BASE_VARIABLE_COUNT + 143 + 10
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
                    write(b"c normalized_root_degree 18\n")
                    write(
                        b"c degree18 boundary anchors A[0:4]=I4 B[0:4]=K4; "
                        b"canonical 4x4 cross matrix\n"
                    )
                    write(
                        f"p cnf {variable_count} {clause_count}\n".encode(
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
        "degree": DEGREE,
        "base_cnf_sha256": actual_base_sha256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
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
            "This is a symmetry-complete branch encoding, not a SAT/UNSAT "
            "result."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--base-cnf", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()
    if args.base_cnf is None:
        if args.output is not None or args.metadata is not None:
            raise SystemExit(
                "--output/--metadata require --base-cnf; use --plan alone"
            )
        result = build_plan()
        destination = args.plan
    else:
        if args.output is None:
            raise SystemExit("--base-cnf requires --output")
        result = write_union_cnf(args.base_cnf, args.output)
        destination = args.metadata
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if destination:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            raise FileExistsError(f"refusing to overwrite {destination}")
        destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
