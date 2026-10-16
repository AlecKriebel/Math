#!/usr/bin/env python3
"""Fresh checks designed from PROOF.md, without importing submission code."""
from collections import deque
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json, platform, time

COUNTS = {}

def count(name, n=1): COUNTS[name] = COUNTS.get(name, 0) + n

def require(condition, message):
    if not condition: raise RuntimeError(message)

def adjacency(n, edges, removed=frozenset()):
    adj = [set() for _ in range(n)]
    for i, (a,b) in enumerate(edges):
        if i not in removed:
            adj[a].add(b); adj[b].add(a)
    return adj

def distance(adj, a, b):
    d = {a:0}; queue = deque([a])
    while queue:
        x = queue.popleft()
        if x == b: return d[x]
        for y in adj[x]:
            if y not in d: d[y]=d[x]+1; queue.append(y)
    return float('inf')

def distances(n, edges, removed=frozenset()):
    adj = adjacency(n, edges, removed)
    return tuple(distance(adj, a,b) for a,b in ((0,1),(0,2),(1,2)))

def geodesics(n, edges):
    adj = adjacency(n, edges)
    edge_index={frozenset(e):i for i,e in enumerate(edges)}
    all_paths=set()
    for start,finish in ((0,1),(0,2),(1,2)):
        target=distance(adj,start,finish)
        if target == float('inf'): continue
        def visit(path):
            x=path[-1]
            if len(path)-1 == target:
                if x==finish:
                    all_paths.add(frozenset(edge_index[frozenset((a,b))] for a,b in zip(path,path[1:])))
                return
            for y in adj[x]:
                if y not in path: visit(path+[y])
        visit([start])
    return all_paths

def cover(vertices, h_edges, selected):
    return all(a in selected or b in selected for a,b in h_edges)

def covers(vertices, h_edges):
    for mask in range(1 << len(vertices)):
        selected=frozenset(v for i,v in enumerate(vertices) if mask>>i&1)
        if cover(vertices,h_edges,selected): yield selected

def tau(vertices,h_edges):
    return min(map(len,covers(vertices,h_edges)))

def minimum_hitting_set(pathsets):
    # Dynamic recursion on the residual family of paths, independent of H-covers.
    @lru_cache(None)
    def solve(paths):
        if not paths: return 0
        chosen=min(paths,key=len)
        return 1+min(solve(tuple(p for p in paths if edge not in p)) for edge in chosen)
    canonical=tuple(sorted((tuple(sorted(p)) for p in pathsets),key=lambda p:(len(p),p)))
    return solve(canonical)

def graph(parts,h_edges,backups=False):
    vertices=tuple(v for part in parts for v in part)
    edges=[(terminal,v) for terminal,part in enumerate(parts) for v in part]+list(h_edges)
    n=max((2,)+vertices)+1
    if backups:
        for a,b in ((0,1),(0,2),(1,2)):
            path=(a,n,n+1,n+2,b); n+=3
            edges.extend(zip(path,path[1:]))
    return n,edges,vertices

def endpoint_covers(parts,h_edges,removed):
    vertices=tuple(v for part in parts for v in part)
    selected={vertices[i] for i in removed if i<len(vertices)}
    selected_edges=[h_edges[i-len(vertices)] for i in removed if len(vertices)<=i<len(vertices)+len(h_edges)]
    for choices in product(*selected_edges):
        yield selected|set(choices)

