#!/usr/bin/env python3
"""Independent finite controls of protected relative collapse; no high-dimensional certificate."""
from fractions import Fraction as Q
from itertools import combinations
from collections import Counter, defaultdict, deque
from pathlib import Path
import json

counts=Counter()
def check(x,label):
    assert x,label
    counts[label]+=1

def faces(facets):
    return {frozenset(c) for f in facets for n in range(1,len(f)+1) for c in combinations(sorted(f),n)}

def admissible(C,a,b,K):
    return (bool(a) and a in C and b in C and a < b and len(a)+1==len(b)
            and a not in K and b not in K and {f for f in C if a<f}=={b})

def validate(initial,target,moves):
    C=set(initial)
    check(target<=C,'target_in_initial')
    for a,b in moves:
        check(admissible(C,a,b,target),'valid_free_pair')
        C.difference_update((a,b))
        check(target<=C,'protected_faces_survive')
        check(all(g in C for f in C for g in faces([f])),'downward_closed_after_move')
    check(C==target,'exact_final_target')
    return C

def boundary(tri):
    e=Counter(frozenset(x) for t in tri for x in combinations(sorted(t),2))
    check(all(n in (1,2) for n in e.values()),'manifold_edge_incidence')
    b={f for f,n in e.items() if n==1}
    adj=defaultdict(list)
    for u,v in map(tuple,b):adj[u].append(v);adj[v].append(u)
    check(all(len(x)==2 for x in adj.values()),'boundary_cycle_degree')
    first=min(adj);cycle=[first];prev=None;cur=first
    while True:
        nxt=min(v for v in adj[cur] if v!=prev)
        if nxt==first:break
        cycle.append(nxt);prev,cur=cur,nxt
    check(len(cycle)==len(b),'one_boundary_cycle')
    return cycle,b

def certificate(tri,K,reverse=False):
    incid=defaultdict(list)
    for t in tri:
        for e in combinations(sorted(t),2):incid[frozenset(e)].append(t)
    rootedge=sorted((e for e,v in incid.items() if len(v)==1 and e not in K),
                    key=lambda e:tuple(sorted(e)),reverse=reverse)[0]
    root=incid[rootedge][0];parent={root:rootedge};todo=[root]
    # Depth-first traversal, distinct from the submitted breadth-first traversal.
    stack=[root]
    while stack:
        t=stack.pop()
        for e in sorted(faces([t]),key=lambda f:(len(f),tuple(sorted(f))),reverse=reverse):
            if len(e)!=2:continue
            for u in incid[e]:
                if u not in parent:
                    parent[u]=e;todo.append(u);stack.append(u)
    check(len(parent)==len(tri),'dual_tree_spans')
    C=faces(tri);moves=[]
    for t in todo:
        e=parent[t];check(admissible(C,e,t,K),'generator_triangle_pair')
        C.remove(e);C.remove(t);moves.append((e,t))
    check(all(len(f)<=2 for f in C),'residual_is_graph')
    vertices={next(iter(f)) for f in C if len(f)==1}
    edges=[f for f in C if len(f)==2]
    check(len(edges)==len(vertices)-1,'residual_tree_euler')
    while C!=K:
        adj=defaultdict(list)
        for e in C:
            if len(e)==2:
                for v in e:adj[v].append(e)
        opts=[v for v in vertices if frozenset([v]) not in K and len(adj[v])==1]
        check(bool(opts),'unprotected_leaf_exists')
        v=max(opts) if reverse else min(opts);a=frozenset([v]);b=adj[v][0]
        C.remove(a);C.remove(b);vertices.remove(v);moves.append((a,b))
    return moves

def area2(P,t):
    a,b,c=(P[i] for i in t)
    return abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))

