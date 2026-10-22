#!/usr/bin/env python3
"""Exact finite consistency controls; not a proof of the all-body classification."""
import json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

counts={}
def check(group,condition):
    if not condition:
        raise AssertionError(group)
    counts[group]=counts.get(group,0)+1

# Exact truth table for the nonnegative extended-addition support rule.
allowed=[]
for k,l,u,c in product((False,True),repeat=4):
    compatible=(k or l)==(u or c)
    # Values are 1 or infinity. Model infinity by None, with absorbing addition.
    vals=[None if z else 1 for z in (k,l,u,c)]
    add=lambda a,b: None if a is None or b is None else a+b
    check('boolean_support',compatible==(add(vals[0],vals[1])==add(vals[2],vals[3])))
    if compatible: allowed.append([k,l,u,c])
check('boolean_allowed_count',len(allowed)==10)

# Crossed-dilate geometry for all chosen endpoint quadruples.
grid=[Q(1,3),Q(1,2),Q(1),Q(2),Q(3)]
for a0,b0,a,b in product(grid,repeat=4):
    lam,mu=a/a0,b/b0
    other=(mu*a0,lam*b0)
    U=(max(a,other[0]),max(b,other[1]))
    C=(min(a,other[0]),min(b,other[1]))
    check('crossed_dilate_union',U==(max(lam,mu)*a0,max(lam,mu)*b0))
    check('crossed_dilate_intersection',C==(min(lam,mu)*a0,min(lam,mu)*b0))

# Finite one-dimensional families, using rational powers with integer exponent.
for q in (-3,-1,0,1,2,5):
    for A,B in ((Q(0),Q(1)),(Q(1),Q(0)),(Q(2,3),Q(5,4))):
        F=lambda a,b: A*a**q+B*b**q
        for a,b,c,d in product(grid,repeat=4):
            check('interval_valuation',F(a,b)+F(c,d)==F(max(a,c),max(b,d))+F(min(a,c),min(b,d)))
        for a,b,t in product(grid,repeat=3):
            check('interval_homogeneity',F(t*a,t*b)==t**q*F(a,b))

# Scalar truncation is demonstrably not a valuation even for length.
check('volume_identity',Q(4)+Q(4)==Q(6)+Q(2))
check('truncation_rejected',min(4,4)+min(4,4)!=min(6,4)+min(2,4))

# Box counterexample, endpoint asymmetry and exact volumes.
for n in range(2,9):
    K=(Q(1),Q(2)); L=(Q(2),Q(1)); U=(Q(2),Q(2)); C=(Q(1),Q(1))
    r=lambda pair:max(pair[0]/pair[1],pair[1]/pair[0])
    check('box_asymmetry',[r(x) for x in (K,L,U,C)]==[2,2,1,1])
    vol=lambda pair:(pair[0]+pair[1])*2**(n-1)
    check('box_volume',vol(K)+vol(L)==vol(U)+vol(C))
    for threshold in (Q(5,4),Q(3,2),Q(2)):
        flags=[r(x)>=threshold for x in (K,L,U,C)]
        check('asymmetry_boolean_failure',(flags[0] or flags[1])!=(flags[2] or flags[3]))

# Symbolic-exponent identities represented exactly as rational arithmetic.
for n in range(2,13):
    for alpha in (Q(-2),Q(-1,2),Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1),Q(3,2),Q(2)):
        q=n*(1-2*alpha)
        check('ball_power_scaling',n-2*n*alpha==q)
        if alpha!=1:
            p=n*alpha/(1-alpha)
            check('p_q_relation',p==n*(n-q)/(n+q))
        check('interior_degree_range',(0<alpha<1)==(-n<q<n))
        curvature_exponent=(n-1)*(1-alpha)
        check('rounded_cube_divergence',(curvature_exponent<0)==(alpha>1))
        if alpha==1:
            check('rounded_cube_endpoint',curvature_exponent==0)

result={'status':'PASS','total_assertions':sum(counts.values()),'groups':counts,
        'boolean_compatible_patterns':allowed,
        'scope':'Finite exact algebra and geometry consistency controls only. No infinite-dimensional classification is computationally proved.'}
if __name__=='__main__':
    print(json.dumps(result,sort_keys=True,indent=2))
