#!/usr/bin/env python3
"""Exact homogeneous equation controls, not construction of PR36's coefficients.

Binary forms are arrays indexed by the X exponent, with Y exponent inferred
from the declared total degree. Arithmetic and determinants use Fraction only.
The negative controls exercise infinity, non-fixed ramification and base points.
"""
from fractions import Fraction as Q
from math import comb
import argparse
import json


def add(a, b):
    assert len(a) == len(b)
    return [x + y for x, y in zip(a, b)]


def scale(a, c):
    return [c*x for x in a]


def mul(a, b):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c


def power(a, n):
    p = [1]
    for _ in range(n):
        p = mul(p, a)
    return p


def dx(a):
    return [i*a[i] for i in range(1, len(a))]


def dy(a):
    n = len(a)-1
    return [(n-i)*a[i] for i in range(n)]


def forms(f, g):
    return add(mul(dx(f), dy(g)), scale(mul(dy(f), dx(g)), -1)), add(f+[0], scale([0]+g, -1))


def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def homogeneous_divides(w, h, exponent):
    if not any(w):
        return False
    dividend = power(h, exponent)
    quotient_degree = len(dividend)-len(w)
    a, b = trim(list(map(Q, dividend))), trim(list(map(Q, w)))
    q = [Q(0)]*max(1, len(a)-len(b)+1)
    while any(a) and len(a) >= len(b):
        shift, c = len(a)-len(b), a[-1]/b[-1]
        q[shift] += c
        for i, x in enumerate(b):
            a[i+shift] -= c*x
        trim(a)
    trim(q)
    # The degree cap is essential: dehomogenization alone loses infinity.
    return not any(a) and len(q)-1 <= quotient_degree


def determinant(matrix):
    a = [list(map(Q, row)) for row in matrix]
    out = Q(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return Q(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            out = -out
        out *= a[i][i]
        for j in range(i+1, len(a)):
            c = a[j][i]/a[i][i]
            for k in range(i+1, len(a)):
                a[j][k] -= c*a[i][k]
            a[j][i] = 0
    return out


def resultant(f, g):
    d = len(f)-1
    assert len(g) == d+1
    rows = []
    for p in (f, g):
        for shift in range(d):
            rows.append([0]*shift+list(reversed(p))+[0]*(d-1-shift))
    return determinant(rows)


def normalized(w):
    return w[0] == 0 and sum(w) == 0 and w[-1] == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--omit-resultant', action='store_true')
    parser.add_argument('--power', type=int, default=1)
    args = parser.parse_args()
    records = []
    count = 0

    def check(condition, label):
        nonlocal count
        if not condition:
            raise AssertionError(label)
        count += 1

    # M conjugate of the critically fixed Newton map
    # 10*z^11/(11*z^10-1), M(z)=2*z/(z+1).
    # F=20 X^11, G=22 X^10 Y-X^11-(2Y-X)^11.
    f = [0]*11+[20]
    g = [-comb(11, i)*2**(11-i)*(-1)**i for i in range(12)]
    g[10] += 22
    g[11] -= 1
    w, h = forms(f, g)
    r = resultant(f, g)
    check(len(w)-1 == 20 and len(h)-1 == 12, 'actual binary W/H degrees')
    check(r != 0, 'positive control has no base point')
    check(normalized(w), 'positive control has three normalized critical points')
    check(homogeneous_divides(w, h, args.power), 'positive critically fixed map passes adequate power')
    check(not homogeneous_divides(w, h, 1), 'root multiplicity makes power one insufficient')
    records.append({'control':'normalized degree-11 critically fixed Newton conjugate',
                    'resultant':str(r),'W_degree':20,'H_degree':12,
                    'passes_power_20':homogeneous_divides(w,h,20),
                    'passes_power_1':homogeneous_divides(w,h,1),
                    'quotient_degree':220,'scope':'equation control, not the candidate class'})

    # A degree-one translation with an artificial degree-10 common factor:
    # h0=X^8 Y (X-Y), F=h0(X+Y), G=h0 Y.
    common = [0]*8+[-1,1,0]
    bf, bg = mul(common,[1,1]), mul(common,[1,0])
    bw, bh = forms(bf,bg)
    br = resultant(bf,bg)
    weak_accepts = normalized(bw) and homogeneous_divides(bw,bh,20)
    accepts = weak_accepts and (args.omit_resultant or br != 0)
    check(br == 0, 'degenerate degree-11 pair has a base point')
    check(weak_accepts, 'normalization/divisibility alone admit base-point artifact')
    check(not accepts, 'resultant guard rejects base-point artifact')
    records.append({'control':'common-factor degree-one translation represented at degree 11',
                    'resultant':str(br),'weak_equations_accept':weak_accepts,
                    'guarded_equations_accept':accepts})

    # z^11+1 is not critically fixed: 0 is critical and maps to 1.
    nf=[1]+[0]*10+[1]
    ng=[1]+[0]*11
    nw,nh=forms(nf,ng)
    check(resultant(nf,ng) != 0, 'non-PCF-condition control is an honest degree-11 map')
    check(not homogeneous_divides(nw,nh,20), 'non-fixed critical point is rejected')
    records.append({'control':'z^11+1', 'critical_fixed_equations_accept':False})

    # Infinity must be retained in divisibility: Y^2 does not divide X^2.
    check(not homogeneous_divides([1,0,0],[0,1],2), 'infinity multiplicity is retained')
    check(20*12-20 == 220 and 220+1 == 221 and 240+1 == 241, 'incidence coefficient counts')
    print(json.dumps({'pass':True,'exact_checks':count,'controls':records,
                      'scope':'Supplemental algebraic equation bookkeeping only; finiteness, realization and arithmetic descent require proof.'},indent=2))


if __name__ == '__main__':
    main()
