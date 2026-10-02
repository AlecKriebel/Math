#!/usr/bin/env python3
"""Exact controls for Turn 1. No random matrices or floating-point arithmetic."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import comb
from collections import Counter
import json
import sympy as sp

COUNTS=Counter()
def check(group, condition):
    if not condition:
        raise AssertionError(group)
    COUNTS[group]+=1

def compositions(n,k):
    if k==0:
        if n==0: yield ()
        return
    for a in range(n+1):
        for tail in compositions(n-a,k-1): yield (a,)+tail

def cumulants(mom):
    k=[0]*len(mom)
    for n in range(1,len(mom)):
        subtotal=0
        for j in range(1,n):
            subtotal+=k[j]*sum(product_values(mom[a] for a in comp)
                                for comp in compositions(n-j,j))
        k[n]=sp.expand(mom[n]-subtotal)
    return k

def product_values(xs):
    out=1
    for x in xs: out*=x
    return out

def moments(k):
    m=[1]+[0]*(len(k)-1)
    for n in range(1,len(k)):
        m[n]=sp.expand(sum(k[j]*sum(product_values(m[a] for a in comp)
                                    for comp in compositions(n-j,j))
                           for j in range(1,n+1)))
    return m

def word_evaluator(ka,kb):
    @lru_cache(None)
    def ev(word):
        if not word: return 1
        possible=[j for j in range(1,len(word)) if word[j]==word[0]]
        out=0
        for size in range(len(possible)+1):
            for tail in combinations(possible,size):
                block=(0,)+tail
                value=(ka if word[0]==0 else kb)[len(block)]
                for left,right in zip(block,block[1:]+(len(word),)):
                    value*=ev(word[left+1:right])
                out+=value
        return out
    return ev

p,t,b1,b2,b3=sp.symbols('p t b1 b2 b3')
kp=cumulants([1]+[p]*6)
check('projection_cumulant_2',sp.expand(kp[2]-p*(1-p))==0)
check('projection_cumulant_4',sp.expand(kp[4]-(t*(1-5*t)).subs(t,p*(1-p)))==0)
check('projection_cumulant_6',sp.expand(kp[6]-(t*(1-14*t+42*t*t)).subs(t,p*(1-p)))==0)
check('projection_moment_roundtrip',moments(kp)==[1]+[p]*6)
kd=[0,0,2*t,0,2*t*(1-5*t),0,2*t*(1-14*t+42*t*t)]
md=moments(kd)
target=[1,2*t,2*t-2*t*t,2*t-4*t*t+4*t**3]
for n in range(1,4):
    check('difference_moment_identity',sp.expand(md[2*n]-target[n])==0)

# Direct noncommutative commutator expansion: i(PU-UP), then freeness.
# For fixed power n<=6 its polynomial degree in p is at most n, so seven
# distinct rational values also give an exact polynomial interpolation check.
ku=cumulants([1]+[int(n%2==0) for n in range(1,7)])
values={n:[] for n in range(1,7)}
for pv in [F(j,6) for j in range(7)]:
    ka=[v.subs(p,sp.Rational(pv.numerator,pv.denominator)) if hasattr(v,'subs') else v for v in kp]
    ev=word_evaluator(ka,ku)
    for n in range(1,7):
        value=0
        for choices in product([0,1],repeat=n):
            word=tuple(x for c in choices for x in ((0,1) if c==0 else (1,0)))
            value+=(-1)**sum(choices)*ev(word)
        value=sp.expand(sp.I**n*value)
        expected=0 if n%2 else target[n//2].subs(t,pv*(1-pv))
        check('direct_free_word_commutator',value==expected)
        values[n].append((sp.Rational(pv.numerator,pv.denominator),value))
for n in range(1,7):
    polynomial=sp.interpolate(values[n],p)
    expected=0 if n%2 else target[n//2].subs(t,p*(1-p))
    check('exact_interpolation_degree_bound',sp.expand(polynomial-expected)==0)

# Obtain alternating AB moments from colored noncrossing partitions.
arcsine=[1,2,6,20]
for n in range(1,4): check('arcsine_moments',arcsine[n]==comb(2*n,n))
ka=cumulants(arcsine);kb=cumulants([1,b1,b2,b3]);ev=word_evaluator(ka,kb)
formulas=[1,2*b1,4*b2+2*b1*b1,8*b3+12*b1*b2]
for n in range(1,4):
    check('free_product_moment_identity',sp.expand(ev((0,1)*n)-formulas[n])==0)
sol={b1:t,b2:t/2-t*t,b3:t/4-5*t*t/4+2*t**3}
for n in range(1,4):
    check('forced_factor_moments',sp.expand(formulas[n].subs(sol)-target[n])==0)
det=sp.factor((b1*b3-b2*b2).subs(sol))
check('shifted_hankel_identity',sp.expand(det-t**3*(t-sp.Rational(1,4)))==0)
certificate=sp.expand(sol[b3]-2*(sp.Rational(1,2)-t)*sol[b2]+(sp.Rational(1,2)-t)**2*sol[b1])
check('nonnegative_polynomial_certificate',sp.factor(certificate)==t*t*(4*t-1)/4)
check('strict_sign_parameter_identity',sp.expand(p*(1-p)-sp.Rational(1,4)+(p-sp.Rational(1,2))**2)==0)
for denominator in range(2,41):
    for numerator in range(1,denominator):
        pv=F(numerator,denominator);tv=pv*(1-pv)
        value=tv**3*(tv-F(1,4))
        check('rational_sign_controls',value==0 if pv==F(1,2) else value<0)
        check('reflection_control',tv==(1-pv)*pv)
for n in range(1,4):
    check('symmetric_boundary_delta',sp.expand(sol[[b1,b2,b3][n-1]].subs(t,sp.Rational(1,4))-sp.Rational(1,4)**n)==0)
    check('deterministic_boundary_delta',sol[[b1,b2,b3][n-1]].subs(t,0)==0)

print(json.dumps({'problem_id':30004022,'turn':1,'status':'PASS',
    'counts':dict(sorted(COUNTS.items())),'exact_assertions':sum(COUNTS.values()),
    'forced_factor_moments':[str(sol[x]) for x in (b1,b2,b3)],
    'shifted_hankel_determinant':str(det),
    'scope':'Checks the stated partial fixed-arcsine-factor obstruction. Full nonsymmetric source representation problem remains unresolved; no novelty or independent review claimed.',
    'arithmetic':'exact rational arithmetic and symbolic polynomial identities'},indent=2,sort_keys=True))
