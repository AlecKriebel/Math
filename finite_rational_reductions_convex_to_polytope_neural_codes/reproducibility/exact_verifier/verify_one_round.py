#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from itertools import product, combinations
import json

ROOT = Path(__file__).resolve().parents[1]

def cross(o,a,b):
    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])

def hull(points):
    pts=sorted(set(points))
    if len(pts)<=1: return pts
    lo=[]
    for p in pts:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    up=[]
    for p in reversed(pts):
        while len(up)>=2 and cross(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]

def inside_closed(poly,p):
    return all(cross(a,b,p)>=0 for a,b in zip(poly,poly[1:]+poly[:1]))

def inside_open(poly,p):
    return all(cross(a,b,p)>0 for a,b in zip(poly,poly[1:]+poly[:1]))

def line_intersection(p1,p2,q1,q2):
    rx,ry=p2[0]-p1[0],p2[1]-p1[1]
    sx,sy=q2[0]-q1[0],q2[1]-q1[1]
    den=rx*sy-ry*sx
    if den==0: return None
    qpx,qpy=q1[0]-p1[0],q1[1]-p1[1]
    t=(qpx*sy-qpy*sx)/den
    return (p1[0]+t*rx,p1[1]+t*ry)

def clip(subject, clip_poly):
    out=subject[:]
    for a,b in zip(clip_poly,clip_poly[1:]+clip_poly[:1]):
        inp=out; out=[]
        if not inp: break
        prev=inp[-1]; prev_in=cross(a,b,prev)>=0
        for cur in inp:
            cur_in=cross(a,b,cur)>=0
            if cur_in:
                if not prev_in:
                    z=line_intersection(prev,cur,a,b); assert z is not None; out.append(z)
                out.append(cur)
            elif prev_in:
                z=line_intersection(prev,cur,a,b); assert z is not None; out.append(z)
            prev,prev_in=cur,cur_in
    return hull(out) if out else []

def parse_point(p): return tuple(F(x) for x in p)

def bary(points,weights):
    assert sum(weights,F(0))==1
    return tuple(sum(w*p[k] for w,p in zip(weights,points)) for k in range(2))

def facet_ineqs(poly):
    # CCW polygon interior: A*x+B*y <= C; strict for interior.
    out=[]
    for (x1,y1),(x2,y2) in zip(poly,poly[1:]+poly[:1]):
        dx=x2-x1; dy=y2-y1
        out.append((dy,-dx,dy*x1-dx*y1))
    return out

def solve3(rows, rhs):
    A=[list(r)+[b] for r,b in zip(rows,rhs)]
    n=3
    for col in range(n):
        piv=next((r for r in range(col,n) if A[r][col]),None)
        if piv is None: return None
        A[col],A[piv]=A[piv],A[col]
        q=A[col][col]
        A[col]=[z/q for z in A[col]]
        for r in range(n):
            if r==col: continue
            q=A[r][col]
            if q:
                A[r]=[A[r][c]-q*A[col][c] for c in range(n+1)]
    return tuple(A[i][n] for i in range(n))

def branch_feasible(constraints):
    # constraints (a,b,c,strict) mean a*x+b*y <= c, strict if flagged.
    # Maximize eps with strict rows relaxed to a*x+b*y+eps<=c.
    rows=[]; rhs=[]
    for a,b,c,s in constraints:
        rows.append((a,b,F(1) if s else F(0))); rhs.append(c)
    rows += [(F(0),F(0),F(-1)),(F(0),F(0),F(1))]
    rhs += [F(0),F(1)]
    best=None; bestpt=None
    for ids in combinations(range(len(rows)),3):
        sol=solve3([rows[i] for i in ids],[rhs[i] for i in ids])
        if sol is None: continue
        if all(sum(r[k]*sol[k] for k in range(3))<=b for r,b in zip(rows,rhs)):
            if best is None or sol[2]>best:
                best=sol[2]; bestpt=sol
    return (best is not None and best>0), bestpt

def exact_code(Q, polys):
    qcons=[(*z,True) for z in facet_ineqs(Q)]
    fcons={i:facet_ineqs(P) for i,P in polys.items()}
    out=set()
    witness={}
    n=max(polys)
    for mask in range(1<<n):
        active={i+1 for i in range(n) if mask>>i&1}
        inactive=[j for j in range(1,n+1) if j not in active]
        branches=product(*[range(len(fcons[j])) for j in inactive])
        for choices in branches:
            cons=list(qcons)
            for i in active:
                cons += [(*z,True) for z in fcons[i]]
            for j,f in zip(inactive,choices):
                a,b,c=fcons[j][f]
                cons.append((-a,-b,-c,False))
            ok,pt=branch_feasible(cons)
            if ok:
                word=''.join(str(i) for i in sorted(active))
                out.add(word); witness[word]=(pt[0],pt[1]); break
    return out,witness

