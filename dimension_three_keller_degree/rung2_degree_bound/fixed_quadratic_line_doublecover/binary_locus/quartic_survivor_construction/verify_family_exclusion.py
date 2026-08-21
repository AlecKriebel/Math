#!/usr/bin/env python3
"""Exact full-family descent for frozen family D3-BS-N1-CONTACT.

No BCW reduction is used.  The program constructs the weighted determinant
directly, retains all binary lower summands and every entry of the linear
part, and checks the complete E7/E6 branch split followed by E5/E4/E3.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
coords = (p, q, r)
mon2 = (p**2, p*q, p*r, q**2, q*r, r**2)
mon2b = (p**2, p*q, q**2)
mon3b = (p**3, p**2*q, p*q**2, q**3)

x, y0, y1, y2 = sp.symbols("x y0 y1 y2")
u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
t = sp.symbols("t0:3")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("l0:9")

A = sum(c*m for c, m in zip(a, mon2))
B = sum(c*m for c, m in zip(b, mon2))
L = sp.Matrix(3, 3, ell)
U0 = sum(c*m for c, m in zip(u, mon3b))
V0 = sum(c*m for c, m in zip(v, mon3b))
T0 = sum(c*m for c, m in zip(t, mon2b))

h = p**2
P = p**4
Q = p**2*q**2
R = p*(p**2+q**2)
U = U0 + 4*y0*p**2*r
V = V0 + r*((-3*y0+y1)*p**2+y2*p*q+y0*q**2) + x*p*r**2/2
T = T0 + r*(y1*p+y2*q) + x*r**2/2


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def coeffs(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return [
        pp.coeff_monomial(p**i*q**j*r**(degree-i-j))
        for i in range(degree, -1, -1)
        for j in range(degree-i, -1, -1)
    ]


def stage(expr, *subs):
    out = expr
    for sub in subs:
        out = sp.expand(out.subs(sub))
    return out


def linear_stage(poly, degree, variables, rows=None):
    equations = coeffs(poly, degree)
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    if rows is None:
        rows = matrix.T.rref()[1][:matrix.rank()]
    small_m = matrix[list(rows), :]
    small_rhs = rhs[list(rows), :]
    solution = tuple(next(iter(sp.linsolve((small_m, small_rhs), variables))))
    substitution = dict(zip(variables, solution))
    residual = sp.Poly(stage(poly, substitution), p, q, r)
    return matrix, rhs, substitution, residual


def nonzero_terms(poly):
    return {mon: sp.factor(c) for mon, c in poly.terms() if c != 0}


H2 = sp.Matrix([A, B, T])
H3 = sp.Matrix([U, V, R])
H4 = sp.Matrix([P, Q, 0])
D = sp.Poly(
    sp.expand(
        (L+z*H2.jacobian(coords)+z**2*H3.jacobian(coords)+z**3*H4.jacobian(coords)).det()
    ),
    z,
)
E = {degree: D.coeff_monomial(z**degree) for degree in range(1, 10)}
require(all(E[d] == 0 for d in (9, 8, 7)), "full E9/E8/E7 parameterization")

# Frozen registry binding.
registry = (
    Path(__file__).resolve().parents[2]
    / "audit_delta_ge3_denominator"
    / "DENOMINATOR.json"
)
raw = registry.read_bytes()
data = json.loads(raw)
require(len(data["families"]) == 26, "frozen family count")
family = next(f for f in data["families"] if f["id"] == "D3-BS-N1-CONTACT")
require(
    family["normal_form"] == {"h": "p^2", "R": "p(p^2+q^2)"},
    "frozen normal form",
)
print("REGISTRY_SHA256", hashlib.sha256(raw).hexdigest())

# Complete division-free E6 pivot and compatibility ideal.
C = 4*t[1]-3*u[1]-4*v[1]
e6_pivot = {
    a[2]: -4*t[2]*y0+3*u[0]*y0+u[1]*y2/2-3*u[2]*y0+u[2]*y1
          -sp.Rational(9,2)*u[3]*y2-6*v[3]*y2,
    a[4]: sp.Rational(3,2)*u[1]*y0+u[2]*y2+sp.Rational(3,2)*u[3]*y1+6*v[3]*y0,
    a[5]: u[2]*x/2+6*y0**2,
    b[2]: ell[8]-2*t[0]*y0-t[1]*y2/2+6*t[2]*y0-t[2]*y1
          +sp.Rational(27,8)*u[3]*y2+3*v[0]*y0+v[1]*y2/2
          -3*v[2]*y0+v[2]*y1+sp.Rational(9,2)*v[3]*y2,
    b[4]: -t[1]*y0/2-t[2]*y2+sp.Rational(3,8)*u[1]*y0-u[1]*y1/8
          -sp.Rational(27,8)*u[3]*y0+sp.Rational(3,2)*v[1]*y0+v[2]*y2
          -9*v[3]*y0+sp.Rational(3,2)*v[3]*y1,
    b[5]: -t[2]*x/2+v[2]*x/2-6*y0**2+y0*y1,
}
e6_expected = (
    (3*y0-y1)*C*p**6 - x*C*p**5*r
    +(-u[1]*x+9*u[3]*x+12*v[3]*x+16*y0*y2)*p**3*q**2*r
    +12*x*y0*p**3*q*r**2
    -3*u[3]*y2*p*q**5-3*u[3]*x*p*q**4*r+3*u[3]*y0*q**6
)
require(sp.expand(stage(E[6], e6_pivot)-e6_expected) == 0, "complete E6 pivot residual")
print("E6_COMPATIBILITY",
      "(3*y0-y1)*C, x*C, x*(-u1+9*u3+12*v3)+16*y0*y2, "
      "x*y0, u3*y2, u3*x, u3*y0")

lower6 = (a[2], a[4], a[5], b[2], b[4], b[5], ell[8])
lower5 = (a[0], a[1], a[3], b[0], b[1], b[3]) + ell[:8]


def solve_chart(base, extra_e5=()):
    base_all = dict(base)
    base_all.update(extra_e5)
    d6 = stage(E[6], base_all)
    m6, rhs6, s6, residual6 = linear_stage(d6, 6, lower6)
    require(not nonzero_terms(residual6), "chart E6 consistency")
    d5 = stage(E[5], base_all, s6)
    m5, rhs5, s5, residual5 = linear_stage(d5, 5, lower5)
    return s6, s5, residual5


# Chart X: x != 0.  Source scaling and the shear
# r -> r-y1*p-y2*q give x=1,y1=y2=0.
base_x = {
    x: 1, y0: 0, y1: 0, y2: 0,
    u[3]: 0, u[1]: 12*v[3], t[1]: 9*v[3]+v[1],
}
sx6, sx5, rx5 = solve_chart(base_x)
require(
    nonzero_terms(rx5).get((2, 0, 3)) == -6*v[3],
    "X chart E5 forces v3=0",
)
base_x0 = dict(base_x)
base_x0[v[3]] = 0
sx6, sx5, rx5 = solve_chart(base_x0)
require(not nonzero_terms(rx5), "X chart complete E5")
d4x = stage(E[4], base_x0, sx6, sx5)
mx, rx = sp.linear_eq_to_matrix(coeffs(d4x, 4), (ell[1], ell[4]))
solx = tuple(next(iter(sp.linsolve((mx, rx), (ell[1], ell[4])))))
subx = {ell[1]: solx[0], ell[4]: solx[1]}
require(stage(d4x, subx) == 0, "X chart complete E4")
require(sp.factor(stage(L.det(), base_x0, sx6, sx5, subx)) == 0, "X chart detL")
print("X_CHART", "E5:[p^2*r^3]=-6*v3; E4=>detL=0")

# Chart Y2: x=y0=y1=0, y2 != 0, normalized to one.
base_y2 = {x: 0, y0: 0, y1: 0, y2: 1, u[3]: 0}
sy26, sy25, ry25 = solve_chart(base_y2)
ty2 = nonzero_terms(ry25)
require(sp.expand(ty2[(4, 0, 1)]-C/2) == 0, "Y2 E5 C")
require(sp.expand(ty2[(2, 2, 1)]-(u[1]-36*v[3])/2) == 0, "Y2 E5 u1")
base_y2c = dict(base_y2)
base_y2c.update({u[1]: 36*v[3], t[1]: v[1]+27*v[3]})
sy26, sy25, ry25 = solve_chart(base_y2c)
require(not nonzero_terms(ry25), "Y2 complete E5")
d4y2 = sp.Poly(stage(E[4], base_y2c, sy26, sy25), p, q, r)
require(
    sp.factor(d4y2.coeff_monomial(p*q*r**2)) == 12*v[3]
    and sp.factor(d4y2.coeff_monomial(q**3*r)) == -144*v[3]**2,
    "Y2 E4 forces v3=0",
)
base_y2z = dict(base_y2c)
base_y2z[v[3]] = 0
sy26, sy25, ry25 = solve_chart(base_y2z)
y2_contact = {ell[2]: ell[8]*u[2], ell[5]: ell[8]*(v[2]-t[2])}
d4y2 = stage(E[4], base_y2z, sy26, sy25, y2_contact)
my2, ry2 = sp.linear_eq_to_matrix(coeffs(d4y2, 4), (ell[1], ell[4]))
soly2 = tuple(next(iter(sp.linsolve((my2, ry2), (ell[1], ell[4])))))
suby2 = {ell[1]: soly2[0], ell[4]: soly2[1]}
require(stage(d4y2, suby2) == 0, "Y2 complete E4")
require(
    sp.factor(stage(L.det(), base_y2z, sy26, sy25, y2_contact, suby2)) == 0,
    "Y2 detL",
)
print("Y2_CHART", "E5=>C=0,u1=36*v3; E4=>v3=0,detL=0")

# Chart Y1: x=y0=y2=0, y1 != 0, normalized to one.
base_y1 = {x: 0, y0: 0, y1: 1, y2: 0, t[1]: (3*u[1]+4*v[1])/4}
sy16, sy15, ry15 = solve_chart(base_y1)
ty1 = nonzero_terms(ry15)
require(sp.expand(ty1[(2, 2, 1)]+sp.Rational(3,2)*u[3]) == 0, "Y1 E5 u3")
require(
    sp.expand(ty1[(4, 0, 1)]+sp.Rational(3,2)*(u[1]-3*u[3]-4*v[3])) == 0,
    "Y1 E5 u1",
)
base_y1c = dict(base_y1)
base_y1c.update({u[3]: 0, u[1]: 4*v[3], t[1]: 3*v[3]+v[1]})
sy16, sy15, ry15 = solve_chart(base_y1c)
require(not nonzero_terms(ry15), "Y1 complete E5")

# v3 != 0: complete E4 pivots leave the two equal E3 obstructions.
y1_nonzero = {
    ell[8]: t[2],
    u[0]: u[2]+4*t[2],
    ell[2]: t[2]*u[2]+12*v[3]**2,
    ell[7]: 3*t[0]*v[3]+t[2]*v[1]-12*t[2]*v[3]-3*v[0]*v[3]+3*v[2]*v[3],
}
d4y1n = stage(E[4], base_y1c, sy16, sy15, y1_nonzero)
mn, rn = sp.linear_eq_to_matrix(coeffs(d4y1n, 4), (ell[1], ell[4]))
soln = tuple(next(iter(sp.linsolve((mn, rn), (ell[1], ell[4])))))
subn = {ell[1]: soln[0], ell[4]: soln[1]}
require(stage(d4y1n, subn) == 0, "Y1 v3-nonzero complete E4")
d3y1n = sp.Poly(stage(E[3], base_y1c, sy16, sy15, y1_nonzero, subn), p, q, r)
require(
    sp.factor(d3y1n.coeff_monomial(p**2*r)) == -12*v[3]**3
    and sp.factor(d3y1n.coeff_monomial(q**2*r)) == -12*v[3]**3,
    "Y1 v3-nonzero E3 obstruction",
)

# v3=0.  Put d=t2-l8.  On d!=0 E4 forces the displayed l2,l5 and detL=0.
base_y1z = dict(base_y1c)
base_y1z[v[3]] = 0
sy16z, sy15z, ry15z = solve_chart(base_y1z)
y1_dnz = {ell[2]: ell[8]*u[2], ell[5]: ell[8]*(v[2]-t[2])}
d4dnz = stage(E[4], base_y1z, sy16z, sy15z, y1_dnz)
md, rd = sp.linear_eq_to_matrix(coeffs(d4dnz, 4), (ell[1], ell[4]))
sold = tuple(next(iter(sp.linsolve((md, rd), (ell[1], ell[4])))))
subd = {ell[1]: sold[0], ell[4]: sold[1]}
require(stage(d4dnz, subd) == 0, "Y1 d-nonzero complete E4")
require(sp.factor(stage(L.det(), base_y1z, sy16z, sy15z, y1_dnz, subd)) == 0, "Y1 d-nonzero detL")

# On d=0, E3 has a common factor g which also divides detL.  If g!=0,
# its two cofactors force the same l2,l5 values and the quotient vanishes.
y1_d0 = {t[2]: ell[8]}
d4d0 = stage(E[4], base_y1z, sy16z, sy15z, y1_d0)
m0, r0 = sp.linear_eq_to_matrix(coeffs(d4d0, 4), (ell[1], ell[4]))
sol0 = tuple(next(iter(sp.linsolve((m0, r0), (ell[1], ell[4])))))
sub0 = {ell[1]: sol0[0], ell[4]: sol0[1]}
require(stage(d4d0, sub0) == 0, "Y1 d-zero complete E4")
g = -ell[7]+ell[8]*v[1]
d3d0 = sp.Poly(stage(E[3], base_y1z, sy16z, sy15z, y1_d0, sub0), p, q, r)
require(
    sp.expand(sp.factor(d3d0.coeff_monomial(p*q**2))-g*(-ell[2]+ell[8]*u[2])) == 0,
    "Y1 d0 E3 first",
)
detd0 = sp.factor(stage(L.det(), base_y1z, sy16z, sy15z, y1_d0, sub0))
quot = sp.factor(detd0/g)
require(sp.denom(quot) == 1, "Y1 d0 determinant factor")
forced_d0 = {ell[2]: ell[8]*u[2], ell[5]: ell[8]*(v[2]-ell[8])}
require(sp.factor(quot.subs(forced_d0)) == 0, "Y1 d0 nonzero-g determinant quotient")
print("Y1_CHART", "v3!=0=>[p^2*r]E3=-12*v3^3; v3=0=>g|detL and E3=>detL=0")

# Mixed chart y1=1,y2=s !=0.  Generic pivot 3*s^2!=1.
s = sp.symbols("s")
base_mix = {
    x: 0, y0: 0, y1: 1, y2: s, u[3]: 0,
    t[1]: (3*u[1]+4*v[1])/4,
}
sm6, sm5, rm5 = solve_chart(base_mix)
tm = nonzero_terms(rm5)
require(sp.expand(tm[(4, 0, 1)]+sp.Rational(3,2)*(u[1]-4*v[3])) == 0, "mixed E5 first")
require(sp.expand(tm[(3, 1, 1)]+s*(u[1]+12*v[3])) == 0, "mixed E5 second")
base_mix0 = dict(base_mix)
base_mix0.update({u[1]: 0, v[3]: 0, t[1]: v[1]})
sm6, sm5, rm5 = solve_chart(base_mix0)
require(not nonzero_terms(rm5), "mixed complete E5")
Mcontact = ell[5]+ell[8]*(t[2]-v[2])
d4m = sp.Poly(stage(E[4], base_mix0, sm6, sm5), p, q, r)
require(
    sp.cancel(
        sp.factor(d4m.coeff_monomial(p**3*r))
        - 12*s*Mcontact/(3*s**2-1)
    ) == 0,
    "mixed generic E4 contact",
)
dm_contact = {ell[5]: ell[8]*(v[2]-t[2])}
d4mc = stage(E[4], base_mix0, sm6, sm5, dm_contact)
mm, rr = sp.linear_eq_to_matrix(coeffs(d4mc, 4), (ell[1], ell[4]))
solm = tuple(next(iter(sp.linsolve((mm, rr), (ell[1], ell[4])))))
subm = {ell[1]: solm[0], ell[4]: solm[1]}
require(sp.cancel(stage(d4mc, subm)) == 0, "mixed generic complete E4")
require(sp.cancel(stage(L.det(), base_mix0, sm6, sm5, dm_contact, subm)) == 0, "mixed generic detL")

# The omitted pivot divisor 3*s^2=1 is one irreducible quadratic field.
ss = sp.sqrt(3)/3
base_ms = {
    k: sp.expand(sp.sympify(val).subs(s, ss))
    for k, val in base_mix.items()
    if k != y2
}
base_ms[y2] = ss
base_ms.update({u[1]: 0, v[3]: 0, t[1]: v[1]})
sms6, sms5, rms5 = solve_chart(base_ms)
require(not nonzero_terms(rms5), "mixed special complete E5")
d4ms = sp.Poly(stage(E[4], base_ms, sms6, sms5), p, q, r)
require(
    sp.factor(d4ms.coeff_monomial(p**3*r))
    == 3*sp.sqrt(3)*(-ell[2]+ell[8]*u[2]),
    "mixed special E4 contact",
)
special_contact = {ell[2]: ell[8]*u[2]}
d4msc = stage(E[4], base_ms, sms6, sms5, special_contact)
mms, rrs = sp.linear_eq_to_matrix(coeffs(d4msc, 4), (ell[1], ell[4]))
solms = tuple(next(iter(sp.linsolve((mms, rrs), (ell[1], ell[4])))))
subms = {ell[1]: solms[0], ell[4]: solms[1]}
require(stage(d4msc, subms) == 0, "mixed special complete E4")
require(sp.factor(stage(L.det(), base_ms, sms6, sms5, special_contact, subms)) == 0, "mixed special detL")
print("MIXED_CHART", "s!=0: E5=>u1=v3=0; generic and 3*s^2=1 E4 charts give detL=0")

# y0 !=0: normalize y0=1, put m=y1.  E6 gives x=y2=u3=0 and
# (m-3)C=0.  Both m!=3 and m=3 are inconsistent already at E5.
m = sp.symbols("m")
base_y0 = {
    x: 0, y0: 1, y1: m, y2: 0, u[3]: 0,
    t[1]: (3*u[1]+4*v[1])/4,
}
sy06, _, _ = solve_chart(base_y0)
d5y0 = stage(E[5], base_y0, sy06)
My0, by0 = sp.linear_eq_to_matrix(coeffs(d5y0, 5), lower5)
require(My0.rank() == 6, "y0 generic coefficient rank")
Aug = My0.row_join(by0)
rows = [0, 1, 3, 6, 10, 15, 8]
cols = [0, 1, 2, 3, 4, 13, 14]
require(
    sp.expand(sp.factor(Aug[rows, cols].det())-98304*(m-3)) == 0,
    "y0 generic augmented minor",
)

base_y03 = {x: 0, y0: 1, y1: 3, y2: 0, u[3]: 0}
sy036, _, _ = solve_chart(base_y03)
d5y03 = stage(E[5], base_y03, sy036)
My03, by03 = sp.linear_eq_to_matrix(coeffs(d5y03, 5), lower5)
require(My03.rank() == 5, "y0 special coefficient rank")
Aug3 = My03.row_join(by03)
rows3 = [1, 3, 6, 10, 15, 8]
cols3 = [0, 1, 2, 3, 4, 14]
require(Aug3[rows3, cols3].det() == 12288, "y0 special augmented minor")
print("Y0_CHART", "rank(M5)=6, augmented minor=98304*(m-3); m=3 minor=12288")

# E7 origin.  E6 gives A_r=0 and B_r=l8*p.  If l8=0 every nonlinear
# term is binary.  If l8!=0, F3=l8*r+B3(p,q) is a coordinate of degree <=3.
origin = {x: 0, y0: 0, y1: 0, y2: 0}
_, _, so6, ro6 = linear_stage(stage(E[6], origin), 6, lower6)
require(
    tuple(sp.factor(so6[vv]) for vv in lower6)
    == (0, 0, 0, ell[8], 0, 0, ell[8]),
    "origin E6 solution",
)
print("ORIGIN", "E6: A_r=0, B_r=l8*p; l8=0 binary exit, l8!=0 coordinate exit")
print("D3_BS_N1_CONTACT_FULL_FAMILY_EXCLUSION_PASS")
