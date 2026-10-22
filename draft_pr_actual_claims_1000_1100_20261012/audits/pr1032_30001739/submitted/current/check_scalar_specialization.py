#!/usr/bin/env python3
"""Independent exact scalar checks; does not calculate invariant-functional spaces."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sympy as sp

ROOT = Path(__file__).resolve().parent
SEGMENTS = {'E': (4, 6), 'D': (2, 5), 'C': (3, 3), 'B': (1, 4), 'A': (0, 2)}
ORDERS = [('E','D','C','B','A'), ('E','C','D','B','A'), ('E','D','B','C','A')]
t = sp.Symbol('t')  # q^{-s}; t = 1 means s = 0

def demand(condition, message):
    if not condition:
        raise RuntimeError(message)

def l_exponents(first, second):
    # JPSS 8.2: shift by centers and (m+n)/2-i, i=1,...,min(m,n).
    a,b = SEGMENTS[first]
    c,d = SEGMENTS[second]
    m,n = b-a+1,d-c+1
    shift = Fraction(a+b-c-d+m+n,2)
    answer = [shift-i for i in range(1,min(m,n)+1)]
    demand(all(x.denominator == 1 for x in answer), 'Nonintegral exponent')
    return [int(x) for x in answer]

def gamma_unit_part(first, second, sign, q):
    # epsilon(s) is an analytic unit and intentionally omitted.
    # gamma(s) = epsilon(s) L(1-s,dual)/L(s,original).
    forward = l_exponents(first,second)
    reverse = l_exponents(second,first)
    return sp.cancel(sp.prod(1-sign*sp.Rational(q)**(-e)*t for e in forward)
                     /sp.prod(1-sign*sp.Rational(q)**(-1-e)/t for e in reverse))

def order_at_one(expression):
    num,den = sp.fraction(sp.cancel(expression))
    def multiplicity(polynomial):
        p=sp.Poly(polynomial,t)
        count=0
        while p.eval(1)==0:
            p=sp.div(p,sp.Poly(t-1,t))[0]
            count+=1
        return count
    return multiplicity(num)-multiplicity(den)

expected = {
    ('E','D'):([4,3,2],[1,0,-1],-1,1,2),
    ('E','C'):([3],[-1],-1,0,1),
    ('E','B'):([5,4,3],[0,-1,-2],-1,1,2),
    ('E','A'):([6,5,4],[-2,-3,-4],0,0,0),
    ('D','C'):([2],[1],0,0,0),
    ('D','B'):([4,3,2,1],[2,1,0,-1],-1,1,2),
    ('D','A'):([5,4,3],[0,-1,-2],-1,1,2),
    ('C','B'):([2],[1],0,0,0),
    ('C','A'):([3],[-1],-1,0,1),
    ('B','A'):([4,3,2],[1,0,-1],-1,1,2),
}
rows=[]
for first,second in combinations(SEGMENTS,2):
    fwd,rev,fg,rg,cg=expected[first,second]
    demand(l_exponents(first,second)==fwd and l_exponents(second,first)==rev,'Exponents disagree')
    for q in [3,9]:
        for sign in [1,-1]:
            forward=gamma_unit_part(first,second,sign,q)
            reverse=gamma_unit_part(second,first,sign,q)
            ratio=sp.cancel(reverse.subs(t,1/t)/forward)
            observed=[order_at_one(forward),order_at_one(reverse),order_at_one(ratio)]
            predicted=[fg,rg,cg] if sign==1 else [0,0,0]
            demand(observed==predicted,'Gamma orders disagree')
            result={
                'pair':[first,second], 'residue_cardinality':q, 'character_at_uniformizer':sign,
                'forward_L0_exponents':fwd,'reverse_L0_exponents':rev,
                'forward_gamma_order':observed[0],'reverse_gamma_order':observed[1],
                'reverse_over_forward_coefficient_order':observed[2],
                'coefficient_epsilon_unit_omitted':str(ratio),
                'coefficient_value_epsilon_unit_omitted':str(sp.limit(ratio,t,1))
            }
            if (first,second) in [('D','C'),('C','B')]:
                demand(all(x==0 for x in observed),'Nested scalar not a unit')
                demand(sp.limit(ratio,t,1)!=0,'Nested coefficient vanished')
            rows.append(result)
order_checks=[]
for order in ORDERS:
    for first,second in combinations(order,2):
        a,b=SEGMENTS[first];c,d=SEGMENTS[second]
        earlier_flo_precedes_later=a<=c<=b<=d
        demand(not earlier_flo_precedes_later,'FLO Corollary 13.6 hypothesis failed')
        order_checks.append({'order':list(order),'pair':[first,second],'earlier_FLO_relation':False})
result={
 'status':'PASS',
 'scope':'Exact rational scalar and Corollary 13.6 endpoint checks, not a calculation of Hom spaces',
 'all_10_pairs_checked':True,'scalar_rows':rows,'all_30_order_conditions':order_checks,
 'linked_pairs_used':[['E','D'],['B','A'],['E','C'],['D','B'],['C','A']],
 'nested_swaps_used':[['D','C'],['C','B']]
}
print(json.dumps(result, indent=2, sort_keys=True))
