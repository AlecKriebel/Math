#!/usr/bin/env python3
"""Independent finite planar-dual/circuit controls, with no archived imports."""
from collections import Counter,deque
from datetime import datetime,timezone
from pathlib import Path
from fractions import Fraction as F
import random,json,hashlib
BASE=Path(__file__).resolve().parent
rng=random.Random(23387753)
counts=Counter()
def check(c,n):
    counts[n]+=1
    if not c:raise AssertionError(n)
def ed(a,b):return tuple(sorted((a,b)))
def adjmap(V,E):
    a={v:[] for v in V}
    for v,w in E:a[v].append(w);a[w].append(v)
    return a
def path(A,a,b):
    parent={a:None};q=deque([a])
    while b not in parent:
        v=q.popleft()
        for w in A[v]:
            if w not in parent:parent[w]=v;q.append(w)
    p=[b]
    while p[-1]!=a:p.append(parent[p[-1]])
    return p[::-1]
def inside(point,polygon):
    x,y=point;ans=False
    for (a,b),(c,d) in zip(polygon,polygon[1:]+polygon[:1]):
        if (b>y)!=(d>y) and x<(c-a)*(y-b)/(d-b)+a:ans=not ans
    return ans

for N in [4,5,6]:
    V=list(range(N*N));xy=lambda v:(v%N,v//N)
    E=[ed(v,w) for v in V for w in V if v<w and sum(abs(a-b) for a,b in zip(xy(v),xy(w)))==1]
    faces=list(range((N-1)**2))+[-1]
    def face(x,y):return y*(N-1)+x if 0<=x<N-1 and 0<=y<N-1 else -1
    def dual(e):
        (x,y),(u,v)=map(xy,e)
        if y==v:return ed(face(min(x,u),y),face(min(x,u),y-1))
        return ed(face(x,min(y,v)),face(x-1,min(y,v)))
    for trial in range(40):
        perm=E[:];rng.shuffle(perm);uf={v:v for v in V}
        def find(v):
            while uf[v]!=v:uf[v]=uf[uf[v]];v=uf[v]
            return v
        T=[]
        for a,b in perm:
            if find(a)!=find(b):uf[find(a)]=find(b);T.append((a,b))
        Tset=set(T);A=adjmap(V,T);parent={0:None};order=[0]
        for v in order:
            for w in A[v]:
                if w not in parent:parent[w]=v;order.append(w)
        past={v:{v} for v in V}
        for v in reversed(order[1:]):past[parent[v]].update(past[v])
        D=[dual(e) for e in E if e not in Tset];DA=adjmap(faces,D)
        dp={-1:None};do=[-1]
        for v in do:
            for w in DA[v]:
                if w not in dp:dp[w]=v;do.append(w)
        check(len(do)==len(faces) and len(D)==len(faces)-1,'dual_complement_is_tree')
        ds={v:{v} for v in faces}
        for v in reversed(do[1:]):ds[dp[v]].update(ds[v])
        size={ed(v,dp[v]):len(ds[v]) for v in do[1:]}
        counts['sampled_grid_trees']+=1
        for child in V[1:]:
            S=past[child];t=ed(child,parent[child])
            cut=[e for e in E if (e[0] in S)!=(e[1] in S)]
            cutdual=[dual(e) for e in cut]
            p=path(DA,*dual(t));pedges=[ed(a,b) for a,b in zip(p,p[1:])]
            check(set(cutdual)==set(pedges+[dual(t)]),'fundamental_dual_cycle_identity')
            check(all(v==2 for v in Counter(v for e in cutdual for v in e).values()),'dual_cut_even_simple_cycle')
            expectation=sum(F(1,4**size[e]) for e in pedges)
            check(expectation<=F(2,3),'dual_bypass_expectation_bound')
            if -1 in p:continue
            # Subdivide the simple dual cycle into a nearest-neighbor fine-grid
            # circuit. Face centers are odd/odd; edge midpoints have mixed parity.
            center=lambda f:(2*(f%(N-1))+1,2*(f//(N-1))+1)
            poly=[]
            for f,g in zip(p,p[1:]+p[:1]):
                a,b=center(f),center(g)
                poly.extend([a,((a[0]+b[0])//2,(a[1]+b[1])//2)])
            check(len(set(poly))==len(poly),'fine_circuit_is_simple')
            check(all(abs(a-c)+abs(b-d)==1 for (a,b),(c,d) in zip(poly,poly[1:]+poly[:1])),'fine_circuit_nearest_neighbor')
            coarse_inside={v for v in V if inside(tuple(2*c for c in xy(v)),poly)}
            check(coarse_inside==S,'fine_circuit_encloses_exact_finite_past')
            tree_midpoints={tuple(a+b for a,b in zip(xy(v),xy(w))) for v,w in T}
            open_sites=[v for v in poly if v in tree_midpoints]
            check(len(open_sites)==1,'exactly_one_initially_open_circuit_midpoint')
            counts['fine_circuits_checked']+=1

result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'counts':dict(counts),'seed':23387753,
        'limits':'Finite planar identities only. The outer face models a wired exterior; its finite rooted tree is not a sample of the infinite UST. The infinite-volume conclusions rely on the written proof and primary spanning-tree results.'}
(BASE/'planar_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