j=json.loads((ROOT/'one_round/counterexamples/three_neuron_counterexample.json').read_text())
S1=list(map(parse_point,j['protected_simplices']['1']))
S2=list(map(parse_point,j['protected_simplices']['2']))
S3=list(map(parse_point,j['protected_simplices']['123']))
R=list(map(parse_point,j['atlas_patch']))
W=list(map(parse_point,j['second_patch']))
Q=[(F(-4),F(-4)),(F(4),F(-4)),(F(4),F(4)),(F(-4),F(4))]
P10=hull(S1+S3); P20=hull(S2+S3); P30=hull(S3)
K0=clip(P10,P20)
assert K0==hull([(F(-1,10),F(-1,10)),(F(1,10),F(-1,10)),(F(0),F(1,5))])
assert all(inside_open(R,v) for v in K0)
assert inside_open(P10,(F(-1),F(3))) and not inside_closed(P20,(F(-1),F(3)))
assert inside_open(P20,(F(1),F(3))) and not inside_closed(P10,(F(1),F(3)))
assert inside_open(P10,(F(0),F(0))) and inside_open(P20,(F(0),F(0))) and inside_open(P30,(F(0),F(0)))
assert inside_open(P10,(F(0),F(3,20))) and inside_open(P20,(F(0),F(3,20))) and not inside_closed(P30,(F(0),F(3,20)))
D0,w0=exact_code(Q,{1:P10,2:P20,3:P30})
assert D0=={'','1','2','12','123'},D0
P11=hull(P10+R); P21=hull(P20+R); P31=hull(P30+R)
K1=clip(P11,P21)
expected_K1=hull([(F(-1,2),F(-1,5)),(F(1,2),F(-1,5)),(F(1,2),F(1,2)),(F(0),F(41,30)),(F(-1,2),F(1,2))])
assert K1==expected_K1
x=(F(0),F(1))
assert inside_open(P11,x) and inside_open(P21,x) and not inside_closed(P31,x)
D1,w1code=exact_code(Q,{1:P11,2:P21,3:P31})
assert D1=={'','1','2','12','123'},D1
L=(F(-1),F(31,10)); u=(F(-1,2),F(1,2)); v=(F(1,2),F(1,2)); Rap=(F(1),F(31,10))
w1=[F(5,26),F(11,52),F(31,52)]
w2=[F(5,26),F(31,52),F(11,52)]
assert bary([L,u,v],w1)==x
assert bary([Rap,u,v],w2)==x
P12=hull(P11+W); P22=hull(P21+W); P32=hull(P31+W)
K2=clip(P12,P22)
assert K2==hull(W)==P32
D2,w2code=exact_code(Q,{1:P12,2:P22,3:P32})
assert D2=={'','1','2','123'},D2
for p,word in [((F(-1),F(3)),'1'),((F(1),F(3)),'2'),((F(0),F(0)),'123'),((F(0),F(-1,2)),'')]:
    got=''.join(str(i) for i,P in [(1,P12),(2,P22),(3,P32)] if inside_open(P,p))
    assert got==word,(p,got,word)
# Source containment, including every repair hull.
assert max(x for x,y in P12)<F(3,4) and min(y for x,y in P12)>-1
assert min(x for x,y in P22)>F(-3,4) and min(y for x,y in P22)>-1
assert max(x for x,y in P32)<F(3,4) and min(x for x,y in P32)>F(-3,4) and min(y for x,y in P32)>-1
print('PHASE-XIX ONE-ROUND COUNTEREXAMPLE PASS')
print('SOURCE CODE: empty,1,2,123')
print('INITIAL SUPERCODE: empty,1,2,12,123')
print('ONE-ROUND CODE: empty,1,2,12,123')
print('ONE-ROUND FORBIDDEN WITNESS: (0,1) HAS WORD 12')
print('COLORED CIRCUIT: 4 VERTICES, LABELS 1,2,123')
print('SECOND SYNCHRONIZED CORE SPLIT: EXACT TARGET CODE')
