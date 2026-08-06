#!/usr/bin/env python3
"""Exact finite-grid and asymptotic drift checks for candidate Lyapunov functions."""
from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Callable, Iterable, Sequence

import sympy as sp

from .class_analyzer import linkage_classes, molecularity_profile
from .generator import Reaction, State, generator_value, propensity_factor

ExactFunction = Callable[[State], Fraction | int]


def total_linear_drift(x: State, reactions: Sequence[Reaction]) -> Fraction:
    return sum(r.propensity(x) * r.delta_molecularity for r in reactions)


def mixed_linkage_barrier(
    x: State,
    reactions: Sequence[Reaction],
    weights: Sequence[Fraction] | None = None,
) -> Fraction:
    """Candidate N + sum_L c_L(1+N)^2/(1+quadratic availability).

    This is exploratory unless accompanied by a separate exact certificate.
    """
    links = [L for L in linkage_classes(reactions) if 2 in molecularity_profile(L) and molecularity_profile(L) != frozenset({2})]
    if weights is None:
        weights = [Fraction(1) for _ in links]
    if len(weights) != len(links):
        raise ValueError("one weight per mixed linkage is required")
    n = sum(x)
    value = Fraction(n)
    for coeff, linkage in zip(weights, links):
        denominator = 1
        for y in linkage:
            if sum(y) == 2:
                denominator += propensity_factor(x, y)
        value += coeff * Fraction((n + 1) ** 2, denominator)
    return value


def grid_drift_violations(
    reactions: Sequence[Reaction],
    function: ExactFunction,
    upper: int,
    lower_norm: int = 0,
) -> list[tuple[State, Fraction]]:
    d = reactions[0].dimension if reactions else 0
    bad: list[tuple[State, Fraction]] = []
    for x in product(range(upper + 1), repeat=d):
        if sum(x) < lower_norm:
            continue
        drift = Fraction(generator_value(x, reactions, function))
        if drift >= 0:
            bad.append((x, drift))
    return bad


def symbolic_generator_polynomial(
    reactions: Sequence[Reaction], polynomial: sp.Expr
) -> sp.Expr:
    """Compute L applied to a polynomial in x_0,...,x_{d-1}."""
    if not reactions:
        return sp.Integer(0)
    d = reactions[0].dimension
    xs = sp.symbols(f"x0:{d}", integer=True, nonnegative=True)
    if polynomial.free_symbols - set(xs):
        raise ValueError("polynomial uses unexpected symbols")
    total = 0
    for r in reactions:
        propensity = sp.Rational(r.rate.numerator, r.rate.denominator)
        for xi, yi in zip(xs, r.source):
            for j in range(yi):
                propensity *= xi - j
        shifted = {xs[i]: xs[i] + r.vector[i] for i in range(d)}
        total += propensity * (polynomial.xreplace(shifted) - polynomial)
    return sp.expand(total)


def self_test() -> None:
    rs = [Reaction((0,), (1,)), Reaction((1,), (0,))]
    x = sp.symbols("x0", integer=True, nonnegative=True)
    assert symbolic_generator_polynomial(rs, x) == 1 - x
    assert total_linear_drift((3,), rs) == -2
    bad = grid_drift_violations(rs, lambda state: state[0], upper=5, lower_norm=2)
    assert bad == []


if __name__ == "__main__":
    self_test()
    print("drift_checker.py self-test: OK")
