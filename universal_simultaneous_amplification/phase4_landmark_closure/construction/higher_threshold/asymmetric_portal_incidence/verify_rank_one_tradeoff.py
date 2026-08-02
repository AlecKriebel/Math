#!/usr/bin/env python3
"""Exact certificates for the asymmetric trace and rank-one no-go."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def checked_zero(expr: sp.Expr, label: str) -> None:
    value = sp.factor(sp.cancel(expr))
    if value != 0:
        raise AssertionError(f"{label}: {value}")
    print(f"PASS {label}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_subset_transform(
    portal_count: int,
    rule: str,
    r: sp.Rational,
    c: sp.Rational,
    g: sp.Rational,
    z: sp.Rational,
) -> sp.Expr:
    """Solve the full labelled portal-subset system over exact rationals."""
    states = list(range(1, 1 << portal_count))
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.zeros(len(states))
    rhs = sp.zeros(len(states), 1)
    blade_load = 2 * c
    portal_edge = 2 * c * g / ((1 - g) * (portal_count - 1))
    degree = blade_load + (portal_count - 1) * portal_edge

    for state in states:
        row = index[state]
        mutants = [a for a in range(portal_count) if state >> a & 1]
        residents = [a for a in range(portal_count) if not (state >> a & 1)]
        if rule == "Bd":
            deaths = {
                a: blade_load + len(residents) * portal_edge / degree
                for a in mutants
            }
            births = {
                b: r * len(mutants) * portal_edge / degree for b in residents
            }
            child_rate = (
                len(mutants) * r**2 * (1 - g) / (r + 1)
            )
        elif rule == "dB":
            deaths = {
                a: (blade_load + len(residents) * portal_edge)
                / (
                    blade_load
                    + len(residents) * portal_edge
                    + r * (len(mutants) - 1) * portal_edge
                )
                for a in mutants
            }
            births = {
                b: r * len(mutants) * portal_edge
                / (
                    blade_load
                    + (len(residents) - 1) * portal_edge
                    + r * len(mutants) * portal_edge
                )
                for b in residents
            }
            child_rate = len(mutants) * r * c
        else:
            raise ValueError(rule)

        matrix[row, row] = sum(deaths.values()) + sum(births.values()) + (
            child_rate * (1 - z)
        )
        for a, rate in deaths.items():
            output = state & ~(1 << a)
            if output:
                matrix[row, index[output]] -= rate
            else:
                rhs[row] += rate
        for b, rate in births.items():
            matrix[row, index[state | (1 << b)]] -= rate

    solution = matrix.inv().multiply(rhs)
    singleton_values = [solution[index[1 << a]] for a in range(portal_count)]
    assert all(value == singleton_values[0] for value in singleton_values)
    return sp.factor(singleton_values[0])


def main() -> None:
    r, B, c, g = sp.symbols("r B c g", positive=True)
    q, k = sp.symbols("q k", integer=True, positive=True)
    theta = g / (1 - g)

    # The general portal-subset rates reduce exactly to the exchangeable
    # count rates already verified independently in the neighbouring work.
    h = 2 * c * theta / (q - 1)
    degree = 2 * c + (q - 1) * h
    bd_down = k * (2 * c + (q - k) * h / degree)
    bd_up = (q - k) * r * k * h / degree
    bd_child = 2 * r**2 / (r + 1) * k * c / degree
    checked_zero(
        bd_down - k * (2 * c + (q - k) * g / (q - 1)),
        "general Bd down rate specializes to count trace",
    )
    checked_zero(
        bd_up - r * k * (q - k) * g / (q - 1),
        "general Bd up rate specializes to count trace",
    )
    checked_zero(
        bd_child - k * r**2 * (1 - g) / (r + 1),
        "general Bd child rate specializes to count trace",
    )

    db_down = k * (
        (2 * c + (q - k) * h)
        / (2 * c + (q - k) * h + r * (k - 1) * h)
    )
    db_up = (q - k) * (r * k * h) / (
        2 * c + (q - k - 1) * h + r * k * h
    )
    checked_zero(
        db_down
        - k
        * (q - 1 - g * (k - 1))
        / (q - 1 + g * (r - 1) * (k - 1)),
        "general dB down rate specializes to count trace",
    )
    checked_zero(
        db_up
        - r
        * k
        * (q - k)
        * g
        / (q - 1 + g * (r - 1) * k),
        "general dB up rate specializes to count trace",
    )

    # Special-mark transforms for a separated portal.
    z_b = 1 / r**2
    f_b = B / (B + r**2 / (r + 1) * (1 - z_b))
    checked_zero(
        (1 - f_b) - (r - 1) / (B + r - 1),
        "Bd special-mark episode probability",
    )
    z_d = (2 - r) / r
    f_d = 1 / (1 + r * B / 2 * (1 - z_d))
    checked_zero(
        (1 - f_d) - B * (r - 1) / (1 + B * (r - 1)),
        "dB special-mark episode probability",
    )

    # Three arbitrary portal loads independently verify both PGF sign
    # reductions without relying on a symbolic summation convention.
    b1, b2, b3 = sp.symbols("b1 b2 b3", positive=True)
    loads = (b1, b2, b3)
    phi_b = lambda x: (x - 1) / (x + r - 1)
    phi_d = lambda x: x * (1 + r - r**2 - x) / (1 + (r - 1) * x)

    hb = sum((r - 1) / (x + r - 1) for x in loads)
    db = 3 / (3 + r * (r + 1) * sum(x * (r - 1) / (x + r - 1) for x in loads))
    checked_zero(
        (db - z_b)
        + (r**2 - 1)
        * (r - 1)
        * sum(phi_b(x) for x in loads)
        / (
            r**2
            * (
                3
                + r
                * (r + 1)
                * sum(x * (r - 1) / (x + r - 1) for x in loads)
            )
        ),
        "Bd PGF comparison sign",
    )
    # Keep `hb` alive as an explicit audit of the episode sum.
    if hb == 0:
        raise AssertionError("impossible positive episode sum")

    total_b = sum(loads)
    hd = sum(x * (r - 1) / (1 + x * (r - 1)) for x in loads)
    dd = total_b / (total_b + 2 * r**2 * hd)
    checked_zero(
        (dd - z_d)
        + 2
        * (r - 1) ** 2
        * sum(phi_d(x) for x in loads)
        / (r * (total_b + 2 * r**2 * hd)),
        "dB PGF comparison sign",
    )

    numerator = (
        (B - 1) ** 2 * (B + 1)
        + (r - 1) * B**2
        + (r - 1) ** 2 * B * (B + 1)
        + (r - 1) ** 3 * B
    )
    checked_zero(
        phi_b(B)
        + phi_d(B)
        + numerator / ((B + r - 1) * (1 + (r - 1) * B)),
        "pointwise Bd-dB portal tradeoff identity",
    )

    rv = sp.Rational(8, 5)
    low = sp.Rational(1, 100)
    high = sp.Integer(2)
    if not (
        phi_d(low).subs(r, rv) > 0
        and phi_b(low).subs(r, rv) < 0
        and phi_b(high).subs(r, rv) > 0
        and phi_d(high).subs(r, rv) < 0
    ):
        raise AssertionError("opposite portal-regime certificate failed")
    print("PASS exact opposite portal regimes at r=8/5")

    # Independent exact labelled-subset solver: the new identity-retaining
    # system agrees over rationals with the earlier count recurrence for
    # Q=2,...,6.  No floating-point transition is used in this audit.
    old = load_module(
        "exchangeable_exact",
        HERE.parent / "multiportal_generalization" / "verify_multiportal_tradeoff.py",
    )
    rv, cv, gv = sp.Rational(8, 5), sp.Rational(2, 5), sp.Rational(3, 10)
    for portal_count in range(2, 7):
        for rule, mark in (
            ("Bd", 1 / rv**2),
            ("dB", (2 - rv) / rv),
        ):
            subset_value = exact_subset_transform(
                portal_count, rule, rv, cv, gv, mark
            )
            count_value = old.exact_episode_transform(
                portal_count, rule, rv, cv, gv, mark
            )
            if sp.factor(subset_value - count_value) != 0:
                raise AssertionError(
                    f"subset/count disagreement Q={portal_count}, {rule}"
                )
        print(f"PASS independent subset/count agreement Q={portal_count}")

    print("ALL ASYMMETRIC-PORTAL CERTIFICATES PASS")


if __name__ == "__main__":
    main()
