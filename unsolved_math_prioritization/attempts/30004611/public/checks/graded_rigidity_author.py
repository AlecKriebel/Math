#!/usr/bin/env python3
# Reader edition: explicit runtime checks; results go only to stdout.
"""Authored exact and finite controls; no external source program is executed."""
import json, hashlib
from pathlib import Path
import sympy as s
x, y, z, t = s.symbols('x y z t')
p = x * (x - z)
q = y * (y - z)
r = (x - y) ** 2 - z * z
G = [x * x - x * z, x * y - (x * z + y * z - z * z) / 2, y * y - y * z, x * z * z + y * z * z - z ** 3]
GB = s.groebner(G, x, y, z, order='grlex', domain=s.QQ)
if not all((GB.reduce(f)[1] == 0 for f in [p, q, r])):
    raise RuntimeError('Check failed at accepted-source line 9')
if not all((s.groebner([p, q, r], x, y, z, order='grlex', domain=s.QQ).reduce(f)[1] == 0 for f in G)):
    raise RuntimeError('Check failed at accepted-source line 10')
S_checks = []
for i in range(len(G)):
    for j in range(i):
        fi = s.Poly(G[i], x, y, z, domain=s.QQ)
        fj = s.Poly(G[j], x, y, z, domain=s.QQ)
        mi, ci = fi.terms(order='grlex')[0]
        mj, cj = fj.terms(order='grlex')[0]
        lcm = tuple((max(a, b) for a, b in zip(mi, mj)))
        mono = lambda es: s.prod((v ** e for v, e in zip((x, y, z), es)))
        spol = mono(tuple((a - b for a, b in zip(lcm, mi)))) * G[i] / ci - mono(tuple((a - b for a, b in zip(lcm, mj)))) * G[j] / cj
        rem = s.reduced(spol, G, x, y, z, order='grlex')[1]
        if not rem == 0:
            raise RuntimeError((i, j, rem))
        S_checks.append([j, i, str(rem)])
u = -x + 3 * y - z
v = 3 * x - y - z
h = -x + y
if not s.expand(p * u - q * v - r * h) == 0:
    raise RuntimeError('Check failed at accepted-source line 24')
if not s.cancel((x * u - y * v).subs(z, 0) / (x - y)) == -(x + y):
    raise RuntimeError('Check failed at accepted-source line 25')
if not s.cancel((p * q / x - p * q / y).subs(z, 0) / (x - y)) == -x * y:
    raise RuntimeError('Check failed at accepted-source line 26')
H_D = t + t ** 3 + 2 * t ** 4 - t ** 5
H_F = t + 2 * t ** 3 + t ** 4 - t ** 5
ordinary = s.factor(((1 + t + t * t) * (1 - t) - (1 + H_D) + t * (1 + H_F)) / (1 - t) ** 4)
ziegler = s.factor((1 + t + t * t - (1 + 3 * t * t - t ** 3)) / (1 - t) ** 3)
if not s.cancel(ordinary - (t * t + t ** 3) / (1 - t)) == 0:
    raise RuntimeError('Check failed at accepted-source line 31')
if not s.cancel(ziegler - t / (1 - t)) == 0:
    raise RuntimeError('Check failed at accepted-source line 32')

def exps(d, n):
    if n == 1:
        return [(d,)]
    return [(a,) + e for a in range(d + 1) for e in exps(d - a, n - 1)]

def rankmod(A, p):
    A = [[a % p for a in r] for r in A]
    r = 0
    if not A:
        return 0
    for c in range(len(A[0])):
        pivot = next((k for k in range(r, len(A)) if A[k][c]), None)
        if pivot is None:
            continue
        A[r], A[pivot] = (A[pivot], A[r])
        inv = pow(A[r][c], -1, p)
        A[r] = [a * inv % p for a in A[r]]
        for k in range(r + 1, len(A)):
            if A[k][c]:
                a = A[k][c]
                A[k] = [(b - a * cc) % p for b, cc in zip(A[k], A[r])]
        r += 1
        if r == len(A):
            break
    return r

def dim_der(forms, d, prime, kill_z=False):
    mons = exps(d, 3)
    polys = [x ** a * y ** b * z ** c for a, b, c in mons]
    coords = (x, y) if kill_z else (x, y, z)
    cols = len(polys) * len(coords)
    rows = []
    for f in forms:
        normal = [int(s.diff(f, w)) for w in (x, y, z)]
        k = next((k for k, a in enumerate(normal) if a % prime))
        vars2 = [w for i, w in enumerate((x, y, z)) if i != k]
        replacement = -sum((normal[i] * pow(normal[k] % prime, -1, prime) % prime * w for i, w in enumerate((x, y, z)) if i != k))
        keys = exps(d, 2)
        idx = {a: i for i, a in enumerate(keys)}
        block = [[0] * cols for _ in keys]
        for j, w in enumerate(coords):
            norm = normal[(x, y, z).index(w)] % prime
            if not norm:
                continue
            for b, poly in enumerate(polys):
                pp = s.Poly(s.expand(poly.subs((x, y, z)[k], replacement)), *vars2)
                for mon, coeff in pp.terms():
                    if coeff:
                        block[idx[mon]][j * len(polys) + b] = norm * int(coeff) % prime
        rows += block
    return cols - rankmod(rows, prime)
forms = [z, x, y, x - z, y - z, x - y + z, x - y - z]
checks = []
for prime in (3, 5, 7):
    for d in range(7):
        dimD = dim_der(forms, d, prime)
        dimF = dim_der(forms[1:], d, prime)
        predD = int(s.expand(s.series(H_D / (1 - t) ** 3, t, 0, 7).removeO()).coeff(t, d))
        predF = int(s.expand(s.series(H_F / (1 - t) ** 3, t, 0, 7).removeO()).coeff(t, d))
        if not (dimD, dimF) == (predD, predF):
            raise RuntimeError((prime, d, dimD, dimF, predD, predF))
        checks.append({'field': f'F{prime}', 'degree': d, 'dim_D': dimD, 'dim_F': dimF})
result = {'all_checks_pass': True, 'groebner_S_polynomial_remainders': S_checks, 'ordinary_promoted_discrepancy': str(ordinary), 'ziegler_promoted_discrepancy': str(ziegler), 'finite_controls': checks, 'scope': 'Controls supplement the symbolic all-degree proofs; no novelty or independent acceptance claim.'}
print(json.dumps(result, indent=2))
