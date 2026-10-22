#!/usr/bin/env python3
"""Finite algebraic/numerical controls, never a proof of Problem 6.111."""
import cmath
import json
import math
from pathlib import Path
import random
from fractions import Fraction

ROOT=Path(__file__).resolve().parent
rng=random.Random(2306111)
checks={}

def sigma(d,q):
    a=abs(d)**2;b=4*abs(q)**2;c=2*(d*q.conjugate()).imag
    det=4*(d*q.conjugate()).real**2
    return math.sqrt(max(0,2*det/(a+b+math.hypot(a-b,2*c))))

def m(A,B,r):
    return math.exp(-A*r) if B==0 else math.exp((A-B)/B*math.log1p(-B*r))

# Exact rational identity underlying the operator norm for n>=2:
# cos^2+4 sin^2/n^2 <= cos^2+sin^2=1.
for n in range(2,1001):
    assert Fraction(4,n*n)<=1
checks['exact_rational_coefficient_factors_n_2_through_1000']=True

# Random finite-polynomial operator-norm and extremizer checks.
max_residual=0.; max_ratio=0.
for _ in range(1000):
    r=rng.uniform(.01,.999);z=cmath.rect(r,rng.uniform(-math.pi,math.pi));theta=rng.uniform(-math.pi,math.pi)
    c=[complex(rng.gauss(0,1),rng.gauss(0,1)) for _ in range(16)]
    norm=sum((n+2)*abs(v) for n,v in enumerate(c))
    L=sum(((n+2)*math.cos(theta)-2j*math.sin(theta))*v*z**(n+1) for n,v in enumerate(c))
    ratio=abs(L)/(r*norm);assert ratio<=1+1e-12;max_ratio=max(max_ratio,ratio)
    # Use a known convex quadratic f=z+a z^2, |a|<1/4.
    a=cmath.rect(rng.uniform(0,.24),rng.uniform(-math.pi,math.pi));d=1+2*a*z;q=1+a*z
    Lf=math.cos(theta)*d-2j*math.sin(theta)*q
    cc=-Lf/(2*z*cmath.exp(-1j*theta))
    Lg=math.cos(theta)*(d+2*cc*z)-2j*math.sin(theta)*(q+cc*z)
    max_residual=max(max_residual,abs(Lg))
    assert abs(Lg)<2e-12
    assert abs(2*abs(cc)-abs(Lf)/r)<2e-10
checks['1000_operator_norm_and_quadratic_witness_checks']={'max_norm_ratio':max_ratio,'max_zero_residual':max_residual}

# Independent sampled theta minimization must agree from above with the Gram value.
max_grid_gap=0.
for _ in range(25):
    d=complex(rng.uniform(.2,2),rng.uniform(-1,1));q=complex(rng.uniform(.2,2),rng.uniform(-1,1))
    exact_formula=sigma(d,q)
    sampled=min(abs(math.cos(math.pi*k/8192)*d-2j*math.sin(math.pi*k/8192)*q) for k in range(8192))
    assert sampled>=exact_formula-1e-10
    assert sampled-exact_formula<1e-4
    max_grid_gap=max(max_grid_gap,sampled-exact_formula)
checks['25_gram_vs_8192_angle_controls']={'maximum_gap':max_grid_gap}

# Distortion formula, B=0 continuity and scale compatibility in finite samples.
for A,B in [(.4,0),(.2,.1),(1,-1),(-.9,-1),(0,-1),(.5,-.97),(-.5,-.94),(.9,.8)]:
    delta=m(A,B,1)
    for r in [.01,.1,.5,.9,.99]:
        assert m(A,B,r)>delta>r*delta
        assert math.isclose(m(A*r,B*r,1),m(A,B,r),rel_tol=1e-13)
for B in [-1e-8,1e-8]:
    assert abs(m(.4,B,1)-math.exp(-.4))<2e-8
checks['distortion_B_zero_limit_and_scaling']=True

# Exact rational boundary checks for log model: delta=1/2,
# g_eta'(-r)=1/(1+r)-eta*r, eta=3/5; opposite signs inside D.
eta=Fraction(3,5)
assert 1/(1+Fraction(4,5))-eta*Fraction(4,5)>0
assert 1/(1+Fraction(9,10))-eta*Fraction(9,10)<0
r=(-3+math.sqrt(69))/6
assert .8<r<.9 and abs(1/(1+r)-.6*r)<1e-14
checks['exact_rational_upper_bound_counterexample_bracket']={'A':0,'B':-1,'eta':'3/5','root_bracket':['4/5','9/10'],'root_approximation':r}

# Radial extremal: d=m(r); q is positive and >=d. Simpson checks supplement proof.
for b in [.94,.97,1.]:
    for beta in [.1,.5,1.,1.5,1.9]:
        for r in [.1,.7,.99]:
            d=(1+b*r)**(-beta)
            q=math.log1p(b*r)/(b*r) if beta==1 else ((1+b*r)**(1-beta)-1)/(b*r*(1-beta))
            assert q>=d-1e-13
            assert math.isclose(sigma(complex(d),complex(q)),d,rel_tol=1e-12)
checks['45_radial_extremal_Gram_controls']=True
c0=(2+math.sqrt(3))/4
assert .933<c0<.934
for B in [-1,-.97,-.94]:
    R=c0/abs(B);assert c0<=R<1 and abs(R*B+c0)<1e-14
checks['subdisk_radius_scaling']=True
report={'problem_id':2306111,'result':'PASS','seed':2306111,'checks':checks,'limits':'Finite tests and exact rational identities only. No interval proof of the Janowski singular-value inequality, no complete literature audit, and no exhaustive measure search.'}
text=json.dumps(report,indent=2)+'\n'
print(text)
if '--write' in __import__('sys').argv:
    (ROOT/'CONTROL_RESULTS.json').write_text(text)
