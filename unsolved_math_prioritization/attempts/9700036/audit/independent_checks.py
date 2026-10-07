#!/usr/bin/env python3
"""Independent exact finite checks, not a continuum proof or proof assistant."""
from fractions import Fraction as Q
from itertools import combinations, permutations
import json,heapq

def need(x,msg):
    if not x: raise ValueError(msg)

def components(n,edges,cut=None):
    adj=[set() for _ in range(n)]
    for a,b in edges: adj[a].add(b);adj[b].add(a)
    unseen=set(range(n))-{cut};out=[]
    while unseen:
        stack=[next(iter(unseen))];part=set()
        while stack:
            v=stack.pop()
            if v in unseen:
                unseen.remove(v);part.add(v);stack.extend(adj[v]-{cut})
        out.append(part)
    return out

def main():
    moments=0
    for r in map(Q,['1/7','1','7/3','19']):
        for j in range(13):
            numerator=r**(j+2)/Q(j+2);denominator=r*r/2
            need(numerator/denominator==2*r**j/(j+2),'radial density');moments+=1
        need((r**3/Q(3))/(r*r/2)==2*r/3,'mean separation')
    need(Q(1,2)!=Q(2,3),'uniform radius must not substitute for uniform disk')
    need((Q(24,100)-Q(8,10)*Q(5,1000)-Q(1,1000))/Q(93,100)>Q(21,100),'blue lower bound')
    need((Q(20,100)-Q(8,10)*Q(5,1000)-Q(1,1000))/Q(89,100)>Q(21,100),'red lower bound')
    need(Q(21,100)-Q(1,640000)>Q(20,100),'recoloring slack')
    need(Q(1,200)-4*Q(1,1000)>Q(1,2000),'excluded square boundary slack')
    need(Q(20,100)-Q(1,100)>Q(18,100),'short contour area slack')
    trees=centroids=0
    for n in range(2,7):
        pairs=list(combinations(range(n),2))
        for edges in combinations(pairs,n-1):
            if len(components(n,edges))!=1: continue
            trees+=1
            cuts=[components(n,edges,v) for v in range(n)]
            for mask in range(1,1<<n):
                marked={i for i in range(n) if mask>>i&1}
                need(any(all(2*len(c&marked)<=len(marked) for c in cc) for cc in cuts),'weighted centroid')
                centroids+=1
    graphs=triple_tree=triple_cycle=0
    for n in range(2,6):
        pairs=list(combinations(range(n),2));B=1<<(len(pairs)+1)
        for mask in range(1,1<<len(pairs)):
            edges=[p for j,p in enumerate(pairs) if mask>>j&1]
            if len(components(n,edges))!=1:continue
            graphs+=1;adj=[[] for _ in range(n)]
            for j,(a,b) in enumerate(pairs):
                if mask>>j&1:adj[a].append((b,B+(1<<j),j));adj[b].append((a,B+(1<<j),j))
            routes={}
            for a in range(n):
                todo=[(0,a,frozenset())];seen=set()
                while todo:
                    d,v,path=heapq.heappop(todo)
                    if v in seen:continue
                    seen.add(v);routes[a,v]=path
                    for w,c,e in adj[v]:
                        if w not in seen:heapq.heappush(todo,(d+c,w,path|{e}))
            compatible=all(routes[a,b]<=routes[a,c]|routes[c,b] for a,b,c in permutations(range(n),3))
            is_tree=len(edges)==n-1
            need(compatible==is_tree,'triple condition versus finite used-edge union')
            if is_tree:triple_tree+=1
            else:triple_cycle+=1
    need(trees==1441,'tree enumeration count')
    need(graphs==771 and triple_tree==145 and triple_cycle==626,'connected graph coverage')
    out={'status':'PASS','radial_moments':moments,'enumerated_labeled_trees':trees,'terminal_weighted_centroid_cases':centroids,'connected_unique_route_graphs':graphs,'tree_triple_controls':triple_tree,'cyclic_triple_negative_controls':triple_cycle,'source_constant_checks':5,'scope':'Exact finite diagnostics only; analytic proof in audit and accepted note.'}
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
