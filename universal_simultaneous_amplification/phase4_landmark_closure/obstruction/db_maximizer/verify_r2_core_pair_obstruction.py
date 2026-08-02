#!/usr/bin/env python3
"""Exact certificate for the r=2 clique-core/pair-satellite obstruction."""

from __future__ import annotations

from itertools import product

import sympy as sp
from flint import arb, fmpq, fmpq_mat


def verify_polynomial_certificate():
    T, x, u = sp.symbols("T x u")
    F = sp.expand(
        2 * (2 * T - 1) * (2 * T + x)
        - T * (8 * x + 1) * (2 * T - (2 * T - 1) * x)
    )
    vertex = sp.factor(-sp.Poly(F, x).coeff_monomial(x) /
                       (2 * sp.Poly(F, x).coeff_monomial(x**2)))
    assert vertex == (14 * T**2 - 3 * T + 2) / (16 * T * (2 * T - 1))
    minimum = sp.factor(F.subs(x, vertex))
    numerator = 188 * T**4 - 364 * T**3 + 63 * T**2 + 12 * T - 4
    assert minimum == numerator / (32 * T * (2 * T - 1))
    shifted = sp.Poly(sp.expand(numerator.subs(T, u + 2)), u)
    assert shifted.as_expr() == (
        188 * u**4 + 1140 * u**3 + 2391 * u**2 + 1912 * u + 368
    )
    assert all(coefficient > 0 for _, coefficient in shifted.terms())

    # General clique-satellite lemma.  All cases except m=2 and the three
    # pairs below are immediate from d_c-s_m <= 0.  Check the three remaining
    # rational quadratics independently from the definitions.
    cases = {
        (3, 3): 64 * x**2 - 7 * x + 1,
        (4, 3): 4480 * x**2 - 65 * x + 27,
        (3, 4): 3456 * x**2 - 65 * x + 35,
    }
    for (core_size, satellite_size), expected in cases.items():
        core_scale = sp.Integer(2) ** (core_size - 2)
        satellite_scale = sp.Integer(2) ** (satellite_size - 2)
        core_mass = (
            sp.Rational(core_size - 1) * core_scale
            / (2 * core_scale - 1)
        )
        satellite_mass = (
            sp.Rational(satellite_size - 1) * satellite_scale
            / (2 * satellite_scale - 1)
        )
        core_excess = core_mass / (2 * core_scale)
        satellite_slack = sp.Rational(satellite_size, 2) - satellite_mass
        difference = (
            core_mass * x / (1 + x)
            + satellite_mass
            / (1 + 16 * core_scale * satellite_scale * x)
            - core_excess
            + satellite_slack
        )
        numerator = sp.Poly(sp.cancel(difference).as_numer_denom()[0], x)
        expected_poly = sp.Poly(expected, x)
        quotient, remainder = sp.div(numerator, expected_poly)
        assert remainder.is_zero
        assert quotient.degree() == 0 and quotient.LC() > 0
        assert sp.discriminant(expected_poly.as_expr(), x) < 0

    # The monotonicity reduction used to dispose of all larger m.
    def d(size):
        scale = sp.Integer(2) ** (size - 2)
        return sp.Rational(size - 1, 2 * (2 * scale - 1))

    assert d(3) == sp.Rational(1, 3)
    assert sp.Rational(1, 2) - d(5) == sp.Rational(11, 30)
    assert sp.Rational(1, 2) - d(4) == sp.Rational(2, 7)
    assert sp.Rational(1, 2) - d(3) == sp.Rational(1, 6)
    assert d(4) == sp.Rational(3, 14)
    assert d(5) == sp.Rational(2, 15)

    # Endpoint reduction for an arbitrary satellite module satisfying the
    # two open module invariants (M1)--(M2).  This verifies only the proved
    # conditional scalar algebra, not the open invariants themselves.
    e, kappa = sp.symbols("e kappa", positive=True)
    relaxed_satellite_loss = e * (e + sp.Rational(1, 2)) / (
        e + kappa * (e + sp.Rational(1, 2))
    )
    shifted_loss = sp.factor(relaxed_satellite_loss - e)
    assert shifted_loss == -e * (2 * e * kappa + kappa - 1) / (
        2 * e * kappa + 2 * e + kappa
    )
    shifted_derivative = sp.factor(sp.diff(shifted_loss, e))
    assert shifted_derivative == (
        -kappa
        * (2 * e + 1)
        * (2 * e * kappa + 2 * e + kappa - 1)
        / (2 * e * kappa + 2 * e + kappa) ** 2
    )


