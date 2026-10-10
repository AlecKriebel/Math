#!/usr/bin/env python3
"""Independent finite/BFS controls of credited statements. No theorem or novelty claim."""
import json, hashlib
from collections import deque
from itertools import product
from pathlib import Path

checks=0

def require(x):
    global checks
    assert x
    checks+=1

def bfs(identity, generators, mul, depth=None):
    lengths={identity:0};todo=deque([identity])
    while todo:
        x=todo.popleft()
        if depth is not None and lengths[x]==depth: continue
        for t in generators:
            y=mul(x,t)
            if y not in lengths:
                lengths[y]=lengths[x]+1;todo.append(y)
    return lengths

def interval_data(top, identity, lengths, mul, inverse):
    vertices=sorted((x for x in lengths if (r:=mul(inverse(x),top)) in lengths and lengths[x]+lengths[r]==lengths[top]), key=lambda x:(lengths[x],x))
    lo=[];hi=[0]*len(vertices)
    for j,y in enumerate(vertices):
        lower=0
        for i,x in enumerate(vertices):
            xy=mul(inverse(x),y)
            if xy in lengths and lengths[x]+lengths[xy]==lengths[y]:
                lower|=1<<i;hi[i]|=1<<j
        lo.append(lower)
    # Test actual least/greatest bounds, without using number of minimal rank bounds.
    failures=[]
    for i,x in enumerate(vertices):
        for j in range(i,len(vertices)):
            y=vertices[j]; upper=hi[i]&hi[j]; lower=lo[i]&lo[j]
            joins=[];meets=[]
            for k in range(len(vertices)):
                if upper>>k&1 and upper&hi[k]==upper: joins.append(vertices[k])
                if lower>>k&1 and lower&lo[k]==lower: meets.append(vertices[k])
            if len(joins)!=1 or len(meets)!=1:
                failures.append({'pair':[x,y], 'join_count':len(joins), 'meet_count':len(meets)})
                return {'vertices':vertices,'lattice':False,'failure':failures[0]}
    return {'vertices':vertices,'lattice':True}

# Quaternion multiplication avoids reusing the submitted S3 model.
base=[[(0,0),(0,1),(0,2),(0,3)],[(0,1),(1,0),(0,3),(1,2)],[(0,2),(1,3),(1,0),(0,1)],[(0,3),(0,2),(1,1),(1,0)]]
def qmul(a,b):
    s,k=base[a[1]][b[1]]
    return ((a[0]+b[0]+s)%2,k)
def qinv(a): return (a[0] if a[1]==0 else 1-a[0],a[1])
Q=list(product(range(2),range(4))); q1=(0,0)
e=(q1,0,0)
def pmul(a,b): return (qmul(a[0],b[0]),(a[1]+b[1])%4,(a[2]+b[2])%6)
def pinv(a): return (qinv(a[0]),(-a[1])%4,(-a[2])%6)
T={(q,0,0) for q in Q if q!=q1}|{(q1,1,0),(q1,3,0),(q1,0,1),(q1,0,5)}
d=bfs(e,T,pmul);require(len(d)==192)
require(all(pinv(t) in T for t in T))
require(all(pmul(pmul(x,t),pinv(x)) in T for x in d for t in T))
require(all(v==int(x[0]!=q1)+min(x[1],4-x[1])+min(x[2],6-x[2]) for x,v in d.items()))
positive=0; sizes={}
for g in d:
    out=interval_data(g,e,d,pmul,pinv)
    require(out['lattice']);positive+=1;sizes[len(out['vertices'])]=sizes.get(len(out['vertices']),0)+1

# Degenerate order-two factor and identity checked separately.
e2=(0,0); add2=lambda a,b:((a[0]+b[0])%2,(a[1]+b[1])%2);inv2=lambda a:a
T2={(1,0),(0,1)};d2=bfs(e2,T2,add2)
for g in d2: require(interval_data(g,e2,d2,add2,inv2)['lattice'])

# Unbounded groups enumerated by word radius, not by the asserted metric formulas.
zero=(0,0);add=lambda a,b:(a[0]+b[0],a[1]+b[1]);neg=lambda a:(-a[0],-a[1])
axis={(1,0),(-1,0),(0,1),(0,-1)};king=set(product(range(-1,2),repeat=2))-{zero}
da=bfs(zero,axis,add,10);dk=bfs(zero,king,add,10)
require(all(v==abs(x[0])+abs(x[1]) for x,v in da.items()))
require(all(v==max(abs(x[0]),abs(x[1])) for x,v in dk.items()))
axial_count=0
for g,l in da.items():
    if l<=5: require(interval_data(g,zero,da,add,neg)['lattice']);axial_count+=1
ia=interval_data((3,0),zero,da,add,neg);ik=interval_data((3,0),zero,dk,add,neg)
require(ia['lattice'] and len(ia['vertices'])==4)
require(not ik['lattice'] and len(ik['vertices'])==8)
# Independently count both missing join and meet for the exact imported witness.
a,b,x,y=(1,0),(1,1),(2,0),(2,1)
le=lambda p,q:dk[p]+dk[add(neg(p),q)]==dk[q]
ups=[z for z in ik['vertices'] if le(a,z) and le(b,z)]
mins=[z for z in ups if not any(v!=z and le(v,z) for v in ups)]
lows=[z for z in ik['vertices'] if le(z,x) and le(z,y)]
maxs=[z for z in lows if not any(v!=z and le(z,v) for v in lows)]
require(set(mins)=={x,y});require(set(maxs)=={a,b})

# Independent finite Coxeter spot controls, with signed permutations for D4/D6.
def dtype(n):
    ident=tuple(range(1,n+1)); central=tuple(-i for i in ident)
    def mul(a,b):return tuple((1 if v>0 else -1)*a[abs(v)-1] for v in b)
    def inv(a):
        r=[0]*n
        for i,v in enumerate(a):r[abs(v)-1]=(i+1)*(1 if v>0 else -1)
        return tuple(r)
    gen=[]
    for i in range(n):
        for j in range(i+1,n):
            for sign in [1,-1]:
                r=list(ident);r[i]=sign*(j+1);r[j]=sign*(i+1);gen.append(tuple(r))
    dist=bfs(ident,gen,mul)
    result=interval_data(central,ident,dist,mul,inv)
    require(len(dist)==(192 if n==4 else 23040))
    require(result['lattice']==(n==4))
    return {'group_order':len(dist),'reflection_count':len(gen),'endpoint':'central -I (longest element)','endpoint_length':dist[central], 'interval_size':len(result['vertices']),'lattice':result['lattice'],'first_failure':result.get('failure')}
cox={str(n):dtype(n) for n in (4,6)}
result={'status':'PASS','assertions':checks,'positive_Q8_C4_C6_intervals':positive,'product_interval_size_histogram':sizes,'positive_C2_C2_intervals':4,'positive_Z2_axial_endpoints_radius_5':axial_count,'same_group_same_endpoint_marking_control':{'endpoint':[3,0],'axis_interval':ia['vertices'],'axis_lattice':ia['lattice'],'king_interval':ik['vertices'],'king_lattice':ik['lattice'],'king_minimal_upper_bounds':mins,'king_maximal_lower_bounds':maxs},'finite_Coxeter_spot_checks':cox,'limits':'Independent exact finite controls only. General claims rest on the credited proofs/theorems; computations establish neither novelty nor exhaustive source resolution.'}
print(json.dumps(result,indent=2))
