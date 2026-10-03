#!/usr/bin/env python3
"""Exact supplementary controls for sparse repairs; no simulations."""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
import json

checks=0
counts={}
def ck(x,scope):
    global checks
    assert x, scope
    checks+=1; counts[scope]=counts.get(scope,0)+1
H=[Q(0)]
for i in range(1,65): H.append(H[-1]+Q(1,i))
# Independent simplex-volume inclusion-exclusion integral vs exponential spacings.
for E in range(1,33):
    means=[]
    for j in range(1,E+1):
        v=sum((Q((-1)**(r-j)*comb(r-1,j-1)*comb(E,r),r*E)
               for r in range(j,E+1)),Q(0))
        ck(v==(H[E]-H[j-1])/E,'independent_order_statistic_integrals')
        means.append(v)
    for k in range(1,E+1):
        a=sum(means[:k]); b=Q(k,E)*(1+H[E]-H[k])
        ck(a==b,'top_k_mean_identity')
        ck(Q(k,E)<=b<=1,'mean_range')
        ck(b-(Q(k-1,E)*(1+H[E]-H[k-1]) if k>1 else 0)==means[k-1],
           'mean_increment')
# The indicator inversion underlying (4), independently on all integer counts.
for n in range(33):
    for j in range(1,34):
        v=sum((-1)**(r-j)*comb(r-1,j-1)*comb(n,r) for r in range(j,n+1))
        ck(v==int(n>=j),'inclusion_exclusion_indicator')
# Harmonic spacing sum for larger independent range and deterministic edge cases.
for E in range(1,65):
    ck(Q(E,E)*(1+H[E]-H[E])==1,'all_edges_mean')
    ck(H[E]/E==Q(1,E)*(1+H[E]-H[1]),'one_edge_mean')
    for k in range(1,E+1):
        ck(sum((H[E]-H[j-1] for j in range(1,k+1)),Q(0))
           ==k*(1+H[E]-H[k]),'exponential_spacing_sum')
        ck(H[E]-H[k]>=0,'harmonic_nonnegativity')
# Pointwise adaptive-subset capacity, independently exhaustive over each tiny vector.
vector_cases=subset_cases=0
for E in range(1,8):
    for seed in range(5):
        raw=[Q(1+(i*i+3*i+seed)%11) for i in range(E)]
        x=[v/sum(raw) for v in raw]
        for k in range(E+1):
            top=sum(sorted(x,reverse=True)[:k],Q(0))
            for I in combinations(range(E),k):
                chosen=set(I); C=Q(7,3)
                y=[v*(C if (i+seed)%2 else Q(1,3)) if i in chosen else v
                   for i,v in enumerate(x)]
                net=sum(y)-1
                mass=sum((x[i] for i in I),Q(0))
                ck(mass<=top,'adaptive_top_k_domination')
                ck(net<=(C-1)*mass,'repair_capacity')
                ck(net<=(C-1)*top,'combined_capacity')
                if net>0:
                    actual_C=max(y[i]/x[i] for i in range(E))
                    ck(actual_C>=1+net/top,'necessary_random_stretch')
                subset_cases+=1
        vector_cases+=1
# Rational finite-genus certificates are evaluations of the theorem, not empirical rates.
bounds=[]
for g,k,C in [(100,1,Q(2)),(1000,1,Q(2)),(1000,10,Q(2)),(10000,1,Q(3)),(10000,20,Q(3,2))]:
    E=6*g-3
    h=sum((Q(1,j) for j in range(k+1,E+1)),Q(0))
    bound=min(Q(1),25*(C-1)*Q(k,E)*(1+h))
    ck(0<=bound<=1,'finite_probability_bound_range')
    bounds.append({'genus':g,'edges':E,'changed_edges':k,'factor':str(C),
                  'bound_upper_decimal_6':str((bound*10**6).__ceil__())+'/1000000'})
print(json.dumps({'assertions':checks,'by_scope':counts,
 'arithmetic':'exact integer and rational; no simulations or floating-point probability controls',
 'independent_integral_max_edges':32,'spacing_identity_max_edges':64,
 'rational_vectors':vector_cases,'exhaustive_subsets':subset_cases,
 'finite_genus_probability_upper_bounds':bounds,
 'scope':'Supplementary finite controls; the full quantified proof is TURN_5.md.'},indent=2)+'\n',end='')
