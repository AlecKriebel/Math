#!/usr/bin/env python3
"""Independent audit controls; does not import or execute the author's checks."""
from collections import deque, Counter
from functools import lru_cache
from itertools import combinations, product, permutations
from pathlib import Path
import hashlib, json, random, time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
R=Counter()
started=time.time()


def vertex_cover(n, edges):
    # Independent exact endpoint-branching solver over remaining edge masks.
    incident=[0]*n
    for i,(u,v) in enumerate(edges):
        incident[u]|=1<<i; incident[v]|=1<<i
    @lru_cache(None)
    def rec(todo):
        if not todo: return 0
        i=(todo & -todo).bit_length()-1
        u,v=edges[i]
        return 1+min(rec(todo & ~incident[u]), rec(todo & ~incident[v]))
    return rec((1<<len(edges))-1)


def brute_cover(n, edges):
    masks=[(1<<u)|(1<<v) for u,v in edges]
    return min(x.bit_count() for x in range(1<<n) if all(x&e for e in masks))


def distances(n, edges, deleted, terminals):
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(edges):
        if not ((deleted>>i)&1):
            adj[u].append(v); adj[v].append(u)
    answer=[]
    for a,b in combinations(terminals,2):
        ds=[n+1]*n; ds[a]=0; queue=deque([a])
        while queue:
            u=queue.popleft()
            for v in adj[u]:
                if ds[v]==n+1:
                    ds[v]=ds[u]+1; queue.append(v)
        answer.append(ds[b])
    return tuple(answer)


def attach(parts, edges):
    w=len(parts); spokes=[(w+p,u) for u,p in enumerate(parts)]
    return w+3,spokes+list(edges),(w,w+1,w+2)


def subdivide(n, oriented):
    edges=[]; parts=[0]*n
    for u,v in oriented:
        b=len(parts); parts.extend([1,2]); c=b+1
        edges.extend([(u,b),(b,c),(c,v)])
    return parts,edges


def added_routes(n,edges,terminals,length=4):
    out=list(edges)
    for a,b in combinations(terminals,2):
        seq=[a]+list(range(n,n+length-1))+[b]; n+=length-1
        out.extend(zip(seq,seq[1:]))
    return n,out


def extracted_cover(w, hedges, deleted, choose_second):
    x=deleted & ((1<<w)-1)
    for j,(u,v) in enumerate(hedges,w):
        if (deleted>>j)&1: x|=1<<(v if choose_second else u)
    return x


def all_deletions_suite(tail):
    parts=[0,1]+[2]*tail; w=len(parts)
    universe=[(u,v) for u,v in combinations(range(w),2) if parts[u]!=parts[v]]
    for hmask in range(1<<len(universe)):
        h=[e for i,e in enumerate(universe) if (hmask>>i)&1]
        if {tuple(sorted((parts[u],parts[v]))) for u,v in h}!={(0,1),(0,2),(1,2)}: continue
        n,g,terminals=attach(parts,h)
        assert distances(n,g,0,terminals)==(3,3,3)
        target=brute_cover(w,h); observed=len(g)
        paths=[(1<<u)|(1<<v)|(1<<(w+j)) for j,(u,v) in enumerate(h)]
        for deleted in range(1<<len(g)):
            ds=distances(n,g,deleted,terminals)
            feasible=all(d>=4 for d in ds)
            assert feasible==all(deleted&p for p in paths)
            R['all_deletion_subsets']+=1
            if feasible:
                R['feasible_blockers']+=1; observed=min(observed,deleted.bit_count())
                for second in (False,True):
                    x=extracted_cover(w,h,deleted,second)
                    assert x.bit_count()<=deleted.bit_count()
                    assert all(x & ((1<<u)|(1<<v)) for u,v in h)
                    R['cover_extractions']+=1
        assert observed==target
        R['all_deletion_graphs']+=1


def path_hitting_optimum(n,g,terminals):
    # Enumerate all simple shortest paths directly from adjacency, independent
    # of the expected spoke/edge formula; solve their minimum hitting set.
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(g): adj[u].append((v,i)); adj[v].append((u,i))
    d=distances(n,g,0,terminals); paths=[]
    for (a,b),depth in zip(combinations(terminals,2),d):
        found=[]
        def walk(u,seen,mask,left):
            if left==0:
                if u==b: found.append(mask)
                return
            for v,e in adj[u]:
                if not (seen>>v)&1: walk(v,seen|(1<<v),mask|(1<<e),left-1)
        walk(a,1<<a,0,depth); paths.extend(found)
    cover_masks=[sum(1<<j for j,p in enumerate(paths) if (p>>e)&1) for e in range(len(g))]
    @lru_cache(None)
    def rec(todo):
        if not todo: return 0
        p=paths[(todo & -todo).bit_length()-1]
        return 1+min(rec(todo & ~cover_masks[e]) for e in range(len(g)) if (p>>e)&1)
    return rec((1<<len(paths))-1),set(paths)


