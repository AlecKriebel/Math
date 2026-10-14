#!/usr/bin/env python3
# Reader edition: explicit runtime checks; results go only to stdout.
"""Independent exact polynomial controls for the pass-4 rigidity report."""
from pathlib import Path
from itertools import combinations
import json
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ, QQ
x, y, z, t = s.symbols('x y z t')
vars = (x, y, z)
p = x * (x - z)
q = y * (y - z)
r = (x - y) ** 2 - z * z

def coefficient_matrix(polys, degree):
    mons = [x ** a * y ** b * z ** (degree - a - b) for a in range(degree + 1) for b in range(degree - a + 1)]
    return s.Matrix([[s.Poly(v, *vars).coeff_monomial(m) for v in polys] for m in mons])
M0 = coefficient_matrix([p, -q, -r], 2)
M1 = coefficient_matrix([f * l for f in [p, -q, -r] for l in vars], 3)
D0 = smith_normal_form(M0, domain=ZZ)
D1 = smith_normal_form(M1, domain=ZZ)
diag0 = [int(D0[i, i]) for i in range(3)]
diag1 = [int(D1[i, i]) for i in range(9)]
if not sorted((abs(a) for a in diag0)) == [1, 1, 1]:
    raise RuntimeError('Check failed at accepted-source line 18')
if not sorted((abs(a) for a in diag1)) == [0] + [1] * 8:
    raise RuntimeError('Check failed at accepted-source line 19')
v = s.Matrix([-1, 3, -1, 3, -1, -1, -1, 1, 0])
if not M1 * v == s.zeros(10, 1):
    raise RuntimeError('Check failed at accepted-source line 20')
u = -x + 3 * y - z
vv = 3 * x - y - z
if not s.expand(x * u.subs(z, 0) - y * vv.subs(z, 0) + (x + y) * (x - y)) == 0:
    raise RuntimeError('Check failed at accepted-source line 22')
if not s.expand((x - 2 * y + z) * p + x * q - x * r - x * y * z) == 0:
    raise RuntimeError('Check failed at accepted-source line 23')
G = [p, (2 * x * y - x * z - y * z + z * z) / 2, q, x * z * z + y * z * z - z ** 3]
if not s.expand(G[3] - (2 * x * y * z - z * (2 * G[1]))) == 0:
    raise RuntimeError('Check failed at accepted-source line 25')
checks = []
for a, b in combinations(range(4), 2):
    Pa = s.Poly(G[a], *vars, domain=QQ)
    Pb = s.Poly(G[b], *vars, domain=QQ)
    ma = Pa.LM(order='grlex').exponents
    mb = Pb.LM(order='grlex').exponents
    lcm = tuple((max(aa, bb) for aa, bb in zip(ma, mb)))
    multiply = lambda exp: s.prod((vv ** ee for vv, ee in zip(vars, exp)))
    Sp = multiply(tuple((aa - bb for aa, bb in zip(lcm, ma)))) * G[a] - multiply(tuple((aa - bb for aa, bb in zip(lcm, mb)))) * G[b]
    quot, rem = s.reduced(Sp, G, *vars, order='grlex')
    if not rem == 0:
        raise RuntimeError('Check failed at accepted-source line 34')
    denominators = [int(c.q) for pol in quot for c in s.Poly(pol, *vars, domain=QQ).coeffs()]
    if not all((d > 0 and d & d - 1 == 0 for d in denominators)):
        raise RuntimeError('Check failed at accepted-source line 36')
    checks.append({'pair': [a, b], 'remainder': str(rem), 'quotients': [str(e) for e in quot], 'coefficient_denominators': denominators})
standard_dims = []
for d in range(8):
    cnt = sum((1 for a in range(d + 1) for b in range(d - a + 1) if a < 2 and b < 2 and (not (a and b)) and (not (a and d - a - b >= 2))))
    standard_dims.append(cnt)
if not standard_dims == [1, 3, 3, 2, 2, 2, 2, 2]:
    raise RuntimeError('Check failed at accepted-source line 42')
Hquot = (1 + 2 * t - t ** 3) / (1 - t)
HE = s.factor((3 * t * t - 1) / (1 - t) ** 3 + Hquot)
HD = (t + t ** 3 + 2 * t ** 4 - t ** 5) / (1 - t) ** 3
if not s.factor(HE + t / (1 - t) ** 3 - HD) == 0:
    raise RuntimeError('Check failed at accepted-source line 46')
HF = (t + 2 * t ** 3 + t ** 4 - t ** 5) / (1 - t) ** 3
HT = (t + t * t) / (1 - t) ** 2
if not s.factor(HT - HD + t * HF - (t * t + t ** 3)) == 0:
    raise RuntimeError('Check failed at accepted-source line 49')
D4 = (1 + t + t ** 3 + 2 * t ** 4 - t ** 5) / (1 - t) ** 4
F4 = (1 + t + 2 * t ** 3 + t ** 4 - t ** 5) / (1 - t) ** 4
T4 = (1 + t + t * t) / (1 - t) ** 3
if not s.factor(T4 - D4 + t * F4 - (t * t + t ** 3) / (1 - t)) == 0:
    raise RuntimeError('Check failed at accepted-source line 53')
E4 = (1 + 3 * t * t - t ** 3) / (1 - t) ** 4
if not s.factor(T4 - (1 - t) * E4 - t / (1 - t)) == 0:
    raise RuntimeError('Check failed at accepted-source line 55')
a = s.symbols('a:9')
A = s.Matrix(3, 3, a)
conditions = []
for beta in [s.Matrix([[1, 0, 0]]), s.Matrix([[0, 1, 0]]), s.Matrix([[1, -1, 0]]), s.Matrix([[0, 0, 1]])]:
    for w in beta.nullspace():
        conditions.append((beta * A * w)[0])
MC = s.linear_eq_to_matrix(conditions, a)[0]
End_basis = [s.Matrix(3, 3, vv) for vv in MC.nullspace()]
if not len(End_basis) == 2:
    raise RuntimeError('Check failed at accepted-source line 63')
if not all((B[0, 0] == B[1, 1] and all((B[i, j] == 0 for i in range(3) for j in range(3) if i != j)) for B in End_basis)):
    raise RuntimeError('Check failed at accepted-source line 64')
report = {'constant_syzygy_smith_diagonal': diag0, 'linear_syzygy_smith_diagonal': diag1, 'linear_syzygy_generator': list(map(int, v)), 'groebner_S_pairs': checks, 'universal_characteristic_qualification': 'All Groebner quotient denominators are powers of 2; the certificate applies over every field of characteristic not 2.', 'standard_monomial_dimensions_degrees_0_to_7': standard_dims, 'seven_plane_E_Hilbert': str(HE), 'promoted_ordinary_deficit': str(s.factor(T4 - D4 + t * F4)), 'promoted_Ziegler_deficit': str(s.factor(T4 - (1 - t) * E4)), 'promoted_ordinary_End_basis': [[[str(c) for c in B.row(i)] for i in range(3)] for B in End_basis], 'all_passed': True}
print(json.dumps(report, indent=2))
