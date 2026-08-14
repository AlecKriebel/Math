#!/usr/bin/env python3
"""Exact replay of the Kac Schur derivative and endpoint-pin obstruction."""

from __future__ import annotations

import sympy as sp


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.together(expr)) == 0, sp.factor(sp.together(expr))


def full_state_schur_derivative() -> None:
    # A generic two-state killed block.  Row-sum zero fixes the root column
    # and root diagonal; no reversibility is used.
    a, b, c, d = sp.symbols("a b c d", nonzero=True)
    x, y = sp.symbols("x y")
    g0, g1, g2, theta = sp.symbols("g0 g1 g2 theta")
    dmat = sp.Matrix([[a, b], [c, d]])
    brow = sp.Matrix([[x, y]])
    one = sp.ones(2, 1)
    ccol = -dmat * one
    q00 = -(brow * one)[0]
    mark = sp.diag(g1, g2)

    schur = q00 + theta * g0 - (
        brow * (dmat + theta * mark).inv() * ccol
    )[0]
    derivative = sp.diff(schur, theta).subs(theta, 0)
    green_reward = g0 + (brow * (-dmat).inv() * sp.Matrix([g1, g2]))[0]
    assert_zero(schur.subs(theta, 0))
    assert_zero(derivative - green_reward)


def endpoint_pin_hessian_algebra() -> None:
    # The hard-pin curvature is the scalar Schur complement, reciprocal to
    # the corresponding diagonal entry of H^{-1}.
    h00, h01, h11 = sp.symbols("h00 h01 h11", nonzero=True)
    hmat = sp.Matrix([[h00, h01], [h01, h11]])
    hard_pin_curvature = h00 - h01**2 / h11
    assert_zero(hard_pin_curvature - 1 / hmat.inv()[0, 0])

    # Implicit source response H z' = e_i and envelope curvature -z_i'.
    source_response = hmat.inv() * sp.Matrix([1, 0])
    assert_zero(-source_response[0] + hmat.inv()[0, 0])


def complete_graph_reward_algebra() -> None:
    r = sp.symbols("r", positive=True)
    n = sp.symbols("n", integer=True, positive=True)
    cfit = r - 1
    p0 = cfit / r

    u = cfit / (r**n - 1)
    rho_b = cfit * r ** (n - 1) / (r**n - 1)
    v = (n - 1) * cfit / (n * (r ** (n - 1) - 1))
    rho_d = (n - 1) * cfit * r ** (n - 2) / (
        n * (r ** (n - 1) - 1)
    )
    psi_b = sp.factor((rho_b - p0) / u)
    psi_d = sp.factor((rho_d - p0) / v)
    assert_zero(psi_b - 1 / r)
    assert_zero(psi_d - (n - r ** (n - 1)) / (r * (n - 1)))
    assert_zero(
        psi_b - psi_d - (r ** (n - 1) - 1) / (r * (n - 1))
    )


def active_k2_generator_replay() -> None:
    r = sp.symbols("r", positive=True)
    cfit = r - 1
    # State order: {1}, {2}, {1,2}.  The dB doubleton is transient, while
    # Bd is recurrent on all three states.
    q_b = sp.Matrix(
        [
            [-r, 1, cfit],
            [1, -r, cfit],
            [1, 1, -2],
        ]
    )
    q_d = sp.Matrix(
        [
            [-1, 1, 0],
            [1, -1, 0],
            [1, 1, -2],
        ]
    )
    mu_b = sp.Matrix([[1 / (r + 1), 1 / (r + 1), cfit / (r + 1)]])
    mu_d = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2), 0]])
    for entry in mu_b * q_b:
        assert_zero(entry)
    for entry in mu_d * q_d:
        assert_zero(entry)
    assert_zero(sum(mu_b) - 1)
    assert_zero(sum(mu_d) - 1)

    ranks = sp.Matrix([1, 1, 2])
    rho_b = (mu_b * ranks)[0] / 2
    rho_d = (mu_d * ranks)[0] / 2
    p0 = cfit / r
    psi_b = sp.factor((rho_b - p0) / mu_b[0])
    psi_d = sp.factor((rho_d - p0) / mu_d[0])
    assert_zero(psi_b - 1 / r)
    assert_zero(psi_d - (2 - r) / r)
    assert_zero(r**3 * psi_b * psi_d - r * (2 - r))
    # The diagonal target is true here by the exact square below.
    assert_zero(1 - r * (2 - r) - (r - 1) ** 2)


def regular_endpoint_action_identity() -> None:
    r = sp.symbols("r", positive=True)
    z1, z2 = sp.symbols("z1 z2", positive=True)
    phi = lambda z: -z - sp.log(1 - z)
    # K_2 has uniform pi and P swapping the coordinates.  With a=t=1,
    # both endpoint actions are literally this same expression.
    action_b = (phi(z1) + phi(z2)) / (2 * r) - z1 * z2 / 2
    action_d = (phi(z1) + phi(z2)) / (2 * r) - z1 * z2 / 2
    assert_zero(action_b - action_d)
    p0 = (r - 1) / r
    for z in (z1, z2):
        assert_zero(sp.diff(action_b, z).subs({z1: p0, z2: p0}))
    hessian = sp.hessian(action_b, (z1, z2)).subs({z1: p0, z2: p0})
    expected = sp.Matrix([[r / 2, -sp.Rational(1, 2)],
                          [-sp.Rational(1, 2), r / 2]])
    for entry in hessian - expected:
        assert_zero(entry)


def main() -> None:
    full_state_schur_derivative()
    endpoint_pin_hessian_algebra()
    complete_graph_reward_algebra()
    active_k2_generator_replay()
    regular_endpoint_action_identity()
    print("PASS full-state root-Schur directional derivative")
    print("PASS endpoint source/hard-pin Hessian identities")
    print("PASS complete-graph signed Kac reward formulas")
    print("PASS active K2 stationary-generator replay")
    print("PASS regular Bd/dB endpoint-action identity")


if __name__ == "__main__":
    main()
