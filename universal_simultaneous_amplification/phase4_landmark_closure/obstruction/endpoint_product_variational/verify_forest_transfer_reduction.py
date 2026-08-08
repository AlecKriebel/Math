#!/usr/bin/env python3
"""Exact audit of the electrical two-tree determinant reduction.

The universal sign of the final transfer scalar is open.  This verifier
checks every algebraic reduction on a weighted P3 over exact rationals and
confirms that the transfer scalar equals the actual stationary chord gap.
"""

from __future__ import annotations

from fractions import Fraction as F

import sympy as sp

from verify_root_marked_tree_transform import generators, stationary


def rational(value: F) -> sp.Rational:
    return sp.Rational(value.numerator, value.denominator)


def main() -> None:
    weights = (
        (0, 0, 1),
        (0, 0, 17),
        (1, 17, 0),
    )
    left_fraction, reverse_fraction = generators(weights)
    left = sp.Matrix([[rational(value) for value in row] for row in left_fraction])
    reverse = sp.Matrix(
        [[rational(value) for value in row] for row in reverse_fraction]
    )
    midpoint = (left + reverse) / 2
    defect = (left - reverse) / 2
    size = midpoint.rows
    mu = sp.Matrix(
        [sp.Rational(1, 2) ** state.bit_count() for state in range(1, size + 1)]
    )
    mu /= sum(mu)
    mass = sp.diag(*mu)
    laplacian = -mass * midpoint

    state_edges = [
        (first, second)
        for first in range(size)
        for second in range(first + 1, size)
        if midpoint[first, second]
    ]
    edge_count = len(state_edges)
    incidence = sp.zeros(size, edge_count)
    signless = sp.zeros(size, edge_count)
    conductance = []
    current = []
    for edge, (first, second) in enumerate(state_edges):
        incidence[first, edge] = 1
        incidence[second, edge] = -1
        signless[first, edge] = signless[second, edge] = 1
        conductance.append(mu[first] * midpoint[first, second])
        current.append(mu[first] * defect[first, second])
    current_matrix = sp.diag(*current)

    # H_s=D_mu(-Q_s)=H_0+s B J A^T.
    assert laplacian == incidence * sp.diag(*conductance) * incidence.T
    perturbation = signless * current_matrix * incidence.T
    assert perturbation == -mass * defect

    # Matrix determinant lemma at an interior interpolation, killing, and
    # rational root mark.
    interpolation = sp.Rational(2, 3)
    killing = sp.Rational(2, 5)
    root_mark = sp.Rational(5, 4)
    rank = sp.Matrix([state.bit_count() for state in range(1, size + 1)])
    marked_mass = sp.diag(
        *[
            mu[state - 1] * root_mark ** state.bit_count()
            for state in range(1, size + 1)
        ]
    )
    killed_midpoint = laplacian + killing * marked_mass
    killed_green = killed_midpoint.inv()
    transfer = current_matrix * incidence.T * killed_green * signless
    plus_determinant = (killed_midpoint + interpolation * perturbation).det()
    minus_determinant = (killed_midpoint - interpolation * perturbation).det()
    midpoint_determinant = killed_midpoint.det()
    assert sp.factor(
        plus_determinant * minus_determinant / midpoint_determinant**2
        - (sp.eye(edge_count) - interpolation**2 * transfer**2).det()
    ) == 0

    # The coefficient of epsilon is the root-marked tree polynomial, up to
    # the common factor product(mu).
    epsilon = sp.symbols("epsilon")
    plus_laplacian = laplacian + interpolation * perturbation
    forest_determinant = sp.Poly(
        (plus_laplacian + epsilon * marked_mass).det(method="domain-ge"),
        epsilon,
    )
    linear_coefficient = forest_determinant.coeff_monomial(epsilon)
    # Compare directly with the cofactor expansion, avoiding any imported
    # tree-theorem implementation.
    direct_cofactor_sum = sum(
        marked_mass[root, root]
        * plus_laplacian.extract(
            [index for index in range(size) if index != root],
            [index for index in range(size) if index != root],
        ).det()
        for root in range(size)
    )
    assert linear_coefficient == direct_cofactor_sum

    # Singular-killing limit.  H^# is the Euclidean group inverse because H
    # is a symmetric connected Laplacian.  The exact chord derivative is
    # 4 s^2 1^T X (I-s^2 X^2)^(-1) u.
    one_state = sp.ones(size, 1)
    projection = one_state * one_state.T / size
    green = (laplacian + projection).inv() - projection
    centered_signless = signless - 2 * mu * sp.ones(1, edge_count)
    limiting_transfer = (
        current_matrix * incidence.T * green * centered_signless
    )
    midpoint_mean = (mu.T * rank)[0]
    poisson = green * mass * (rank - midpoint_mean * one_state)
    marked_current = current_matrix * incidence.T * poisson
    resolvent = (
        sp.eye(edge_count) - interpolation**2 * limiting_transfer**2
    ).inv()
    transfer_scalar = (
        sp.ones(1, edge_count)
        * limiting_transfer
        * resolvent
        * marked_current
    )[0]
    predicted_chord = sp.factor(4 * interpolation**2 * transfer_scalar)

    def stationary_mean(sign: int) -> F:
        generator = [
            [
                (left_fraction[i][j] + reverse_fraction[i][j]) / 2
                + sign
                * F(2, 3)
                * (left_fraction[i][j] - reverse_fraction[i][j])
                / 2
                for j in range(size)
            ]
            for i in range(size)
        ]
        law = stationary(generator)
        return sum(
            (law[state - 1] * state.bit_count() for state in range(1, size + 1)),
            F(0),
        )

    actual_chord = (
        rational(stationary_mean(1) + stationary_mean(-1))
        - 2 * midpoint_mean
    )
    assert predicted_chord == actual_chord
    assert predicted_chord < 0

    print("PASS: exact conductance Laplacian and signless-incidence split")
    print("PASS: exact two-tree determinant transfer identity")
    print("PASS: exact root-marked forest coefficient identity")
    print("PASS: limiting transfer scalar equals the stationary chord gap")
    print("weighted-P3 chord:", predicted_chord)
    print("STATUS: the universal sign of the transfer scalar remains OPEN")


if __name__ == "__main__":
    main()
