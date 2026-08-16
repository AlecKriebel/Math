#!/usr/bin/env python3
"""Exact rational polygon utilities for finite neural-code calibrations."""
from fractions import Fraction as F
from itertools import combinations, product


def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])


def hull(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    lo=[]
    for p in pts:
        while len(lo)>=2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up=[]
    for p in reversed(pts):
        while len(up)>=2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def inside_open(poly,p):
    return all(cross(a,b,p)>0 for a,b in zip(poly, poly[1:]+poly[:1]))


def facet_ineqs(poly):
    # CCW polygon interior: A*x+B*y <= C; strict for open interior.
    out=[]
    for (x1,y1),(x2,y2) in zip(poly,poly[1:]+poly[:1]):
        dx=x2-x1; dy=y2-y1
        out.append((dy,-dx,dy*x1-dx*y1))
    return out


def solve3(rows,rhs):
    A=[list(r)+[b] for r,b in zip(rows,rhs)]
    n=3
    for col in range(n):
        piv=next((r for r in range(col,n) if A[r][col]),None)
        if piv is None:
            return None
        A[col],A[piv]=A[piv],A[col]
        q=A[col][col]
        A[col]=[z/q for z in A[col]]
        for r in range(n):
            if r==col:
                continue
            q=A[r][col]
            if q:
                A[r]=[A[r][c]-q*A[col][c] for c in range(n+1)]
    return tuple(A[i][n] for i in range(n))


def branch_feasible(constraints):
    # (a,b,c,strict) means a*x+b*y <= c, strict if flagged.
    # Introduce eps and maximize it subject to strict rows + eps <= c.
    rows=[]; rhs=[]
    for a,b,c,s in constraints:
        rows.append((a,b,F(1) if s else F(0))); rhs.append(c)
    rows += [(F(0),F(0),F(-1)),(F(0),F(0),F(1))]
    rhs += [F(0),F(1)]
    best=None; bestpt=None
    for ids in combinations(range(len(rows)),3):
        sol=solve3([rows[i] for i in ids],[rhs[i] for i in ids])
        if sol is None:
            continue
        if all(sum(r[k]*sol[k] for k in range(3))<=b for r,b in zip(rows,rhs)):
            if best is None or sol[2]>best:
                best=sol[2]; bestpt=sol
    return (best is not None and best>0), bestpt


def exact_code(Q, polys):
    qcons=[(*z,True) for z in facet_ineqs(Q)]
    fcons={i:facet_ineqs(P) for i,P in polys.items()}
    n=max(polys) if polys else 0
    out=set(); witnesses={}
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
                out.add(word); witnesses[word]=(pt[0],pt[1])
                break
    return out,witnesses
