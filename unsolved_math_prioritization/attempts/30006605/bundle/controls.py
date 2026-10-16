#!/usr/bin/env python3
"""Exact tests of a threshold reduction and implicit search, NOT the fast BDH oracle.

Standard library only. The default additive oracle is quadratic on an already
computed distance matrix. A separate rerooting oracle is linear on trees.
Nothing here empirically establishes the general median-graph runtime theorem.
"""
from collections import deque, Counter
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import random


def distances(adj):
    out=[]
    for s in range(len(adj)):
        row=[None]*len(adj); row[s]=0; q=deque([s])
        while q:
            v=q.popleft()
            for u in adj[v]:
                if row[u] is None:
                    row[u]=row[v]+1; q.append(u)
        if None in row:
            return None
        out.append(row)
    return out


def additive_reference(dist,a):
    return [max(du+au for du,au in zip(row,a)) for row in dist]


def additive_tree(adj,a):
    """Independent O(n) rerooting DP for the additive eccentricities of a tree."""
    n=len(adj); parent=[-1]*n; parent[0]=0; order=[0]
    for v in order:
        for u in adj[v]:
            if u!=parent[v]:
                assert parent[u]==-1, 'not a tree'
                parent[u]=v; order.append(u)
    assert len(order)==n
    down=a.copy(); up=[-1]*n
    for v in reversed(order[1:]):
        down[parent[v]]=max(down[parent[v]],down[v]+1)
    for v in order:
        # Candidate contribution of each child measured at v; top two suffice.
        first=(-1,-1); second=(-1,-1)
        for u in adj[v]:
            if parent[u]==v and u!=v:
                item=(down[u]+1,u)
                if item[0]>first[0]: second=first; first=item
                elif item[0]>second[0]: second=item
        for u in adj[v]:
            if parent[u]==v and u!=v:
                other=second[0] if first[1]==u else first[0]
                up[u]=1+max(a[v],up[v],other)
    return [max(down[v],up[v]) for v in range(n)]


def first_index(w,value,lo,stop,strict):
    """First k in [lo,stop) with k*w > value (strict) or >= value."""
    while lo<stop:
        m=(lo+stop)//2
        if (m*w>value if strict else m*w>=value): stop=m
        else: lo=m+1
    return lo


def threshold(weights,R,oracle):
    n=len(weights); D=n-1
    if R<0: return []
    a=[]
    for w in weights:
        # Last k with k*w<=R, capped by D, also correct for w=0.
        b=first_index(w,R,0,n,True)-1
        assert 0<=b<=D
        a.append(D-b)
    assert all(isinstance(t,int) and 0<=t<=D for t in a)
    labels=oracle(a)
    return [v for v in range(n) if labels[v]<=D]


