"""Explicit quartic invariants separating the theta pair under K2P/K3P."""

from __future__ import annotations

from typing import Mapping, Sequence, Tuple

import sympy as sp


Assignment = Tuple[int, int, int, int]
InvariantTerm = Tuple[int, Tuple[Assignment, ...]]


# The normalized coordinate q_(0,0,0,0)=1 is written explicitly in the first
# four monomials so that every relation is homogeneous of coordinate degree 4.
K2P_THETA_SOURCE_INVARIANT: Tuple[InvariantTerm, ...] = (
    (-1, ((0, 0, 0, 0), (0, 0, 1, 1), (1, 2, 0, 3), (2, 3, 2, 3))),
    (+1, ((0, 0, 0, 0), (0, 0, 2, 2), (1, 2, 1, 2), (2, 3, 0, 1))),
    (+1, ((0, 0, 0, 0), (0, 2, 1, 3), (1, 0, 0, 1), (2, 3, 2, 3))),
    (-1, ((0, 0, 0, 0), (0, 2, 3, 1), (1, 2, 1, 2), (2, 0, 0, 2))),
    (+1, ((0, 0, 1, 1), (0, 2, 0, 2), (1, 2, 0, 3), (2, 0, 2, 0))),
    (-1, ((0, 0, 2, 2), (0, 2, 0, 2), (1, 0, 1, 0), (2, 3, 0, 1))),
    (-1, ((0, 2, 0, 2), (0, 2, 1, 3), (1, 0, 0, 1), (2, 0, 2, 0))),
    (+1, ((0, 2, 0, 2), (0, 2, 3, 1), (1, 0, 1, 0), (2, 0, 0, 2))),
)


K3P_THETA_SOURCE_INVARIANT: Tuple[InvariantTerm, ...] = (
    (-1, ((0, 0, 0, 0), (0, 0, 1, 1), (1, 2, 0, 3), (3, 2, 3, 2))),
    (+1, ((0, 0, 0, 0), (0, 0, 3, 3), (1, 2, 1, 2), (3, 2, 0, 1))),
    (+1, ((0, 0, 0, 0), (0, 2, 1, 3), (1, 0, 0, 1), (3, 2, 3, 2))),
    (-1, ((0, 0, 0, 0), (0, 2, 3, 1), (1, 2, 1, 2), (3, 0, 0, 3))),
    (+1, ((0, 0, 1, 1), (0, 2, 0, 2), (1, 2, 0, 3), (3, 0, 3, 0))),
    (-1, ((0, 0, 3, 3), (0, 2, 0, 2), (1, 0, 1, 0), (3, 2, 0, 1))),
    (-1, ((0, 2, 0, 2), (0, 2, 1, 3), (1, 0, 0, 1), (3, 0, 3, 0))),
    (+1, ((0, 2, 0, 2), (0, 2, 3, 1), (1, 0, 1, 0), (3, 0, 0, 3))),
)


def evaluate_invariant(
    coordinates: Mapping[Assignment, sp.Expr], terms: Sequence[InvariantTerm]
) -> sp.Expr:
    result = sp.Integer(0)
    for coefficient, factors in terms:
        result += coefficient * sp.prod(coordinates[g] for g in factors)
    return sp.factor(result)

