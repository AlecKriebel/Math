#!/usr/bin/env python3
"""Exact finite algebra checks; the analytic proofs remain in PROOF.md."""
from fractions import Fraction as F
import json


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i+j] += x*y
    return out


def derivative(p):
    return [i*p[i] for i in range(1, len(p))]


def evaluate(p, x):
    ans = F(0)
    for c in reversed(p):
        ans = ans*x+c
    return ans


def add(x, y):
    return (x[0]+y[0], x[1]+y[1])


def neg(x):
    return (-x[0], -x[1])


def cmul(x, y):
    return (x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0])


def scale(x, r):
    return (r*x[0], r*x[1])


def abs2(x):
    return x[0]**2+x[1]**2


def divide(x, y):
    return scale(cmul(x, (y[0], -y[1])), 1/abs2(y))


def cpoly(p, z):
    ans = (F(0), F(0))
    for c in reversed(p):
        ans = add(cmul(ans, z), (c, F(0)))
    return ans


roots = [F(1, 2), F(3, 4), F(-1, 3)]
p = [F(0), F(0), F(1)]
for a in roots:
    p = mul(p, [-a, F(1)])
assert p[:2] == [0, 0]
assert all(evaluate(p, a) == 0 for a in roots)
M = sum(abs(c) for c in derivative(p))
epsilon = 1/(2*M)
assert epsilon*M == F(1, 2)

# a_n = 1 - 2^-n; exact infinite geometric series formulas.
S = 2*F(1, 2)/(1-F(1, 2))-F(1, 4)/(1-F(1, 4))
E = 4*S
bound = 12+E
assert (S, E, bound) == (F(5, 3), F(20, 3), F(56, 3))
assert F(3, 112)*bound == F(1, 2)

# Exact checks on rational points are regression controls, not infinite proofs.
one = (F(1), F(0))
P = [F(0), F(0), F(1), F(-2), F(1)]
DP = derivative(P)
aset = [1-F(1, 2**n) for n in range(1, 7)]
EN = 4*sum(1-a*a for a in aset)
points = 0
for ix in range(-6, 7):
    for iy in range(-6, 7):
        z = (F(ix, 7), F(iy, 7))
        if abs2(z) >= 1:
            continue
        B, DB = one, (F(0), F(0))
        for a in aset:
            denominator = add(one, scale(z, -a))
            numerator = add((a, F(0)), neg(z))
            b = divide(numerator, denominator)
            db = divide((-(1-a*a), F(0)), cmul(denominator, denominator))
            DB = add(cmul(DB, b), cmul(B, db))
            B = cmul(B, b)
            assert abs2(add(one, neg(z))) <= 4*abs2(denominator)
        HP = add(cmul(cpoly(DP, z), B), cmul(cpoly(P, z), DB))
        assert abs2(HP) <= (12+EN)**2
        assert abs2(scale(HP, F(3, 112))) < F(1, 4)
        points += 1

small_norm = []
for k in [2, 3, 5, 10]:
    N = k**4
    c = F(1, k**3)
    # q' numerator for q=z/(1+c*z^(N+1)) is 1-N*c*z^(N+1).
    assert N*c == k
    energy = N*c*c
    assert energy == F(1, k*k)
    assert c < 1 and N*c > 1
    # Positive root is k^(-1/(N+1)), strictly between 0 and 1.
    small_norm.append({'k':k,'N':N,'sup_h':str(c),'dirichlet_energy':str(energy),
                       'derivative_numerator_coefficient':str(N*c)})

# Explicit finite-interpolation collapse budgets.
assert all(F(1, 2**N) < 1 for N in range(1, 20))

print(json.dumps({
  'result':'PASS',
  'arithmetic':'fractions.Fraction; no floating point or third-party package',
  'finite_polynomial_coefficients':[str(c) for c in p],
  'finite_polynomial_M':str(M),
  'finite_polynomial_epsilon':str(epsilon),
  'infinite_radial_exact_constants':{'sum_one_minus_a_squared':str(S),
      'E':str(E),'derivative_bound':str(bound),'epsilon':'3/112'},
  'finite_product_rational_grid_points':points,
  'finite_product_degree':len(aset),
  'small_dirichlet_nonunivalence_controls':small_norm,
  'limitations':[
    'Finite computations do not establish the full characterization.',
    'Infinite product convergence, injectivity and necessary conditions are analytic proofs in PROOF.md.',
    'The rational grid is a regression test, not a domain-wide certificate.'
  ]
}, indent=2, sort_keys=True))
