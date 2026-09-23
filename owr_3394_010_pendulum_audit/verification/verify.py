#!/usr/bin/env python3
"""Exact algebra audit, Python 3 standard library only.

This checks polynomial identities, not the imported dynamical-systems theorem,
measure-zero arguments, source priority, or all input signals by simulation.
Variables are w=omega, s=sin(theta), c=cos(theta), d=input, l=eigenvalue.
Trigonometric equalities are reduced modulo s**2+c**2-1.
"""
from fractions import Fraction as F
import json


class P:
    """Small sparse rational polynomial, with explicit coefficient equality."""
    def __init__(self, terms=0):
        if isinstance(terms, P):
            terms = terms.terms
        if not isinstance(terms, dict):
            terms = {(0, 0, 0, 0, 0): F(terms)}
        self.terms = {k: F(v) for k, v in terms.items() if v}

    def __add__(self, other):
        result = dict(self.terms)
        for k, v in P(other).terms.items():
            result[k] = result.get(k, 0) + v
        return P(result)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        result = {}
        for a, u in self.terms.items():
            for b, v in P(other).terms.items():
                k = tuple(x + y for x, y in zip(a, b))
                result[k] = result.get(k, 0) + u*v
        return P(result)

    __rmul__ = __mul__

    def __pow__(self, n):
        result = P(1)
        for _ in range(n):
            result = result*self
        return result

    def diff(self, i):
        result = {}
        for k, v in self.terms.items():
            if k[i]:
                e = list(k)
                e[i] -= 1
                result[tuple(e)] = v*k[i]
        return P(result)

    def circle_reduce(self):
        result = P(0)
        for k, v in self.terms.items():
            e = list(k)
            e[1] = k[1] % 2
            result += P({tuple(e): v}) * (1-c*c)**(k[1]//2)
        return result


w, s, c, d, lam = [P({tuple(int(i == j) for i in range(5)): 1})
                    for j in range(5)]
checks = []


def equal(name, left, right, circle=False):
    difference = P(left)-right
    if circle:
        difference = difference.circle_reduce()
    if difference.terms:
        raise AssertionError((name, difference.terms))
    checks.append(name)


def lie(poly, forced=True):
    # s_dot=c*w, c_dot=-s*w, w_dot=-s-w+d; d is not differentiated.
    return (poly.diff(0)*(-s-w+(d if forced else 0))
            + poly.diff(1)*c*w - poly.diff(2)*s*w)


H = F(1, 2)*w*w + 1-c
V = H + F(1, 2)*w*s
equal("circle reduction", s*s+c*c, 1, circle=True)
equal("lower bound V >= H/2", V-F(1, 2)*H,
      F(1, 4)*(w+s)**2+F(1, 4)*(1-c)**2, circle=True)
equal("upper bound V <= 3H/2", F(3, 2)*H-V,
      F(1, 4)*(w-s)**2+F(1, 4)*(1-c)**2, circle=True)
equal("forced mechanical energy derivative", lie(H), -w*w+w*d)
equal("strict unforced Lyapunov certificate", -lie(V, False),
      F(1, 4)*(w*w+s*s)+F(1, 4)*(w+s)**2+F(1, 2)*(1-c)*w*w)
equal("forced comparison inequality certificate",
      -F(1, 2)*H+1+F(1, 2)*d*d-lie(H),
      F(1, 2)*(w-d)**2+F(1, 4)*w*w+F(1, 2)*(1+c))
f_theta, f_omega = w, -s-w+d
a11 = f_theta.diff(1)*c-f_theta.diff(2)*s
a12 = f_theta.diff(0)
a21 = f_omega.diff(1)*c-f_omega.diff(2)*s
a22 = f_omega.diff(0)
characteristic = (lam-a11)*(lam-a22)-a12*a21
equal("state characteristic polynomial", characteristic, lam*lam+lam+c)
equal("downward characteristic polynomial", characteristic-c+1, lam*lam+lam+1)
equal("upright characteristic polynomial", characteristic-c-1, lam*lam+lam-1)
equal("state divergence", a11+a22, -1)
# Reject at least one deliberately wrong certificate (avoid vacuous checking).
try:
    equal("negative control", lie(H), -2*w*w+w*d)
except AssertionError:
    checks.append("negative control rejected")
else:
    raise AssertionError("Incorrect identity was accepted")

print(json.dumps({
    "status": "PASS", "exact_checks": len(checks), "checks": checks,
    "inequality_conditions": "w,s,c,d real; s^2+c^2=1, hence -1<=c<=1",
    "scope": "Algebra only; read AUDIT.md for analytic proof and imported theorem."
}, indent=2))