def optimize(weights,oracle):
    n=len(weights); assert n and all(w>=0 for w in weights)
    D=n-1; B=D*max(weights); witness=0
    if B==0:
        return B,list(range(n)),[]
    low=[0]*n; high=[D]*n; trace=[]
    while True:
        entries=[]; M=0
        for u in range(n):
            if low[u]<=high[u]:
                L=high[u]-low[u]+1; M+=L
                entries.append((weights[u]*((low[u]+high[u])//2),L))
        if not M: break
        entries.sort(); cum=0
        for q,L in entries:
            cum+=L
            if 2*cum>=M: break
        assert 2*sum(L for x,L in entries if x<=q)>=M
        assert 2*sum(L for x,L in entries if x>=q)>=M
        feasible=threshold(weights,q,oracle)
        if feasible:
            if q<B: B=q; witness=feasible[0]
            for u in range(n):
                if low[u]<=high[u]:
                    high[u]=first_index(weights[u],q,low[u],high[u]+1,False)-1
        else:
            for u in range(n):
                if low[u]<=high[u]:
                    low[u]=first_index(weights[u],q,low[u],high[u]+1,True)
        Mnext=sum(max(0,h-l+1) for l,h in zip(low,high))
        assert 4*Mnext<=3*M, (M,Mnext)
        trace.append((M,Mnext))
    centers=threshold(weights,B,oracle)
    assert witness in centers
    return B,centers,trace


def median_graph(dist):
    n=len(dist)
    return all(sum(dist[x][m]+dist[m][y]==dist[x][y]
                   and dist[x][m]+dist[m][z]==dist[x][z]
                   and dist[y][m]+dist[m][z]==dist[y][z]
                   for m in range(n))==1
               for x,y,z in combinations(range(n),3))


def cube(d):
    return [[v^(1<<j) for j in range(d)] for v in range(1<<d)]


def grid(dims):
    verts=list(product(*(range(k) for k in dims))); ix={v:i for i,v in enumerate(verts)}
    adj=[[] for _ in verts]
    for i,v in enumerate(verts):
        for j in range(len(dims)):
            for s in (-1,1):
                u=list(v); u[j]+=s; u=tuple(u)
                if u in ix: adj[i].append(ix[u])
    return adj


def run():
    stats=Counter(); digest=hashlib.sha256(); rng=random.Random(59830006605)
    alphabet=[F(0),F(1,3),F(1),F(7,2)]
    def check(adj,weights,all_thresholds=False,is_median=None):
        dist=distances(adj); assert dist is not None
        actual=[max(w*d for w,d in zip(weights,row)) for row in dist]
        best=min(actual); centers=[v for v,r in enumerate(actual) if r==best]
        def oracle(a):
            stats['reference_oracle_calls']+=1
            return additive_reference(dist,a)
        got,cs,trace=optimize(weights,oracle)
        assert got==best and cs==centers
        stats['optimization_cases']+=1; stats['pruning_steps']+=len(trace)
        stats['max_pruning_steps']=max(stats['max_pruning_steps'],len(trace))
        if is_median: stats['median_graph_optimization_cases']+=1
        vals=sorted(set(k*w for w in weights for k in range(len(adj))))
        tests=[F(-1),F(0),best,best+F(1,1000003)]
        if all_thresholds:
            tests+=vals+[ (a+b)/2 for a,b in zip(vals,vals[1:]) ]
        for R in set(tests):
            want=[v for v,r in enumerate(actual) if r<=R]
            assert threshold(weights,R,oracle)==want
            stats['full_feasible_set_checks']+=1
        if sum(map(len,adj))==2*(len(adj)-1):
            for a in ([0]*len(adj),list(range(len(adj))),[rng.randrange(len(adj)) for _ in adj]):
                assert additive_tree(adj,a)==additive_reference(dist,a)
                stats['tree_oracle_vector_checks']+=1
            alt,ac,at=optimize(weights,lambda a:additive_tree(adj,a))
            assert (alt,ac)==(best,centers)
            stats['tree_fast_oracle_optimization_checks']+=1
        digest.update(json.dumps([len(adj),[str(w) for w in weights],str(got),cs,trace],sort_keys=True).encode())
    # Exhaustive all connected labelled simple graphs up to order four and every
    # profile over the four-element rational alphabet (including zero weights).
    for n in range(1,5):
        pairs=list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            adj=[[] for _ in range(n)]
            for j,(u,v) in enumerate(pairs):
                if mask>>j&1: adj[u].append(v); adj[v].append(u)
            dist=distances(adj)
            if dist is None: continue
            med=median_graph(dist); stats['exhaustive_graphs']+=1
            if med: stats['exhaustive_median_graphs']+=1
            for w in product(alphabet,repeat=n): check(adj,list(w),True,med)
    # Higher-dimensional median families. Medianity independently checked via
    # triples, not assumed merely from their names.
    families=[cube(d) for d in range(1,5)]+[grid(ds) for ds in [(3,3),(4,5),(3,3,3),(2,2,2,2)]]
    for adj in families:
        assert median_graph(distances(adj)); stats['higher_median_families']+=1
        n=len(adj)
        profiles=[[F(0)]*n,[F(1)]*n,[F(i%3,7) for i in range(n)]]
        profiles+=[[F(rng.randrange(20),rng.randrange(1,20)) for _ in adj] for _ in range(40)]
        profiles+=[[F(2**(i*8),2**257+93) for i in range(n)],
                   [F(2**257+93,2**(i*8)) for i in range(n)]]
        for w in profiles: check(adj,w,False,True)
    # More generic graphs test the graph-independent nature of both reductions.
    for t in range(250):
        n=rng.randrange(5,21); adj=[[] for _ in range(n)]
        for v in range(1,n):
            u=rng.randrange(v); adj[u].append(v); adj[v].append(u)
        if t%2:
            for u,v in combinations(range(n),2):
                if v not in adj[u] and rng.random()<0.13: adj[u].append(v); adj[v].append(u)
        weights=[F(rng.randrange(51),rng.randrange(1,101)) for _ in adj]
        check(adj,weights,False)
    # Many tied candidates and extreme weight scales on longer paths and stars.
    for n in (31,100):
        path=[[] for _ in range(n)]; star=[[] for _ in range(n)]
        for i in range(1,n):
            path[i].append(i-1); path[i-1].append(i)
            star[0].append(i); star[i].append(0)
        for adj in (path,star):
            for w in ([F(1)]*n,[F(0)]*(n-1)+[F(2**512+1,2**521-1)],
                      [F(2**256 if i%2 else 1,2**256+1) for i in range(n)]):
                check(adj,w,False,True)
    return {
        'status':'PASS', 'seed':59830006605, 'statistics':dict(sorted(stats.items())),
        'case_digest_sha256':digest.hexdigest(),
        'limits':[
            'Finite exact tests support but do not prove the universal reduction.',
            'The general additive oracle is quadratic reference code, not BDH.',
            'The independent linear additive oracle is restricted to trees.',
            'No benchmark or implementation of the general O(n log^4 n) oracle is claimed.',
            'No formal proof assistant or human peer review was used.'
        ]
    }

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
