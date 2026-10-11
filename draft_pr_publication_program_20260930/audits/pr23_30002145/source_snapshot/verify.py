#!/usr/bin/env python3
"""Small exact checks of established classification formulas, not a novelty claim.

Run: python3 verify.py
Requires SymPy (tested with 1.14.0). No network, randomness, or numerical tolerance.
"""
import sympy as s


def symmetric_gradient(u, x):
    D = u.jacobian(x)
    return (D + D.T) / 2


def assert_matrix_zero(M):
    assert all(s.simplify(z) == 0 for z in M), M


for d in (2, 3, 4):
    x = s.Matrix(s.symbols(f'x0:{d}'))
    a = s.Matrix(s.symbols(f'a0:{d}'))
    b = s.Matrix(s.symbols(f'b0:{d}'))
    v = s.Matrix(s.symbols(f'v0:{d}'))
    A, B, V = x.dot(a), x.dot(b), x.dot(v)
    H1, H2 = s.Function('H1'), s.Function('H2')
    u = a * (H1(B) + B * V) + b * (H2(A) + A * V) - v * A * B
    t = s.Symbol('t')
    lam = s.diff(H1(t), t).subs(t, B) + s.diff(H2(t), t).subs(t, A) + 2 * V
    assert_matrix_zero(symmetric_gradient(u, x) - lam * (a * b.T + b * a.T) / 2)
    print(f'PASS independent-vector formula, symbolic d={d}')

    H = s.Function('H')
    P = [s.Function(f'P{j}')(x[0]) for j in range(1, d)]
    u = s.Matrix([H(x[0]) + sum(x[j] * s.diff(P[j-1], x[0]) for j in range(1, d))] + [-p for p in P])
    lam = s.diff(H(x[0]), x[0]) + sum(x[j] * s.diff(P[j-1], x[0], 2) for j in range(1, d))
    target = s.zeros(d)
    target[0, 0] = lam
    assert_matrix_zero(symmetric_gradient(u, x) - target)
    print(f'PASS parallel-vector formula, symbolic d={d}')

x, y, z = s.symbols('x y z')
u = s.Matrix([y*z, x*z, -x*y])
assert_matrix_zero(symmetric_gradient(u, s.Matrix([x,y,z])) - s.Matrix([[0,z,0],[z,0,0],[0,0,0]]))
assert s.diff(2*z, z) == 2
print('PASS transverse quadratic obstruction in dimension 3')

u = s.Matrix([4*x**3*y, -x**4])
assert_matrix_zero(symmetric_gradient(u, s.Matrix([x,y])) - s.diag(12*x*x*y, 0))
assert s.diff(12*x*x*y, y) == 12*x*x
print('PASS parallel-vector non-one-directional example in dimension 2')
print('All 8 exact symbolic checks passed. Necessity is supplied by the cited theorem, not these checks.')
