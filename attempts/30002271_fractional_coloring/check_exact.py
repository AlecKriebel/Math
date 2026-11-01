#!/usr/bin/env python3
"""Exact, standard-library graph and fractional-coloring certificate checks."""
import json
from fractions import Fraction as F
from pathlib import Path

def require(ok, message):
    if not ok:
        raise ValueError(message)

def maximal_cliques(adj):
    # Generic pivoted Bron–Kerbosch, used also on the complement graph.
    def visit(r, p, x):
        if not p and not x:
            yield r
            return
        pivot = max(p | x, key=lambda v: len(p & adj[v]))
        for v in sorted(p - adj[pivot]):
            yield from visit(r | {v}, p & adj[v], x & adj[v])
            p.remove(v)
            x.add(v)
    return list(visit(set(), set(adj), set()))

def check(k):
    n = k * (k + 1)
    adj = {v: set() for v in range(n)}
    def edge(a,b):
        adj[a].add(b); adj[b].add(a)
    for i in range(k):
        for j in range(i): edge(i,j)
        for j in range(k): edge(i,k+i*k+j)
    vertices=set(adj)
    require(all(v not in adj[v] and all(v in adj[w] for w in adj[v]) for v in adj), 'simple undirected graph')
    cliques=maximal_cliques(adj)
    gamma={}
    for v in adj:
        closed=adj[v]|{v}
        # Any clique in the neighborhood extends to a global maximal clique;
        # intersection with closed is still a clique, so this computes exact omega.
        omega=max(len(c & closed) for c in cliques)
        gamma[v]=F(len(adj[v])+1+omega,2)
        require(omega==(max(k,2) if v<k else 2), 'local clique number')
        require(gamma[v]==(F(3*k,2) if v<k and k>=2 else F(2)), 'gamma')
    averages={v:sum((gamma[w] for w in adj[v]|{v}),F(0))/(len(adj[v])+1) for v in adj}
    expected=F(3*k,4)+1 if k>=2 else F(2)
    require(set(averages.values())=={expected},'closed-neighborhood average')
    colors={v:v for v in range(k)} if k>=2 else {0:0}
    for i in range(k):
        for j in range(k): colors[k+i*k+j]=(i+1)%k if k>=2 else 1
    require(all(colors[v]!=colors[w] for v in adj for w in adj[v]),'proper coloring primal certificate')
    chi=max(k,2)
    require(len(set(colors.values()))==chi,'primal weight')
    dual={v:int(v<k) for v in adj} if k>=2 else {0:1,1:1}
    comp={v:vertices-adj[v]-{v} for v in adj}
    independent=maximal_cliques(comp)
    require(all(sum(dual[v] for v in s)<=1 for s in independent),'fractional dual feasibility')
    require(sum(dual.values())==chi,'dual weight equals primal weight')
    require((F(chi)>expected)==(k>=5),'strict threshold')
    clique_average=max(sum((gamma[v] for v in c),F(0))/len(c) for c in cliques)
    require(clique_average==(F(3*k,2) if k>=2 else F(2)), 'maximal-clique variant')
    return {'k':k,'vertices':n,'edges':sum(map(len,adj.values()))//2,'maximal_cliques':len(cliques),'maximal_independent_sets':len(independent),'chi_f':chi,'closed_neighborhood_average':str(expected),'gap':str(F(chi)-expected),'strict_counterexample':k>=5,'maximal_clique_average':str(clique_average),'exact_primal_dual_certificates':True}

if __name__=='__main__':
    results=[check(k) for k in range(1,13)]
    print(json.dumps({'problem_id':30002271,'arithmetic':'fractions.Fraction; no floating-point LP','cases':results,'passed':True},indent=2))