def exact_close_case():
    core_size = 60
    blades = 3
    order = core_size + 2 * blades
    fitness = fmpq(2)
    core_weight = fmpq(1)
    outer = fmpq(1, 10**8)
    internal = fmpq(10**10)
    distributions = [
        (x0, x1, blades - x0 - x1)
        for x0 in range(blades + 1)
        for x1 in range(blades - x0 + 1)
    ]
    extinction = (0, blades, 0, 0)
    fixation_state = (core_size, 0, 0, blades)
    states = [
        (core, *distribution)
        for core in range(core_size + 1)
        for distribution in distributions
        if (core, *distribution) not in (extinction, fixation_state)
    ]
    index = {state: row for row, state in enumerate(states)}
    matrix = fmpq_mat(len(states), len(states))
    rhs = fmpq_mat(len(states), 1)

    for state, row in index.items():
        core, x0, x1, x2 = state
        counts = [x0, x1, x2]
        mutant_blade_vertices = x1 + 2 * x2
        resident_blade_vertices = 2 * x0 + x1
        changes = []
        if core < core_size:
            mutant_mass = core_weight * core + outer * mutant_blade_vertices
            resident_mass = (
                core_weight * (core_size - core - 1)
                + outer * resident_blade_vertices
            )
            rate = ((core_size - core) * fitness * mutant_mass /
                    (fitness * mutant_mass + resident_mass))
            if rate:
                changes.append(((core + 1, x0, x1, x2), rate))
        if core > 0:
            mutant_mass = core_weight * (core - 1) + outer * mutant_blade_vertices
            resident_mass = (
                core_weight * (core_size - core)
                + outer * resident_blade_vertices
            )
            rate = core * resident_mass / (fitness * mutant_mass + resident_mass)
            if rate:
                changes.append(((core - 1, x0, x1, x2), rate))

        for count, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            if count < 2:
                mutant_mass = internal * count + outer * core
                resident_mass = internal * (1 - count) + outer * (core_size - core)
                rate = (
                    multiplicity * (2 - count) * fitness * mutant_mass
                    / (fitness * mutant_mass + resident_mass)
                )
                if rate:
                    target_counts = counts.copy()
                    target_counts[count] -= 1
                    target_counts[count + 1] += 1
                    changes.append(((core, *target_counts), rate))
            if count > 0:
                mutant_mass = internal * (count - 1) + outer * core
                resident_mass = internal * (2 - count) + outer * (core_size - core)
                rate = (
                    multiplicity * count * resident_mass
                    / (fitness * mutant_mass + resident_mass)
                )
                if rate:
                    target_counts = counts.copy()
                    target_counts[count] -= 1
                    target_counts[count - 1] += 1
                    changes.append(((core, *target_counts), rate))

        changing = sum((rate for _, rate in changes), fmpq(0))
        matrix[row, row] = 1
        for target, rate in changes:
            probability = rate / changing
            if target == fixation_state:
                rhs[row, 0] += probability
            elif target != extinction:
                matrix[row, index[target]] -= probability

    solution = matrix.solve(rhs)
    assert matrix * solution == rhs
    core_singleton = solution[index[(1, blades, 0, 0)], 0]
    blade_singleton = solution[index[(0, blades - 1, 1, 0)], 0]
    rho = (core_size * core_singleton + 2 * blades * blade_singleton) / order
    complete = (
        fmpq(order - 1, 2 * order)
        / (1 - fmpq(2) ** (-(order - 1)))
    )
    excess = rho - complete
    assert excess < 0
    return excess


def main():
    verify_polynomial_certificate()
    excess = exact_close_case()
    print("PASS: clique and conditional arbitrary-module scale tradeoffs")
    print("PASS: exact 608-transient-state close-case solve")
    print(f"exact close-case excess is negative: {float(arb(excess)):.16g}")


if __name__ == "__main__":
    main()
