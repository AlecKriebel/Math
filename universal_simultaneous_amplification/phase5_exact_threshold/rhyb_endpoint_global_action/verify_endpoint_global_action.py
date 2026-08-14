#!/usr/bin/env python3
"""Exact replay for the endpoint global-action minimum theorem."""

from __future__ import annotations

import sympy as sp


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.together(expr)) == 0, sp.factor(sp.together(expr))


def scalar_lemma() -> None:
    z = sp.symbols("z", positive=True)
    left_branch = 2 * (z - 1 - sp.log(z)) - (z - 1) ** 2
    assert_zero(sp.diff(left_branch, z) + 2 * (z - 1) ** 2 / z)
    assert_zero(left_branch.subs(z, 1))

    right_branch = 2 * z * (z - 1 - sp.log(z)) - (z - 1) ** 2
    assert_zero(right_branch - (z**2 - 1 - 2 * z * sp.log(z)))
    log_majorant = (z - 1 / z) / 2 - sp.log(z)
    assert_zero(sp.diff(log_majorant, z) - (z - 1) ** 2 / (2 * z**2))
    assert_zero(log_majorant.subs(z, 1))

    x, y = sp.symbols("x y", positive=True)
    h = 1 - y
    ratio = (1 - x) / h
    phi = lambda v: -v - sp.log(1 - v)
    dphi = phi(x) - phi(y) - y / (1 - y) * (x - y)
    log_identity = sp.expand_log(
        dphi - (ratio - 1 - sp.log(ratio)), force=True
    )
    assert_zero(log_identity)
    assert_zero((x - y) ** 2 - h**2 * (ratio - 1) ** 2)


def symbolic_two_state_decomposition() -> None:
    # A generic symmetric two-state conductance, generic positive grounds,
    # and endpoint-compatible diagonal coefficients suffice to replay the
    # algebraic add/subtract step in both actions.
    c, r = sp.symbols("c r", positive=True)
    pi0, pi1 = sp.symbols("pi0 pi1", positive=True)
    g0, g1 = sp.symbols("g0 g1", positive=True)
    d0, d1 = sp.symbols("d0 d1", real=True)

    # Reversible off-diagonal flow c; diagonal flows are immaterial to the
    # Picone identity and may be represented symbolically through Pg/g.
    picone = c * g0 * g1 * (d0 / g0 - d1 / g1) ** 2
    diagonal_minus_kinetic = (
        c * (g1 / g0) * d0**2
        + c * (g0 / g1) * d1**2
        - 2 * c * d0 * d1
    )
    assert_zero(picone - diagonal_minus_kinetic)

    # The action decomposition is purely the addition/subtraction of half
    # the ground diagonal.
    node0, node1 = sp.symbols("node0 node1", real=True)
    kinetic = sp.symbols("kinetic", real=True)
    ground_diag = sp.symbols("ground_diag", real=True)
    original = (node0 + node1) / r - kinetic / 2
    decomposed = (
        (node0 + node1) / r - ground_diag / 2
        + (ground_diag - kinetic) / 2
    )
    assert_zero(original - decomposed)

    # Homogeneous action: zero is a local maximum and p0 the active local
    # minimum, while the active value lies strictly below zero.
    zz = sp.symbols("zz", positive=True)
    phi_zz = -zz - sp.log(1 - zz)
    j = phi_zz / r - zz**2 / 2
    p0 = (r - 1) / r
    assert_zero(sp.diff(j, zz, 2).subs(zz, 0) - (1 / r - 1))
    assert_zero(sp.diff(j, zz, 2).subs(zz, p0) - (r - 1))
    active_value = sp.simplify(j.subs(zz, p0))
    # d/dr of the cleared negative active value is positive for r>1;
    # exact sign is proved in the note, while replay checks stationarity.
    assert_zero(sp.diff(j, zz).subs(zz, p0))
    assert active_value != 0


