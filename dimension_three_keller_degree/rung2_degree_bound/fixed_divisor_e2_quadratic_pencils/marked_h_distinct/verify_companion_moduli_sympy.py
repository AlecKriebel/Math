#!/usr/bin/env python3
"""Exact certificate for the failure of the two-companion-orbit claim."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: verification requires assertions; do not use -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

x, y, z = sp.symbols("x y z")
a, b, lam, mu = sp.symbols("a b lam mu")
xyz = (x, y, z)


def jac3(f, g, h):
    return sp.Matrix([f, g, h]).jacobian(xyz).det()


def conic_matrix(q):
    return sp.hessian(q, xyz) / 2


def rank(q):
    return conic_matrix(q).rank()


s = x**2
rt_r = y * z
ro_r = y**2 + x * z

# The discriminant divisor constrains the induced action on each pencil.
assert sp.factor(conic_matrix(a * s + b * rt_r).det()) == -a * b**2 / 4
assert sp.factor(conic_matrix(a * s + b * ro_r).det()) == -b**3 / 4

# Explicit source transformations realize the expected base actions.
assert sp.expand(s.subs(x, lam * x, simultaneous=True) - lam**2 * s) == 0
assert sp.expand(rt_r.subs(x, lam * x, simultaneous=True) - rt_r) == 0
assert (
    sp.expand(
        ro_r.subs({z: z + mu * x}, simultaneous=True) - (ro_r + mu * s)
    )
    == 0
)
assert (
    sp.expand(
        ro_r.subs({x: lam * x, z: z / lam}, simultaneous=True) - ro_r
    )
    == 0
)
assert (
    sp.expand(
        s.subs({x: lam * x, z: z / lam}, simultaneous=True) - lam**2 * s
    )
    == 0
)

# The complete top kernel really contains every projective mixture.
for h, r in ((rt_r, rt_r), (s + rt_r, rt_r), (ro_r, ro_r)):
    g = a * h + b * s
    assert sp.expand(jac3(h**2, h * s, x * g)) == 0

# Exact counterexamples to the claimed endpoint exhaustion.
rt_reducible_mixed = s + rt_r
assert (rank(s), rank(rt_r), rank(rt_reducible_mixed)) == (1, 2, 3)
assert sp.expand(jac3(rt_r**2, rt_r * s, x * rt_reducible_mixed)) == 0

rt_smooth_h = s + rt_r
rt_smooth_third = rt_r
assert (rank(s), rank(rt_smooth_third), rank(rt_smooth_h)) == (1, 2, 3)
assert sp.expand(
    jac3(rt_smooth_h**2, rt_smooth_h * s, x * rt_smooth_third)
) == 0

print("PASS companion moduli: endpoint exhaustion is false")
