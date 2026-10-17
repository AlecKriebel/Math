"""Fresh exact support-order reconstruction, with integral cycle witnesses.

Coverage: every ordered partition of simplex vertex heights is realized by a
linear functional after subtracting height[0]. Together with t in {-1,0,1}
this meets every normal cone of the product sum. No imported supplied checker.
"""
from itertools import product, combinations
from fractions import Fraction
from collections import Counter,deque
import json

def require(condition, message):
    if not condition: raise RuntimeError(message)

def rank(rows):
    a=[[Fraction(x) for x in row] for row in rows]
    if not a:return 0
    r=0
    for c in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][c]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        v=a[r][c];a[r]=[x/v for x in a[r]]
        for i in range(r+1,len(a)):
            v=a[i][c]
            if v:a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def dim(points):
    p=list(points);return rank([[x-y for x,y in zip(q,p[0])] for q in p[1:]])
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def expose(points,u):
    heights={p:sum(a*b for a,b in zip(p,u)) for p in points};m=max(heights.values())
    return frozenset(p for p,h in heights.items() if h==m)
def weak_orders(k):
    for s in range(1,k+1):
        for h in product(range(s),repeat=k):
            if len(set(h))==s:yield h

def faces(m,interval=True,lengths=(1,1),shear=False):
    zero=(0,)*m
    simplex=[zero]+[tuple(int(i==j) for i in range(m)) for j in range(m)]
    # An invertible integral affine map, preserving all ranks and inclusions.
    def transform(p):
        if not shear:return p
        return tuple(p[i]+(2*p[i+1] if i+1<len(p) else 0) + 7*(i+1) for i in range(len(p)))
    P=[v+(z,) for v in simplex for z in (0,lengths[0])] if interval else simplex
    Q=[tuple(-x for x in v)+(z,) for v in simplex for z in (0,lengths[1])] if interval else [tuple(-x for x in v) for v in simplex]
    # We transform support-selected sets after exposing; invertibility ensures
    # transformed witnesses exist, without floating inverse computations.
    records={};normal_count=0
    for h in weak_orders(m+1):
        u=tuple(x-h[0] for x in h[1:])
        for t in (-1,0,1) if interval else (None,):
            normal_count+=1
            w=u+(t,) if interval else u
            F=expose(P,w);G=expose(Q,w)
            F=frozenset(map(transform,F));G=frozenset(map(transform,G))
            H=frozenset(add(x,y) for x in F for y in G)
            value=(dim(F),dim(G),dim(H),t)
            old=records.get(H)
            require(old is None or old[:3]==value[:3],'canonical face dimensions inconsistent')
            records[H]=value
    return records,normal_count

def graph_certificate(records):
    selected=sorted([f for f,(a,b,c,t) in records.items() if a>0 and b>0 and c==a+b],key=lambda x:(len(x),sorted(x)))
    edges=[(i,j) for i,f in enumerate(selected) for j,g in enumerate(selected) if f<g]
    require(not any(selected[i]<selected[j]<selected[k] for i,j in edges for j2,k in edges if j2==j),'higher chain')
    adj=[[] for f in selected]
    for e,(i,j) in enumerate(edges):adj[i].append((j,e));adj[j].append((i,e))
    seen=set();tree=set();components=[];cycles=[]
    for root in range(len(selected)):
        if root in seen:continue
        parent={root:(None,None)};todo=deque([root]);seen.add(root)
        while todo:
            u=todo.popleft()
            for v,e in adj[u]:
                if v in seen:continue
                seen.add(v);parent[v]=(u,e);tree.add(e);todo.append(v)
        components.append(sorted(parent))
        for e,(a,b) in enumerate(edges):
            if a not in parent or e in tree:continue
            # A unique chord with coefficient +1, completed along tree from b to a.
            todo=deque([b]);pred={b:(None,None)}
            while a not in pred:
                u=todo.popleft()
                for v,f in adj[u]:
                    if f in tree and v not in pred:pred[v]=(u,f);todo.append(v)
            cycle={e:1};u=a
            while pred[u][0] is not None:
                v,f=pred[u];cycle[f]=1 if edges[f]==(v,u) else -1;u=v
            boundary=Counter()
            for f,c in cycle.items():
                x,y=edges[f];boundary[x]-=c;boundary[y]+=c
            require(not any(boundary.values()),'cycle boundary nonzero')
            require(all(f in tree or f==e for f in cycle),'nonunique chord')
            cycles.append(cycle)
    require(all(adj),'purity')
    require(len(tree)==len(selected)-len(components),'tree rank')
    require(len(cycles)==len(edges)-len(tree),'cycle spanning rank')
    return {'vertices':len(selected),'edges':len(edges),'component_sizes':sorted(map(len,components)),
            'degree_histogram':dict(sorted(Counter(map(len,adj)).items())),
            'integral_boundary_rank':len(tree),'integral_cycle_basis_rank':len(cycles),
            'cycles_zero_boundary_and_unique_chord':True},selected,edges

