#!/usr/bin/env python3
"""Independent exact controls; imports no implementation from the audited payload."""
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter
import json

counts = Counter()
def check(name, value):
    assert value, name
    counts[name] += 1

def identity():
    return [[F(i == j) for j in range(4)] for i in range(4)]
def transpose(a):
    return list(map(list, zip(*a)))
def mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
def inv(a):
    a = [list(map(F, row)) + identity()[i] for i, row in enumerate(a)]
    for j in range(4):
        k = next(k for k in range(j, 4) if a[k][j])
        a[k], a[j] = a[j], a[k]
        z = a[j][j]
        a[j] = [x/z for x in a[j]]
        for k in range(4):
            if k != j:
                z = a[k][j]
                a[k] = [a[k][i]-z*a[j][i] for i in range(8)]
    return [row[4:] for row in a]
def pull(f, a):
    return mul(transpose(f), mul(a, f))
def form(values):
    a = [[F(0) for j in range(4)] for i in range(4)]
    for (i,j), value in zip(combinations(range(4), 2), values):
        a[i][j], a[j][i] = F(value), -F(value)
    return a
def wedge(a, b):
    # Generic exterior multiplication by index disjointness and permutation sign.
    ans = F(0)
    for i,j in combinations(range(4), 2):
        for k,l in combinations(range(4), 2):
            indices = (i,j,k,l)
            if len(set(indices)) == 4:
                parity = sum(indices[u] > indices[v] for u in range(4) for v in range(u+1,4))
                ans += (-1)**parity * a[i][j] * b[k][l]
    return ans

def positive_minimum(A,B,C):
    quadratic, linear = A-2*B+C, 2*(B-A)
    minimum = min(A,C)
    if quadratic > 0:
        t = -linear/(2*quadratic)
        if 0 < t < 1:
            minimum = min(minimum, quadratic*t*t+linear*t+A)
    return minimum > 0

values = sorted({F(n,d) for n in range(1,9) for d in range(1,4)})
for A,C in product(values, repeat=2):
    for B in (F(k,2) for k in range(-32,33)):
        check('affine_rational_minimum', positive_minimum(A,B,C) == (B >= 0 or A*C > B*B))
for p,q in product(range(1,13), repeat=2):
    A,B,C = F(p*p), F(-p*q), F(q*q)
    t = F(p,p+q)
    check('affine_unequal_endpoint_equality', A*(1-t)**2+2*B*t*(1-t)+C*t*t == 0)
    check('affine_boundary_rejected', not positive_minimum(A,B,C))

omega = form((1,0,0,0,0,1))
R = identity()
R[1][1] = R[3][3] = -1
check('half_turn_pullback', pull(R,omega) == [[-v for v in row] for row in omega])
check('half_turn_volume', wedge(pull(R,omega),pull(R,omega)) == wedge(omega,omega) == 2)

# Noncommuting invertible examples make composition order observable.
matrices = []
for seed in range(1,13):
    m = identity()
    for u in range(6):
        i, j = (seed+u)%4, (seed+u+1+(u%2))%4
        if i == j:
            j = (j+1)%4
        shear = identity()
        shear[i][j] = F((seed+2*u)%7-3)
        m = mul(shear, m)
    matrices.append(m)
wrong_order_failures = 0
for fi,fj in product(matrices, repeat=2):
    h = mul(inv(fj), fi)
    check('noncommuting_pullback_order', pull(h,pull(fj,omega)) == pull(fi,omega))
    wrong = mul(fi, inv(fj))
    wrong_order_failures += pull(wrong,pull(fj,omega)) != pull(fi,omega)
check('wrong_order_negative_control', wrong_order_failures > 0)

for a,b in product(product(range(-2,3),repeat=3), repeat=2):
    m = form((a[0],a[1],a[2],b[2],-b[1],b[0]))
    check('torus_generic_exterior_product', wedge(m,m) == 2*sum(x*y for x,y in zip(a,b)))

print(json.dumps({'all_checks_passed':True, 'assertions':sum(counts.values()),
                  'groups':dict(sorted(counts.items())),
                  'wrong_order_failures_detected':wrong_order_failures,
                  'scope':'Independent finite exact controls only; no classification or theorem certification.'},indent=2,sort_keys=True))
