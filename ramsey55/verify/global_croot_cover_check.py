#!/usr/bin/env python3
"""Independent structural checker for the exact order-43 c-root cover plan.

The checker imports neither the plan generator nor the Ramsey CNF modules.
It independently reconstructs edge variables, both families of sequential
threshold counters, all four c-root cardinality branches, and all nine
exact-mu selector refinements.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


ORDER = 43
BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
CROOT_DEGREES = (18, 19, 20, 21)
MU_VALUES = (18, 19, 20)
CHECKER_ID = "ramsey55.global_croot_cover_checker.v1"


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


def edge_variable(left: int, right: int) -> int:
    if left > right:
        left, right = right, left
    if not 0 <= left < right < ORDER:
        raise ValueError("invalid edge")
    return 1 + left * (2 * ORDER - left - 1) // 2 + right - left - 1


def allocate_rows(
    input_count: int, bound: int, first_auxiliary: int
) -> tuple[tuple[tuple[int, ...], ...], int]:
    if bound <= 0 or bound >= input_count:
        return (), first_auxiliary
    width = bound + 1
    rows: list[tuple[int, ...]] = []
    next_variable = first_auxiliary
    for prefix_length in range(1, input_count + 1):
        row_width = min(prefix_length, width)
        rows.append(tuple(range(next_variable, next_variable + row_width)))
        next_variable += row_width
    return tuple(rows), next_variable


def counter_clauses(
    literals: Sequence[int],
    bound: int,
    rows: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    if bound < 0:
        return ((),)
    if bound >= len(literals):
        return ()
    if bound == 0:
        return tuple((-literal,) for literal in literals)
    width = bound + 1
    if len(rows) != len(literals) or len(rows[-1]) != width:
        raise AssertionError("malformed independent counter")
    clauses: list[tuple[int, ...]] = []
    for index, literal in enumerate(literals):
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
    return tuple(clauses)


def base_counter_finals() -> tuple[tuple[tuple[int, ...], ...], int]:
    next_variable = math.comb(ORDER, 2) + 1
    finals: list[tuple[int, ...]] = []
    for _vertex in range(ORDER):
        for _kind in range(2):
            rows, next_variable = allocate_rows(42, 24, next_variable)
            finals.append(tuple(rows[-1]))
    if next_variable - 1 != BASE_VARIABLE_COUNT:
        raise AssertionError("independent base-counter layout changed")
    return tuple(finals), next_variable


def interval_units(mu: int) -> tuple[int, ...]:
    if mu not in MU_VALUES:
        raise ValueError("unsupported mu")
    if mu == 18:
        return ()
    finals, _next_variable = base_counter_finals()
    threshold = ORDER - mu
    return tuple(
        -finals[2 * vertex + kind][threshold - 1]
        for vertex in range(ORDER)
        for kind in (0, 1)
    )


def star_units(degree: int) -> tuple[int, ...]:
    return tuple(
        (
            edge_variable(0, other)
            if other <= degree
            else -edge_variable(0, other)
        )
        for other in range(1, ORDER)
    )


def good_literals(degree: int) -> tuple[int, ...]:
    side_a = tuple(range(1, degree + 1))
    side_b = tuple(range(degree + 1, ORDER))
    return tuple(
        edge_variable(left, right)
        for left, right in itertools.combinations(side_a, 2)
    ) + tuple(
        -edge_variable(left, right)
        for left, right in itertools.combinations(side_b, 2)
    )


def threshold(degree: int) -> int:
    b_size = ORDER - 1 - degree
    value = Fraction(math.comb(b_size, 2), 1) - Fraction(
        degree * (ORDER - 2 * degree), 2
    )
    return math.ceil(value)


def croot_counter_data(
    degree: int,
) -> tuple[
    tuple[int, ...],
    int,
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
    int,
]:
    good = good_literals(degree)
    bad = tuple(-literal for literal in good)
    bound = len(good) - threshold(degree)
    rows, next_variable = allocate_rows(
        len(bad), bound, BASE_VARIABLE_COUNT + 1
    )
    clauses = counter_clauses(bad, bound, rows)
    return bad, bound, rows, clauses, next_variable


def basic_record(degree: int) -> dict[str, object]:
    good = good_literals(degree)
    _bad, bound, rows, counter, next_variable = croot_counter_data(degree)
    additions = tuple((literal,) for literal in star_units(degree)) + counter
    b_size = ORDER - 1 - degree
    raw_bound = Fraction(math.comb(b_size, 2), 1) - Fraction(
        degree * (ORDER - 2 * degree), 2
    )
    return {
        "degree": degree,
        "A_size": degree,
        "B_size": b_size,
        "croot_threshold_rational": (
            str(raw_bound.numerator)
            if raw_bound.denominator == 1
            else f"{raw_bound.numerator}/{raw_bound.denominator}"
        ),
        "good_literal_count": len(good),
        "good_literal_stream_sha256": clause_stream_sha256(
            (literal,) for literal in good
        ),
        "required_good_literal_count": threshold(degree),
        "bad_literal_at_most_bound": bound,
        "star_unit_count": len(star_units(degree)),
        "star_units_sha256": clause_stream_sha256(
            (literal,) for literal in star_units(degree)
        ),
        "counter_first_auxiliary": BASE_VARIABLE_COUNT + 1,
        "counter_auxiliary_count": sum(map(len, rows)),
        "counter_clause_count": len(counter),
        "appended_clause_count": len(additions),
        "appended_clause_stream_sha256": clause_stream_sha256(additions),
        "variable_count": next_variable - 1,
        "clause_count": BASE_CLAUSE_COUNT + len(additions),
    }


def refined_data(
    degree: int, mu: int
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[int, ...],
    tuple[int, ...],
    int,
    int,
]:
    _bad, _bound, rows, croot_clauses, next_variable = croot_counter_data(
        degree
    )
    selectors = tuple(range(next_variable, next_variable + 2 * ORDER))
    finals, _base_next = base_counter_finals()
    selector_clauses: list[tuple[int, ...]] = [selectors]
    triggers: list[int] = []
    for vertex in range(ORDER):
        low_selector = selectors[2 * vertex]
        high_selector = selectors[2 * vertex + 1]
        edge_trigger = finals[2 * vertex][mu]
        nonedge_trigger = finals[2 * vertex + 1][mu]
        selector_clauses.append((-low_selector, -edge_trigger))
        selector_clauses.append((-high_selector, -nonedge_trigger))
        triggers.extend((edge_trigger, nonedge_trigger))
    additions = (
        tuple((literal,) for literal in star_units(degree))
        + croot_clauses
        + tuple((literal,) for literal in interval_units(mu))
        + tuple(selector_clauses)
    )
    return (
        additions,
        selectors,
        tuple(triggers),
        sum(map(len, rows)),
        next_variable + 2 * ORDER,
    )


def refined_record(degree: int, mu: int) -> dict[str, object]:
    additions, selectors, triggers, auxiliary_count, after = refined_data(
        degree, mu
    )
    units = interval_units(mu)
    return {
        "branch_id": f"mu{mu}_d{degree}",
        "mu": mu,
        "degree": degree,
        "global_degree_interval": [mu, ORDER - 1 - mu],
        "global_interval_unit_count": len(units),
        "global_interval_units_sha256": clause_stream_sha256(
            (literal,) for literal in units
        ),
        "exact_mu_condition": (
            "at least one selected vertex has degree mu or degree 42-mu"
        ),
        "selector_variable_first": selectors[0],
        "selector_count": len(selectors),
        "selector_order": (
            "vertex 0 low, vertex 0 high, vertex 1 low, vertex 1 high, ..."
        ),
        "selector_cover_clause_sha256": clause_stream_sha256((selectors,)),
        "selector_implication_clause_count": 2 * ORDER,
        "base_counter_trigger_variable_count": len(triggers),
        "base_counter_trigger_variables_sha256": clause_stream_sha256(
            (variable,) for variable in triggers
        ),
        "counter_auxiliary_count": auxiliary_count,
        "appended_clause_count": len(additions),
        "appended_clause_stream_sha256": clause_stream_sha256(additions),
        "variable_count": after - 1,
        "clause_count": BASE_CLAUSE_COUNT + len(additions),
    }


def graph_degrees(adjacency: Sequence[int]) -> tuple[int, ...]:
    return tuple(neighbors.bit_count() for neighbors in adjacency)


def complement(adjacency: Sequence[int]) -> list[int]:
    order = len(adjacency)
    mask = (1 << order) - 1
    return [
        mask & ~(neighbors | (1 << vertex))
        for vertex, neighbors in enumerate(adjacency)
    ]


def induced_edges(adjacency: Sequence[int], vertices: Sequence[int]) -> int:
    return sum(
        (adjacency[left] >> right) & 1
        for left, right in itertools.combinations(vertices, 2)
    )


def local_excess_twice(adjacency: Sequence[int], vertex: int) -> int:
    order = len(adjacency)
    neighbors = tuple(
        other
        for other in range(order)
        if other != vertex and (adjacency[vertex] >> other) & 1
    )
    nonneighbors = tuple(
        other
        for other in range(order)
        if other != vertex and not (adjacency[vertex] >> other) & 1
    )
    degree = len(neighbors)
    return 2 * (
        induced_edges(adjacency, nonneighbors)
        - induced_edges(adjacency, neighbors)
    ) - degree * (order - 2 * degree)


def algebra_audit() -> dict[str, object]:
    thresholds = {str(degree): threshold(degree) for degree in CROOT_DEGREES}
    complement_invariance = True
    for degree in range(ORDER):
        complement_degree = ORDER - 1 - degree
        correction = math.comb(degree, 2) - math.comb(complement_degree, 2)
        penalty = Fraction(degree * (ORDER - 2 * degree), 2)
        complement_penalty = Fraction(
            complement_degree * (ORDER - 2 * complement_degree), 2
        )
        if complement_penalty - penalty != correction:
            complement_invariance = False
    refined_pairs = [
        [mu, degree]
        for mu in MU_VALUES
        for degree in CROOT_DEGREES
        if mu <= degree
    ]
    return {
        "zero_sum_edge_contribution_identity": (
            "for each edge xy, common-nonneighbor count minus "
            "common-neighbor count equals 43-d(x)-d(y)"
        ),
        "zero_sum_degree_polynomial_identity": (
            "sum_v d(v)(43-2d(v))/2=43|E|-sum_v d(v)^2"
        ),
        "complement_invariance_checked_for_all_degrees_0_through_42": (
            complement_invariance
        ),
        "thresholds": thresholds,
        "thresholds_match_expected": thresholds
        == {"18": 213, "19": 206, "20": 201, "21": 200},
        "basic_degrees": list(CROOT_DEGREES),
        "refined_mu_degree_pairs": refined_pairs,
        "refined_pair_count": len(refined_pairs),
        "mu21_parity_degree_sum": 21 * ORDER,
        "mu21_parity_impossible": (21 * ORDER) % 2 == 1,
        "valid": (
            complement_invariance
            and thresholds
            == {"18": 213, "19": 206, "20": 201, "21": 200}
            and len(refined_pairs) == 9
            and (21 * ORDER) % 2 == 1
        ),
    }


def load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} does not contain an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    plan = load_object(args.plan)
    errors: list[str] = []
    if plan.get("schema") != "ramsey55.global_croot_cover.v1":
        errors.append("unexpected plan schema")
    if plan.get("status") != "EXACT_COVER_PLAN_NO_SOLVE_CLAIM":
        errors.append("unexpected plan status")
    if plan.get("base_variable_count") != BASE_VARIABLE_COUNT:
        errors.append("base variable count mismatch")
    if plan.get("base_clause_count") != BASE_CLAUSE_COUNT:
        errors.append("base clause count mismatch")

    source_path = Path(str(plan.get("source", "src/global_croot_cover.py")))
    if not source_path.is_file():
        errors.append("generator source is missing")
    elif sha256_file(source_path) != plan.get("source_sha256"):
        errors.append("generator source hash mismatch")
    if plan.get("checker_source_sha256") != sha256_file(Path(__file__)):
        errors.append("checker source hash mismatch")

    algebra = algebra_audit()
    if algebra["valid"] is not True:
        errors.append("independent algebra audit failed")

    basic_section = plan.get("basic_cover")
    if not isinstance(basic_section, dict):
        basic_section = {}
        errors.append("basic cover section missing")
    expected_basic = [basic_record(degree) for degree in CROOT_DEGREES]
    if basic_section.get("branches") != expected_basic:
        errors.append("basic branch records mismatch")
    if basic_section.get("branch_count") != len(expected_basic):
        errors.append("basic branch count mismatch")

    refined_section = plan.get("optional_exact_mu_refinement")
    if not isinstance(refined_section, dict):
        refined_section = {}
        errors.append("exact-mu refinement section missing")
    expected_refined = [
        refined_record(degree, mu)
        for mu in MU_VALUES
        for degree in CROOT_DEGREES
        if mu <= degree
    ]
    if refined_section.get("branches") != expected_refined:
        errors.append("exact-mu branch records mismatch")
    if refined_section.get("branch_count") != len(expected_refined):
        errors.append("exact-mu branch count mismatch")

    audit = {
        "checker": CHECKER_ID,
        "checker_source_sha256": sha256_file(Path(__file__)),
        "plan_sha256": sha256_file(args.plan),
        "independent_algebra": algebra,
        "independent_basic_branch_count": len(expected_basic),
        "independent_exact_mu_branch_count": len(expected_refined),
        "errors": errors,
        "valid": not errors,
        "claim_boundary": (
            "This checks the algebra and deterministic CNF additions only. "
            "It makes no SAT, UNSAT, or Ramsey-bound claim."
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
