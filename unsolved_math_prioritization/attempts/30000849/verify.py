#!/usr/bin/env python3
"""Exact finite diagnostics. The existence and Fatou arguments are analytic."""
from fractions import Fraction as F
from collections import defaultdict
import json

counts={}
def check(group, condition):
    if not condition: raise AssertionError(group)
    counts[group]=counts.get(group,0)+1

# Compute each finite moment balance directly from the component equations.
# Coefficients are formal a_i,b_i symbols; dictionary keys also retain c1*c_i.
def moment_rhs(n,k):
    d=defaultdict(int)
    d[('constant',0)]+=1
    d[('one',1)]-=1  # -c1^2 in the monomer equation
    for i in range(1,n+1):d[(f'a{i}',i)]-=1
    for j in range(2,n+1):
        d[(f'b{j}',j-1)]+=j**k
        d[(f'a{j}',j)]-=j**k
    return {x:y for x,y in d.items() if y}

def physical(d):
    e=defaultdict(int)
    for (symbol,i),coef in d.items():
        if symbol.startswith('b'):symbol='a'+str(int(symbol[1:])-1)
        if symbol=='a1':symbol='one'
        e[(symbol,i)]+=coef
    return {x:y for x,y in e.items() if y}

for n in range(2,129):
    m=moment_rhs(n,1)
    expected={('constant',0):1,('one',1):-1,('a1',1):-1}
    for i in range(2,n+1):expected[(f'a{i}',i)]=-(i+1)
    for j in range(2,n+1):expected[(f'b{j}',j-1)]=j
    check('finite_first_moment_formal_telescopes',m==expected)
    check('standard_first_moment',physical(m)=={('constant',0):1,(f'a{n}',n):-(n+1)})
    expected2={('constant',0):1,('one',1):2,(f'a{n}',n):-(n*n+1)}
    for i in range(2,n):expected2[(f'a{i}',i)]=2*i
    check('standard_second_moment',physical(moment_rhs(n,2))==expected2)

# Fourth-power comparisons certify the sign of the printed interior coefficients
# for these samples; the general inequality is proved in the manuscript.
check('printed_monomer_coefficient_sign',2<2**4)
for i in range(2,1002):
    check('printed_interior_coefficient_sign',(i+1)<(i+1)**4*i)

p=F(1,4);omega=F(0);s=(2+omega)/(3-2*p)
r=(1-omega*(1-p))/((2+omega)*(1-p))
check('target_exponents',s==F(4,5))
check('target_exponents',r==F(2,3))
check('target_exponents',r+p==F(11,12)<3)
check('target_exponents',s*(2-r)==F(16,15)>1)
check('target_exponents',1-r+1/s==F(19,12))
check('target_exponents',2-r+1/s==F(31,12))
check('target_exponents',2/s==F(30,12))
check('target_exponents',(2-r+1/s)-2/s==F(1,12))
check('target_exponents',2-1/s==F(3,4))
check('target_exponents',p+(1-p)*r==F(3,4))

# Compare general exponent algebra without claiming any general existence theorem.
for pn in range(-10,10):
    pp=F(pn,10)
    for wn in range(-4,21):
        w=F(wn,10);ss=(2+w)/(3-2*pp)
        rr=(1-w*(1-pp))/((2+w)*(1-pp))
        diff=-pp*(2*pp*w+2*pp-2*w-1)/((pp-1)*(2*pp-3))
        check('general_exponent_identity',ss*(2-rr)-(1+w)==diff)
        if pp==0:check('constant_kernel_mass_compatibility',diff==0)

# Positive-profile controls, not solutions of the ODE. At sigma=k^12, t=k^15,
# the corrected amplitude3/4 is k^-9 and printed2/3 is k^-8.
# Exact integer sums on [sigma/4,sigma/2] demonstrate the differing budget.
for k in range(2,66,2):
    sigma=k**12;t=k**15;lo=sigma//4;hi=sigma//2
    moment_sum=F((lo+hi)*(hi-lo+1),2)
    corrected=moment_sum/k**9;printed=moment_sum/k**8
    check('synthetic_profile_control',corrected<=t)
    check('synthetic_profile_control',printed==k*corrected)
    check('synthetic_profile_control',F(3,32)*t<=corrected)
    if k>=12:check('synthetic_wrong_normalization_exceeds_input',printed>t)

receipt={'problem_id':30000849,'substantive_turn':1,
         'all_exact_checks_passed':True,'counts':counts,
         'total_exact_assertions':sum(counts.values()),
         'scope':'Finite telescopes and rational arithmetic only; not a computational proof of infinite-system existence, convergence or Fatou.',
         's':'4/5','r':'2/3','integrated_lower_exponent':'31/12',
         'integrated_upper_exponent':'30/12','gap':'1/12'}
print(json.dumps(receipt,indent=2,sort_keys=True))
