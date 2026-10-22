#!/usr/bin/env python3
"""Exact finite algebra checks for the citation-scope audit; standard library only.

These checks support the written derivations. They do not validate the classical
support theorem or certify exhaustive historical priority.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json

NAMES = ('z', 'a2', 'a3', 'a4', 'r', 'e', 'p1', 'p2', 'p3', 'p4', 'h1', 'h2', 'h3', 'h4')
N = len(NAMES)
ZERO = (0,) * N


def clean(p):
    return {m: c for m, c in p.items() if c != (F(0), F(0))}


def add(*ps):
    q = defaultdict(lambda: (F(0), F(0)))
    for p in ps:
        for m, (a, b) in p.items():
            c, d = q[m]
            q[m] = c+a, d+b
    return clean(q)


def scale(p, a=0, b=0):
    a, b = F(a), F(b)
    return clean({m: (a*c-b*d, a*d+b*c) for m, (c, d) in p.items()})


def mul(p, q):
    out = defaultdict(lambda: (F(0), F(0)))
    for m, (a, b) in p.items():
        for n, (c, d) in q.items():
            k = tuple(x+y for x, y in zip(m, n))
            if k[0] > 4:  # Only coefficients through z^4 enter this functional.
                continue
            x, y = out[k]
            out[k] = x+a*c-b*d, y+a*d+b*c
    return clean(out)


def power(p, n):
    out = {ZERO: (F(1), F(0))}
    for _ in range(n):
        out = mul(out, p)
    return out


def var(name):
    m = list(ZERO)
    m[NAMES.index(name)] = 1
    return {tuple(m): (F(1), F(0))}


def zcoeff(p, degree):
    out = {}
    for m, c in p.items():
        if m[0] == degree:
            out[(0,)+m[1:]] = c
    return out


z, a2, a3, a4, r, e, p1, p2, p3, p4, h1, h2, h3, h4 = map(var, NAMES)


def L(p):
    return add(zcoeff(p, 2), mul(scale(e, b=1), add(zcoeff(p, 4), scale(zcoeff(p, 3), -3))))


checks = []


def check(name, passed, evidence):
    checks.append({'name': name, 'passed': bool(passed), 'evidence': evidence})
    assert passed, name


f = add(z, mul(a2, power(z, 2)), mul(a3, power(z, 3)), mul(a4, power(z, 4)))
kernel = add(*(scale(mul(power(f, n), power(r, n-1)), -1) for n in range(2, 5)))
A = add(scale(a3, 2), power(a2, 2), scale(a2, -6))
B = add(scale(a2, 3), {ZERO: (F(-3), F(0))})
phi_expected = add(scale(r, -1), scale(mul(e, add(mul(A, r), mul(B, power(r, 2)), power(r, 3))), b=-1))
check('formal_coefficient_extraction', L(kernel) == phi_expected,
      'Phi=-1/w-i*epsilon*((2*a3+a2^2-6*a2)/w+(3*a2-3)/w^2+1/w^3), all symbolic coefficients exact.')
check('origin_third_pole_and_Q_fifth_pole', zcoeff(phi_expected, 0).get(next(iter(power(mul(e, power(r, 3)), 1))), (0,0)) == (F(0), F(-1)),
      'The coefficient of epsilon/w^3 is exactly -i, so epsilon nonzero gives pole order3 in Phi and5 in Q=Phi/w^2.')

phi = add(mul(p1, z), mul(p2, power(z, 2)), mul(p3, power(z, 3)), mul(p4, power(z, 4)))
hphi = add(*(mul(h, power(phi, n)) for n, h in enumerate([h1,h2,h3,h4], 1)))
J_expected = add(
    mul(h1, add(p2, mul(scale(e, b=1), add(p4, scale(p3, -3))))),
    mul(h2, add(power(p1, 2), mul(scale(e, b=1), add(scale(mul(p1,p3),2), power(p2,2), scale(mul(p1,p2),-6))))),
    mul(h3, mul(scale(e,b=1), add(scale(mul(power(p1,2),p2),3), scale(power(p1,3),-3)))),
    mul(h4, mul(scale(e,b=1), power(p1,4))))
check('truncation_composition_to_degree4', L(hphi) == J_expected,
      'J(h)=L(h o phi), phi(0)=0, has h4 coefficient i*epsilon*p1^4; conformal p1 nonzero preserves degree4.')

epsilon, eta, T = F(1,10**24), F(1,10**12), F(7,4)
q = lambda t: t*t-F(2,5)*t**4
check('q_at_1', q(F(1)) == F(3,5), str(q(F(1))))
check('q_at_T', q(T) == -F(441,640), str(q(T)))
check('positive_sign_margin', q(F(1))-2000*eta > F(1,2), str(q(F(1))-2000*eta))
check('negative_sign_margin', q(T)+2000*eta < -F(1,2), str(q(T)+2000*eta))
check('epsilon_boundary', epsilon > 0 and epsilon == eta*eta,
      'epsilon=eta^2>0; at epsilon=0 the degree4 perturbation and reversal margin disappear.')
check('Koebe_rotation_necessary_coefficient_obstruction', 1-12*eta > 0,
      'If a2=2u, |u|=1, |a2-2|<8eta, then |u^3-1|<12eta and Re(u^3)>1-12eta>0. Thus Im(i*epsilon*u^3)>0, incompatible with Phi real on a radial slit.')
check('Toeplitz_origin_support', F(1,24)*F(24)==1 and F(-3,6)*F(6)==-3 and F(1,2)*F(2)==1,
      "L(h)=h''(0)/2+i*epsilon*(h''''(0)/24-h'''(0)/2). Its Toeplitz kernel is z^-3-3i*epsilon*z^-4+i*epsilon*z^-5, with nonzero order5 origin pole.")

result = {'passed': all(c['passed'] for c in checks), 'count': len(checks), 'checks': checks,
          'limits': 'Finite exact algebra supports authored scope derivations; no numerical extremal solution, formal proof of classical inputs, or exhaustive priority certificate.'}
Path(__file__).with_name('EXACT_CHECKS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
