#!/usr/bin/env python3
"""Exact, finite checks for the authored three-terminal BSP reduction.
Only Python's standard library is required. This is not a proof of NP-hardness.
"""
from collections import deque
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib, json, platform, time

PAIRS = ((0,1),(0,2),(1,2))

def adjacency(n, edges, deleted=0):
    a = [[] for _ in range(n)]
    for i,(u,v) in enumerate(edges):
        if not (deleted>>i)&1:
            a[u].append((v,i)); a[v].append((u,i))
    return a

def distances(a,s):
    d=[None]*len(a); d[s]=0; q=deque([s])
    while q:
        u=q.popleft()
        for v,_ in a[u]:
            if d[v] is None: d[v]=d[u]+1; q.append(v)
    return d

def actual_shortest_path_masks(n, edges):
    a=adjacency(n,edges); masks=[]
    ds=[]
    for s,t in PAIRS:
        d=distances(a,s); ds.append(d[t]); assert d[t] is not None
        def walk(u,mask):
            if u==t: masks.append(mask); return
            if d[u]>=d[t]: return
            for v,e in a[u]:
                if d[v]==d[u]+1: walk(v,mask|(1<<e))
        walk(s,0)
    return tuple(sorted(masks)),ds

@lru_cache(None)
def hit_number(constraints):
    if not constraints:return 0
    p=min(constraints,key=int.bit_count)
    return 1+min(hit_number(tuple(c for c in constraints if not c&bit))
        for bit in bits(p))

def bits(mask):
    while mask:
        b=mask&-mask; yield b; mask^=b

def vertex_cover(n,edges):
    constraints=tuple(sorted((1<<u)|(1<<v) for u,v in edges))
    return hit_number(constraints)

def brute_vertex_cover(n,edges):
    return min(x.bit_count() for x in range(1<<n)
        if all((x>>u)&1 or (x>>v)&1 for u,v in edges))

def terminal_graph(parts,edges):
    # Terminals 0,1,2; H vertices shifted by 3. Spokes are listed first.
    n=len(parts)
    g=[(parts[v],v+3) for v in range(n)]
    g += [(u+3,v+3) for u,v in edges]
    return n+3,g

def all_tripartite(sizes):
    parts=tuple(i for i,size in enumerate(sizes) for _ in range(size))
    poss=[(u,v) for u,v in combinations(range(len(parts)),2) if parts[u]!=parts[v]]
    for mask in range(1<<len(poss)):
        es=[e for i,e in enumerate(poss) if (mask>>i)&1]
        types={tuple(sorted((parts[u],parts[v]))) for u,v in es}
        if types==set(PAIRS):yield parts,es

def classify_all_deletions(parts,hes,counters):
    hn=len(parts); n,ges=terminal_graph(parts,hes)
    paths,d=actual_shortest_path_masks(n,ges)
    assert d==[3,3,3]
    expected=tuple(sorted((1<<u)|(1<<v)|(1<<(hn+i)) for i,(u,v) in enumerate(hes)))
    assert paths==expected
    optimum=len(ges)
    for mask in range(1<<len(ges)):
        hit=all(mask&p for p in paths)
        a=adjacency(n,ges,mask)
        # Two BFS searches suffice to independently test all three distances.
        dr,ds=distances(a,0),distances(a,1)
        now=(dr[1],dr[2],ds[2])
        bfs=all(x is None or x>=4 for x in now)
        assert hit==bfs,(parts,hes,mask,now)
        if bfs:
            optimum=min(optimum,mask.bit_count())
            cover=mask&((1<<hn)-1)
            for i,(u,v) in enumerate(hes):
                if (mask>>(hn+i))&1: cover|=1<<u
            assert cover.bit_count()<=mask.bit_count()
            assert all((cover>>u)&1 or (cover>>v)&1 for u,v in hes)
            counters['feasible_deletion_sets_mapped_to_covers']+=1
        counters['deletion_sets_directly_checked_by_BFS']+=1
    assert optimum==brute_vertex_cover(hn,hes)
    counters['tripartite_graphs_with_all_deletions_checked']+=1

def subdivide(n,edges):
    parts=[0]*n; h=[]
    for u,v in edges:
        b=len(parts);c=b+1;parts.extend([1,2]);h.extend([(u,b),(b,c),(c,v)])
    return tuple(parts),h

def main():
    started=time.monotonic()
    c={k:0 for k in ['tripartite_graphs_with_all_deletions_checked',
        'deletion_sets_directly_checked_by_BFS',
        'feasible_deletion_sets_mapped_to_covers',
        'tripartite_222_graphs_exact_optimum_checks',
        'nonempty_base_graphs_through_5_vertices',
        'base_graph_budget_equivalences',
        'finite_distance_cover_checks']}
    for sizes in [(1,1,1),(2,1,1),(2,2,1)]:
        for parts,hes in all_tripartite(sizes): classify_all_deletions(parts,hes,c)
    for parts,hes in all_tripartite((2,2,2)):
        n,ges=terminal_graph(parts,hes)
        paths,d=actual_shortest_path_masks(n,ges)
        assert d==[3,3,3]
        assert len(paths)==len(hes)
        assert hit_number(paths)==brute_vertex_cover(len(parts),hes)
        c['tripartite_222_graphs_exact_optimum_checks']+=1
    for n in range(2,6):
        poss=list(combinations(range(n),2))
        for mask in range(1,1<<len(poss)):
            es=[e for i,e in enumerate(poss) if (mask>>i)&1]
            tau=brute_vertex_cover(n,es)
            parts,hes=subdivide(n,es)
            h_tau=vertex_cover(len(parts),hes)
            assert h_tau==len(es)+tau
            gn,ges=terminal_graph(parts,hes)
            paths,d=actual_shortest_path_masks(gn,ges)
            assert d==[3,3,3]
            bsp=hit_number(paths)
            assert bsp==h_tau
            assert gn==n+2*len(es)+3 and len(ges)==n+5*len(es)
            for k in range(n+1):
                assert (tau<=k)==(bsp<=len(es)+k)
                c['base_graph_budget_equivalences']+=1
            c['nonempty_base_graphs_through_5_vertices']+=1
    # Optional robust variant: add internally disjoint terminal paths of length 4.
    for parts,hes in all_tripartite((2,1,1)):
        n,ges=terminal_graph(parts,hes)
        for s,t in PAIRS:
            new=(n,n+1,n+2);n+=3
            ges.extend(zip((s,)+new,new+(t,)))
        paths,d=actual_shortest_path_masks(n,ges); assert d==[3,3,3]
        for cover in range(1<<len(parts)):
            if all((cover>>u)&1 or (cover>>v)&1 for u,v in hes):
                a=adjacency(n,ges,cover)
                dr,ds=distances(a,0),distances(a,1)
                assert (dr[1],dr[2],ds[2])==(4,4,4)
                c['finite_distance_cover_checks']+=1
    out={"result":"PASS","checks":c,
         "method":"Integer bitmask enumeration, independently computed BFS distances, exact memoized hitting-set recurrence, and brute-force vertex cover",
         "python":platform.python_version(),"runtime_seconds":round(time.monotonic()-started,3),
         "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         "limitations":"Finite checks support the construction but do not substitute for the written reduction proof. No random tests or floating-point optimizers were used."}
    p=Path(__file__).with_name('check_results.json');p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
