#!/usr/bin/env python3
"""CP-SAT model for the complete characteristic-2/3 anti-fold relaxation.

The support bits occur quadratically.  This model expands every retained
product as

    (1-x)(1-y) = 1-x-y+xy

and shares the Boolean products across all twenty independent lags.  After
dividing each integer equation by its content (four in the canonical
instances), divisibility by six imposes the complete normalized
characteristic-two and characteristic-three relaxations simultaneously.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
import json
from math import gcd
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))

from ortools.sat.python import cp_model  # noqa: E402

import search_eliahou_antifold_sat as exact  # noqa: E402
import search_char3_antifold as char3  # noqa: E402


SupportKey = tuple[str, int]
ProductKey = tuple[SupportKey, SupportKey]


@dataclass(frozen=True)
class QuadraticEquation:
    lag: int
    constant: int
    linear: dict[SupportKey, int]
    quadratic: dict[ProductKey, int]
    content: int


def retained_key(
    row: int,
    cell: int,
    case: exact.PairCase,
    support_keys: set[SupportKey],
    seed_rows: tuple[tuple[int, ...], ...],
) -> bool | SupportKey | None:
    if seed_rows[row][cell] == 0:
        return None
    active_row = 1 if case.block == "L" else 3
    if row == active_row and cell in exact.q_cells(case):
        return None
    block = "L" if row < 2 else "S"
    key = (block, cell)
    return key if key in support_keys else True


def add_coefficient(mapping: dict, key, coefficient: int) -> None:
    mapping[key] = mapping.get(key, 0) + coefficient
    if mapping[key] == 0:
        del mapping[key]


def quadratic_equations(
    case: exact.PairCase,
    support_keys: set[SupportKey],
) -> tuple[QuadraticEquation, ...]:
    seed_rows = exact.seed_antifold()
    result = []
    for lag in range(1, exact.FOLD // 2):
        constant = 0
        linear: dict[SupportKey, int] = {}
        quadratic: dict[ProductKey, int] = {}
        for row, left, right in product(
            range(4), range(exact.FOLD), range(exact.FOLD)
        ):
            exponent = left - right
            wrap_sign = 1
            if exponent < 0:
                exponent += exact.FOLD
                wrap_sign = -1
            if exponent != lag:
                continue
            left_key = retained_key(
                row, left, case, support_keys, seed_rows
            )
            right_key = retained_key(
                row, right, case, support_keys, seed_rows
            )
            if left_key is None or right_key is None:
                continue
            coefficient = (
                wrap_sign * seed_rows[row][left] * seed_rows[row][right]
            )
            constant += coefficient
            if left_key is not True:
                add_coefficient(linear, left_key, -coefficient)
            if right_key is not True and right_key != left_key:
                add_coefficient(linear, right_key, -coefficient)
            if (
                left_key is not True
                and right_key is not True
                and left_key != right_key
            ):
                pair = tuple(sorted((left_key, right_key)))
                add_coefficient(quadratic, pair, coefficient)

        content = abs(constant)
        for coefficient in (*linear.values(), *quadratic.values()):
            content = gcd(content, abs(coefficient))
        if content == 0:
            content = 1
        result.append(
            QuadraticEquation(
                lag=lag,
                constant=constant // content,
                linear={
                    key: value // content for key, value in linear.items()
                },
                quadratic={
                    key: value // content
                    for key, value in quadratic.items()
                },
                content=content,
            )
        )
    return tuple(result)


def expression_bounds(
    equation: QuadraticEquation,
) -> tuple[int, int]:
    coefficients = (
        *equation.linear.values(),
        *equation.quadratic.values(),
    )
    return (
        equation.constant + sum(min(0, value) for value in coefficients),
        equation.constant + sum(max(0, value) for value in coefficients),
    )


def build(
    case: exact.PairCase,
    modulus: int,
) -> tuple[
    cp_model.CpModel,
    dict[SupportKey, cp_model.IntVar],
    tuple[QuadraticEquation, ...],
    int,
]:
    if modulus < 2:
        raise ValueError("modulus must be at least two")
    model = cp_model.CpModel()

    # Reuse the authoritative support-domain construction.
    _, _, id_variables, _ = char3.build(case, ())
    support_keys = set(id_variables)
    support = {
        key: model.NewBoolVar(f"{key[0]}_{key[1]}")
        for key in sorted(support_keys)
    }
    model.Add(sum(support.values()) == 39)

    equations = quadratic_equations(case, support_keys)
    product_keys = sorted(
        {
            pair
            for equation in equations
            for pair in equation.quadratic
        }
    )
    pair_variables = {}
    for left, right in product_keys:
        variable = model.NewBoolVar(
            f"prod_{left[0]}_{left[1]}_{right[0]}_{right[1]}"
        )
        model.AddMultiplicationEquality(
            variable, [support[left], support[right]]
        )
        pair_variables[(left, right)] = variable

    for equation in equations:
        expression = (
            equation.constant
            + sum(
                coefficient * support[key]
                for key, coefficient in equation.linear.items()
            )
            + sum(
                coefficient * pair_variables[key]
                for key, coefficient in equation.quadratic.items()
            )
        )
        minimum, maximum = expression_bounds(equation)
        quotient = model.NewIntVar(
            minimum // modulus - 1,
            maximum // modulus + 1,
            f"quotient_lag_{equation.lag}",
        )
        model.Add(expression == modulus * quotient)
    return model, support, equations, len(pair_variables)


def replay(
    case: exact.PairCase,
    selected: tuple[SupportKey, ...],
    equations: tuple[QuadraticEquation, ...],
    modulus: int,
) -> dict[str, object]:
    correlations = exact.negacyclic_correlations(
        exact.direct_rows(case, set(selected))
    )
    if len(selected) != 39 or correlations[0] != 334:
        raise AssertionError("CP-SAT support failed shell replay")
    normalized = []
    for equation in equations:
        value = correlations[equation.lag]
        if value % equation.content:
            raise AssertionError("equation content failed direct replay")
        value //= equation.content
        if value % modulus:
            raise AssertionError("CP-SAT support failed modular replay")
        normalized.append(value)
    return {
        "selected": [[block, cell] for block, cell in selected],
        "normalized_residuals": normalized,
        "full_exact": all(value == 0 for value in normalized),
        "nonzero_lags": sum(value != 0 for value in normalized),
        "l1": sum(abs(value) for value in normalized),
        "linf": max(abs(value) for value in normalized),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=30)
    parser.add_argument(
        "--modulus",
        type=int,
        default=6,
        help="6 combines the normalized characteristic-2 and -3 layers",
    )
    parser.add_argument("--time-limit", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    char3.factorization_self_test()
    if args.time_limit <= 0 or args.workers < 1:
        raise ValueError("time limit and worker count must be positive")
    cases = char3.canonical_cases()
    if not 0 <= args.start <= args.stop <= len(cases):
        raise ValueError("invalid case range")

    output = []
    for case_number in range(args.start, args.stop):
        case = cases[case_number]
        started = time.monotonic()
        model, support, equations, product_count = build(
            case, args.modulus
        )
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = args.time_limit
        solver.parameters.num_search_workers = args.workers
        solver.parameters.random_seed = 668_423
        status = solver.Solve(model)
        record = None
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            selected = tuple(
                key
                for key, variable in support.items()
                if solver.Value(variable)
            )
            record = replay(case, selected, equations, args.modulus)
        output.append(
            {
                "case": case_number,
                "block": case.block,
                "q_index": case.index,
                "modulus": args.modulus,
                "support_variables": len(support),
                "product_variables": product_count,
                "equation_contents": [
                    equation.content for equation in equations
                ],
                "status": solver.StatusName(status),
                "model": record,
                "conflicts": solver.NumConflicts(),
                "branches": solver.NumBranches(),
                "wall_time": solver.WallTime(),
                "total_seconds": time.monotonic() - started,
            }
        )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