def tripartite_suite():
    for sizes in ((1,1,1),(2,1,1)):
        parts=[]; cursor=3
        for size in sizes:
            parts.append(tuple(range(cursor,cursor+size))); cursor+=size
        choices=tuple((a,b) for i,j in ((0,1),(0,2),(1,2)) for a in parts[i] for b in parts[j])
        for hmask in range(1<<len(choices)):
            h=tuple(e for i,e in enumerate(choices) if hmask>>i&1)
            n,edges,vertices=graph(parts,h)
            d=distances(n,edges)
            types=tuple(any(a in parts[i] and b in parts[j] or b in parts[i] and a in parts[j] for a,b in h) for i,j in ((0,1),(0,2),(1,2)))
            require(tuple(x==3 for x in d)==types,'cross-part premise failed')
            count('graphs_including_premise_negative_controls')
            if not all(types): continue
            expected_paths={frozenset((vertices.index(a),vertices.index(b),len(vertices)+i)) for i,(a,b) in enumerate(h)}
            require(geodesics(n,edges)==expected_paths,'unexpected original geodesic')
            best=len(edges)
            nb,eb,_=graph(parts,h,True)
            require(geodesics(nb,eb)==expected_paths,'backup introduced geodesic')
            for fmask in range(1<<len(edges)):
                removed=frozenset(i for i in range(len(edges)) if fmask>>i&1)
                feasible=all(x>=4 for x in distances(n,edges,removed))
                hits=all(path&removed for path in expected_paths)
                require(feasible==hits,'distance and geodesic tests disagree')
                count('original_deletion_subsets')
                if not feasible: continue
                best=min(best,len(removed)); count('feasible_original_deletions')
                for extracted in endpoint_covers(parts,h,removed):
                    require(len(extracted)<=len(removed) and cover(vertices,h,extracted),'arbitrary middle-edge conversion invalid')
                    count('arbitrary_endpoint_conversion_choices')
                # Every one-edge perturbation to a backup path is checked. Its deletion
                # cannot create a geodesic or evade the original cover lower bound.
                for backup_edge in range(len(edges),len(eb)):
                    augmented=removed|{backup_edge}
                    require(all(x>=4 for x in distances(nb,eb,augmented)),'backup deletion lost feasibility')
                    count('arbitrary_single_backup_edge_deletions')
            require(best==tau(vertices,h),'full deletion optimum differs from H-cover')
            require(minimum_hitting_set(geodesics(nb,eb))==best,'backup unrestricted optimum differs')
            for selected in covers(vertices,h):
                removed=frozenset(vertices.index(v) for v in selected)
                require(distances(nb,eb,removed)==(4,4,4),'finite strengthening not exactly four')
                count('finite_cover_checks')
            count('eligible_tripartite_graphs')
    # Isolates in every part remain permitted under the edge-type hypothesis.
    parts=((3,4),(5,6),(7,8)); h=((3,5),(3,7),(5,7))
    n,edges,vertices=graph(parts,h)
    require(distances(n,edges)==(3,3,3),'isolates changed original distances')
    require(minimum_hitting_set(geodesics(n,edges))==tau(vertices,h)==2,'isolates changed optimum')
    selected=frozenset((3,5)); nb,eb,_=graph(parts,h,True)
    require(distances(nb,eb,frozenset(vertices.index(v) for v in selected))==(4,4,4),'finite isolate case failed')
    require(len(adjacency(nb,eb,frozenset(vertices.index(v) for v in selected))[3])>0,'unexpected isolate premise')
    count('isolate_fixture')

def subdivide(vertices,q):
    a=tuple(v+3 for v in vertices); b=[]; c=[]; h=[]; cursor=3+len(vertices)
    for u,v in q:
        be,ce=cursor,cursor+1; cursor+=2; b.append(be); c.append(ce)
        h.extend(((u+3,be),(be,ce),(ce,v+3)))
    return (a,tuple(b),tuple(c)),tuple(h)

def source_suite():
    for n in range(0,5):
        vertices=tuple(range(n)); possible=tuple(combinations(vertices,2))
        for qmask in range(1<<len(possible)):
            q=tuple(e for i,e in enumerate(possible) if qmask>>i&1)
            t=tau(vertices,q)
            if not q:
                require(t==0,'empty graph not zero-cover')
                # Total reduction uses the fixed triangle-spoke graph and B=2.
                nf,ef,_=graph(((3,),(4,),(5,)),((3,4),(3,5),(4,5)))
                require(minimum_hitting_set(geodesics(nf,ef))<=2,'fixed yes-instance wrong')
                count('edgeless_total_reduction_checks'); continue
            parts,h=subdivide(vertices,q); nh,eh,hvertices=graph(parts,h)
            ht=tau(hvertices,h); optimum=minimum_hitting_set(geodesics(nh,eh))
            require(ht==len(q)+t==optimum,'composed reduction optimum identity false')
            require(nh==n+2*len(q)+3 and len(eh)==n+5*len(q),'construction size mismatch')
            require(distances(nh,eh)==(3,3,3),'source construction distance not three')
            for k in (0,1,n,n+1,(1<<4096)-1):
                budget=len(q)+k
                require((t<=k)==(optimum<=budget),'binary budget equivalence false')
                require(budget.bit_length()<=max(k.bit_length(),len(q).bit_length())+1,'budget bit bound failed')
                count('budget_checks_including_4096_bit_k')
            # Enumerate every H-cover, test the lemma's reverse inequality even for
            # nonminimal covers and endpoints uncovered in the source graph.
            for x in covers(hvertices,h):
                s={v-3 for v in x if v in parts[0]}
                uncovered=[e for e in q if not(set(e)&s)]
                require(len(x)>=len(s)+len(q)+len(uncovered),'cover reverse gadget inequality failed')
                extended=s|{e[0] for e in uncovered}
                require(cover(vertices,q,extended) and len(extended)<=len(x)-len(q),'source cover extraction failed')
                count('all_subdivision_cover_checks')
            count('nonempty_source_graphs')

if __name__=='__main__':
    began=time.monotonic(); tripartite_suite(); source_suite()
    result={'status':'PASS','python':platform.python_version(),'optimization_level':__import__('sys').flags.optimize,'counts':COUNTS,'seconds':time.monotonic()-began,'scope':'Finite consistency checks plus implementation checks; universal lemmas require proof.'}
    output=Path(__file__).with_name('independent_structural_results'+('_optimized' if __import__('sys').flags.optimize else '')+'.json')
    output.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
