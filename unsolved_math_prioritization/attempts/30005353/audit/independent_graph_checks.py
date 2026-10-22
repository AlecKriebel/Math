#!/usr/bin/env python3
"""Exact independent degree-reduction samples, sharing only auditor primitives."""
from collections import defaultdict,deque
from itertools import combinations
from pathlib import Path
import json
from independent_checks import all_short_cycles,append_basis,cycle_vector,spanning_chords,group_certificate

def connected(n,edges):
    adj=defaultdict(set)
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    seen={0};todo=[0]
    for a in todo:
        for b in adj[a]:
            if b not in seen:seen.add(b);todo.append(b)
    return len(seen)==n

def shortest_path(edges,s,t):
    adj=defaultdict(set)
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    parent={s:None};todo=[s]
    for a in todo:
        if a==t:break
        for b in sorted(adj[a]):
            if b not in parent:parent[b]=a;todo.append(b)
    path=[t]
    while path[-1]!=s:path.append(parent[path[-1]])
    return path[::-1]

def basis(n,edges):
    chords=spanning_chords(list(range(n)),edges);piv={};selected=[]
    cycles=all_short_cycles(list(range(n)),edges,n)
    for c in cycles:
        if append_basis(piv,cycle_vector(c,chords,2),2):selected.append(c)
    assert len(selected)==len(chords)
    return sum(map(len,selected)),selected,cycles,chords

def blowup(n,edges,L):
    incident={v:sorted([b if a==v else a for a,b in edges if v in (a,b)]) for v in range(n)}
    count=0;out=set();ports={};tree_edges={};vertex_tree={};D=0;external={}
    def vertex(v=None):
        nonlocal count
        x=count;count+=1
        if v is not None:vertex_tree[x]=v
        return x
    for v,nbrs in incident.items():
        if len(nbrs)>=4:nbrs=nbrs[::2]+nbrs[1::2]
        d=len(nbrs)
        if d==1:
            pp=[vertex(v)];te=set()
        elif d==2:
            pp=[vertex(v),vertex(v)];te={tuple(pp)}
        else:
            spine=[vertex(v) for _ in nbrs];pp=[vertex(v) for _ in nbrs]
            te={tuple(sorted(e)) for e in zip(spine,spine[1:])}|{tuple(sorted(e)) for e in zip(spine,pp)}
        for w,port in zip(nbrs,pp):ports[v,w]=port
        out|=te;tree_edges[v]=te
        D=max(D,max(len(shortest_path(te,a,b))-1 for a in pp for b in pp))
    for a,b in sorted(edges):
        path=[ports[a,b]]+[vertex() for _ in range(L-1)]+[ports[b,a]]
        es={tuple(sorted(e)) for e in zip(path,path[1:])};external[a,b]=es;out|=es
    return count,out,D,external,ports,tree_edges

def check_case(n,edges,index):
    cost,base,cycles,chords=basis(n,edges);r=len(chords);records=[]
    # A fundamental family is certified directly from its unique chord relations.
    tree=edges-set(chords)
    fundamental=[tuple(shortest_path(tree,a,b)) for a,b in chords]
    for L in (1,3):
        N,E,D,external,ports,trees=blowup(n,edges,L)
        new_cost,new_basis,new_cycles,new_chords=basis(N,E)
        assert len(new_chords)==r and L*cost<=new_cost<=(L+D)*cost
        deg=defaultdict(int)
        for a,b in E:deg[a]+=1;deg[b]+=1
        assert max(deg.values())<=3
        nonsimple=0
        for c in new_cycles:
            used={tuple(sorted(e)) for e in zip(c,c[1:]+c[:1])};original=[]
            for e,path in external.items():
                assert not(used&path) or path<=used
                if path<=used:original.append(e)
            assert original and L*len(original)<=len(c)
            dd=defaultdict(int)
            for a,b in original:dd[a]+=1;dd[b]+=1
            assert all(d%2==0 for d in dd.values())
            nonsimple+=any(d>2 for d in dd.values())
        lifted=[]
        for c in fundamental:
            walk=[]
            for i,v in enumerate(c):
                prev=c[i-1];nxt=c[(i+1)%len(c)]
                walk+=shortest_path(trees[v],ports[v,prev],ports[v,nxt])[:-1]
                walk+=shortest_path(external[tuple(sorted((v,nxt)))],ports[v,nxt],ports[nxt,v])[:-1]
            assert len(walk)==len(set(walk)) and L*len(c)<=len(walk)<=(L+D)*len(c)
            lifted.append(tuple(walk))
        gg,rr,_=group_certificate(lifted,new_chords);assert not gg and not rr
        records.append(dict(case=index,L=L,rank=r,D=D,original_cost=cost,expanded_cost=new_cost,expanded_cycles=len(new_cycles),nonsimple_projections=nonsimple))
    return records

if __name__=='__main__':
    cases=[]
    for n in (3,4):
        possible=list(combinations(range(n),2))
        for bits in range(1<<len(possible)):
            edges={e for i,e in enumerate(possible) if bits>>i&1}
            if len(edges)>=n and connected(n,edges):cases.append((n,edges))
    cases.append((5,{(0,1),(1,2),(0,2),(0,3),(3,4),(0,4)}))
    records=[row for i,(n,e) in enumerate(cases) for row in check_case(n,e,i)]
    out=dict(status='pass',cases=len(cases),expansions=len(records),total_expanded_cycles=sum(row['expanded_cycles'] for row in records),nonsimple_projections=sum(row['nonsimple_projections'] for row in records),records=records)
    Path(__file__).with_name('INDEPENDENT_GRAPH_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
