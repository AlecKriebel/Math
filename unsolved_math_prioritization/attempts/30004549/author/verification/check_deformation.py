#!/usr/bin/env python3
"""Finite symbolic checks only, not a global geometric proof or independent audit."""
import json
from itertools import combinations
import sympy as s
u,v,x,t=s.symbols('u v x t', real=True)
coords=(u,v,x,t)
R=s.Function('R')(*coords)
epsilon=s.symbols('epsilon',real=True,nonzero=True)

def simp(p):
    return {I:s.simplify(a) for I,a in p.items() if s.simplify(a)!=0}
def add(*forms):
    out={}
    for P in forms:
        for I,a in P.items():out[I]=out.get(I,0)+a
    return simp(out)
def scale(c,P):return simp({I:c*a for I,a in P.items()})
def wedge(P,Q):
    out={}
    for I,a in P.items():
        for K,b in Q.items():
            if len(set(I+K))<len(I+K):continue
            sign=(-1)**sum(i>k for i in I for k in K)
            S=tuple(sorted(I+K));out[S]=out.get(S,0)+sign*a*b
    return simp(out)
def d(P):
    out={}
    for I,a in P.items():
        for j,z in enumerate(coords):out=add(out,wedge({(j,):s.diff(a,z)},{I:1}))
    return simp(out)
def same(name,P,Q):
    diff=add(P,scale(-1,Q))
    if diff:raise RuntimeError(f'{name}: {diff}')
    checks.append(name)
checks=[]
e=[{(i,):1} for i in range(4)]
vol={(0,1,2,3):1}
alpha={(0,2):1,(1,3):-1}
beta={(0,3):1,(1,2):1}
gamma=add(scale(u,alpha),scale(-v,beta))
delta=d(scale(R,e[1]))
B=add(beta,delta)
G=add(gamma,scale(-1,d(scale(R*v,e[1]))))
same('d alpha = 0',d(alpha),{})
same('d beta_epsilon = 0',d(B),{})
same('d gamma_epsilon = 0',d(G),{})
same('simultaneous third-form relation',G,add(scale(u,alpha),scale(-v,B)))
same('alpha square',wedge(alpha,alpha),scale(2,vol))
same('beta_epsilon square',wedge(B,B),scale(2*(1-s.diff(R,x)),vol))
same('mixed wedge',wedge(alpha,B),scale(s.diff(R,t),vol))
# Work in a formal positive-D field using an independent q with q^2=D.
D=1-s.diff(R,x)-s.diff(R,t)**2/4
numerator=add(B,scale(-s.diff(R,t)/2,alpha))
same('orthogonalization',wedge(alpha,numerator),{})
same('normalized square numerator',wedge(numerator,numerator),scale(2*D,vol))
k=1-epsilon*x
phi1=add(e[0],scale(s.I*s.sqrt(k),e[1]))
phi2=add(e[2],scale(s.I/s.sqrt(k),e[3]))
coreB=add({(0,3):1},scale(k,{(1,2):1}))
Psi=add(alpha,scale(s.I/s.sqrt(k),coreB))
same('core factorization',wedge(phi1,phi2),Psi)
same('Frobenius obstruction',wedge(d(phi1),Psi),scale(-epsilon/(2*k),vol))
# Coordinate Nijenhuis tensor: J columns are images of coordinate vectors.
J=s.Matrix([[0,-s.sqrt(k),0,0],[1/s.sqrt(k),0,0,0],[0,0,0,-1/s.sqrt(k)],[0,0,s.sqrt(k),0]])
def bracket(A,B):return s.Matrix([sum(A[j]*s.diff(B[i],coords[j])-B[j]*s.diff(A[i],coords[j]) for j in range(4)) for i in range(4)])
U=s.eye(4)[:,0];X=s.eye(4)[:,2]
N=bracket(J*U,J*X)-J*bracket(J*U,X)-J*bracket(U,J*X)-bracket(U,X)
expected=(-epsilon/(2*k))*U
if any(s.simplify(a)!=0 for a in N-expected):raise RuntimeError(f'Nijenhuis mismatch: {N}')
checks.append('coordinate Nijenhuis obstruction')
# A genuinely failed sign mutation must be rejected, even under python -O.
try:same('intentional wrong mixed-wedge sign',wedge(alpha,B),scale(-s.diff(R,t),vol))
except RuntimeError:checks.append('adversarial sign mutation rejected')
else:raise RuntimeError('incorrect sign mutation was accepted')
print(json.dumps({'result':'pass','sympy_version':s.__version__,'checks':checks,'limits':'Only symbolic local identities; does not certify global existence, smooth patching, cohomological independence, literature status or novelty.'},indent=2))
