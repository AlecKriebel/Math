#!/usr/bin/env python3
"""Exact finite controls for the scoped lemmas, not a proof of an open problem."""
from fractions import Fraction as Q
from math import gcd
import json
from pathlib import Path


def add(a,b):
    out=dict(a)
    for m,v in b.items():out[m]=out.get(m,Q(0))+v
    return {m:v for m,v in out.items() if v}
def scale(a,c):return {m:c*v for m,v in a.items() if c*v}
def mul(a,b):
    out={}
    for m,v in a.items():
        for n,w in b.items():
            k=tuple(x+y for x,y in zip(m,n));out[k]=out.get(k,Q(0))+v*w
    return {m:v for m,v in out.items() if v}
def sub(a,b):return add(a,scale(b,-1))
def deriv(a):return {(m[0]-1,):m[0]*v for m,v in a.items() if m[0]}
def peval(a,x):return sum(v*x**m[0] for m,v in a.items())

def period_bound(d,periods,*,julia=True,excludes_rotation_boundaries=True):
    """Encoding of the asserted scope only; this is not a proof checker."""
    if d<2 or not julia or not excludes_rotation_boundaries:
        raise ValueError('The claimed bound does not apply to these inputs')
    if not periods or any(p<1 or int(p)!=p for p in periods):raise ValueError('bad period')
    L=1
    for p in periods:L=L*p//gcd(L,p)
    return {'iterate':L,'bound':d**L-1,'degree_only_invariant_bound':L==1}

def run():
    checks={}
    one={(0,0):Q(1)}; a={(1,0):Q(1)};r={(0,1):Q(1)}
    a2=mul(a,a);r2=mul(r,r)
    trace=sub(add(one,r2),a2)
    disc=sub(mul(trace,trace),scale(r2,4))
    factor=mul(sub(mul(sub(one,r),sub(one,r)),a2),sub(mul(add(one,r),add(one,r)),a2))
    assert disc==factor
    checks['reflection_discriminant_exact_identity']=True
    assert disc!=add(mul(trace,trace),scale(r2,4))
    checks['wrong_discriminant_mutation_rejected']=True
    cases=0
    for ai in range(20):
        for ri in range(1,20):
            av,rv=Q(ai,20),Q(ri,20)
            if av+rv<1:
                assert ((1-rv)**2-av**2)*((1+rv)**2-av**2)>0
                cases+=1
    checks['disjoint_circle_positive_discriminant_samples']=cases
    # B(z)=z^2(z-3)/(1-3z). The phase multiplier does not alter zeros of B'.
    num={(3,):Q(1),(2,):Q(-3)};den={(0,):Q(1),(1,):Q(-3)}
    derivative_num=sub(mul(deriv(num),den),mul(num,deriv(den)))
    expected={(3,):Q(-6),(2,):Q(12),(1,):Q(-6)}
    assert derivative_num==expected
    assert derivative_num!=scale(expected,-1)
    assert peval(num,Q(1,3))!=0 and peval(den,Q(1,3))==0
    checks['blaschke_derivative_exact']='-6*z*(z-1)^2/(1-3*z)^2'
    checks['blaschke_finite_pole']='1/3 (multiplicity 1); infinity has multiplicity 2'
    checks['blaschke_critical_multiplicity']=1+2+1
    assert checks['blaschke_critical_multiplicity']==2*3-2
    # Exact reciprocal identity B(z)B(1/z)=1 for the real coefficient model.
    def rev(poly,degree):return {(degree-m[0],):v for m,v in poly.items()}
    # Numerator and denominator of B(1/z), after multiplying by z^3.
    invnum=rev(num,3); invden=rev(den,3)
    assert mul(num,invnum)==mul(den,invden)
    checks['blaschke_circle_reflection_identity']=True
    # Fibonacci denominator controls supporting, but not replacing, the infinite proof.
    q=[1,1]
    for _ in range(1000):q.append(q[-1]+q[-2])
    assert all(q[n+2]>=2*q[n] for n in range(1000))
    assert all(q[n]<=2**n for n in range(1002))
    checks['golden_mean_denominator_recurrences_checked']=1000
    assert period_bound(3,[1,1])=={'iterate':1,'bound':2,'degree_only_invariant_bound':True}
    assert period_bound(3,[2,3])=={'iterate':6,'bound':728,'degree_only_invariant_bound':False}
    checks['period_scope_controls']=[period_bound(3,[1]),period_bound(3,[2]),period_bound(3,[2,3])]
    rejections=0
    for opts in [{'julia':False},{'excludes_rotation_boundaries':False}]:
        try:period_bound(3,[1],**opts)
        except ValueError:rejections+=1
    try:period_bound(1,[1])
    except ValueError:rejections+=1
    assert rejections==3
    checks['missing_hypothesis_controls_rejected']=rejections
    return {'result':'PASS','scope':'Exact finite algebra and scope controls only; no open-problem proof certification.','checks':checks}

if __name__=='__main__':
    result=run()
    print(json.dumps(result,indent=2,sort_keys=True))
