#!/usr/bin/env python3
"""Exact one-hot SAT search for the orbit-2 h=0 second digit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
SECOND = SEARCH / "phase_second_digit"
HIGHER = SECOND / "higher_digits"
sys.path[:0] = [str(HIGHER), str(SECOND), str(SEARCH)]

from pysat.solvers import Solver  # noqa: E402

import solve_full_second_digit_sat as sat  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
from verify_lp333_order3_labeled_jet import actual_word  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    first_digit_equations,
    matrix_rank,
    profiles_from_ids,
)
from verify_lp333_order3_phase_transfer import row_sum_catalog  # noqa: E402


PROFILE_IDS_A = (1, 2, 6, 1, 5, 1, 4, 5, 1, 5, 7, 4)
PROFILE_IDS_B = (2, 4, 2, 4, 4, 6, 5, 5, 8, 1, 5, 8)
TARGET = (-3, 0, 0, 3)
ACTIVE_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))


def labelled_aggregate(
    masks_a: tuple[int, ...], masks_b: tuple[int, ...]
) -> tuple[int, ...]:
    words = tuple(
        tuple(
            actual_word(channel, class_index, masks[class_index])
            for class_index in range(12)
        )
        for channel, masks in enumerate((masks_a, masks_b))
    )
    aggregate = []
    for row in range(9):
        plus_a = sum(word[row] for word in words[0])
        plus_b = sum(word[row] for word in words[1])
        aggregate.extend((plus_a + plus_b - 12, plus_b - plus_a))
    return tuple(aggregate)


def exact_forms():
    profiles = profiles_from_ids(PROFILE_IDS_A, PROFILE_IDS_B)
    rows = augmented_system(first_digit_equations(profiles))
    coefficients = tuple(row[:-1] for row in rows)
    origin = canonical_solution(rows, 54)
    if origin is None:
        raise AssertionError("first digit became inconsistent")
    basis = second.nullspace_basis(coefficients, columns=54)
    if matrix_rank(coefficients) != 18 or len(basis) != 36:
        raise AssertionError("first-digit rank/nullity changed")
    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles), origin, basis
    )
    active = tuple(
        index
        for index in range(20)
        if (
            constants[index]
            or any(linears[index])
            or any(value for row in polars[index] for value in row)
        )
    )
    if active != ACTIVE_ROWS:
        raise AssertionError("the eighteen active quadrics changed")
    return (
        profiles,
        origin,
        basis,
        tuple(constants[index] for index in active),
        tuple(linears[index] for index in active),
        tuple(polars[index] for index in active),
    )


def solve(solver_name: str = "cadical195") -> dict:
    profiles, origin, basis, constants, linears, polars = exact_forms()
    circuit, inputs = sat.build_cnf(constants, linears, polars)
    with Solver(
        name=solver_name, bootstrap_with=circuit.clauses
    ) as solver:
        satisfiable = solver.solve()
        statistics = solver.accum_stats()
        model = solver.get_model() if satisfiable else None
    if not satisfiable:
        return {
            "status": "UNSAT",
            "profile_ids_a": PROFILE_IDS_A,
            "profile_ids_b": PROFILE_IDS_B,
            "target": TARGET,
            "cnf": {
                "boolean_variables": circuit.next_variable - 1,
                "ternary_wires": circuit.trits,
                "truth_table_gates": circuit.gates,
                "clauses": len(circuit.clauses),
                "solver": solver_name,
                "statistics": statistics,
            },
        }
    if model is None:
        raise AssertionError("SAT result omitted its model")
    affine = sat.decode_trits(model, inputs)
    placement = second.lift_affine_point(origin, basis, affine)
    first = second.symbolic_first_digits(
        first_digit_equations(profiles), placement
    )
    symbolic_second = second.symbolic_second_digits(
        second.second_digit_term_data(profiles), placement
    )
    direct_second = second.direct_second_digits(profiles, placement)
    if first != (0,) * 20:
        raise AssertionError("SAT point failed first digit")
    if symbolic_second != (0,) * 20 or direct_second != (0,) * 20:
        raise AssertionError("SAT point failed direct second-digit replay")
    values = second.displayed_values(profiles, placement)
    digits = tuple(second.lambda_digits(value, 10) for value in values)
    digit_counts = tuple(
        sum(row[digit] != 0 for row in digits) for digit in range(10)
    )
    masks_a, masks_b = second.masks_from_trits(profiles, placement)
    aggregate = labelled_aggregate(masks_a, masks_b)
    return {
        "status": "SAT",
        "scope": (
            "Exact digit-2 placement witness for the orbit-2 h=0 "
            "compressed profile; not an LP(333) or H(668)."
        ),
        "profile_ids_a": PROFILE_IDS_A,
        "profile_ids_b": PROFILE_IDS_B,
        "target": TARGET,
        "active_quadratic_rows": ACTIVE_ROWS,
        "first_layer_rank": 18,
        "first_layer_nullity": 36,
        "affine_coordinates": affine,
        "placement_trits": placement,
        "masks_a": masks_a,
        "masks_b": masks_b,
        "displayed_exact_values": values,
        "lambda_digits_through_9": digits,
        "digit_residual_counts": digit_counts,
        "row_margin_aggregate": aggregate,
        "row_margin_catalog_member": aggregate in row_sum_catalog(),
        "cnf": {
            "boolean_variables": circuit.next_variable - 1,
            "ternary_wires": circuit.trits,
            "truth_table_gates": circuit.gates,
            "clauses": len(circuit.clauses),
            "solver": solver_name,
            "statistics": statistics,
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    result = solve(args.solver)
    print(json.dumps(result, indent=2))
    if result["status"] == "SAT":
        print("PASS: orbit-2 digit-2 witness replayed exactly")
    else:
        print("PASS: orbit-2 digit-2 system excluded by exact SAT")
