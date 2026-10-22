#!/usr/bin/env python3
"""Exact arithmetic regression checks for REPORT.md; no external data or packages.
These checks do not certify contact realization, all open books, or imported theorems.
"""
from fractions import Fraction as Q
from itertools import product
import json

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
            assert exponent_vector(commutator(w*n, [x]), 2*g) == [0]*(2*g)
            count += 1
checks['boundary_twist_relator_abelianizations'] = count

count = 0
for g in range(1, 51):
    for h in range(0, g+4):
        b_min = max(1, 2*g+1-2*h)
        assert 2*h+b_min-1 >= 2*g
        assert 2*h+b_min-2 >= 2*g-1
        if b_min > 1:
            assert 2*h+(b_min-1)-1 < 2*g
        count += 1
    assert 2*g+1-2 == 2*g-1
    assert (2*(g-1)+1-1) < 2*g
    if g>=2:
        assert 2*1+(2*g-1)-2 == 2*g-1
checks['page_complexity_cases'] = count
checks['annulus_control'] = {'absolute_monodromy_cokernel_rank': 1,
    'actual_filled_rank_for_nonzero_twist': 0,
    'purpose': 'The multi-boundary coker(phi_*-I) shortcut is invalid.'}

count = 0
for g,b,d in product(range(1,13), repeat=3):
    h = 1+d*(g-1)+Q((d-1)*b,2)
    assert 2-2*h-b == d*(2-2*g-b)
    assert h-g == (d-1)*(g-1+Q(b,2))
    assert h>=g
    count += 1
checks['horizontal_cover_arithmetic'] = count

# Reeb conformal-change equation in a symplectic two-plane, omega=dx wedge dy.
count = 0
for f,px,py,vx,vy in product(range(1,5),range(-2,3),range(-2,3),range(-2,3),range(-2,3)):
    zx,zy=Q(py,f*f),Q(-px,f*f)
    assert zx*vy-zy*vx == Q(px*vx+py*vy,f*f)
    count += 1
checks['conformal_reeb_linear_equations'] = count

samples=[]
for g in range(0,101):
    c_square=-(1-2*g)**2
    chi=2-2*g
    signature=-1
    d3=Q(c_square-2*chi-3*signature,4)
    assert d3 == -g*g+2*g-Q(1,2)
    assert -d3-Q(1,2) == g*g-2*g
    if g<=6:
        samples.append({'g':g,'d3':str(d3),'candidate_contact_grading':g*g-2*g})
checks['d3_arithmetic']={'cases':101,'samples':samples}

count=0
for m in range(0,21):
    c=1<<m
    mask=(1<<(m+1))-1
    assert ((c<<1)&mask)==0
    for d in range(m+3):
        # U^d image has monomial basis u^d,...,u^m.
        image_support=sum(1<<j for j in range(d,m+1))
        belongs = (c & ~image_support)==0
        assert belongs == (d<=m)
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
            assert total==b*n+12*sum(mask.bit_count()*s for mask,s in zip(subsets,multiplicities))
            assert n<=min(es)
            assert all(e>=0 and e%12==n%12 for e in es)
            assert length<=Q(total,min(b,12))
            candidates=[v for v in range(min(es)+1) if all((e-v)%12==0 for e in es)]
            sharper=max(Q(total,12)+v*(1-Q(b,12)) for v in candidates)
            assert length<=sharper
            count+=1
checks['capping_vector_factor_counts']=count

# Boundary twists around all boundaries at once are homologically trivial.
# Their capping vector would be (12,...,12), but they are not allowable factors.
for b in range(1,21):
    allowed=range(1,(1<<b)-1)
    assert ((1<<b)-1) not in allowed
checks['excluded_homologically_trivial_separating_types']=20

for h in range(0,10):
    for b in range(1,10):
        old_chi=2-2*h-b
        assert 2-2*h-(b+1)==old_chi-1
        if b>=2:
            assert 2-2*(h+1)-(b-1)==old_chi-1
checks['stabilization_euler_controls']=90

result={'status':'PASS','arithmetic_only':True,
        'does_not_prove_original_problem':True,'checks':checks}
print(json.dumps(result,indent=2,sort_keys=True))
