#!/usr/bin/env python3
"""Exact, modest finite controls. Python 3 standard library only.
No numerical experiment proves the universal statements in the turn files.
Run: python3 verify.py; python3 verify.py --check
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from math import comb
from pathlib import Path
import argparse, json

# Polynomials use {nonnegative exponent: integer coefficient}.
def clean(a): return {k:v for k,v in a.items() if v}
def add(a,b):
    c=dict(a)
    for k,v in b.items(): c[k]=c.get(k,0)+v
    return clean(c)
def scale(a,t): return clean({k:t*v for k,v in a.items()})
def shift(a,k):
    assert all(d+k>=0 for d in a)
    return {d+k:v for d,v in a.items()}
def mul(a,b):
    c={}
    for i,u in a.items():
        for j,v in b.items(): c[i+j]=c.get(i+j,0)+u*v
    return clean(c)
def power(a,n):
    r={0:1}
    for _ in range(n): r=mul(r,a)
    return r
def evaluate(a,q): return sum(v*q**k for k,v in a.items())
def divide_monic(a,b):
    a=dict(a); out={}; d=max(b); assert b[d]==1
    while a and max(a)>=d:
        k=max(a)-d; v=a[k+d]; out[k]=v
        a=add(a,scale(shift(b,k),-v))
    assert not a, ('nonzero remainder',a)
    return out

def components(n,edges,vertices=None,complement=False):
    vertices=set(range(n)) if vertices is None else set(vertices)
    es={tuple(sorted(e)) for e in edges}; unseen=set(vertices); c=0
    while unseen:
        c+=1; frontier=[unseen.pop()]
        while frontier:
            u=frontier.pop()
            nxt=[v for v in unseen if ((tuple(sorted((u,v))) in es) != complement)]
            for v in nxt: unseen.remove(v); frontier.append(v)
    return c

def maximum_matching(n,edges):
    adj=[0]*n
    for a,b in edges: adj[a]|=1<<b; adj[b]|=1<<a
    @lru_cache(None)
    def rec(mask):
        if not mask:return 0
        low=mask&-mask; u=low.bit_length()-1; rest=mask^low
        best=rec(rest); options=adj[u]&rest
        while options:
            b=options&-options; options-=b
            best=max(best,1+rec(rest^b))
        return best
    return rec((1<<n)-1)

def p_polynomial(n,edges):
    out={}
    for mask in range(1,1<<n):
        S=[v for v in range(n) if mask>>v&1]
        c=components(n,edges,S,True)
        if c>=2:
            term={j-1:comb(c-1,j) for j in range(1,c)}
            out=add(out,mul(power({0:-1,1:1},len(S)-1),term))
    return out

def k_polynomial(n,edges):
    m=len(edges); out={}
    for mask in range(1<<n):
        S={v for v in range(n) if mask>>v&1}; N=set(S)
        for a,b in edges:
            if a in S: N.add(b)
            if b in S: N.add(a)
        d=m-len(N)+components(n,edges,S)
        assert d>=0
        out=add(out,shift(power({0:-1,1:1},len(S)),d))
    return out

def matching_three_polynomials(n,edges):
    nu=maximum_matching(n,edges); assert nu<=3
    P=p_polynomial(n,edges); out=[{0:1},P]
    T=add(add({len(edges):1},{0:-1}),scale(P,-1))
    if nu<=1:
        assert not T
        return out
    if nu==2:return out+[T]
    K=k_polynomial(n,edges)
    H=add(add(K,{n:-1}),scale(shift(P,n-2),-1))
    d=n-6; denominator={d+2:1,d:-1}
    N2=divide_monic(add(H,scale(shift(T,d),-1)),denominator)
    N3=divide_monic(add(shift(T,d+2),scale(H,-1)),denominator)
    return out+[N2,N3]

def rank_mod(A,p):
    A=[list(x) for x in A]; rows=len(A); cols=len(A[0]) if rows else 0; r=0
    for c in range(cols):
        pivot=next((k for k in range(r,rows) if A[k][c]%p),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]; inv=pow(A[r][c],-1,p)
        A[r]=[(x*inv)%p for x in A[r]]
        for k in range(r+1,rows):
            t=A[k][c]%p
            if t: A[k]=[(x-t*y)%p for x,y in zip(A[k],A[r])]
        r+=1
        if r==rows:break
    return r

def matrix(n,edges,weights,p):
    A=[[0]*n for _ in range(n)]
    for (a,b),v in zip(edges,weights):A[a][b]=v;A[b][a]=(-v)%p
    return A

def enumerate_counts(n,edges,p,receipt):
    counts=Counter(); nu=maximum_matching(n,edges)
    forest=len(edges)==n-components(n,edges)
    for values in product(range(p),repeat=len(edges)):
        r=rank_mod(matrix(n,edges,values,p),p)
        assert r%2==0 and r<=2*nu
        counts[r//2]+=1;receipt['matrices_enumerated']+=1
        if forest:
            H=[e for e,v in zip(edges,values) if v]
            assert r==2*maximum_matching(n,H)
            receipt['forest_weightings_checked']+=1
    assert counts[0]==1
    assert sum(counts.values())==p**len(edges)
    assert counts[1]==evaluate(p_polynomial(n,edges),p)
    assert sum(p**(n-2*i)*v for i,v in counts.items())==evaluate(k_polynomial(n,edges),p)
    assert sum((p**(n-2*i)*v)*p**(2*i) for i,v in counts.items())==p**(n+len(edges))
    if nu<=3:
        polys=matching_three_polynomials(n,edges)
        for i in range(n//2+1):assert counts[i]==(evaluate(polys[i],p) if i<len(polys) else 0)
        receipt['polynomial_recovery_checks']+=1
    receipt['graph_field_cases']+=1
    return dict(sorted(counts.items()))

def run():
    r={'status':'PASS','arithmetic':'exact finite-field and integer polynomial arithmetic',
       'matrices_enumerated':0,'forest_weightings_checked':0,'graph_field_cases':0,
       'polynomial_recovery_checks':0,'schrodinger_phase_checks':0,
       'bipartite_rank_checks':0,'schur_complement_checks':0}
    # Every labelled graph through four vertices, over F_3 and F_5.
    for n in range(1,5):
        all_edges=list(combinations(range(n),2))
        for bits in product((0,1),repeat=len(all_edges)):
            edges=[e for e,bit in zip(all_edges,bits) if bit]
            for p in (3,5):enumerate_counts(n,edges,p,r)
    cases={
      'C6':(6,[(i,i+1) for i in range(5)]+[(0,5)]),
      'C6_chord':(6,[(i,i+1) for i in range(5)]+[(0,5),(0,3)]),
      'two_triangles':(6,[(0,1),(1,2),(0,2),(3,4),(4,5),(3,5)]),
      'path7_two_chords':(7,[(i,i+1) for i in range(6)]+[(0,3),(2,6)]),
      'star8':(8,[(0,i) for i in range(1,8)]),
      'cover_three_8':(8,[(0,3),(0,4),(0,5),(1,4),(1,6),(1,7),(2,3),(2,6),(2,7)]),
      'matching4':(8,[(0,1),(2,3),(4,5),(6,7)]),
    }
    r['selected_distributions']={}
    for name,(n,edges) in cases.items():
        r['selected_distributions'][name]=enumerate_counts(n,edges,3,r)
    # Explicit same-support C4 obstruction, independently by row rank.
    edges=[(0,1),(0,3),(1,2),(2,3)]
    ranks=[rank_mod(matrix(4,edges,v,3),3) for v in [(1,1,1,1),(1,2,1,1)]]
    assert ranks==[4,2];r['C4_same_support_ranks']=ranks
    # Verify the representation multiplication phase, not floating-point roots of unity.
    for p in (3,5):
        half=pow(2,-1,p)
        for x,y,z,u,v,w,t in product(range(p),repeat=7):
            left=z+y*t+half*x*y+w+v*(t+x)+half*u*v
            right=z+w+half*(x*v-y*u)+(y+v)*t+half*(x+u)*(y+v)
            assert (left-right)%p==0;r['schrodinger_phase_checks']+=1
    # Every 2 by 3 matrix, block alternating embedding, p=3,5.
    for p in (3,5):
        for vals in product(range(p),repeat=6):
            M=[vals[:3],vals[3:]];B=[[0]*5 for _ in range(5)]
            for a in range(2):
                for b in range(3):B[a][2+b]=M[a][b];B[2+b][a]=-M[a][b]%p
            assert rank_mod(B,p)==2*rank_mod(M,p);r['bipartite_rank_checks']+=1
    # All 4 by 4 alternating matrices with a nonzero first pivot over F_3.
    for a in (1,2):
        for r0,r1,s0,s1,c in product(range(3),repeat=5):
            B=[[0,a,r0,r1],[-a,0,s0,s1],[-r0,-s0,0,c],[-r1,-s1,-c,0]]
            residual=(c+(s0*r1-r0*s1)*pow(a,-1,3))%3
            assert rank_mod(B,3)==2+(2 if residual else 0)
            r['schur_complement_checks']+=1
    # Moment-null direction for matching number four.
    for q in (3,5,7,11):
        delta=(1,-(q*q+1),q*q)
        assert sum(delta)==0
        assert sum(q**(8-2*i)*t for i,t in zip((2,3,4),delta))==0
    r['scope']='Finite controls only; no full-source resolution and no novelty claim.'
    return r

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    data=run();text=json.dumps(data,indent=2,sort_keys=True)+'\n'
    path=Path(__file__).with_name('VERIFICATION.json')
    if args.check:
        assert json.loads(path.read_text())==json.loads(text),'receipt mismatch'
        print('PASS: reproduced VERIFICATION.json exactly')
    else:path.write_text(text);print(text,end='')
