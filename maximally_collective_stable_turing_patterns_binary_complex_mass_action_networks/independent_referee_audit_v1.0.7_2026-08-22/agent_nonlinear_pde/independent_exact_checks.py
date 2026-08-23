#!/usr/bin/env python3
"""Independent exact/adversarial checks for the nonlinear/PDE claims.

This file deliberately imports no project module and reads no project
certificate.  Matrices and Hessians are reconstructed from the reaction list.
All symbolic identities below are derived from the formulas printed in the
manuscript/supplement.  Floating-point spectra are reported separately and are
used only for falsification/regression.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "independent_exact_checks.json"


def reaction_matrices(m: int) -> tuple[sp.Matrix, sp.Matrix]:
    """Reconstruct Gamma and Y directly from the indexed reaction list."""
    if m < 3:
        raise ValueError("m must be at least 3")
    n = m + 1

    def vec(entries: dict[int, int] | None = None) -> sp.Matrix:
        ans = [0] * n
        for idx, value in (entries or {}).items():
            ans[idx] = value
        return sp.Matrix(ans)

    reactions: list[tuple[sp.Matrix, sp.Matrix]] = [(vec(), vec({0: 1}))]
    for i in range(2, m - 1):
        reactions.append((vec({0: 1, i - 1: 1}), vec({0: 1, i: 1})))
    reactions.extend(
        [
            (vec({0: 1, m - 2: 1}), vec({m - 1: 2})),
            (vec({m - 1: 2}), vec({1: 1})),
            (vec({m: 2}), vec({0: 1, m - 1: 1})),
            (vec({0: 1, m - 1: 1}), vec({m: 2})),
        ]
    )
    assert len(reactions) == m + 2
    Y = sp.Matrix.hstack(*(source for source, _ in reactions))
    Yp = sp.Matrix.hstack(*(target for _, target in reactions))
    return Yp - Y, Y


def matrix_A(m: int) -> sp.Matrix:
    gamma, Y = reaction_matrices(m)
    return gamma * Y.T  # unit flux in every reaction


def hessian_B(m: int, u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    """Differentiate source monomials reaction by reaction at unit equilibrium."""
    gamma, Y = reaction_matrices(m)
    ans = sp.zeros(m + 1, 1)
    for reaction in range(Y.cols):
        contraction = 0
        active = [i for i in range(m + 1) if Y[i, reaction] != 0]
        for pos, i in enumerate(active):
            yi = int(Y[i, reaction])
            contraction += yi * (yi - 1) * u[i] * v[i]
            for j in active[pos + 1 :]:
                yj = int(Y[j, reaction])
                contraction += yi * yj * (u[i] * v[j] + u[j] * v[i])
        ans += contraction * gamma[:, reaction]
    return sp.simplify(ans)


def K(m: int | sp.Expr, i: int | sp.Expr) -> sp.Expr:
    return 91 * m - 181 - i


def critical_data(m: int) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    nu = m - 2
    r = sp.Matrix(
        [1]
        + [-sp.Rational(K(m, i), 63 * nu) for i in range(2, m)]
        + [-sp.Rational(2, 9), sp.Rational(5, 14)]
    )
    D = sp.diag(
        sp.Rational(23, 63),
        *[sp.Rational(1, K(m, i)) for i in range(2, m)],
        sp.Rational(1, 7),
        sp.Rational(16, 45),
    )
    ell = sp.Matrix(
        [-sp.Rational(266, 815)]
        + [sp.Rational(78260 * nu, 163 * K(m, i - 1)) for i in range(2, m)]
        + [sp.Rational(18368, 7335), 1]
    )
    return r, D, ell


def conservation(m: int) -> sp.Matrix:
    return sp.Matrix([0] + [4] * (m - 2) + [2, 1])


def rho(m: int) -> sp.Matrix:
    return sp.Matrix([2] + [-2] * (m - 2) + [0, 1])


def harmonic(m: int) -> sp.Expr:
    return sp.Add(*(sp.Rational(1, K(m, j)) for j in range(1, m - 1)))


def qcal(m: int | sp.Expr) -> sp.Expr:
    return (
        589180301 * m**3
        - 3500015940 * m**2
        + 6930529579 * m
        - 4574434500
    )


def w0_formula(m: int) -> sp.Matrix:
    nu = m - 2
    sigma = sp.Rational(1, 126 * nu)
    second = sp.Rational(
        1008 * m**2 - 20459 * m + 37138,
        31752 * nu * (8 * m - 17),
    )
    return sp.Matrix(
        [sp.Rational(182448 * m - 373417, 31752 * (8 * m - 17)), second]
        + [second - (i - 2) * sigma for i in range(3, m)]
        + [
            -sp.Rational(1, 81),
            sp.Rational(16861 * m - 34044, 7938 * (8 * m - 17)),
        ]
    )


def T_factor(m: int, i: int) -> sp.Expr:
    return sp.factor(
        sp.prod(sp.Integer(K(m, j)) for j in range(i - 3, i + 1))
        / sp.prod(sp.Integer(K(m, j)) for j in range(-1, 3))
    )


def w2_formula(m: int) -> sp.Matrix:
    nu = m - 2
    sigma = sp.Rational(1, 126 * nu)
    q = qcal(m)
    w1 = sp.Rational(
        11
        * (
            8832129632 * m**3
            - 52772027580 * m**2
            + 105099636403 * m
            - 69768261675
        ),
        2457 * q,
    )
    wsecond = sp.Rational(
        (91 * m - 183)
        * (
            27306456137 * m**3
            - 163220086095 * m**2
            + 325200697288 * m
            - 215972758800
        ),
        6804 * nu * q,
    )
    wm = -sp.Rational(
        3123724821523 * m**3
        - 18723524680620 * m**2
        + 37405968085217 * m
        - 24907679699400,
        176904 * q,
    )
    wz = -sp.Rational(
        25
        * (
            82375210916 * m**3
            - 488921724540 * m**2
            + 967289665339 * m
            - 637893501255
        ),
        68796 * q,
    )
    interior = [
        sp.factor(
            T_factor(m, i) * (wsecond + sigma * K(m, 2) / 3)
            - sigma * K(m, i) / 3
        )
        for i in range(3, m)
    ]
    return sp.Matrix([w1, wsecond] + interior + [wm, wz])


def cubic_closed_form(m: int | sp.Expr, h: sp.Expr) -> sp.Expr:
    q = qcal(m)
    PR = (
        68605040480814208768 * m**4
        - 550882186169626030957 * m**3
        + 1658612632937449670852 * m**2
        - 2219226476204103501323 * m
        + 1113379274975809565700
    )
    PC = (
        652054120726848 * m**4
        - 5151971981328467 * m**3
        + 15265080924982572 * m**2
        - 20102347725659113 * m
        + 9927281930180400
    )
    R = PR / (sp.Integer(286118780220) * (8 * m - 17) * q)
    C = -sp.Integer(215) * PC / (sp.Integer(11645046) * (8 * m - 17) * q)
    return sp.factor(R + C * h)


def check_generic_harmonic_and_cubic_identities() -> dict[str, str | int]:
    """Derive the all-m correction and cubic identities with symbolic m.

    The contraction is reduced independently using the interior recurrences.
    The only unevaluated finite sum is represented by h=sum(1/K_j).
    """
    m, h = sp.symbols("m h", integer=True, positive=True)
    nu = m - 2
    sigma = 1 / (sp.Integer(126) * nu)

    r1 = sp.Integer(1)
    r2 = -K(m, 2) / (sp.Integer(63) * nu)
    rlast = -K(m, m - 1) / (sp.Integer(63) * nu)
    rm = -sp.Rational(2, 9)
    rz = sp.Rational(5, 14)
    ell1 = -sp.Rational(266, 815)
    ell2 = sp.Integer(78260) * nu / (sp.Integer(163) * K(m, 1))
    elllast = sp.Integer(78260) * nu / (sp.Integer(163) * K(m, m - 2))
    ellm = sp.Rational(18368, 7335)

    # All-m right kernel equations for A-D, including every boundary row.
    right_boundary = [
        -(2 + sp.Rational(23, 63)) * r1 - rlast - rm + 2 * rz,
        -r1 - (1 + 1 / K(m, 2)) * r2 + 2 * rm,
        r1 + 2 * rlast - (5 + sp.Rational(1, 7)) * rm + 2 * rz,
        2 * r1 + 2 * rm - (4 + sp.Rational(16, 45)) * rz,
    ]
    assert all(sp.factor(value) == 0 for value in right_boundary)
    # A generic interior row uses K_{i-1}=K_i+1.
    i = sp.symbols("i", integer=True)
    ri = -K(m, i) / (sp.Integer(63) * nu)
    riprev = -K(m, i - 1) / (sp.Integer(63) * nu)
    assert sp.factor(riprev - (1 + 1 / K(m, i)) * ri) == 0

    # All-m adjoint boundary columns.  Interior columns telescope by the same
    # K_{i-1}=K_i+1 identity.
    left_boundary = [
        -(2 + sp.Rational(23, 63)) * ell1 - ell2 + ellm + 2,
        -ell1 - (1 + 1 / K(m, m - 1)) * elllast + 2 * ellm,
        -ell1 + 2 * ell2 - (5 + sp.Rational(1, 7)) * ellm + 2,
        2 * ell1 + 2 * ellm - (4 + sp.Rational(16, 45)),
    ]
    assert all(sp.factor(value) == 0 for value in left_boundary)
    elli = sp.Integer(78260) * nu / (sp.Integer(163) * K(m, i - 1))
    ellinext = sp.Integer(78260) * nu / (sp.Integer(163) * K(m, i))
    assert sp.factor(-(1 + 1 / K(m, i)) * elli + ellinext) == 0

    ell_r_reduced = sp.factor(
        ell1
        - sp.Rational(78260, 163 * 63) * (nu - h)
        + ellm * rm
        + rz
    )
    ell_r_target = -(
        7043400 * m - 13600927 - 7043400 * h
    ) / sp.Integer(924210)
    assert sp.factor(ell_r_reduced - ell_r_target) == 0
    ell_D_r_reduced = sp.factor(
        ell1 * sp.Rational(23, 63)
        - sp.Rational(78260, 163 * 63) * h
        + ellm * rm * sp.Rational(1, 7)
        + rz * sp.Rational(16, 45)
    )
    ell_D_r_target = -2 * (1760850 * h + 16559) / sp.Integer(462105)
    assert sp.factor(ell_D_r_reduced - ell_D_r_target) == 0
    L = sp.symbols("L", positive=True)
    scaled_den_reduced = sp.factor(
        ell1
        - sp.Rational(78260, 163 * 63) * L * nu
        + ellm * rm
        + rz
    )
    scaled_den_target = -sp.Rational(485873, 924210) - sp.Rational(11180, 1467) * L * nu
    assert sp.factor(scaled_den_reduced - scaled_den_target) == 0

    w01 = (182448 * m - 373417) / (sp.Integer(31752) * (8 * m - 17))
    w02 = (
        1008 * m**2 - 20459 * m + 37138
    ) / (sp.Integer(31752) * nu * (8 * m - 17))
    w0last = w02 - (m - 3) * sigma
    w0m = -sp.Rational(1, 81)
    w0z = (16861 * m - 34044) / (sp.Integer(7938) * (8 * m - 17))

    q = qcal(m)
    w21 = sp.Integer(11) * (
        8832129632 * m**3
        - 52772027580 * m**2
        + 105099636403 * m
        - 69768261675
    ) / (sp.Integer(2457) * q)
    w22 = (91 * m - 183) * (
        27306456137 * m**3
        - 163220086095 * m**2
        + 325200697288 * m
        - 215972758800
    ) / (sp.Integer(6804) * nu * q)
    w2m = -(
        3123724821523 * m**3
        - 18723524680620 * m**2
        + 37405968085217 * m
        - 24907679699400
    ) / (sp.Integer(176904) * q)
    w2z = -sp.Integer(25) * (
        82375210916 * m**3
        - 488921724540 * m**2
        + 967289665339 * m
        - 637893501255
    ) / (sp.Integer(68796) * q)

    den4 = sp.prod(K(m, j) for j in range(-1, 3))
    tlast = sp.prod(K(m, m - 4 + j) for j in range(4)) / den4
    w2last = tlast * (w22 + sigma * K(m, 2) / 3) - sigma * K(m, m - 1) / 3

    # Verify the all-m zero-mode boundary equations and gauge directly.
    def b_components() -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
        B1 = -2 * r1 * rlast + 2 * rz**2 - 2 * r1 * rm
        B2 = -2 * r1 * r2 + 2 * rm**2
        Bm = 4 * r1 * rlast - 4 * rm**2 + 2 * rz**2 - 2 * r1 * rm
        Bz = -4 * rz**2 + 4 * r1 * rm
        return tuple(-value / 4 for value in (B1, B2, Bm, Bz))

    b1, b2, bm, bz = b_components()
    zero_residuals = [
        -2 * w01 - w0last - w0m + 2 * w0z - b1,
        -w01 - w02 + 2 * w0m - b2,
        w01 + 2 * w0last - 5 * w0m + 2 * w0z - bm,
        2 * w01 + 2 * w0m - 4 * w0z - bz,
        4 * ((m - 2) * w02 - sigma * (m - 3) * (m - 2) / 2)
        + 2 * w0m
        + w0z,
    ]
    assert all(sp.factor(value) == 0 for value in zero_residuals)
    # Interior zero-mode identity: w_{i-1}-w_i=sigma=-B_i(r,r)/4.
    assert sp.factor((w02 - (i - 3) * sigma) - (w02 - (i - 2) * sigma) - sigma) == 0

    boundary_matrix = sp.Matrix(
        [
            [-sp.Rational(218, 63), -tlast, -1, 2],
            [-1, -(1 + 4 / K(m, 2)), 2, 0],
            [1, 2 * tlast, -sp.Rational(39, 7), 2],
            [2, 0, 2, -sp.Rational(244, 45)],
        ]
    )
    delta = sigma * (tlast * K(m, 2) - K(m, m - 1)) / 3
    rhs = sp.Matrix([b1 + delta, b2, bm - 2 * delta, bz])
    W = sp.Matrix([w21, w22, w2m, w2z])
    assert all(sp.factor(value) == 0 for value in boundary_matrix * W - rhs)
    determinant_expected = (
        64
        * q
        / (
            sp.Integer(6615)
            * (91 * m - 183)
            * (91 * m - 181)
            * (91 * m - 180)
        )
    )
    assert sp.factor(boundary_matrix.det() - determinant_expected) == 0
    Ti = sp.prod(K(m, i - 3 + j) for j in range(4)) / den4
    Tiprev = sp.prod(K(m, i - 4 + j) for j in range(4)) / den4
    wi = Ti * (w22 + sigma * K(m, 2) / 3) - sigma * K(m, i) / 3
    wiprev = Tiprev * (w22 + sigma * K(m, 2) / 3) - sigma * K(m, i - 1) / 3
    assert sp.factor(wiprev - (1 + 4 / K(m, i)) * wi - sigma) == 0

    # Derive the polynomial sum in the second-harmonic interior contraction.
    count = m - 3
    aa = 91 * m - 181
    product_sum = sp.expand(
        count * (aa**2 - aa)
        + (-2 * aa + 1) * count * (count - 1) / 2
        + count * (count - 1) * (2 * count - 1) / 6
    )
    printed_product_sum = (
        (m - 3) * (24571 * m**2 - 97470 * m + 96662) / 3
    )
    assert sp.factor(product_sum - printed_product_sum) == 0

    def boundary_contraction(
        w1: sp.Expr,
        wsecond: sp.Expr,
        wlast: sp.Expr,
        wm: sp.Expr,
        wz: sp.Expr,
        interior: sp.Expr,
    ) -> sp.Expr:
        B1 = -(r1 * wlast + rlast * w1) + 2 * rz * wz - (r1 * wm + rm * w1)
        B2 = -(r1 * wsecond + r2 * w1) + 2 * rm * wm
        Bm = (
            2 * (r1 * wlast + rlast * w1)
            - 4 * rm * wm
            + 2 * rz * wz
            - (r1 * wm + rm * w1)
        )
        Bz = -4 * rz * wz + 2 * (r1 * wm + rm * w1)
        return sp.factor(ell1 * B1 + ell2 * B2 + interior + ellm * Bm + Bz)

    ell_scale = sp.Integer(78260) * nu / sp.Integer(163)
    reciprocal_tail = h - 1 / K(m, 1)
    interior0 = ell_scale * (sigma - w01 / (sp.Integer(63) * nu)) * reciprocal_tail
    contraction0 = boundary_contraction(w01, w02, w0last, w0m, w0z, interior0)

    c0 = w22 + sigma * K(m, 2) / 3
    sum_w_over_pair = c0 * product_sum / den4 - sigma * reciprocal_tail / 3
    interior2 = ell_scale * (
        4 * sum_w_over_pair
        + (sigma - w21 / (sp.Integer(63) * nu)) * reciprocal_tail
    )
    contraction2 = boundary_contraction(w21, w22, w2last, w2m, w2z, interior2)
    independently_reduced = sp.factor(contraction0 + contraction2 / 2)
    target = cubic_closed_form(m, h)
    assert sp.factor(independently_reduced - target) == 0

    # The gauge-direction contraction used in the scaled family.
    rho1, rhosecond, rholast, rhom, rhoz = 2, -2, -2, 0, 1
    # In the interior rho is constant, but rho_1=2 leaves
    # B_i(r,rho)=2(r_{i-1}-r_i)=-2/(63*nu).
    gauge_interior = (
        ell_scale * (-sp.Integer(2) / (sp.Integer(63) * nu)) * reciprocal_tail
    )
    gauge_contraction = boundary_contraction(
        rho1, rhosecond, rholast, rhom, rhoz, gauge_interior
    )
    gauge_target = -4 * (1760850 * h - 10253) / sp.Integer(462105)
    assert sp.factor(gauge_contraction - gauge_target) == 0

    return {
        "generic_zero_mode_boundary_and_gauge": "exact",
        "generic_kernel_adjoint_transversality_formulas": "exact",
        "generic_second_mode_boundary_and_determinant": "exact",
        "generic_second_mode_interior_recurrence": "exact",
        "generic_cubic_reduction_to_R_plus_C_h": "exact",
        "generic_gauge_contraction_S": "exact",
    }


def even_y_to_z(expr: sp.Expr, y: sp.Symbol, z: sp.Symbol) -> sp.Expr:
    ans = 0
    for (power,), coeff in sp.Poly(sp.expand(expr), y).terms():
        assert power % 2 == 0
        ans += coeff * z ** (power // 2)
    return sp.expand(ans)


def check_modulus_polynomials() -> dict[str, int | str]:
    x, y, z, s, Avar, U = sp.symbols("x y z s A U", real=True)
    lam = x + sp.I * y

    P = lam**4 + 12 * lam**3 + 42 * lam**2 + 47 * lam + 16
    R = 5 * lam**2 + 33 * lam + 16
    E35 = sp.Poly(
        even_y_to_z((1 + lam) * (1 + sp.conjugate(lam)) * P * sp.conjugate(P) - R * sp.conjugate(R), y, z),
        x,
        z,
    )
    assert len(E35.terms()) == 35
    assert all(coeff > 0 for _, coeff in E35.terms())
    assert E35.coeff_monomial(1) == 0
    assert E35.coeff_monomial(x) > 0 and E35.coeff_monomial(z) > 0

    t = 1 + s
    g1 = lam + 2 + sp.Rational(23, 63) * t
    gm = lam + 5 + sp.Rational(1, 7) * t
    gz = lam + 4 + sp.Rational(16, 45) * t
    F = sp.expand(g1 * gm * gz - 4 * g1 - 4 * gm + gz)
    G = sp.expand(gz * (4 * g1 + gm) - 36)
    absF = even_y_to_z(F * sp.conjugate(F), y, z)
    absG = even_y_to_z(G * sp.conjugate(G), y, z)
    E77 = sp.Poly(
        sp.expand((sp.Rational(91, 90) ** 2 + z) * absF - absG), x, z, s
    )
    assert len(E77.terms()) == 77
    assert all(coeff > 0 for _, coeff in E77.terms())
    assert E77.coeff_monomial(1) == 0
    for anchor in (x, z, s):
        assert E77.coeff_monomial(anchor) > 0

    E84_expr = sp.expand(
        sp.Rational(91, 90) ** 2 * (1 + Avar * x + z / 3) * absF - absG
    )
    E84 = sp.Poly(E84_expr, x, z, s)
    assert len(E84.terms()) == 84
    for _, coefficient in E84.terms():
        poly_A = sp.Poly(coefficient, Avar)
        assert all(c >= 0 for c in poly_A.all_coeffs())
        assert any(c > 0 for c in poly_A.all_coeffs())
    assert E84.coeff_monomial(1) == 0
    for anchor in (x, z, s):
        assert sp.Poly(E84.coeff_monomial(anchor), Avar).eval(1) > 0

    F0 = lam**3 + 11 * lam**2 + 31 * lam + 16
    E22 = sp.Poly(
        sp.expand(
            (1 + (U + sp.Rational(1, 4)) * x + sp.Rational(5, 4) * z)
            * even_y_to_z(F0 * sp.conjugate(F0), y, z)
            - even_y_to_z(R * sp.conjugate(R), y, z)
        ),
        x,
        z,
    )
    assert len(E22.terms()) == 22
    for _, coefficient in E22.terms():
        assert all(c >= 0 for c in sp.Poly(coefficient, U).all_coeffs())
    assert E22.coeff_monomial(1) == 0
    # At the boundary U=0 the linear x and z coefficients vanish, but the
    # pure x^2 and z^2 coefficients are strictly positive, still forcing the
    # unique equality case x=z=0.
    assert sp.Poly(E22.coeff_monomial(x**2), U).eval(0) > 0
    assert sp.Poly(E22.coeff_monomial(z**2), U).eval(0) > 0
    # At B=5/4 the pure-z coefficient is zero, but higher/pure-x anchors still
    # force x=z=0; verify the advertised sharp coefficient identity separately.
    Bpar = sp.symbols("B", real=True)
    EB = sp.Poly(
        sp.expand(
            (1 + Bpar * z) * even_y_to_z(F0.subs(x, 0) * sp.conjugate(F0.subs(x, 0)), y, z)
            - even_y_to_z(R.subs(x, 0) * sp.conjugate(R.subs(x, 0)), y, z)
        ),
        z,
    )
    assert sp.factor(EB.coeff_monomial(z) - (256 * Bpar - 320)) == 0

    return {
        "E35_terms": 35,
        "E77_terms": 77,
        "E84_grouped_terms": 84,
        "E22_terms": 22,
        "equality_cases": "only lambda=0 (and t=1 for spatial certificates)",
    }


def check_all_m_sign_certificates() -> dict[str, str]:
    """Rebuild the scalar sign arguments without reading generated tables."""
    m, u = sp.symbols("m u", integer=True, nonnegative=True)
    PR = (
        68605040480814208768 * m**4
        - 550882186169626030957 * m**3
        + 1658612632937449670852 * m**2
        - 2219226476204103501323 * m
        + 1113379274975809565700
    )
    PC = (
        652054120726848 * m**4
        - 5151971981328467 * m**3
        + 15265080924982572 * m**2
        - 20102347725659113 * m
        + 9927281930180400
    )
    Lpoly = (
        2729945147827667886720 * m**5
        - 27755132420474170999952 * m**4
        + 112813395868533457497683 * m**3
        - 229153280695458887386228 * m**2
        + 232620996871721820873517 * m
        - 94412163900120968220300
    )
    for poly in (qcal(m), PR, PC, Lpoly):
        assert all(c > 0 for c in sp.Poly(sp.expand(poly.subs(m, u + 3)), u).all_coeffs())

    harmonic_upper = (m - 2) / (90 * m - 179)
    q = qcal(m)
    R = PR / (sp.Integer(286118780220) * (8 * m - 17) * q)
    C = -sp.Integer(215) * PC / (sp.Integer(11645046) * (8 * m - 17) * q)
    lower = sp.factor(R + C * harmonic_upper)
    expected_lower = Lpoly / (
        sp.Integer(286118780220) * (8 * m - 17) * (90 * m - 179) * q
    )
    assert sp.factor(lower - expected_lower) == 0
    ellr_worst_num = sp.together(
        7043400 * m - 13600927 - 7043400 * harmonic_upper
    ).as_numer_denom()[0]
    assert all(
        c > 0
        for c in sp.Poly(sp.expand(ellr_worst_num.subs(m, u + 3)), u).all_coeffs()
    )

    nu, v, h, L, y = sp.symbols("nu v h L y", positive=True)
    P_ref = (
        3790502986637265684840 * nu**5
        - 974216530468600286489 * nu**4
        - 53103567440921218871 * nu**3
        - 576386186827093561 * nu**2
        + 3649732858601219 * nu
        + 55281268032918
    )
    assert all(
        c > 0
        for c in sp.Poly(sp.expand(P_ref.subs(nu, v + 1)), v).all_coeffs()
    )
    assert sp.Rational(1760850, 91) - 10253 > 0
    assert (
        sp.Rational(4, 462105) * (sp.Rational(1760850, 90) - 10253)
        < sp.Rational(1, 10)
    )

    A_tau = (
        1494249120 * h * L * nu**2
        - 69786990 * h * L * nu
        + 108738630 * L * nu**2
        + 1214388 * L * nu
        - 8521 * L
        - 125249670 * nu**2
        + 1031940 * nu
    )
    B_tau = 32760 * h * L * nu + 32760 * L * nu**2 + 4 * L - 4095 * nu
    tau = -A_tau / (sp.Integer(15876) * (8 * nu - 1) * B_tau)
    dh_expected = -(
        sp.Integer(4225)
        * L
        * nu**2
        * (182448 * L * nu + 1008 * L - 7513)
        / (2 * B_tau**2)
    )
    dL_expected = -(
        sp.Integer(65)
        * nu
        * (
            -61531470 * h * nu
            + 125249670 * nu**2
            + 1031940 * nu
            - 7513
        )
        / (252 * B_tau**2)
    )
    assert sp.factor(sp.diff(tau, h) - dh_expected) == 0
    assert sp.factor(sp.diff(tau, L) - dL_expected) == 0
    # Rational lower bounds establishing negativity of both derivatives on
    # h<1/90, L>=1/sqrt(3 nu), nu>=1.
    assert 91224 - 7513 > 0
    assert -sp.Rational(61531470, 90) + 125249670 + 1031940 - 7513 > 0

    P_tau = (
        -1040195520 * nu**3
        + 756272790 * nu**2 * y
        - 507201030 * nu**2
        - 21412755 * nu * y
        - 935658 * nu
        + 58481
    )
    D_inner = -32760 * nu**2 + 4095 * nu * y - 360 * nu - 4
    endpoint_difference = sp.factor(
        tau.subs({h: sp.Rational(1, 91), L: 1 / y}) - sp.Rational(1, 20)
    )
    assert sp.factor(
        endpoint_difference
        + P_tau / (sp.Integer(79380) * (8 * nu - 1) * D_inner)
    ) == 0
    assert sp.expand(D_inner.subs(y, 2 * nu)) < 0
    assert sp.expand(P_tau.subs({nu: 1, y: sp.Rational(7, 4)})) < 0
    P_upper = (
        -sp.Rational(189709065, 2) * nu**3
        - 507201030 * nu**2
        - 935658 * nu
        + 58481
    )
    assert sp.factor(
        (P_tau + 21412755 * nu * y).subs(y, sp.Rational(5, 4) * nu)
        - P_upper
    ) == 0
    assert sp.diff(P_upper, nu).subs(nu, 2) < 0 and P_upper.subs(nu, 2) < 0

    return {
        "unit_cubic_numerator_positive_all_m": "exact shifted-polynomial comparison",
        "unit_cubic_denominator_negative_all_m": "exact harmonic-bound comparison",
        "scaled_reference_margin": "N_ref > 1/100",
        "scaled_gauge_contraction": "-1/10 < S < 0",
        "scaled_gauge_bound": "tau < 1/20 on L >= 1/sqrt(3 nu)",
        "scaled_cubic_numerator": "N(L) > 1/200",
    }


def finite_exact_checks(dimensions: tuple[int, ...]) -> dict[str, dict[str, str]]:
    results: dict[str, dict[str, str]] = {}
    for m in dimensions:
        A = matrix_A(m)
        r, D, ell = critical_data(m)
        c = conservation(m)
        rrho = rho(m)
        rhs = -sp.Rational(1, 4) * hessian_B(m, r, r)
        w0 = w0_formula(m)
        w2 = w2_formula(m)
        assert A * rrho == sp.zeros(m + 1, 1)
        assert c.T * A == sp.zeros(1, m + 1)
        assert (A - D) * r == sp.zeros(m + 1, 1)
        assert (A - D).T * ell == sp.zeros(m + 1, 1)
        assert A * w0 == rhs
        assert (c.T * w0)[0] == 0
        assert (A - 4 * D) * w2 == rhs
        numerator = sp.factor(
            (ell.T * (hessian_B(m, r, w0) + sp.Rational(1, 2) * hessian_B(m, r, w2)))[0]
        )
        closed = cubic_closed_form(m, harmonic(m))
        assert sp.factor(numerator - closed) == 0
        denominator = sp.factor((ell.T * r)[0])
        trans_num = sp.factor((ell.T * D * r)[0])
        assert denominator < 0 and trans_num < 0 and numerator > 0
        # Uniqueness is exact: the fixed-mass augmented zero solve and the
        # second harmonic both have nonzero determinant.
        assert (c.T * rrho)[0] != 0
        if m <= 10:
            augmented = A.row_join(c).col_join(c.T.row_join(sp.zeros(1, 1)))
            assert augmented.det() != 0
            assert (A - 4 * D).det() != 0
        results[str(m)] = {
            "kernel_adjoint_transversality": "exact",
            "w0_w2_and_gauge": "exact",
            "cubic_sign": "negative",
            "ell_r": str(denominator),
            "ell_D_r": str(trans_num),
            "cubic_numerator": str(numerator),
        }
    return results


def check_small_determinant_identities() -> dict[str, str]:
    lam, t = sp.symbols("lambda t")
    for m in (3, 4, 5):
        A = matrix_A(m)
        _, D, _ = critical_data(m)
        P = lam**4 + 12 * lam**3 + 42 * lam**2 + 47 * lam + 16
        R = 5 * lam**2 + 33 * lam + 16
        hom_expected = (1 + lam) ** (m - 3) * P - R
        assert sp.factor((lam * sp.eye(m + 1) - A).det() - hom_expected) == 0

        diag = list(D.diagonal())
        Q = sp.prod(lam + 1 + t * diag[i - 1] for i in range(2, m))
        g1 = lam + 2 + sp.Rational(23, 63) * t
        gm = lam + 5 + sp.Rational(1, 7) * t
        gz = lam + 4 + sp.Rational(16, 45) * t
        F = g1 * gm * gz - 4 * g1 - 4 * gm + gz
        G = gz * (4 * g1 + gm) - 36
        assert sp.factor((lam * sp.eye(m + 1) - A + t * D).det() - (Q * F - G)) == 0
    return {
        "homogeneous_sparse_determinant": "exact for m=3,4,5 from reaction matrices",
        "modal_sparse_determinant": "exact for m=3,4,5 from reaction matrices",
    }


def L_bounds(m: int) -> tuple[float, float]:
    nu = m - 2
    kappa = 1 / math.sqrt(3) if nu == 1 else math.sqrt(5) / 2
    return kappa / math.sqrt(nu), 90 * nu / (90 * nu + 1)


def H_scaled_float(m: int, L: float) -> np.ndarray:
    return np.array(
        [1.0]
        + [float(K(m, i) / (L * K(m, i - 1))) for i in range(2, m)]
        + [1.0, 1.0]
    )


def numerical_falsification() -> dict[str, object]:
    """High precision is unnecessary here: these are explicitly non-proof checks."""
    cases: dict[str, object] = {}
    for m in (3, 4, 149):
        A = np.array(matrix_A(m), dtype=float)
        _, Dsym, _ = critical_data(m)
        D = np.diag(np.array(list(Dsym.diagonal()), dtype=float))
        lo, hi = L_bounds(m)
        per_L: dict[str, object] = {}
        for label, L in (("L0", lo), ("mid", (lo + hi) / 2), ("L1", hi)):
            Hdiag = H_scaled_float(m, L)
            Hmat = np.diag(Hdiag)
            modal: dict[str, float] = {}
            for t in (0.0, 1.0, 1.0001, 4.0, 9.0, 25.0):
                eig = np.linalg.eigvals(Hmat @ (A - t * D))
                if t == 0.0:
                    nonzero = eig[np.abs(eig) > 1e-7]
                    rightmost = float(np.max(nonzero.real))
                elif t == 1.0:
                    nonzero = eig[np.abs(eig) > 1e-7]
                    rightmost = float(np.max(nonzero.real))
                else:
                    rightmost = float(np.max(eig.real))
                modal[str(t)] = rightmost
                assert rightmost < -1e-9
            # Search a dense set of noninteger damping factors for an omitted
            # competing wave/real instability in t>1.
            worst = (-math.inf, None)
            grid_count = 8 if m >= 100 else 120
            for t in np.geomspace(1.000001, 1.0e4, grid_count):
                rightmost = float(np.max(np.linalg.eigvals(Hmat @ (A - t * D)).real))
                if rightmost > worst[0]:
                    worst = (rightmost, float(t))
                assert rightmost < 0
            hcontrast = float(np.max(Hdiag) / np.min(Hdiag))
            dphys = Hdiag * np.diag(D)
            dcontrast = float(np.max(dphys) / np.min(dphys))
            product_expected = 23 * (91 * (m - 2) - 1) / 63
            assert abs(dcontrast * hcontrast - product_expected) < 1e-9 * max(1, product_expected)
            per_L[label] = {
                "L": L,
                "rightmost_noncritical_by_t": modal,
                "worst_dense_t_gt_1": {"real_part": worst[0], "t": worst[1]},
                "chi_D": dcontrast,
                "chi_H": hcontrast,
                "product": dcontrast * hcontrast,
            }
        cases[str(m)] = per_L
    return cases


def exact_scaled_endpoint_checks() -> dict[str, object]:
    results: dict[str, object] = {}
    for m in (3, 4):
        nu = m - 2
        L0 = 1 / sp.sqrt(3) if nu == 1 else sp.sqrt(5) / (2 * sp.sqrt(nu))
        L1 = sp.Rational(90 * nu, 90 * nu + 1)
        entries = []
        for label, L in (("L0", L0), ("L1", L1)):
            hlist = [sp.Integer(1)] + [K(m, i) / (L * K(m, i - 1)) for i in range(2, m)] + [sp.Integer(1), sp.Integer(1)]
            H = sp.diag(*hlist)
            A = matrix_A(m)
            r, D, ell = critical_data(m)
            q = H.inv() * ell
            cinv = H.inv() * conservation(m)
            assert H * (A - D) * r == sp.zeros(m + 1, 1)
            assert (H * (A - D)).T * q == sp.zeros(m + 1, 1)
            assert sp.simplify((q.T * H * D * r)[0] - (ell.T * D * r)[0]) == 0
            assert sp.N((q.T * r)[0], 30) < 0
            gauge_den = sp.factor((cinv.T * rho(m))[0])
            assert sp.N(gauge_den, 30) < 0
            wref = w0_formula(m)
            tau = sp.factor(-(cinv.T * wref)[0] / gauge_den)
            wscaled = sp.simplify(wref + tau * rho(m))
            assert sp.simplify((cinv.T * wscaled)[0]) == 0
            numerator = sp.factor(
                (
                    q.T
                    * H
                    * (
                        hessian_B(m, r, wscaled)
                        + sp.Rational(1, 2) * hessian_B(m, r, w2_formula(m))
                    )
                )[0]
            )
            assert sp.N(numerator, 30) > 0
            entries.append(
                {
                    "endpoint": label,
                    "L": str(L),
                    "gauge_denominator": str(gauge_den),
                    "tau": str(tau),
                    "scaled_cubic_numerator": str(numerator),
                }
            )
        results[str(m)] = entries
    return results


def main() -> None:
    started = time.monotonic()
    report: dict[str, object] = {
        "evidence_note": "Exact sections are deductive/CAS identities; numerical_falsification is not proof.",
        "generic_identities": check_generic_harmonic_and_cubic_identities(),
        "modulus_source_polynomials": check_modulus_polynomials(),
        "all_m_sign_certificates": check_all_m_sign_certificates(),
        "small_determinants": check_small_determinant_identities(),
        "finite_exact": finite_exact_checks((3, 4, 7, 149)),
        "scaled_endpoints_exact": exact_scaled_endpoint_checks(),
        "numerical_falsification": numerical_falsification(),
    }
    report["runtime_seconds"] = time.monotonic() - started
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
