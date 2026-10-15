#!/usr/bin/env python3
"""Exact root boundary/Koszul checks; no author or peer checker imports."""
from fractions import Fraction as F
import json

def require(ok,message):
    if not ok: raise ValueError(message)

def mat(rows):return [[F(x) for x in row] for row in rows]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def tr(a):return [list(x) for x in zip(*a)]
def mul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def n2(a):return sum((x*x for row in a for x in row),F(0))
def scale(a,s):return [[s*x for x in row] for row in a]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sym(a):return scale(add(a,tr(a)),F(1,2))
def comm(a,b):return sub(mul(a,b),mul(b,a))
def au(u):return mat([[0,-1,0,0],[1,0,0,0],[0,0,0,u],[0,0,0,0]])
def ricci(a):
    n=len(a)+1
    c=[[[F(0) for h in range(n)] for j in range(n)] for i in range(n)]
    for i in range(n-1):
        for j in range(n-1):c[0][j+1][i+1]=a[i][j];c[j+1][0][i+1]=-a[i][j]
    g=[[[F(1,2)*(c[i][j][h]-c[j][h][i]+c[h][i][j]) for h in range(n)] for j in range(n)] for i in range(n)]
    return [[sum((g[j][h][l]*g[i][l][i]-g[i][h][l]*g[j][l][i]-c[i][j][l]*g[l][h][i] for i in range(n) for l in range(n)),F(0)) for h in range(n)] for j in range(n)]
def functional(a):
    r=ricci(a);den=n2(r);require(den>0,'nonflat condition');return sum((r[i][i] for i in range(len(r))),F(0))**2/den
checks=[]
for u in (F(1,8),F(1,4),F(3,8)):
    a=au(u);r=ricci(a);diag=[-u*u/2,0,0,u*u/2,-u*u/2]
    require(r==[[F(diag[i]) if i==j else F(0) for j in range(5)] for i in range(5)],'direct Ricci candidate')
    require(functional(a)==F(1,3),'candidate ratio')
    require(diag[3]+u*u/2-(diag[0]+u*u/2)-(diag[4]+u*u/2)==u*u,'derivation residual')
    checks.append({'u':str(u),'F':str(functional(a)),'derivation_failure':str(u*u)})
b=mat([[0,-1,0,0],[1,0,0,0],[1,0,0,1],[0,-1,0,0]])
require(functional(b)==F(9,17),'nonglobal direct Koszul comparison')
boundaries=[]
for u in (F(1,4),F(1,2),F(3,4)):
    for epsilon in (F(1,100),F(1,10)):
        t=eye(4);ti=eye(4);t[2][1]=-2*u*epsilon;t[3][0]=-epsilon;ti[2][1]=2*u*epsilon;ti[3][0]=epsilon
        require(mul(t,ti)==eye(4),'explicit exact inverse')
        m=mul(mul(t,au(u)),ti);expected=au(u);expected[2][0]=-u*epsilon;expected[3][1]=epsilon
        require(m==expected,'entire metric path stays same similarity orbit')
        p=n2(comm(m,tr(m)))-8*n2(sym(m))**2
        require(p==2*(1-4*u*u)*epsilon*epsilon-4*u*u*epsilon**4,'exact boundary polynomial')
        f=functional(m)
        require((p>=0)==(f<=F(1,3)),'curvature inequality equivalence')
        require(p>0 if u<F(1,2) else p<0,'open-interval versus boundary ascent')
        boundaries.append({'u':str(u),'epsilon':str(epsilon),'P':str(p),'F':str(f),'same_group':True})
print(json.dumps({'result':'PASS','arithmetic':'Python standard-library exact Fraction','author_and_peer_checker_imports':False,'candidate_checks':checks,'same_group_comparison_F':str(functional(b)),'boundary_paths':boundaries,'scope':'Finite exact falsifiers supplement the written local normal-form proof; they do not replace its all-metrics uniform-neighborhood argument.'},indent=2))
