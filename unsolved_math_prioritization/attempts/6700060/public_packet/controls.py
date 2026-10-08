#!/usr/bin/env python3
"""Exact convention controls; they are not analytic theorem certificates."""
from fractions import Fraction as F
import json

count = 0

def require(x):
    global count
    count += 1
    if not x:
        raise AssertionError('exact control failed')

def tr(a): return list(map(list, zip(*a)))
def mm(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def inv(a):
    n=len(a); b=[list(map(F,r))+s for r,s in zip(a,eye(n))]
    for j in range(n):
        k=next(i for i in range(j,n) if b[i][j]); b[j],b[k]=b[k],b[j]
        x=b[j][j]; b[j]=[v/x for v in b[j]]
        for i in range(n):
            if i != j:
                x=b[i][j]; b[i]=[v-x*w for v,w in zip(b[i],b[j])]
    return [r[n:] for r in b]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def mv(a,v): return [dot(r,v) for r in a]

# Covector normals under g=A^T A. No approximate square roots are used.
for n in range(2,7):
    for seed in range(1,8):
        a=[[F((i+j+seed)%5-2) if j>i else F(seed+i+1) if i==j else F(0)
            for j in range(n)] for i in range(n)]
        ai=inv(a); g=mm(tr(a),a); gi=inv(g)
        require(mm(g,gi)==eye(n))
        normals=eye(n)+[[F((i+seed)%3-1) for i in range(n)]]
        for u in normals:
            if not any(u): continue
            gu=mv(gi,u); pushed=mv(a,gu); expected=mv(tr(ai),u)
            require(pushed==expected)
            require(dot(gu,mv(g,gu))==dot(pushed,pushed))
            for v in normals:
                if not any(v): continue
                gv=mv(gi,v)
                require(dot(gu,mv(g,gv))==dot(pushed,mv(a,gv)))
        # Metric product preserves old inverse-normal pairings and gives zero new pairings.
        gp=[r+[F(0)] for r in g]+[[F(0)]*n+[F(1)]]
        gip=inv(gp)
        require([r[:n] for r in gip[:n]]==gi)
        require(all(gip[i][n]==0 for i in range(n)))

# Planar turning budget in units of pi; strictly reducing any interior angle
# strictly increases total exterior turning past 2, incompatible with k>=0.
for m in range(3,51):
    angles=[F(m-2,m)]*m
    require(sum(1-x for x in angles)==2)
    for j in range(m):
        eps=angles[j]/(j+2)
        changed=angles[:];changed[j]-=eps
        require(sum(1-x for x in changed)==2+eps)
        require(-eps<0) # only negative integrated curvature could repair the budget

# Gaussian-rational 2x2 Clifford matrices, with exact arithmetic.
def z(a=0,b=0):return (F(a),F(b))
def za(a,b):return (a[0]+b[0],a[1]+b[1])
def zm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def zs(a,s):return (a[0]*s,a[1]*s)
def madd(a,b):return [[za(x,y) for x,y in zip(r,s)] for r,s in zip(a,b)]
def mul(a,b):
    return [[za(zm(a[i][0],b[0][j]),zm(a[i][1],b[1][j])) for j in range(2)] for i in range(2)]
def scale(a,s):return [[zs(x,s) for x in r] for r in a]
I=[[z(1),z()],[z(),z(1)]]
C=[[[z(),z(0,1)],[z(0,1),z()]],[[z(),z(1)],[z(-1),z()]],[[z(0,-1),z()],[z(),z(0,1)]]]
def cliff(v):
    ans=[[z(),z()],[z(),z()]]
    for t,c in zip(v,C): ans=madd(ans,scale(c,t))
    return ans
require(mul(mul(C[0],C[1]),C[2])==scale(I,-1))
vectors=[[F(a),F(b),F(c)] for a in range(-2,3) for b in range(-2,3) for c in [-1,0,1]]
for u in vectors:
    cu=cliff(u)
    require(mul(cu,cu)==scale(I,-dot(u,u)))
    for v in [[F(3,5),F(4,5),F(0)],[F(0),F(5,13),F(12,13)],[F(1),F(2),F(-3)]]:
        cv=cliff(v)
        require(madd(mul(cu,cv),mul(cv,cu))==scale(I,-2*dot(u,v)))

print(json.dumps({"assertions":count,"arithmetic":"standard-library rational and Gaussian-rational", "groups":["pullback normal and Gram identities", "product metric normals", "planar turning budget", "Clifford anticommutators and volume convention"],"scope":"finite convention checks only; no PDE or source theorem certification"},sort_keys=True,indent=2))