def components_of_poset(fs):
    remaining=set(range(len(fs)));count=0
    while remaining:
        count+=1;todo=[remaining.pop()]
        while todo:
            i=todo.pop();more={j for j in remaining if fs[i]<fs[j] or fs[j]<fs[i]}
            remaining-=more;todo.extend(more)
    return count

rec,n=faces(4)
answer,selected,edges=graph_certificate(rec)
require(len(rec)==543 and n==1623,'exhaustive normal count')
require(answer['component_sizes']==[50,50] and answer['edges']==120,'main count')
require(answer['integral_boundary_rank']==98 and answer['integral_cycle_basis_rank']==22,'main homology')
require(Counter(c for f,(a,b,c,t) in rec.items() if f in selected)=={2:60,3:40},'dimension histogram')
vertical=[(a,b,c) for a,b,c,t in rec.values() if t==0]
require(all(c<a+b for a,b,c in vertical),'excluded vertical face passed')
# Lower-bound definition intentionally includes bridge faces; verify an explicit witness.
broad=[f for f,(a,b,c,t) in rec.items() if a>=1 and b>=1 and 2<=c<5]
require(components_of_poset(broad)==1,'broader definition did not reconnect')
bridge=[f for f,(a,b,c,t) in rec.items() if t==0 and (a,b,c)==(2,2,3)]
require(len(bridge)==30 and all(f not in selected for f in bridge),'definition witness')
# Invariance under unequal common segment lengths and nonorthogonal affine coordinates.
variants=[]
for lengths,shear in [((2,3),False),((2,3),True)]:
    r,nn=faces(4,lengths=lengths,shear=shear);ans,_,_=graph_certificate(r)
    require(ans==answer and len(r)==543,'affine or segment length invariant failed')
    variants.append({'lengths':lengths,'invertible_integral_affine_map':shear,'same_certificate':True})
base,_=faces(4,interval=False);base_ans,_,_=graph_certificate(base)
require(base_ans['component_sizes']==[50] and base_ans['integral_cycle_basis_rank']==11,'base')
small,_=faces(3,interval=False)
points=[f for f,(a,b,c,t) in small.items() if a*b>0 and c==a+b]
require(len(points)==6 and not any(f<g for f in points for g in points),'tetrahedron control')
# A whole face really can qualify for lower-dimensional transverse summands.
F={(0,0),(1,0)};G={(0,0),(0,1)};H={add(x,y) for x in F for y in G}
require((dim(F),dim(G),dim(H))==(1,1,2),'whole positive control')
# Deleting one component would wrongly make the shellability obstruction disappear;
# a graph shelling is given by rooted tree discovery, followed by all remaining edges.
require(base_ans['component_sizes']==[50] and all(base_ans['degree_histogram']),'connected graph shelling control')
print(json.dumps({'coverage':'all weak orders on five simplex heights times three interval signs',
 'normal_representatives':n,'nonempty_sum_faces':len(rec),'main':answer,
 'base':base_ans,'variants':variants,'vertical_face_count':len(vertical),
 'vertical_dimension_deficit_histogram':dict(Counter(a+b-c for a,b,c in vertical)),
 'broader_filter':{'faces':len(broad),'components':1,'explicit_vertical_223_witnesses':len(bridge)},
 'adverse_controls':{'six_point_zero_dimensional_shellable_control':len(points),
 'transverse_segments_whole_face_qualifies':True,'separate_base_graph_shellable':True,
 'no_artificial_extrema_used':True}},indent=2,sort_keys=True))
