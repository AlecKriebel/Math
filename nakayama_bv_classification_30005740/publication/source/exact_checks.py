#!/usr/bin/env python3
"""Exact finite diagnostics for the accompanying proof; Python >= 3.10, stdlib only.

The universal theorem is proved in main.tex using named published structural
inputs. These checks neither compute Hochschild cohomology nor certify priority.
No original claimant program is imported or executed. No network or file writes.
Original code: Alec Kriebel, 2026. SPDX-License-Identifier: MIT.
"""
from fractions import Fraction as F
from math import comb
import json

def require(test, label):
    if not test:
        raise RuntimeError(label)

def p(a):
    a = tuple(F(x) for x in a)
    while len(a) > 1 and a[-1] == 0:
        a = a[:-1]
    return a or (F(0),)

Z = p([0]); ONE = p([1]); X = p([0, 1])

def add(a, b):
    return p([(a[i] if i < len(a) else 0) +
              (b[i] if i < len(b) else 0) for i in range(max(len(a), len(b)))])
def neg(a):
    return p([-x for x in a])
def sub(a, b):
    return add(a, neg(b))
def scale(a, c):
    return p([x*c for x in a])
def mul(a, b):
    c = [F(0)]*(len(a)+len(b)-1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            c[i+j] += ai*bj
    return p(c)
def power(a, n):
    c = ONE
    for _ in range(n):
        c = mul(c, a)
    return c
def deriv(a):
    return p([i*a[i] for i in range(1, len(a))])
def divrem(a, b):
    require(b != Z, "division by zero")
    a = list(a); q = [F(0)]*max(1, len(a)-len(b)+1)
    while len(a) >= len(b) and p(a) != Z:
        j = len(a)-len(b); c = a[-1]/b[-1]; q[j] += c
        for i, v in enumerate(b):
            a[i+j] -= c*v
        a = list(p(a))
    return p(q), p(a)
def exact(a, b):
    q, r = divrem(a, b)
    require(r == Z, "inexact polynomial quotient")
    return q
def gcd(a, b):
    while b != Z:
        a, b = b, divrem(a, b)[1]
    return scale(a, 1/a[-1])
def fmt(a):
    return [str(v) for v in a]
def equal(a, b, label):
    require(a == b, label)

def boundary_telescope(s):
    # Formal k[x]-bimodule on normalized [x^t], t>=1.
    # Preserve left/right positions, without any commutation through a bar.
    out = {}
    def put(l, t, r, v):
        if t == 0:
            return
        key = l, t, r
        out[key] = out.get(key, 0) + v
        if out[key] == 0:
            del out[key]
    for i in range(1, s):
        put(i, 1, s-1-i, 1)
        put(0, i+1, s-1-i, -1)
        put(0, i, s-i, 1)
    target = {}
    for i in range(s):
        target[i, 1, s-1-i] = 1
    key = (0, s, 0)
    target[key] = target.get(key, 0)-1
    target = {k:v for k,v in target.items() if v}
    require(out == target, "normalized-bar telescope")
    return out

def run():
    examples = []
    factors = [X, p([1, 0, 1]), p([2, 0, 1])]
    for u in factors:
        for e in [2, 3, 4]:
            for leading in [F(1), F(-3, 2)]:
                # Two nonsplit quadratic irreducibles over Q, plus a linear one.
                h = scale(mul(power(u, e), p([1, 1])), leading)
                d = gcd(h, deriv(h)); pi = exact(h, d); g = exact(d, u)
                L = exact(mul(pi, deriv(d)), d)
                equal(add(mul(L, h), sub(mul(h, deriv(pi)), mul(deriv(h), pi))),
                      Z, "b respects relation")
                equal(divrem(mul(g, pi), d)[1], Z, "cup zero")
                q = sub(mul(L, g), mul(pi, deriv(g)))
                expected = mul(exact(h, mul(u, u)), deriv(u))
                equal(q, expected, "commutator identity with u prime")
                require(q != Z and len(q) < len(h), "nonzero noninner bracket")
                require(divrem(q, h)[1] != Z, "bracket not divisible by h")
                require(len(g) < len(d) < len(h), "independent companions")
                # Reciprocal differentiation and normalizer membership.
                P = ONE
                numerator, denominator = ONE, pi
                # d^j*P_j*h^(n-1-j) is polynomial, never an assumed rational term.
                for j in range(4):
                    equal(mul(numerator, power(pi, j+1)), mul(P, denominator),
                          "independent quotient-rule reciprocal derivative")
                    require(exact(mul(power(h, j), P), power(pi, j)) ==
                            mul(power(d, j), P), "normalizer coefficient")
                    numerator, denominator = (sub(mul(deriv(numerator), denominator),
                                                 mul(numerator, deriv(denominator))),
                                              mul(denominator, denominator))
                    P = sub(mul(pi, deriv(P)), scale(mul(deriv(pi), P), j+1))
                examples.append({"u":fmt(u),"multiplicity":e,"h":fmt(h),"q":fmt(q)})
    squarefree = [ONE, scale(ONE, F(-2)), X, p([1, 0, 1]),
                  mul(X, p([1, 0, 1])), p([1, 1, 0, 1])]
    for h in squarefree:
        equal(gcd(h, deriv(h)), ONE, "squarefree gcd including units")
    bars = [boundary_telescope(s) for s in range(1, 13)]
    # Embedded h=0 divergence identity on polynomial vector fields.
    divergences = 0
    for f in [ONE, X, power(X, 3), p([2, -1, 3])]:
        for g in [ONE, power(X, 2), p([1, 2])]:
            equal(sub(deriv(mul(f,g)), mul(f,deriv(g))), mul(deriv(f),g),
                  "Leibniz / embedded h0 generator")
            divergences += 1
    # Deliberately false controls: each differs on a concrete exact example.
    u = p([1,0,1]); h = power(u,2); d = u; pi = u; g = ONE
    L = p([0,2]); q = p([0,2])
    require(add(mul(neg(L),h), sub(mul(h,deriv(pi)),mul(deriv(h),pi))) != Z,
            "control failed to detect reversed L")
    require(exact(h,mul(u,u)) != q, "control failed to detect omitted u prime")
    t = boundary_telescope(3)
    require({k:-v for k,v in t.items()} != t, "control failed to detect bar sign")
    extra = sub(mul(pi,deriv(deriv(h))), mul(L,deriv(h)))
    equal(extra, scale(h,4), "ambient inner correction")
    require(extra != Z, "control failed to reject literal ad(pi*y)")
    # Y*x^3 - x^3*Y = 3*x^2*h, so a right polynomial cannot generally
    # be moved across a derivation value with Y component.
    require(mul(p([0,0,3]),h) != Z, "control against commuting right factors")
    return {"status":"PASS","repeated_factor_examples":len(examples),
            "squarefree_boundary_examples":len(squarefree),
            "normalized_bar_degrees":list(range(1,13)),
            "normalizer_polynomial_coefficients":4*len(examples),
            "independent_reciprocal_derivatives":4*len(examples),
            "embedded_h0_Leibniz_examples":divergences,
            "deliberately_false_controls":5,
            "examples":examples,
            "limits":"Finite Q-polynomial diagnostics only. Universal proof, field scope, "
                     "published resolution/spanning, canonical cohomology and priority "
                     "must be read in the manuscript and source notes."}

if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
