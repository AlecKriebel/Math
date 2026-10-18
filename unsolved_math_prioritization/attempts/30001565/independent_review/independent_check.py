#!/usr/bin/env python3
"""Independent exact tests of the split-component and star correspondence.
This does not implement or benchmark the published lattice algorithm.
"""
import json
from itertools import permutations
import sympy as s
count=0
def ck(v):
 global count
 assert v
 count+=1
def eq(A,B):
 global count
 assert A.shape==B.shape
 for a,b in zip(A,B):
  assert s.simplify(s.expand_complex(a-b))==0,(a,b)
  count+=1
# Actual thin Schurian coherent algebra from the regular S3 action.
G=list(permutations(range(3)));ident=tuple(range(3));idx={g:i for i,g in enumerate(G)}
def comp(g,h):return tuple(g[h[i]] for i in range(3))
def inv(g):return tuple(g.index(i) for i in range(3))
def perm_matrix(g,left=False):
 M=s.zeros(6)
 for h in G:
  gh=comp(g,h) if left else comp(h,inv(g))
  M[idx[gh],idx[h]]=1
 return M
R={g:perm_matrix(g) for g in G};L={g:perm_matrix(g,True) for g in G}
eq(sum(R.values(),s.zeros(6)),s.ones(6))
for g in G:
 eq(R[g].T,R[inv(g)])
 for h in G:
  eq(R[g]*R[h],R[comp(g,h)])
  eq(L[g]*R[h],R[h]*L[g])
chi=lambda g:sum(g[i]==i for i in range(3))-1
e=sum((s.Rational(1,3)*chi(inv(g))*R[g] for g in G),s.zeros(6))
eq(e*e,e);eq(e.T,e);ck(e.rank()==4)
Bspan=s.Matrix.hstack(*[(e*R[g]).reshape(36,1) for g in G]);ck(Bspan.rank()==4)
swap=(1,0,2);x=e*(s.eye(6)+R[swap])/2
eq(x*x,x);ck(x.rank()==2)  # Physical rank2, reduced rank1.
cols=s.Matrix.hstack(*[(R[g]*x).reshape(36,1) for g in G]).columnspace();ck(len(cols)==2)
V=s.Matrix.hstack(*cols);basis=[c.reshape(6,6) for c in cols]
H=s.Matrix([[s.trace(a.T*b) for b in basis] for a in basis]);ck(H.det()>0);ck(H[0,0]>0)
rho={}
for g in G:
 rr=[]
 for a in basis:
  sol=V.gauss_jordan_solve((R[g]*a).reshape(36,1))[0];rr.append(sol)
 rho[g]=s.Matrix.hstack(*rr)
for g in G:
 eq(rho[g].T*H,H*rho[inv(g)])
 for h in G:eq(rho[g]*rho[h],rho[comp(g,h)])
C=H.cholesky().T;eq(C.T*C,H)
phi={g:s.simplify(C*rho[g]*C.inv()) for g in G}
for g in G:
 eq(phi[g].T,phi[inv(g)])
 for h in G:eq(phi[g]*phi[h],phi[comp(g,h)])
ck(s.Matrix.hstack(*[z.reshape(4,1) for z in phi.values()]).rank()==4)
# Independent standard S3 realization: invariant Gram space and square-class obstruction.
S=s.Matrix([[0,1],[1,0]]);T=s.Matrix([[-1,-1],[1,0]])
a,b,c=s.symbols('a b c',real=True);Q=s.Matrix([[a,b],[b,c]])
rels=list(S.T*Q*S-Q)+list(T.T*Q*T-Q)
coef=s.linear_eq_to_matrix(rels,[a,b,c])[0];ker=coef.nullspace();ck(len(ker)==1)
H0=s.Matrix([[2,1],[1,2]]);eq(S.T*H0*S,H0);eq(T.T*H0*T,H0);ck(H0.det()==3)
# Repeated physical multiplicities and arbitrary nonorthogonal complex bases.
for m in range(1,5):
 for repeat in range(1,4):
  B=s.eye(m)
  for i in range(m):
   for j in range(i+1,m):B[i,j]=i+j+1+s.I*(j-i)
  Gram=repeat*(B.conjugate().T*B)
  for i in range(m):
   for j in range(m):
    E=s.zeros(m);E[i,j]=1
    F=s.kronecker_product(s.eye(repeat),E)
    ck(F.rank()==repeat)
    rhoij=B.inv()*E*B
    Eadj=E.T;rhoadj=B.inv()*Eadj*B
    eq(rhoij.conjugate().T*Gram,Gram*rhoadj)
    C=s.sqrt(repeat)*B;eq(C.conjugate().T*C,Gram)
    eq(s.simplify(C*rhoij*C.inv()),E)
# Negative control: arbitrary eigenvectors from distinct eigenvalues need not form a module.
E11=s.Matrix([[1,0],[0,0]]);E22=s.Matrix([[0,0],[0,1]]);E12=s.Matrix([[0,1],[0,0]])
X=s.diag(1,2);eq(X*E11,E11);eq(X*E22,2*E22)
ck(s.Matrix.hstack(E11.reshape(4,1),E22.reshape(4,1),(E12*E22).reshape(4,1)).rank()==3)
print(json.dumps({'status':'PASS','exact_assertions':count,'actual_schurian_example':'regular S3 orbital algebra; standard block dimension4; minimal ideal dimension2; physical rank2','scope':'Exact representation, trace-Gram, multiplicity and normalization checks. No reimplementation, complexity benchmark or proof of lattice-algorithm termination by finite test.'},indent=2,sort_keys=True))
