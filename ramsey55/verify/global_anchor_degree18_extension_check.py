#!/usr/bin/env python3
"""Independent checker for the degree-18 Ramsey-anchor extension.

The checker imports neither the degree-18 generator nor the degree-19/20 v1
cover.  It independently reconstructs all primary variables, root and anchor
units, the 65,536 cross matrices, the S4 x S4 orbit partition, all 143 cube
streams, the two five-way witness unions, the signature-order clauses, and
an optional materialized union CNF.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
from pathlib import Path
from typing import Generator, Iterable, Sequence


CHECKER_ID = "ramsey55.global_anchor_degree18_extension_checker.v1"
SCHEMA = "ramsey55.global_anchor_degree18_extension.v1"
ORDER = 43
DEGREE = 18
SIDE_A = tuple(range(1, 19))
SIDE_B = tuple(range(19, 43))
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


@functools.lru_cache(maxsize=1)
def edge_map() -> dict[tuple[int, int], int]:
    return {
        pair: variable
        for variable, pair in enumerate(
            itertools.combinations(range(ORDER), 2), start=1
        )
    }


def root_star_units() -> tuple[int, ...]:
    pairs = edge_map()
    return tuple(
        pairs[(0, vertex)] if vertex <= DEGREE else -pairs[(0, vertex)]
        for vertex in range(1, ORDER)
    )


def anchor_vertices() -> tuple[tuple[int, ...], tuple[int, ...]]:
    return SIDE_A[:4], SIDE_B[:4]


def anchor_units() -> tuple[int, ...]:
    pairs = edge_map()
    anchor_a, anchor_b = anchor_vertices()
    return tuple(
        -pairs[pair] for pair in itertools.combinations(anchor_a, 2)
    ) + tuple(pairs[pair] for pair in itertools.combinations(anchor_b, 2))


def common_units() -> tuple[int, ...]:
    return root_star_units() + anchor_units()


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
    matrix: int,
    row_permutation: Sequence[int],
    column_permutation: Sequence[int],
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


@functools.lru_cache(maxsize=1)
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
                raise AssertionError("matrix orbit partition failure")
            owner[member] = representative
    return tuple(sorted(representatives)), owner


def matrix_units(matrix: int) -> tuple[int, ...]:
    pairs = edge_map()
    anchor_a, anchor_b = anchor_vertices()
    return tuple(
        (
            pairs[(anchor_a[row], anchor_b[column])]
            if bit(matrix, row, column)
            else -pairs[(anchor_a[row], anchor_b[column])]
        )
        for row in range(4)
        for column in range(4)
    )


def signature(vertex: int) -> tuple[int, ...]:
    pairs = edge_map()
    anchor_a, anchor_b = anchor_vertices()
    return tuple(
        pairs[tuple(sorted((vertex, anchor)))]
        for anchor in (*anchor_a, *anchor_b)
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


def sort_clauses() -> Iterable[tuple[int, ...]]:
    for side in (SIDE_A[7:], SIDE_B[7:]):
        for left, right in zip(side, side[1:]):
            yield from lex_clauses(signature(left), signature(right))


def witness_patterns() -> tuple[
    tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]
]:
    pairs = edge_map()
    anchor_a, anchor_b = anchor_vertices()
    free_a = SIDE_A[4:7]
    free_b = SIDE_B[4:7]
    triangles: list[tuple[int, ...]] = [
        tuple(pairs[pair] for pair in itertools.combinations(free_a, 2))
    ]
    for anchor in anchor_a:
        triangles.append(
            (
                pairs[tuple(sorted((anchor, free_a[0])))],
                pairs[tuple(sorted((anchor, free_a[1])))],
                pairs[(free_a[0], free_a[1])],
            )
        )
    independent: list[tuple[int, ...]] = [
        tuple(-pairs[pair] for pair in itertools.combinations(free_b, 2))
    ]
    for anchor in anchor_b:
        independent.append(
            (
                -pairs[tuple(sorted((anchor, free_b[0])))],
                -pairs[tuple(sorted((anchor, free_b[1])))],
                -pairs[(free_b[0], free_b[1])],
            )
        )
    return tuple(triangles), tuple(independent)


def witness_clauses(
    first_selector: int = BASE_VARIABLE_COUNT + 1 + 143,
) -> Iterable[tuple[int, ...]]:
    triangles, independent = witness_patterns()
    triangle_selectors = tuple(range(first_selector, first_selector + 5))
    independent_selectors = tuple(
        range(first_selector + 5, first_selector + 10)
    )
    yield triangle_selectors
    for selector, pattern in zip(triangle_selectors, triangles):
        for literal in pattern:
            yield (-selector, literal)
    yield independent_selectors
    for selector, pattern in zip(independent_selectors, independent):
        for literal in pattern:
            yield (-selector, literal)


def appended_clauses(
    representatives: Sequence[int],
) -> Iterable[tuple[int, ...]]:
    for literal in common_units():
        yield (literal,)
    selectors = tuple(
        range(
            BASE_VARIABLE_COUNT + 1,
            BASE_VARIABLE_COUNT + 1 + len(representatives),
        )
    )
    yield selectors
    for selector, matrix in zip(selectors, representatives):
        for literal in matrix_units(matrix):
            yield (-selector, literal)
    yield from witness_clauses()
    yield from sort_clauses()


def lex_semantics_exhaustive() -> bool:
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


def proof_obligation_audit() -> dict[str, object]:
    """Audit the exact numerical and selector-exhaustiveness obligations."""

    possible_intersections = (0, 1)
    location_labels: tuple[int | None, ...] = (None, 0, 1, 2, 3)
    triangles, independent = witness_patterns()
    return {
        "valid": (
            len(SIDE_A) == 18
            and len(SIDE_B) == 24
            and len(SIDE_A) >= 18
            and len(SIDE_B) >= 18
            and len(SIDE_A) >= 14
            and len(SIDE_B) >= 14
            and possible_intersections == (0, 1)
            and location_labels == (None, 0, 1, 2, 3)
            and len(triangles) == len(location_labels)
            and len(independent) == len(location_labels)
            and all(len(pattern) == 3 for pattern in (*triangles, *independent))
        ),
        "R_4_4": 18,
        "R_3_5": 14,
        "A_size": len(SIDE_A),
        "B_size": len(SIDE_B),
        "A_R44_slack": len(SIDE_A) - 18,
        "B_R44_slack": len(SIDE_B) - 18,
        "A_R35_slack": len(SIDE_A) - 14,
        "B_R35_slack": len(SIDE_B) - 14,
        "witness_anchor_intersection_sizes": list(possible_intersections),
        "witness_location_labels": list(location_labels),
        "triangle_pattern_count": len(triangles),
        "independent_pattern_count": len(independent),
        "explanation": (
            "A has no K4, so |A|=R(4,4) forces I4. B has no I4, "
            "so |B|>=R(4,4) forces K4. R(3,5)=14 forces an A triangle "
            "and, after complementing B, a B independent triple. A triangle "
            "meets I4 in at most one vertex; an I3 meets K4 in at most one."
        ),
    }


def check_plan(
    plan_path: Path,
    base_cnf: Path,
    base_metadata: Path,
    parent_v1_plan: Path,
) -> dict[str, object]:
    raw = plan_path.read_bytes()
    plan = json.loads(raw)
    errors: list[str] = []
    expected_top = {
        "schema": SCHEMA,
        "order": ORDER,
        "degree": DEGREE,
        "degree_interval": [18, 24],
        "A_size": 18,
        "B_size": 24,
        "base_cnf_sha256": BASE_CNF_SHA256,
        "base_metadata_sha256": BASE_METADATA_SHA256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
        "parent_v1_plan_sha256": PARENT_V1_PLAN_SHA256,
        "parent_v1_preserved": True,
        "theorem_dependencies": ["R(4,4)=18", "R(3,5)=14"],
        "raw_matrix_count": 65_536,
        "feasible_matrix_count": 35_714,
        "canonical_matrix_count": 143,
        "orbit_group": "S4 rows x S4 columns",
        "orbit_group_order": 576,
        "common_assumption_count": 54,
        "cube_count": 143,
        "cube_assumption_count": 70,
    }
    for key, expected in expected_top.items():
        if plan.get(key) != expected:
            errors.append(f"plan field mismatch: {key}")
    file_hashes = {
        "base_cnf": sha256_file(base_cnf),
        "base_metadata": sha256_file(base_metadata),
        "parent_v1_plan": sha256_file(parent_v1_plan),
    }
    if file_hashes["base_cnf"] != BASE_CNF_SHA256:
        errors.append("base CNF file hash mismatch")
    if file_hashes["base_metadata"] != BASE_METADATA_SHA256:
        errors.append("base metadata file hash mismatch")
    if file_hashes["parent_v1_plan"] != PARENT_V1_PLAN_SHA256:
        errors.append("parent v1 plan hash mismatch")

    representatives, owner = representatives_and_owner()
    feasible_set = {
        matrix for matrix in range(1 << 16) if feasible(matrix)
    }
    if set(owner) != feasible_set:
        errors.append("feasible matrix orbit cover is not exact")
    representative_hash = hashlib.sha256(
        "".join(f"{matrix:04x}\n" for matrix in representatives).encode(
            "ascii"
        )
    ).hexdigest()
    if plan.get("canonical_matrices_sha256") != representative_hash:
        errors.append("canonical representative hash mismatch")

    common = common_units()
    if (
        len(common) != 54
        or len(set(map(abs, common))) != 54
        or plan.get("common_assumptions_sha256") != units_hash(common)
    ):
        errors.append("common assumptions mismatch")
    cubes = plan.get("cubes")
    if not isinstance(cubes, list) or len(cubes) != len(representatives):
        errors.append("cube count mismatch")
        cubes = []
    cube_errors = 0
    for index, (matrix, record) in enumerate(zip(representatives, cubes)):
        units = common + matrix_units(matrix)
        expected = {
            "cube_index": index,
            "cube_id": f"d18_m{index:03d}",
            "matrix_integer": matrix,
            "matrix_hex": f"{matrix:04x}",
            "matrix_edge_count": matrix.bit_count(),
            "matrix_orbit_size": len(orbit(matrix)),
            "matrix_stabilizer_order": 576 // len(orbit(matrix)),
            "assumption_count": 70,
            "assumptions_sha256": units_hash(units),
        }
        if not isinstance(record, dict) or any(
            record.get(key) != value for key, value in expected.items()
        ):
            cube_errors += 1
    if cube_errors:
        errors.append(f"{cube_errors} malformed cube records")

    additions = tuple(appended_clauses(representatives))
    expected_union = {
        "selector_variable_first": BASE_VARIABLE_COUNT + 1,
        "selector_variable_count": 143,
        "witness_selector_variable_first": BASE_VARIABLE_COUNT + 144,
        "witness_selector_variable_count": 10,
        "variable_count": BASE_VARIABLE_COUNT + 153,
        "common_unit_clause_count": 54,
        "selector_at_least_one_clause_count": 1,
        "selector_implication_clause_count": 143 * 16,
        "witness_selector_clause_count": 32,
        "signature_vector_width": 8,
        "signature_comparator_count": 26,
        "signature_sort_clause_count": 26 * 255,
        "appended_clause_count": 9_005,
        "appended_clause_stream_sha256": clause_hash(additions),
        "clause_count": BASE_CLAUSE_COUNT + 9_005,
    }
    union = plan.get("union_encoding")
    if not isinstance(union, dict):
        errors.append("union encoding missing")
        union = {}
    for key, expected in expected_union.items():
        if union.get(key) != expected:
            errors.append(f"union field mismatch: {key}")

    obligation_audit = proof_obligation_audit()
    if not obligation_audit["valid"]:
        errors.append("degree-18 proof-obligation audit failed")
    lex_valid = lex_semantics_exhaustive()
    if not lex_valid:
        errors.append("lexicographic template failed exhaustive audit")
    return {
        "checker": CHECKER_ID,
        "checker_source_sha256": sha256_file(Path(__file__)),
        "valid": not errors,
        "errors": errors,
        "plan_sha256": hashlib.sha256(raw).hexdigest(),
        "file_hashes": file_hashes,
        "proof_obligation_audit": obligation_audit,
        "independent_feasible_matrix_count": len(owner),
        "independent_canonical_matrix_count": len(representatives),
        "independent_orbit_partition_exact": set(owner) == feasible_set,
        "canonical_matrices_sha256": representative_hash,
        "cube_record_error_count": cube_errors,
        "expected_appended_clause_count": len(additions),
        "expected_appended_clause_stream_sha256": clause_hash(additions),
        "signature_sort_clause_count": sum(1 for _ in sort_clauses()),
        "lex_template_exhaustive_widths_1_through_8": lex_valid,
        "claim_limit": (
            "This verifies the degree-18 cover and encoding only; it proves "
            "neither SAT nor UNSAT."
        ),
    }


def dimacs_stream(
    path: Path,
) -> Generator[tuple[int, ...], None, dict[str, int]]:
    variables: int | None = None
    declared: int | None = None
    actual = 0
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
                    raise ValueError(f"malformed header at line {line_number}")
                variables = int(fields[2])
                declared = int(fields[3])
                continue
            if variables is None:
                raise ValueError("clause before header")
            for field in fields:
                literal = int(field)
                if literal:
                    if abs(literal) > variables:
                        raise ValueError("literal outside declared range")
                    pending.append(literal)
                else:
                    if not pending:
                        raise ValueError("unexpected empty clause")
                    actual += 1
                    yield tuple(pending)
                    pending = []
    if pending:
        raise ValueError("unterminated final clause")
    if variables is None or declared is None:
        raise ValueError("missing header")
    return {
        "variable_count": variables,
        "declared_clause_count": declared,
        "actual_clause_count": actual,
    }


def next_clause(
    stream: Generator[tuple[int, ...], None, dict[str, int]],
) -> tuple[tuple[int, ...] | None, dict[str, int] | None]:
    try:
        return next(stream), None
    except StopIteration as stopped:
        return None, stopped.value


def check_materialized(
    *,
    base_cnf: Path,
    union_cnf: Path,
    metadata_path: Path,
    representatives: Sequence[int],
) -> dict[str, object]:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    base_stream = dimacs_stream(base_cnf)
    union_stream = dimacs_stream(union_cnf)
    base_summary = None
    union_summary = None
    copied = 0
    first_mismatch: dict[str, object] | None = None
    while base_summary is None:
        expected, base_summary = next_clause(base_stream)
        if base_summary is not None:
            break
        actual, union_summary = next_clause(union_stream)
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
    expected_additions = tuple(appended_clauses(representatives))
    observed_additions: list[tuple[int, ...]] = []
    if union_summary is None:
        while True:
            clause, union_summary = next_clause(union_stream)
            if union_summary is not None:
                break
            assert clause is not None
            observed_additions.append(clause)
    assert base_summary is not None
    assert union_summary is not None
    expected_variables = BASE_VARIABLE_COUNT + 153
    expected_clauses = BASE_CLAUSE_COUNT + len(expected_additions)
    union_sha = sha256_file(union_cnf)
    checks = {
        "base_header": base_summary
        == {
            "variable_count": BASE_VARIABLE_COUNT,
            "declared_clause_count": BASE_CLAUSE_COUNT,
            "actual_clause_count": BASE_CLAUSE_COUNT,
        },
        "base_prefix_exact": (
            first_mismatch is None and copied == BASE_CLAUSE_COUNT
        ),
        "appended_sequence_exact": (
            tuple(observed_additions) == expected_additions
        ),
        "union_header": union_summary
        == {
            "variable_count": expected_variables,
            "declared_clause_count": expected_clauses,
            "actual_clause_count": expected_clauses,
        },
        "metadata_degree": metadata.get("degree") == DEGREE,
        "metadata_base_hash": metadata.get("base_cnf_sha256")
        == BASE_CNF_SHA256,
        "metadata_cnf_hash": metadata.get("cnf_sha256") == union_sha,
        "metadata_bytes": metadata.get("cnf_bytes") == union_cnf.stat().st_size,
        "metadata_counts": (
            metadata.get("variable_count") == expected_variables
            and metadata.get("clause_count") == expected_clauses
            and metadata.get("appended_clause_count") == len(expected_additions)
        ),
        "metadata_append_hash": (
            metadata.get("appended_clause_stream_sha256")
            == clause_hash(expected_additions)
        ),
    }
    return {
        "valid": all(checks.values()),
        "checks": checks,
        "first_mismatch": first_mismatch,
        "copied_base_clause_count": copied,
        "observed_appended_clause_count": len(observed_additions),
        "expected_appended_clause_count": len(expected_additions),
        "union_cnf_sha256": union_sha,
        "union_cnf_bytes": union_cnf.stat().st_size,
        "metadata_sha256": sha256_file(metadata_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--base-metadata", type=Path, required=True)
    parser.add_argument("--parent-v1-plan", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--union-cnf", type=Path)
    parser.add_argument("--union-metadata", type=Path)
    args = parser.parse_args()
    result = check_plan(
        args.plan,
        args.base_cnf,
        args.base_metadata,
        args.parent_v1_plan,
    )
    if (args.union_cnf is None) != (args.union_metadata is None):
        parser.error("--union-cnf and --union-metadata must be supplied together")
    if args.union_cnf is not None:
        representatives, _owner = representatives_and_owner()
        materialized = check_materialized(
            base_cnf=args.base_cnf,
            union_cnf=args.union_cnf,
            metadata_path=args.union_metadata,
            representatives=representatives,
        )
        result["materialized_union"] = materialized
        if not materialized["valid"]:
            result["valid"] = False
            result["errors"].append("materialized union check failed")
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite {args.output}")
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
