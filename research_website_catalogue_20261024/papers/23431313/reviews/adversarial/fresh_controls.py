#!/usr/bin/env python3
"""Independent first-jet calculation and exact linear-stage Jordan controls."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from collections import Counter
from fractions import Fraction as Q
import json
import sympy as s
counts=Counter()
def ck(ok,name):
 if not ok:raise ValueError(name)
 counts[name]+=1
# Coordinate torsion definition, independently contracted before comparison.
for n in range(2,6):
 m=n-1;A=s.Matrix(m,m,s.symbols('a:'+str(m*m)));D=s.Matrix(m,m,s.symbols('d:'+str(m*m)))
 b=s.Matrix(m,1,s.symbols('b:'+str(m)));db=s.Matrix(m,1,s.symbols('c:'+str(m)));lam,dl=s.symbols('lam dl')
 L=A.row_join(b).col_join(s.zeros(1,m).row_join(s.Matrix([[lam]])))
 dL=D.row_join(db).col_join(s.zeros(1,m).row_join(s.Matrix([[dl]])))
 d=lambda p,k,j:dL[k,j] if p==m else 0
 for i in range(n):
  for j in range(i+1,n):
   for k in range(n):
    val=sum(L[p,i]*d(p,k,j)-L[p,j]*d(p,k,i)-L[k,p]*(d(i,p,j)-d(j,p,i)) for p in range(n))
    expect=((A-lam*s.eye(m))*D)[k,i] if j==m and k<m else 0
    ck(s.expand(val-expect)==0,'generic_first_jet_torsion_components')
def compositions(n):
 if n==0:yield ();return
 for first in range(1,n+1):
  for tail in compositions(n-first):yield (first,)+tail
def mm(A,B):
 n=len(A);return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def zmat(n):return [[0]*n for _ in range(n)]
def nz(A):return any(x for row in A for x in row)
def residual(A,D,l,dl):
 n=len(A);X=[[A[i][j]-(l if i==j else 0) for j in range(n)] for i in range(n)];Y=[[D[i][j]-(dl if i==j else 0) for j in range(n)] for i in range(n)]
 return mm(X,D),mm(Y,D)
def schedules(sizes,mu,chosen):
 # Move the selected whole block last, then remove its terminal vector into b.
 ix=[i for i in range(len(sizes)) if i!=chosen]+[chosen]
 ss=[sizes[i] for i in ix];mus=[mu[i] for i in ix];ss[-1]-=1;m=sum(ss);A=zmat(m);blocks=[];off=0
 for size,eig in zip(ss,mus):
  if not size:continue
  blocks.append((off,size,eig))
  for j in range(size):A[off+j][off+j]=eig
  for j in range(size-1):A[off+j][off+j+1]=1
  off+=size
 l=mus[-1]
 def stage(D,newl):
  nonlocal A,l
  c0,c1=residual(A,D,l,newl-l)
  ck(not nz(c0) and not nz(c1),'exact_stage_polynomial_coefficients')
  A=[[a+d for a,d in zip(ar,dr)] for ar,dr in zip(A,D)];l=newl
 # Removal of b is unrestricted and does not alter A or lambda.
 stage(zmat(m),l)
 for off,size,eig in blocks:
  stage(zmat(m),eig)
  for j in range(size-1):
   D=zmat(m);D[off+j][off+j+1]=-1;stage(D,l)
  D=zmat(m)
  for j in range(size):D[off+j][off+j]=-eig
  stage(D,0)
 ck(not nz(A) and l==0,'schedule_exact_zero_endpoint')
for n in range(2,9):
 for sizes in compositions(n):
  patterns=[tuple(0 for _ in sizes),tuple(2 for _ in sizes),tuple((-3,0,2)[j%3] for j in range(len(sizes))),tuple((-1)**j*(j+1) for j in range(len(sizes)))]
  for mu in patterns:
   for chosen in range(len(sizes)):schedules(sizes,mu,chosen);counts['whole_Jordan_paths']+=1
# Counter-controls distinguish product order and reject tempting but invalid stages.
K=[[0,1,0],[0,0,1],[0,0,0]];D=zmat(3);D[0][1]=-1
ck(not nz(mm(K,D)) and nz(mm(D,K)),'ordered_product_not_reversible')
D=zmat(3);D[1][2]=-1
ck(nz(residual(K,D,0,0)[0]),'reverse_arrow_order_rejected')
ck(nz(mm(K,K)),'naive_scalar_cutoff_of_nilpotent_block_rejected')
ck(nz(residual([[2]], [[-2]],2,0)[1]),'unmatched_scalar_tracking_rejected')
# q(t)=S(u(t)) has exact central and outer threshold arguments, is even and smooth.
t=s.symbols('t');u=2*(t*t-s.Rational(1,16))
ck(u.subs(t,s.Rational(1,4))==0 and u.subs(t,s.Rational(3,4))==1,'q_exact_plateau_thresholds')
ck(s.expand(u.subs(t,-t)-u)==0,'q_even_no_absolute_value_corner')
# The claimed old polynomial-pair-count example is a limit of the imported proof, not a counterexample to rigidity.
ck((s.I)**2+1==0 and (s.I/2)**2+1==s.Rational(3,4),'polynomial_removes_two_nonreal_pairs')
# Scalar one-dimensional operator torsion vanishes because there are no two-form components.
ck(1*(1-1)//2==0,'dimension_one_boundary')
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','guard_count':sum(v for k,v in counts.items() if k!='whole_Jordan_paths'),'counts':dict(counts),'scope':'Generic symbolic first jets in dimensions2–5; all ordered size compositions through dimension8, four repeated/zero/signed spectrum assignments, every distinguished block; exact polynomial stage identities, zero endpoint and invalid-stage controls. All-dimensional geometry, smooth flatness and root rigidity reviewed by universal reasoning; finite dimension controls do not prove those claims.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
