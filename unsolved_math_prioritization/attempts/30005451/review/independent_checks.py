#!/usr/bin/env python3
"""Independent exact diagnostics for the affine comparison; not a limit proof."""
from fractions import Fraction as F
from itertools import product
from collections import Counter,defaultdict
from math import factorial,prod
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
counts=Counter()
def ck(kind,v):
    if not v:raise AssertionError(kind)
    counts[kind]+=1

def rising(x,n):return prod((x+j for j in range(n)),start=F(1))

# Independently compare two-time affine birth transitions with integrated Cox laws.
cox_cases=0
for nu,z1,k,j in product((F(1,3),F(1,2),F(1),F(3,2),F(2),F(5,2)),(F(3,2),F(2),F(3)),range(5),range(5)):
    for z2 in (z1+F(1,2),z1+1,2*z1):
        ratio=z2/z1
        # The common factor z2**(-nu) is canceled, so all remaining values are rational.
        markov=(rising(nu,k)/factorial(k)*(z1-1)**k/z1**k
                *rising(nu+k,j)/factorial(j)*(ratio-1)**j/ratio**(k+j))
        cox=rising(nu,k+j)/factorial(k)/factorial(j)*(z1-1)**k*(z2-z1)**j/z2**(k+j)
        ck('two_time_cox_identity',markov==cox)
        ck('palm_shape_shift',rising(nu,k+j+1)/nu==rising(nu+1,k+j))
        cox_cases+=1

# Exact sequence distributions: independent draws versus reinforced draws.
sequence_models=0
for ds,a,b,m in product(((0,0,0),(0,1,0),(1,0,2),(2,2,0),(3,1,2),(0,3,3),(1,2,3)),(F(0),F(1,4),F(3,4)),(F(1,3),F(1)),range(6)):
    w=tuple(a*d+b for d in ds);S=sum(w);seqdist=defaultdict(F);freezedist=defaultdict(F);path_tv=F(0)
    for choices in product(range(3),repeat=m):
        h=[0,0,0];q=p=F(1)
        for t,v in enumerate(choices):
            q*= (w[v]+a*h[v])/(S+a*t);p*=w[v]/S;h[v]+=1
        seqdist[tuple(h)]+=q;freezedist[tuple(h)]+=p;path_tv+=abs(q-p)/2
    ck('row_distribution_normalization',sum(seqdist.values())==sum(freezedist.values())==1)
    bound=sum((a*t/(S+a*t) for t in range(m)),F(0))
    ck('sequence_tv_bound',path_tv<=bound)
    ck('row_tv_contraction',sum(abs(seqdist[h]-freezedist[h]) for h in seqdist)/2<=path_tv)
    for h,prob in seqdist.items():
        multinomial=F(factorial(m),prod(factorial(x) for x in h))
        if a:
            formula=multinomial*prod(rising(wv/a,k) for wv,k in zip(w,h))/rising(S/a,m)
        else:
            formula=multinomial*prod((wv/S)**k for wv,k in zip(w,h))
        ck('dirichlet_multinomial_count_law',prob==formula)
    sequence_models+=1

# Graph operations with loop and parallel-edge seed controls.
def degree(n,G):
    out=[0]*n
    for (i,j),m in G.items():out[i]+=m;out[j]+=m
    return out

def dist(n,G,A):
    D={x:0 for x in A};front=set(A)
    for t in range(1,n+1):
        new={v for (x,y),m in G.items() if m for u,v in ((x,y),(y,x)) if u in front and v not in D}
        for v in new:D[v]=t
        front=new
        if not front:break
    return D

def ball(n,G,o,r):
    vertices=frozenset(v for v,d in dist(n,G,{o}).items() if d<=r)
    return vertices,tuple(sorted((e,m) for e,m in G.items() if m and e[0] in vertices and e[1] in vertices))

def edge_cost(A,B):return sum(abs(A.get(e,0)-B.get(e,0)) for e in A.keys()|B.keys())

