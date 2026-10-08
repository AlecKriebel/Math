#!/usr/bin/env python3
"""Exact arithmetic regression checks for REPORT.md; no external data or packages.
These checks do not certify contact realization, all open books, or imported theorems.
"""
from fractions import Fraction as Q
from itertools import product
import json

def require(condition, message):
    """Retain validation in normal, -O, and -OO interpreters."""
    if not condition:
        raise ValueError(message)

checks = {}

def inverse(word):
    return [-x for x in reversed(word)]

def commutator(u, v):
    return u + v + inverse(u) + inverse(v)

def exponent_vector(word, generators):
    ans = [0] * generators
    for x in word:
        ans[abs(x)-1] += 1 if x > 0 else -1
    return ans

count = 0
for g in range(1, 13):
    w = []
    for i in range(g):
        w += commutator([2*i+1], [2*i+2])
    for n in range(1, 10):
        for x in range(1, 2*g+1):
            require(exponent_vector(commutator(w*n, [x]), 2*g) == [0]*(2*g), 'check_math.py:30: verification predicate failed')
            count += 1
checks['boundary_twist_relator_abelianizations'] = count

count = 0
for g in range(1, 51):
    for h in range(0, g+4):
        b_min = max(1, 2*g+1-2*h)
        require(2*h+b_min-1 >= 2*g, 'check_math.py:38: verification predicate failed')
        require(2*h+b_min-2 >= 2*g-1, 'check_math.py:39: verification predicate failed')
        if b_min > 1:
            require(2*h+(b_min-1)-1 < 2*g, 'check_math.py:41: verification predicate failed')
        count += 1
    require(2*g+1-2 == 2*g-1, 'check_math.py:43: verification predicate failed')
    require((2*(g-1)+1-1) < 2*g, 'check_math.py:44: verification predicate failed')
    if g>=2:
        require(2*1+(2*g-1)-2 == 2*g-1, 'check_math.py:46: verification predicate failed')
checks['page_complexity_cases'] = count
checks['annulus_control'] = {'absolute_monodromy_cokernel_rank': 1,
    'actual_filled_rank_for_nonzero_twist': 0,
    'purpose': 'The multi-boundary coker(phi_*-I) shortcut is invalid.'}

count = 0
for g,b,d in product(range(1,13), repeat=3):
    h = 1+d*(g-1)+Q((d-1)*b,2)
    require(2-2*h-b == d*(2-2*g-b), 'check_math.py:55: verification predicate failed')
    require(h-g == (d-1)*(g-1+Q(b,2)), 'check_math.py:56: verification predicate failed')
    require(h>=g, 'check_math.py:57: verification predicate failed')
    count += 1
checks['horizontal_cover_arithmetic'] = count

# Reeb conformal-change equation in a symplectic two-plane, omega=dx wedge dy.
count = 0
for f,px,py,vx,vy in product(range(1,5),range(-2,3),range(-2,3),range(-2,3),range(-2,3)):
    zx,zy=Q(py,f*f),Q(-px,f*f)
    require(zx*vy-zy*vx == Q(px*vx+py*vy,f*f), 'check_math.py:65: verification predicate failed')
    count += 1
checks['conformal_reeb_linear_equations'] = count

samples=[]
for g in range(0,101):
    c_square=-(1-2*g)**2
    chi=2-2*g
    signature=-1
    d3=Q(c_square-2*chi-3*signature,4)
    require(d3 == -g*g+2*g-Q(1,2), 'check_math.py:75: verification predicate failed')
    require(-d3-Q(1,2) == g*g-2*g, 'check_math.py:76: verification predicate failed')
    if g<=6:
        samples.append({'g':g,'d3':str(d3),'candidate_contact_grading':g*g-2*g})
checks['d3_arithmetic']={'cases':101,'samples':samples}

count=0
for m in range(0,21):
    c=1<<m
    mask=(1<<(m+1))-1
    require(((c<<1)&mask)==0, 'check_math.py:85: verification predicate failed')
    for d in range(m+3):
        # U^d image has monomial basis u^d,...,u^m.
        image_support=sum(1<<j for j in range(d,m+1))
        belongs = (c & ~image_support)==0
        require(belongs == (d<=m), 'check_math.py:90: verification predicate failed')
        count+=1
checks['finite_U_summand_depth_cases']=count
checks['tower_control']='For every d>=0, U^d times the class of U^(-d) equals the class of 1.'

count=0
for b in range(1,5):
    subsets=[mask for mask in range(1,(1<<b)-1)]
    values=range(3) if b<=3 else range(2)
    n_values=range(16) if b<=3 else range(3)
    for multiplicities in product(values,repeat=len(subsets)):
        for n in n_values:
            es=[n+12*sum(s for mask,s in zip(subsets,multiplicities) if mask&(1<<i)) for i in range(b)]
            total=sum(es)
            length=n+sum(multiplicities)
            require(total==b*n+12*sum(mask.bit_count()*s for mask,s in zip(subsets,multiplicities)), 'check_math.py:105: verification predicate failed')
            require(n<=min(es), 'check_math.py:106: verification predicate failed')
            require(all(e>=0 and e%12==n%12 for e in es), 'check_math.py:107: verification predicate failed')
            require(length<=Q(total,min(b,12)), 'check_math.py:108: verification predicate failed')
            candidates=[v for v in range(min(es)+1) if all((e-v)%12==0 for e in es)]
            sharper=max(Q(total,12)+v*(1-Q(b,12)) for v in candidates)
            require(length<=sharper, 'check_math.py:111: verification predicate failed')
            count+=1
checks['capping_vector_factor_counts']=count

# Boundary twists around all boundaries at once are homologically trivial.
# Their capping vector would be (12,...,12), but they are not allowable factors.
for b in range(1,21):
    allowed=range(1,(1<<b)-1)
    require(((1<<b)-1) not in allowed, 'check_math.py:119: verification predicate failed')
checks['excluded_homologically_trivial_separating_types']=20

for h in range(0,10):
    for b in range(1,10):
        old_chi=2-2*h-b
        require(2-2*h-(b+1)==old_chi-1, 'check_math.py:125: verification predicate failed')
        if b>=2:
            require(2-2*(h+1)-(b-1)==old_chi-1, 'check_math.py:127: verification predicate failed')
checks['stabilization_euler_controls']=90

result={'status':'PASS','arithmetic_only':True,
        'does_not_prove_original_problem':True,'checks':checks}
print(json.dumps(result,indent=2,sort_keys=True))
