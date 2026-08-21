#!/usr/bin/env python3
"""Exact ell=0 identities and the two low-degree plane-coordinate exits."""

from __future__ import annotations

import sympy as sp

import explore_power_fibre_v9zero as D


if not __debug__:
    raise RuntimeError("assertions must remain enabled")

p, q, r = D.p, D.q, D.r
c, u, v, l = D.c, D.u, D.v, D.l
w = sp.symbols("w")


def coefficient(degree: int, r_power: int, substitutions) -> sp.Expr:
    return sp.factor(
        sp.Poly(D.E[degree].as_expr(), r)
        .coeff_monomial(r**r_power)
        .subs(substitutions)
    )


def assert_same(left, right) -> None:
    assert sp.factor(sp.together(left - right)) == 0


ell_zero = {v[9]: 0, v[7]: 0, v[8]: 0, D.tt: 0}

# E6[r] forces tq=0 and aa=2tp^2/9.
e6_r1 = coefficient(6, 1, ell_zero)
assert_same(
    e6_r1,
    -sp.Rational(4, 3)
    * p**2
    * q
    * (
        9 * D.aa * p**2
        - 2 * p**2 * D.tp**2
        - 4 * p * q * D.tp * D.tq
        - 2 * q**2 * D.tq**2
    ),
)

top = {
    **ell_zero,
    D.tq: 0,
    D.aa: sp.Rational(2, 9) * D.tp**2,
}
e5_r2 = coefficient(5, 2, top)
assert_same(e5_r2, -sp.Rational(8, 9) * p**2 * q * D.tp**3)

# Hence the only possible ell=0 leaf has tp=tq=tt=aa=0.
tp_zero = {
    v[9]: 0,
    v[7]: 0,
    v[8]: 0,
    D.tt: 0,
    D.tq: 0,
    D.tp: 0,
    D.aa: 0,
}

source = sp.Matrix((p, q, r))
F = sp.expand(D.L * source + D.H2 + D.H3 + D.H4)
F0 = sp.Matrix([sp.expand(component.subs(tp_zero)) for component in F])

# The third component is l33*r+G(p,q).
G = sp.expand(F0[2].subs({r: 0}))
assert sp.expand(F0[2] - (l[8] * r + G)) == 0

# If l33!=0, w=F3 is a triangular source coordinate.  Eliminating r
# leaves a plane Keller map in p,q of degree at most six over C(w).
r_from_w = (w - G) / l[8]
plane_l33 = [
    sp.together(F0[index].subs({r: r_from_w}))
    for index in (0, 1)
]
degrees_l33 = [
    sp.Poly(expression.as_numer_denom()[0], p, q).total_degree()
    for expression in plane_l33
]
assert max(degrees_l33) <= 6
assert sp.expand(F0[2].subs({r: r_from_w}) - w) == 0

# If l33=0, the Keller condition says G has no critical point.  For
# G=p^3+c0*p^2+c1*p*q+c2*q^2+l31*p+l32*q:
#   c2!=0 gives a quadratic critical equation with leading coefficient 3;
#   c2=0,c1!=0 gives a critical point by two linear solves;
# hence c1=c2=0 and l32!=0.
G_l330 = sp.expand(G.subs({l[8]: 0}))
expected_G = (
    p**3
    + c[0] * p**2
    + c[1] * p * q
    + c[2] * q**2
    + l[6] * p
    + l[7] * q
)
assert sp.expand(G_l330 - expected_G) == 0
q_critical = -(c[1] * p + l[7]) / (2 * c[2])
critical_equation = sp.together(
    sp.diff(expected_G, p).subs({q: q_critical})
).as_numer_denom()[0]
assert sp.Poly(critical_equation, p).degree() == 2
assert sp.Poly(critical_equation, p).LC() == 6 * c[2]
assert sp.diff(expected_G, p, q) == c[1]

# On the only submersion leaf, w=G is the triangular coordinate replacing q.
coordinate_leaf = {
    **tp_zero,
    l[8]: 0,
    c[1]: 0,
    c[2]: 0,
}
F_coordinate = sp.Matrix(
    [sp.expand(component.subs(coordinate_leaf)) for component in F]
)
q_from_w = (w - p**3 - c[0] * p**2 - l[6] * p) / l[7]
plane_l320 = [
    sp.together(F_coordinate[index].subs({q: q_from_w}))
    for index in (0, 1)
]
degrees_l320 = [
    sp.Poly(expression.as_numer_denom()[0], p, r).total_degree()
    for expression in plane_l320
]
assert max(degrees_l320) <= 9
assert sp.expand(F_coordinate[2].subs({q: q_from_w}) - w) == 0

print("PASS v9=ell=0, tp!=0 obstruction E5[r^2]=-(8/9)p^2*q*tp^3")
print(f"PASS l33 coordinate exit has plane degree <= {max(degrees_l33)}")
print("PASS binary cubic submersion classification forces c1=c2=0, l32!=0")
print(f"PASS l32 coordinate exit has plane degree <= {max(degrees_l320)}")
print("ALL v9=0 ell=0 CHECKS PASSED")