multi_pairs=0
edges=tuple((i,j) for i in range(3) for j in range(i+1))
for vals in product(range(3),repeat=len(edges)):
    A={e:v for e,v in zip(edges,vals) if v}
    for changed in edges:
        B=dict(A);B[changed]=B.get(changed,0)+1
        H={e:max(A.get(e,0),B.get(e,0)) for e in A.keys()|B.keys()}
        da,db,dh=degree(3,A),degree(3,B),degree(3,H)
        ck('multigraph_degree_bound',all(z<=2*x+abs(y-x) for x,y,z in zip(da,db,dh)))
        ck('degree_discrepancy_bound',sum(abs(x-y) for x,y in zip(da,db))<=2*edge_cost(A,B))
        bad=set(changed);D=dist(3,H,bad)
        for r,o in product(range(3),range(3)):
            if D.get(o,4)>r:ck('induced_multigraph_ball',ball(3,A,o,r)==ball(3,B,o,r))
        multi_pairs+=1

# Independent five-vertex threshold/pruning tests, complementing whole columns.
def prune(n,G,K):
    incoming=[0]*n
    for (i,j),m in G.items():incoming[j]+=m
    H={e:m for e,m in G.items() if incoming[e[1]]<=K}
    deg=degree(n,H)
    return H,{e:m for e,m in H.items() if deg[e[0]]<=K and deg[e[1]]<=K}

prune_pairs=0
n=5;edges=tuple((i,j) for i in range(n) for j in range(i))
for bits in product((0,1),repeat=len(edges)):
    A={e:b for e,b in zip(edges,bits) if b}
    for col in range(n-1):
        B={e:(1-A.get(e,0) if e[1]==col else A.get(e,0)) for e in edges}
        B={e:m for e,m in B.items() if m};prune_pairs+=1
        for K in (1,2,3):
            H,J=prune(n,A,K);Hp,Jp=prune(n,B,K)
            ck('capped_column_edit',edge_cost(H,Hp)<=2*K)
            ck('explicit_pruning_edit_bound',edge_cost(J,Jp)<=2*K+12*K*K)
            ck('pruned_degree_bound',max(degree(n,J)+degree(n,Jp))<=K)
            olddeg=degree(n,A)
            ck('removed_edge_high_degree_incidence',edge_cost(A,J)<=sum(x for x in olddeg if x>K))
            # Every edge changed in second pruning has an endpoint with changed status,
            # apart from the initially changed intermediate edges.
            d,dp=degree(n,H),degree(n,Hp)
            crossing={v for v in range(n) if (d[v]>K)!=(dp[v]>K)}
            ck('threshold_crossing_degree',all(max(d[v],dp[v])<=3*K for v in crossing))
            ck('pruning_locality',all(H.get(e,0)!=Hp.get(e,0) or bool(set(e)&crossing)
                                     for e in J.keys()|Jp.keys() if J.get(e,0)!=Jp.get(e,0)))

# Scalar recursions and moment constants are checked independently in rational form.
for a,b,n,T in product((F(0),F(1,4),F(3,4),F(9,10)),(F(1,4),F(1)),range(1,8),range(8)):
    mean=a*T/n+b
    rhs=(1+a/n)**2*T*T+(2*b*(1+a/n)+a/n)*T+b*b+b
    ck('total_edge_second_moment_identity',(T+mean)**2+mean==rhs)
    lam=b/(1-a)
    ck('normalization_mean',a*lam+b==lam)
    ck('comparison_supersolution',(1+a/n)*F(n)/(1-a)+1==F(n+1)/(1-a))

proof=HERE/'author_replay'/'CANDIDATE.md'
print(json.dumps({
 'status':'PASS','assertions':sum(counts.values()),'families':dict(counts),
 'cox_two_time_cases':cox_cases,'sequence_models':sequence_models,
 'loop_parallel_edge_pairs':multi_pairs,'five_vertex_column_pairs':prune_pairs,
 'artifact_sha256':sha256(proof.read_bytes()).hexdigest(),
 'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'limitations':'Finite exact controls only; all-degree graph limits and source scope are justified in the written review, not by finite enumeration.'
},indent=2,sort_keys=True))
