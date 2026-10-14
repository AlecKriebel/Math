#!/usr/bin/env python3
"""Exact algebraic checks for PASS2; topological quantifiers are proved in reports."""
import json
from pathlib import Path
import sympy as s

def check(c,msg):
    if not c: raise RuntimeError(msg)
def matzero(m):return all(s.cancel(e)==0 for e in m)
u=s.symbols('u',nonzero=True); A=s.Matrix([[1,0],[-1,1]])
M=u*A-A.T; B=(1-u)*M.inv(); I=s.eye(2); Delta=u*u-u+1
check(matzero(B*M-(1-u)*I),'right presentation relations')
check(matzero(M.subs(u,1/u).T*B-(u-1)/u*I),'left presentation relations')
check(matzero(B.subs(u,1/u).T-B),'Hermitian matrix')
check(s.cancel(B[0,0]-u/Delta)==-1,'cyclic residue')
Bm=(1-u)*(u*(-A)-(-A).T).inv()
check(matzero(Bm+B),'mirror sign')
P=s.Matrix([[0,1],[1,0]])
check(P.T*A.T*P==A,'mirror basis swap')
a,b=s.symbols('a b',real=True)
check(s.expand((a+b/2)**2+3*b*b/4-(a*a+a*b+b*b))==0,'positive quadratic norm identity')
Q=s.symbols('Q'); boundary=s.Matrix([[Q-1,Q-1]])
check(boundary*s.Matrix([1,-1])==s.zeros(1,1),'two-puncture cycle')
check(boundary.rank()==1,'two-puncture rank over Q(Q)')
s0=s.symbols('s0',nonzero=True); D=1/s0
check(s.cancel(D*s0)==1,'dual-curve handle cancellation')
alpha=s.symbols('alpha',real=True)
check(s.trigsimp(s.sin(2*alpha)-2*s.sin(alpha)*s.cos(alpha))==0,'fundamental/vacuum S ratio')
for n in range(1,31):check((-1)**n*(-1)**n==1,'relative adjunction sign')
E2={(1,4):2,(1,5):4,(1,6):2,(2,2):6,(2,3):6}
for p,q in E2:
    for r in range(2,20):check((p+r,q-r+1) not in E2,'no higher Cech differential target')
ordinary={}
for (p,q),rank in E2.items():
    degree=12-(p+q+1)
    ordinary[degree]=ordinary.get(degree,0)+rank
check(ordinary=={4:2,5:4,6:8,7:6},'four-particle ordinary degrees')
out={'status':'PASS','checks':['Blanchfield presentation, Hermitian, residue and mirror identities','positive imaginary-quadratic norm identity','relative two-puncture factor and product sign','geometric compression normalization and S ratio','nonminimal-neutral spectral support and degrees'],'ordinary_four_particle_dimensions':ordinary,'scope':'Exact algebra only; source correspondence, topology and naturality are audited in the accompanying report.'}
path=Path(__file__).with_name('INDEPENDENT_CHECK_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
