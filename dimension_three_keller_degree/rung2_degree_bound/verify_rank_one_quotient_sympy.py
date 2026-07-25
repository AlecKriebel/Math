#!/usr/bin/env python3
"""Exact checks for WORKING_RANK_ONE_QUOTIENT_CUBIC.md."""

import sympy as sp

x, y, z, t = sp.symbols("x y z t")
X = sp.Matrix([x, y, z])

# A concrete generic-looking cubic pair and the exceptional normal form.
L = x + 2 * y + 3 * z
Q = x**3 + 2 * y**3 + 3 * z**3 + x * y * z
P = L**3
h = L * (5 * P + 7 * Q)
assert sp.expand(sp.det(sp.Matrix.hstack(sp.diff(P, X),
                                         sp.diff(Q, X),
                                         sp.diff(h, X)))) == 0

# Formal row-oriented Jacobian check:
# coefficient of two copies of B and one C is Jac(P,Q,h).
p1, p2, p3 = sp.symbols("p1 p2 p3")
q1, q2, q3 = sp.symbols("q1 q2 q3")
s1, s2, s3 = sp.symbols("s1 s2 s3")
r1, r2, r3 = sp.symbols("r1 r2 r3")
B = sp.Matrix([[p1, p2, p3], [q1, q2, q3], [s1, s2, s3]])
C = sp.Matrix([[0, 0, 0], [0, 0, 0], [r1, r2, r3]])
coefficient = sp.expand((B + t * C).det()).coeff(t, 1)
jacobian = sp.Matrix([[p1, p2, p3],
                      [q1, q2, q3],
                      [r1, r2, r3]]).det()
assert sp.expand(coefficient - jacobian) == 0

print("rank-one quotient-cubic SymPy checks passed")
