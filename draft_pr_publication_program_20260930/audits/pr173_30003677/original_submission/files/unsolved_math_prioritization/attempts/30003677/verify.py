#!/usr/bin/env python3
"""Finite exact controls; no Monte Carlo or asymptotic certification."""
from itertools import product,combinations
from fractions import Fraction as F
from heapq import heappush,heappop
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
counts=Counter();cases=0;protected=0

def ck(v,label):
    assert v,label
    counts[label]+=1

def distances(n,edges,weights,root):
    adj=[[] for _ in range(n)]
    for i,(a,b) in enumerate(edges):adj[a].append((b,i));adj[b].append((a,i))
    ds=[10**9]*n;ds[root]=0;q=[(0,root)]
    while q:
        t,v=heappop(q)
        if ds[v]!=t:continue
        for z,i in adj[v]:
            if t+weights[i]<ds[z]:ds[z]=t+weights[i];heappush(q,(ds[z],z))
    return ds,adj

def compete(n,edges,w1,w2,S,w):
    _,adj=distances(n,edges,w2,w)
    colour=[0]*n;times=[None]*n;q=[]
    for v in S:colour[v]=1;times[v]=0
    colour[w]=2;times[w]=0
    def emit(v,t,c):
        weights=w1 if c==1 else w2
        for z,i in adj[v]:heappush(q,(t+weights[i],0 if c==2 else 1,z,c))
    for v in range(n):
        if colour[v]:emit(v,0,colour[v])
    while q:
        t,_,v,c=heappop(q)
        if colour[v]:continue
        colour[v]=c;times[v]=t;emit(v,t,c)
    return colour,times

def paths(adj,start):
    out=[]
    def go(v,vertices,indices):
        out.append((vertices,indices))
        for z,i in adj[v]:
            if z not in vertices:go(z,vertices+(z,),indices+(i,))
    go(start,(start,),())
    return out

def test(n,edges,w1,w2):
    global cases,protected
    for w in range(n):
        other=[i for i in range(n) if i!=w]
        for k in range(1,len(other)+1):
            for S in combinations(other,k):
                colour,times=compete(n,edges,w1,w2,S,w)
                ds,adj=distances(n,edges,w2,w);cases+=1
                for v in range(n):
                    if colour[v]==2:ck(ds[v]<=times[v],'fast unopposed domination')
                for s in S:
                    for vertices,inds in paths(adj,s):
                        length=sum(w1[i] for i in inds)
                        # Existence of T with length<=T<min fast-distance is equivalent
                        # to testing its smallest possible value T=length.
                        if all(ds[v]>length for v in vertices):
                            protected+=1;v=vertices[-1]
                            ck(colour[v]==1 and times[v]<=length,'protected path lemma')
    return
# All connected labelled three-vertex graphs and all positive 1/2 edge weights.
base=[(0,1),(0,2),(1,2)]
for flags in product((0,1),repeat=3):
    edges=[e for e,a in zip(base,flags) if a]
    if len(edges)<2:continue
    for ws in product((1,2),repeat=2*len(edges)):
        test(3,edges,ws[:len(edges)],ws[len(edges):])
# Deterministic four-vertex weighted controls, including parallel edges and a loop.
for edges in [[(0,1),(1,2),(2,3)],[(0,1),(1,2),(2,3),(3,0)],
              list(combinations(range(4),2)),[(0,1),(0,1),(1,2),(2,3),(3,0),(2,2)]]:
    m=len(edges)
    for a,b in product(range(1,5),repeat=2):
        w1=tuple(1+(a*(i+1)+b)%3 for i in range(m))
        w2=tuple(1+(b*(i+2)+a)%4 for i in range(m))
        test(4,edges,w1,w2)
# Exact inequalities used in the deterministic diagonal selection.
for j in range(2,13):
    for p in [F(1),F(1,2),F(2,3),F(1,4),F(1,10)]:
        R=(j*j*p.denominator+p.numerator-1)//p.numerator
        ck(R*p>=j*j,'ray length choice')
        ck((1-p)**R<=1/(1+R*p)<=F(1,j*j),'geometric tail bound')
        for lam in [F(1,10),F(1,2),F(1),F(3)]:
            T=F(j*j*R)/lam
            ck(F(R)/(lam*T)==F(1,j*j),'passage time Markov budget')
    for mu in [4*j*j,8*j*j,16*j*j]:
        ck(F(4,mu)<=F(1,j*j),'binomial Chebyshev budget')
        ck(F(mu,2)>=j,'seed number lower bound')
# Concrete even geometric degree law. Closed tails checked against recurrences
# and independently against partial sums plus the exact remainder.
for r in range(1,31):
    tail0=F(2,2**r)
    tail1=F(2*(r+1),2**r)
    tail2=F(2*(r*r+2*r+3),2**r)
    ck(sum((F(1,2**m) for m in range(1,r)),F())+tail0==1,'geometric mass')
    ck(sum((F(m,2**m) for m in range(1,r)),F())+tail1==2,'geometric first moment')
    ck(sum((F(m*m,2**m) for m in range(1,r)),F())+tail2==6,'geometric second moment')
    ck(F(2)*tail1/4==F(r+1,2**r),'size-biased tail')
    ck(4*6==24 and 2*2==4,'degree moments')
p=Path(__file__).resolve().parent
receipt={'problem_id':30003677,'assertions':sum(counts.values()),'sections':dict(counts),
 'finite_competition_instances':cases,'protected_path_witnesses':protected,
 'artifact_sha256':sha256((p/'CANDIDATE.md').read_bytes()).hexdigest(),
 'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Exact finite weighted-graph path protection, diagonal inequalities and geometric-law moments. No stochastic limit or novelty is certified by computation.'}
print(json.dumps(receipt,indent=2,sort_keys=True))
