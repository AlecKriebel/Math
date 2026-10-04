#!/usr/bin/env python3
"""Finite exact and numerical controls, not a proof of the open problem.
Python 3.10+ standard library only. No network, external inputs, or writes.
"""
from fractions import Fraction as Q
from math import atan, pi, sqrt, sin, exp
import cmath
import json

# Gaussian rational arithmetic and univariate polynomial arithmetic.
def ga(a=0,b=0): return (Q(a),Q(b))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def sub(a,b): return add(a,neg(b))
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a): return (a[0],-a[1])
def div(a,b):
    d=b[0]*b[0]+b[1]*b[1]
    assert d
    c=mul(a,conj(b)); return (c[0]/d,c[1]/d)
def scale(a,q): return (a[0]*q,a[1]*q)
ZERO,ONE,I=ga(),ga(1),ga(0,1)
def padd(p,q):
    r=[ZERO]*max(len(p),len(q))
    for j,v in enumerate(p): r[j]=add(r[j],v)
    for j,v in enumerate(q): r[j]=add(r[j],v)
    return r

def pmul(p,q):
    r=[ZERO]*(len(p)+len(q)-1)
    for j,a in enumerate(p):
        for k,b in enumerate(q): r[j+k]=add(r[j+k],mul(a,b))
    return r

def peval(p,z):
    r=ZERO
    for a in reversed(p): r=add(mul(r,z),a)
    return r

# Two-variable Gaussian polynomials for exact degree and cleared identities.
def badd(p,q):
    r=p.copy()
    for k,v in q.items(): r[k]=add(r.get(k,ZERO),v)
    return {k:v for k,v in r.items() if v!=ZERO}
def bmul(p,q):
    r={}
    for (j,k),a in p.items():
        for (l,m),b in q.items():
            e=(j+l,k+m); r[e]=add(r.get(e,ZERO),mul(a,b))
    return {k:v for k,v in r.items() if v!=ZERO}
def bconj(p): return {k:conj(v) for k,v in p.items()}
def to_bivar(p):
    z={(1,0):ONE,(0,1):I}; power={(0,0):ONE}; r={}
    for a in p:
        r=badd(r,{k:mul(a,v) for k,v in power.items()})
        power=bmul(power,z)
    return r

def beval(p,x,y):
    r=ZERO
    for (j,k),v in p.items():r=add(r,scale(v,x**j*y**k))
    return r

checks={}
# Cayley inverse, membership in D, and the single-atom circle equation.
num=0
for s in [Q(1,4),Q(1),Q(4)]:
    for y in [Q(-5),Q(-1,3),Q(0),Q(7,2)]:
        w=ga(s,y); z=div(sub(w,ONE),add(w,ONE)); W=div(add(ONE,z),sub(ONE,z))
        assert W==w
        norm=z[0]**2+z[1]**2
        assert 1-norm==4*s/((s+1)**2+y*y)>0
        assert (z[0]-s/(s+1))**2+z[1]**2==1/(s+1)**2
        num+=1
checks['cayley_and_single_atom_exact_cases']=num

# Finite Herglotz numerators. Algebraic-degree checks are not length estimates
# on arbitrary transcendental limits.
degrees=[]
for n in range(1,9):
    atoms=[]
    for j in range(1,n+1):
        t=Q(j,9); zeta=ga((1-t*t)/(1+t*t),2*t/(1+t*t)); a=Q(1,2**j)
        assert zeta[0]**2+zeta[1]**2==1
        atoms.append((a,zeta))
    P=[ZERO]; R=[ONE]
    for a,zeta in atoms:
        den=[zeta,neg(ONE)]; nom=[scale(zeta,a),ga(a)]
        P=padd(pmul(P,den),pmul(nom,R)); R=pmul(R,den)
    pb,rb=to_bivar(P),to_bivar(R)
    product=bmul(pb,bconj(rb)); modulus=bmul(rb,bconj(rb)); s=Q(1,3)
    level=badd({k:ga(v[0]) for k,v in product.items()}, {k:scale(v,-s) for k,v in modulus.items()})
    assert level and all(v[1]==0 for v in level.values())
    degree=max(sum(k) for k in level); assert degree<=2*n
    for z in [ga(0),ga(Q(1,4),Q(1,3)),ga(Q(-1,2),Q(1,5))]:
        H=ZERO
        for a,zeta in atoms:H=add(H,scale(div(add(zeta,z),sub(zeta,z)),a))
        assert div(peval(P,z),peval(R,z))==H
        q=peval(R,z); expected=(q[0]**2+q[1]**2)*(H[0]-s)
        assert beval(level,z[0],z[1])==ga(expected)
    degrees.append({'atoms':n,'degree':degree,'bound':2*n})
checks['finite_herglotz_exact_clearing']=degrees

# Exact tail bounds with a_j=2^-j. These illustrate deterioration near boundary.
tails=[]
for k in [1,2,4,8]:
    r=1-Q(1,2**k); n=4*k; tail=Q(1,2**n)
    tails.append({'radius':str(r),'N':n,'tail':str(tail),
        'function_bound':str((1+r)/(1-r)*tail),
        'derivative_bound':str(2*tail/(1-r)**2)})
checks['exact_tail_bounds']=tails
checks['harmonic_lower_sums']=[{'N':n,'sum_fraction':str(sum((Q(1,2*k+1) for k in range(n)),Q(0)))} for n in [1,4,16,64]]

# Floating diagnostics only. They are not interval proofs of identities,
# connectivity, total length, or asymptotic divergence.
residual=0.0
for k in range(-4,5):
    b=pi*(k+0.5)
    for x in [0.25,1.0,4.0]:
        w=complex(x,b); z=(w-1)/(w+1)
        f=cmath.exp(cmath.exp(-(1+z)/(1-z)))
        residual=max(residual,abs(abs(f)-1))
assert residual<1e-12
checks['floating_modulus_one_max_residual']=residual
checks['component_lengths_formula']=[{'k':k,'length':2*atan(pi*(k+0.5))/(pi*(k+0.5)),'proved_lower_bound':1/(2*k+1)} for k in [0,1,4,16,64]]
checks['regular_approximant_total_length_lower_bounds']=[{'n':n,'lower_bound':2*n*(1-exp(-n))} for n in [1,2,4,8,16]]
chord_sums=[]
for N in [8,32,128,512]:
    ts=[sqrt(pi/2+n*pi) for n in range(1,N+2)]
    points=[complex(1-1/t,sin(t*t)/t) for t in ts]
    assert all(abs(z)<1 for z in points)
    assert all(points[j].real<points[j+1].real for j in range(len(points)-1))
    lower=sum(1/ts[j]+1/ts[j+1] for j in range(N))
    chords=sum(abs(points[j+1]-points[j]) for j in range(N))
    assert chords+1e-10>=lower
    chord_sums.append({'N':N,'vertical_lower_sum':lower,'chord_sum':chords})
checks['oscillatory_arc_floating_diagnostics']=chord_sums
print(json.dumps({'passed':True,'arithmetic':'Fraction exact where labeled; IEEE-754 floating diagnostics otherwise','limits':'Finite controls only. Infinite divergence, analytic topology, Crofton, and componentwise claims require the written proofs. No numerical experiment solves Problem 5.70.','checks':checks},indent=2,sort_keys=True))
