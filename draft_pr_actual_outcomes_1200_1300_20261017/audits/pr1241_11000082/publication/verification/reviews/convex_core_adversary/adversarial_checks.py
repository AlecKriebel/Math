#!/usr/bin/env python3
"""Exact finite boundary controls; no numeric certificate of an infinite claim."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

def mul(a,b):
    p,q,r,s=a; t,u,v,w=b
    return (p*t+q*v,p*u+q*w,r*t+s*v,r*u+s*w)
def inv(a):
    p,q,r,s=a
    assert p*s-q*r==1
    return s,-q,-r,p
def pw(a,n):
    if n<0: return pw(inv(a),-n)
    z=(1,0,0,1)
    while n:
        if n&1: z=mul(z,a)
        a=mul(a,a);n//=2
    return z
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
def tr(a):return a[0]+a[3]
def neg(a):return tuple(-v for v in a)
def inverse_word(w):return tuple(-v for v in w[::-1])
def word(e):
    w=(1,)
    for j,s in enumerate(e,1):
        u=w if s==1 else inverse_word(w)
        v=inverse_word(u)
        w=v+(2,)*(2*j)+u+(2,)*(2*j-1)+v+(2,)*(2*j)+u
    return w
def cyclic(w):
    z=[]
    for v in w:
        if z and z[-1]==-v:z.pop()
        else:z.append(v)
    i=0;j=len(z)
    while i<j and z[i]==-z[j-1]:i+=1;j-=1
    return tuple(z[i:j])
def least_rotation(w):
    # Booth algorithm, independently written for large exact word controls.
    n=len(w);v=w+w;a=0;b=1;t=0
    while a<n and b<n and t<n:
        if v[a+t]==v[b+t]:t+=1;continue
        if v[a+t]>v[b+t]:
            a+=t+1
            if a<=b:a=b+1
        else:
            b+=t+1
            if b<=a:b=a+1
        t=0
    a=min(a,b)
    return v[a:a+n]
def evaluate(w,a,b):
    lookup={1:a,-1:inv(a),2:b,-2:inv(b)}
    z=(1,0,0,1)
    for v in w:z=mul(z,lookup[v])
    return z
def y_syllables(w):
    # Rotate to x so an initial/final y run is counted as one cyclic syllable.
    start=next(i for i,v in enumerate(w) if abs(v)==1)
    w=w[start:]+w[:start]
    out=[];i=0
    while i<len(w):
        if abs(w[i])==2:
            s=w[i];j=i+1
            while j<len(w) and w[j]==s:j+=1
            out.append((1 if s>0 else -1)*(j-i));i=j
        else:i+=1
    return out

out={'scope':'Finite consistency and altered-hypothesis controls only.'}
count=0; qzero=0
for mu in (Q(-4),Q(0),Q(1),Q(2),Q(4),Q(3,2)):
    b=(1,0,-mu,1)
    for a,t,z in product(range(-2,3),repeat=3):
        c=mul(mul((1,a,0,1),(1,0,t,1)),(1,z,0,1))
        d=comm(b,c);p,q,r,s=c
        assert d==(1+mu*q*s,-mu*q*q,mu*(s*s-1)-mu*mu*q*s,1-mu*q*s+mu*mu*q*q)
        assert tr(d)==2+mu*mu*q*q
        if q==0:
            qzero+=1;assert tr(d)==2
        count+=1
out['generic_commutator']={'exact_cases':count,'q_zero_nongeneric_controls':qzero,'all_passed':True}

reps=[
    ((1,0,0,1),(1,0,0,1)),
    ((1,1,0,1),(1,3,0,1)),
    ((Q(2),0,0,Q(1,2)),(Q(3),0,0,Q(1,3))),
    ((1,4,0,1),(1,0,-4,1)),
    (neg((1,4,0,1)),(1,0,-4,1)),
    ((1,4,0,1),neg((1,0,-4,1))),
    (neg((1,4,0,1)),neg((1,0,-4,1))),
]
trace_levels=[];word_levels=[]
for m in range(1,7):
    words=[word(e) for e in product((-1,1),repeat=m)]
    cyc=[cyclic(w) for w in words]
    assert len({least_rotation(w) for w in cyc})==2**m
    for w in cyc:
        ys=y_syllables(w)
        assert ys.count(2*m-1)==1
        assert -(2*m-1) not in ys
        assert ys.count(4*m)==1
    word_levels.append({'m':m,'classes':2**m,'unique_positive_odd_marker':True,'unique_closing_4m_marker':True})
    if m<=4:
        assert all(len({tr(evaluate(w,a,b)) for w in words})==1 for a,b in reps)
        # A degenerate representation has trace 2 despite nontrivial words:
        # exact trace universality does not imply hyperbolicity by itself.
        assert {tr(evaluate(w,*reps[0])) for w in words}=={2}
        trace_levels.append(m)
out['horowitz_word_controls']=word_levels
out['trace_boundary_controls']={'levels':trace_levels,'representations':len(reps),'types':['trivial','commuting unipotent','rational diagonal','noncommuting integral','all three changes of generator lift signs'],'all_passed':True,'trivial_representation_produces_trace_2':True}

# Algebraic finite control for the normal-subgroup counterexample in the report:
# phi(b^n a b^-n)=0 but the centralizer-obstruction quotient n-m is nonzero.
out['normal_subgroup_control']={'indices_tested':list(range(-10,11)),'number_of_distinct_quotient_obstructions':len({n-m for n,m in product(range(-10,11),repeat=2) if n!=m}),'interpretation':'Illustrative quotient arithmetic; the infinite statement is proved in DERIVATIONS.md.'}
Path(__file__).with_name('adversarial_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_passed':True,'generic_commutator_cases':count,'largest_cyclic_word_family':64,'trace_boundary_representations':len(reps)}))
