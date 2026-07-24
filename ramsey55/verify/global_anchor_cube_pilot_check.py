#!/usr/bin/env python3
"""Independent audit of the degree-18/19/20 selector-cube pilot.

This checker imports neither the pilot worker nor either anchor-cover
generator.  It reconstructs the 143 feasible S4 x S4 matrix orbits, the
degree-branch and anchor assumptions, their historical cube hashes, the
selector schedule, and every aggregate in the pilot result.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
ORDER = 43
BASE_VARIABLE_COUNT = 65_403
SELECTOR_VARIABLE_FIRST = 65_404
SELECTOR_COUNT = 143
CHECKER_ID = "ramsey55.global_anchor_selector_cube_pilot_checker.v1"
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
ALLOWED_STATUSES = {
    "SAT",
    "OBSERVED_UNSAT_UNCHECKED",
    "BUDGET_EXHAUSTED",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def sha256_json_object(value: object) -> str:
    return hashlib.sha256(
        (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode(
            "utf-8"
        )
    ).hexdigest()


def clause_stream_hash(clauses: Iterable[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return digest.hexdigest()


def selector_assumption_hash(selector: int) -> str:
    return clause_stream_hash(((selector,),))


@functools.lru_cache(maxsize=1)
def edge_map() -> dict[tuple[int, int], int]:
    return {
        pair: variable
        for variable, pair in enumerate(
            itertools.combinations(range(ORDER), 2), start=1
        )
    }


def allocate_final(
    first_variable: int, input_count: int, bound: int
) -> tuple[tuple[int, ...], int]:
    width = bound + 1
    final: tuple[int, ...] = ()
    for prefix in range(1, input_count + 1):
        row_width = min(prefix, width)
        final = tuple(range(first_variable, first_variable + row_width))
        first_variable += row_width
    return final, first_variable


@functools.lru_cache(maxsize=1)
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
    if degree == 18:
        return star
    finals, final_variable = counter_finals()
    if final_variable != BASE_VARIABLE_COUNT:
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
    anchor_a, anchor_b = anchor_vertices(degree)
    return tuple(
        -pairs[pair] for pair in itertools.combinations(anchor_a, 2)
    ) + tuple(pairs[pair] for pair in itertools.combinations(anchor_b, 2))


def matrix_bit(matrix: int, row: int, column: int) -> int:
    return (matrix >> (4 * row + column)) & 1


def feasible(matrix: int) -> bool:
    return all(
        any(not matrix_bit(matrix, row, column) for column in range(4))
        for row in range(4)
    ) and all(
        any(matrix_bit(matrix, row, column) for row in range(4))
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
            if matrix_bit(matrix, row, column):
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
                raise AssertionError("anchor matrix orbit partition failure")
            owner[member] = representative
    return tuple(sorted(representatives)), owner


def matrix_units(degree: int, matrix: int) -> tuple[int, ...]:
    pairs = edge_map()
    anchor_a, anchor_b = anchor_vertices(degree)
    return tuple(
        (
            pairs[tuple(sorted((anchor_a[row], anchor_b[column])))]
            if matrix_bit(matrix, row, column)
            else -pairs[tuple(sorted((anchor_a[row], anchor_b[column])))]
        )
        for row in range(4)
        for column in range(4)
    )


def expected_schedule(degree: int) -> list[dict[str, object]]:
    representatives, owner = representatives_and_owner()
    if len(owner) != 35_714 or len(representatives) != SELECTOR_COUNT:
        raise AssertionError("unexpected independent anchor orbit census")
    common = branch_units(degree) + anchor_units(degree)
    result: list[dict[str, object]] = []
    for index, matrix in enumerate(representatives):
        full_units = common + matrix_units(degree, matrix)
        selector = SELECTOR_VARIABLE_FIRST + index
        result.append(
            {
                "degree": degree,
                "cube_index": index,
                "cube_id": f"d{degree}_m{index:03d}",
                "matrix_integer": matrix,
                "matrix_hex": f"{matrix:04x}",
                "matrix_edge_count": matrix.bit_count(),
                "matrix_orbit_size": len(orbit(matrix)),
                "full_cube_assumption_count": len(full_units),
                "full_cube_assumptions_sha256": clause_stream_hash(
                    (literal,) for literal in full_units
                ),
                "selector": selector,
                "selector_assumption_sha256": selector_assumption_hash(selector),
            }
        )
    return result


def decode_graph6(text: str) -> list[int]:
    line = text.strip()
    if not line or ord(line[0]) - 63 != ORDER:
        raise ValueError("candidate is not short graph6 of order 43")
    payload = [ord(character) - 63 for character in line[1:]]
    needed = ORDER * (ORDER - 1) // 2
    if len(payload) * 6 < needed or any(not 0 <= value < 64 for value in payload):
        raise ValueError("invalid graph6 payload")
    adjacency = [0] * ORDER
    bit_index = 0
    for right in range(1, ORDER):
        for left in range(right):
            value = payload[bit_index // 6]
            edge = (value >> (5 - bit_index % 6)) & 1
            bit_index += 1
            if edge:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return adjacency


def independent_forbidden_counts(adjacency: list[int]) -> tuple[int, int]:
    clique_count = 0
    independent_count = 0
    for subset in itertools.combinations(range(ORDER), 5):
        edges = [
            (adjacency[left] >> right) & 1
            for offset, left in enumerate(subset)
            for right in subset[offset + 1 :]
        ]
        clique_count += int(all(edges))
        independent_count += int(not any(edges))
    return clique_count, independent_count


def replay_dimacs_truth(
    cnf_path: Path, true_variables: set[int], selector: int
) -> tuple[int, int]:
    header_variables: int | None = None
    header_clauses: int | None = None
    clauses_seen = 0
    pending = False
    pending_satisfied = False
    with cnf_path.open("r", encoding="ascii") as source:
        for line_number, raw_line in enumerate(source, start=1):
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("c"):
                continue
            if stripped.startswith("p"):
                fields = stripped.split()
                if (
                    len(fields) != 4
                    or fields[:2] != ["p", "cnf"]
                    or header_variables is not None
                ):
                    raise ValueError(
                        f"malformed DIMACS header on line {line_number}"
                    )
                header_variables = int(fields[2])
                header_clauses = int(fields[3])
                continue
            if header_variables is None:
                raise ValueError("DIMACS clause precedes header")
            for token in stripped.split():
                literal = int(token)
                if literal == 0:
                    if not pending:
                        raise ValueError(f"empty clause on line {line_number}")
                    clauses_seen += 1
                    if not pending_satisfied:
                        raise ValueError(
                            f"model falsifies DIMACS clause {clauses_seen}"
                        )
                    pending = False
                    pending_satisfied = False
                    continue
                if abs(literal) > header_variables:
                    raise ValueError("literal lies outside DIMACS header")
                pending = True
                if (literal > 0) == (abs(literal) in true_variables):
                    pending_satisfied = True
    if pending or header_variables is None or header_clauses is None:
        raise ValueError("incomplete DIMACS stream")
    if clauses_seen != header_clauses:
        raise ValueError("DIMACS clause-count mismatch")
    if selector not in true_variables:
        raise ValueError("selector assumption is false in saved model")
    if any(not 1 <= variable <= header_variables for variable in true_variables):
        raise ValueError("saved true variable is outside DIMACS header")
    return header_variables, clauses_seen


def verify_construction(
    construction: dict[str, object], cpp_verifier: Path, union_cnf: Path
) -> dict[str, object]:
    candidate_path = Path(str(construction["candidate_path"]))
    graph6 = candidate_path.read_text(encoding="ascii").strip()
    errors: list[str] = []
    if graph6 != construction.get("graph6"):
        errors.append("candidate graph6 differs from result")
    expected_hash = hashlib.sha256((graph6 + "\n").encode("ascii")).hexdigest()
    if expected_hash != construction.get("graph6_sha256"):
        errors.append("candidate graph6 SHA-256 mismatch")
    counts = independent_forbidden_counts(decode_graph6(graph6))
    if counts != (0, 0):
        errors.append(f"independent forbidden counts are {counts}")
    cpp = subprocess.run(
        [str(cpp_verifier), str(candidate_path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    if cpp.returncode != 0:
        errors.append("C++ verifier rejected candidate")
    true_variables_raw = construction.get("model_true_variables")
    replay_counts: tuple[int, int] | None = None
    if not isinstance(true_variables_raw, list) or any(
        not isinstance(variable, int) for variable in true_variables_raw
    ):
        errors.append("saved SAT model is malformed")
    else:
        true_variables = set(true_variables_raw)
        if len(true_variables) != len(true_variables_raw):
            errors.append("saved SAT model repeats a true variable")
        try:
            replay_counts = replay_dimacs_truth(
                union_cnf, true_variables, int(construction["selector"])
            )
        except (ValueError, OSError) as error:
            errors.append(f"independent union-CNF replay failed: {error}")
    return {
        "errors": errors,
        "independent_forbidden_counts": list(counts),
        "independent_union_cnf_replay_counts": (
            list(replay_counts) if replay_counts is not None else None
        ),
        "cpp_verifier_returncode": cpp.returncode,
        "cpp_verifier_stdout": cpp.stdout.strip(),
        "valid": not errors,
    }


def load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} does not contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    plan = load_object(args.plan)
    result = load_object(args.result)
    errors: list[str] = []
    if plan.get("schema") != "ramsey55.global_anchor_selector_cube_pilot.v1":
        errors.append("unexpected plan schema")
    if plan.get("status") != "FROZEN_BEFORE_RUN":
        errors.append("plan is not frozen")
    if result.get("schema") != (
        "ramsey55.global_anchor_selector_cube_pilot_result.v1"
    ):
        errors.append("unexpected result schema")
    if result.get("plan_sha256") != sha256_file(args.plan):
        errors.append("result plan SHA-256 mismatch")
    if result.get("worker_source_sha256") != plan.get("worker_source_sha256"):
        errors.append("worker source binding mismatch")
    worker_source = Path(str(plan.get("worker_source", "")))
    if (
        not worker_source.is_file()
        or sha256_file(worker_source) != plan.get("worker_source_sha256")
    ):
        errors.append("frozen worker source file mismatch")
    if sha256_file(Path(__file__)) != plan.get("checker_source_sha256"):
        errors.append("frozen checker source file mismatch")
    if result.get("proof_logging") is not False:
        errors.append("proof logging was not false")
    if result.get("negative_certified") is not False:
        errors.append("result improperly certifies negative outcomes")

    input_errors: list[str] = []
    inputs = plan.get("inputs")
    if not isinstance(inputs, list):
        input_errors.append("plan inputs missing")
        inputs = []
    for item in inputs:
        if not isinstance(item, dict):
            input_errors.append("input record is not an object")
            continue
        path = Path(str(item["path"]))
        if not path.is_file():
            input_errors.append(f"input missing: {path}")
        elif sha256_file(path) != item.get("sha256"):
            input_errors.append(f"input hash mismatch: {path}")
    errors.extend(input_errors)

    branches = plan.get("branches")
    if not isinstance(branches, list):
        branches = []
        errors.append("plan branches missing")
    schedules: dict[int, list[dict[str, object]]] = {}
    cover_plan_errors: list[str] = []
    union_check_errors: list[str] = []
    for branch in branches:
        if not isinstance(branch, dict):
            cover_plan_errors.append("branch record is not an object")
            continue
        degree = int(branch["degree"])
        schedule = expected_schedule(degree)
        schedules[degree] = schedule
        if sha256_json_object(schedule) != branch.get("schedule_sha256"):
            cover_plan_errors.append(f"degree-{degree} schedule hash mismatch")

        cover_plan = load_object(Path(str(branch["cover_plan"])))
        cover_branch = cover_plan
        if degree != 18:
            candidates = [
                item
                for item in cover_plan.get("branches", [])
                if isinstance(item, dict) and item.get("degree") == degree
            ]
            cover_branch = candidates[0] if len(candidates) == 1 else {}
        observed_cubes = cover_branch.get("cubes")
        if not isinstance(observed_cubes, list) or len(observed_cubes) != 143:
            cover_plan_errors.append(f"degree-{degree} cover cube count")
        else:
            for expected, observed in zip(schedule, observed_cubes):
                for expected_key, observed_key in (
                    ("cube_id", "cube_id"),
                    ("cube_index", "cube_index"),
                    ("matrix_integer", "matrix_integer"),
                    ("matrix_hex", "matrix_hex"),
                    ("matrix_edge_count", "matrix_edge_count"),
                    ("matrix_orbit_size", "matrix_orbit_size"),
                    ("full_cube_assumption_count", "assumption_count"),
                    ("full_cube_assumptions_sha256", "assumptions_sha256"),
                ):
                    if expected[expected_key] != observed.get(observed_key):
                        cover_plan_errors.append(
                            f"{expected['cube_id']} field {observed_key}"
                        )

        check = load_object(Path(str(branch["union_check"])))
        materialized = check.get("materialized_union")
        if check.get("valid") is not True or not isinstance(materialized, dict):
            union_check_errors.append(f"degree-{degree} union check invalid")
        else:
            if materialized.get("valid") is not True:
                union_check_errors.append(
                    f"degree-{degree} materialized union invalid"
                )
            if materialized.get("union_cnf_sha256") != branch.get(
                "union_cnf_sha256"
            ):
                union_check_errors.append(
                    f"degree-{degree} union hash not tied to check"
                )
    errors.extend(cover_plan_errors)
    errors.extend(union_check_errors)

    expected_records = [
        record for degree in (18, 19, 20) for record in schedules.get(degree, [])
    ]
    records = result.get("records")
    if not isinstance(records, list):
        records = []
        errors.append("result records missing")
    record_errors: list[str] = []
    for position, (expected, observed) in enumerate(
        zip(expected_records, records)
    ):
        if not isinstance(observed, dict):
            record_errors.append(f"record {position} is not an object")
            continue
        for key, expected_value in expected.items():
            if observed.get(key) != expected_value:
                record_errors.append(f"record {position} field {key}")
        if observed.get("branch_schedule_position") != position // 143:
            record_errors.append(
                f"record {position} branch_schedule_position"
            )
        if observed.get("cube_schedule_position") != position % 143:
            record_errors.append(f"record {position} cube_schedule_position")
        status = observed.get("status")
        if status not in ALLOWED_STATUSES:
            record_errors.append(f"record {position} status")
        if observed.get("negative_certified") is not False:
            record_errors.append(f"record {position} negative certification")
        if observed.get("conflict_budget") != plan.get(
            "conflict_budget_per_cube"
        ):
            record_errors.append(f"record {position} conflict budget")
        for key in ("conflicts", "decisions", "propagations"):
            value = observed.get(key)
            if not isinstance(value, int) or value < 0:
                record_errors.append(f"record {position} field {key}")
    if len(records) > len(expected_records):
        record_errors.append("result has more records than schedule")
    errors.extend(record_errors)

    status_counts = Counter(
        record.get("status")
        for record in records
        if isinstance(record, dict)
    )
    aggregate_errors: list[str] = []
    if result.get("completed_cube_count") != len(records):
        aggregate_errors.append("completed_cube_count mismatch")
    if result.get("status_counts") != dict(sorted(status_counts.items())):
        aggregate_errors.append("status_counts mismatch")
    for result_key, record_key in (
        ("total_conflicts", "conflicts"),
        ("total_decisions", "decisions"),
        ("total_propagations", "propagations"),
    ):
        expected_total = sum(
            int(record.get(record_key, 0))
            for record in records
            if isinstance(record, dict)
        )
        if result.get(result_key) != expected_total:
            aggregate_errors.append(f"{result_key} mismatch")
    construction = result.get("construction")
    if construction is None:
        if result.get("scheduled_complete") is not True:
            aggregate_errors.append("no-SAT result is not schedule-complete")
        if result.get("full_cover_screened") is not True:
            aggregate_errors.append("no-SAT result is not full-cover screened")
        if len(records) != 429:
            aggregate_errors.append("no-SAT result does not cover 429 cubes")
        if status_counts.get("SAT", 0):
            aggregate_errors.append("SAT record lacks construction")
    else:
        if not isinstance(construction, dict):
            aggregate_errors.append("construction is not an object")
        if status_counts.get("SAT", 0) != 1:
            aggregate_errors.append("construction does not have one SAT record")
        if not records or records[-1].get("status") != "SAT":
            aggregate_errors.append("pilot did not stop immediately at SAT")
    errors.extend(aggregate_errors)

    construction_check: dict[str, object] | None = None
    if isinstance(construction, dict):
        matching_branches = [
            branch
            for branch in branches
            if isinstance(branch, dict)
            and branch.get("degree") == construction.get("degree")
        ]
        if len(matching_branches) != 1:
            errors.append("construction branch is not uniquely specified")
            matching_union = Path("/nonexistent")
        else:
            matching_union = Path(str(matching_branches[0]["union_cnf"]))
        construction_check = verify_construction(
            construction,
            Path(str(plan["cpp_verifier"])),
            matching_union,
        )
        if construction_check["valid"] is not True:
            errors.extend(
                f"construction: {message}"
                for message in construction_check["errors"]
            )

    audit = {
        "checker": CHECKER_ID,
        "checker_source_sha256": sha256_file(Path(__file__)),
        "plan_sha256": sha256_file(args.plan),
        "result_sha256": sha256_file(args.result),
        "independent_feasible_matrix_count": len(representatives_and_owner()[1]),
        "independent_canonical_matrix_count": len(
            representatives_and_owner()[0]
        ),
        "independent_schedule_cube_count": len(expected_records),
        "input_error_count": len(input_errors),
        "cover_plan_error_count": len(cover_plan_errors),
        "union_check_error_count": len(union_check_errors),
        "record_error_count": len(record_errors),
        "aggregate_error_count": len(aggregate_errors),
        "construction_check": construction_check,
        "errors": errors,
        "valid": not errors,
        "claim_boundary": (
            "This checks schedule coverage, exact selector-to-cube bindings, "
            "and result arithmetic. Negative solver outcomes remain unproved."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(audit, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(args.output)
    print(json.dumps(audit, sort_keys=True))
    return 0 if audit["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
