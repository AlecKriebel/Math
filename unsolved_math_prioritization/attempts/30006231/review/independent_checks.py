#!/usr/bin/env python3
"""Independent exact checks, emphasizing complex kernels and source-state distinctions."""
from pathlib import Path
from hashlib import sha256
from itertools import combinations,product
import sympy as s
import json
n=0;groups={}
def ck(ok,g):
 global n
 assert bool(ok),g
 n+=1;groups[g]=groups.get(g,0)+1
def eq(A,B,g):
 for x in A-B:ck(s.simplify(x)==0,g)
def psd(A):
 return all(s.simplify(A.extract(I,I).det())>=0 for k in range(1,A.rows+1) for I in combinations(range(A.rows),k))
I=s.I
# Complex rank-one kernel compression, exact positive step and a violating
# coupling. Congruence moves the kernel away from coordinate axes.
S=s.Matrix([[1,I,1],[0,1,1-I],[0,0,1]])
vecs=[s.Matrix(v) for v in [(1,0),(0,1),(1,1),(1,I),(1,1+I),(2-I,1)]]
for v in vecs:
 w=s.Matrix([-s.conjugate(v[1]),s.conjugate(v[0])]);eq(v.conjugate().T*w,s.zeros(1),'orthogonal complex nullspace')
 for alpha,d,q in product((0,1,I,1+I),(-2,0,3),(1,2)):
  M=s.diag(0,0,q);C=v*v.conjugate().T
  D=C.row_join(s.conjugate(alpha)*v).col_join((alpha*v.conjugate().T).row_join(s.Matrix([[d]])))
  step=s.Rational(q,2)/(1+abs(d)+s.expand_complex(alpha*s.conjugate(alpha)))
  ck(psd(M+step*D),'complex radial sufficiency')
  ck(psd(S.conjugate().T*(M+step*D)*S),'noncoordinate kernel sufficiency')
  bad=C.row_join(s.conjugate(alpha)*v+w).col_join((alpha*v.conjugate().T+w.conjugate().T).row_join(s.Matrix([[d]])))
  W=w.col_join(s.zeros(1,1));e3=s.Matrix([0,0,1]);Z=W.row_join(e3)
  minor=s.simplify((Z.conjugate().T*(M+step*bad)*Z).det())
  ck(minor<0,'nullspace coupling necessity')
# Empty kernel and wholly zero slack are separate radial edge cases.
for d in range(-5,6):
 t=s.Rational(1,2*(1+abs(d)))
 ck(1+t*d>0,'empty kernel control')
 ck((t*d>=0)==(d>=0),'zero slack control')

# Reconstruct the 7D example from the six Pauli eigenvectors as a tight frame.
P=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-I],[I,0]]),s.diag(1,-1)]
rows=[s.Matrix([[1,1]])/s.sqrt(6),s.Matrix([[1,-1]])/s.sqrt(6),s.Matrix([[1,-I]])/s.sqrt(6),s.Matrix([[1,I]])/s.sqrt(6),s.Matrix([[1,0]])/s.sqrt(3),s.Matrix([[0,1]])/s.sqrt(3),s.zeros(1,2)]
V=s.Matrix.vstack(*rows);e=s.eye(7)[:,6];U=V.row_join(e)
B=[s.diag(*[1 if j==2*i else -1 if j==2*i+1 else 0 for j in range(7)]) for i in range(3)]
A=s.eye(7)-U*U.conjugate().T
eq(U.conjugate().T*U,s.eye(3),'frame isometry')
eq(A*A,A,'ground projector')
ck(A.rank()==4,'ground projector')
for i,b in enumerate(B):
 eq(V.conjugate().T*b*V,P[i]/3,'independent Pauli compression')
 eq(b*e,s.zeros(7,1),'critical expectation point')
 for c in B:eq(b*c,c*b,'commuting observables')
ck(s.Matrix.hstack(*[a.reshape(49,1) for a in [s.eye(7)]+B]).rank()==4,'affine independence')
rho0=e*e.T;rho1=V*V.conjugate().T/2
for t in (s.Rational(1,5),s.Rational(1,2),s.Rational(4,5)):
 rho=(1-t)*rho0+t*rho1
 ck(rho.rank()==3,'maximal ensemble support')
 ck(s.trace(rho)==1,'ensemble states')
 eq(A*rho,s.zeros(7),'ensemble states')
 for b in B:ck(s.simplify(s.trace(b*rho))==0,'ensemble states')
# Solve the Hermitian constraints on the 3D ground space symbolically.
a,b,c,d,e0,f,g,h,j=s.symbols('a b c d e f g h j',real=True)
X=s.Matrix([[a,d+I*e0,f+I*g],[d-I*e0,b,h+I*j],[f-I*g,h-I*j,c]])
constraints=[s.trace(X)]+[s.simplify(s.trace((U.conjugate().T*bi*U)*X)) for bi in B]
L=s.linear_eq_to_matrix(constraints,[a,b,c,d,e0,f,g,h,j])[0]
ck(L.rank()==4 and len(L.nullspace())==5,'ensemble support criterion')
x,y,z,w=s.symbols('x y z w',real=True);xi=s.Matrix([x+I*y,z+I*w])
bloch=[s.expand((xi.conjugate().T*p*xi)[0]) for p in P]
ck(s.expand(sum(t*t for t in bloch)-(x*x+y*y+z*z+w*w)**2)==0,'pure fiber identity')
l1,l2,l3,lam=s.symbols('l1 l2 l3 lam',real=True)
H=sum((v*p for v,p in zip([l1,l2,l3],P)),s.zeros(2))/3
ck(s.expand((lam*s.eye(2)-H).det()-lam**2+(l1*l1+l2*l2+l3*l3)/9)==0,'parameter spectrum')
# For the 2x2 examples, compute exact feasible pencils.
t=s.symbols('t',real=True)
ck((s.Matrix([[0,t],[t,1]])).det()==-t*t,'off-diagonal obstruction')
ck((s.Matrix([[0,1],[1,t]])).det()==-1,'boundary nonattainment')
# Infinite-dimensional caution: M e_n=(1/n)e_n, D e_n=(-1)^n e_n.
# Any nonzero rational t has a finite negative witness, while kernel compression
# and coupling to e_0 are both zero. This supports the explicit scope limit.
for a in range(-7,8):
 for b in range(1,8):
  if not a:continue
  t0=s.Rational(a,b);N=int(s.floor(1/abs(t0)))+1
  parity=1 if t0>0 else 0
  if N%2!=parity:N+=1
  ck(s.Rational(1,N)+t0*(-1)**N<0,'infinite-dimensional scope control')
receipt={'verdict':'PASS','assertions':n,'groups':groups,'artifact_sha256':sha256(Path('author_replay/PARTIAL.md').read_bytes()).hexdigest(),'independent_code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite-dimensional PSD and state distinctions; no general pure-fiber classification or infinite-dimensional extension.'}
Path('independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
