#!/usr/bin/env python3
"""Exact counterexample to a statewise batching-superharmonicity route.

For the declared positive symmetric K4 weights at r=3/2, this script builds
the forward reversed-arrow biased-link generator C, solves its fixation
committor F_C exactly, and proves that the dB generator has positive drift at
one state.  It also reconstructs F_C as the coverage function of the exact
stationary C dual.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


SOURCE = Path(__file__).parents[1] / "verify_exact_duals.py"
SPEC = importlib.util.spec_from_file_location("exact_duals", SOURCE)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

R = sp.Rational(3, 2)
WEIGHTS = [
    [0, 7, 3, 17],
    [7, 0, 15, 6],
    [3, 15, 0, 5],
    [17, 6, 5, 0],
]


def row_kernel() -> list[list[sp.Rational]]:
    return [
        [sp.Rational(value, sum(row)) for value in row]
        for row in WEIGHTS
    ]


def link_generator(p: list[list[sp.Rational]]) -> sp.Matrix:
    """Forward generator dual to the reversed-arrow set process C."""
    n = len(p)
    full = (1 << n) - 1
    generator = sp.zeros(full + 1, full + 1)
    for state in range(full + 1):
        for target in range(n):
            mutant_mass = sum(
                p[target][source]
                for source in range(n)
                if (state >> source) & 1
            )
            if (state >> target) & 1:
                rate = 1 - mutant_mass
                new_state = state & ~(1 << target)
            else:
                rate = R * mutant_mass
                new_state = state | (1 << target)
            if new_state != state and rate:
                generator[state, new_state] += rate
        generator[state, state] = -sum(generator.row(state))
    return generator


def committor(generator: sp.Matrix) -> list[sp.Expr]:
    full = generator.rows - 1
    transient = list(range(1, full))
    matrix = generator.extract(transient, transient)
    rhs = -generator.extract(transient, [full])
    solution = list(matrix.inv() * rhs)
    return [sp.Integer(0), *map(sp.cancel, solution), sp.Integer(1)]


def db_drift(
    p: list[list[sp.Rational]], values: list[sp.Expr], state: int
) -> sp.Expr:
    drift = 0
    for target in range(len(p)):
        mutant_mass = sum(
            p[target][source]
            for source in range(len(p))
            if (state >> source) & 1
        )
        denominator = 1 + (R - 1) * mutant_mass
        if (state >> target) & 1:
            rate = (1 - mutant_mass) / denominator
            new_state = state & ~(1 << target)
        else:
            rate = R * mutant_mass / denominator
            new_state = state | (1 << target)
        drift += rate * (values[new_state] - values[state])
    return sp.factor(drift)


def main() -> None:
    p = row_kernel()
    c_forward = link_generator(p)
    values = committor(c_forward)

    for state in range(1, 15):
        residual = sum(
            c_forward[state, new_state] * values[new_state]
            for new_state in range(16)
        )
        assert sp.cancel(residual) == 0

    c_dual = MOD.reversed_arrow_generator(WEIGHTS, R)
    invariant = MOD.stationary(c_dual)
    for state in range(16):
        coverage = sum(
            invariant[dual_state - 1]
            for dual_state in range(1, 16)
            if dual_state & state
        )
        assert sp.cancel(values[state] - coverage) == 0

    # Mask 0b0110 is the mutant set {1,2} in zero-based indexing.
    witness_state = 0b0110
    witness = db_drift(p, values, witness_state)
    assert witness == sp.Rational(
        19320943980314880741118267311163716984393,
        1350751487384526329949760252671364412445376,
    )
    assert witness > 0

    print("PASS exact C-harmonicity and stationary-dual coverage identity")
    print("PASS exact counterexample: D F_C(0b0110) =", witness, "> 0")


if __name__ == "__main__":
    main()
