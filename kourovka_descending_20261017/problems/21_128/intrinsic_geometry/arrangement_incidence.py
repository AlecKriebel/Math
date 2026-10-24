#!/usr/bin/env python3
"""Exact Q(phi) reflection-arrangement flat census; no floating-point arithmetic."""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from collections import Counter
from pathlib import Path
import json, argparse, time

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[0],-x[1])
def mul(x,y):
    a,b=x;c,d=y
    return (a*c+b*d,a*d+b*c+b*d)
def sub(x,y): return add(x,neg(y))
def div(x,y):
    a,b=y; n=a*a+a*b-b*b
    if not n: raise ZeroDivisionError
    return mul(x,((a+b)/n,-b/n))
Z=(F(0),F(0)); ONE=(F(1),F(0))
def q(n):return(F(n),F(0))
def norm(v):
    x=next(x for x in v if x!=Z)
    return tuple(div(y,x) for y in v)
def encode(v):return [[str(a),str(b)] for a,b in v]
def roots(kind):
    out=[]
    for i in range(4):
        for s in (-1,1):out.append(tuple(q(2*s) if i==j else Z for j in range(4)))
    for ss in product((-1,1),repeat=4):out.append(tuple(q(s) for s in ss))
    if kind=='F4':
        for i,j in combinations(range(4),2):
            for s,t in product((-1,1),repeat=2):out.append(tuple(q(2*s) if k==i else q(2*t) if k==j else Z for k in range(4)))
    else:
        # Even permutations of (0, +/-1, +/-phi, +/-1/phi), scaled roots by 2.
        for perm in permutations(range(4)):
            if sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))%2:continue
            for a,b,c in product((-1,1),repeat=3):
                v=(Z,q(a),(F(0),F(b)),(F(-c),F(c)))
                out.append(tuple(v[i] for i in perm))
    return sorted(set(norm(v) for v in out))
def wedge2(a,b):return tuple(sub(mul(a[i],b[j]),mul(a[j],b[i])) for i,j in combinations(range(4),2))
def det3(a,b,c):
    return add(sub(mul(a[0],sub(mul(b[1],c[2]),mul(b[2],c[1]))),mul(a[1],sub(mul(b[0],c[2]),mul(b[2],c[0])))),mul(a[2],sub(mul(b[0],c[1]),mul(b[1],c[0]))))
def wedge3(a,b,c):return tuple(det3(tuple(a[i] for i in ix),tuple(b[i] for i in ix),tuple(c[i] for i in ix)) for ix in combinations(range(4),3))
def dot(v,w):
    t=Z
    for x,y in zip(v,w):t=add(t,mul(x,y))
    return t

def reflection_basis(kind):
    if kind=='F4':
        return [tuple(q(x) for x in row) for row in ((0,2,-2,0),(0,0,2,-2),(0,0,0,2),(1,-1,-1,-1))]
    # Fixed exact basis, no numerical sign or root selection.
    return [(Z,Z,Z,ONE),(Z,q(1),(F(0),F(-1)),(F(-1),F(-1))),
            (Z,Z,ONE,Z),(q(1),(F(-1),F(-1)),(F(0),F(-1)),Z)]

def verify_reflection_model(kind,r):
    basis=reflection_basis(kind);rr=set(r);seen={norm(v) for v in basis};todo=list(seen)
    while todo:
        v=todo.pop()
        for s in basis:
            c=div(mul(q(2),dot(v,s)),dot(s,s));w=norm(tuple(sub(x,mul(c,y)) for x,y in zip(v,s)))
            assert w in rr
            if w not in seen:seen.add(w);todo.append(w)
    assert seen==rr
    target=[(F(1,4),F(0)),(F(1,2),F(0)),(F(1,4),F(0))] if kind=='F4' else [(F(1,4),F(1,4)),(F(1,4),F(0)),(F(1,4),F(0))]
    for i,j in combinations(range(4),2):
        x=dot(basis[i],basis[j])
        if j-i>1:assert x==Z
        else:assert div(mul(x,x),mul(dot(basis[i],basis[i]),dot(basis[j],basis[j])))==target[i]
    return {'simple_roots':[encode(v) for v in basis], 'gram':[[list(map(str,dot(v,w))) for w in basis] for v in basis],
            'orbit_size':len(seen),'all_roots_reached':True,'adjacent_cosine_squares':[list(map(str,v)) for v in target]}

def census(kind, rank3=False):
    r=roots(kind); planes={}; pairkey={}
    for i,j in combinations(range(len(r)),2):
        k=norm(wedge2(r[i],r[j]));planes.setdefault(k,set()).update((i,j));pairkey[i,j]=k
    flats=[{'members':sorted(v),'wedge':encode(k)} for k,v in sorted(planes.items())]
    report={'type':kind,'reflection_model':verify_reflection_model(kind,r),'hyperplanes':[encode(v) for v in r], 'rank2_flats':flats,
            'rank2_multiplicity_counts':dict(sorted(Counter(len(v) for v in planes.values()).items())),
            'hyperplane_rank2_profiles':dict(Counter(str(sorted(Counter(len(v) for v in planes.values() if i in v).items())) for i in range(len(r))))}
    if rank3:
        spaces={}
        for i,j,k in combinations(range(len(r)),3):
            v=wedge3(r[i],r[j],r[k])
            if all(x==Z for x in v):continue
            spaces.setdefault(norm(v),set()).update((i,j,k))
        report['rank3_flats']=[]
        profiles=Counter()
        for key,members in sorted(spaces.items()):
            local=Counter(len(v) for v in planes.values() if v<=members)
            profile=(len(members),tuple(sorted(local.items())))
            profiles[str(profile)]+=1
            report['rank3_flats'].append({'members':sorted(members),'wedge':encode(key),'rank2_profile':dict(sorted(local.items()))})
        report['rank3_profiles']=dict(profiles)
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--rank3',action='store_true');args=p.parse_args()
    start=time.monotonic();data=[census(t,args.rank3) for t in ('F4','H4')]
    Path(args.output).write_text(json.dumps({'field':'Q(phi), phi^2=phi+1','types':data,'elapsed_seconds':time.monotonic()-start},indent=2)+'\n')
    for r in data:print(r['type'],len(r['hyperplanes']),r['rank2_multiplicity_counts'],r.get('rank3_profiles',{}))
