#!/usr/bin/env python3
"""Exact polynomial checks for a local model; not a proof of KP-1.65."""
import json
from fractions import Fraction

# Polynomials in (s,u), represented by exponent-pair to rational coefficient.
def clean(p):
    return {k: Fraction(v) for k, v in p.items() if v != 0}

def add(a, b):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, Fraction(0)) + v
    return clean(r)

def scale(a, c):
    return clean({k: c*v for k, v in a.items()})

def sub(a, b):
    return add(a, scale(b, -1))

def mul(a, b):
    r = {}
    for (i,j), v in a.items():
        for (k,l), w in b.items():
            e = (i+k,j+l)
            r[e] = r.get(e, Fraction(0)) + v*w
    return clean(r)

def derivative(p, variable):
    r = {}
    for exponent, coefficient in p.items():
        degree = exponent[variable]
        if degree:
            new = list(exponent)
            new[variable] -= 1
            r[tuple(new)] = degree*coefficient
    return clean(r)

ONE = {(0,0): Fraction(1)}
S = {(1,0): Fraction(1)}
U = {(0,1): Fraction(1)}
ZERO = {}

def contact_pullback(y, z):
    # x=u; alpha=dz-y dx. Return the (ds,du) coefficients.
    return derivative(z, 0), sub(derivative(z, 1), y)

def omega_coefficient(a, b):
    # d(exp(s)*(a ds+b du))/exp(s), coefficient of ds wedge du.
    return sub(add(derivative(b, 0), b), derivative(a, 1))

def require(condition, label):
    if not condition:
        raise RuntimeError('FAIL: ' + label)


def main():
    tests = []
    def check(condition, label):
        require(condition, label)
        tests.append(label)

    check(derivative(mul(S,U),0)==U, 'polynomial derivative in s')
    check(derivative(mul(S,U),1)==S, 'polynomial derivative in u')
    check(sub(ONE,ONE)==ZERO, 'normalization removes zero terms')
    a,b = contact_pullback(S, mul(add(S,ONE),U))
    check(a==U and b==ONE, 'local contact pullback is u ds plus du')
    check(omega_coefficient(a,b)==ZERO, 'local pullback of omega vanishes')
    # f=exp(s)*U, so f_s/exp(s)=U+U_s and f_u/exp(s)=U_u.
    check(a==add(U,derivative(U,0)), 'primitive derivative in s')
    check(b==derivative(U,1), 'primitive derivative in u')
    check(b!=ZERO, 'height slices fail the Legendrian tangent condition')
    check(derivative(S,0)==ONE and derivative(S,1)==ZERO,
          'height differential is ds and has no critical points')
    # Generic family y=A*s, z=B*s*u+C*u is Lagrangian iff A=B=C.
    for av in range(-2,3):
        for bv in range(-2,3):
            for cv in range(-2,3):
                aa,bb=contact_pullback(scale(S,av),
                     mul(add(scale(S,bv),scale(ONE,cv)),U))
                closed=omega_coefficient(aa,bb)==ZERO
                check(closed==(av==bv==cv),
                      'family parameters '+str((av,bv,cv)))
    # The guard must reject failures even when Python optimization is enabled.
    rejected=False
    try:
        require(False,'deliberate negative control')
    except RuntimeError:
        rejected=True
    check(rejected,'false premise is rejected')
    print(json.dumps({'status':'PASS','checks':len(tests),
          'scope':'local polynomial differential identities only',
          'problem_2724_solved':False},sort_keys=True))

if __name__=='__main__':
    main()
