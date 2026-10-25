#!/usr/bin/env python3
"""Exact constructive simulator for the rank-zero singular stratum.

Input data are rational Gram entries:
  a[i] = p(A_binary=0, B_ternary=i)
  b[i] = p(A_binary=1, B_ternary=i)
  c[i][j] = p(A_ternary=i, B_ternary=j), c symmetric, c[i][i]=0.

The function returns deterministic local components.  Fractions are used throughout.
"""
from __future__ import annotations
from fractions import Fraction
from typing import Iterable

F = Fraction


def _max(xs):
    return max(xs)


def _min(xs):
    return min(xs)


def simulate_rank_zero(a: Iterable[Fraction], b: Iterable[Fraction], c):
    a = list(map(F, a)); b = list(map(F, b))
    c = [[F(x) for x in row] for row in c]
    assert len(a) == len(b) == 3 and len(c) == 3 and all(len(row) == 3 for row in c)
    assert sum(a) == sum(b) == F(1,2)
    for i in range(3):
        assert c[i][i] == 0
        assert sum(c[i][j] for j in range(3)) == a[i] + b[i]
        for j in range(3):
            assert c[i][j] == c[j][i] and c[i][j] >= 0

    d1 = (b[0]-a[0])/2
    d2 = (b[1]-a[1])/2
    intervals = [
        (-c[0][1]/2, c[0][1]/2),
        (d1-c[0][2]/2, d1+c[0][2]/2),
        (-d2-c[1][2]/2, -d2+c[1][2]/2),
    ]
    lo = _max(L for L,R in intervals)
    hi = _min(R for L,R in intervals)
    assert lo <= hi
    t = lo

    f12=t; f13=d1-t; f23=d2+t
    q = [[F(0) for _ in range(3)] for _ in range(3)]
    q[0][1]=c[0][1]/2+f12; q[1][0]=c[0][1]/2-f12
    q[0][2]=c[0][2]/2+f13; q[2][0]=c[0][2]/2-f13
    q[1][2]=c[1][2]/2+f23; q[2][1]=c[1][2]/2-f23

    for i in range(3):
        assert sum(q[i]) == b[i]
        assert sum(q[j][i] for j in range(3)) == a[i]
        for j in range(3):
            assert 0 <= q[i][j] <= c[i][j]

    # Deterministic assignments are (A0,A1,B0,B1), with A0/B0 binary in {0,1}
    # and A1/B1 ternary in {0,1,2}.
    components=[]
    for i in range(3):
        for j in range(3):
            if i == j: continue
            if q[i][j] > 0:
                components.append({"weight": q[i][j], "outputs": (0,i,1,j)})
            rem=c[i][j]-q[i][j]
            if rem > 0:
                components.append({"weight": rem, "outputs": (1,i,0,j)})
    assert sum(z["weight"] for z in components) == 1
    return components


def verify_components(a,b,c,components):
    # Four setting blocks in dense declared architecture.
    p0000=[[F(0) for _ in range(2)] for _ in range(2)]
    p011=[[F(0) for _ in range(3)] for _ in range(2)]
    p110=[[F(0) for _ in range(2)] for _ in range(3)]
    p1111=[[F(0) for _ in range(3)] for _ in range(3)]
    for z in components:
        w=F(z["weight"]); A0,A1,B0,B1=z["outputs"]
        p0000[A0][B0]+=w
        p011[A0][B1]+=w
        p110[A1][B0]+=w
        p1111[A1][B1]+=w
    assert p0000 == [[0,F(1,2)],[F(1,2),0]]
    assert p011 == [list(map(F,a)),list(map(F,b))]
    assert p110 == [[F(a[i]),F(b[i])] for i in range(3)]
    assert p1111 == [[F(x) for x in row] for row in c]
    return True


if __name__ == "__main__":
    # Exact symmetric trine rank-zero example.
    a=[F(1,6)]*3; b=[F(1,6)]*3
    c=[[F(0),F(1,6),F(1,6)],
       [F(1,6),F(0),F(1,6)],
       [F(1,6),F(1,6),F(0)]]
    comps=simulate_rank_zero(a,b,c)
    verify_components(a,b,c,comps)
    print("Exact rank-zero simulator passed on the symmetric trine instance.")
    for z in comps:
        print(z)
