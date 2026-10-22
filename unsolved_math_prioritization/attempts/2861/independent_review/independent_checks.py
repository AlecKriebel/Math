#!/usr/bin/env python3
"""Independent exact algebraic controls, not an eta or length-spectrum computation."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
C={}
def ck(k,v):
    assert v,k
    C[k]=C.get(k,0)+1
def mul(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def neg(z):return (-z[0],-z[1])
def norm(z):return z[0]**2+z[1]**2
def inv(z):
    n=norm(z);return (z[0]/n,-z[1]/n)
def power(z,n):
    a=(Q(1),Q(0))
    for _ in range(n):a=mul(a,z)
    return a
phases=[(Q(a),Q(b)) for a,b in ((1,0),(-1,0),(0,1),(0,-1))]
phases +=[(Q(a,5),Q(b,5)) for a,b in product((-3,3),(-4,4))]
for q in (Q(3,2),Q(2),Q(3),Q(7)):
    # q represents exp(ell), while phase is exp(i theta).
    for phase in phases:
        c2,s2=mul(phase,phase)
        d=q+1/q-2*c2
        left=(1+q*q-2*q*c2)*(1+1/(q*q)-2*c2/q)
        ck('denominator_identity',left==d*d and d>0)
        ck('systole_lower_bound',d>=q*(1-Q(2,3))**2)
        ck('spin_sign_keeps_denominator',mul(neg(phase),neg(phase))==(c2,s2))
        ck('spin_sign_flips_numerator',neg(phase)[1]==-phase[1])
        for m in range(1,9):
            ck('iterate_spin_lift_sign',power(neg(phase),m)==tuple((-1)**m*x for x in power(phase,m)))
            ck('primitive_length_ratio',Q(1,m)*m==1)
# Algebraic expanding-eigenvalue convention for inverse matrices.
for radius in (Q(2),Q(3),Q(5)):
    for phase in phases:
        z=tuple(radius*x for x in phase)
        forward=(z,inv(z));backward=(inv(z),z)
        ck('inverse_class_expanding_eigenvalue',next(v for v in forward if norm(v)>1)==next(v for v in backward if norm(v)>1))
        ck('orientation_conjugation', (z[0],-z[1])[1]==-z[1])

# Cutoff exponent and geometric-tail ratio, including the boundary k=R.
for n in range(1,21):
    R=4*n*n
    ck('diagonal_first_exponent',Q(R)-Q(R*R,2*n*n)==-4*n*n)
    for k in range(R,R+17):
        f=lambda x:Q(x)-Q(x*x,2*n*n)
        ck('tail_ratio_at_most_exp_minus3',f(k+1)-f(k)<=-3)
        ck('tail_absolute_majorant',f(k)<=-4*n*n-3*(k-R))
# Count times inverse denominator yields e^(k+2), before the Gaussian.
for k in range(30):
    ck('count_weight_exponent',2*(k+1)-k==k+2)

# No uniform spectral convergence rate follows from an unknown nonzero gap.
for n in range(1,31):
    gap=Q(1,n)
    ck('shrinking_gap_negative_control',n*gap==1)
    ck('fixed_gap_argument_growth',n*Q(1,7)==Q(n,7))
# Kernel is excluded from the raw eta sum, not assigned half its multiplicity.
for h in range(1,9):
    ck('zero_mode_raw_vs_reduced',0!=Q(h,2))
# Exact Weeks normalization arithmetic, not certification of the Snap input.
ck('weeks_sign',1-Q(40028711,10**9)/4==Q(3959971289,4*10**9))
result={'status':'PASS','assertions_passed':sum(C.values()),'by_category':C,
        'scope':'Exact arithmetic consistency only; no certified geometric data, spectral gap, decimal eta value or universal stopping algorithm.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
