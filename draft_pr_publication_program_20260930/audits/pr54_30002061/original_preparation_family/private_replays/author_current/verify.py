#!/usr/bin/env python3
"""Exact planar collapse certificates; not a higher-dimensional search."""
from fractions import Fraction as F
from itertools import combinations
from collections import defaultdict,deque
from pathlib import Path
import hashlib,json
checks=0
stats=[]
def ck(v):
    global checks
    assert v
    checks+=1
def closure(triangles):
    faces=set()
    for tri in triangles:
        V=sorted(tri)
        for n in range(1,len(V)+1):faces.update(frozenset(c) for c in combinations(V,n))
    return faces
def area(tri):
    a,b,c=sorted(tri)
    return abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2
def grid(n):
    P=lambda i,j:(F(i,n),F(j,n))
    tr=[]
    for i in range(n):
        for j in range(n-i):
            tr.append(frozenset([P(i,j),P(i+1,j),P(i,j+1)]))
            if i+j<=n-2:tr.append(frozenset([P(i+1,j),P(i+1,j+1),P(i,j+1)]))
    return tr
def refine(triangles,steps):
    tr=list(triangles)
    for k in range(steps):
        i=(7*k+3)%len(tr);tri=tr.pop(i);c=tuple(sum(p[j] for p in tri)/3 for j in range(2))
        tr.extend(frozenset([*edge,c]) for edge in combinations(sorted(tri),2))
    return tr
def key(face):return tuple(sorted(face))
def target(faces):return {f for f in faces if all(p[0]==0 for p in f) or all(p[1]==0 for p in f)}
def admissible_pair(faces,small,big,K):
    return small in faces and big in faces and small not in K and big not in K and len(big)==len(small)+1 and small<big and {f for f in faces if small<f}=={big}
def remove(faces,small,big,K):
    ck(admissible_pair(faces,small,big,K));faces.remove(small);faces.remove(big);ck(K<=faces)
def certificate(triangles):
    faces=closure(triangles);K=target(faces);start=set(faces)
    ck(all(area(T)>0 for T in triangles));ck(sum(area(T) for T in triangles)==F(1,2))
    edges=defaultdict(list)
    for T in triangles:
        for e in combinations(sorted(T),2):edges[frozenset(e)].append(T)
    ck(all(len(v) in (1,2) for v in edges.values()))
    rootedge=min((e for e,v in edges.items() if len(v)==1 and e not in K),key=key)
    root=edges[rootedge][0];parentedge={root:rootedge};order=[root];queue=deque([root]);adj=defaultdict(list)
    for e,ts in edges.items():
        if len(ts)==2:adj[ts[0]].append((ts[1],e));adj[ts[1]].append((ts[0],e))
    while queue:
        T=queue.popleft()
        for U,e in sorted(adj[T],key=lambda v:key(v[0])):
            if U not in parentedge:parentedge[U]=e;order.append(U);queue.append(U)
    ck(len(order)==len(triangles));moves=[]
    for T in order:
        e=parentedge[T];remove(faces,e,T,K);moves.append((e,T))
    ck(all(len(f)<=2 for f in faces))
    vertices={next(iter(f)) for f in faces if len(f)==1};E=[f for f in faces if len(f)==2]
    ck(len(E)==len(vertices)-1)
    nbr=defaultdict(set)
    for e in E:
        a,b=tuple(e);nbr[a].add(b);nbr[b].add(a)
    reached={next(iter(vertices))};queue=deque(reached)
    while queue:
        for u in nbr[queue.popleft()]-reached:reached.add(u);queue.append(u)
    ck(reached==vertices)
    while faces!=K:
        E=[f for f in faces if len(f)==2];degree=defaultdict(int)
        for e in E:
            for v in e:degree[v]+=1
        leaves=[v for v,deg in degree.items() if deg==1 and frozenset([v]) not in K]
        ck(bool(leaves));v=min(leaves);small=frozenset([v]);big=next(e for e in E if v in e)
        remove(faces,small,big,K);moves.append((small,big))
    ck(faces==K)
    return start,K,moves
sample=None
for n in range(1,13):
    T=grid(n);C,K,moves=certificate(T)
    stats.append({'grid_denominator':n,'stellar_insertions':0,'triangles':len(T),'moves':len(moves),'target_faces':len(K)})
    if n==2:sample=(C,K,moves)
    # Glue an independently triangulated lower triangle along the protected axis.
    if n<=6:
        outside=closure([frozenset((x,-y) for x,y in tri) for tri in T])
        ck(C&outside<=K);G=C|outside;protected=K|outside
        for small,big in moves:remove(G,small,big,protected)
        ck(G==protected)
for n in range(1,6):
    for steps in [5,10,15]:
        T=refine(grid(n),steps);C,K,moves=certificate(T)
        stats.append({'grid_denominator':n,'stellar_insertions':steps,'triangles':len(T),'moves':len(moves),'target_faces':len(K)})
# A topologically free pair that destroys the prescribed target must be rejected.
T=grid(1);C=closure(T);K=target(C);bad=min((f for f in K if len(f)==2),key=key)
ck({f for f in C if bad<f}=={T[0]});ck(not admissible_pair(C,bad,T[0],K))
# Publish one small explicit certificate with rational coordinate labels.
C,K,moves=sample;vertices=sorted({v for face in C for v in face});index={v:i for i,v in enumerate(vertices)}
enc=lambda face:sorted(index[v] for v in face)
cert={'vertices':[[str(x),str(y)] for x,y in vertices],'initial_faces':sorted([enc(f) for f in C],key=lambda f:(len(f),f)),'protected_faces':sorted([enc(f) for f in K],key=lambda f:(len(f),f)),'collapse_pairs':[{'free_face':enc(a),'coface':enc(b)} for a,b in moves]}
root=Path(__file__).resolve().parent
(root/'sample_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
result={'passed':checks,'failed':0,'cases':stats,'glued_region_cases':6,'arithmetic':'exact rational coordinates and finite face-set checks','scope':'Planar certificates and relative gluing controls only; no universal higher-dimensional proof or counterexample.','partial_sha256':hashlib.sha256((root/'PARTIAL.md').read_bytes()).hexdigest()}
(root/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':checks,'failed':0,'cases':len(stats),'glued_region_cases':6,'partial_sha256':result['partial_sha256']}))
