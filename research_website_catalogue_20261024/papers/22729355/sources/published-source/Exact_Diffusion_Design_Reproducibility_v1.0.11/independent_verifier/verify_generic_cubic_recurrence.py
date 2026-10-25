#!/usr/bin/env python3
"""Standalone all-dimensional symbolic bridge for the cubic numerator.

This verifier imports no project construction helper.  With symbolic ``m``
and a formal harmonic sum ``hfrak``, it checks the printed zero-mode and
second-harmonic recurrences, reduces the interior contraction, and proves
identically that the result is ``R_m + C_m*hfrak``.  Finite matrix checks in
``verify_cubic_sign.py`` are regression evidence; this script is the generic
recurrence-to-closed-form bridge.
"""
from __future__ import annotations

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import sympy as sp


def K(m: sp.Expr, i: sp.Expr | int) -> sp.Expr:
    """Return the affine chain factor K_i=91m-181-i."""
    return 91 * m - 181 - i


def qcal(m: sp.Expr) -> sp.Expr:
    """Return the printed cubic denominator polynomial."""
    return (
        589180301 * m**3
        - 3500015940 * m**2
        + 6930529579 * m
        - 4574434500
    )


def cubic_closed_form(m: sp.Expr, hfrak: sp.Expr) -> sp.Expr:
    """Return the claimed all-dimensional numerator R_m+C_m*hfrak."""
    q = qcal(m)
    p_r = (
        68605040480814208768 * m**4
        - 550882186169626030957 * m**3
        + 1658612632937449670852 * m**2
        - 2219226476204103501323 * m
        + 1113379274975809565700
    )
    p_c = (
        652054120726848 * m**4
        - 5151971981328467 * m**3
        + 15265080924982572 * m**2
        - 20102347725659113 * m
        + 9927281930180400
    )
    r_term = p_r / (sp.Integer(286118780220) * (8 * m - 17) * q)
    c_term = (
        -sp.Integer(215)
        * p_c
        / (sp.Integer(11645046) * (8 * m - 17) * q)
    )
    return sp.factor(r_term + c_term * hfrak)


