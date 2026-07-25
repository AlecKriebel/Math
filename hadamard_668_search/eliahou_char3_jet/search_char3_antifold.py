#!/usr/bin/env python3
"""Solve the complete characteristic-2/3 distance-41 anti-fold relaxation.

For each orientation-free support instance, the exact anti-fold equations
are first divided by their integer content.  The resulting equations are
imposed modulo 2 and modulo 3.  The modulo-3 system is the complete
three-jet condition because

    z^42 + 1 = (z^14 + 1)^3  over F_3.

This is a necessary relaxation only.  Every SAT model is replayed from the
physical four anti-fold rows before it is reported.
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

from pysat.card import CardEnc, EncType as CardEncType  # noqa: E402
from pysat.formula import CNF, IDPool  # noqa: E402
from pysat.solvers import Solver  # noqa: E402

import search_eliahou_antifold_sat as exact  # noqa: E402
import verify_eliahou_antifold42 as antifold  # noqa: E402
from eliahou_cyclotomic_cascade import (  # noqa: E402
    verify_cyclotomic_cascade as cascade,
)


@dataclass(frozen=True)
class NormalizedEquation:
    lag: int
    coefficients: dict[int, int]
    constant: int
    content: int


def canonical_cases() -> tuple[exact.PairCase, ...]:
    """Return the 30 orientation-free cases in the cascade ordering."""

    result = []
    by_key: dict[tuple[str, int], exact.PairCase] = {
        (case.block, case.index): case for case in exact.cases()
    }
    for block, index in cascade.canonical_cases():
        result.append(by_key[(block, index)])
    if len(result) != 30:
        raise AssertionError("the canonical case count changed")
    return tuple(result)


def normalized_equations(
    cnf: CNF,
    pool: IDPool,
    case: exact.PairCase,
    variables: dict[tuple[str, int], int],
) -> tuple[NormalizedEquation, ...]:
    """Expose the twenty independent normalized anti-fold equations."""

    seed_rows = exact.seed_antifold()
    product_cache: dict[tuple[int, int], int] = {}
    equations = []
    for target_lag in range(1, exact.FOLD // 2):
        coefficients: dict[int, int] = {}
        constant = 0
        for row, left, right in product(
            range(4), range(exact.FOLD), range(exact.FOLD)
        ):
            exponent = left - right
            wrap_sign = 1
            if exponent < 0:
                exponent += exact.FOLD
                wrap_sign = -1
            if exponent != target_lag:
                continue
            left_retained = exact.retained_literal(
                row, left, case, variables, seed_rows
            )
            right_retained = exact.retained_literal(
                row, right, case, variables, seed_rows
            )
            if left_retained is None or right_retained is None:
                continue
            coefficient = (
                wrap_sign * seed_rows[row][left] * seed_rows[row][right]
            )
            term = exact.product_literal(
                cnf,
                pool,
                product_cache,
                left_retained,
                right_retained,
            )
            if term is True:
                constant += coefficient
            elif term < 0:
                constant += coefficient
                coefficients[-term] = (
                    coefficients.get(-term, 0) - coefficient
                )
            else:
                coefficients[term] = (
                    coefficients.get(term, 0) + coefficient
                )

        content = abs(constant)
        for coefficient in coefficients.values():
            content = gcd(content, abs(coefficient))
        if content == 0:
            content = 1
        equations.append(
            NormalizedEquation(
                lag=target_lag,
                coefficients={
                    variable: coefficient // content
                    for variable, coefficient in coefficients.items()
                },
                constant=constant // content,
                content=content,
            )
        )
    return tuple(equations)


def build(
    case: exact.PairCase,
    moduli: tuple[int, ...] = (2, 3),
) -> tuple[
    CNF,
    IDPool,
    dict[tuple[str, int], int],
    tuple[NormalizedEquation, ...],
]:
    pool = IDPool()
    cnf = CNF()
    variables, flat = exact.support_variables(pool, case)
    cnf.extend(
        CardEnc.equals(
            flat,
            bound=39,
            vpool=pool,
            encoding=CardEncType.totalizer,
        ).clauses
    )
    equations = normalized_equations(cnf, pool, case, variables)
    for equation in equations:
        for modulus in moduli:
            exact.add_modular_sum(
                cnf,
                pool,
                equation.coefficients,
                equation.constant,
                modulus,
                f"lag_{equation.lag}_mod{modulus}",
            )
    return cnf, pool, variables, equations


def selected_support(
    model: set[int],
    variables: dict[tuple[str, int], int],
) -> tuple[tuple[str, int], ...]:
    return tuple(
        key for key, variable in variables.items() if variable in model
    )


def replay(
    case: exact.PairCase,
    selected: tuple[tuple[str, int], ...],
    equations: tuple[NormalizedEquation, ...],
    model: set[int],
    moduli: tuple[int, ...],
) -> dict[str, object]:
    if len(selected) != 39:
        raise AssertionError("solver support has the wrong weight")
    rows = exact.direct_rows(case, set(selected))
    correlations = exact.negacyclic_correlations(rows)
    if correlations[0] != 334:
        raise AssertionError("solver support has the wrong zero-lag energy")
    for lag in range(1, exact.FOLD // 2):
        if correlations[exact.FOLD - lag] != -correlations[lag]:
            raise AssertionError("negacyclic reflection failed")

    normalized_residuals = []
    for equation in equations:
        algebraic = equation.constant + sum(
            coefficient
            for variable, coefficient in equation.coefficients.items()
            if variable in model
        )
        physical = correlations[equation.lag] // equation.content
        if equation.content * physical != correlations[equation.lag]:
            raise AssertionError("equation content does not divide replay")
        if algebraic != physical:
            raise AssertionError("CNF equation disagrees with direct replay")
        if any(algebraic % modulus for modulus in moduli):
            raise AssertionError("SAT model failed a modular equation")
        normalized_residuals.append(algebraic)
    return {
        "selected": [[block, cell] for block, cell in selected],
        "normalized_residuals": normalized_residuals,
        "full_exact": all(value == 0 for value in normalized_residuals),
        "nonzero_lags": sum(value != 0 for value in normalized_residuals),
        "l1": sum(abs(value) for value in normalized_residuals),
        "linf": max(abs(value) for value in normalized_residuals),
    }


def factorization_self_test() -> None:
    """Check the characteristic-three cyclotomic multiplicities directly."""

    # Low-first coefficients.
    phi4 = (1, 0, 1)
    phi12_mod3 = (1, 0, 2, 0, 1)
    phi28_mod3 = (1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1)
    phi84_mod3 = (
        1, 0, 1, 0, 0, 0, 2, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2,
        0, 2, 0, 0, 0, 1, 0, 1,
    )

    def multiply(left: tuple[int, ...], right: tuple[int, ...]):
        result = [0] * (len(left) + len(right) - 1)
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                result[i + j] = (result[i + j] + a * b) % 3
        return tuple(result)

    assert multiply(phi4, phi4) == phi12_mod3
    assert multiply(phi28_mod3, phi28_mod3) == phi84_mod3
    factor = multiply(phi4, phi28_mod3)
    cube = multiply(multiply(factor, factor), factor)
    expected = (1,) + (0,) * 41 + (1,)
    assert cube == expected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=30)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument(
        "--moduli",
        default="2,3",
        help="comma-separated normalized-equation moduli (default: 2,3)",
    )
    parser.add_argument(
        "--enumerate",
        type=int,
        default=1,
        help="maximum models to enumerate per case",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    factorization_self_test()
    moduli = tuple(int(value) for value in args.moduli.split(",") if value)
    if not moduli or any(value < 2 for value in moduli):
        raise ValueError("all moduli must be at least two")
    if args.enumerate < 1:
        raise ValueError("--enumerate must be positive")
    cases = canonical_cases()
    if not 0 <= args.start <= args.stop <= len(cases):
        raise ValueError("invalid case range")

    output = []
    for case_number in range(args.start, args.stop):
        case = cases[case_number]
        started = time.monotonic()
        cnf, pool, variables, equations = build(case, moduli)
        records = []
        with Solver(
            name=args.solver,
            bootstrap_with=cnf.clauses,
        ) as solver:
            while len(records) < args.enumerate and solver.solve():
                model = set(solver.get_model())
                selected = selected_support(model, variables)
                records.append(
                    replay(case, selected, equations, model, moduli)
                )
                solver.add_clause(
                    [
                        -variable if variable in model else variable
                        for variable in variables.values()
                    ]
                )
        output.append(
            {
                "case": case_number,
                "block": case.block,
                "q_index": case.index,
                "moduli": list(moduli),
                "variables": pool.top,
                "clauses": len(cnf.clauses),
                "equation_contents": [
                    equation.content for equation in equations
                ],
                "models": records,
                "status": "SAT" if records else "UNSAT",
                "seconds": time.monotonic() - started,
            }
        )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
