#!/usr/bin/env python3
"""Independent exact polynomial checks; Python standard library only.

Checks algebra used in PROOF.md, with arbitrary formal t,s,c,d,n,m. No candidate
code is imported. These checks support, but do not replace, the analytic proof.
"""
import json
import platform
from pathlib import Path

# Rational coefficient polynomials in the formal variables t,s,c,d,n,m.
from fractions import Fraction
NV = 6
Z = {}
def const(v):
    return {} if not v else {(0,) * NV: Fraction(v)}
def var(i):
    e = [0] * NV; e[i] = 1
    return {tuple(e): Fraction(1)}
def add(a, b):
    out = dict(a)
    for e, v in b.items():
        out[e] = out.get(e, 0) + v
        if not out[e]: del out[e]
    return out
def neg(a): return {e: -v for e, v in a.items()}
def mul(a, b):
    out = {}
    for e, v in a.items():
        for f, w in b.items():
            g = tuple(x + y for x, y in zip(e, f))
            out[g] = out.get(g, 0) + v * w
            if not out[g]: del out[g]
    return out
def mm(A, B):
    return [[sum_poly(mul(A[i][k], B[k][j]) for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]
def sum_poly(seq):
    r = Z
    for x in seq: r = add(r, x)
    return r
def ident(size):
    return [[const(int(i == j)) for j in range(size)] for i in range(size)]
def transpose(A): return [list(x) for x in zip(*A)]
def det(A):
    if len(A) == 1: return A[0][0]
    return sum_poly(mul(const((-1) ** j), mul(A[0][j], det([
        row[:j] + row[j + 1:] for row in A[1:]]))) for j in range(len(A)))
def frame(t):
    C = ident(4); C[1][0] = neg(t); return C
def shear2(n):
    A = ident(2); A[1][0] = n; return A

t, s, c, d, n, m = [var(i) for i in range(NV)]
checks = {}
A = shear2(const(1))
Sigma = [[Z, const(1)], [const(-1), Z]]
checks['skew_shift_preserves_area'] = mm(mm(transpose(A), Sigma), A) == Sigma
checks['all_integer_iterate_cocycle_polynomial'] = mm(shear2(n), shear2(m)) == shear2(add(n, m))
checks['iterate_determinant_one'] = det(shear2(n)) == const(1)
Dg = ident(4); Dg[1][0] = const(1)
checks['frame_descends_through_mapping_torus'] = mm(Dg, frame(t)) == frame(add(t, const(-1)))
S = ident(4); S[1][0] = s
checks['all_time_frame_derivative_constant_speed'] = mm(frame(add(t, s)), S) == frame(t)
checks['inverse_shear_polynomial'] = mm(S, [row[:] for row in (
    [[const(1), Z, Z, Z], [neg(s), const(1), Z, Z],
     [Z, Z, const(1), Z], [Z, Z, Z, const(1)]])]) == ident(4)
Omega = [[Z, const(1), Z, Z], [const(-1), Z, Z, Z],
         [Z, Z, Z, const(1)], [Z, Z, const(-1), Z]]
checks['symplectic_form_nondegenerate'] = det(Omega) == const(1)
checks['symplectic_form_descends'] = mm(mm(transpose(Dg), Omega), Dg) == Omega
checks['hamiltonian_contraction_sign'] = Omega[2] == [Z, Z, Z, const(1)]
# General compact Hamiltonian H=h(E): c=h'(E), d=h''(E).
Dcover = ident(4); Dcover[2][3] = mul(s, d)
Scompact = ident(4); Scompact[1][0] = mul(s, c); Scompact[2][3] = mul(s, d)
checks['general_hamiltonian_all_tangent_cocycle'] = (
    mm(frame(add(t, mul(s, c))), Scompact) == mm(Dcover, frame(t)))
# The lifted y coordinate has n*x+a*n(n-1)/2. Verify its quadratic
# increment equals x+n*a, using an extra variable c as formal a.
yn = mul(mul(c, n), add(n, const(-1)))
yn = mul(const(Fraction(1, 2)), yn)
np1 = add(n, const(1))
ynp1 = mul(const(Fraction(1, 2)), mul(mul(c, np1), n))
checks['quadratic_iterate_phase_recurrence'] = add(ynp1, neg(yn)) == mul(c, n)
assert all(checks.values()), checks
result = {'status': 'PASS', 'method': 'exact formal-polynomial coefficient identities',
          'python': platform.python_version(), 'checks': checks,
          'limits': 'Does not mechanically verify Fubini, ergodicity, or compactness of L2 orbits; see PROOF.md.'}
Path(__file__).with_name('ALGEBRA_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
