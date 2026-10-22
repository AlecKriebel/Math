"""Fresh review: exhaust all ordered height types, then certify graph cycles.

No imports of distributed programs or their expected outputs. The five affine
simplex vertices identify a functional up to additive constant with five heights.
Every ordered partition of those heights has a representative in range(5).
Its extreme sets, together with the sign of the interval functional, completely
determine the exposed faces. Thus this is an exact normal-fan census, not a sample.
"""
from itertools import product
from fractions import Fraction
from collections import Counter, deque
import json

CHECKS = 0
def need(value, message):
    global CHECKS
    CHECKS += 1
    if not value:
        raise RuntimeError(message)

def rank(rows):
    a = [list(map(Fraction, row)) for row in rows]
    r = 0
    if not a:
        return 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = a[r][c]
        a[r] = [x / z for x in a[r]]
        for i in range(r + 1, len(a)):
            z = a[i][c]
            if z:
                a[i] = [x-z*y for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r

def dimension(points):
    p = list(points)
    return rank([[x-y for x,y in zip(q,p[0])] for q in p[1:]])

def plus(a,b):
    return tuple(x+y for x,y in zip(a,b))

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def support(points,u):
    h = max(map(lambda p: dot(p,u),points))
    return frozenset(p for p in points if dot(p,u)==h)

def census(d, interval):
    v = [(0,)*d]+[tuple(int(i==j) for i in range(d)) for j in range(d)]
    p1 = frozenset(x+(t,) for x in v for t in range(2)) if interval else frozenset(v)
    p2 = frozenset(tuple(-z for z in x)+(t,) for x in v for t in range(2)) if interval else frozenset(tuple(-z for z in x) for x in v)
    allpoints = frozenset(plus(x,y) for x in p1 for y in p2)
    faces = {}
    heighttypes = [h for h in product(range(d+1),repeat=d+1) if set(h)==set(range(max(h)+1))]
    for h in heighttypes:
        u0 = tuple(h[i]-h[0] for i in range(1,d+1))
        for t in (-1,0,1) if interval else (None,):
            u = u0+(t,) if interval else u0
            a,b = support(p1,u),support(p2,u)
            f = support(allpoints,u)
            need(f==frozenset(plus(x,y) for x in a for y in b),'Support decomposition')
            record = (dimension(f),dimension(a),dimension(b))
            if f in faces:
                need(faces[f]==record,'Canonical dimensions independent of representative')
            faces[f] = record
    selected = [f for f, (c,a,b) in faces.items() if a>0 and b>0 and c==a+b]
    edges = [(i,j) for i,f in enumerate(selected) for j,g in enumerate(selected) if i<j and (f<g or g<f)]
    need(not any(a<b<c for a in selected for b in selected for c in selected),'No three-element strict chain')
    return faces,selected,edges,len(heighttypes)

def graph_certificate(n, edges):
    adj = [[] for _ in range(n)]
    for k,(a,b) in enumerate(edges):
        adj[a].append((b,k));adj[b].append((a,k))
    parent = {}; tree = set(); comps = []
    for root in range(n):
        if root in parent:
            continue
        parent[root] = None
        comp = []; queue = deque([root])
        while queue:
            a=queue.popleft();comp.append(a)
            for b,k in adj[a]:
                if b not in parent:
                    parent[b]=(a,k);tree.add(k);queue.append(b)
        comps.append(comp)
    incidence = [[0]*len(edges) for _ in range(n)]
    for k,(a,b) in enumerate(edges):
        incidence[a][k]=-1;incidence[b][k]=1
    cycles=[]
    for k,(a,b) in enumerate(edges):
        if k in tree:
            continue
        # Unit non-tree edge a -> b; paths b -> root and root -> a close it.
        z=[0]*len(edges);z[k]=1
        for start,sgn in [(b,1),(a,-1)]:
            cur=start
            while parent[cur] is not None:
                par,e=parent[cur]
                z[e]+=sgn*(1 if edges[e]==(cur,par) else -1)
                cur=par
        need(all(sum(x*y for x,y in zip(row,z))==0 for row in incidence),'Fundamental cycle has zero signed boundary')
        need(all(z[j]==int(j==k) for j in range(len(edges)) if j not in tree),'Non-tree coordinates independent')
        cycles.append(z)
    r=rank(incidence)
    need(r==n-len(comps),'Rational incidence rank equals spanning-forest rank')
    need(rank(cycles)==len(edges)-r,'Explicit independent cycle basis is complete')
    return {'components':sorted(map(len,comps)),'vertices':n,'edges':len(edges),'degrees':dict(sorted(Counter(map(len,adj)).items())), 'boundary_rank':r,'betti':[n-r,len(edges)-r], 'independent_cycles':len(cycles)}

faces,selected,edges,types=census(4,True)
main=graph_certificate(len(selected),edges)
need(types==541,'All 541 ordered height types')
need(len(faces)==543,'543 nonempty faces')
need(dict(Counter(c for c,a,b in faces.values()))=={0:40,1:140,2:200,3:130,4:32,5:1},'Complete f vector')
need(main['components']==[50,50] and main['edges']==120 and main['betti']==[2,22],'Main conclusion')
need(main['degrees']=={2:60,3:40},'Pure graph degrees')
vertical=[(f,dims) for f,dims in faces.items() if len({x[-1] for x in f})>1]
need(all(not (a>0 and b>0 and c==a+b) for _,(c,a,b) in vertical),'Every vertical face fails additivity')
witnesses=[f for f,(c,a,b) in vertical if (c,a,b)==(3,2,2)]
need(len(witnesses)==30,'30 vertical witnesses to strictly broader criterion')
stable=[f for f,(c,a,b) in faces.items() if a>=1 and b>=1 and c>=2]
need(all(f in stable for f in selected) and all(f in stable for f in witnesses),'Stable lower-bound mutation retains vertical bridges')
# Mutation controls: joining components must change H0, while the same cycle
# count persists; deleting an entire component must halve the first Betti rank.
cross=next((a,b) for a in range(len(selected)) for b in range(a+1,len(selected)) if {x[-1] for x in selected[a]}!={x[-1] for x in selected[b]})
joined=graph_certificate(len(selected),edges+[cross])
need(joined['betti']==[1,22],'Cross-edge mutation detected')
end=[i for i,f in enumerate(selected) if {x[-1] for x in f}=={0}]
renumber={x:i for i,x in enumerate(end)}
half=graph_certificate(len(end),[(renumber[a],renumber[b]) for a,b in edges if a in renumber and b in renumber])
need(half['betti']==[1,11],'Component deletion mutation detected')
base3,s3,e3,types3=census(3,False)
small=graph_certificate(len(s3),e3)
need(small['betti']==[6,0] and small['edges']==0,'Six-point shellable control')
need(graph_certificate(3,[(0,1),(1,2)])['betti']==[1,0],'Tree positive control')
need(graph_certificate(3,[(0,1),(1,2),(0,2)])['betti']==[1,1],'Circle positive control')
print(json.dumps({'status':'PASS','checks':CHECKS,'height_types':types,'nonempty_faces':len(faces),'face_dimensions':dict(sorted(Counter(c for c,a,b in faces.values()).items())),'main':main,'vertical_faces':len(vertical),'broader_filter_vertical_witnesses':len(witnesses),'broader_filter_faces':len(stable),'controls':{'cross_component_edge':joined,'delete_component':half,'six_points':small}},indent=2,sort_keys=True))