def oriented_subdivisions():
    for n in range(2,5):
        universe=list(combinations(range(n),2))
        for state in product(range(3),repeat=len(universe)):
            q=[((u,v) if direction==1 else (v,u)) for (u,v),direction in zip(universe,state) if direction]
            p,h=subdivide(n,q)
            tq=brute_cover(n,q); th=vertex_cover(len(p),h)
            assert th==len(q)+tq
            R['oriented_subdivision_instances']+=1
            if q:
                ng,g,t=attach(p,h)
                assert ng==n+2*len(q)+3 and len(g)==n+5*len(q)
                assert distances(ng,g,0,t)==(3,3,3)
                opt,paths=path_hitting_optimum(ng,g,t)
                expected={(1<<u)|(1<<v)|(1<<(len(p)+j)) for j,(u,v) in enumerate(h)}
                assert paths==expected and opt==th
                for k in list(range(n+2))+[2**2048]:
                    assert (tq<=k)==(opt<=len(q)+k)
                    R['budget_comparisons']+=1
                R['oriented_compositions']+=1


def larger_subdivisions():
    rng=random.Random(30000347)
    cases=[]
    for n in (5,6,7):
        univ=list(combinations(range(n),2))
        for _ in range(150):
            density=rng.choice([.1,.3,.5,.8,1.0])
            cases.append((n,[((v,u) if rng.randrange(2) else (u,v)) for u,v in univ if rng.random()<density]))
    for n in range(3,11): cases.append((n,[(u,(u+1)%n) for u in range(n)]))
    cases.extend([(6,[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3)]),(7,[(0,1)])])
    for n,q in cases:
        p,h=subdivide(n,q)
        assert vertex_cover(len(p),h)==len(q)+brute_cover(n,q)
        R['larger_subdivision_instances']+=1


def extension_suite():
    cases=[(2,[(0,1)]),(3,[(0,1)]),(3,[(0,1),(1,2)]),(3,[(0,1),(1,2),(2,0)])]
    for nq,q in cases:
        p,h=subdivide(nq,q); ng,g,t=attach(p,h); ne,ge=added_routes(ng,g,t)
        assert distances(ne,ge,0,t)==(3,3,3)
        tau=vertex_cover(len(p),h)
        # Direct BFS search through every sub-optimal deletion set, including
        # deletions on the fallback routes, not just spoke-only candidates.
        for k in range(tau):
            for positions in combinations(range(len(ge)),k):
                deleted=sum(1<<i for i in positions)
                assert not all(d>=4 for d in distances(ne,ge,deleted,t))
                R['extension_suboptimal_subsets']+=1
        for x in range(1<<len(p)):
            if all(x & ((1<<u)|(1<<v)) for u,v in h):
                assert distances(ne,ge,x,t)==(4,4,4)
                R['extension_cover_witnesses']+=1
        R['extension_instances']+=1


def negative_controls():
    # Without all three demands, the edge-path to the omitted pair survives.
    p=[0,1,2]; h=[(0,1),(0,2),(1,2)]; n,g,t=attach(p,h)
    ds=distances(n,g,1,t)
    assert ds[0]>=4 and ds[1]>=4 and ds[2]==3
    # The nonempty cross-part-type assumption cannot simply be omitted.
    n,g,t=attach(p,[(0,1),(1,2)])
    assert distances(n,g,0,t)==(3,4,3)
    # Four-edge fallback paths must not be replaced by three-edge paths.
    n,g,t=attach(p,h); ne,ge=added_routes(n,g,t,3)
    assert distances(ne,ge,(1<<0)|(1<<1),t)==(3,3,3)
    # One subdivision per source edge does not have the stated m+tau shift.
    assert vertex_cover(3,[(0,2),(2,1)])==1 != 1+brute_cover(2,[(0,1)])
    # Unit traversal length differs from deletion cost. Disconnection must
    # remain accepted by the standard model (the first control supplies it).
    assert ds[0]>n and ds[1]>n
    R['negative_controls']=5


def verify_freeze():
    packet=ROOT/'frozen_packet'
    manifest=json.loads((packet/'FROZEN_MANIFEST.json').read_text())
    for filename,expected in manifest['files'].items():
        b=(packet/filename).read_bytes()
        assert len(b)==expected['bytes']
        assert hashlib.sha256(b).hexdigest()==expected['sha256']
        R['frozen_payloads_verified']+=1
    assert hashlib.sha256((packet/'FROZEN_MANIFEST.json').read_bytes()).hexdigest()=='b13c9cee3e806a263ba0e24b2838599692727ea48d26977d4fca714e1e30d273'
    # Fully explicit fixed yes-instance for every edgeless source graph.
    p,h=subdivide(2,[(0,1)]); n,g,t=attach(p,h)
    assert path_hitting_optimum(n,g,t)[0]==2
    R['edgeless_fixed_yes_control']=1

if __name__=='__main__':
    verify_freeze(); negative_controls()
    for tail in (3,4): all_deletions_suite(tail)
    print('Exhaustive deletion suite passed',dict(R),flush=True)
    oriented_subdivisions(); print('Oriented compositions passed',dict(R),flush=True)
    larger_subdivisions(); extension_suite()
    result={'status':'PASS','seed':30000347,'elapsed_seconds':round(time.time()-started,3),'counts':dict(R),'fresh_control_implementation_preceded_author_script_inspection':True,'author_check_code_imported_by_fresh_controls':False,'other_audit_read':False}
    (HERE/'fresh_control_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