def mesh(stage):
    P=[(Q(0),Q(0)),(Q(1),Q(0)),(Q(0),Q(1))]
    T={frozenset([0,1,2])}
    for k in range(stage):
        ordered=sorted(T,key=lambda t:tuple(sorted(t)))
        if k%3==0:
            edgecounts=Counter(e for t in T for e in combinations(sorted(t),2))
            bd=sorted(e for e,n in edgecounts.items() if n==1)
            a,b=bd[(5*k+1)%len(bd)]
            v=len(P);P.append(tuple((2*P[a][j]+P[b][j])/3 for j in (0,1)))
            t=next(t for t in T if {a,b}<=t);c=next(iter(t-{a,b}))
            T.remove(t);T.update([frozenset([a,v,c]),frozenset([v,b,c])])
        else:
            t=ordered[(7*k+2)%len(ordered)];a,b,c=sorted(t);v=len(P)
            P.append(tuple((P[a][j]+2*P[b][j]+3*P[c][j])/6 for j in (0,1)))
            T.remove(t);T.update(frozenset([v,*e]) for e in combinations(sorted(t),2))
    check(all(area2(P,t)>0 for t in T),'nondegenerate_rational_triangles')
    check(sum(area2(P,t) for t in T)==1,'exact_total_area')
    return P,T

stats=[]
for stage in range(0,13):
    P,T=mesh(stage);C=faces(T);cyc,bedges=boundary(T);n=len(cyc)
    # Every singleton and every proper connected boundary arc, not only two original sides.
    targets=[]
    for start in range(n):
        targets.append(faces([(cyc[start],)]))
        for length in range(1,n):
            targets.append(faces([(cyc[(start+j)%n],cyc[(start+j+1)%n]) for j in range(length)]))
    for num,K in enumerate(targets):
        moves=certificate(T,K,reverse=bool(num%2))
        validate(C,K,moves)
        # Glue an abstract cone over the entire protected path using one new vertex.
        # It may have many triangles, but meets the original disk precisely in K.
        apex=len(P)
        external=faces([tuple(f|{apex}) for f in K])
        check(C&external==K,'exact_gluing_intersection')
        validate(C|external,external,moves)
    stats.append({'stellar_steps':stage,'triangles':len(T),'boundary_vertices':n,'targets':len(targets)})

# One-dimensional endpoints, including the unsplit interval.
interval_cases=0
for n in range(1,16):
    C=faces([(i,i+1) for i in range(n)])
    for endpoint in [0,n]:
        K=faces([(endpoint,)])
        order=list(range(n,0,-1)) if endpoint==0 else list(range(n))
        moves=[(frozenset([v]),frozenset([v,v-1 if endpoint==0 else v+1])) for v in order]
        validate(C,K,moves);interval_cases+=1

# Independent replay of the author's small, explicitly listed rational certificate.
root=Path(__file__).resolve().parent
s=json.loads((root/'submitted_sample_certificate.json').read_text())
C={frozenset(f) for f in s['initial_faces']};K={frozenset(f) for f in s['protected_faces']}
moves=[(frozenset(m['free_face']),frozenset(m['coface'])) for m in s['collapse_pairs']]
validate(C,K,moves)

# Adversarial controls: preservation and external cofaces are real requirements.
C=faces([(0,1,2)]);a=frozenset([0,1]);b=frozenset([0,1,2])
K=faces([(0,2),(1,2)])
check(admissible(C,a,b,K),'unprotected_free_pair_is_legal')
check(not admissible(C,frozenset([0,2]),b,K),'reject_target_destroying_pair')
bad_union=C|faces([(0,1,3)])
check(not admissible(bad_union,a,b,K),'reject_new_external_coface')
full_boundary=faces([(0,1),(1,2),(0,2)])
check(not any(admissible(C,f,g,full_boundary) for f in C for g in C),'reject_entire_boundary_target')
check(not admissible(C,frozenset(),frozenset([0]),set()),'reject_empty_face_collapse')

out={'passed':sum(counts.values()),'failed':0,'checks_by_kind':dict(sorted(counts.items())),
     'meshes':stats,'disk_target_cases':sum(x['targets'] for x in stats),
     'gluing_cases':sum(x['targets'] for x in stats),'interval_cases':interval_cases,
     'submitted_sample_certificate_replayed':True,
     'scope':'Finite exact relative-collapse controls in dimensions one and two; no higher-dimensional result.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('checks_by_kind','meshes')},indent=2))
