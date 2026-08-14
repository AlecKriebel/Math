#!/usr/bin/env python3
"""Exact replay of the mixed-cofactor feedback reduction.

This script verifies determinant identities and a scoped proof-route
obstruction.  It performs no graph enumeration and does not assert the
open physical Kac inequality.
"""

from __future__ import annotations

import itertools

import sympy as sp


def cofactor_vector(laplacian: sp.Matrix) -> sp.Matrix:
    """Return the diagonal cofactor column of a rank-one Laplacian."""

    return sp.Matrix(
        [laplacian.minor_submatrix(i, i).det() for i in range(laplacian.rows)]
    )


def poisson_data(
    generator: sp.Matrix, reward: sp.Matrix, root: int
) -> tuple[sp.Matrix, list[int], sp.Matrix, sp.Matrix, sp.Expr, sp.Expr, sp.Expr]:
    """Return L, R, killed block, Poisson column, residue, cofactor, tree mark."""

    laplacian = -generator
    rest = [index for index in range(generator.rows) if index != root]
    killed = laplacian.extract(rest, rest)
    reward_rest = reward.extract(rest, [0])
    killed_solution = killed.inv() * reward_rest
    poisson = sp.zeros(generator.rows, 1)
    for index, value in zip(rest, killed_solution):
        poisson[index] = value
    root_row = laplacian.extract([root], rest)
    residue = sp.factor(reward[root] - (root_row * killed_solution)[0])
    root_cofactor = sp.factor(killed.det())
    cofactors = cofactor_vector(laplacian)
    tree_mark = sp.factor((cofactors.T * reward)[0])
    return (
        laplacian,
        rest,
        killed,
        poisson,
        residue,
        root_cofactor,
        tree_mark,
    )


def one_rule_gauge_audit(
    generator: sp.Matrix, reward: sp.Matrix, root: int
) -> tuple[sp.Matrix, list[int], sp.Matrix, sp.Matrix, sp.Expr, sp.Expr, sp.Expr]:
    """Verify the determinant-one rank-one Poisson gauge exactly."""

    data = poisson_data(generator, reward, root)
    laplacian, _, _, poisson, residue, root_cofactor, tree_mark = data
    basis = sp.zeros(generator.rows, 1)
    basis[root] = 1
    gauge = sp.eye(generator.rows) - poisson * basis.T

    assert poisson[root] == 0
    assert gauge.det() == 1
    assert reward - laplacian * poisson == residue * basis
    assert (
        (laplacian + reward * basis.T) * gauge
        == laplacian + residue * basis * basis.T
    )
    assert sp.factor((laplacian + reward * basis.T).det() - tree_mark) == 0
    assert sp.factor(tree_mark - root_cofactor * residue) == 0

    t = sp.symbols("t")
    diagonal_pencil = laplacian + t * sp.diag(*list(reward))
    derivative = sp.diff(diagonal_pencil.det(), t).subs(t, 0)
    assert sp.factor(derivative - tree_mark) == 0
    return data


