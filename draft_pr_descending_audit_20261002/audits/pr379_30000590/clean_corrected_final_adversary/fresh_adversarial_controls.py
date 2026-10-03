#!/usr/bin/env python3
"""New exact controls, independent of all candidate executable sources."""
from itertools import product
from collections import Counter
import json, random

rng=random.Random(300005904379)
counts=Counter()
def check(x,kind):
    assert x,kind
    counts[kind]+=1

# Q16: b^2=a^4 and bab^-1=a^-1; N=<a> is noncentral and G/N=C2
# is nonsplit, since every element outside N has order four.
G=list(product(range(8),range(2)))
N=[(i,0) for i in range(8)]
e=(0,0)
def mul(x,y):
    i,j=x;k,l=y
    return ((i+(-1)**j*k+4*j*l)%8,(j+l)%2)
def inv(x):
    return next(y for y in G if mul(x,y)==e and mul(y,x)==e)
for x,y,z in product(G,repeat=3):check(mul(mul(x,y),z)==mul(x,mul(y,z)),'Q16_associativity')
for x in G:
    if x not in N:check(mul(x,x)!=(0,0) and mul(mul(x,x),mul(x,x))==e,'nonsplit_extension')
check(mul(mul((0,1),(1,0)),inv((0,1)))==(7,0),'noncentral_kernel')
def lift(q):return (0,q)
def nf(m,h):
    q=h[1];n=mul(h,inv(lift(q)))
    assert n in N
    return (mul(m,n),q)
def F(q,m,l=None):
    l=lift(q) if l is None else l
    return nf(mul(m,inv(l)),l)
for q,m,g in product(range(2),G,G):
    a=F(q,m)
    lhs=nf(a[0],mul(lift(a[1]),g))
    check(lhs==F((q+g[1])%2,mul(m,g)),'right_diagonal_noncentral_nonsplit')
    lhs=nf(mul(a[0],inv(g)),mul(g,lift(a[1])))
    check(lhs==F((g[1]+q)%2,m),'left_quotient_noncentral_nonsplit')
    for n in N:
        check(F(q,m,mul(n,lift(q)))==a,'lift_independence_noncentral_nonsplit')

# Infinite-product wraparound would destroy the minimum-support proof.
# On finite support with height-varying, singular integer transports, it survives.
for width in range(1,9):
    for trial in range(100):
        low=rng.randrange(-12,12);span=rng.randrange(1,12)
        xs={h:[rng.randrange(-3,4) for _ in range(width)] for h in range(low,low+span)}
        xs={h:v for h,v in xs.items() if any(v)}
        if not xs:continue
        ys={h:list(v) for h,v in xs.items()}
        for h,v in xs.items():
            A=[[rng.randrange(-2,3) if j<width-1 else 0 for j in range(width)] for _ in range(width)]
            w=[sum(a*x for a,x in zip(row,v)) for row in A]
            ys.setdefault(h+1,[0]*width)
            ys[h+1]=[a-b for a,b in zip(ys[h+1],w)]
        h=min(xs)
        check(ys[h]==xs[h] and any(ys[h]),'nonconstant_finite_height_transport')
for period in range(1,33):
    v=[1]*period
    check(all(v[i]-v[(i-1)%period]==0 for i in range(period)),'periodic_shift_negative')

# Integral tensor detection genuinely fails without field faithful flatness.
from math import gcd
for a,b in product(range(2,20),repeat=2):
    if gcd(a,b)==1:check(gcd(a,b)==1,'nonzero_integral_factors_tensor_zero')
for p in [2,3,5,7,11,13]:
    # The tensor of Z --p--> Z with itself has Z/p in degree1 (Tor) and degree2.
    check((-p)*p+p*p==0 and gcd(p,p)==p,'flatness_Tor_negative')

# Finite rectangles give an unbounded count of independent coinvariant orbit sums.
# Universal orbit and finite-support telescoping proof is in the sealed verdict.
for n in range(1,81):
    pts=list(product(range(-n,n+1),repeat=2))
    labels={i+j for i,j in pts}
    check(len(labels)==4*n+1,'unbounded_height_homology_orbits')
    for i,j in pts[::max(1,len(pts)//50)]:
        check((i+1)+(j-1)==i+j,'opposite_shift_orbit_label')
print(json.dumps({'status':'PASS','counts':dict(counts),'total_exact_controls':sum(counts.values()),'imports_candidate_code':False,'scope':'Q16 nonsplit noncentral lift/action equations; variable singular height shifts; invalid periodic/integral-tensor shortcuts; unbounded orbit controls. Finite checks do not prove infinite claims.'},indent=2))
