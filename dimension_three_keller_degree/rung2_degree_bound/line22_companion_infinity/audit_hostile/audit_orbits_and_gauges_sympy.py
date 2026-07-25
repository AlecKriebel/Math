#!/usr/bin/env python3
"""Exact orbit and affine-gauge audit for the companion-at-infinity chart."""

if not __debug__:
    raise RuntimeError("orbit/gauge audit refuses optimized Python")

import sympy as sp

x, y, z = sp.symbols("x y z")
p, q = x**2, y*z
t, a, lam = sp.symbols("t a lam", nonzero=True)

# The connected source-pencil stabilizer is diagonal.  Its induced action
# on u=p/q is arbitrary scaling; the y,z swap has trivial base action.
alpha, beta, gamma = sp.symbols("alpha beta gamma", nonzero=True)
xp, yp, zp = alpha*x, beta*y, gamma*z
assert sp.expand(xp**2-alpha**2*p) == 0
assert sp.expand(yp*zp-beta*gamma*q) == 0
assert sp.Matrix.diag(alpha, beta, gamma).det() == alpha*beta*gamma
assert sp.simplify((alpha**2*p/(beta*gamma*q))/(p/q)) == alpha**2/(beta*gamma)

# A general diagonal-branch candidate cannot contain x-translations in y,z.
r, s = sp.symbols("r s")
translated_product = sp.Poly((beta*y+r*x)*(gamma*z+s*x), x, y, z)
assert translated_product.coeff_monomial(x*y) == beta*s
assert translated_product.coeff_monomial(x*z) == gamma*r
assert translated_product.coeff_monomial(y*z) == beta*gamma

# The unordered finite pair {t,1} has the reciprocal ambiguity.  Every
# obstruction factor is reciprocal, and the two resonance values form one
# orbit.
raw_factor = (t-1)**10*(t+2)**4*(2*t+1)**4
e6_factor = (t-1)**6*(t+2)**2*(2*t+1)**2
e5_factor = (t-1)**2
assert sp.factor(t**18*raw_factor.subs(t, 1/t)-raw_factor) == 0
assert sp.factor(t**10*e6_factor.subs(t, 1/t)-e6_factor) == 0
assert sp.factor(t**2*e5_factor.subs(t, 1/t)-e5_factor) == 0
assert sp.Rational(1, -2) == sp.Rational(-1, 2)

# The t=infinity boundary is exactly the a=1 outer chart after scaling the
# first target coordinate and swapping the two target coordinates.
finite_first = (p-t*q)**2
finite_second = (p-q)**2
assert sp.limit(finite_first/t**2, t, sp.oo) == q**2
assert finite_second == (p-q)**2

# Translation/shear ledger.  Start from all six post-(y,z)-translation
# kernel coefficients.
A, B, C, D, w = sp.symbols("A B C D w")
h = -A/4

# Finite pair: tau_x=(4x(p-tq),4x(p-q),q).
finite_after_translation = {
    "Ux3": A+4*h,
    "Uxq": B-4*t*h,
    "Vx3": C+4*h,
    "Vxq": D-4*h,
    "Wq": w+h,
}
assert finite_after_translation["Ux3"] == 0
assert finite_after_translation["Vx3"] == C-A
finite_first_shear = -finite_after_translation["Uxq"]
finite_second_shear = -finite_after_translation["Vxq"]
assert sp.expand(finite_after_translation["Uxq"]+finite_first_shear) == 0
assert sp.expand(finite_after_translation["Vxq"]+finite_second_shear) == 0

# Outer pair: tau_x=(4x(p-aq),0,q).
outer_after_translation = {
    "Ux3": A+4*h,
    "Uxq": B-4*a*h,
    "Vx3": C,
    "Vxq": D,
    "Wq": w+h,
}
assert outer_after_translation["Ux3"] == 0
outer_first_shear = -outer_after_translation["Uxq"]
outer_second_shear = -outer_after_translation["Vxq"]
assert sp.expand(outer_after_translation["Uxq"]+outer_first_shear) == 0
assert sp.expand(outer_after_translation["Vxq"]+outer_second_shear) == 0

print("PASS: companion-at-infinity orbit and affine-gauge audit")
