#!/usr/bin/env python3
"""Independent exact evaluation checks. Imports no author-packet code.

This finite diagnostic corroborates the operator normalization; it does not
prove the imported universal mesh theorem. Run with Python -I -S -B.
"""
from fractions import Fraction as Q
from math import comb, factorial
from random import Random
import hashlib
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def value(coefficients, x):
    result = Q(0)
    for coefficient in reversed(coefficients):
        result = result * x + coefficient
    return result


def factorial_value(m, x, direction=-1):
    result = Q(1)
    for j in range(m):
        result *= x + direction * j
    return result


def difference_values(samples, m, forward=False):
    # Direct binomial finite-difference formula, rather than iterated
    # polynomial subtraction as in the author verifier.
    return [sum(((-1) ** (k-j if forward else j) * comb(k, j) * samples[j]
                 for j in range(k+1)), Q(0)) for k in range(m+1)]


def differences(function, m, x, forward=False):
    direction = 1 if forward else -1
    return difference_values([function(x + direction*j) for j in range(m+1)],
                             m, forward)


def convolution_value(f, g, m, x, forward=False):
    left = differences(f, m, x, forward)
    right = differences(g, m, Q(0), forward)
    return sum((left[k]*right[m-k] for k in range(m+1)), Q(0))


def trim(p):
    while p and p[-1] == 0:
        p.pop()
    return p


def multiply(p, q):
    out = [Q(0)] * (len(p)+len(q)-1) if p and q else []
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] += a*b
    return trim(out)


def interpolate_grid(ys):
    """Newton reconstruction from integer grid, with explicit monic factors."""
    result = [Q(0)]*len(ys)
    basis = [Q(1)]
    row = list(ys)
    for k in range(len(ys)):
        c = row[0]/factorial(k)
        for j, b in enumerate(basis):
            result[j] += c*b
        row = [row[j+1]-row[j] for j in range(len(row)-1)]
        basis = multiply(basis, [Q(-k), Q(1)])
    return trim(result)


def remainder(p, q):
    p = list(p)
    while p and len(p) >= len(q):
        k = len(p)-len(q)
        c = p[-1]/q[-1]
        for j, b in enumerate(q):
            p[j+k] -= c*b
        trim(p)
    return p


def sturm(p):
    p = trim(list(p))
    seq = [p, [Q(i)*p[i] for i in range(1, len(p))]]
    while seq[-1]:
        r = [-a for a in remainder(seq[-2], seq[-1])]
        if not r:
            break
        seq.append(r)
    return seq


def variation(seq, x):
    signs = []
    for p in seq:
        y = value(p, x)
        if y:
            signs.append(1 if y > 0 else -1)
    return sum(a != b for a, b in zip(signs, signs[1:]))


def certify_strict_mesh(p):
    """Exact Sturm interval certificate for selected strictly separated cases."""
    if len(p) <= 2:
        return []
    seq = sturm(p)
    need(len(seq[-1]) == 1, 'repeated-root output')
    bound = Q(2+max(abs(a/p[-1]) for a in p[:-1]))
    left, right = -bound, bound
    need(variation(seq,left)-variation(seq,right) == len(p)-1, 'nonreal output')
    intervals = [(left,right,len(p)-1)]
    for _ in range(512):
        if all(n == 1 for a,b,n in intervals):
            if all(intervals[i+1][0]-intervals[i][1] >= 1
                   for i in range(len(intervals)-1)):
                return [[str(a),str(b)] for a,b,n in intervals]
        refined = []
        for a,b,n in intervals:
            middle = (a+b)/2
            # Never place an exact polynomial root on a Sturm endpoint.
            while value(p,middle) == 0:
                middle = (a+middle)/2
            nl = variation(seq,a)-variation(seq,middle)
            nr = variation(seq,middle)-variation(seq,b)
            need(nl+nr == n, 'Sturm subdivision')
            if nl:
                refined.append((a,middle,nl))
            if nr:
                refined.append((middle,b,nr))
        intervals = refined
    raise ValueError('strict mesh interval certificate did not terminate')


