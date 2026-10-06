#!/usr/bin/env python3
"""Independent exact finite diagnostics for the four-adic candidate."""
from fractions import Fraction as Q
from collections import Counter
from itertools import product
from math import comb
from pathlib import Path
import hashlib,json
counts={}
def ck(name,b):
    assert b,name
    counts[name]=counts.get(name,0)+1

# Compute the middle pair directly from its required sum, not by importing
# the author's search implementation. A zero sum chooses (-1,+1).
def split(left,v,right):
    if not v:return (0,0,0,0)
    e=1 if left>=v else -1
    f=1 if right>v else -1
    s=-(e+f)
    middle={-2:(-1,-1),0:(-1,1),2:(1,1)}[s]
    return (v+e,v+middle[0],v+middle[1],v+f)
def step(v):
    n=len(v)
    return [x for j in range(n) for x in split(v[(j-1)%n],v[j],v[(j+1)%n])]

# Facing-sign cases include large base heights and each allowed signed gap.
for a in (0,1,2,3,10,101):
    for d in (-2,-1,0,1,2):
        b=a+d
        if b<0:continue
        for ld,rd in product((-2,-1,0,1,2),repeat=2):
            left,right=a+ld,b+rd
            if min(left,right)<0:continue
            A=split(left,a,b);B=split(a,b,right)
            ck('facing_neighbor_bound',abs(A[-1]-B[0])<=2)
            ck('mass_and_nonnegativity',sum(A)==4*a and min(A)>=0)
            if a:ck('unit_steps_and_fairness',sorted(x-a for x in A)==[-1,-1,1,1])

levels=[[1]]
for n in range(8):
    v=levels[n];N=4**n
    ck('stage_probability_mass',sum(v)==N)
    ck('stage_growth_bound',max(v)<=n+1 and min(v)>=0)
    ck('walk_survival_formula',sum(x>0 for x in v)==2**n*comb(n,n//2))
    for j,x in enumerate(v):
        ck('every_cyclic_edge',abs(x-v[(j+1)%N])<=2)
    if n<7:
        w=step(v)
        for j,x in enumerate(v):
            ck('every_parent_consistency',sum(w[4*j:4*j+4])==4*x)
            ck('every_parent_absorption',(w[4*j:4*j+4]==[0]*4) if x==0 else all(abs(t-x)==1 for t in w[4*j:4*j+4]))
        levels.append(w)

# Exact primitives with prefix sums, at translated rational points.
def prim(v):
    N=len(v);s=[0]
    for x in v:s.append(s[-1]+x-1)
    def f(x):
        x=Q(x);x-=x.numerator//x.denominator
        q=x*N;j=q.numerator//q.denominator
        return Q(s[j],N)+(x-Q(j,N))*(v[j]-1)
    return f
for n in range(1,5):
    v,w=levels[n],levels[n+1];N=len(v)
    P,R=prim(v),prim(w)
    for j in range(4*N+1):
        x=Q(j,4*N)
        ck('uniform_primitive_increment',abs(R(x)-P(x))<=Q(1,N))
    for denominator in (3,5,7):
        for k in range(-2,10):
            x=Q(k,denominator)
            for h in (Q(1,4*N),Q(1,N),Q(3,2*N),Q(1,4),Q(1,3),Q(2,3)):
                ck('arbitrary_arc_second_difference',abs(P(x+h)+P(x-h)-2*P(x))<=24*h)

# Midpoint coupling from each finer atomic measure to a coarser one.
for n in range(4):
    N=4**n
    for m in range(n+1,6):
        M=4**m;v=levels[m];block=M//N
        cost=Q(0)
        for j,x in enumerate(v):
            child=Q(2*j+1,2*M);parent=Q(2*(j//block)+1,2*N)
            cost+=Q(x,M)*abs(child-parent)
        ck('exact_midpoint_transport_cost',cost<=Q(1,2*N))
        for j in range(N):
            ck('atomic_coarse_mass',sum(v[j*block:(j+1)*block])==block*levels[n][j])

# An independent nonconstancy witness: mass 3/4 lies where sin(4*pi*x)>=sqrt(2)/2.
v=levels[2]
ck('second_fourier_nonzero_mass',sum(v[j] for j in (1,2,9,10))==12)
ck('all_mass_in_positive_sine_arcs',all(v[j]==0 for j in range(16) if j not in (0,1,2,3,8,9,10,11)))

# Gaussian-rational arithmetic: exact first approximants B0=-z, B1=-i*z^2.
def plus(z,w):return (z[0]+w[0],z[1]+w[1])
def neg(z):return (-z[0],-z[1])
def sub(z,w):return plus(z,neg(w))
def mul(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def div(z,w):
    den=w[0]**2+w[1]**2;assert den
    return ((z[0]*w[0]+z[1]*w[1])/den,(z[1]*w[0]-z[0]*w[1])/den)
one=(Q(1),Q(0));ii=(Q(0),Q(1))
for x,y in product(range(-3,4),repeat=2):
    z=(Q(x,5),Q(y,5))
    if z[0]**2+z[1]**2>=1:continue
    F0=div(sub(one,z),plus(one,z))
    ck('first_rational_inner_formula',div(sub(F0,one),plus(F0,one))==neg(z))
    zz=mul(z,z);F1=div(plus(ii,zz),sub(ii,zz))
    ck('second_rational_inner_formula',div(sub(F1,one),plus(F1,one))==mul(neg(ii),zz))
    ck('finite_positive_real_parts',F0[0]>0 and F1[0]>0)
    # Difference of Cayley transforms: exact identity used in the error estimate.
    lhs=sub(div(sub(F0,one),plus(F0,one)),div(sub(F1,one),plus(F1,one)))
    rhs=div(mul((Q(2),Q(0)),sub(F0,F1)),mul(plus(F0,one),plus(F1,one)))
    ck('cayley_difference_identity',lhs==rhs)

# Unit increments cannot converge to any positive constant, unlike shrinking increments.
for v in range(1,10):
    ck('positive_integer_step_separation',all(abs((v+e)-v)==1 for e in (-1,1)))
ck('tail_geometric_constant',sum(Q(1,4**k) for k in range(20))<Q(4,3))
receipt={'status':'PASS','assertions_passed':sum(counts.values()),'by_category':counts,
         'maximum_stage':7,'maximum_cells':4**7,
         'scope':'Finite exact diagnostics; analytic boundary and factorization conclusions are proved in the review, not inferred from samples.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
