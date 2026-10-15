#!/usr/bin/env python3
"""Review-owned exact arithmetic; no candidate imports and no floating acceptance."""
from fractions import Fraction as Q
from math import isqrt
import json

def need(ok, label):
    if not ok:
        raise RuntimeError(label)

def exponential(x, degree):
    total = term = Q(1)
    for k in range(1, degree + 1):
        term = term * x / k
        total += term
    omitted = term * x / (degree + 1)
    need(0 <= x < degree + 2, 'positive Taylor range')
    return total, total + omitted / (1 - x / (degree + 2))

def root_hi(x):
    scale = 10**8
    k = isqrt(x.numerator * scale**2 // x.denominator)
    need(Q(k, scale)**2 <= x < Q(k+1, scale)**2, 'root lattice')
    return Q(k+1, scale)

def arctangent(x):
    total = term = Q(0)
    for k in range(24):
        total += (-1)**k * x**(2*k+1) / (2*k+1)
    return total, total + x**49/49

def main():
    thirds, sevenths = arctangent(Q(1,3)), arctangent(Q(1,7))
    pi_lo = 8*thirds[0] + 4*sevenths[0]
    pi_hi = 8*thirds[1] + 4*sevenths[1]
    need(Q(1772,1000)**2 < pi_lo < pi_hi < Q(1773,1000)**2, 'sqrt pi bracket')
    need(exponential(Q(1),14)[1] < Q(2719,1000), 'e bracket')
    need(pi_hi*exponential(Q(1),14)[1]**3 < 128, 'round attainment witness')
    need(2*pi_lo**2 > Q(7,5), 'Poisson correction sign')
    need(1+Q(8,3)/exponential(Q(1),14)[0]**3 < 2, 'each cap integral')
    lower = Q(1772,2719)*Q(10000000-7092,10004000)
    need(lower == Q(1106714561,1700054750), 'lower reduction')
    need(lower-Q(13,20) == Q(3357947,3400109500), 'exact margin')
    small = Q(1773,4000)*exponential(Q(7,20),14)[1]
    bounds = [small]
    endpoints = [Q(k,10) for k in range(14,21)]
    for a,b in zip(endpoints,endpoints[1:]):
        need(Q(16,9)/(1+7*a) < Q(1,2), 'spectral geometric ratio')
        A = b*root_hi(b)/exponential(3*b/4,50)[0]
        D = a*root_hi(a)*(4/exponential(15*a/4,50)[0]+18/exponential(35*a/4,50)[0])
        bounds.append(A+D)
    printed = [629002,631338,636143,639464,641172,641202,639541]
    need(len(bounds)==7 and all(x<Q(y,10**6) for x,y in zip(bounds,printed)), 'seven printed table enclosures')
    need(max(printed)==641202 and Q(max(printed),10**6)<Q(321,500)<Q(13,20), 'all-time strict separation')
    return {'status':'PASS','arithmetic':'integers and fractions only','candidate_imports':False,
            'lower_exact':str(lower),'lower_margin_over_13_20':str(lower-Q(13,20)),
            'table_exact':[str(x) for x in bounds],'printed_table_numerators':printed,
            'round_table_max':'641202/1000000','round_threshold':'321/500',
            'cap_integral_lt_2':True,'round_attainment_witness':True,
            'analytic_obligations_certified_by_program':False}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
