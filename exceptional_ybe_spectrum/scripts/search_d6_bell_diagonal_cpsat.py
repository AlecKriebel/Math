#!/usr/bin/env python3
"""Exact CP-SAT search for balanced Bell-diagonal d=6 reflections.

This is a discovery/exhaustion driver.  It expands every computational-basis
coefficient of

    H_1 H_2 H_1 - H_2 H_1 H_2 = (H_1-H_2)/3

as an integer linear combination of degree-one and square-free degree-three
monomials in the 36 signs which diagonalize H in the generalized Bell basis.
The degree-three monomials are encoded by exact Boolean parity constraints.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from ortools.sat.python import cp_model


D = 6

# 2*zeta**e = REAL2[e] + i*sqrt(3)*IMAG2[e].
REAL2 = (2, 1, -1, -2, -1, 1)
IMAG2 = (0, 1, 1, 0, -1, -1)


def sign_index(a: int, b: int) -> int:
    return (a % D) * D + (b % D)


def reduced_monomial(indices: tuple[int, int, int]) -> tuple[int, ...]:
    """Reduce a product of three signs using s_i^2=1."""

    counts = Counter(indices)
    return tuple(sorted(i for i, multiplicity in counts.items() if multiplicity & 1))


def add_phase(
    equation: dict[tuple[int, ...], list[int]],
    monomial: tuple[int, ...],
    exponent: int,
    multiplier: int,
) -> None:
    pair = equation[monomial]
    pair[0] += multiplier * REAL2[exponent % D]
    pair[1] += multiplier * IMAG2[exponent % D]


def coefficient_equation(
    a: int, c: int, p: int, r: int
) -> dict[tuple[int, ...], tuple[int, int]]:
    """Return twice the exact cyclotomic coefficient equation.

    The input basis vector is |0,a,a+c>.  The selected output is
    |r,r+a+p,r+a+p+c-r>.  Multiplication by d^3 clears the three Fourier
    denominators.  The right side then has multiplier d^2/3=12.
    """

    equation: dict[tuple[int, ...], list[int]] = defaultdict(lambda: [0, 0])

    # H_1 H_2 H_1.
    for t in range(D):
        for b1 in range(D):
            i1 = sign_index(a, b1)
            for b2 in range(D):
                i2 = sign_index(c - t, b2)
                for b3 in range(D):
                    i3 = sign_index(a + p, b3)
                    exponent = b1 * t + b2 * p + b3 * (r - t)
                    add_phase(
                        equation,
                        reduced_monomial((i1, i2, i3)),
                        exponent,
                        1,
                    )

    # -H_2 H_1 H_2.
    for u in range(D):
        for b1 in range(D):
            i1 = sign_index(c, b1)
            for b2 in range(D):
                i2 = sign_index(a + u, b2)
                for b3 in range(D):
                    i3 = sign_index(c - r, b3)
                    exponent = b1 * u + b2 * r + b3 * (p - u)
                    add_phase(
                        equation,
                        reduced_monomial((i1, i2, i3)),
                        exponent,
                        -1,
                    )

    # -(d^2/3)(delta_{p,0} H_1 - delta_{r,0} H_2).
    rhs_multiplier = D * D // 3
    if p == 0:
        for b in range(D):
            add_phase(
                equation,
                (sign_index(a, b),),
                b * r,
                -rhs_multiplier,
            )
    if r == 0:
        for b in range(D):
            add_phase(
                equation,
                (sign_index(c, b),),
                b * p,
                rhs_multiplier,
            )

    return {
        monomial: (pair[0], pair[1])
        for monomial, pair in equation.items()
        if pair != [0, 0]
    }


def build_all_equations() -> list[dict[tuple[int, ...], tuple[int, int]]]:
    equations = []
    for a in range(D):
        for c in range(D):
            for p in range(D):
                for r in range(D):
                    equation = coefficient_equation(a, c, p, r)
                    for coordinate in range(2):
                        scalar = {
                            monomial: pair[coordinate]
                            for monomial, pair in equation.items()
                            if pair[coordinate]
                        }
                        if scalar:
                            equations.append(scalar)
    return equations


def equation_digest(
    equations: list[dict[tuple[int, ...], int]]
) -> str:
    serializable = [
        [[list(monomial), coefficient] for monomial, coefficient in sorted(eq.items())]
        for eq in equations
    ]
    payload = json.dumps(serializable, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--time-limit", type=float, default=0.0)
    parser.add_argument("--log-search", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    started = time.time()
    equations = build_all_equations()

    model = cp_model.CpModel()
    negative = [model.new_bool_var(f"x_{i}") for i in range(D * D)]
    # Complement symmetry h -> -h lets us fix h_(0,0)=+1.
    model.add(negative[0] == 0)
    model.add(sum(negative) == D * D // 2)

    cubic_keys = sorted(
        {
            monomial
            for equation in equations
            for monomial in equation
            if len(monomial) == 3
        }
    )
    parity = {}
    for monomial in cubic_keys:
        y = model.new_bool_var("p_" + "_".join(map(str, monomial)))
        i, j, k = monomial
        # y = x_i xor x_j xor x_k.
        model.add_bool_xor([negative[i], negative[j], negative[k], y.Not()])
        parity[monomial] = y

    for equation in equations:
        constant = sum(equation.values())
        terms = []
        for monomial, coefficient in equation.items():
            if len(monomial) == 1:
                variable = negative[monomial[0]]
            elif len(monomial) == 3:
                variable = parity[monomial]
            else:
                raise AssertionError(monomial)
            terms.append(-2 * coefficient * variable)
        model.add(sum(terms) + constant == 0)

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 20260729
    solver.parameters.cp_model_presolve = True
    solver.parameters.log_search_progress = args.log_search
    if args.time_limit:
        solver.parameters.max_time_in_seconds = args.time_limit

    status = solver.solve(model)
    elapsed = time.time() - started
    result = {
        "d": D,
        "equation_count": len(equations),
        "equation_sha256": equation_digest(equations),
        "cubic_parity_variables": len(cubic_keys),
        "status": solver.status_name(status),
        "wall_time_seconds": elapsed,
        "branches": solver.num_branches,
        "conflicts": solver.num_conflicts,
        "python": sys.version,
        "platform": platform.platform(),
    }
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        signs = [
            -1 if solver.value(variable) else 1 for variable in negative
        ]
        result["signs"] = [signs[row * D : (row + 1) * D] for row in range(D)]

    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n")


if __name__ == "__main__":
    main()
