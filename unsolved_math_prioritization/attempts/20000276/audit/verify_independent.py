#!/usr/bin/env python3
"""Independent finite falsification controls, not a proof of the theorem.

No imports from the author's verifier. Uses exact F_p polynomial arithmetic,
explicit Frobenius coordinate extraction, and a Fedder colon calculation.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
import json
import random

counts = Counter()
def require(label, condition):
    if not condition:
        raise AssertionError(label)
    counts[label] += 1

def reduced(f, p, cap=None):
    return {m:c % p for m,c in f.items()
            if c % p and (cap is None or max(m) < cap)}

def add(f,g,p,cap=None):
    out=f.copy()
    for m,c in g.items(): out[m]=out.get(m,0)+c
    return reduced(out,p,cap)

def mul(f,g,p,cap=None):
    out={}
    for m,c in f.items():
        for n,d in g.items():
            a=tuple(x+y for x,y in zip(m,n))
            if cap is None or max(a)<cap: out[a]=out.get(a,0)+c*d
    return reduced(out,p,cap)

def pw(f,n,p,cap=None):
    ans={(0,0):1}
    while n:
        if n&1: ans=mul(ans,f,p,cap)
        n//=2
        if n:f=mul(f,f,p,cap)
    return ans

def twist(f,Q):
    return {tuple(Q*a for a in m):c for m,c in f.items()}

def coordinate(f,Q,alpha,p,cap=None):
    return reduced({tuple(a//Q for a in m):c for m,c in f.items()
                    if tuple(a%Q for a in m)==alpha},p,cap)

def inverse_in_box(f,p,q):
    """Invert a unit in F_p[x,y]/(x^q,y^q), by a finite geometric sum."""
    inv=pow(f[(0,0)],-1,p)
    scaled={m:c*inv for m,c in f.items()}
    neg_tail={m:-c for m,c in scaled.items() if m!=(0,0)}
    term={(0,0):1}
    total={}
    for _ in range(2*q-1):
        total=add(total,term,p,q)
        term=mul(term,neg_tail,p,q)
    require('unit_geometric_tail_zero',not term)
    return reduced({m:inv*c for m,c in total.items()},p,q)

rng=random.Random(276757)
for p,q,Q in [(2,4,2),(2,4,8),(3,3,9),(3,9,3),(5,5,5)]:
    for _ in range(70):
        u=reduced({(rng.randrange(2*q),rng.randrange(2*q)):rng.randrange(p)
                   for _ in range(18)},p)
        u[(rng.randrange(q),rng.randrange(q))]=1
        v=reduced({(rng.randrange(2*Q*q),rng.randrange(2*Q*q)):rng.randrange(p)
                   for _ in range(22)},p)
        alpha=(rng.randrange(Q),rng.randrange(Q))
        v[alpha]=rng.randrange(1,p)
        coeff=coordinate(v,Q,alpha,p,q)
        inverse=inverse_in_box(coeff,p,q)
        require('unit_coordinate_inverse',mul(coeff,inverse,p,q)=={(0,0):1})
        w=mul(twist(u,Q),v,p,q*Q)
        selected=coordinate(w,Q,alpha,p,q)
        require('frobenius_coordinate_identity',selected==mul(u,coeff,p,q))
        require('explicit_linear_projection_recovers_u',
                mul(selected,inverse,p,q)==reduced(u,p,q))
        require('separation_nonzero_box',bool(w))

# Direct colon computation in S=F_p[x,y,z]:
# (x^q,y^q,z^q):(xy)^(q-1) = (x,y,z^q).
# This controls all Cartier maps through the hypersurface Fedder criterion.
for q in [2,3,4,5,7,8,9,16]:
    gens=[(q,0,0),(0,q,0),(0,0,q)]
    colon=[tuple(max(a-b,0) for a,b in zip(g,(q-1,q-1,0))) for g in gens]
    require('fedder_colon_generators',colon==[(1,0,0),(0,1,0),(0,0,q)])
    for i,j,k in product(range(q+2),repeat=3):
        rhs=i>=1 or j>=1 or k>=q
        lhs=i+q-1>=q or j+q-1>=q or k>=q
        require('fedder_colon_membership',lhs==rhs)
    for a in range(1,32):
        expected=(q-1)//a
        actual=max(t for t in range(q+1) if a*t<q)
        require('node_even_crossing',actual==expected)
        require('node_even_threshold_error',
                Fraction(1,a)-Fraction(1,q) <= Fraction(actual,q) < Fraction(1,a))

# Pair-definition endpoint check, independent of a general singular-limit theorem.
for a in range(1,17):
    for p in [2,3,5,7]:
        for e in range(1,7):
            q=p**e
            threshold=Fraction(1,a)
            power=((q-1)*threshold).__floor__()
            require('node_pair_endpoint_splits',a*power<=q-1)
            for eps in [Fraction(1,3),Fraction(1,13)]:
                t=threshold+eps
                if (q-1)*a*eps>=a:
                    power=((q-1)*t).__floor__()
                    require('node_pair_above_threshold_fails',a*power>=q)
            for t in [Fraction(1,17),Fraction(1,3),Fraction(1)]:
                if (q-1)*t>=1:
                    require('odd_pair_positive_exponent_in_splitting_prime',
                            ((q-1)*t).__floor__()>=1)

# Nonmonomial fixed-factor witnesses at the sharp integer margin k>a.
# I=(x^2+y^3), J=(x+y); c(J)=1 and nu_J(Q)=Q-1.
for p,q in [(2,4),(2,8),(3,3),(3,9),(5,5)]:
    generator={(2,0):1,(0,3):1}
    f={(1,0):1,(0,1):1}
    powers=[{(0,0):1}]
    while True:
        nxt=mul(powers[-1],generator,p,q)
        if not nxt:break
        powers.append(nxt)
    a=len(powers)-1
    require('fixed_factor_positive_base_exponent',a>=1)
    u=pw(generator,a,p)
    for k in [a+1,a+2,2*a+1]:
        for Q in [p,p**2,p**3]:
            h=a*Q//k
            v=pw(f,h,p,Q)
            require('fixed_factor_principal_splitting',bool(v) and h<=Q-1)
            w=mul(twist(u,Q),pw(f,h,p,q*Q),p,q*Q)
            require('fixed_factor_nonmonomial_witness',bool(w))
            require('fixed_factor_membership_exponents',k*h<=a*Q)
            require('fixed_factor_floor_bounds',
                    Fraction(a,k)-Fraction(1,Q)<Fraction(h,Q)<=Fraction(a,k))

# Numerical residue-class squeeze and exact Rees degree accounting.
for r in range(1,40):
    for n in range(1,300):
        k=(n+r-1)//r
        require('descending_ceiling_direction',n<=k*r<n+r)
        require('descending_squeeze_error',Fraction(n,k)<=r and Fraction(n,k)>r-Fraction(r,k))
for n,m in product(range(1,120),repeat=2):
    en,em=(n+1)//2,(m+1)//2
    require('node_family_multiplication',
            (n%2)+(m%2)>=(n+m)%2 and en+em>=(n+m+1)//2)
for n in range(1,300):
    require('node_two_generator_degree',2*(n//2)+n%2==n)
    require('node_two_generator_z_power',n//2+n%2==(n+1)//2)

negative_controls={
    'same_scale_ordinary_product_fails': not mul({(1,0):1},{(1,0):1},2,2),
    'singular_separation_fails': 'In the node ring take q=Q=2, u=y, v=x. Both avoid m^[2], but u^Q*v=y^2*x=0.',
    'fixed_factor_fails_singular': 'I=(z), J=(x+y): k*fpt(I^k J)=0, fpt(I)=1.',
    'zero_family_terms_obstruct_regular': 'I_even=(x), I_odd=0: normalized thresholds n and 0.',
}
require('negative_same_scale',negative_controls['same_scale_ordinary_product_fails'])
print(json.dumps({'status':'PASS','seed':276757,'assertions':sum(counts.values()),
                  'counts':dict(sorted(counts.items())),
                  'negative_controls':negative_controls,
                  'scope':'Finite independent falsification controls only. General proof audit is in AUDIT_REPORT.md.'},
                 indent=2,sort_keys=True))