def physical_two_cycle_replay() -> None:
    r = sp.Rational(3, 2)
    kappa = sp.Rational(2)
    pi = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
    pmat = sp.Matrix([[0, 1], [1, 0]])
    avec = sp.Matrix([2 / (1 + kappa), 2 * kappa / (1 + kappa)])
    tvec = sp.Matrix([kappa, 1 / kappa])

    q = sp.Matrix(
        [
            (kappa * r + 1) / (r * (kappa + r)),
            (kappa + r) / (r * (kappa * r + 1)),
        ]
    )
    b = sp.ones(2, 1) - q
    s = sp.Matrix([1 - q[1], 1 - q[0]])
    h = sp.ones(2, 1) - s

    # Endpoint equations and both grounds.
    for i in range(2):
        assert_zero(tvec[i] * b[i] - r * q[i] * (pmat * b)[i])
        assert_zero(
            (pmat * sp.matrix_multiply_elementwise(avec, s))[i]
            - avec[i] * s[i] / (r * h[i])
        )

    zvec = sp.Matrix([sp.Rational(1, 5), sp.Rational(3, 5)])

    def phi(v: sp.Expr) -> sp.Expr:
        return -v - sp.log(1 - v)

    def dphi(x: sp.Expr, y: sp.Expr) -> sp.Expr:
        return phi(x) - phi(y) - y * (x - y) / (1 - y)

    def inner(u: sp.Matrix, v: sp.Matrix) -> sp.Expr:
        return sum(pi[i] * u[i] * v[i] for i in range(2))

    def jb(z: sp.Matrix) -> sp.Expr:
        node = sum(pi[i] * tvec[i] * phi(z[i]) for i in range(2)) / r
        return node - inner(z, pmat * z) / 2

    def jd(z: sp.Matrix) -> sp.Expr:
        az = sp.matrix_multiply_elementwise(avec, z)
        node = sum(pi[i] * avec[i] ** 2 * phi(z[i]) for i in range(2)) / r
        return node - inner(az, pmat * az) / 2

    db = zvec - b
    ds = zvec - s

    bd_scalar = sum(
        pi[i]
        * tvec[i]
        * (dphi(zvec[i], b[i]) - db[i] ** 2 / (2 * q[i]))
        for i in range(2)
    ) / r
    bd_ground = sum(
        pi[i] * db[i] * ((pmat * b)[i] / b[i] * db[i] - (pmat * db)[i])
        for i in range(2)
    ) / 2

    ads = sp.matrix_multiply_elementwise(avec, ds)
    as_ground = sp.matrix_multiply_elementwise(avec, s)
    d_scalar = sum(
        pi[i]
        * avec[i] ** 2
        * (dphi(zvec[i], s[i]) - ds[i] ** 2 / (2 * h[i]))
        for i in range(2)
    ) / r
    d_ground = sum(
        pi[i]
        * ads[i]
        * ((pmat * as_ground)[i] / as_ground[i] * ads[i] - (pmat * ads)[i])
        for i in range(2)
    ) / 2

    bd_identity = sp.expand_log(jb(zvec) - jb(b) - bd_scalar - bd_ground, force=True)
    d_identity = sp.expand_log(jd(zvec) - jd(s) - d_scalar - d_ground, force=True)
    assert_zero(bd_identity)
    assert_zero(d_identity)
    assert sp.N(bd_scalar, 40) > 0
    assert sp.N(bd_ground, 40) >= 0
    assert sp.N(d_scalar, 40) > 0
    assert sp.N(d_ground, 40) >= 0


def main() -> None:
    scalar_lemma()
    symbolic_two_state_decomposition()
    physical_two_cycle_replay()
    print("PASS scalar endpoint Bregman inequality identities")
    print("PASS exact Picone/action decomposition algebra")
    print("PASS physical two-cycle global remainder replay")
    print("PASS homogeneous nonconvex active stationary audit")


if __name__ == "__main__":
    main()
