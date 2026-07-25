#!/usr/bin/env python3
"""Bounded exact lower/upper/none diagnostic for one Eliahou long case.

Each eligible cell has mutually exclusive lower- and upper-endpoint flip
Booleans.  The same variables drive:

* the exact 39-cell support and four signed root-profile equations;
* the characteristic-two anti-fold equations;
* both 42-fold cyclic norm images; and, by default,
* all 83 original aperiodic base-sequence equations.

All quadratic sign products are shared.  A CP-SAT status is only a bounded
diagnostic.  Every assignment is decoded to the physical four rows and
replayed with independent integer correlation routines before it is reported.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
from random import Random
import sys
from typing import Iterable

from ortools.sat.python import cp_model


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
TRIAGE = SEARCH / "eliahou_long_block_exact_triage"
CHAR3 = SEARCH / "eliahou_char3_jet"
sys.path[:0] = [str(HERE), str(CHAR3), str(TRIAGE), str(SEARCH)]

import audit_orientation_cascade as cascade  # noqa: E402
import search_char3_local as local  # noqa: E402
import verify_eliahou_adjacent42_repair as adjacent  # noqa: E402
import verify_eliahou_antifold42 as antifold  # noqa: E402


@dataclass
class Polynomial:
    constant: int
    linear: dict[int, int]
    quadratic: dict[tuple[int, int], int]


def add_coefficient(table: dict, key, value: int) -> None:
    if not value:
        return
    table[key] = table.get(key, 0) + value
    if not table[key]:
        del table[key]


def add_polynomials(
    terms: Iterable[tuple[int, Polynomial]],
) -> Polynomial:
    constant = 0
    linear: dict[int, int] = {}
    quadratic: dict[tuple[int, int], int] = {}
    for scale, term in terms:
        constant += scale * term.constant
        for key, value in term.linear.items():
            add_coefficient(linear, key, scale * value)
        for key, value in term.quadratic.items():
            add_coefficient(quadratic, key, scale * value)
    return Polynomial(constant, linear, quadratic)


def sign_product(
    left: tuple[int, int | None],
    right: tuple[int, int | None],
    exclusive_pairs: set[tuple[int, int]],
) -> Polynomial:
    """Expand s_i(1-2b_i)s_j(1-2b_j) as a Boolean polynomial."""

    seed_product = left[0] * right[0]
    left_flip = left[1]
    right_flip = right[1]
    if left_flip is None and right_flip is None:
        return Polynomial(seed_product, {}, {})
    if left_flip == right_flip:
        # This includes the zero-lag square of one signed coordinate.
        return Polynomial(seed_product, {}, {})
    linear: dict[int, int] = {}
    if left_flip is not None:
        add_coefficient(linear, left_flip, -2 * seed_product)
    if right_flip is not None:
        add_coefficient(linear, right_flip, -2 * seed_product)
    quadratic: dict[tuple[int, int], int] = {}
    if left_flip is not None and right_flip is not None:
        pair = tuple(sorted((left_flip, right_flip)))
        if pair not in exclusive_pairs:
            quadratic[pair] = 4 * seed_product
    return Polynomial(seed_product, linear, quadratic)


def aperiodic_polynomials(
    sign_rows: tuple[tuple[tuple[int, int | None], ...], ...],
    exclusive_pairs: set[tuple[int, int]],
) -> tuple[Polynomial, ...]:
    result = []
    for lag in range(adjacent.LONG):
        terms = []
        for row in sign_rows:
            for index in range(len(row) - lag):
                terms.append(
                    (
                        1,
                        sign_product(
                            row[index],
                            row[index + lag],
                            exclusive_pairs,
                        ),
                    )
                )
        result.append(add_polynomials(terms))
    return tuple(result)


def cyclic_equations(
    correlations: tuple[Polynomial, ...],
) -> list[tuple[str, Polynomial, int]]:
    """Return the plus and anti 42-fold norm equations."""

    result = [
        (
            "plus_0",
            add_polynomials(((1, correlations[0]), (2, correlations[42]))),
            334,
        ),
        (
            "anti_0",
            add_polynomials(((1, correlations[0]), (-2, correlations[42]))),
            334,
        ),
    ]
    for lag in range(1, 21):
        result.append(
            (
                f"plus_{lag}",
                add_polynomials(
                    (
                        (1, correlations[lag]),
                        (1, correlations[42 - lag]),
                        (1, correlations[42 + lag]),
                        (1, correlations[84 - lag]),
                    )
                ),
                0,
            )
        )
        result.append(
            (
                f"anti_{lag}",
                add_polynomials(
                    (
                        (1, correlations[lag]),
                        (-1, correlations[42 - lag]),
                        (-1, correlations[42 + lag]),
                        (1, correlations[84 - lag]),
                    )
                ),
                0,
            )
        )
    result.append(
        (
            "plus_21",
            add_polynomials(
                ((2, correlations[21]), (2, correlations[63]))
            ),
            0,
        )
    )
    return result


def evaluate_polynomial(
    polynomial: Polynomial, assignment: dict[int, int]
) -> int:
    return (
        polynomial.constant
        + sum(
            coefficient * assignment[index]
            for index, coefficient in polynomial.linear.items()
        )
        + sum(
            coefficient * assignment[left] * assignment[right]
            for (left, right), coefficient in polynomial.quadratic.items()
        )
    )


def audit_symbolic_correlations(
    case,
    states: dict[
        tuple[str, int], tuple[cp_model.IntVar, cp_model.IntVar]
    ],
    correlations: tuple[Polynomial, ...],
) -> None:
    """Replay deterministic arbitrary trit points against physical rows."""

    generator = Random(668_840 + case.index)
    cyclic = cyclic_equations(correlations)
    for _ in range(16):
        assignment: dict[int, int] = {}
        rows = cascade.q_adjusted_original_rows(case)
        for (block, cell), (lower, upper) in states.items():
            state = generator.randrange(3)
            assignment[lower.Index()] = int(state == 1)
            assignment[upper.Index()] = int(state == 2)
            if not state:
                continue
            coordinate = cell if state == 1 else cell + 42
            for row in ((0, 1) if block == "L" else (2, 3)):
                rows[row][coordinate] *= -1
        physical = tuple(tuple(row) for row in rows)
        direct_aperiodic = adjacent.base_correlations(physical)
        symbolic_aperiodic = tuple(
            evaluate_polynomial(polynomial, assignment)
            for polynomial in correlations
        )
        if symbolic_aperiodic != direct_aperiodic:
            raise AssertionError("symbolic aperiodic expansion failed replay")
        plus = adjacent.summed_periodic_correlations(
            adjacent.fold_quadruple(physical)
        )
        anti = antifold.negacyclic_norm_coefficients(
            antifold.antifold_quadruple(physical)
        )
        symbolic_cyclic = {
            name: evaluate_polynomial(polynomial, assignment)
            for name, polynomial, _ in cyclic
        }
        if any(
            symbolic_cyclic[f"plus_{lag}"] != plus[lag]
            for lag in range(22)
        ) or any(
            symbolic_cyclic[f"anti_{lag}"] != anti[lag]
            for lag in range(21)
        ):
            raise AssertionError("symbolic cyclic images failed replay")


def build_model(
    case_number: int,
    profile_number: int,
    cyclic_only: bool,
) -> tuple[
    cp_model.CpModel,
    dict[tuple[str, int], tuple[cp_model.IntVar, cp_model.IntVar]],
    dict[str, int],
]:
    case, keys, _, anti_constant, anti_linear, _ = local.arrays(
        case_number
    )
    if not 0 <= profile_number < len(case.profiles):
        raise ValueError("profile number lies outside this case")

    model = cp_model.CpModel()
    states: dict[
        tuple[str, int], tuple[cp_model.IntVar, cp_model.IntVar]
    ] = {}
    variables_by_index: dict[int, cp_model.IntVar] = {}
    exclusive_pairs: set[tuple[int, int]] = set()
    for block, cell in keys:
        lower = model.new_bool_var(f"lower_{block}_{cell}")
        upper = model.new_bool_var(f"upper_{block}_{cell}")
        model.add(lower + upper <= 1)
        states[(block, cell)] = (lower, upper)
        variables_by_index[lower.Index()] = lower
        variables_by_index[upper.Index()] = upper
        exclusive_pairs.add(tuple(sorted((lower.Index(), upper.Index()))))
    model.add(
        sum(lower + upper for lower, upper in states.values()) == 39
    )

    # The four exact root-profile equations.  The lower contribution is
    # -seed[cell] z^cell and the upper contribution is its negative.
    root_targets = cascade.root_targets(case.profiles[profile_number])
    seed = adjacent.eliahou_base()
    for block in ("L", "S"):
        seed_row = 0 if block == "L" else 2
        for root in (1, -1):
            expression = []
            for key, (lower, upper) in states.items():
                key_block, cell = key
                if key_block != block:
                    continue
                coefficient = -seed[seed_row][cell] * root**cell
                expression.append(coefficient * lower)
                expression.append(-coefficient * upper)
            model.add(
                sum(expression) == root_targets[(block, root)]
            )

    # Exact characteristic-two anti-fold shadow, exposed as XOR clauses.
    parity_one = model.new_bool_var("fixed_parity_one")
    model.add(parity_one == 1)
    for equation in range(len(anti_constant)):
        literals = []
        for variable, coefficient in enumerate(anti_linear[equation]):
            if int(coefficient) & 1:
                lower, upper = states[keys[variable]]
                literals.extend((lower, upper))
        if not (int(anti_constant[equation]) & 1):
            literals.append(parity_one)
        model.add_bool_xor(literals)

    # Map every physical sign to its adjusted seed sign and, if eligible,
    # the Boolean which flips that endpoint.
    adjusted_rows = cascade.q_adjusted_original_rows(case)
    endpoint_variables: list[list[cp_model.IntVar | None]] = [
        [None] * len(row) for row in adjusted_rows
    ]
    for (block, cell), (lower, upper) in states.items():
        for row in ((0, 1) if block == "L" else (2, 3)):
            endpoint_variables[row][cell] = lower
            endpoint_variables[row][cell + 42] = upper
    sign_rows = tuple(
        tuple(
            (
                adjusted_rows[row][coordinate],
                (
                    None
                    if endpoint_variables[row][coordinate] is None
                    else endpoint_variables[row][coordinate].Index()
                ),
            )
            for coordinate in range(len(adjusted_rows[row]))
        )
        for row in range(4)
    )
    correlations = aperiodic_polynomials(sign_rows, exclusive_pairs)
    if (
        correlations[0].constant != 334
        or correlations[0].linear
        or correlations[0].quadratic
    ):
        raise AssertionError("zero-lag energy polynomial changed")
    audit_symbolic_correlations(case, states, correlations)

    equations = cyclic_equations(correlations)
    if not cyclic_only:
        equations.extend(
            (f"aperiodic_{lag}", correlations[lag], 0)
            for lag in range(1, adjacent.LONG)
        )

    used_pairs = {
        pair
        for _, polynomial, _ in equations
        for pair in polynomial.quadratic
    }
    product_variables: dict[tuple[int, int], cp_model.IntVar] = {}
    for left, right in sorted(used_pairs):
        product = model.new_bool_var(f"product_{left}_{right}")
        model.add_multiplication_equality(
            product,
            (variables_by_index[left], variables_by_index[right]),
        )
        product_variables[(left, right)] = product

    for _, polynomial, target in equations:
        expression = polynomial.constant
        expression += sum(
            coefficient * variables_by_index[index]
            for index, coefficient in polynomial.linear.items()
        )
        expression += sum(
            coefficient * product_variables[pair]
            for pair, coefficient in polynomial.quadratic.items()
        )
        model.add(expression == target)

    validation_error = model.validate()
    if validation_error:
        raise AssertionError(f"invalid CP-SAT model: {validation_error}")
    counts = {
        "case": case_number,
        "q_index": case.index,
        "profile": profile_number,
        "state_cells": len(states),
        "primary_booleans": 2 * len(states),
        "shared_quadratic_products": len(product_variables),
        "cyclic_norm_equations": len(cyclic_equations(correlations)),
        "aperiodic_equations": 0 if cyclic_only else 83,
        "anti_mod2_xor_equations": len(anti_constant),
        "variables": len(model.proto.variables),
        "constraints": len(model.proto.constraints),
    }
    return model, states, counts


def decode_and_replay(
    case_number: int,
    profile_number: int,
    states: dict[
        tuple[str, int], tuple[cp_model.IntVar, cp_model.IntVar]
    ],
    solver: cp_model.CpSolver,
) -> dict[str, object]:
    case, _, _, _, _, _ = local.arrays(case_number)
    rows = cascade.q_adjusted_original_rows(case)
    state_record = []
    root_values = {
        ("L", 1): 0,
        ("L", -1): 0,
        ("S", 1): 0,
        ("S", -1): 0,
    }
    seed = adjacent.eliahou_base()
    for (block, cell), (lower, upper) in states.items():
        lower_value = int(solver.value(lower))
        upper_value = int(solver.value(upper))
        if lower_value + upper_value > 1:
            raise AssertionError("decoded trit is not lower/upper/none")
        if not lower_value and not upper_value:
            continue
        orientation = "lower" if lower_value else "upper"
        coordinate = cell if lower_value else cell + 42
        for row in ((0, 1) if block == "L" else (2, 3)):
            rows[row][coordinate] *= -1
        seed_row = 0 if block == "L" else 2
        orientation_sign = 1 if lower_value else -1
        for root in (1, -1):
            root_values[(block, root)] += (
                -seed[seed_row][cell]
                * root**cell
                * orientation_sign
            )
        state_record.append([block, cell, orientation])

    physical_rows = tuple(tuple(row) for row in rows)
    aperiodic = adjacent.base_correlations(physical_rows)
    plus = adjacent.summed_periodic_correlations(
        adjacent.fold_quadruple(physical_rows)
    )
    anti = antifold.negacyclic_norm_coefficients(
        antifold.antifold_quadruple(physical_rows)
    )
    targets = cascade.root_targets(case.profiles[profile_number])
    roots_valid = all(
        root_values[key] == targets[key] for key in root_values
    )
    cyclic_valid = plus == (334,) + (0,) * 41 and anti == (
        334,
    ) + (0,) * 41
    aperiodic_valid = aperiodic == (334,) + (0,) * 83
    residuals = {
        str(lag): value
        for lag, value in enumerate(aperiodic)
        if lag and value
    }
    return {
        "selected_states": state_record,
        "selected_cell_count": len(state_record),
        "root_values": {
            f"{block}_{root:+d}": root_values[(block, root)]
            for block in ("L", "S")
            for root in (1, -1)
        },
        "roots_valid": roots_valid,
        "plus_fold_valid": plus == (334,) + (0,) * 41,
        "anti_fold_valid": anti == (334,) + (0,) * 41,
        "joint_cyclic_valid": cyclic_valid,
        "aperiodic_valid": aperiodic_valid,
        "nonzero_aperiodic_residuals": residuals,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=int, default=1)
    parser.add_argument("--profile", type=int, choices=(0, 1), default=0)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--max-memory-mb", type=int, default=6000)
    parser.add_argument("--seed", type=int, default=668)
    parser.add_argument(
        "--cyclic-only",
        action="store_true",
        help=(
            "impose only plus/anti 42-fold norms; this is a necessary "
            "mod-z^84 cyclic gate, not the full aperiodic construction"
        ),
    )
    parser.add_argument("--log", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 1 <= args.case <= 20:
        raise SystemExit("this bounded diagnostic is pinned to long cases 1..20")
    if args.time_limit <= 0 or not 1 <= args.max_memory_mb <= 6000:
        raise SystemExit("require positive time and memory in 1..6000 MB")

    model, states, counts = build_model(
        args.case, args.profile, args.cyclic_only
    )
    print("model=" + json.dumps(counts, sort_keys=True), flush=True)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = 1
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    solver.parameters.random_seed = args.seed
    solver.parameters.log_search_progress = args.log
    status = solver.solve(model)
    status_name = solver.status_name(status)
    diagnostic = {
        "status": status_name,
        "wall_time_seconds": solver.wall_time,
        "branches": solver.num_branches,
        "conflicts": solver.num_conflicts,
        "cyclic_only": args.cyclic_only,
    }
    print("diagnostic=" + json.dumps(diagnostic, sort_keys=True))
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print(
            "NO CLAIM: bounded CP-SAT returned no replayable assignment; "
            "INFEASIBLE is not a proof certificate"
        )
        raise SystemExit(2 if status == cp_model.UNKNOWN else 1)

    replay = decode_and_replay(
        args.case, args.profile, states, solver
    )
    if (
        not replay["roots_valid"]
        or not replay["joint_cyclic_valid"]
        or (not args.cyclic_only and not replay["aperiodic_valid"])
    ):
        raise AssertionError("CP-SAT assignment failed exact physical replay")
    print("replay=" + json.dumps(replay, sort_keys=True))
    if replay["aperiodic_valid"]:
        print("PASS: exact BS(84,83) construction replayed")
    else:
        print(
            "CYCLIC-ONLY SURVIVOR: plus/anti folds pass, but full "
            "aperiodic equations fail"
        )


if __name__ == "__main__":
    main()