def main():
    rng = Random(2200009)
    counts = {}
    trace = hashlib.sha256()
    def check(label, a, b):
        need(a == b, label)
        counts[label] = counts.get(label, 0)+1
        trace.update((label+' '+repr(a)+'\n').encode())
    def random_poly(d):
        if d < 0:
            return []
        return [Q(rng.randrange(-5,6), rng.randrange(1,5)) for _ in range(d)] + [Q(rng.choice([-3,-1,1,2]))]

    for m in range(13):
        stencils = [(),(0,),(1,),(0,0,0,1),(Q(2,3),Q(-5,7),Q(9,4))]
        stencils += [tuple((-1)**j*comb(order,j) for j in range(order+1))
                     for order in sorted({1,m,m+1,m+4})]
        stencils += [tuple(rng.randrange(-4,5) for _ in range(m+8)) for _ in range(3)]
        for coefficients in stencils:
            def h(y):
                return sum((a*factorial_value(m,y-j) for j,a in enumerate(coefficients)),Q(0))
            def r(y):
                return h(y+m-1)
            recovered = differences(r,m,Q(0))
            for s in range(m+1):
                c = (-1)**s*sum((comb(j,s)*coefficients[j]
                    for j in range(s,len(coefficients))),Q(0))
                check('coefficient-recovery', recovered[m-s], factorial(m)*c)
            for d in range(-1,m+1):
                p = random_poly(d)
                def f(y):
                    return value(p,y)
                for x in (Q(-2),Q(0),Q(3,2)):
                    direct = sum((a*f(x-j) for j,a in enumerate(coefficients)),Q(0))
                    check('backward-bridge',convolution_value(f,r,m,x),factorial(m)*direct)
                    check('forward-bridge',convolution_value(f,h,m,x,True),factorial(m)*direct)
            symbol = interpolate_grid([h(Q(x)) for x in range(m+1)])
            check('full-degree-nonzero-convention', len(symbol)==m+1, sum(coefficients,Q(0)) != 0)
        for d in range(-1,m+1):
            for e in range(-1,m+1):
                p,q = random_poly(d),random_poly(e)
                f = lambda x:value(p,x)
                g = lambda x:value(q,x)
                ys = [convolution_value(f,g,m,Q(x)) for x in range(m+1)]
                output = interpolate_grid(ys)
                expected_degree = d+e-m if d>=0 and e>=0 and d+e>=m else -1
                check('degree',len(output)-1,expected_degree)
                if output:
                    check('leading-coefficient',output[-1],p[-1]*q[-1]*Q(factorial(d)*factorial(e),factorial(expected_degree)))
                x = Q(5,3)
                check('symmetry',convolution_value(f,g,m,x),convolution_value(g,f,m,x))
                check('reflection',convolution_value(lambda z:f(-z),lambda z:g(-z),m,x),(-1)**m*convolution_value(f,g,m,-x,True))

    # Separate exact Sturm certificates in degrees up to six. The inputs use
    # widely spaced rational roots, including degree loss and zero cases.
    certificates=[]
    for m in range(2,7):
        for d in range(m+1):
            for e in range(m+1):
                p,q=[Q(1)],[Q(1)]
                for j in range(d):
                    p=multiply(p,[-Q(3*j-5,2),Q(1)])
                for j in range(e):
                    q=multiply(q,[-Q(4*j+1,2),Q(1)])
                f,g=lambda x:value(p,x),lambda x:value(q,x)
                out=interpolate_grid([convolution_value(f,g,m,Q(x)) for x in range(m+1)])
                intervals=certify_strict_mesh(out)
                check('sturm-mesh-certificate',len(intervals),max(0,len(out)-1) if len(out)>2 else 0)
                certificates.append({'m':m,'d':d,'e':e,'degree':len(out)-1,'intervals':intervals})

    # Explicit incorrect-formula witnesses and the nonzero-output trap.
    m=2
    f=lambda x:x*x
    h=lambda x:factorial_value(m,x)
    check('missing-translation-rejected',convolution_value(f,h,m,Q(0)) != factorial(m)*f(Q(0)),True)
    check('missing-factorial-rejected',convolution_value(f,lambda x:h(x+1),m,Q(2)) != f(Q(2)),True)
    check('wrong-direction-rejected',convolution_value(f,h,m,Q(0)) != convolution_value(f,h,m,Q(0),True),True)
    check('difference-kills-constant',Q(1)-Q(1),Q(0))
    check('difference-symbol-linear',[h(Q(x))-h(Q(x-1)) for x in range(3)],[Q(-2),Q(0),Q(2)])
    check('twice-difference-symbol-constant',[h(Q(x))-2*h(Q(x-1))+h(Q(x-2)) for x in range(3)],[Q(2)]*3)
    return {'schema':'mesh-preserver-independent-diagnostics-v1','status':'PASS',
            'seed':2200009,'counts':counts,'total_checks':sum(counts.values()),
            'trace_sha256':trace.hexdigest(),'sturm_cases':len(certificates),
            'sturm_nontrivial_cases':sum(bool(c['intervals']) for c in certificates),
            'scope':'Independent exact finite diagnostics, not a proof of the imported universal mesh theorem.'}


if __name__ == '__main__':
    print(json.dumps(main(),sort_keys=True,separators=(',',':')))