def verify_generic_cubic_recurrence() -> None:
    """Prove the recurrence reduction in the rational function field Q(m,h)."""
    m, hfrak = sp.symbols("m hfrak", integer=True, positive=True)
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

    # Anchor the generic contraction to the printed right and adjoint vectors.
    right_boundary = (
        -(2 + sp.Rational(23, 63)) * r1 - rlast - rm + 2 * rz,
        -r1 - (1 + 1 / K(m, 2)) * r2 + 2 * rm,
        r1 + 2 * rlast - (5 + sp.Rational(1, 7)) * rm + 2 * rz,
        2 * r1 + 2 * rm - (4 + sp.Rational(16, 45)) * rz,
    )
    assert all(sp.factor(value) == 0 for value in right_boundary)

    i = sp.symbols("i", integer=True)
    ri = -K(m, i) / (sp.Integer(63) * nu)
    riprev = -K(m, i - 1) / (sp.Integer(63) * nu)
    assert sp.factor(riprev - (1 + 1 / K(m, i)) * ri) == 0

    left_boundary = (
        -(2 + sp.Rational(23, 63)) * ell1 - ell2 + ellm + 2,
        -ell1 - (1 + 1 / K(m, m - 1)) * elllast + 2 * ellm,
        -ell1 + 2 * ell2 - (5 + sp.Rational(1, 7)) * ellm + 2,
        2 * ell1 + 2 * ellm - (4 + sp.Rational(16, 45)),
    )
    assert all(sp.factor(value) == 0 for value in left_boundary)
    elli = sp.Integer(78260) * nu / (sp.Integer(163) * K(m, i - 1))
    ellinext = sp.Integer(78260) * nu / (sp.Integer(163) * K(m, i))
    assert sp.factor(-(1 + 1 / K(m, i)) * elli + ellinext) == 0

    ell_r_reduced = sp.factor(
        ell1
        - sp.Rational(78260, 163 * 63) * (nu - hfrak)
        + ellm * rm
        + rz
    )
    ell_r_target = -(
        7043400 * m - 13600927 - 7043400 * hfrak
    ) / sp.Integer(924210)
    assert sp.factor(ell_r_reduced - ell_r_target) == 0

    ell_d_r_reduced = sp.factor(
        ell1 * sp.Rational(23, 63)
        - sp.Rational(78260, 163 * 63) * hfrak
        + ellm * rm * sp.Rational(1, 7)
        + rz * sp.Rational(16, 45)
    )
    ell_d_r_target = -2 * (
        1760850 * hfrak + 16559
    ) / sp.Integer(462105)
    assert sp.factor(ell_d_r_reduced - ell_d_r_target) == 0

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

    denominator4 = sp.prod(K(m, j) for j in range(-1, 3))
    tlast = sp.prod(K(m, m - 4 + j) for j in range(4)) / denominator4
    w2last = (
        tlast * (w22 + sigma * K(m, 2) / 3)
        - sigma * K(m, m - 1) / 3
    )

    def forcing_components() -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
        b1 = -2 * r1 * rlast + 2 * rz**2 - 2 * r1 * rm
        b2 = -2 * r1 * r2 + 2 * rm**2
        bm = 4 * r1 * rlast - 4 * rm**2 + 2 * rz**2 - 2 * r1 * rm
        bz = -4 * rz**2 + 4 * r1 * rm
        return tuple(-value / 4 for value in (b1, b2, bm, bz))

    b1, b2, bm, bz = forcing_components()
    zero_residuals = (
        -2 * w01 - w0last - w0m + 2 * w0z - b1,
        -w01 - w02 + 2 * w0m - b2,
        w01 + 2 * w0last - 5 * w0m + 2 * w0z - bm,
        2 * w01 + 2 * w0m - 4 * w0z - bz,
        4 * ((m - 2) * w02 - sigma * (m - 3) * (m - 2) / 2)
        + 2 * w0m
        + w0z,
    )
    assert all(sp.factor(value) == 0 for value in zero_residuals)
    assert sp.factor(
        (w02 - (i - 3) * sigma) - (w02 - (i - 2) * sigma) - sigma
    ) == 0

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
    boundary_values = sp.Matrix([w21, w22, w2m, w2z])
    assert all(
        sp.factor(value) == 0
        for value in boundary_matrix * boundary_values - rhs
    )
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

    ti = sp.prod(K(m, i - 3 + j) for j in range(4)) / denominator4
    tiprev = sp.prod(K(m, i - 4 + j) for j in range(4)) / denominator4
    wi = ti * (w22 + sigma * K(m, 2) / 3) - sigma * K(m, i) / 3
    wiprev = (
        tiprev * (w22 + sigma * K(m, 2) / 3)
        - sigma * K(m, i - 1) / 3
    )
    assert sp.factor(wiprev - (1 + 4 / K(m, i)) * wi - sigma) == 0

    # Reduce the four-factor interior sum to a polynomial plus hfrak.
    count = m - 3
    affine_origin = 91 * m - 181
    product_sum = sp.expand(
        count * (affine_origin**2 - affine_origin)
        + (-2 * affine_origin + 1) * count * (count - 1) / 2
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
        component1 = (
            -(r1 * wlast + rlast * w1)
            + 2 * rz * wz
            - (r1 * wm + rm * w1)
        )
        component2 = -(r1 * wsecond + r2 * w1) + 2 * rm * wm
        componentm = (
            2 * (r1 * wlast + rlast * w1)
            - 4 * rm * wm
            + 2 * rz * wz
            - (r1 * wm + rm * w1)
        )
        componentz = -4 * rz * wz + 2 * (r1 * wm + rm * w1)
        return sp.factor(
            ell1 * component1
            + ell2 * component2
            + interior
            + ellm * componentm
            + componentz
        )

    ell_scale = sp.Integer(78260) * nu / sp.Integer(163)
    reciprocal_tail = hfrak - 1 / K(m, 1)
    interior0 = (
        ell_scale
        * (sigma - w01 / (sp.Integer(63) * nu))
        * reciprocal_tail
    )
    contraction0 = boundary_contraction(
        w01, w02, w0last, w0m, w0z, interior0
    )

    recurrence_constant = w22 + sigma * K(m, 2) / 3
    sum_w_over_pair = (
        recurrence_constant * product_sum / denominator4
        - sigma * reciprocal_tail / 3
    )
    interior2 = ell_scale * (
        4 * sum_w_over_pair
        + (sigma - w21 / (sp.Integer(63) * nu)) * reciprocal_tail
    )
    contraction2 = boundary_contraction(
        w21, w22, w2last, w2m, w2z, interior2
    )
    independently_reduced = sp.factor(contraction0 + contraction2 / 2)
    assert sp.factor(
        independently_reduced - cubic_closed_form(m, hfrak)
    ) == 0

    # The same generic contraction supplies the scaled-family gauge term S_m.
    gauge_interior = (
        ell_scale
        * (-sp.Integer(2) / (sp.Integer(63) * nu))
        * reciprocal_tail
    )
    gauge_contraction = boundary_contraction(2, -2, -2, 0, 1, gauge_interior)
    gauge_target = -4 * (
        1760850 * hfrak - 10253
    ) / sp.Integer(462105)
    assert sp.factor(gauge_contraction - gauge_target) == 0


if __name__ == "__main__":
    verify_generic_cubic_recurrence()
    print("GENERIC_CUBIC_RECURRENCE_PASS")
