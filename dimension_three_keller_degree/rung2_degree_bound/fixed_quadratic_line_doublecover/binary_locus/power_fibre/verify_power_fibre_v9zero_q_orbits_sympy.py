#!/usr/bin/env python3
"""Exact exclusion of the ell=q and ell=p+q v9=0 power-fibre orbits."""

from __future__ import annotations

import sympy as sp

import explore_power_fibre_v9zero as D


if not __debug__:
    raise RuntimeError("assertions must remain enabled")

p, q, r = D.p, D.q, D.r
c, u, v, x, l = D.c, D.u, D.v, D.x, D.l


def coefficient(degree: int, r_power: int, substitutions) -> sp.Expr:
    return sp.factor(
        sp.Poly(D.E[degree].as_expr(), r)
        .coeff_monomial(r**r_power)
        .subs(substitutions)
    )


def exact_zero(value) -> bool:
    numerator = sp.together(value).as_numer_denom()[0]
    return sp.Poly(sp.expand(numerator), p, q, r).is_zero


def assert_same(left, right) -> None:
    assert sp.factor(sp.together(left - right)) == 0


def run_orbit(ell_p: int) -> None:
    """ell_p=0 is ell=q; ell_p=1 is ell=p+q."""

    orbit = {
        v[9]: 0,
        v[7]: ell_p,
        v[8]: 1,
        D.tt: 0,
    }

    # E5[r^3] forces tq=0 and aa=2tp^2/9.
    e5_r3 = coefficient(5, 3, orbit)
    if ell_p == 0:
        expected_e5_r3 = -sp.Rational(2, 3) * (
            p**2 * (9 * D.aa - 2 * D.tp**2) + 2 * q**2 * D.tq**2
        )
    else:
        expected_e5_r3 = -sp.Rational(2, 3) * (
            p**2
            * (9 * D.aa - 2 * D.tp**2 + 4 * D.tp * D.tq)
            + 4 * p * q * D.tq**2
            + 2 * q**2 * D.tq**2
        )
    assert_same(e5_r3, expected_e5_r3)

    top = {
        **orbit,
        D.tq: 0,
        D.aa: sp.Rational(2, 9) * D.tp**2,
        u[1]: sp.Rational(4, 3) * c[1],
        u[2]: sp.Rational(4, 3) * c[2],
        u[3]: 0,
    }
    assert exact_zero(coefficient(6, 1, top))
    assert exact_zero(coefficient(5, 3, top))

    # E6[r^0] first fixes ap, aq and gives c2*tp=0.
    e6_r0 = sp.Poly(coefficient(6, 0, top), p, q)
    assert_same(
        e6_r0.coeff_monomial(p**5 * q),
        sp.Rational(2, 3)
        * (
            -9 * D.ap
            - 8 * c[0] * D.tp
            + 12 * l[8]
            + 9 * D.tp * u[0]
        ),
    )
    assert_same(
        e6_r0.coeff_monomial(p**4 * q**2),
        sp.Rational(2, 3) * (-9 * D.aq + 4 * c[1] * D.tp),
    )
    assert_same(
        e6_r0.coeff_monomial(p**3 * q**3),
        sp.Rational(8, 3) * c[2] * D.tp,
    )

    e6_solution = {
        **top,
        D.ap: (12 * l[8] + D.tp * (9 * u[0] - 8 * c[0])) / 9,
        D.aq: sp.Rational(4, 9) * c[1] * D.tp,
    }
    # After these E6 relations, E5[r^2] contains -8*tp^3/9.
    e5_r2 = sp.Poly(coefficient(5, 2, e6_solution), p, q)
    assert_same(
        e5_r2.coeff_monomial(p**2 * q),
        -sp.Rational(8, 9) * D.tp**3
        - sp.Rational(16, 3) * ell_p * c[2] * D.tp,
    )
    # Together with c2*tp=0, this forces tp=0.

    before_c2 = {
        **orbit,
        D.tq: 0,
        D.tp: 0,
        D.aa: 0,
        u[1]: sp.Rational(4, 3) * c[1],
        u[2]: sp.Rational(4, 3) * c[2],
        u[3]: 0,
        D.ap: sp.Rational(4, 3) * l[8],
        D.aq: 0,
    }
    e5_r1_pre = sp.Poly(coefficient(5, 1, before_c2), p, q)
    assert_same(
        e5_r1_pre.coeff_monomial(q**4),
        -sp.Rational(16, 3) * c[2] ** 2,
    )

    lower_top = {
        **before_c2,
        c[2]: 0,
        u[2]: 0,
    }
    through_e5_r1 = {
        **lower_top,
        x[1]: (
            sp.Rational(4, 3) * l[7]
            - c[1] * (8 * c[0] - 9 * u[0]) / 9
        ),
        x[2]: sp.Rational(2, 9) * c[1] ** 2,
    }
    assert exact_zero(coefficient(5, 1, through_e5_r1))

    e5_r0 = coefficient(5, 0, through_e5_r1)
    assert sp.expand(
        e5_r0
        - sp.Rational(2, 3)
        * p**3
        * q
        * (
            p * (-8 * c[0] * l[8] - 9 * l[2] + 9 * l[8] * u[0])
            + 4 * c[1] * l[8] * q
        )
    ) == 0

    # E4 forces c1=0 independently of the c1*l33 split in E5.
    e4_r1_pre = sp.Poly(coefficient(4, 1, through_e5_r1), p, q)
    assert_same(
        e4_r1_pre.coeff_monomial(q**3),
        sp.Rational(8, 9) * c[1] ** 3,
    )

    c1_zero = {
        **lower_top,
        c[1]: 0,
        u[1]: 0,
        x[1]: sp.Rational(4, 3) * l[7],
        x[2]: 0,
        l[2]: l[8] * (u[0] - sp.Rational(8, 9) * c[0]),
    }
    assert exact_zero(coefficient(5, 0, c1_zero))

    e4_r1 = sp.Poly(coefficient(4, 1, c1_zero), p, q)
    base_relation = -8 * c[0] * l[7] - 9 * l[1] + 9 * l[7] * u[0]

    if ell_p == 1:
        assert_same(
            e4_r1.coeff_monomial(p**3),
            -sp.Rational(2, 3) * base_relation,
        )
        assert_same(
            e4_r1.coeff_monomial(p**2 * q),
            -sp.Rational(2, 3) * (base_relation - 4 * l[8] ** 2),
        )
        # Both coefficients can vanish only if l33=0.
        singular_leaf = {
            **c1_zero,
            l[8]: 0,
            D.ap: 0,
            l[2]: 0,
            l[1]: l[7] * (u[0] - sp.Rational(8, 9) * c[0]),
        }
        e3_r1 = sp.Poly(coefficient(3, 1, singular_leaf), p, q)
        assert_same(
            e3_r1.coeff_monomial(q**2),
            -sp.Rational(8, 3) * l[7] ** 2,
        )
        # Hence l32=0, and l12=l13=l32=l33=0 makes det(L)=0.
        return

    # ell=q: E4[r] fixes l12 with an extra l33^2 term.
    assert_same(
        e4_r1.coeff_monomial(p**2 * q),
        -sp.Rational(2, 3) * (base_relation - 4 * l[8] ** 2),
    )
    e4_solution = {
        **c1_zero,
        l[1]: (
            l[7] * (u[0] - sp.Rational(8, 9) * c[0])
            - sp.Rational(4, 9) * l[8] ** 2
        ),
    }
    e4_r0 = sp.Poly(coefficient(4, 0, e4_solution), p, q)
    assert_same(
        e4_r0.coeff_monomial(p**4),
        -sp.Rational(4, 3) * v[4] * l[8] ** 2,
    )

    # If l33=0, E3[r] makes l32=0 and L is singular.
    l33_zero = {
        **e4_solution,
        l[8]: 0,
        D.ap: 0,
        l[2]: 0,
        l[1]: l[7] * (u[0] - sp.Rational(8, 9) * c[0]),
    }
    e3_r1_l33_zero = sp.Poly(coefficient(3, 1, l33_zero), p, q)
    assert_same(
        e3_r1_l33_zero.coeff_monomial(q**2),
        -sp.Rational(8, 3) * l[7] ** 2,
    )

    # If l33!=0, E4 forces v4=0.  Combining E4[r^0] and E3[r^2]
    # then forces v5=v6=l32=0 and fixes l31.
    l33_nonzero = {**e4_solution, v[4]: 0}
    e4_r0_nz = sp.Poly(coefficient(4, 0, l33_nonzero), p, q)
    e3_r2_nz = sp.Poly(coefficient(3, 2, l33_nonzero), p, q)
    e4_pq = sp.factor(e4_r0_nz.coeff_monomial(p**3 * q))
    e4_q2 = sp.factor(e4_r0_nz.coeff_monomial(p**2 * q**2))
    e3_p = sp.factor(e3_r2_nz.coeff_monomial(p))
    e3_q = sp.factor(e3_r2_nz.coeff_monomial(q))
    assert_same(e3_p - e4_pq / 2, 2 * l[8] ** 2 * v[5])
    assert_same(e4_q2 + 2 * e3_q, 4 * l[8] ** 2 * v[6])
    assert_same(2 * e4_q2 + e3_q, 4 * l[8] * l[7])

    final = {
        **l33_nonzero,
        v[5]: 0,
        v[6]: 0,
        l[7]: 0,
        l[1]: -sp.Rational(4, 9) * l[8] ** 2,
        x[1]: 0,
        l[6]: (8 * c[0] ** 2 - 9 * c[0] * u[0] + 9 * x[0]) / 6,
        D.bb: v[1] / 2,
        v[2]: sp.Rational(2, 3) * c[0],
        v[3]: 0,
    }
    assert exact_zero(coefficient(4, 0, final))
    assert exact_zero(coefficient(3, 2, final))
    assert exact_zero(coefficient(3, 1, final))
    e3_r0_final = sp.Poly(coefficient(3, 0, final), p, q)
    assert_same(
        e3_r0_final.coeff_monomial(p * q**2),
        sp.Rational(8, 9) * l[8] ** 3,
    )


run_orbit(0)
print("PASS v9=0, ell=q orbit excluded")
run_orbit(1)
print("PASS v9=0, ell=p+q orbit excluded")
print("ALL v9=0 q-CONTAINING ORBIT CHECKS PASSED")