def bordered_feedback_audit() -> None:
    """Verify the exact two-rule bordered determinant and M-matrix reduction."""

    generator_b = sp.Matrix(
        [
            [-3, 1, 2, 0],
            [2, -5, 1, 2],
            [1, 2, -4, 1],
            [3, 0, 1, -4],
        ]
    )
    generator_d = sp.Matrix(
        [
            [-4, 1, 3],
            [2, -5, 3],
            [1, 4, -5],
        ]
    )
    reward_b = sp.Matrix(
        [-sp.Rational(1, 100), sp.Rational(1, 4), sp.Rational(2, 5), sp.Rational(1, 2)]
    )
    # The scale makes the illustrative feedback matrix a strict M-matrix.
    # No physical inequality is inferred from this arbitrary exact instance.
    reward_d = sp.Matrix(
        [-sp.Rational(1, 1000), sp.Rational(1, 30), sp.Rational(1, 20)]
    )
    root = 0
    data_b = one_rule_gauge_audit(generator_b, reward_b, root)
    data_d = one_rule_gauge_audit(generator_d, reward_d, root)
    lap_b, rest_b, killed_b, poisson_b, kappa_b, tau_b, tree_b = data_b
    lap_d, rest_d, killed_d, poisson_d, kappa_d, tau_d, tree_d = data_d
    assert kappa_b > 0 and kappa_d > 0

    q = sp.Rational(27, 8)
    nb = len(rest_b)
    nd = len(rest_d)
    size = nb + nd + 2
    a_index = nb + nd
    b_index = a_index + 1
    master = sp.zeros(size)
    master[:nb, :nb] = killed_b
    master[nb : nb + nd, nb : nb + nd] = killed_d
    master[:nb, b_index] = q * reward_b.extract(rest_b, [0])
    master[nb : nb + nd, a_index] = reward_d.extract(rest_d, [0])
    master[a_index, :nb] = lap_b.extract([root], rest_b)
    master[b_index, nb : nb + nd] = lap_d.extract([root], rest_d)
    master[a_index, a_index] = 1
    master[a_index, b_index] = q * reward_b[root]
    master[b_index, a_index] = reward_d[root]
    master[b_index, b_index] = 1

    claimed_gap = tau_b * tau_d - q * tree_b * tree_d
    assert sp.factor(master.det() - claimed_gap) == 0
    assert sp.factor(
        master.det() - tau_b * tau_d * (1 - q * kappa_b * kappa_d)
    ) == 0

    # Perform both determinant-one Poisson column operations explicitly.
    column_gauge = sp.eye(size)
    for local, state in enumerate(rest_b):
        column_gauge[local, b_index] = -q * poisson_b[state]
    for local, state in enumerate(rest_d):
        column_gauge[nb + local, a_index] = -poisson_d[state]
    assert column_gauge.det() == 1
    gauged = master * column_gauge
    expected = sp.zeros(size)
    expected[:nb, :nb] = killed_b
    expected[nb : nb + nd, nb : nb + nd] = killed_d
    expected[a_index, :nb] = lap_b.extract([root], rest_b)
    expected[b_index, nb : nb + nd] = lap_d.extract([root], rest_d)
    expected[a_index, a_index] = 1
    expected[a_index, b_index] = q * kappa_b
    expected[b_index, a_index] = kappa_d
    expected[b_index, b_index] = 1
    assert gauged == expected

    # Sign the D block and its feedback vertex.  The result is a Z-matrix.
    signs = [1] * nb + [-1] * nd + [1, -1]
    signature = sp.diag(*signs)
    z_matrix = signature * gauged * signature
    for row, column in itertools.product(range(size), repeat=2):
        if row != column:
            assert z_matrix[row, column] <= 0

    feedback = z_matrix.extract([a_index, b_index], [a_index, b_index])
    assert feedback == sp.Matrix([[1, -q * kappa_b], [-kappa_d, 1]])
    assert sp.factor(feedback.det() - (1 - q * kappa_b * kappa_d)) == 0
    assert feedback.det() > 0
    assert all(entry >= 0 for entry in z_matrix.inv())

    # Scaling the second reward crosses the feedback threshold while leaving
    # the two killed M-matrix blocks unchanged.  Generic block M-matrix facts
    # therefore cannot supply the missing physical gain bound.
    bad_feedback = sp.Matrix([[1, -q * kappa_b], [-10 * kappa_d, 1]])
    assert bad_feedback.det() < 0


def higher_coefficient_obstruction_audit() -> None:
    """Verify that Poisson gauge preserves only the first diagonal coefficient."""

    r, t = sp.symbols("r t", positive=True)
    laplacian = sp.Matrix([[1, -1], [-1, 1]])
    g_singleton = (3 - 2 * r) / (3 * r)
    g_doubleton = (3 - r) / (3 * r)
    reward = sp.Matrix([g_singleton, g_doubleton])
    kappa = sp.factor(g_singleton + g_doubleton)
    gauged_reward = sp.Matrix([kappa, 0])

    original = sp.factor((laplacian + t * sp.diag(*list(reward))).det())
    gauged = sp.factor((laplacian + t * sp.diag(*list(gauged_reward))).det())
    assert sp.factor(original - (t * kappa + t**2 * g_singleton * g_doubleton)) == 0
    assert sp.factor(gauged - t * kappa) == 0
    assert sp.factor(sp.diff(original, t).subs(t, 0) - sp.diff(gauged, t).subs(t, 0)) == 0
    assert sp.factor(sp.diff(original - gauged, t, 2) - 2 * g_singleton * g_doubleton) == 0

    diagnostic_r = sp.Rational(151, 100)
    assert g_singleton.subs(r, diagnostic_r) < 0
    assert g_doubleton.subs(r, diagnostic_r) > 0
    assert kappa.subs(r, diagnostic_r) > 0


def main() -> None:
    bordered_feedback_audit()
    higher_coefficient_obstruction_audit()
    print("PASS: determinant-one rank-one Poisson gauge")
    print("PASS: exact bordered mixed-cofactor gap")
    print("PASS: active feedback Z/M-matrix equivalence")
    print("PASS: higher diagonal coefficients are not gauge invariant")
    print("OPEN: physical cross-rule feedback gain bound")


if __name__ == "__main__":
    main()
