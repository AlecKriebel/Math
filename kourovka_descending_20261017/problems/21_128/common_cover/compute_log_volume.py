#!/usr/bin/env python3
"""Exact rank-four reflection-flat enumeration and candidate log intersection.

All arithmetic is in Q(phi), phi**2=phi+1, using Fraction pairs.  No numeric
comparison is used in rank, equality, flat, or incidence decisions.
The output is a checkable computation, not a group commensurability invariant.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from collections import Counter
from pathlib import Path
import json, time

Z = (F(0), F(0))
O = (F(1), F(0))
PH = (F(0), F(1))
PI = (F(-1), F(1))

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[0],-x[1])
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    a,b=x; c,d=y
    return (a*c+b*d,a*d+b*c+b*d)
def inv(x):
    a,b=x; n=a*a+a*b-b*b
    if not n: raise ZeroDivisionError(x)
    return ((a+b)/n,-b/n)
def div(x,y): return mul(x,inv(y))
def dot(x,y):
    r=Z
    for a,b in zip(x,y): r=add(r,mul(a,b))
    return r
def canon(v):
    lead=next((x for x in v if x!=Z),None)
    return tuple(div(x,lead) for x in v) if lead is not None else None
def signed(x,s): return x if s==1 else neg(x)
def det3(m):
    return add(sub(mul(m[0][0],sub(mul(m[1][1],m[2][2]),mul(m[1][2],m[2][1]))),
                   mul(m[0][1],sub(mul(m[1][0],m[2][2]),mul(m[1][2],m[2][0])))),
               mul(m[0][2],sub(mul(m[1][0],m[2][1]),mul(m[1][1],m[2][0]))))
def normal3(a,b,c):
    return canon(tuple(signed(det3([[v[j] for j in range(4) if j!=i] for v in (a,b,c)]),(-1)**i)
                       for i in range(4)))
def wedge2(a,b):
    return canon(tuple(sub(mul(a[i],b[j]),mul(a[j],b[i])) for i,j in combinations(range(4),2)))
def parity(p): return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
def roots(typ):
    out=set()
    for i in range(4):
        out.add(canon(tuple(O if j==i else Z for j in range(4))))
    if typ in {'F4','H4'}:
        for signs in product((-1,1),repeat=4):
            out.add(canon(tuple(signed(O,s) for s in signs)))
    if typ in {'F4','B4','A4'}:
        for i,j in combinations(range(4),2):
            for sign in ((-1,) if typ=='A4' else (-1,1)):
                out.add(canon(tuple(O if k==i else signed(O,sign) if k==j else Z for k in range(4))))
    elif typ=='H4':
        for p in permutations(range(4)):
            if parity(p): continue
            for signs in product((-1,1),repeat=3):
                base=(Z,signed(O,signs[0]),signed(PH,signs[1]),signed(PI,signs[2]))
                out.add(canon(tuple(base[p[i]] for i in range(4))))
    else: raise ValueError(typ)
    return sorted(out)

def reflect(w,v):
    c=div(mul((F(2),F(0)),dot(w,v)),dot(v,v))
    return canon(tuple(sub(a,mul(c,b)) for a,b in zip(w,v)))

def verify_root_system(rs,typ):
    if typ=='A4':
        # Coordinates fix the fifth configuration point at zero. This is a
        # linear arrangement model, not an orthonormal A4 root realization.
        return {'coordinate_model':'x_i=0 and x_i=x_j; fifth configuration point fixed at zero',
                'euclidean_reflection_check':'not applicable in these coordinates'}
    universe=set(rs)
    for v in rs:
        assert all(reflect(w,v) in universe for w in rs)
    targets={'F4':((F(1,4),F(0)),(F(1,2),F(0)),(F(1,4),F(0))),
             'H4':((F(1,4),F(1,4)),(F(1,4),F(0)),(F(1,4),F(0)))}
    if typ not in targets: return {'all_reflections_preserve_normal_set':True}
    sq={}
    for i,j in combinations(range(len(rs)),2):
        d=dot(rs[i],rs[j]); sq[i,j]=div(mul(d,d),mul(dot(rs[i],rs[i]),dot(rs[j],rs[j])))
    def angle(i,j): return sq[min(i,j),max(i,j)]
    simple=None
    for i,j in permutations(range(len(rs)),2):
        if angle(i,j)!=targets[typ][0]:continue
        for k in range(len(rs)):
            if k in (i,j) or angle(j,k)!=targets[typ][1] or angle(i,k)!=Z:continue
            for l in range(len(rs)):
                if l in (i,j,k):continue
                if angle(k,l)!=targets[typ][2] or angle(i,l)!=Z or angle(j,l)!=Z:continue
                if dot(normal3(rs[i],rs[j],rs[k]),rs[l])==Z:continue
                simple=(i,j,k,l);break
            if simple:break
        if simple:break
    assert simple
    orbit={rs[i] for i in simple}; pending=list(orbit)
    while pending:
        w=pending.pop()
        for i in simple:
            x=reflect(w,rs[i])
            if x not in orbit: orbit.add(x);pending.append(x)
    assert orbit==universe
    return {'all_reflections_preserve_normal_set':True,'simple_chain_indices':simple,
            'simple_chain_labels':{'F4':[3,4,3],'H4':[5,3,3]}[typ],
            'simple_reflection_orbit_count':len(orbit)}

def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,(tuple,list)): return [encode(t) for t in x]
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    return x

def compute(typ):
    started=time.time(); rs=roots(typ); n=len(rs)
    assert n=={'F4':24,'H4':60,'A4':10,'B4':16}[typ]
    root_checks=verify_root_system(rs,typ)
    # Each vector is the normal of one complexified reflecting hyperplane.
    # A rank-two flat is represented by the two-dimensional normal span;
    # a projective point is represented by its one-dimensional annihilator.
    lines={}
    for i,j in combinations(range(n),2):
        key=wedge2(rs[i],rs[j]); assert key is not None
        lines.setdefault(key,set()).update((i,j))
    points={}
    for i,j,k in combinations(range(n),3):
        key=normal3(rs[i],rs[j],rs[k])
        if key is not None: points.setdefault(key,set()).update((i,j,k))
    # Completion by exact incidences independently checks the union-of-bases
    # enumeration.  Rank-two closure is equivalently equality of wedge spans.
    line_sets=[]
    for key,ix in lines.items():
        i=min(ix)
        full={j for j in range(n) if j==i or wedge2(rs[i],rs[j])==key}
        assert full==ix
        line_sets.append(tuple(sorted(full)))
    point_sets=[]
    for key,ix in points.items():
        full={j for j in range(n) if dot(key,rs[j])==Z}
        assert full==ix
        point_sets.append(tuple(sorted(full)))
    line_sets.sort(); point_sets.sort()
    mu_lines=[len(l)-1 for l in line_sets]
    mu_points=[-1+len(p)-sum(len(l)-1 for l in line_sets if set(l)<=set(p)) for p in point_sets]
    euler=4-3*n+2*sum(mu_lines)+sum(mu_points)
    # Blow up every intersection point, then every strict-transform line.
    # Distinct line centers are disjoint after all intersection points blew up.
    volume=(n-4)**3
    point_correction=sum((3-len(p))**3 for p in point_sets)
    volume+=point_correction
    line_details=[]
    for l in line_sets:
        containing=[p for p in point_sets if set(l)<=set(p)]
        # Degree on the transformed line of D=K+reduced boundary.
        dl=(n-4)+sum(3-len(p) for p in containing)
        normal=2-2*len(containing)
        a=2-len(l)
        correction=-3*a*a*dl-a*a*a*normal
        volume+=correction
        line_details.append({'hyperplanes':l,'multiplicity':len(l),
            'point_count':len(containing),'D_dot_line':dl,'normal_degree':normal,
            'cube_correction':correction})
    out={'type':typ,'hyperplane_count':n,'roots_Qphi':encode(rs),
         'root_system_checks':root_checks,
         'projective_points':point_sets,'projective_lines':line_details,
         'point_multiplicity_histogram':dict(sorted(Counter(map(len,point_sets)).items())),
         'line_multiplicity_histogram':dict(sorted(Counter(map(len,line_sets)).items())),
         'initial_cube':(n-4)**3,'point_cube_correction':point_correction,
         'final_log_divisor_cube':volume,'projective_complement_euler':euler,
         'volume_over_abs_euler':str(F(volume,abs(euler))),
         'elapsed_seconds':time.time()-started}
    return out

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--type',choices=['F4','H4','A4','B4','both','tests'],default='both')
    ap.add_argument('--output',default='log_volume_data.json'); args=ap.parse_args()
    types=['F4','H4'] if args.type=='both' else ['A4','B4'] if args.type=='tests' else [args.type]
    result={t:compute(t) for t in types}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({t:{k:v for k,v in d.items() if k not in {'roots_Qphi','projective_points','projective_lines'}}
                      for t,d in result.items()},indent=2))
