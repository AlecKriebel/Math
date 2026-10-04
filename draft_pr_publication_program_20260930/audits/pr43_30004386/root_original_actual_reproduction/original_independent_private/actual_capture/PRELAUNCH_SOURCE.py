#!/usr/bin/env python3
"""Independent exact controls, not an LDP proof.
Run from this directory: python independent_checks.py > independent_results.json
"""
from fractions import Fraction as F
from collections import Counter
from itertools import permutations
from math import factorial
import json
counts=Counter()
def check(ok,name):
    assert ok,name
    counts[name]+=1

# Squared coefficients; a different prefix rule m=floor(N/2) is used.
families={
 'gaussian':(lambda j:F(0),F(0)),
 'single_boundary':(lambda j:F(j==1),F(1)),
 'plateau_interior':(lambda j:F(1,4) if j<=3 else F(0),F(3,16)),
 'finite_boundary':(lambda j:[F(4,9),F(4,9),F(1,9)][j-1] if j<=3 else F(0),F(11,27)),
 'infinite_interior':(lambda j:F(1,3**j),F(1,8)),
 'infinite_boundary':(lambda j:F(2,3**j),F(1,2)),
}
dimensions=[2,5,8,17,32]
for name,(squared,total_fourth) in families.items():
    for n in dimensions:
        m=n//2; r=n-m
        retained=[squared(j) for j in range(1,m+1)]
        mass=sum(retained,F(0)); filler=(1-mass)/r
        arranged=sorted(retained+[filler]*r,reverse=True)
        check(1<=m<n,'valid_alternative_prefix')
        check(F(0)<=filler<=F(1,r),'vanishing_filler_bound')
        check(sum(arranged,F(0))==1,'unit_sphere_normalization')
        check(sum(arranged,F(0))/3==F(1,3),'projection_variance')
        for j,a2 in enumerate(retained):
            check(a2<=arranged[j]<=max(a2,filler),'sorted_coordinate_interval')
            check(F(0)<=arranged[j]-a2<=filler,'coordinate_error_bound')
        tail_fourth=total_fourth-sum((x*x for x in retained),F(0))
        check(tail_fourth>=0,'exact_target_fourth_tail')
        excess=r*filler*filler
        check(excess<=F(1,r),'gaussian_filler_fourth_bound')
        finite_fourth=sum((x*x for x in arranged),F(0))
        check(abs(finite_fourth-total_fourth)<=tail_fourth+F(1,r),'total_fourth_error_bound')
        moment4=F(1,3)-F(2,15)*finite_fourth
        check(F(1,5)<=moment4<=F(1,3),'projection_fourth_moment_range')

# Characteristic-polynomial coefficients up to t^6, using z=t^2.
def multiply(x,y):
    return [sum((x[j]*y[k-j] for j in range(k+1)),F(0)) for k in range(4)]
def cf_coefficients(squares, gaussian_variance):
    result=[(-gaussian_variance/F(2))**k/F(factorial(k)) for k in range(4)]
    for q in squares:
        result=multiply(result,[F(1),-q/F(6),q*q/F(120),-q**3/F(5040)])
    return result
vectors=[[],[F(1)],[F(1,4)]*3,[F(4,9),F(4,9),F(1,9)],[F(1,4),F(1,9),F(1,25)]]
for squares in vectors:
    norm2=sum(squares,F(0))
    result=cf_coefficients(squares,(1-norm2)/3)
    p4=sum((q*q for q in squares),F(0)); p6=sum((q**3 for q in squares),F(0))
    moment4=F(1,3)-F(2,15)*p4
    moment6=F(5,9)-F(2,3)*p4+F(16,63)*p6
    check(result[0]==1,'characteristic_normalization')
    check(result[1]==-F(1,6),'characteristic_variance_coefficient')
    check(result[2]==moment4/24,'characteristic_fourth_moment')
    check(result[3]==-moment6/720,'characteristic_sixth_moment')
    for perm in set(permutations(squares)):
        check(cf_coefficients(perm,(1-norm2)/3)==result,'permutation_invariance_control')
    check(result[1]!=-F(1,2),'variance_one_negative_control')

# Norm discontinuity controls and Gaussian filler cumulants.
for n in [2,3,8,25,64]:
    squares=[F(1,n)]*n
    check(sum(squares,F(0))==1,'diffuse_unit_norm')
    check(sum((x*x for x in squares),F(0))==F(1,n),'diffuse_fourth_decay')
    check(sum((x**3 for x in squares),F(0))==F(1,n*n),'diffuse_sixth_decay')

print(json.dumps({
 'status':'PASS','arithmetic':'Python standard-library exact rational arithmetic',
 'assertions':sum(counts.values()),'checks':dict(counts),
 'dimensions':dimensions,'families':list(families),
 'scope':'Finite normalization, coordinatewise filler-error, moment and characteristic-coefficient controls only. '
         'The LDP is supplied by the cited published theorem; both limit-set directions are audited in REVIEW.md.'
},indent=2))
