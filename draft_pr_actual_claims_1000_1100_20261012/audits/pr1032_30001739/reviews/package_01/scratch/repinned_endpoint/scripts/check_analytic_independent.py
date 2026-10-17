#!/usr/bin/env python3
"""Finite endpoint/rational-germ checks; never computes a Hom space.

No submitted checker, asserted source-result flag, or historical verdict is
imported. Gamma epsilon factors are omitted analytic units, explicitly.
"""
from fractions import Fraction
from itertools import combinations, product
import json

SEGMENTS = {'E': (4, 6), 'D': (2, 5), 'C': (3, 4), 'B': (1, 4), 'A': (0, 2)}
ORDERS = [('E', 'D', 'C', 'B', 'A'), ('E', 'C', 'D', 'B', 'A'),
          ('E', 'D', 'B', 'C', 'A')]
EDGES = [('E', 'D'), ('B', 'A'), ('E', 'C'), ('D', 'B'), ('C', 'A')]
NESTED = [('D', 'C'), ('C', 'B')]

def require(value, detail):
    if not value:
        raise RuntimeError(detail)

def exponent_set(first, second):
    a, b = first
    c, d = second
    m, n = b-a+1, d-c+1
    center_difference = Fraction(a+b-c-d, 2)
    # JPSS equation (20): centers plus (m+n)/2-i, i=1,...,min(m,n).
    exponents = [center_difference+Fraction(m+n,2)-i
                 for i in range(1,min(m,n)+1)]
    require(all(v.denominator == 1 for v in exponents), 'noninteger exponent')
    return [int(v) for v in exponents]

def ratio_germ(first, second, sign, q):
    p = exponent_set(first, second)
    r = exponent_set(second, first)
    numerator_exponents = r + [v+1 for v in r]
    denominator_exponents = p + [v+1 for v in p]
    order, leading = 0, Fraction(1)
    for exponent in numerator_exponents:
        value = 1-sign*Fraction(q)**(-exponent)
        if value == 0:
            order += 1
            # 1-1/t=(t-1)/t: leading coefficient +1 at t=1.
        else:
            leading *= value
    for exponent in denominator_exponents:
        value = 1-sign*Fraction(q)**(-exponent)
        if value == 0:
            order -= 1
            # 1-t=-(t-1): leading coefficient -1 at t=1.
            leading *= -1
        else:
            leading /= value
    return {'P':p,'Q':r,'order':order,'leading_in_t_minus_1':str(leading),
            'value_at_t_1':str(leading) if order == 0 else ('0' if order > 0 else 'pole'),
            'epsilon_factors_omitted_as_analytic_units':True,
            't_definition':'q^(-(lambda_i-lambda_j))'}

def flo_rel(first, second):
    a,b=first
    c,d=second
    return a <= c <= b <= d

def precedes(first, second):
    a,b=first
    c,d=second
    # Set-based LM linkage, independent of the FLO relation.
    left, right = set(range(a,b+1)), set(range(c,d+1))
    union=left|right
    contiguous = len(union)==max(union)-min(union)+1
    return contiguous and not left <= right and not right <= left and a < c

def main():
    order_checks=[]
    for ordering in ORDERS:
        for first,second in combinations(ordering,2):
            f=flo_rel(SEGMENTS[first],SEGMENTS[second])
            l=precedes(SEGMENTS[first],SEGMENTS[second])
            require(not f and not l, 'order condition failed')
            order_checks.append({'order':ordering,'pair':[first,second],
                                 'FLO_relation':f,'LM_precedes':l})
    rows=[]
    for first,second in combinations(SEGMENTS,2):
        for q in [3,9]:
            for sign in [1,-1]:
                germ=ratio_germ(SEGMENTS[first],SEGMENTS[second],sign,q)
                if (first,second) in EDGES:
                    require(germ['order'] == (0 if sign == -1 else
                            (1 if (first,second) in [('E','C'),('C','A')] else 2)),
                            'linked order disagrees')
                if (first,second) in NESTED:
                    require(germ['order']==0 and germ['value_at_t_1']!='0',
                            'nested coefficient not a unit')
                rows.append({'pair':[first,second],'q':q,'character_sign':sign,**germ})
    labels=[dict(zip(['E','D','C','B','A'],(0,)+bits))
            for bits in product([0,1],repeat=4)]
    survivors=[]
    for count in range(len(EDGES)+1):
        passing=[e for e in labels if all(e[a]!=e[b] for a,b in EDGES[:count])]
        survivors.append({'edges':EDGES[:count],'count':len(passing),'labels':passing})
    require(survivors[-1]['count']==0, 'odd cycle has a coloring')
    chamber=[{'pair':[i,j],'center_difference':str(Fraction(sum(SEGMENTS[i])-sum(SEGMENTS[j]),2))}
             for i,j in EDGES+NESTED]
    require(all(Fraction(r['center_difference'])>0 for r in chamber),'chamber wall')
    boundary={'shared_endpoint_unlinked':ratio_germ((0,2),(1,2),1,3),
              'equal_center_nested_difference':str(Fraction(sum((0,4))-sum((1,3)),2))}
    print(json.dumps({'status':'PASS','computed_Hom_space':False,
                      'scope':'Finite exact endpoint and gamma-unit-part germs only',
                      'basis_coordinate_count':len(labels),'order_checks':order_checks,
                      'scalar_checks':rows,'coordinate_survivors':survivors,
                      'strict_chamber_checks':chamber,'boundary_checks':boundary},
                     indent=2,sort_keys=True))

if __name__=='__main__':
    main()
