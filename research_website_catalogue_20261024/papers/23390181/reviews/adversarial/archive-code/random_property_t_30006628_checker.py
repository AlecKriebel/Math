#!/usr/bin/env python3
"""Exact finite diagnostics for the candidate FPD Property-(T) proof.
Not a formal proof checker. Python 3, standard library only; no assertions.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import argparse, json, sys

class Failure(Exception): pass

def require(c, msg):
    if not c: raise Failure(msg)

def alphabet(sizes):
    colors = tuple(i for i,n in enumerate(sizes) for _ in range(n))
    inv=[]; off=0
    for n in sizes:
        # Odd part sizes have one self-inverse letter, the others inverse pairs.
        for j in range(n):
            inv.append(off+(j if n%2 and j==n-1 else j^1))
        off+=n
    require(all(inv[inv[a]]==a and colors[inv[a]]==colors[a] for a in range(len(inv))), 'bad involution')
    return colors, tuple(inv)

def inverse(w, inv): return tuple(inv[x] for x in reversed(w))

def words(colors, t):
    out=[(a,) for a in range(len(colors))]
    for _ in range(1,t):
        out=[w+(a,) for w in out for a in range(len(colors)) if colors[w[-1]]!=colors[a]]
    return out

def parts(ell):
    k,r=divmod(ell,3)
    return (k,k,k) if r==0 else ((k,k,k+1) if r==1 else (k,k+1,k+1))

def coefficients(lens):
    out=Counter()
    for j in range(3):
        t,u=lens[j],lens[(j+1)%3]
        out[t,u]+=1;out[u,t]+=1
    return out

def aggregate(sizes,ell,mutate=None):
    colors,inv=alphabet(sizes); lens=parts(ell); ts=sorted(set(lens))
    ws={t:words(colors,t) for t in ts}
    good={t:[w for w in ws[t] if inverse(w,inv)!=w] for t in ts}
    vertex={(t,w):(t,w[0],w[-1]) for t in ts for w in good[t]}
    counts=Counter(vertex.values()); actual=Counter(); good_rel=0; total=0
    # Exhaustive cyclic words, not a random sample.
    for rel in words(colors,ell):
        if colors[rel[0]]==colors[rel[-1]]:continue
        total+=1; i=0;bs=[]
        for t in lens:bs.append(rel[i:i+t]);i+=t
        if any(inverse(w,inv)==w for w in bs):continue
        good_rel+=1
        for j in range(3):
            t,u=lens[j],lens[(j+1)%3]
            x,y=inverse(bs[j],inv),bs[(j+1)%3]
            a,b=vertex[t,x],vertex[u,y]
            actual[a,b]+=1;actual[b,a]+=1
    c=coefficients(lens)
    if mutate=='missing_edge':
        # Remove two oriented counts from one length-pair family.
        pair=next(iter(c)); c[pair]-=1
    expected=Counter(); completion={}
    for h in ts:
        for b,d in product(range(len(colors)),repeat=2):
            completion[h,b,d]=sum(colors[b]!=colors[w[0]] and colors[w[-1]]!=colors[d] for w in good[h])
    for a,b in product(counts,repeat=2):
        t,af,al=a;u,bf,bl=b
        if not c[t,u]:continue
        h=ell-t-u
        comp=(colors[af]!=colors[bf])
        if mutate=='wrong_boundary':comp=True
        n=counts[a]*counts[b]*c[t,u]*int(comp)*completion[h,al,bl]
        if n:expected[a,b]=n
    require(dict(actual)==dict(expected),'exact expected-link kernel mismatch')
    require(sum(actual.values())==6*good_rel,'six oriented edge occurrences per retained relator')
    # Inversion orbit counts and the endpoint-size symmetry used in compression.
    require(all(vertex.get((t,inverse(w,inv))) is not None for t in ts for w in good[t]), 'inverse closure')
    return {'sizes':sizes,'ell':ell,'parts':lens,'cyclic_relators':total,'retained_relators':good_rel,
            'vertices':len(vertex),'endpoint_classes':len(counts),'kernel_exact':True},counts,actual

def positive_definite(M):
    # Rational LDL elimination with strictly positive pivots (Sylvester criterion).
    a=[[F(x) for x in row] for row in M];n=len(a)
    if any(a[i][j]!=a[j][i] for i in range(n) for j in range(n)):return False
    for k in range(n):
        p=a[k][k]
        if p<=0:return False
        for i in range(k+1,n):
            for j in range(i,n):
                z=a[i][j]-a[i][k]*a[j][k]/p
                a[i][j]=z;a[j][i]=z
    return True

def strict_gap_half(adj):
    n=len(adj);deg=[sum(r) for r in adj];vol=sum(deg)
    if not vol or min(deg)<=0:return False
    # 2L-D+2dd'/vol is positive definite iff normalized Laplacian gap >1/2.
    m=[[(deg[i] if i==j else 0)-2*adj[i][j]+F(2*deg[i]*deg[j],vol)
        for j in range(n)] for i in range(n)]
    return positive_definite(m)

def limit_check(n,unequal):
    q=[[F(1)]] if not unequal else [[F(1,2),F(1,2)],[F(1),F(0)]]
    pi=[F(1)] if not unequal else [F(2,3),F(1,3)]
    labels=list(product(range(len(q)),range(n)))
    a=[[pi[t]*F(1,n)*q[t][u]*(F(1,n-1) if i!=j else 0)
        for u,j in labels] for t,i in labels]
    return strict_gap_half(a)

def run(mutant=None):
    if mutant:
        if mutant in ('missing_edge','wrong_boundary'):aggregate((1,1,1),7,mutant)
        elif mutant=='two_factor_strict':require(limit_check(2,True),'two-factor strict gap is false')
        elif mutant=='critical_density':require(F(1,3)>F(1,3),'density exponent must be positive')
        else:raise Failure('unknown mutant')
        raise Failure('negative control failed to trip')
    tests=[]
    for sizes,ells in [((1,1,1),range(6,15)),((1,1,2),range(6,10))]:
        for ell in ells:
            rec,counts,adj=aggregate(sizes,ell)
            labs=sorted(counts);mat=[[adj[a,b] for b in labs] for a in labs]
            rec['finite_mean_gap_strictly_above_half']=strict_gap_half(mat)
            tests.append(rec)
    require(all(limit_check(n,u) for n in range(3,9) for u in (False,True)),'limiting spectral certificate')
    require(not limit_check(2,True),'n=2 boundary negative control')
    require(F(2,5)-F(1,3)>0,'supercritical exponent')
    # Finite-index cancellation witnesses with both endpoints outside the two forbidden colors.
    colors,inv=alphabet((1,1,1))
    witnesses=0
    for t in range(4,10):
        for a,b in product(range(3),repeat=2):
            choices=[v for v in words(colors,t-1) if colors[v[0]] not in (colors[a],colors[inv[b]])
                     and inverse((a,)+v,inv)!=(a,)+v and inverse((inv[b],)+v,inv)!=(inv[b],)+v]
            require(bool(choices),'missing finite-index witness');witnesses+=1
    return {'status':'PASS','kind':'exact finite diagnostics, not formal proof certification',
            'kernel_cases':tests,'finite_index_witnesses':witnesses,'limit_cases':12,
            'negative_controls_required':['missing_edge','wrong_boundary','two_factor_strict','critical_density']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mutant');a=p.parse_args()
    try:print(json.dumps(run(a.mutant),sort_keys=True,indent=2))
    except Failure as e:print(json.dumps({'status':'REJECTED','reason':str(e)}));sys.exit(1)
